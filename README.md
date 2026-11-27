# Trốn Tìm

Game giải đố kiểu escape room làm bằng Ren'Py 8.6, viết dựa trên cốt truyện và tâm lý nhân vật lớp trưởng Mai/Minh và bác bảo vệ Thọ.

Bốn học sinh lớp 5A trở lại trường Vĩnh Ninh vào một đêm để chơi một ván trốn tìm cuối cùng. Qua lễ cầu siêu ba bước (Chấp nhận, Buông bỏ, Siêu thoát), các em dần nhớ ra chuyện gì đã xảy ra trong đêm 14 tháng 10.

## Chạy game

1. Cài [Ren'Py SDK](https://www.renpy.org/latest.html) bản 8.6 trở lên.
2. Mở Ren'Py Launcher, đặt Projects Directory là thư mục chứa repo này, chọn project rồi bấm **Launch Project**.

Muốn có bản chạy độc lập (`TronTim.exe`) thì dùng **Build Distributions → Windows** trong Launcher.

## Cách chơi

- Bấm vào đồ vật trong phòng để xem xét.
- Bấm một món ở thanh đồ dưới đáy màn hình để cầm lên, rồi bấm vào chỗ muốn dùng. Bấm chuột phải hoặc Esc để cất đi.
- **I** mở túi đồ, **J** mở sổ ký ức, **H** hỏi lớp trưởng khi bí.

## Cấu trúc

| File | Nội dung |
|---|---|
| `game/script.rpy` | Kịch bản 10 hồi |
| `game/hns_core.rpy` | Nhân vật, biến, túi đồ, gợi ý, điểm tương tác, HUD |
| `game/hns_puzzles.rpy` | Các câu đố: khóa số, trộm chìa, bảng điện, xếp chỗ, bản đồ, bàn thờ |
| `game/hns_visual.rpy` | Nhân vật động, bối cảnh có hiệu ứng, đèn pin |
| `game/Plan/` | File kế hoạch tâm lý nhân vật và DJ (không đưa vào bản build) |
| `tools/` | Bộ vẽ sinh toàn bộ ảnh của game |

## Ảnh và âm thanh

Toàn bộ ảnh trong `game/images/` và các file `hns_*.png` trong `game/gui/` được sinh bằng code. Chạy lại bằng lệnh:

```
powershell -ExecutionPolicy Bypass -File tools\gen_art.ps1
```

Lệnh này ghi đè toàn bộ ảnh. Nếu đã thay bằng ảnh vẽ tay cùng tên file thì đừng chạy lại.

Game chưa có âm thanh. Muốn thêm thì cho file `.ogg` vào `game/audio/` đúng tên được gọi trong các lệnh `sfx(...)` và `bgm(...)` của `script.rpy`. File nào chưa có thì game tự bỏ qua.
