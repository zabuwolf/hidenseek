## =============================================================================
##  TRỐN TÌM — Kịch bản chính
##  Lễ cầu siêu 3 bước: CHẤP NHẬN -> BUÔNG BỎ -> SIÊU THOÁT
##  Tâm lý lớp trưởng: vui (mv) -> trầm dần (mt) -> buồn (mb)
## =============================================================================

label start:
    scene bg den
    $ bgm("bg_phase1.ogg")
    n "Có những trò chơi tưởng như đã kết thúc từ rất lâu rồi."
    n "Nhưng có một ván trốn tìm... vẫn chưa ai đếm xong."

    menu:
        n "Lớp trưởng lớp 5A của các cậu tên là gì?"
        "Mai":
            $ mai_name = "Mai"
        "Minh":
            $ mai_name = "Minh"

    $ name_in = renpy.input("Còn cậu, cậu tên là gì?", default="Bin", length=12).strip()
    if not name_in or name_in in ("Tùng", "Linh", "Khoa", "Mai", "Minh"):
        $ name_in = "Bin"
    $ pname = name_in

    jump act1_cong

label wrong_item:
    $ used_name = item_label(used)
    n "Dùng [used_name] ở đây chẳng có tác dụng gì."
    return

## ---------------------------------------------------------------------------
##  HỒI 1 — CỔNG TRƯỜNG
## ---------------------------------------------------------------------------
label act1_cong:
    $ room_name = "Cổng trường"
    scene bg cong with blackout
    show screen hud
    $ cast("tung", "linh", "khoa", tung="so", linh="vui")
    n "Mười giờ đêm. Cậu, Tùng, Linh và Khoa đứng trước cổng trường Tiểu học Vĩnh Ninh."
    n "Không ai nhớ rõ mình đã đi tới đây bằng đường nào. Chỉ nhớ là... đã hẹn nhau."
    tung "Tối thế này... hay thôi về đi các cậu."
    linh "Sợ thì về đi, Tùng nhát cáy!"
    khoa "Suỵt. Trong chòi bảo vệ có tiếng người."
    tho "Khụ... khụ... Đứa nào lảng vảng ngoài đấy? Đêm hôm không về nhà ngủ đi, ra ngoài kia mà chơi!"
    n "Tiếng quát lè nhè rồi tắt hẳn. Một tiếng chai thủy tinh lăn trên nền xi măng."

    $ sfx("hu.ogg")
    $ cast("tung", "mai", "linh", "khoa", tung="so", linh="so", khoa="so", mai="vui")
    mv "HÙUUUUUUUUU!" with vpunch
    tung "ÁÁÁÁ!"
    $ ex(linh="vui", khoa=None)
    mv "Hahaha! Mặt Tùng trắng bệch kìa! Trèo vào trường đi, nhanh lên!"
    n "[mai_name] — lớp trưởng của các cậu — ngồi vắt vẻo trên bờ tường, giơ cổ tay đeo chiếc vòng hạt cườm xanh đỏ."
    $ ex(mai="tram", tung=None)
    mv "Eeeee sao các cậu đến muộn thế, tớ đợi ở đây muỗi chích hết cả người rồi này!"
    mv "Tớ không biết đâu, tớ dỗi rồi. Phải khao tớ ăn kem thì tớ mới hết giận!"

    menu:
        "Ừ, chơi xong tớ khao cậu kem.":
            mv "Hứa rồi đấy nhé! Ngoéo tay! Không được nuốt lời đâu!"
        "Kem gì, đến muộn có tí thôi mà.":
            mv "Hứ! Thế thì tớ dỗi tiếp. ...Thôi được, nhưng chơi xong vẫn phải khao đấy."

    $ ex(mai=None)
    mv "Các cậu nhớ hôm nay mình đến trường làm gì không? Chơi trốn tìm đấy! Hẹn nhau ra đây mà không nhớ à."
    khoa "Trốn tìm... ở trường... ban đêm. Ừ, hình như là thế thật."
    mv "Mà các cậu nghe đồn gì chưa? Chưa à? Buổi đêm ý... trường mình..."
    $ ex(tung="so", linh=None)
    mv "...có ma đấyyyyy. Ai sợ thì đi về nhé!"
    tung "Tớ... tớ không sợ!"
    n "Cả bọn lần lượt trèo qua bờ tường. Tay ai cũng lạnh ngắt."
    jump act2_lop

## ---------------------------------------------------------------------------
##  HỒI 2 — LỚP 5A: BỊ NHỐT, TÌM ĐỒNG XU ÂM DƯƠNG
## ---------------------------------------------------------------------------
label act2_lop:
    $ room_name = "Lớp 5A"
    scene bg lop with blackout
    $ cast("tung", "mai", "linh", "khoa", tung=None, linh=None, khoa=None, mai=None)
    mv "Các cậu đến muộn rồi nên phải nghe tớ nhé. Tớ trốn trước, xong các cậu trốn. Ok?"
    mv "Vào lớp úp mặt lên bảng mà đếm. Đếm chậm thôi, cấm được ti hí, nhớ chưa?"
    mv "À, nhẹ nhàng thôi nhé. Bác bảo vệ khó tính lắm. Bác ấy mà bắt được là đi đời cả lũ."
    n "Cả bọn úp mặt lên bảng. Một... hai... ba..."
    $ cast("tung", "linh", "khoa")
    $ sfx("cua_dong.ogg")
    n "CẠCH. Tiếng then cửa sập lại từ bên ngoài." with hpunch
    mv "(Từ ngoài cửa) Hihi, tớ khóa cửa rồi. Muốn ra thì tự tìm cách nhé, tớ để lại lời nhắn trên bàn cô đấy!"
    $ ex(tung="so")
    tung "Cái... cái gì? Nhốt bọn mình lại á?"
    $ give("giay_mai")
    $ stage = "lop_board"
    jump lop_loop

label lop_loop:
    call screen room_view("lop")
    $ act = _return
    $ used = held_item
    $ held_item = None
    if act == "__hint__":
        if f_drawer_open:
            $ stage = "lop_coin"
        elif f_board_read:
            $ stage = "lop_drawer"
        call mai_hint
    elif used and (act, used) not in ITEM_USES:
        call wrong_item
    elif act == "bang":
        $ f_board_read = True
        n "Trên bảng, nét phấn đã nhòe nhưng vẫn đọc được:"
        n "“Thứ Sáu, ngày 14 tháng 10.  Sĩ số: 5.  Vắng: 1 — lớp trưởng (ốm).”"
        linh "Ơ... sao bảng vẫn còn chữ từ hôm nào thế này. Không ai lau à?"
        khoa "Sĩ số 5. Năm đứa mình. Vắng lớp trưởng..."
        $ add_memory("Trên bảng lớp 5A: “Thứ Sáu, ngày 14 tháng 10. Vắng: lớp trưởng (ốm).” Nét phấn này... trông quen quá.")
    elif act == "ban_co":
        if f_drawer_open:
            n "Ngăn bàn cô đã mở. Bên trong chỉ còn mấy viên phấn gãy."
        else:
            n "Ngăn kéo bàn cô khóa bằng một ổ khóa số 4 chữ số."
            call screen code_lock("NGĂN KÉO BÀN CÔ", 4, "Cô giáo hay nhìn lên bảng rồi mới bấm mã.")
            if _return == "1410":
                $ f_drawer_open = True
                $ sfx("mo_khoa.ogg")
                n "Tách! Ngăn kéo bật mở."
                $ give("dong_xu")
                n "Bên trong là một đồng xu đồng khắc hình âm dương, lạnh buốt như vừa lấy ra từ tủ đá."
                $ stage = "lop_coin"
                # --- DJ 4.0: luồng dọa ma trong lớp ---
                $ sfx("cuoi_doa.ogg")
                scene bg lop_toi with flash
                $ hide_cast()
                show ma at ma_flicker(0.82)
                n "Đèn phụt tắt. Ngoài cửa sổ có tiếng cười khúc khích của rất nhiều đứa trẻ."
                hide ma
                $ show_cast()
                $ ex(linh="so", tung="khoc", khoa="so")
                linh "ÁÁÁ! Có... có cái gì đứng ở cửa sổ!"
                tung "Tớ muốn về... tớ muốn về..."
                scene bg lop with flash
                $ ex(linh=None, tung="so", khoa=None)
                n "Đèn sáng trở lại. Cửa sổ trống trơn."
                n "(Mẹo: bấm vào một món ở thanh đồ phía dưới để cầm lên, rồi bấm vào chỗ muốn dùng nó.)"
            elif _return is not None:
                $ sfx("sai.ogg")
                n "Ổ khóa không nhúc nhích."
    elif act == "cua_so":
        n "Ngoài cửa sổ là sân trường tối om. Gốc bàng già đứng im lìm như một người đang chờ ai."
        if f_drawer_open:
            n "Trên mặt kính còn in mấy dấu bàn tay nhỏ xíu... ở phía bên ngoài."
    elif act == "ban_hs":
        n "Năm chiếc bàn gỗ. Trên một mặt bàn có khắc nguệch ngoạc: “5A mãi mãi là bạn”."
        khoa "Đây là chỗ của tớ thì phải. Tớ nhớ cái vết khắc này."
    elif act == "cua_lop":
        if used != "dong_xu":
            n "Cửa khóa then từ bên ngoài. Cạnh tay nắm có một cái khe tròn kỳ lạ, nửa đen nửa trắng."
            if has("dong_xu"):
                n "Cái khe này... trông vừa khít với một thứ gì đó trong túi đồ."
        else:
            n "Cậu ấn đồng xu âm dương vào khe tròn. Nó khớp hoàn hảo."
            $ sfx("mo_cua.ogg")
            n "Két... Then cửa bên ngoài tự trượt ra."
            n "Cậu rút đồng xu lại. Có cảm giác nó còn cần dùng đến."
            $ f_door_open = True
            jump act3_san_tim
    jump lop_loop

## ---------------------------------------------------------------------------
##  HỒI 3 — SÂN TRƯỜNG: TÌM LỚP TRƯỞNG
## ---------------------------------------------------------------------------
label act3_san_tim:
    $ room_name = "Sân trường"
    scene bg san with blackout
    $ cast("tung", "linh", "khoa", tung=None, linh="vui", khoa=None)
    $ stage = "san_tim_mai"
    mv "(Tiếng vọng từ đâu đó) Đố các cậu tìm được tớ đấy, lêu lêu!"
    n "Cẩn thận: đi lung tung sẽ gây tiếng động. Bác Thọ mà để ý đủ ba lần là bác sẽ đi tuần ra đây."
    $ wrong_count = 0
    jump san_tim_loop

label san_tim_loop:
    if tho_alert >= 3:
        call tho_patrol
    call screen room_view("san_tim")
    $ act = _return
    $ used = held_item
    $ held_item = None
    if act == "__hint__":
        call mai_hint
    elif used:
        call wrong_item
    elif act == "nha_xe":
        jump mai_found
    elif act == "bao_ve":
        $ alert(2)
        n "Cậu rón rén đến gần phòng bảo vệ. Mùi rượu nồng nặc. Bên trong có tiếng ngáy, rồi đột nhiên im bặt."
        tho "...Đứa nào?"
        n "Cậu lùi lại, tim đập thình thịch."
    else:
        $ alert(1)
        $ wrong_count += 1
        if act == "cot_co":
            n "Sau cột cờ chẳng có ai. Lá cờ rũ xuống, ướt sũng như vừa qua một cơn mưa."
        elif act == "goc_bang":
            n "Gốc bàng có một cái hốc sâu bị đóng ván kín. Không có ai trốn ở đây."
            khoa "Gốc cây này... sao tớ thấy như mình từng ngồi đây rất lâu."
        elif act == "be_nuoc":
            n "Bể nước tĩnh lặng. Mặt nước phản chiếu bốn cái bóng... à không, là năm? Cậu nhìn lại — vẫn là bốn."
        elif act == "nha_vs":
            n "Nhà vệ sinh tối om, vòi nước nhỏ giọt tí tách. Không có ai."
        if wrong_count == 1:
            mv "(Tiếng vọng) Tớ ở đây này, giỏi ra đây mà tìm, hahaha!"
        elif wrong_count == 2:
            mv "(Tiếng vọng) Chỗ tớ toàn sắt với bánh xe, mà chẳng cái nào chạy được đâu nhé!"
        else:
            mv "(Tiếng vọng) Lâu thế! Nhanh không tớ về bây giờ, hừm! Kính coong! Kính coong!"
    jump san_tim_loop

label tho_patrol:
    $ sfx("dep_le.ogg")
    scene bg san_toi with flash
    $ saved_cast = list(cast_list)
    $ cast("tho", tho="say")
    n "Cửa phòng bảo vệ bật mở. Bác Thọ lảo đảo bước ra, một tay cầm chai rượu, tay kia huơ loạn xạ vào không khí."
    tho "♪ Trường làng tôi... có cây bàng già... ♪  Hức."
    tho "Lại là chúng mày. Tại sao chúng mày không tha cho tao?"
    tho "Chúng mày nhìn tao như thế này mà vẫn còn quấy rầy? Chúng mày muốn tao phải chết mới vừa lòng hay sao?"
    menu:
        "Nín thở, đứng im như tượng.":
            n "Bác Thọ đi ngang qua cậu, gần đến mức cậu thấy rõ đôi mắt bác — đục trắng, không còn con ngươi."
            n "Bác không nhìn thấy gì cả. Bác chỉ lẩm bẩm rồi quay vào."
        "Chạy thật nhanh ra sau cột cờ.":
            n "Cậu vấp phải cái gì đó — một đoạn dây điện cũ nằm vắt ngang lối đi — rồi ngã sóng soài."
            n "Bác Thọ quay phắt về phía tiếng động, vung tay chụp vào khoảng không, rồi bật khóc nức nở."
            $ ex(tho="khoc")
            tho "Đừng chạy... đừng chạy nữa mà... đừng vào cái phòng đấy..."
            $ add_memory("Cảm giác vấp phải một sợi dây điện, ngã nhào... Hình như chuyện này đã xảy ra một lần rồi.")
    $ cast(*saved_cast)
    $ ex(tho=None)
    n "Cửa phòng bảo vệ đóng lại. Tiếng ngáy lại vang lên."
    $ tho_alert = 0
    scene bg san with flash
    return

label mai_found:
    $ f_mai_found = True
    $ cast("tung", "mai", "linh", "khoa", mai="vui", linh=None)
    n "Sau dãy xe đạp gỉ sét, [mai_name] đang ngồi bó gối, bấm chuông xe kính coong."
    mv "Mãi mới tìm ra tớ, kém thế!"
    mv "Giờ đến lượt tớ đi tìm nhé. Các cậu trốn đi. Chỗ này tớ thuộc như lòng bàn tay, trốn cho kỹ vào!"
    n "[mai_name] úp mặt vào cột cờ đếm to. Cả bọn tản ra."
    menu:
        n "Cậu trốn ở đâu?"
        "Sau bể nước":
            $ hide_spot = "bể nước"
        "Trong nhà vệ sinh":
            $ hide_spot = "nhà vệ sinh"
        "Dưới gầm cầu thang":
            $ hide_spot = "gầm cầu thang"
    n "Cậu nín thở trốn ở [hide_spot]. Chưa đầy một phút sau..."
    mv "Tìm thấy rồi nhaaaa! [pname] ở [hide_spot]!"
    n "Lần lượt từng đứa bị lôi ra. Tùng sau thùng rác, Linh trên cây, Khoa trong lớp. Cứ như [mai_name] biết trước chỗ của từng người."
    khoa "Sao cậu tìm nhanh thế?"
    mv "Thì tớ đã bảo rồi, chỗ này tớ thuộc như lòng bàn tay. Thua rồi thì mua kem cho tớ đi, la là lá la là~"
    n "[mai_name] nắm lấy tay cả bọn, vừa nhảy chân sáo vừa hát."

    # --- DJ 7.0: sấm + chuỗi hạt rơi ---
    $ sfx("sam.ogg")
    scene bg san_toi with flash
    $ ex(mai="so", tung="so", linh="so", khoa="so")
    n "ẦM! Một tiếng sấm xé toạc bầu trời. Đèn sân trường phụt tắt." with vpunch
    $ sfx("hat_roi.ogg")
    n "Lách tách... lách tách... Tiếng hạt cườm rơi lăn khắp mặt sân."
    mv "Ơ... cái vòng tay của tớ! Nó đứt rồi! Hạt rơi đâu hết rồi?!"
    $ ex(mai="khoc", tung=None, linh=None, khoa=None)
    mv "Tìm giúp tớ đi huhuhu... Cái vòng quan trọng lắm. Hôm sinh nhật tớ, mẹ tớ xâu cho cả nhóm mình mỗi đứa một chiếc giống hệt nhau đấy."
    mv "Mất nó là... là tớ không còn gì để nhớ các cậu nữa đâu."
    n "Giọng [mai_name] run lên — một nỗi hoảng hốt thật sự, khác hẳn mấy trò đùa lúc nãy."
    jump act3_nhat_hat

## ---------------------------------------------------------------------------
##  HỒI 3B — NHẶT 7 HẠT CƯỜM (luồng dọa ma ngoài sân)
## ---------------------------------------------------------------------------
label act3_nhat_hat:
    $ room_name = "Sân trường (mất điện)"
    $ stage = "nhat_hat"
    $ tho_alert = 0
    jump nhat_hat_loop

label nhat_hat_loop:
    if beads >= 7:
        jump nhat_hat_xong
    if tho_alert >= 3:
        call tho_patrol
        scene bg san_toi
    call screen room_view("san_hat")
    $ act = _return
    $ used = held_item
    $ held_item = None
    if act == "__hint__":
        call mai_hint
        jump nhat_hat_loop
    if used:
        call wrong_item
        jump nhat_hat_loop
    $ beads_taken.append(act)
    $ beads += 1
    $ sfx("nhat_hat.ogg")
    if act == "bao_ve":
        $ alert(2)
        n "Một hạt cườm nằm ngay sát bậc cửa phòng bảo vệ. Cậu nhặt lên — bên trong có tiếng trở mình."
    elif act == "goc_bang":
        n "Hạt cườm mắc trong khe ván đóng kín hốc cây. Trên ván có ai khắc mờ hai chữ cái: “3C”."
        $ add_memory("Trên tấm ván đóng kín hốc cây bàng có khắc “3C”.")
    elif act == "quy_hoach":
        n "Hạt cườm nằm dưới chân tấm bảng quy hoạch trường. Tấm bảng chia sân trường thành những ô vuông có chữ và số."
        $ f_saw_map = True
    else:
        n "Cậu mò được một hạt cườm. ([beads]/7)"
    if beads == 4:
        # --- DJ 8.0: dọa ma tiếng hét ---
        $ sfx("tieng_het.ogg")
        $ hide_cast()
        show ma_het at ma_flicker
        n "Một bóng trắng đứng ngay giữa sân. Nó không có chân. Nó đang nhìn thẳng vào cậu." with vpunch
        hide ma_het
        $ show_cast()
        $ ex(linh="so", tung="so", mai="normal")
        linh "ÁÁÁÁÁÁÁ!!!"
        tung "MA! MA THẬT!"
        mv "Ủa sao các cậu hét ầm lên thế, làm tớ giật cả mình. Bé cái mồm thôi, không ông Thọ ra bây giờ!"
        n "[mai_name] nói như thể không hề nhìn thấy gì. Hoặc là... đã quá quen với việc nhìn thấy."
        $ ex(linh=None, tung=None, mai="khoc")
    jump nhat_hat_loop

label nhat_hat_xong:
    $ room_name = "Sân trường"
    scene bg san with flash
    $ ex(mai="vui", tung=None, linh=None, khoa=None)
    n "Đèn sân trường bật sáng trở lại."
    mv "Đủ bảy hạt rồi! Ôi may quá, cái vòng đây rồi! Cảm ơn các cậu nhé!"
    n "[mai_name] ngồi xâu lại chuỗi hạt, rồi đeo vào tay. Rồi bỗng đứng phắt dậy, nói thật to:"
    mv "Giờ mình chơi tiếp đi! Trốn tìm chán rồi, chơi BỊT MẮT BẮT DÊ đi! AI BỊ BẮT PHẢI KHAO KEM NHÉÉÉ!"
    $ ex(khoa="so")
    khoa "Suỵt! Cậu nói to thế bác Thọ nghe thấy bây giờ!"
    jump act4_bat_mai

## ---------------------------------------------------------------------------
##  HỒI 4 — BÁC THỌ BẮT LỚP TRƯỞNG, CỨU NGƯỜI
## ---------------------------------------------------------------------------
label act4_bat_mai:
    $ sfx("cua_bat.ogg")
    $ cast("mai", "tho", mai="so", tho="say", khoa=None)
    n "Cửa phòng bảo vệ bật tung. Bác Thọ lao ra, nhanh một cách khó tin với một người mù." with vpunch
    tho "Đứa nào đây? Con nhà ai? Tại sao đêm hôm vào phá phách trường lớp?!"
    n "Bàn tay chai sạn chụp trúng cổ tay [mai_name] — ngay chỗ chiếc vòng hạt cườm."
    $ ex(mai="khoc")
    mv "Cháu xin lỗi bác, cháu lỡ dại! Bác ơi bác tha cho cháu, cháu đến trường lấy đồ để quên thôi mà!"
    tho "Mày còn đi với ai nữa không? Tao nghe thấy nhiều tiếng động lắm!"
    mv "Cháu đi một mình thôi ạ! Một mình thôi! Bác đừng báo thầy cô, đừng báo bố mẹ cháu, không cháu chết mất!"
    tho "Mày đi vào đây ngay. Tao sẽ báo cho bố mẹ mày biết. Học hành không học, chỉ giỏi phá!"
    $ ex(mai="buon")
    n "Trong một thoáng, [mai_name] khựng lại khi bác Thọ quát “con nhà ai”. Gương mặt lớp trưởng chùng xuống, như vừa bị ai tát."
    n "Rồi cánh cửa phòng tài vụ đóng sầm lại sau lưng [mai_name]. Tiếng khóa lách cách."
    $ cast("tung", "linh", "khoa", tung="so", linh="so", mai="khoc")
    $ mai_mood = "vui"
    $ stage = "cuu_mai"
    $ room_name = "Sân trường"
    mv "(Từ trong tài vụ) Các cậu cứu tớ với! Ông ấy báo về nhà thì bố mẹ tớ đánh chết!"
    mv "(Từ trong tài vụ) Tớ ở trong này sợ lắm huhuhu... Chìa khóa ở trong phòng ông ấy đấy, các cậu tìm cách lấy trộm rồi ra mở cho tớ với, nhanh lên!"
    jump cuu_loop

label cuu_loop:
    call screen room_view("san_cuu")
    $ act = _return
    $ used = held_item
    $ held_item = None
    if act == "__hint__":
        call mai_hint
    elif used and (act, used) not in ITEM_USES:
        call wrong_item
    elif act == "ve_lop":
        n "Không được. Không thể bỏ [mai_name] lại một mình được."
    elif act == "cua_taivu":
        if used != "chia_tai_vu":
            n "Cửa tài vụ khóa chặt. Bên trong vọng ra tiếng sụt sịt."
            mv "Nhanh lên mà... trong này tối lắm..."
            if f_key_tai_vu:
                n "Chùm chìa khóa lấy trộm được vẫn nằm trong túi đồ."
        else:
            n "Cậu tra chìa vào ổ. Cạch."
            jump act5_tai_vu
    elif act == "cua_lua":
        n "Ô cửa lùa phòng bảo vệ hé một khe. Chùm chìa khóa treo trên thanh gỗ, cách tay cậu hơn một sải."
        $ ks_state = "ngay"
        $ ks_step = 0
        $ ks_alert = 0
        call screen key_steal
        if _return == "ok":
            $ f_key_tai_vu = True
            $ give("chia_tai_vu")
            n "Cậu rút tay ra, nắm chặt chùm chìa khóa. Trên cổ tay cậu hằn năm vết ngón tay nhỏ xíu, đỏ ửng."
            $ ex(tung="so", linh="so")
            tung "Cái... cái gì nắm tay cậu thế?"
            n "Không ai trả lời."
        else:
            tho "ĐỨA NÀO?! Lại là chúng mày phải không?!"
            n "Một chai rượu bay vèo qua ô cửa, vỡ tan dưới chân cậu. Cả bọn nép sát vào tường cho đến khi tiếng ngáy vang lên lại."
            n "(Thử lại khi đã bình tĩnh.)"
    jump cuu_loop

## ---------------------------------------------------------------------------
##  HỒI 5 — PHÒNG TÀI VỤ: TỦ TÀI LIỆU & BẢNG ĐIỆN
## ---------------------------------------------------------------------------
label act5_tai_vu:
    $ room_name = "Phòng tài vụ"
    $ sfx("mo_cua.ogg")
    scene bg taivu with blackout
    $ cast("tung", "linh", "khoa", tung=None, linh=None, khoa=None)
    n "Cửa mở. Bên trong tối đen. Không thấy [mai_name] đâu."
    $ sfx("hu.ogg")
    $ cast("tung", "mai", "linh", "khoa", mai="vui", tung="so", linh="so")
    mv "HÙ! TA LÀ MA ĐÂY!" with vpunch
    tung "ÁÁÁÁÁÁ!"
    mv "Hahahaha! Ai bảo các cậu lâu quá, tớ chả có gì làm nên hù các cậu chơi!"

    # --- DJ 14.0: cutscene tài vụ ---
    $ hide_cast()
    scene bg ky_uc with redflash
    $ sfx("cutscene_taivu.ogg")
    treem "Khói! Khói ở đâu ra thế này?!"
    treem "Cửa kẹt rồi! Không mở được! Bác ơi! Bác Thọ ơi cứu bọn cháu với!"
    n "Tiếng ai đó đập cửa thình thịch từ bên ngoài. Tiếng một người đàn ông gào lên khản đặc."
    scene bg taivu with redflash
    $ show_cast()
    $ ex(tung="so", linh="so", mai=None)
    n "Rồi tất cả biến mất. Chỉ còn mùi khét thoang thoảng."
    $ add_memory("Trong phòng tài vụ: khói, cánh cửa bị kẹt, tiếng bác Thọ đập cửa từ bên ngoài.")
    linh "Các cậu... có nghe thấy không?"
    mv "Nghe thấy gì cơ? Thôi, nãy bị nhốt trong này tớ thấy cái tủ kia trông bí ẩn lắm. Thử mở ra xem có gì bên trong nào?"
    $ stage = "tu_tai_lieu"
    jump taivu_loop

label taivu_loop:
    call screen room_view("taivu")
    $ act = _return
    $ used = held_item
    $ held_item = None
    if act == "__hint__":
        call mai_hint
    elif used and (act, used) not in ITEM_USES:
        call wrong_item
    elif act == "lich":
        n "Tờ lịch bóc treo trên tường dừng ở một ngày duy nhất: Thứ Sáu, 14 tháng 10. Không ai xé thêm tờ nào nữa."
        n "Mép tờ lịch xém đen."
    elif act == "vet_khoi":
        n "Mặt trong cánh cửa có những vết cào nhỏ, chi chít, ở độ cao ngang ngực một đứa trẻ lớp 5."
        n "Cậu giơ tay mình lên đặt vào. Vừa khít."
        $ add_memory("Những vết cào bên trong cửa tài vụ vừa khít với bàn tay cậu.")
    elif act == "tu":
        if not has("so_tai_vu"):
            n "Ngăn trên cùng không khóa. Bên trong có một quyển sổ chi tiêu bìa xanh."
            $ give("so_tai_vu")
            mv "Này có quyển sổ gì lạ không này... “Hỗ trợ phóng viên”, “hỗ trợ công an phường”... “phúng viếng: 0”? Nghĩa là sao nhỉ?"
            mv "Ơ trang cuối có ghi mật khẩu kìa."
            $ stage = "tu_tai_lieu"
            $ hint_idx["tu_tai_lieu"] = 1
        elif not f_cabinet_open:
            n "Ngăn dưới tủ khóa bằng ổ khóa số 3 chữ số."
            call screen code_lock("TỦ TÀI LIỆU", 3, "Xem lại quyển sổ chi tiêu trong túi đồ.")
            if _return == "820":
                $ f_cabinet_open = True
                $ sfx("mo_khoa.ogg")
                n "Cạch. Ngăn tủ trượt ra."
                $ give("bai_bao")
                n "Hai bài báo cũ được gấp cẩn thận."
                mv "Mấy bài báo này á? Tớ chỉ biết hồi trước có một nhóm học sinh bị mất tích thôi, cũng không biết gì thêm..."
                $ ex(mai="tram")
                n "[mai_name] nói nhanh quá, mắt không nhìn vào ai."
                n "Dưới đáy ngăn là một hộp đồ nghề. Trong hộp có chiếc chìa khóa nhỏ buộc bằng một sợi dây điện cháy đen."
                $ give("chia_bang_dien")
                $ ex(mai=None, tung=None, linh=None)
                mv "Cái chìa khóa này để làm gì nhỉ? Tìm chỗ cắm nó vào xem... Uầy, đằng sau cái tủ có cái bảng điện này!"
                $ stage = "bang_dien"
                $ bgm("bg_phase2.ogg")
                n "(Mẹo: mở Túi đồ và xem kỹ bài báo — mặt sau có gì đó.)"
            elif _return is not None:
                $ sfx("sai.ogg")
                n "Sai rồi. Ổ khóa kêu “tạch” một tiếng khô khốc."
        else:
            n "Tủ tài liệu đã mở. Không còn gì bên trong."
    elif act == "bang_dien":
        if f_panel_done:
            n "Bảng điện đã thông mạch."
        elif used != "chia_bang_dien":
            n "Một bảng điện cũ, cửa khóa bằng một ổ khóa nhỏ xíu. Mép bảng ám khói đen."
        else:
            n "Cậu tra chìa vào ổ. Mặt bảng điện bật mở, đồng hồ đếm ngược nhảy số: 03:00."
            mv "Uầy, đếm giây kìa! Hết 3 phút liệu nó có nổ không nhỉ? Thử cắm mấy cái dây điện này vào xem!"
            jump panel_try
    jump taivu_loop

label panel_try:
    $ panel_reset()
    call screen panel_puzzle
    if _return == "done":
        $ f_panel_done = True
        $ sfx("cua_mo_mat.ogg")
        n "Cả ba mạch sáng xanh. Đồng hồ dừng lại."
        mv "Khiếp, tò mò thế, không hiểu làm xong thì chuyện gì xảy ra nữa..."
        n "Rầm rầm rầm. Bức tường sau tủ tài liệu từ từ trượt sang một bên."
        mv "Ủa... có cái cửa bí mật này. Vào thử xem nào."
        $ ex(mai="tram")
        mt "Các cậu... vào trước đi. Tớ vào sau."
        jump act6_bi_mat
    else:
        $ sfx("chap_dien.ogg")
        $ hide_cast()
        $ ex(khoa="khoc")
        scene bg ky_uc with redflash
        n "XẸT! Tia lửa bắn tung tóe. Khói đen cuộn lên từ bảng điện." with vpunch
        khoa "Không... không... lại thế này nữa... là tớ... là tại tớ vấp phải..."
        $ add_memory("Khoa: “Lại thế này nữa... là tại tớ vấp phải...” Tia lửa, khói đen từ ổ điện.")
        scene bg taivu with flash
        $ show_cast()
        $ ex(khoa="buon")
        n "Đèn bảng điện nhấp nháy rồi khởi động lại. Đồng hồ trở về 03:00."
        mv "Thử lại đi các cậu! Lần này bình tĩnh thôi!"
        jump panel_try

## ---------------------------------------------------------------------------
##  HỒI 6 — PHÒNG BÍ MẬT LẦN 1: CHIẾC VÒNG CHÁY
## ---------------------------------------------------------------------------
label act6_bi_mat:
    $ room_name = "Căn phòng bí mật"
    $ mai_mood = "tram"
    $ stage = "bi_mat_1"
    scene bg bimat with blackout
    $ cast("tung", "linh", "khoa", tung="so", linh="so", khoa="buon")
    $ sfx("cutscene_keu_cuu.ogg")
    treem "Cứu với... nóng quá... mẹ ơi..."
    treem "Tùng ơi nắm tay tớ! Đừng buông ra!"
    n "Tiếng kêu cứu vọng lên từ khắp bốn bức tường, rồi tắt lịm."
    $ cast("tung", "linh", "mai", "khoa", mai=None)
    n "[mai_name] bước vào sau cùng. Lớp trưởng đi rất chậm, đưa tay sờ lên từng mảng tường ám khói, như đang chạm vào một thứ rất quen."
    mt "Căn phòng này... lạ quá. Các cậu có thấy cảm giác gì đặc biệt không?"
    n "Một luồng sáng rọi xuống góc phòng. Có thứ gì đó lấp lánh trong đống tro."
    menu:
        "Nhặt thứ đang lấp lánh lên.":
            pass
    $ give("vong_chay_1")
    n "Một chiếc vòng hạt cườm cháy sém. Xanh đỏ. Giống hệt chiếc trên tay cậu."
    mt "Cái... cái gì thế này? Tại sao chiếc vòng bị cháy này lại giống chiếc vòng của bọn mình vậy?"
    $ ex(mai="buon", tung="khoc", linh="buon")
    n "[mai_name] nhìn lần lượt từng người. Rồi khuỵu xuống."
    mt "Chẳng lẽ... một người trong số chúng ta đã..."
    $ add_memory("Chiếc vòng cháy đầu tiên, giống hệt vòng của cả nhóm. “Chẳng lẽ một người trong chúng ta đã...”")
    $ sfx("trong_truong.ogg")
    $ ex(tung="so", linh="so", khoa="so", mai="so")
    n "TÙNG... TÙNG... TÙNG... Tiếng trống trường vang lên giữa đêm." with vpunch
    $ ex(mai=None)
    mt "Chắc chắn chúng ta phải tìm hiểu chuyện quái quỷ gì đang xảy ra. Tiếng trống này... có thể là dấu hiệu bảo chúng ta quay trở lại lớp."
    jump act7_lop

## ---------------------------------------------------------------------------
##  HỒI 7 — LỚP HỌC LẦN 2: XẾP CHỖ & BẢN KIỂM ĐIỂM
## ---------------------------------------------------------------------------
label act7_lop:
    $ room_name = "Lớp 5A"
    scene bg lop with blackout
    $ cast("tung", "linh", "mai", "khoa", tung="so", linh="so", khoa="so", mai=None)
    $ sfx("cutscene_co_giao.ogg")
    co "Cả lớp trật tự!"
    co "Ai cho các em ngồi lộn xộn thế này? Lớp trưởng đâu? Xếp lại chỗ cho các bạn ngay!"
    n "Không có ai trên bục giảng. Chỉ có tiếng thước gõ cộc cộc xuống mặt bàn cô."
    n "[mai_name] lấy từ ngăn bàn ra một tờ giấy, đọc dõng dạc, không còn chút đùa cợt nào."
    $ stage = "xep_cho"
    $ seats = ["", "", "", ""]
    jump xep_cho_loop

label xep_cho_loop:
    call screen seating_puzzle
    if _return == "hint":
        call mai_hint
        jump xep_cho_loop
    if not seats_correct():
        $ sfx("thuoc_go.ogg")
        co "SAI! Ngồi lại!" with hpunch
        jump xep_cho_loop
    co "...Được rồi. Đúng chỗ rồi."

    # --- DJ 22.0: cutscene rủ nhau chơi trốn tìm ---
    $ hide_cast()
    scene bg ky_uc with redflash
    $ sfx("cutscene_ru_choi.ogg")
    treem "Tối nay ra trường chơi trốn tìm đi! Ban đêm mới có cảm giác mạnh!"
    treem "Lớp trưởng ốm rồi, không đi được đâu. Thôi bốn đứa mình đi vậy."
    treem "Lạc nhau thì gặp nhau ở chỗ cũ nhé. Nhớ ám hiệu đấy!"
    scene bg lop with flash
    $ show_cast()
    $ ex(tung="buon", linh="buon", khoa="buon", mai="buon")
    $ add_memory("Bốn đứa rủ nhau ra trường chơi trốn tìm vào ban đêm. Lớp trưởng ốm nên không đi.")
    n "Cả bọn im lặng. Không ai dám nhìn ai. [mai_name] cúi gằm mặt, tay mân mê chiếc vòng."
    co "Em [pname]. Em nói chuyện trong giờ. Lên phòng tài vụ lấy bản kiểm điểm."
    mt "Cô bảo cậu ra lấy bản kiểm điểm đi."
    me "Nhưng tớ có nói chuyện đâu?"
    $ ex(tung="so")
    tung "Bạn... bạn ấy có nói chuyện đâu mà bắt ra..."
    mt "Thôi cậu ra lấy đi, cô chờ lâu cô phạt thêm bây giờ. Tùng run thế kia rồi, chỉ có cậu đi được thôi."
    jump act7_kiem_diem

label act7_kiem_diem:
    $ room_name = "Phòng tài vụ"
    scene bg taivu with blackout
    $ cast()
    n "Cậu đi một mình qua sân. Phòng tài vụ mở toang cửa."
    $ sfx("sam.ogg")
    scene bg den with flash
    n "ẦM! Sấm rền. Đèn tắt phụt." with vpunch
    show ma_chay at ma_stand
    n "Dưới ánh chớp, một đứa trẻ đứng giữa phòng. Người nó đen sạm. Nó không lại gần, cũng không bỏ chạy."
    n "Nó chỉ cúi xuống, đặt một tờ giấy dưới sàn... rồi giơ cổ tay lên. Trên đó là một chiếc vòng hạt cườm."
    $ sfx("sam.ogg")
    hide ma_chay with flash
    scene bg taivu with flash
    $ give("ban_kiem_diem")
    n "Cậu nhặt tờ giấy lên. Là một bản kiểm điểm. Nét chữ... là chữ của chính cậu."
    n "“Em xin hứa tối nay sẽ không ra trường chơi nữa...”"
    n "Mặt sau nguệch ngoạc mấy chữ: “Lạc nhau thì gặp ở 3C. Ám hiệu: TẮC KÈ.”"
    $ add_memory("Bản kiểm điểm viết bằng chữ của chính cậu. “Lạc nhau thì gặp ở 3C. Ám hiệu: TẮC KÈ.”")
    $ f_has_note_3c = True
    jump act8_3c

## ---------------------------------------------------------------------------
##  HỒI 8 — TÌM 3C (gốc bàng) — BƯỚC 1: CHẤP NHẬN
## ---------------------------------------------------------------------------
label act8_3c:
    $ room_name = "Sân trường"
    $ stage = "tim_3c"
    scene bg san with blackout
    $ cast("tung", "linh", "mai", "khoa", tung=None, linh=None, khoa=None, mai=None)
    n "Cậu chạy về. [mai_name] đã đứng đợi ở giữa sân, như biết trước cậu sẽ ra đây."
    mt "Ủa 3C là chỗ nào nhỉ, các cậu có biết không? Tớ thấy quen lắm mà không nhớ được ở đâu..."
    jump tim_3c_loop

label tim_3c_loop:
    call screen room_view("san_3c")
    $ act = _return
    $ used = held_item
    $ held_item = None
    if act == "__hint__":
        call mai_hint
    elif used:
        call wrong_item
    elif act == "quy_hoach":
        $ f_saw_map = True
        call screen school_map
        $ stage = "tim_3c"
        $ hint_idx["tim_3c"] = 2
        khoa "Hàng 3, cột C... là cây bàng."
    elif act == "goc_bang":
        if not f_saw_map:
            n "Một gốc bàng già, hốc cây bị đóng ván. Trên ván khắc “3C”. Nhưng 3C là gì nhỉ?"
        else:
            n "Hốc cây bàng bị đóng kín bằng một tấm ván. Trên ván khắc “3C”."
            mt "Đến chỗ này rồi mà có thấy gì đâu... Hay thử nói cái câu “thần chú” kia đi xem nào."
            $ pw_in = renpy.input("Cậu ghé sát vào hốc cây và thì thầm...", length=20).strip().lower()
            $ pw_in = pw_in.replace(" ", "").replace(".", "").replace("!", "")
            if pw_in in ("tắckè", "tacke", "tắcke", "tackè"):
                jump mo_3c
            else:
                n "Không có gì xảy ra. Gió thổi qua tán bàng nghe như tiếng ai cười khẽ."
    else:
        n "Không có gì ở đây cả."
    jump tim_3c_loop

label mo_3c:
    $ sfx("mo_3c.ogg")
    n "Cạch. Tấm ván bật ra như có ai đẩy từ bên trong."
    n "Trong hốc cây là một túi ni lông cũ. Bên trong có..."
    $ give("vong_chay_2")
    $ give("chu_van")
    n "...một chiếc vòng hạt cườm cháy sém có khắc chữ LINH, và một mảnh gỗ khắc chữ Vạn."
    $ ex(linh="so")
    linh "Đấy... đấy là vòng của tớ..."
    n "Linh nhìn xuống cổ tay mình. Rồi nhìn chiếc vòng cháy. Rồi lại nhìn cổ tay mình."
    mt "Vậy... không chỉ một người..."
    mb "...mà toàn bộ chúng ta đã... chết rồi sao?"
    $ mai_mood = "buon"
    $ ex(tung="khoc", linh="khoc", khoa="buon", mai=None)
    n "Không ai trả lời. Tùng bật khóc. Linh lắc đầu liên tục."
    khoa "Tớ nhớ rồi. Hôm đó bọn mình bị bác Thọ đuổi, chạy vào tài vụ trốn. Trời tối, tớ vấp phải dây điện..."
    $ ex(khoa="khoc")
    khoa "Là tại tớ. Tất cả là tại tớ."
    menu:
        "Ôm lấy Khoa: “Không phải lỗi của cậu.”":
            me "Không phải lỗi của cậu. Mình đi cùng nhau, mình chạy cùng nhau. Không ai cố ý cả."
            khoa "..."
            n "Khoa gục vào vai cậu. Lần đầu tiên trong đêm, tay Khoa ấm lên một chút."
        "Nắm tay Khoa thật chặt, không nói gì.":
            n "Cậu nắm chặt tay Khoa. Không cần nói gì cả. Khoa siết lại."
    $ ex(khoa="buon", tung="buon", linh="buon")
    $ add_memory("Đêm 14/10, bốn đứa bị bác Thọ đuổi, chạy trốn vào phòng tài vụ. Khoa vấp phải dây điện. Lửa bén. Cánh cửa bị kẹt. Không ai ra được.")
    $ step_chap_nhan = True
    n "— BƯỚC MỘT CỦA NGHI LỄ: CHẤP NHẬN —"
    jump act9_tho_khoc

## ---------------------------------------------------------------------------
##  HỒI 9 — BÁC THỌ MANG ĐỒ LỄ — ĐÀN CẦU SIÊU — BƯỚC 2: BUÔNG BỎ
## ---------------------------------------------------------------------------
label act9_tho_khoc:
    $ sfx("cutscene_tho_khoc.ogg")
    $ cast("tung", "linh", "tho", "mai", "khoa", tho="khoc")
    n "Có tiếng dép lê lẹp xẹp. Bác Thọ đi ra từ phòng bảo vệ — không còn lảo đảo. Bác ôm trong tay hình nhân giấy, đèn cúng, bát hương và một quyển sách cũ."
    n "Bác vừa đi vừa khóc. Không thành tiếng. Chỉ có vai rung lên từng hồi."
    n "Bác đi thẳng vào phòng tài vụ, vào căn phòng bí mật, rồi đi ra tay không."
    $ cast("tung", "linh", "mai", "khoa")
    mb "Thôi... không còn thời gian nữa đâu. Vào bên trong căn phòng bí mật xem tại sao bác Thọ lại vào đó đi các cậu."
    jump act9_dan_le

label act9_dan_le:
    $ room_name = "Đàn lễ cầu siêu"
    $ bgm("bg_phase3.ogg")
    scene bg phongle with blackout
    $ cast("tung", "linh", "mai", "khoa", tung="buon", linh="buon", khoa="buon")
    $ sfx("cutscene_le.ogg")
    n "Căn phòng cháy sém giờ đã thắp nến. Đồ lễ bác Thọ mang vào được để ngay ngắn dưới đất, cạnh một án thờ trống."
    n "Hình nhân giấy có năm người. Năm đứa trẻ đeo vòng tay."
    mb "Xếp lại bàn thờ theo đúng hướng dẫn trong sách đi các cậu."
    $ stage = "ban_tho"
    $ altar = {"cao_giua": None, "giua": None, "trai": None, "phai": None, "truoc": None}
    $ altar_sel = None
    jump ban_tho_loop

label ban_tho_loop:
    call screen altar_puzzle
    if _return == "hint":
        call mai_hint
        jump ban_tho_loop
    if not altar_correct():
        n "Ngọn nến chao đảo rồi tắt phụt. Có gì đó chưa đúng."
        jump ban_tho_loop
    $ sfx("chuong.ogg")
    n "Ngọn nến bùng sáng. Khói hương cuộn thành một sợi thẳng tắp lên trần."
    mb "Giờ... quỳ xuống đi các cậu. Lạy ba lạy."
    menu:
        "Quỳ xuống, lạy lạy thứ nhất.":
            n "Lạy thứ nhất — cho những ngày còn chạy nhảy dưới gốc bàng."
    menu:
        "Lạy lạy thứ hai.":
            n "Lạy thứ hai — cho bố mẹ ở nhà, vẫn còn đợi."
    menu:
        "Lạy lạy thứ ba.":
            n "Lạy thứ ba — cho bác Thọ."
    $ bgm("bg_phase4.ogg")
    $ sfx("pitong.ogg")
    n "Bức tường phía sau án thờ từ từ tách đôi. Khói trắng tràn ra, lạnh buốt."
    n "Phía bên kia là một khoảng tối mênh mông."
    jump act10_u_minh

## ---------------------------------------------------------------------------
##  HỒI 10 — U MINH — BƯỚC 3: SIÊU THOÁT
## ---------------------------------------------------------------------------
label act10_u_minh:
    $ room_name = "U Minh"
    $ stage = "u_minh"
    scene bg uminh with blackout
    show khoi
    $ cast("tung", "linh", "mai", "khoa", tung="buon", linh="buon", khoa="buon", mai=None)
    $ sfx("cutscene_cuoi.ogg")
    n "Giữa làn khói là một nấm mộ thấp. Trên tấm bia gỗ có năm cái tên — bốn cái tên đã mờ, một cái tên bỏ trống."
    n "Tùng. Linh. Khoa. [pname]."
    mb "Giờ... các cậu đã hiểu chuyện gì xảy ra chưa?"
    menu:
        "“Bọn mình... đã chết ở đây. Từ đêm hôm đó.”":
            pass
        "“Tớ không muốn hiểu đâu.”":
            mb "Tớ biết. Tớ cũng không muốn. Nhưng các cậu phải nhớ ra thì mới đi được."
    mb "Ừ. Chính là các cậu ngày xưa đã chết khi chơi trốn tìm ở trường."
    mb "Hôm đó tớ bị ốm, không đi được. Sáng hôm sau tớ đến lớp... chỉ còn mỗi mình tớ."
    mb "Nhà trường bảo các cậu bị mất tích. Họ đút tiền cho báo, cho công an. Không ai được nói gì cả. Kể cả bố tớ."
    $ ex(tung="so", linh="so", khoa="so")
    tung "Bố... cậu?"
    mb "Bác Thọ là bố tớ."
    n "Không ai nói được lời nào."
    mb "Bố tớ là người duy nhất nhìn thấy. Bố đã cố phá cửa. Không phá được."
    mb "Từ hôm đó, đêm nào bố cũng nghe tiếng các cậu gọi. Bố uống rượu. Rồi một hôm, bố tự chọc mù mắt mình... để khỏi phải nhìn thấy các cậu nữa."
    mb "Còn tớ thì... từ hôm đó tớ cũng nhìn thấy các cậu. Ngày nào cũng thấy. Các cậu vẫn chơi trốn tìm, vẫn chờ tớ đến chơi cùng, không biết là mình đã..."
    mb "Nên tớ đã nhờ thầy dựng lễ cầu siêu này. Một ván trốn tìm cuối cùng. Để các cậu tự nhớ ra. Để các cậu được đi. Và để bố tớ... được tha thứ."

    $ sfx("tho_bo_vao.ogg")
    $ cast("tung", "linh", "mai", "tho", "khoa", tho="khoc", tung="buon", linh="buon", khoa="buon")
    n "Có tiếng sột soạt. Bác Thọ bò vào giữa làn khói, hai tay quờ quạng trên nền đất."
    tho "Các con ơi... bác xin lỗi. Đây là lỗi của bác."
    tho "Bác không nên đuổi các con. Bác không nên... Bác đã cố lắm rồi, cái cửa nó không mở..."
    tho "Bác không biết phải làm gì để đền bù cho các con nữa..."
    tho "[mai_name] ơi... bố xin lỗi con. Bố xin lỗi... Bố còn chẳng nhận ra giọng con nữa..."
    $ ex(mai="khoc")
    n "[mai_name] quỳ xuống, ôm lấy bác Thọ. Lần đầu tiên trong đêm, lớp trưởng khóc thành tiếng."
    mb "Bố ơi... con đây. Không phải lỗi của bố đâu. Chưa bao giờ là lỗi của bố cả."
    n "Bác Thọ quay khuôn mặt mù lòa về phía bốn đứa trẻ."
    menu:
        n "Cậu muốn nói gì với bác Thọ?"
        "“Bác Thọ ơi, bọn cháu không trách bác đâu.”":
            me "Bác Thọ ơi, bọn cháu không trách bác đâu. Bọn cháu chỉ nghịch quá thôi."
        "“Bác đừng uống rượu nữa nhé. Ở lại với lớp trưởng đi.”":
            me "Bác đừng uống rượu nữa nhé. Bác ở lại với [mai_name]. Bạn ấy còn cần bác lắm."
        "“Cảm ơn bác đã cố cứu bọn cháu.”":
            me "Cảm ơn bác đã cố phá cửa. Bọn cháu nghe thấy hết. Bọn cháu biết bác đã cố."
    $ ex(mai=None)
    tung "Bác ơi... bọn cháu xin lỗi vì đã trêu bác suốt bao nhiêu năm."
    linh "Bác đừng khóc nữa..."
    khoa "Bác Thọ... cháu cũng xin lỗi."
    n "Bác Thọ đưa tay ra. Cậu nắm lấy. Bàn tay ông già run bần bật, rồi dần dần yên lại."
    $ ex(tho="hien")
    tho "Ừ... ừ... Các con đi đi. Đi cho thanh thản. Bác... ở lại với [mai_name]."
    n "[mai_name] dìu bác Thọ ngồi tựa vào tường."
    $ cast("tung", "linh", "mai", "khoa")

    mb "Các cậu... bỏ lại vòng tay trên mộ đi. Mang theo nó thì không đi được đâu."
    menu:
        "Tháo vòng tay, đặt lên mộ.":
            pass
    $ take("vong_minh")
    $ take("vong_chay_1")
    $ take("vong_chay_2")
    n "Cậu tháo chiếc vòng hạt cườm, đặt lên nấm mộ, cạnh hai chiếc vòng cháy sém. Tùng, Linh, Khoa cũng làm theo."
    n "Cổ tay nhẹ bẫng. Cứ như vừa đặt xuống một thứ rất nặng mà mình đã mang suốt bao năm."
    $ step_buong_bo = True
    n "— BƯỚC HAI CỦA NGHI LỄ: BUÔNG BỎ —"

    mb "Giờ nắm tay nhau đi. Đứng quanh mộ. Đừng buông ra nhé."
    $ hands = []
    jump nam_tay_loop

label nam_tay_loop:
    if len(hands) >= 3:
        jump sieu_thoat
    menu:
        n "Cậu nắm tay ai?"
        "Nắm tay Tùng" if "Tùng" not in hands:
            $ hands.append("Tùng")
            $ ex(tung="vui")
            tung "Lần này tớ không sợ nữa đâu."
        "Nắm tay Linh" if "Linh" not in hands:
            $ hands.append("Linh")
            $ ex(linh="vui")
            linh "Đi đâu cũng phải đi cùng nhau đấy nhé."
        "Nắm tay Khoa" if "Khoa" not in hands:
            $ hands.append("Khoa")
            $ ex(khoa="vui")
            khoa "Lần này... không ai vấp ngã nữa."
    jump nam_tay_loop

label sieu_thoat:
    $ sfx("cutscene_sieu_thoat.ogg")
    n "Một luồng sáng trắng rọi xuống nấm mộ. Từ khe đất, những bông hoa trắng từ từ nở bung."
    show hoa_no with Dissolve(2.0)
    n "Bốn đứa trẻ đứng thành vòng tròn, tay trong tay. Và cất tiếng hát."
    n "♪ Trốn tìm ơi, trốn tìm ơi — hết giờ rồi, mình về thôi ♪"
    n "♪ Gốc bàng xưa còn đứng đợi — que kem chưa kịp mời ai ♪"
    n "♪ Đếm đến mười rồi mở mắt — bạn bè ơi, mình đi xa ♪"
    n "♪ Người ở lại đừng khóc nhé — mai nắng vẫn sân trường ta ♪"
    $ ex(mai="khoc")
    mb "Các cậu..."
    mb "Ván này tớ thua rồi. Tớ không tìm được các cậu nữa."
    mb "Tạm biệt các cậu nhé."
    menu:
        "“Tạm biệt [mai_name]. Cảm ơn cậu đã tìm thấy bọn tớ.”":
            pass
        "“Tớ vẫn nợ cậu một que kem đấy.”":
            mb "Hì... ừ. Nợ thì nhớ đấy nhé."
    $ step_sieu_thoat = True
    n "— BƯỚC BA CỦA NGHI LỄ: SIÊU THOÁT —"
    $ cast()
    scene bg den with Fade(1.5, 2.0, 1.5, color="#ffffff")
    hide screen hud
    jump epilogue

## ---------------------------------------------------------------------------
##  VĨ THANH
## ---------------------------------------------------------------------------
label epilogue:
    $ bgm("bg_ket.ogg")
    scene bg sang with Dissolve(2.0)
    $ cast("mai", "tho", mai="vui", tho="hien")
    n "Sáng hôm sau."
    n "Người ta thấy bác bảo vệ trường Tiểu học Vĩnh Ninh ngồi dưới gốc bàng, tỉnh táo, không một giọt rượu."
    n "Bên cạnh bác là [mai_name]."
    n "Trên tấm ván hốc cây khắc “3C” có đặt bốn que kem. Đang chảy dần dưới nắng."
    mb "Nợ thì phải trả chứ. Nhưng lần này... để tớ khao các cậu."
    tho "Lớp trưởng của bố giỏi lắm."
    n "Gió thổi qua tán bàng. Xa xa, có tiếng trẻ con đếm đến mười, rồi cười khúc khích."
    n "Lần này, không còn ai phải trốn nữa."
    $ cast()
    scene bg den with Dissolve(2.0)
    n "TRỐN TÌM\n\n— HẾT —"
    return
