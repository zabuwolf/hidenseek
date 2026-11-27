## =============================================================================
##  TRỐN TÌM — Các câu đố
## =============================================================================

## ---------- 1. Khóa số (ngăn bàn cô, tủ tài vụ) ----------
screen code_lock(title, length=4, note=""):
    modal True
    zorder 90
    default code = ""
    add Solid("#000000c8")
    frame:
        xalign 0.5
        yalign 0.42
        xsize 760
        padding (44, 38)
        style "hns_frame"
        vbox:
            spacing 20
            xalign 0.5
            text title size 36 color "#e8d8b0" xalign 0.5
            if note:
                text note size 22 color "#999999" xalign 0.5 text_align 0.5
            frame:
                xalign 0.5
                xsize 420
                padding (20, 14)
                background Frame("gui/hns_slot_idle.png", 16, 16)
                text (" ".join(list(code.ljust(length, "_")))) size 56 color "#ffd28a" xalign 0.5
            grid 3 4:
                xalign 0.5
                spacing 10
                for d in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    textbutton d style "ui_button" xsize 120 text_xalign 0.5 action If(len(code) < length, SetScreenVariable("code", code + d))
                textbutton "Xóa" style "ui_button" xsize 120 text_xalign 0.5 action SetScreenVariable("code", code[:-1])
                textbutton "0" style "ui_button" xsize 120 text_xalign 0.5 action If(len(code) < length, SetScreenVariable("code", code + "0"))
                textbutton "Mở" style "ui_button" xsize 120 text_xalign 0.5 action If(len(code) == length, Return(code))
            textbutton "Thôi" style "ui_button" xalign 0.5 action Return(None)
    key "game_menu" action Return(None)

## ---------- 2. Trộm chìa khóa qua ô cửa lùa ----------
default ks_state = "ngay"
default ks_step  = 0
default ks_alert = 0

init python:
    KS_TEXT = {
        "ngay":    "Khò... khò... KHÒÒÒ... (bác Thọ ngáy rất to)",
        "lam_bam": "Ư... ừm... rượu đâu... (bác đang lẩm bẩm, cựa mình)",
        "im":      "............ (im lặng tuyệt đối)",
    }

    def ks_next():
        store.ks_state = renpy.random.choice(["ngay", "ngay", "lam_bam", "im"])

    def ks_reach():
        if store.ks_state == "ngay":
            store.ks_step += 1
            sfx("loat_xoat.ogg")
            if store.ks_step == 1:
                renpy.notify("Cậu luồn tay qua ô cửa lùa... được một đoạn.")
            elif store.ks_step == 2:
                renpy.notify("Có bàn tay lạnh buốt vừa chạm vào cổ tay cậu từ dưới gầm cửa!")
            else:
                renpy.notify("Ngón tay cậu đã móc được chùm chìa khóa!")
        else:
            store.ks_alert += 1
            sfx("ho_khan.ogg")
            renpy.notify("Bác Thọ khựng lại: “Đứa nào...?”  Cậu rụt tay về.")
            store.ks_step = max(0, store.ks_step - 1)

screen key_steal():
    modal True
    add "bg baove_cua"
    if ks_state == "ngay":
        for d in [0.0, 0.6, 1.2]:
            text "Z" size 56 color "#ffe9b0" bold True at zzz_float(340, 540, d)
    else:
        add Solid("#a00000") at red_pulse
        text ("..." if ks_state == "im" else "ư...") size 60 color "#ffb0a0" xpos 300 ypos 470
    add "images/fx/tay.png" at arm_reach(ks_step)
    if ks_step >= 2:
        add "images/fx/tay_ma.png" at ghost_hand
    timer 1.5 repeat True action Function(ks_next)
    if ks_step >= 3:
        timer 0.8 action Return("ok")
    elif ks_alert >= 3:
        timer 0.5 action Return("caught")
    vbox:
        xalign 0.5
        ypos 110
        spacing 22
        text "Ô CỬA LÙA PHÒNG BẢO VỆ" outlines [(3, "#000000")] size 44 color "#d9a441" xalign 0.5
        text "Chỉ với tay khi bác Thọ đang ngáy to. Bác im lặng hay lẩm bẩm thì phải đứng yên." size 26 color "#e0d0b0" xalign 0.5 outlines [(2, "#000000")]
        frame:
            xalign 0.5
            xsize 1300
            padding (30, 22)
            style "hns_frame"
            text KS_TEXT[ks_state] size 34 xalign 0.5 color ("#ffe9b0" if ks_state == "ngay" else "#ff7060")
    vbox:
        xalign 0.5
        yalign 0.94
        spacing 14
        hbox:
            xalign 0.5
            spacing 14
            text "Tay cậu:" size 28 color "#cccccc"
            for i in range(3):
                text ("■" if i < ks_step else "□") size 34 color "#ffd28a"
        hbox:
            xalign 0.5
            spacing 14
            text "Bác Thọ nghi ngờ:" size 28 color "#cccccc"
            for i in range(3):
                text ("●" if i < ks_alert else "○") size 34 color "#ff5040"
        textbutton "Với tay vào lấy chìa khóa" style "ui_button" xalign 0.5 text_size 34 action Function(ks_reach)

## ---------- 3. Bảng điện (3 phút, 3 mạch) ----------
default panel_round = 0
default panel_time = 180
default panel_left = None
default panel_wires = []
default panel_hush = 0
default panel_hush_done = False

init python:
    PANEL = [([1, 4, 7], [2, 5, 8], 15),
             ([2, 6, 9], [3, 5, 8], 11),
             ([4, 8, 12], [3, 9, 11], 17)]

    def panel_reset():
        store.panel_round = 0
        store.panel_time = 180
        store.panel_left = None
        store.panel_wires = []
        store.panel_hush = 0
        store.panel_hush_done = False

    def panel_pick_left(v):
        store.panel_left = v

    def panel_pick_right(v):
        if store.panel_left is None:
            renpy.notify("Chọn một cực bên trái trước đã.")
            return
        L, R, T = PANEL[store.panel_round]
        if store.panel_left + v == T:
            store.panel_wires.append("%d + %d = %d" % (store.panel_left, v, T))
            store.panel_round += 1
            sfx("tach.ogg")
            renpy.notify("Tách! Mạch số %d đã thông." % store.panel_round)
        else:
            store.panel_time = max(0, store.panel_time - 15)
            sfx("xet_dien.ogg")
            renpy.notify("Xẹt! Tia lửa bắn ra — mất 15 giây!")
        store.panel_left = None

    def panel_tick():
        if store.panel_round >= 3:
            return
        if store.panel_hush > 0:
            store.panel_hush -= 1
            return
        store.panel_time = max(0, store.panel_time - 1)
        if store.panel_time <= 100 and not store.panel_hush_done:
            store.panel_hush_done = True
            store.panel_hush = 6

screen panel_puzzle():
    modal True
    add "bg taivu"
    add Solid("#000000c0")
    timer 1.0 repeat True action Function(panel_tick)
    if panel_round >= 3:
        timer 1.0 action Return("done")
    elif panel_time <= 0:
        timer 0.3 action Return("timeout")

    vbox:
        xalign 0.5
        ypos 70
        spacing 24
        text "BẢNG ĐIỆN PHÒNG TÀI VỤ" size 46 color "#9fd3ff" xalign 0.5
        text ("%02d:%02d" % (panel_time // 60, panel_time % 60)) size 80 xalign 0.5 color ("#ff5040" if panel_time < 60 else "#ffd28a")
        if panel_round < 3:
            text ("Mạch %d / 3  —  Đồng hồ yêu cầu:  %d" % (panel_round + 1, PANEL[panel_round][2])) size 34 color "#e8e8e8" xalign 0.5
            hbox:
                xalign 0.5
                spacing 260
                vbox:
                    spacing 16
                    text "CỰC TRÁI" size 26 color "#ff9070" xalign 0.5
                    for v in PANEL[panel_round][0]:
                        textbutton str(v) style "ui_button" xsize 200 text_xalign 0.5 text_size 44 selected (panel_left == v) sensitive (panel_hush == 0) action Function(panel_pick_left, v)
                vbox:
                    spacing 16
                    text "CỰC PHẢI" size 26 color "#70b0ff" xalign 0.5
                    for v in PANEL[panel_round][1]:
                        textbutton str(v) style "ui_button" xsize 200 text_xalign 0.5 text_size 44 sensitive (panel_hush == 0) action Function(panel_pick_right, v)
        else:
            text "Cả ba mạch đã thông!" size 44 color "#80ff9a" xalign 0.5
        hbox:
            xalign 0.5
            spacing 40
            for w in panel_wires:
                text w size 26 color "#80ff9a"

    if panel_hush > 0:
        frame:
            xalign 0.5
            yalign 0.88
            padding (40, 20)
            style "hns_frame"
            text "Nín thở! Tiếng dép lê của bác Thọ đang lẹp xẹp ngang qua cửa..." size 30 color "#ffdddd"

## ---------- 4. Xếp chỗ ngồi ----------
default seats = ["", "", "", ""]

init python:
    SEAT_NAMES = ["Bàn trên — cạnh cửa sổ", "Bàn trên — phía lối đi",
                  "Bàn dưới — cạnh cửa sổ", "Bàn dưới — phía lối đi"]

    SEAT_TAGS = {"Tùng": "tung", "Linh": "linh", "Khoa": "khoa"}

    def seat_people():
        return [store.pname, "Tùng", "Linh", "Khoa"]

    def cycle_seat(i):
        opts = [""] + seat_people()
        cur = store.seats[i]
        idx = opts.index(cur) if cur in opts else 0
        store.seats[i] = opts[(idx + 1) % len(opts)]

    def seats_correct():
        return list(store.seats) == [store.pname, "Tùng", "Linh", "Khoa"]

screen seating_puzzle():
    modal True
    add "bg lop"
    add Solid("#000000b0")
    hbox:
        xalign 0.5
        ypos 70
        spacing 50
        frame:
          style "hns_frame"
          padding (30, 26)
          vbox:
            spacing 20
            xsize 760
            text "SƠ ĐỒ CHỖ NGỒI — LỚP 5A" size 38 color "#e8d8b0"
            frame:
                xsize 760
                padding (16, 12)
                background Solid("#1e3a2c")
                text "BẢNG ĐEN   |   Bàn cô ở phía lối đi   |   Cửa sổ bên trái" size 22 color "#cccccc"
            frame:
                xsize 360
                padding (16, 12)
                background Frame("gui/hns_slot_idle.png", 16, 16)
                text "Bàn lớp trưởng: VẮNG (ốm)" size 24 color "#c4a3d9"
            grid 2 2:
                spacing 20
                for i in range(4):
                    button:
                        xsize 370
                        ysize 170
                        background Frame("gui/hns_slot_idle.png", 16, 16)
                        hover_background Frame("gui/hns_slot_hover.png", 16, 16)
                        action Function(cycle_seat, i)
                        hbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 14
                            if seats[i] in SEAT_TAGS:
                                add portrait(SEAT_TAGS[seats[i]]) zoom 0.4 yalign 0.5
                            vbox:
                                yalign 0.5
                                spacing 8
                                text SEAT_NAMES[i] size 19 color "#a89878"
                                text (seats[i] if seats[i] else "— trống —") size 34 color "#ffd28a"
            text "Bấm vào từng chỗ để đổi người ngồi." size 22 color "#a89878"
        frame:
          style "hns_paper"
          vbox:
            spacing 22
            xsize 700
            text "LỜI CÔ DẶN (lớp trưởng đọc)" size 34 color "#9a1c16"
            text "1. Tùng ngồi bàn trên, phía lối đi, ngay cạnh bàn cô — để cô còn để mắt." size 27 color "#2a1e14"
            text "2. Linh và Tùng không được ngồi cùng bàn. Hai đứa ngồi cạnh nhau là cãi nhau như mổ bò." size 27 color "#2a1e14"
            text "3. Khoa say nắng, không bao giờ ngồi cạnh cửa sổ." size 27 color "#2a1e14"
            null height 30
            hbox:
                spacing 20
                textbutton "Báo cáo cô: Xếp xong rồi ạ!" style "ui_button" action Return("check")
                textbutton "Hỏi [mai_name]" style "ui_button" action Return("hint")

## ---------- 5. Bảng quy hoạch sân trường ----------
init python:
    MAP_CELLS = {
        ("A", 1): "Cổng", ("B", 1): "Phòng bảo vệ", ("D", 1): "Nhà xe",
        ("A", 2): "Lớp 5A", ("C", 2): "Cột cờ", ("D", 2): "Bể nước",
        ("A", 3): "Tài vụ", ("C", 3): "Cây bàng", ("B", 4): "Nhà vệ sinh",
        ("D", 4): "Bảng điện",
    }

screen school_map():
    modal True
    zorder 90
    add Solid("#000000d0")
    frame:
        xalign 0.5
        yalign 0.45
        style "hns_paper"
        vbox:
            spacing 14
            text "BẢNG QUY HOẠCH TRƯỜNG TIỂU HỌC VĨNH NINH" size 34 color "#3a2a10" xalign 0.5
            grid 5 5:
                spacing 6
                null
                for c in ["A", "B", "C", "D"]:
                    text c size 30 color "#8a2a10" xalign 0.5 xsize 230
                for r in [1, 2, 3, 4]:
                    text str(r) size 30 color "#8a2a10" yalign 0.5 xsize 50
                    for c in ["A", "B", "C", "D"]:
                        frame:
                            xsize 230
                            ysize 110
                            background Solid("#c8b88e")
                            text MAP_CELLS.get((c, r), "") size 24 color "#2a1e14" xalign 0.5 yalign 0.5
            text "Ai đó đã khoanh bút chì rất mờ quanh một ô, rồi lại tẩy đi." size 22 color "#6a5a40" xalign 0.5 italic True
            textbutton "Đóng" style "ui_button" xalign 1.0 action Return(True)
    key "game_menu" action Return(True)

## ---------- 6. Bày bàn thờ ----------
default altar = {"cao_giua": None, "giua": None, "trai": None, "phai": None, "truoc": None}
default altar_sel = None

init python:
    ALTAR_ITEMS = {"chu_van": "Mảnh gỗ chữ Vạn", "dong_xu": "Đồng xu âm dương",
                   "den": "Đèn cúng", "huong": "Bát hương", "bua": "Lá bùa"}
    ALTAR_ICONS = {"chu_van": "chu_van", "dong_xu": "dong_xu", "den": "den", "huong": "huong", "bua": "la_bua"}
    ALTAR_ANSWER = {"cao_giua": "chu_van", "giua": "dong_xu",
                    "trai": "den", "phai": "huong", "truoc": "bua"}
    ALTAR_SLOTS = {"cao_giua": "Cao nhất — chính giữa", "giua": "Giữa bàn",
                   "trai": "Bên tả (trái)", "phai": "Bên hữu (phải)", "truoc": "Trước án (thấp nhất)"}

    def altar_select(i):
        store.altar_sel = None if store.altar_sel == i else i

    def altar_place(slot):
        sel = store.altar_sel
        if sel is None:
            store.altar[slot] = None
            return
        for k in list(store.altar.keys()):
            if store.altar[k] == sel:
                store.altar[k] = None
        store.altar[slot] = sel
        store.altar_sel = None

    def altar_correct():
        return all(store.altar[k] == v for k, v in ALTAR_ANSWER.items())

screen altar_slot(slot, w=330):
    button:
        xsize w
        ysize 110
        background Frame("gui/hns_slot_idle.png", 16, 16)
        hover_background Frame("gui/hns_slot_hover.png", 16, 16)
        action Function(altar_place, slot)
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 10
            if altar[slot]:
                add "images/items/%s.png" % ALTAR_ICONS[altar[slot]] zoom 0.62 yalign 0.5
            vbox:
                yalign 0.5
                text ALTAR_SLOTS[slot] size 18 color "#bb9977"
                text (ALTAR_ITEMS[altar[slot]] if altar[slot] else "...") size 26 color "#ffd28a"

screen altar_puzzle():
    modal True
    add "bg phongle"
    add Solid("#000000a0")
    hbox:
        xpos 70
        ypos 70
        spacing 60
        vbox:
            spacing 22
            xsize 1060
            text "ĐÀN LỄ CẦU SIÊU" size 40 color "#ffcf70" outlines [(2, "#000000")]
            use altar_slot("cao_giua")
            hbox:
                spacing 20
                use altar_slot("trai")
                use altar_slot("giua")
                use altar_slot("phai")
            use altar_slot("truoc")
            null height 10
            text "Đồ lễ chưa bày (chọn một món, rồi bấm vào vị trí):" size 24 color "#f0d8b0" outlines [(2, "#000000")]
            hbox:
                spacing 12
                box_wrap True
                for k, v in ALTAR_ITEMS.items():
                    if k not in altar.values():
                        button:
                            style "ui_button"
                            selected (altar_sel == k)
                            action Function(altar_select, k)
                            hbox:
                                spacing 8
                                add "images/items/%s.png" % ALTAR_ICONS[k] zoom 0.42 yalign 0.5
                                text v style "ui_button_text" yalign 0.5
        frame:
            xsize 680
            style "hns_paper"
            vbox:
                spacing 14
                text "SÁCH CẦU SIÊU" size 32 color "#5a1a00" bold True
                text "— trang đánh dấu bằng sợi chỉ đỏ —" size 20 color "#7a4a20" italic True
                text "Chữ Vạn ngự nơi cao nhất, chính giữa, để Phật soi xuống." size 25 color "#2a1a0a"
                text "Âm dương hợp nhất, đặt ngay dưới chữ Vạn, giữa án thờ — người và ma không còn ngăn cách." size 25 color "#2a1a0a"
                text "Đèn soi đường đặt bên tả. Hương dẫn lối đặt bên hữu." size 25 color "#2a1a0a"
                text "Bùa trấn đặt trước án, nơi thấp nhất, giữ cho vong không lạc." size 25 color "#2a1a0a"
                null height 20
                textbutton "Bày xong — kiểm tra" style "ui_button" action Return("check")
                textbutton "Hỏi [mai_name]" style "ui_button" action Return("hint")
