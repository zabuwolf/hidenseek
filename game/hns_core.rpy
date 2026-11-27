## =============================================================================
##  TRỐN TÌM — Lõi game: nhân vật, biến, túi đồ, HUD, phòng & điểm tương tác
## =============================================================================

## ---------- Nhân vật ----------
## Lớp trưởng có 3 "giọng" theo diễn biến tâm lý: vui -> trầm -> buồn.
## callback=speaker(tag): nhân vật đang nói sẽ nhún & mấp máy môi, người khác tối đi.
define n     = Character(None, what_italic=True, what_color="#cfc6b8", callback=speaker(None))
define mv    = Character("[mai_name]", color="#ff9ec0", callback=speaker("mai"))   # vui vẻ, nghịch ngợm
define mt    = Character("[mai_name]", color="#c4a3d9", callback=speaker("mai"))   # trầm dần, gợi nhớ
define mb    = Character("[mai_name]", color="#8aa0c8", callback=speaker("mai"))   # buồn, sắp chia xa
define tho   = Character("Bác Thọ", color="#d9a441", callback=speaker("tho"))
define tung  = Character("Tùng", color="#7fd18b", callback=speaker("tung"))
define linh  = Character("Linh", color="#f2c14e", callback=speaker("linh"))
define khoa  = Character("Khoa", color="#6fb6ff", callback=speaker("khoa"))
define me    = Character("[pname]", color="#ffffff", callback=speaker("me"))
define co    = Character("Giọng cô giáo", color="#e06c6c", what_italic=True, callback=speaker(None))
define treem = Character("Tiếng trẻ con", color="#ff7a5c", what_italic=True, callback=speaker(None))

## ---------- Hiệu ứng chuyển cảnh ----------
define flash     = Fade(0.08, 0.0, 0.45, color="#ffffff")
define redflash  = Fade(0.1, 0.1, 0.9, color="#4a0000")
define blackout  = Fade(0.4, 0.8, 0.8, color="#000000")

## ---------- Biến trạng thái ----------
default mai_name   = "Mai"
default pname      = "Bin"
default mai_mood   = "vui"      # vui / tram / buon
default stage      = "mo_dau"   # dùng cho gợi ý
default hint_idx   = {}
default room_name  = ""
default tho_alert  = 0          # 0..3 — mức "bác Thọ để ý"
default inventory  = ["vong_minh"]
default memories   = []
default beads      = 0
default beads_taken = []
default flipped_article = False
default step_chap_nhan = False
default step_buong_bo  = False
default step_sieu_thoat = False

# cờ tiến trình
default f_board_read  = False
default f_drawer_open = False
default f_door_open   = False
default f_mai_found   = False
default f_key_tai_vu  = False
default f_cabinet_open = False
default f_panel_key   = False
default f_panel_done  = False
default f_has_note_3c = False
default f_3c_open     = False
default f_saw_map     = False


## ---------- Âm thanh (tự bỏ qua nếu chưa có file trong game/audio) ----------
init python:
    def sfx(name):
        f = "audio/" + name
        if renpy.loadable(f):
            renpy.sound.play(f)

    def bgm(name, fadein=1.5):
        f = "audio/" + name
        if renpy.loadable(f):
            renpy.music.play(f, loop=True, fadein=fadein)
        else:
            renpy.music.stop(fadeout=1.0)

## ---------- Túi đồ & ký ức ----------
init python:
    ITEMS = {
        "vong_minh":  ("Vòng tay chuỗi hạt của cậu",
                       "Vòng hạt cườm xanh đỏ. Hôm sinh nhật lớp trưởng, mẹ của lớp trưởng đã xâu cho mỗi đứa trong nhóm một chiếc giống hệt nhau. Không nhớ cậu đeo nó từ bao giờ."),
        "giay_mai":   ("Mẩu giấy của lớp trưởng",
                       "“Muốn ra thì tìm cái chìa khóa tròn tròn, nửa đen nửa trắng ấy. Tớ giấu trong ngăn bàn cô. Không ăn gian nhé! Lêu lêu.”"),
        "dong_xu":    ("Đồng xu âm dương",
                       "Đồng xu đồng cũ, một mặt khắc vòng âm dương. Cầm lên thấy lạnh buốt như vừa lấy từ tủ đá."),
        "chia_tai_vu":("Chìa khóa phòng tài vụ",
                       "Chùm chìa khóa có thẻ nhựa ghi “TÀI VỤ”. Thẻ nhựa bị chảy sém một góc."),
        "so_tai_vu":  ("Sổ chi tiêu phòng tài vụ",
                       "Trang 14/10 ghi: “Hỗ trợ phóng viên báo Tiếng Nói: 350. Hỗ trợ CA phường: 470. Phúng viếng: 0.” Trang cuối có dòng chữ viết vội: “Mật khẩu tủ = tổng các khoản HỖ TRỢ. Đừng để ai biết.”"),
        "bai_bao":    ("Hai bài báo cũ",
                       "“Chập điện nhỏ tại trường Tiểu học Vĩnh Ninh, không có thương vong.” — “Nhóm học sinh lớp 5A mất tích bí ẩn, gia đình vẫn mòn mỏi chờ.” Hai bài báo đăng cùng một ngày. Mặt sau hình như có gì đó cộm lên."),
        "la_bua":     ("Lá bùa vàng",
                       "Lá bùa giấy vàng, chữ son đỏ, được dán giấu sau bài báo. Có ai đó đã chuẩn bị sẵn từ trước."),
        "chia_bang_dien": ("Chìa khóa bảng điện",
                       "Chiếc chìa nhỏ lấy từ hộp đồ nghề trong tủ. Dây buộc chìa là một sợi dây điện bị cháy đen một đầu."),
        "vong_chay_1":("Chiếc vòng cháy thứ nhất",
                       "Hạt cườm chảy nhựa, dính vào nhau, nhưng vẫn nhận ra màu xanh đỏ — giống hệt chiếc vòng trên tay cậu."),
        "ban_kiem_diem": ("Bản kiểm điểm",
                       "Nét chữ chính là chữ của cậu: “Em xin hứa tối nay sẽ không ra trường chơi nữa...” Mặt sau nguệch ngoạc: “Lạc nhau thì gặp ở 3C. Ám hiệu: TẮC KÈ.”"),
        "vong_chay_2":("Chiếc vòng cháy thứ hai",
                       "Lại một chiếc vòng cháy. Lần này có khắc chữ: LINH."),
        "chu_van":    ("Mảnh gỗ hình chữ Vạn",
                       "Mảnh gỗ mít khắc chữ Vạn, cạnh đã mòn nhẵn như được ai đó cầm nắm suốt nhiều năm."),
    }

    def item_label(i):
        return ITEMS[i][0]

    def has(i):
        return i in store.inventory

    def give(i):
        if i not in store.inventory:
            store.inventory.append(i)
            renpy.notify("Nhận được: " + ITEMS[i][0])

    def take(i):
        if i in store.inventory:
            store.inventory.remove(i)

    def add_memory(t):
        if t not in store.memories:
            store.memories.append(t)
            renpy.notify("Một mảnh ký ức vừa hiện về... (Sổ ký ức)")

    def alert(k=1):
        store.tho_alert = min(3, store.tho_alert + k)

    def flip_article():
        if not store.flipped_article:
            store.flipped_article = True
            give("la_bua")

    def ceremony_text():
        def mark(b):
            return "●" if b else "○"
        return "Chấp nhận %s   Buông bỏ %s   Siêu thoát %s" % (
            mark(store.step_chap_nhan), mark(store.step_buong_bo), mark(store.step_sieu_thoat))

## ---------- Gợi ý của lớp trưởng (giọng đổi theo tâm lý) ----------
init python:
    HINTS = {
        "lop_board":  ["Ơ, các cậu xem bảng chưa? Trên bảng còn viết gì đấy.",
                       "Ngăn bàn cô có khóa số 4 chữ số. Cô toàn nhìn lên bảng rồi mới bấm."],
        "lop_drawer": ["Ngày với tháng trên bảng ấy, ghép lại thành 4 số thử xem! Hì hì."],
        "lop_coin":   ["Cửa lớp có cái khe tròn tròn, nửa đen nửa trắng. Trong túi các cậu có gì vừa với nó không?",
                       "Bấm vào đồng xu âm dương ở thanh đồ bên dưới để cầm lên, rồi bấm vào cửa lớp ấy!"],
        "san_tim_mai":["(Tiếng vọng từ xa) Tớ ở chỗ toàn sắt với bánh xe, mà chẳng cái nào chạy được, lêu lêu!",
                       "(Tiếng vọng từ xa) Kính coong! Kính coong! Nghe thấy chưa?"],
        "nhat_hat":   ["Hạt lăn khắp sân rồi huhu. Cột cờ, bể nước, nhà xe, gốc bàng, bậc thềm... xem giúp tớ với!",
                       "Chỗ phòng bác Thọ cũng có hạt đấy, nhưng đi nhẹ thôi kẻo bác dậy."],
        "cuu_mai":    ["(Vọng ra từ tài vụ) Chìa khóa treo trong phòng bác Thọ, chỗ ô cửa lùa ấy!",
                       "(Vọng ra từ tài vụ) Lúc nào bác ngáy to nhất thì mới với tay vào. Bác mà im là phải đứng im ngay!",
                       "(Vọng ra từ tài vụ) Có chìa rồi thì cầm chìa lên rồi bấm vào cửa tài vụ mở cho tớ đi!"],
        "tu_tai_lieu":["Nãy bị nhốt trong này tớ thấy cái tủ trông bí ẩn lắm. Thử lục xem có quyển sổ nào không?",
                       "Trang cuối quyển sổ có ghi mật khẩu đấy. Cộng mấy khoản “hỗ trợ” lại xem."],
        "bang_dien":  ["Cái chìa nhỏ này chắc cắm vào đâu đó... Uầy, sau cái tủ có bảng điện kìa! Cầm chìa lên rồi bấm vào bảng điện thử xem.",
                       "Hình như phải chọn một cực bên trái với một cực bên phải, cộng lại bằng số trên đồng hồ. Làm ba lần!"],
        "bi_mat_1":   ["Các cậu... nhìn kỹ góc phòng kia xem. Có thứ gì đó đang phát sáng."],
        "xep_cho":    ["Bắt đầu từ Tùng trước. Tùng chỉ có đúng một chỗ thôi.",
                       "Khoa say nắng nên không ngồi cửa sổ. Vậy Khoa chỉ còn một chỗ... rồi Linh nữa."],
        "tim_3c":     ["3C là chỗ nào nhỉ... Tớ thấy quen lắm mà không nhớ được.",
                       "Hình như ngoài sân có cái bảng quy hoạch. Hàng là số, cột là chữ.",
                       "Đến đúng chỗ rồi thì thử nói cái câu “thần chú” kia xem."],
        "ban_tho":    ["Quyển sách cầu siêu bác Thọ mang vào có ghi cách bày đấy. Làm đúng theo sách nhé.",
                       "Chữ Vạn cao nhất. Âm dương ngay dưới. Đèn bên trái, hương bên phải. Bùa ở trước."],
        "u_minh":     ["Nắm tay nhau đi các cậu. Đừng buông ra nhé."],
    }

    def get_hint():
        lst = HINTS.get(store.stage)
        if not lst:
            return "Tớ cũng không biết nữa... các cậu cứ thử xem xung quanh đi."
        i = store.hint_idx.get(store.stage, 0)
        store.hint_idx[store.stage] = min(i + 1, len(lst) - 1)
        return lst[i]

label mai_hint:
    $ hint_line = get_hint()
    if mai_mood == "vui":
        mv "[hint_line]"
    elif mai_mood == "tram":
        mt "[hint_line]"
    else:
        mb "[hint_line]"
    return

## ---------- Điểm tương tác của từng phòng ----------
## (id, nhãn, x, y, rộng, cao, điều kiện hiển thị) — khớp với đồ vật vẽ trên ảnh nền
init python:
    HOTSPOTS = {
        "lop": [
            ("bang",     "Bảng đen",                170, 165, 840, 365, "True"),
            ("ban_co",   "Bàn cô giáo",             630, 590, 490, 180, "True"),
            ("cua_so",   "Cửa sổ",                 1100, 165, 520, 355, "True"),
            ("ban_hs",   "Dãy bàn học sinh",          0, 790, 650, 290, "True"),
            ("cua_lop",  "Cửa lớp",                1655, 215, 240, 570, "True"),
        ],
        "san_tim": [
            ("cot_co",   "Cột cờ",                  840,  80, 130, 720, "True"),
            ("goc_bang", "Gốc bàng già",            120, 420, 230, 480, "True"),
            ("be_nuoc",  "Bể nước",                1050, 630, 190, 190, "True"),
            ("nha_xe",   "Nhà xe",                 1650, 595, 270, 310, "True"),
            ("bao_ve",   "Phòng bảo vệ",            410, 565, 360, 330, "True"),
            ("nha_vs",   "Nhà vệ sinh",             630, 440, 100, 160, "True"),
        ],
        "san_hat": [
            ("cot_co",   "Cột cờ",                  840,  80, 130, 720, "'cot_co' not in beads_taken"),
            ("goc_bang", "Gốc bàng già",            120, 420, 230, 480, "'goc_bang' not in beads_taken"),
            ("be_nuoc",  "Bể nước",                1050, 630, 190, 190, "'be_nuoc' not in beads_taken"),
            ("nha_xe",   "Nhà xe",                 1650, 595, 270, 310, "'nha_xe' not in beads_taken"),
            ("bac_them", "Bậc thềm lớp học",       1245, 590, 210,  70, "'bac_them' not in beads_taken"),
            ("bao_ve",   "Gần phòng bảo vệ",        410, 565, 360, 330, "'bao_ve' not in beads_taken"),
            ("quy_hoach","Dưới bảng quy hoạch",    1430, 550, 200, 255, "'quy_hoach' not in beads_taken"),
        ],
        "san_cuu": [
            ("cua_taivu","Cửa phòng tài vụ",        318, 440, 124, 165, "True"),
            ("cua_lua",  "Ô cửa lùa phòng bảo vệ",  588, 668, 154, 114, "not f_key_tai_vu"),
            ("ve_lop",   "Lớp 5A",                 1288, 440, 124, 165, "True"),
        ],
        "taivu": [
            ("lich",     "Tờ lịch trên tường",      175, 160, 160, 225, "True"),
            ("tu",       "Tủ tài liệu",             695, 255, 270, 550, "True"),
            ("bang_dien","Bảng điện",              1012, 372, 176, 216, "f_cabinet_open"),
            ("vet_khoi", "Cánh cửa ám khói",       1435, 195, 250, 630, "True"),
        ],
        "san_3c": [
            ("quy_hoach","Bảng quy hoạch",         1430, 550, 200, 255, "True"),
            ("cot_co",   "Cột cờ",                  840,  80, 130, 720, "True"),
            ("goc_bang", "Gốc bàng già",            120, 420, 230, 480, "True"),
            ("be_nuoc",  "Bể nước",                1050, 630, 190, 190, "True"),
            ("nha_xe",   "Nhà xe",                 1650, 595, 270, 310, "True"),
        ],
    }

    def hotspots(room):
        return [h for h in HOTSPOTS.get(room, []) if eval(h[6])]

    ## Đồ nào dùng được ở đâu: (điểm tương tác, món đồ)
    ITEM_USES = {("cua_lop", "dong_xu"), ("cua_taivu", "chia_tai_vu"), ("bang_dien", "chia_bang_dien")}

    def hold_item(it):
        store.held_item = None if store.held_item == it else it

    class HeldCursor(renpy.Displayable):
        """Icon món đồ đang cầm bám theo con trỏ chuột."""
        def __init__(self, **kw):
            super(HeldCursor, self).__init__(**kw)
            self.x = -500
            self.y = -500

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            it = store.held_item
            if it:
                d = Transform("images/items/%s.png" % it, zoom=0.6, alpha=0.95)
                rv.blit(renpy.render(d, width, height, st, at), (int(self.x + 14), int(self.y + 10)))
            return rv

        def event(self, ev, x, y, st):
            if (x, y) != (self.x, self.y):
                self.x, self.y = x, y
                renpy.redraw(self, 0)
            return None

    def ceremony_steps():
        return [("Chấp nhận", store.step_chap_nhan), ("Buông bỏ", store.step_buong_bo),
                ("Siêu thoát", store.step_sieu_thoat)]

define config.allow_underfull_grids = True
default held_item = None
default used = None
default used_name = ""

## ---------- Styles ----------
style ui_button:
    background Frame("gui/hns_btn_idle.png", 14, 14)
    hover_background Frame("gui/hns_btn_hover.png", 14, 14)
    selected_background Frame("gui/hns_btn_selected.png", 14, 14)
    insensitive_background Frame("gui/hns_btn_insensitive.png", 14, 14)
    padding (26, 12)
style ui_button_text:
    size 26
    color "#e8d8b0"
    hover_color "#ffffff"
    insensitive_color "#6a6058"
    selected_color "#ffe0a0"

style inv_button is ui_button:
    xfill True
style inv_button_text is ui_button_text

style hns_frame:
    background Frame("gui/hns_panel.png", 24, 24)
    padding (26, 14)

style hns_paper:
    background Frame("gui/hns_paper.png", 24, 24)
    padding (34, 28)

## ---------- HUD ----------
screen hud():
    zorder 40
    hbox:
        xpos 22
        ypos 16
        spacing 14
        frame:
            style "hns_frame"
            text "[room_name]" size 28 color "#f0dcb0"
        frame:
            style "hns_frame"
            padding (24, 16)
            hbox:
                spacing 20
                for lbl, ok in ceremony_steps():
                    hbox:
                        spacing 7
                        text ("◆" if ok else "◇") size 22 color ("#ffd27a" if ok else "#6a5a48") yalign 0.5
                        text lbl size 20 color ("#f0dcb0" if ok else "#8a7a68") yalign 0.5
    frame:
        style "hns_frame"
        xalign 1.0
        xoffset -22
        ypos 16
        padding (24, 14)
        hbox:
            spacing 10
            text "Bác Thọ để ý" size 20 color "#c8b090" yalign 0.5
            for i in range(3):
                text ("●" if i < tho_alert else "○") size 28 color ("#ff5040" if i < tho_alert else "#5a4a40") yalign 0.5

## ---------- Màn khám phá ----------
screen room_view(room):
    modal False
    default hov = None
    default fl = Flashlight()
    default hc = HeldCursor()
    default hov_item = None
    on "show" action SetVariable("exploring", True)
    on "hide" action SetVariable("exploring", False)

    for h in hotspots(room):
        button:
            xpos h[2]
            ypos h[3]
            xysize (h[4], h[5])
            background None
            hover_background Frame("gui/hs_hover.png", 30, 30)
            hovered SetScreenVariable("hov", h)
            unhovered SetScreenVariable("hov", None)
            action Return(h[0])
            add "images/fx/sparkle.png" at hs_pulse xalign 0.5 yalign 0.5

    if room == "san_hat":
        add fl
        frame:
            style "hns_frame"
            xalign 0.5
            ypos 100
            text "Mất điện! Rê chuột để soi đèn pin tìm hạt cườm  ([beads]/7)" size 24 color "#ffe0a0"

    if hov:
        frame:
            style "hns_frame"
            xpos (hov[2] + hov[4] // 2)
            xanchor 0.5
            ypos max(96, hov[3] - 62)
            padding (22, 10)
            if held_item:
                text ("Dùng " + item_label(held_item) + " → " + hov[1]) size 26 color "#ffd27a"
            else:
                text hov[1] size 26 color "#ffe8b0"

    ## món đồ đang cầm
    if held_item:
        frame:
            style "hns_frame"
            xalign 0.5
            yalign 1.0
            yoffset -140
            padding (22, 8)
            text ("Đang cầm: " + item_label(held_item) + "   (chuột phải / Esc để cất đi)") size 22 color "#ffd27a"
    elif hov_item:
        frame:
            style "hns_frame"
            xalign 0.5
            yalign 1.0
            yoffset -140
            padding (22, 8)
            text (item_label(hov_item) + "   — bấm để cầm lên") size 22 color "#e8d8b0"

    ## thanh đồ dưới đáy màn hình
    frame:
        style "hns_frame"
        xalign 0.5
        yalign 1.0
        yoffset -12
        padding (18, 12)
        hbox:
            spacing 10
            for it in inventory[-9:]:
                button:
                    xysize (92, 92)
                    background Frame("gui/hns_slot_%s.png" % ("selected" if held_item == it else "idle"), 16, 16)
                    hover_background Frame("gui/hns_slot_hover.png", 16, 16)
                    hovered SetScreenVariable("hov_item", it)
                    unhovered SetScreenVariable("hov_item", None)
                    action Function(hold_item, it)
                    add "images/items/%s.png" % it zoom 0.62 align (0.5, 0.5)
            null width 14
            vbox:
                spacing 6
                yalign 0.5
                textbutton "Túi đồ (I)" style "ui_button" text_size 20 padding (18, 6) action Show("inventory_screen")
                textbutton "Sổ ký ức (J)" style "ui_button" text_size 20 padding (18, 6) action Show("journal_screen")
            textbutton "Hỏi [mai_name] (H)" style "ui_button" text_size 22 yalign 0.5 action Return("__hint__")
    add hc
    key "i" action Show("inventory_screen")
    key "j" action Show("journal_screen")
    key "h" action Return("__hint__")
    if held_item:
        key "game_menu" action SetVariable("held_item", None)

screen inventory_screen(sel0=None):
    modal True
    zorder 100
    default sel = sel0
    add Solid("#000000c8")
    frame:
        style "hns_frame"
        xalign 0.5
        yalign 0.46
        xysize (1520, 800)
        padding (44, 36)
        vbox:
            spacing 18
            text "TÚI ĐỒ" size 44 color "#f0dcb0"
            hbox:
                spacing 40
                vpgrid:
                    cols 4
                    spacing 14
                    xsize 556
                    ysize 560
                    mousewheel True
                    for it in inventory:
                        button:
                            xysize (128, 128)
                            background Frame("gui/hns_slot_%s.png" % ("selected" if sel == it else "idle"), 16, 16)
                            hover_background Frame("gui/hns_slot_hover.png", 16, 16)
                            action SetScreenVariable("sel", it)
                            add "images/items/%s.png" % it zoom 0.85 align (0.5, 0.5)
                vbox:
                    xsize 800
                    spacing 18
                    if sel:
                        hbox:
                            spacing 24
                            frame:
                                xysize (210, 210)
                                background Frame("gui/hns_slot_idle.png", 16, 16)
                                add "images/items/%s.png" % sel zoom 1.4 align (0.5, 0.5)
                            text ITEMS[sel][0] size 36 color "#ffd28a" yalign 0.5 xmaximum 560
                        text ITEMS[sel][1] size 26 color "#e4dccc"
                        hbox:
                            spacing 16
                            textbutton "Cầm lên để dùng" style "ui_button" action [SetVariable("held_item", sel), Hide("inventory_screen")]
                            if sel == "bai_bao" and not flipped_article:
                                textbutton "Lật mặt sau bài báo" style "ui_button" action Function(flip_article)
                    else:
                        text "Chọn một món đồ để xem kỹ." size 26 color "#998a78"
                    if beads > 0 and beads < 7:
                        text ("Hạt cườm nhặt được: %d / 7" % beads) size 24 color "#ffd28a"
            textbutton "Đóng" style "ui_button" xalign 1.0 action Hide("inventory_screen")
    key "i" action Hide("inventory_screen")
    key "game_menu" action Hide("inventory_screen")

screen journal_screen():
    modal True
    zorder 100
    add Solid("#000000c8")
    frame:
        style "hns_paper"
        xalign 0.5
        yalign 0.46
        xysize (1400, 800)
        vbox:
            spacing 18
            text "SỔ KÝ ỨC" size 44 color "#5a1a40"
            viewport:
                ysize 600
                scrollbars "vertical"
                mousewheel True
                vbox:
                    spacing 16
                    if not memories:
                        text "Chưa có gì cả. Cứ như đầu óc cậu có một khoảng trống..." size 26 color "#7a6a58" italic True
                    for i, m in enumerate(memories):
                        text ("%d. %s" % (i + 1, m)) size 26 color "#2a1e14"
            textbutton "Đóng" style "ui_button" xalign 1.0 action Hide("journal_screen")
    key "j" action Hide("journal_screen")
    key "game_menu" action Hide("journal_screen")
