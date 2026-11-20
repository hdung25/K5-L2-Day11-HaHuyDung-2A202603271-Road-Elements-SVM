# Báo cáo cá nhân — Ngày 11
Họ tên: Hà Huy Dũng    Mã học viên: 2A202603271  
Phiên bản CVAT (Help → About): **CVAT 2.82.0** (Server 2.82.0, UI 2.82.0), chạy local bằng Docker tại `http://localhost:8080`  
Guideline: Road v1.0    Lần nộp (`revision` trong manifest): **2**  
Thời điểm export (ngày giờ trên CVAT): 20/11/2026, 17:46 (giờ VN) — manifest `created_at` 2026-11-20T10:46:37Z    Số lần nộp lại sau Rework: 1 (bản r1 giữ ở `r1/`)

Gói nộp: `hahuydung-front.zip` (A01–A16), `hahuydung-fisheye.zip` (B01–B12), `hahuydung-manifest.json`, `hahuydung-qc1-for-trieuhoanghieu.md`, `hahuydung-report.md`.

## 1. Kiểm project
Project `d11-road-hahuydung` (#3), labels dán từ `configs/road_v1_labels.json` (Raw), 4 task: `front` (A01–A12), `front-extra` (A13–A16), `fisheye` (B01–B08), `fisheye-extra` (B09–B12).

| Mục | Đúng như guideline Road v1.0? | Ghi chú |
| --- | --- | --- |
| 6 label, đúng kiểu | Đúng | lane, road_curb = polyline; crosswalk, drivable = polygon; traffic_light, traffic_sign = rectangle |
| Thuộc tính và giá trị | Đúng | `PYTHONPATH=src python -m road_lab.taxonomy` khớp từng ký tự với tab Raw; `road_check check` vòng tròn: 0 lỗi QC1-12 |
| 4 tag ảnh | Đúng | camera, timeofday, weather, source — mỗi label kiểu Tag có một thuộc tính select `value` |

Cách kết thúc polyline trên bản CVAT này: click lần lượt các điểm từ gần xe ra xa, bấm **N** để kết thúc (Shift+N/Esc huỷ).  
Cách đặt tag ảnh trên bản CVAT này: công cụ **Setup tag** ở thanh trái → chọn label (`camera` trước) → mở **Details** trong bảng Objects và chọn `value` (CVAT tự điền giá trị đầu danh sách nên phải sửa lại từng tag).

## 2. Số lượng đã gán
| Task | Ảnh | lane | road_curb | crosswalk | drivable | traffic_light | traffic_sign |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| front | 12 | 31 | 2 | 3 | 22 | 18 | 18 |
| front-extra (đã làm 4 / 4) | 4 | 10 | 0 | 1 | 6 | 12 | 0 |
| fisheye | 8 | 11 | 2 | 4 | 9 | 5 | 0 |
| fisheye-extra (đã làm 4 / 4) | 4 | 0 | 0 | 3 | 4 | 0 | 0 |

Tổng: 28/28 ảnh, 28/28 ảnh đủ bốn tag, 0 ảnh chưa gán (theo manifest). Mọi job ở trạng thái **completed** (stage acceptance).

## 3. Bảng ca khó
| Ảnh | Nhãn | Phân vân giữa | Đã chọn | Lý do |
| --- | --- | --- | --- | --- |
| A05 | lane L1/R1 | vẽ vạch theo mép xe đỗ / không vẽ | không vẽ lane; chỉ `road_curb` (vỉa phải) + `drivable direct` | phố không có vạch sơn; guideline: không vẽ vạch ảnh không có. Lint báo QC1-02 → **xin coach xác nhận miễn** |
| A06 | lane R1 | kéo R1 theo hàng cột cầu cạn / không vẽ | chỉ vẽ L1 (vàng đôi, đoạn ngắn còn thấy sau xe), không có R1 | phía phải làn không có vạch sơn, chỉ có cột; vạch trắng góc phải không song song hướng đi (thuộc đường ngang). Lint QC1-02 → **xin miễn** |
| A09 | lane R1 / position | coi vạch đôi trắng là L1 hay L2 | vạch đứt = L1, vạch đôi = L2; không có R1 | tâm xe (x≈640) nằm bên phải vạch đứt; phía phải chỉ có vệt nhựa vá, không phải sơn. Lint QC1-02 → **xin miễn** |
| A03 | lane, occluded | bật occluded cho R1 hay R2 | R2 (vạch ô đỗ sát lề) `occluded = true` | đoạn gần của R2 bị xe đỗ che, đã nối qua chỗ che; R1 chỉ bị chữ SCHOOL (sơn) đè, không phải vật che |
| A03 | tag weather | clear / overcast | overcast | trời nhiều mây, mặt đường khô |
| A07, A10, A13 | tag weather | overcast / rain | rain | mặt đường ướt rõ, kính có giọt mưa |
| A07 | lane L1 | vạch trắng mờ sát dải phân cách / bỏ | vẽ L1 trắng liền đoạn còn thấy (200,444)→(440,370) | còn vệt sơn mờ tách khỏi chân barrier; dừng ở mép xe phía trước |
| A08 | traffic_light | đèn nhìn nghiêng / quay lưng | `facing = side`, `color = unknown` cho 4 cụm vỏ vàng không thấy mặt đèn; đèn người đi bộ (bàn tay cam) `type = pedestrian`, `color = red` | không thấy bóng đang sáng nên không đoán màu |
| A09 | traffic_sign group | biển quay lưng | `group = other`, `facing = back` | không đọc được chức năng từ mặt sau |
| A10 | traffic_sign group | prohibitory / supplementary | 3 biển cấm đỗ/dừng (cụm cột trái) = prohibitory; tấm trắng nhỏ dưới biển xa = supplementary | theo bảng nhóm biển Mỹ trong guideline |
| A10 | lane R1, occluded | dừng R1 ở chỗ decal / nối qua | nối qua đoạn bị decal hoa dán kính che, `occluded = true` | decal là vật che ngắn, vạch thấy lại phía xa |
| A11, A12 | traffic_sign group | biển trắng chữ đỏ (quy định đỗ) | prohibitory | chức năng là cấm/hạn chế đỗ |
| A12 | lane | vạch của đường ngang trong giao lộ | không gán | không song song hướng đi của xe |
| B01 | drivable | gồm dải lát đỏ bên trái / không | không gồm | dải đỏ là làn xe đạp (Hà Lan), không phải phần đường ô tô đi |
| B02 | lane | — | không có lane | đoạn tiếp cận vạch ngựa vằn chỉ có vỉa, không có vạch sơn |
| B03, B04 | position (camera sau) | trái/phải theo xe hay theo ảnh | L/R theo ảnh (trái ảnh = L) | thống nhất với GT tổng hợp của checker (`synthetic.py`) |
| B04 | drivable | gồm làn BUS / không | không gồm làn BUS | làn dành riêng xe buýt, không phải làn đang đi |
| B05–B08 | lane position | L1/R1 / other | `position = other` cho mọi lane | camera hai bên (guideline mục 4) |
| B11 | lane | vạch ô đỗ, vạch kẻ chéo vàng | không gán lane | guideline: vạch ô đỗ không gán lane; bãi đỗ không có vạch dọc |
| Mọi ảnh front | lane điểm đầu | dừng ở vệt sơn gần nhất / kéo tới đáy ảnh | vạch đứt còn tiếp tục: kéo điểm đầu tới đáy ảnh (hoặc mép capô) theo hướng vạch | điểm đầu sát xe là điểm quan trọng nhất, vạch đứt là một polyline liên tục |

## 4. Phiếu QC 1 nhận được
Bạn kiểm lô của tôi: Triệu Hoàng Hiếu (`trieuhoanghieu`), phiếu `trieuhoanghieu-qc1-for-hahuydung.md` (bản lưu: `received-trieuhoanghieu-qc1-for-hahuydung.md`), kiểm 6 ảnh A01, A04, A07, A08, A09, B03 — 71 nhãn.  
Quyết định nhận được: **Rework** (0 lỗi nặng, 4 lỗi chính / 71 = 5,63 % > 5 %).

| Mã lỗi | Số lỗi | Đồng ý? | Đã sửa? |
| --- | ---: | --- | --- |
| QC1-04 · A01 lane R2 lệch tâm vạch vàng ~10 px quanh (901, 621) | 1 | Đồng ý — đo lại tâm kênh vàng: tại x = 901 tâm ở y = 615, bản cũ 621 (lệch ~6 px > 5) | Đã sửa: R2 đặt lại theo tâm đo từng cột (1280, 704) → (440, 505) |
| QC1-04 · A01 lane R1 kéo qua vùng không có sơn tới đáy ảnh | 1 | Đồng ý — vệt sơn gần nhất dừng ở ~(657, 682), dưới đó là bóng capô | Đã sửa: điểm đầu R1 = (659, 679); vùng direct/alternative cắt ở y = 720 |
| QC1-04 · A08 lane L2 đoạn đầu đi dọc vạch dừng ngang | 1 | Đồng ý — 60 px đầu bám vạch dừng | Đã sửa: L2 bắt đầu (62, 355) trên vạch dọc |
| QC1-04 · A08 lane R1 bỏ đoạn vạch gần nhất ~(757, 440) | 1 | Đồng ý — còn một vệt đứt trước vạch qua đường | Đã sửa: thêm đoạn, điểm đầu (758, 442) |
| (tự phát hiện khi kiểm lô của Hiếu) QC1-10 · A01 thiếu 2 biển chỉ dẫn xanh | 2 | — | Đã bổ sung `traffic_sign` information (551, 408)–(604, 481) và (434, 464)–(452, 487) |

Ca mơ hồ Hiếu nêu: A07 L1 (vạch rất mờ sát chân dải chắn) — tôi giữ L1 vì đo được gờ sáng tách khỏi chân barrier (mục 3). A05/A06/A09 QC1-02: vẫn chờ coach xác nhận miễn.

Nộp lại: đã cất bản cũ vào `r1/` (`hahuydung-front.zip`, `hahuydung-fisheye.zip`, `hahuydung-manifest-r1.json`), sửa trên CVAT, export lại giữ nguyên tên zip, tạo manifest **revision 2**. Lint sau sửa: chỉ còn 4 cảnh báo QC1-02 đang xin miễn; kiểm vòng tròn 0 lỗi định dạng.

## 5. Kiểm file export
| File | Mở lại được? | Số shape ảnh 1 (job / file) | Số shape ảnh 2 (job / file) | Tag camera có trong XML? |
| --- | --- | --- | --- | --- |
| hahuydung-front.zip | Có (`road_check lint`: 16 ảnh, 0 lỗi định dạng) | A01: 7 / 7 | A02: 5 / 5 | Có — `<tag label="camera"><attribute name="value">front</attribute></tag>` |
| hahuydung-fisheye.zip | Có (`road_check lint`: 12 ảnh, 0 lỗi định dạng) | B01: 4 / 4 | B02: 6 / 6 | Có — `fisheye_front`, `fisheye_rear`, `fisheye_left`, `fisheye_right` đúng hậu tố FV/RV/MVL/MVR |

Bảng kiểm file:
- [x] Format CVAT for images 1.1, **không kèm ảnh** (`contains_images: false` ở cả hai file).
- [x] `road_check lint`: 28 ảnh, chỉ còn 4 cảnh báo QC1-02 ở A05 (L1, R1), A06 (R1), A09 (R1) — ảnh thật sự không thấy vạch, đã ghi ở mục 3 để coach xác nhận miễn.
- [x] Manifest `hahuydung-manifest.json`, `revision 2`, sha256: front `f9212103…cb24b`, fisheye `c9271c81…1cb921`. Manifest revision 1 giữ ở `r1/hahuydung-manifest-r1.json`.
- [x] `road_check check` dùng chính file nộp làm GT (kiểm vòng tròn định dạng): 20/20 ảnh bắt buộc đọc được, 0 lỗi, 205 nhãn — xác nhận file mở lại đúng tên label, thuộc tính, chiều vẽ. (Đây **không** phải điểm so với GT của coach.)

## 6. Ảnh chụp màn hình
1. Tab Labels của project: `screens/01-project-labels.jpg` (6 label + 4 tag).
2. Một ảnh camera trước đã gán đủ (làn, vùng lái, đèn/biển): `screens/02-front-A12.jpg`.
3. Một ảnh fisheye đã gán, phóng to đoạn polyline cong: `screens/03-fisheye-B03.jpg` và phóng to R1 theo cung `screens/03b-fisheye-B03-R1-zoom.png`.
4. Một đoạn XML có `<polyline label="lane">` (trích từ `hahuydung-front.zip`, ảnh A01):

```xml
<polyline label="lane" source="manual" occluded="0" points="0.00,600.80;192.10,544.00;334.60,504.80" z_order="0">
  <attribute name="position">L2</attribute>
  <attribute name="style">solid</attribute>
  <attribute name="color">white</attribute>
  <attribute name="kind">double</attribute>
</polyline>
```
Thêm: `screens/00-about-version.jpg` (Help → About), `screens/04-job-completed.jpg` (job completed), `screens/overlay-front.jpg`, `screens/overlay-fisheye.jpg` (toàn bộ 28 ảnh đã gán).

## 7. Tự đánh giá
Lỗi bạn mắc nhiều nhất hôm nay (theo mã QC1-xx), và cách tránh ở Ngày 20: **QC1-04 (tâm vạch)** ở vạch đôi và vạch rộng gần xe — ban đầu polyline bám mép vạch thay vì tâm (A03 vàng lệch ~6 px, A11 vàng đôi lệch ~10 px vì ảnh tối). Đã sửa bằng cách đo tâm từng vạch theo hàng rồi lấy trung điểm của hai vạch. Ngày 20 (ca đêm, mưa): luôn phóng to ≥4× ở đoạn gần xe và kiểm từng vạch đôi bằng hai mép.  
Nhãn của bạn đi vào model ở đâu? Chọn một lỗi đã sửa và nói nó làm model học sai thế nào: polyline lane là đích của model phát hiện làn kiểu row-anchor (mục 8) dùng cho LKA. Nếu giữ L1 ở A11 lệch 10 px sang trái ở hàng y=720, model học rằng tâm vạch nằm lệch → ước lượng vị trí ngang của xe trong làn sai vài chục cm ở khoảng cách gần, đúng vùng LKA dùng để giữ làn; lỗi lặp lại trên nhiều ảnh ban đêm còn tạo thiên lệch hệ thống cho ca đêm.

## 8. (Tùy chọn, buffer) Từ polyline đến đích row-anchor
Ảnh A01, `road_lab.rowanchor hahuydung-front.zip --image A01`:

| y | 720 | 680 | 640 | 600 | 560 |
| --- | ---: | ---: | ---: | ---: | ---: |
| x của chúng tôi (L1) | 109.3 | 155.2 | 206.4 | 248.0 | 296.2 |
| x của chúng tôi (R1, revision 2) | không có làn | không có làn | 600.7 | 543.3 | 483.4 |
| x của bạn kia (Hiếu, R1) | không có làn | không có làn | 601.4 | 543.8 | 481.2 |

1. Năm số x là đích row-anchor của vạch. Nếu dừng polyline sớm 40 px ở đầu gần (điểm đầu ở y=680 thay vì 720), hàng **720** đổi thành "không có làn".
2. So với Hiếu (R1, A01): cả hai đều không có làn ở hàng 720 (vạch bị bóng capô che); ở hàng 560 lệch 2,2 px (483,4 so với 481,2). Lệch ở hàng 720 (gần xe) ảnh hưởng LKA nhiều hơn vì LKA điều khiển theo vị trí ngang của vạch ngay trước xe.
3. Vẽ từ xa về gần thì nội suy x theo từng hàng không đổi về giá trị, nhưng điểm đầu/điểm cuối bị đảo: `road_check` sẽ báo QC1-04 "vẽ ngược chiều", và script giả định điểm đầu là gần xe (ví dụ cắt polyline, tính điểm dừng) sẽ gặp khó.

---

## Công cụ đã sử dụng
Theo hướng dẫn của giảng viên (được dùng công cụ, ghi lại ở cuối báo cáo):
- **CVAT 2.82.0 self-host** (Docker Desktop, `docker compose up -d` từ repo `cvat-ai/cvat` tag v2.82.0) — không dùng app.cvat.ai, ảnh không rời máy.
- **Claude Code (Anthropic)** hỗ trợ toàn bộ phần thao tác: dựng CVAT local, tạo project/task qua REST API, đặt điểm polyline/polygon/box sau khi xem từng ảnh phóng to, viết các script hỗ trợ, đẩy nhãn vào job qua API, chuyển job sang completed, export, chụp màn hình qua trình duyệt trong app, soạn báo cáo này.
- Script hỗ trợ (thư mục `work/`, Python + numpy/Pillow/OpenCV, chỉ chạy trên máy):
  - `zoom.py`: phóng to vùng ảnh có lưới toạ độ để đọc vị trí điểm.
  - `snap.py`: đưa polyline đặt tay vào **tâm vệt sơn** (lọc "gờ sáng" theo pháp tuyến, tự ước lượng bề rộng vạch) để lệch ≤ 5 px; `ridges.py`/đo đỉnh vàng theo hàng cho vạch mờ, vạch đôi.
  - `blobs.py`: lấy bao lồi các vạch ngựa vằn làm polygon crosswalk; `lamps.py`: tìm bóng đèn đang sáng để khoanh box đèn.
  - `build.py` + `work/spec/*.py`: khai báo nhãn từng ảnh, dựng `ann.json`, vẽ overlay để tự kiểm bằng mắt.
  - `cvat_api.py`: tạo project/task, upload nhãn, set job completed, export CVAT for images 1.1 (không kèm ảnh); `merge_export.py`: gộp task chính + task thêm thành một zip nộp.
- Công cụ của repo lab: `road_check lint` (+ `--manifest`), `road_check check` (kiểm vòng tròn định dạng), `road_lab.rowanchor`, `road_check selftest` (SELFTEST PASS).
