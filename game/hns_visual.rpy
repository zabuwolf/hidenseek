## =============================================================================
##  TRỐN TÌM — Hình ảnh: nhân vật động, bối cảnh có hiệu ứng, đèn pin
##  Ảnh được sinh bởi tools/gen_art.ps1 (có thể thay bằng ảnh vẽ tay cùng tên file)
## =============================================================================

## Lớp "cast" nằm trên nền (master) nên lệnh scene không xóa nhân vật.
init -10 python:
    if "cast" not in config.layers:
        config.layers.insert(config.layers.index("master") + 1, "cast")

default faces = {}          # biểu cảm hiện tại: {"tung": "so", ...}
default cast_list = []      # ai đang đứng trên sân khấu
default cast_hidden = False # ẩn tạm (ký ức, cảnh đặc biệt)
default exploring = False   # đang ở màn khám phá thì nhân vật lui ra
default speaking = None
default talking = False
default saved_cast = []

init -5 python:
    import time, math

    CHAR_PHASE = {"mai": 0.0, "tung": 1.3, "linh": 2.1, "khoa": 0.7, "tho": 1.7}
    CHAR_ZOOM = {"tho": 0.8}
    CHAR_X = {}
    CHAR_A = {}
    OPEN_EYES = ("normal", "so", "buon", "tram")

    def char_base(tag):
        if tag == "mai" and store.mai_name == "Minh":
            return "minh"
        return tag

    def faces_get(tag):
        f = store.faces.get(tag)
        if f:
            return f
        if tag == "mai":
            return {"vui": "vui", "tram": "tram", "buon": "buon"}.get(store.mai_mood, "normal")
        if tag == "tho":
            return "say"
        return "normal"

    def char_dd(st, at, tag):
        ex = faces_get(tag)
        now = time.time()
        op = 0
        if store.speaking == tag and store.talking:
            ph = (now * 7.0 + CHAR_PHASE.get(tag, 0)) % 3.0
            op = 1 if ph < 1.6 else 0
        base = char_base(tag)
        d = Image("images/char/%s_%s_%d.png" % (base, ex, op))
        if tag != "tho" and ex in OPEN_EYES:
            t = (now + CHAR_PHASE.get(tag, 0) * 1.9) % 4.3
            if t < 0.13:
                d = Fixed(d, Image("images/char/%s_blink.png" % base), fit_first=True)
        return d, 0.04

    class CharFx(object):
        """Vị trí, thở, nhún khi nói, run khi sợ, tối đi khi người khác nói."""
        def __init__(self, tag, x):
            self.tag = tag
            self.x = x
            self.last = 0.0

        def __call__(self, trans, st, at):
            tag = self.tag
            now = time.time()
            dt = 0.0 if not self.last else min(0.1, now - self.last)
            self.last = now
            k = min(1.0, dt * 7.0)
            cx = CHAR_X.get(tag, self.x)
            cx += (self.x - cx) * k
            CHAR_X[tag] = cx
            target = 0.0 if (store.exploring or store.cast_hidden) else 1.0
            a = CHAR_A.get(tag, 0.0)
            a += (target - a) * min(1.0, dt * 6.0)
            if abs(a - target) < 0.01:
                a = target
            CHAR_A[tag] = a

            ph = CHAR_PHASE.get(tag, 0)
            ex = faces_get(tag)
            spk = store.speaking
            hop = 0.0
            if spk == tag and store.talking:
                hop = -abs(math.sin(now * 8.0 + ph)) * 7.0
            z = CHAR_ZOOM.get(tag, 0.74)
            trans.xpos = cx
            trans.xanchor = 0.5
            trans.ypos = 1.0
            trans.yanchor = 1.0
            trans.yoffset = int((1.0 - a) * 40 + hop + 14)
            trans.xoffset = int(math.sin(now * 45.0) * 3) if ex == "so" else 0
            trans.xzoom = z
            trans.yzoom = z * (1.0 + math.sin(now * 2.1 + ph) * 0.007)
            trans.alpha = a
            if tag == "tho" and ex == "say":
                trans.rotate = math.sin(now * 1.2 + ph) * 2.2
            else:
                trans.rotate = None
            dim = spk in store.cast_list and spk != tag and not store.cast_hidden
            trans.matrixcolor = BrightnessMatrix(-0.2) * SaturationMatrix(0.75) if dim else None
            return 0.02

    CAST_SLOTS = {1: [0.5], 2: [0.36, 0.64], 3: [0.27, 0.5, 0.73],
                  4: [0.2, 0.4, 0.6, 0.8], 5: [0.13, 0.31, 0.5, 0.69, 0.87]}

    def cast(*tags, **expr):
        """cast("mai", "tung", "linh", tung="so")  — ai đứng trên sân khấu."""
        tags = list(tags)
        removed = False
        for t in list(store.cast_list):
            if t not in tags:
                renpy.hide(t, layer="cast")
                CHAR_A.pop(t, None)
                CHAR_X.pop(t, None)
                removed = True
        xs = CAST_SLOTS.get(len(tags), [0.5])
        for t, x in zip(tags, xs):
            renpy.show(t, at_list=[Transform(function=CharFx(t, x))], layer="cast")
        store.cast_list = tags
        store.cast_hidden = False
        ex(**expr)
        if removed:
            renpy.with_statement(Dissolve(0.25))

    def ex(**expr):
        """ex(tung="so", mai=None) — đổi biểu cảm, None = về mặc định."""
        for k, v in expr.items():
            if v is None:
                store.faces.pop(k, None)
            else:
                store.faces[k] = v

    def hide_cast():
        store.cast_hidden = True

    def show_cast():
        store.cast_hidden = False

    def speaker(tag):
        def cb(event, interact=True, **kwargs):
            if event == "begin":
                store.speaking = tag
                store.talking = True
                store.exploring = False
            elif event in ("slow_done", "end"):
                store.talking = False
        return cb

    SIDE_CROP = {"tho": (130, 60, 340, 340)}
    SIDE = {}

    def side_portrait():
        t = store.speaking
        if t not in ("mai", "tung", "linh", "khoa", "tho"):
            return None
        if t in store.cast_list and not store.cast_hidden and not store.exploring:
            return None
        if t not in SIDE:
            SIDE[t] = Transform(Crop(SIDE_CROP.get(t, (90, 66, 340, 340)), DynamicDisplayable(char_dd, t)), zoom=0.88)
        return SIDE[t]

    def portrait(tag, ex="normal"):
        return Crop(SIDE_CROP.get(tag, (90, 66, 340, 340)), "images/char/%s_%s_0.png" % (tag, ex))

    ## ---------- Đèn pin theo chuột ----------
    class Flashlight(renpy.Displayable):
        def __init__(self, **kw):
            super(Flashlight, self).__init__(**kw)
            self.img = Image("images/fx/flashlight.png")
            self.x = 960
            self.y = 540

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            cr = renpy.render(self.img, width, height, st, at)
            jx = math.sin(st * 13.0) * 2.0
            rv.blit(cr, (int(self.x - 1920 + jx), int(self.y - 1080)))
            renpy.redraw(self, 0.05)
            return rv

        def event(self, ev, x, y, st):
            if (x, y) != (self.x, self.y) and x >= 0:
                self.x, self.y = x, y
                renpy.redraw(self, 0)
            return None

    def stele_names(st, at):
        return Text("Tùng\nLinh\nKhoa\n" + store.pname + "\n ", size=19, color="#d8c8a8b0",
                    text_align=0.5, line_spacing=6, xanchor=0.5, xpos=960, ypos=520), None

    ## ---------- Hạt bay ----------
    def fx_rain():
        return SnowBlossom("images/fx/rain.png", count=170, border=120, xspeed=(-160, -110), yspeed=(1300, 1700), start=0, fast=True)
    def fx_dust(n=26):
        return SnowBlossom("images/fx/dust.png", count=n, border=40, xspeed=(-18, 18), yspeed=(-14, 18), start=0, fast=True)
    def fx_embers(n=30):
        return SnowBlossom("images/fx/ember.png", count=n, border=40, xspeed=(-30, 30), yspeed=(-90, -40), start=0, fast=True)
    def fx_wisps(n=14):
        return SnowBlossom(At("images/fx/wisp.png", wisp_pulse), count=n, border=80, xspeed=(-15, 15), yspeed=(-45, -15), start=0, fast=True)
    def fx_leaves(n=14):
        return SnowBlossom(At("images/fx/leaf.png", leaf_spin), count=n, border=60, xspeed=(-60, -10), yspeed=(50, 110), start=0, fast=True)

## ---------- Transform ----------
transform fog_drift(y=760, spd=70, a=0.7):
    ypos y alpha a xpos 0
    linear spd xpos -1920
    repeat

transform fog_drift_r(y=600, spd=90, a=0.5):
    ypos y alpha a xpos -1920
    linear spd xpos 0
    repeat

transform wisp_pulse:
    alpha 0.4
    ease 1.3 alpha 1.0
    ease 1.3 alpha 0.4
    repeat

transform leaf_spin:
    rotate 0
    linear 2.0 rotate 360
    repeat

transform lightning:
    alpha 0.0
    choice:
        pause 4.0
    choice:
        pause 7.0
    choice:
        pause 11.0
    linear 0.04 alpha 0.75
    linear 0.12 alpha 0.0
    linear 0.04 alpha 0.5
    linear 0.7 alpha 0.0
    repeat

transform fluo_flicker:
    alpha 0.0
    choice:
        pause 6.0
    choice:
        pause 10.0
    linear 0.03 alpha 0.35
    linear 0.05 alpha 0.0
    linear 0.03 alpha 0.25
    linear 0.08 alpha 0.0
    repeat

transform candle_flicker:
    alpha 0.05
    choice:
        linear 0.15 alpha 0.12
    choice:
        linear 0.1 alpha 0.02
    choice:
        linear 0.2 alpha 0.09
    repeat

transform flame_a:
    yalign 1.0 alpha 1.0
    block:
        linear 0.18 alpha 0.35 yoffset 6
        linear 0.18 alpha 1.0 yoffset 0
        repeat

transform flame_b:
    yalign 1.0 alpha 0.35
    block:
        linear 0.18 alpha 1.0 yoffset -8
        linear 0.18 alpha 0.35 yoffset 0
        repeat

transform smoke_rise(x=960, y=700):
    xanchor 0.5 yanchor 0.5 xpos x ypos y alpha 0.0 zoom 0.6
    parallel:
        linear 6.0 ypos (y - 380) zoom 1.4
    parallel:
        linear 1.5 alpha 0.5
        linear 4.5 alpha 0.0
    repeat

transform beam_pulse:
    alpha 0.5
    ease 2.5 alpha 1.0
    ease 2.5 alpha 0.5
    repeat

transform hs_pulse:
    alpha 0.15 zoom 0.55
    ease 1.1 alpha 0.75 zoom 0.75
    ease 1.1 alpha 0.15 zoom 0.55
    repeat

transform ghost_float:
    yoffset 0
    ease 2.0 yoffset -14
    ease 2.0 yoffset 0
    repeat

transform ma_flicker(x=0.5):
    xalign x yalign 1.0
    alpha 0.0
    linear 0.15 alpha 0.6
    linear 0.08 alpha 0.05
    linear 0.15 alpha 0.8
    pause 0.7
    linear 0.5 alpha 0.0

transform ma_stand:
    xalign 0.5 yalign 1.0 alpha 0.0
    parallel:
        linear 1.2 alpha 0.6
    parallel:
        ease 2.0 yoffset -14
        ease 2.0 yoffset 0
        repeat

transform zzz_float(x=330, y=560, d=0.0):
    xpos x ypos y alpha 0.0 zoom 0.6
    pause d
    block:
        xpos x ypos y alpha 0.0 zoom 0.6
        parallel:
            linear 1.8 ypos (y - 160) xpos (x + 60) zoom 1.2
        parallel:
            linear 0.4 alpha 1.0
            linear 1.4 alpha 0.0
        repeat

transform arm_reach(step=0):
    ypos 300
    ease 0.45 xpos (-700 + step * 350)

transform ghost_hand:
    xpos 820 ypos 1080 alpha 0.0
    parallel:
        ease 0.9 ypos 560
    parallel:
        linear 0.5 alpha 0.9

transform red_pulse:
    alpha 0.0
    linear 0.25 alpha 0.35
    linear 0.6 alpha 0.12
    repeat

## ---------- Nhân vật ----------
image mai  = DynamicDisplayable(char_dd, "mai")
image tung = DynamicDisplayable(char_dd, "tung")
image linh = DynamicDisplayable(char_dd, "linh")
image khoa = DynamicDisplayable(char_dd, "khoa")
image tho  = DynamicDisplayable(char_dd, "tho")

image ma      = "images/char/ma.png"
image ma_het  = "images/char/ma_het.png"
image ma_chay = Transform("images/char/ma.png", matrixcolor=TintMatrix("#6a4a30") * BrightnessMatrix(-0.45))
image hoa_no  = "images/fx/hoa.png"
image toi  = Solid("#000000b0")
image khoi = At("images/fx/fog.png", fog_drift(500, 50, 0.9))

## ---------- Bối cảnh ----------
image bg cong = Fixed(
    "images/bg/cong.png",
    At("images/fx/fog.png", fog_drift(700, 80, 0.55)),
    fx_dust(14))

image bg lop = Fixed(
    "images/bg/lop.png",
    fx_dust(28),
    At(Solid("#000000"), fluo_flicker))

image bg lop_toi = Fixed(
    Transform("images/bg/lop.png", matrixcolor=TintMatrix("#7088c8") * BrightnessMatrix(-0.42)),
    fx_dust(16))

image bg san = Fixed(
    "images/bg/san.png",
    At("images/fx/fog.png", fog_drift(720, 90, 0.5)),
    fx_wisps(6))

image bg san_toi = Fixed(
    Transform("images/bg/san.png", matrixcolor=TintMatrix("#6a80c0") * BrightnessMatrix(-0.4)),
    At("images/fx/fog.png", fog_drift_r(700, 70, 0.45)),
    fx_rain(),
    At(Solid("#dfe8ff"), lightning))

image bg baove_cua = Fixed("images/bg/baove_cua.png", fx_dust(18))

image bg taivu = Fixed(
    "images/bg/taivu.png",
    fx_dust(30),
    At(Solid("#000000"), fluo_flicker))

image bg bimat = Fixed(
    "images/bg/bimat.png",
    fx_embers(22),
    At(Solid("#fff4d0"), candle_flicker))

image bg phongle = Fixed(
    "images/bg/phongle.png",
    fx_embers(18),
    At(Solid("#ff9a40"), candle_flicker),
    At("images/fx/smoke.png", smoke_rise(960, 560)),
    At("images/fx/smoke.png", smoke_rise(600, 650)))

image bg uminh = Fixed(
    "images/bg/uminh.png",
    DynamicDisplayable(stele_names),
    At("images/fx/fog.png", fog_drift(760, 90, 0.8)),
    At("images/fx/fog.png", fog_drift_r(560, 120, 0.4)),
    fx_wisps(16))

image bg ky_uc = Fixed(
    Transform("images/bg/taivu.png", matrixcolor=TintMatrix("#ff7a40") * BrightnessMatrix(-0.25)),
    At("images/fx/smoke.png", smoke_rise(700, 500)),
    At("images/fx/smoke.png", smoke_rise(1300, 600)),
    At("images/fx/lua1.png", flame_a),
    At("images/fx/lua2.png", flame_b),
    fx_embers(50))

image bg sang = Fixed("images/bg/sang.png", fx_leaves(12))
image bg den  = Solid("#000000")
