# Phiếu QC 1 — Road v1.0

Lô được kiểm (học viên): Triệu Hoàng Hiếu (`trieuhoanghieu`)        Người kiểm (học viên): Hà Huy Dũng (`hahuydung`)  
Ngày: 20/11/2026                Phiên bản guideline: Road v1.0  
File được kiểm (tên + `revision` trong manifest): `trieuhoanghieu-front.zip` (sha256 `2019f75b…c6d5f8`), `trieuhoanghieu-fisheye.zip` (sha256 `7c120f14…053a44`), manifest **revision 1** — sha256 hai file khớp manifest, `contains_images: false`.  
Số ảnh kiểm: 6 (A01, A04, A08, A10, B03, B05) (+ 0 ảnh thêm)   Số nhãn đã kiểm (shape + tag): **52** (28 shape + 24 tag)

Cách kiểm: chạy `road_check lint` trên cả 28 ảnh; vẽ nhãn của Hiếu lên ảnh gốc, phóng to 3–6× có lưới toạ độ; đo tâm vệt sơn theo từng hàng/cột (độ sáng, kênh vàng) để đối chiếu polyline.

## Tổng hợp theo mã
| Mã | Loại lỗi | Số mục kiểm | Số lỗi | Mức |
| --- | --- | ---: | ---: | --- |
| QC1-01 tag camera | sai thuộc tính / bỏ sót | 24 tag (6 ảnh) | 0 | nặng |
| QC1-02 đủ L1, R1 | bỏ sót | 6 ảnh | 2 | nặng |
| QC1-03 position | sai thuộc tính / thừa | 11 lane | 0 | nặng |
| QC1-04 tâm vạch, chiều, điểm dừng | sai phạm vi / bỏ sót | 11 lane | 4 | chính |
| QC1-05 vạch đứt, che | sai phạm vi / sai thuộc tính | 11 lane | 0 | chính |
| QC1-06 style, color, kind | sai thuộc tính | 11 lane | 0 | chính |
| QC1-07 vùng lái | sai phạm vi / bỏ sót / thừa | 5 drivable + 1 crosswalk + 1 road_curb (front) | 0 | chính |
| QC1-08 đèn, màu | bỏ sót / sai phạm vi / sai thuộc tính | 3 traffic_light | 1 | nặng / chính |
| QC1-09 facing, type, group, biển phụ | sai thuộc tính | 3 đèn + 5 biển | 0 | chính |
| QC1-10 hình in, đủ biển | bỏ sót / sai phạm vi | 5 traffic_sign | 1 | chính |
| QC1-11 fisheye | sai phạm vi / sai thuộc tính | 3 shape (B03, B05) | 2 | chính |
| QC1-12 file | lỗi file | 2 zip + manifest | 0 | nhẹ / nặng |

## Danh sách lỗi (mỗi lỗi một dòng)
| # | Mã | Ảnh | Nhãn (label, id) | Mức | Mô tả ngắn |
| --- | --- | --- | --- | --- | --- |
| 1 | QC1-02 | A08 | lane L1 (không có) | nặng | Thiếu L1: vạch trắng đứt bên trái làn đi thấy rõ từ (258, 425) tới (505, 304). Lint cũng báo. |
| 2 | QC1-02 | A10 | lane R1 (không có) | nặng | Thiếu R1: vạch trắng liền bên phải làn đi từ (1190, 658) tới (762, 423), đoạn giữa bị decal trên kính che → vẽ nối qua và bật `occluded`. |
| 3 | QC1-04 | A01 | lane L2, id 4, điểm đầu (0, 569) | chính | Lệch tâm vạch đôi trắng ~23 px: tại x = 100 tâm vạch ở y ≈ 572, polyline ở y ≈ 549. Đặt lại theo tâm hai nét. |
| 4 | QC1-04 | A08 | lane L2 (không có) | chính | Bỏ sót vạch trắng liền bên trái (62, 355) → (450, 288). |
| 5 | QC1-04 | A10 | lane L2 (không có) | chính | Bỏ sót vạch trắng liền bên trái (78, 652) → (519, 330) (mép dải đỗ). Hiện chỉ có `road_curb` ở mép vỉa hè. |
| 6 | QC1-04 | B03 | lane R2 (không có) | chính | Bỏ sót vạch đứt R2 bên phải, thấy rõ từ (1105, 563) tới (888, 347). |
| 7 | QC1-08 | A08 | traffic_light (không có) | chính | Thiếu đèn xe quay về xe đang xanh tại (520, 175)–(537, 197), cao 22 px; cùng ảnh còn 4 cụm vỏ vàng nhìn nghiêng và 2 đèn người đi bộ chưa gán. |
| 8 | QC1-10 | A10 | traffic_sign, id 2 (45, 47)–(91, 132) | chính | Một box gộp hai tấm biển (NO PARKING ANYTIME ở trên, NO STANDING ở dưới). Mỗi tấm cần một box riêng: (46, 49)–(90, 80) và (48, 80)–(91, 125). |
| 9 | QC1-11 | B03 | lane R1, id 0 | chính | Chỉ có 5 điểm, đoạn (847, 494) → (776, 356) nối thẳng, không theo cung; lệch tới ~14 px ở giữa đoạn. Thêm điểm dày ở đoạn cong. |
| 10 | QC1-11 | B05 | road_curb, id 1 | chính | Một polyline nối hai mép khác nhau: vỉa phải (1190, 508) rồi vòng lên mép vỉa hè phía xa sau vạch ngựa vằn tới (420, 86). Chỉ giữ mép vỉa phải, dừng ở chỗ vỉa đổi hướng (~(897, 171)). |

Ảnh được ghi "không lỗi" (để coach kiểm lại): **A04** — 4 tag đúng; L1 vàng đôi, R1 trắng đứt, R2 trắng liền bám vạch; drivable direct/alternative đúng làn.

## Ca mơ hồ
| Ảnh | Câu hỏi cho lead | Lời đáp (nếu có) |
| --- | --- | --- |
| B03 | Ở camera sau, vệt đứt xa phía trái (≈ (471, 355) → (548, 320)) có tính là L1 không? Hiếu không gán, tôi chưa tính lỗi. | |
| A10 | `road_curb` ở mép vỉa hè trái có giữ được khi đã có vạch trắng liền (L2) phía trong không? Chưa tính lỗi. | |
| B05 | Ảnh B05 ghi `weather = clear`; trời ít thấy trong ảnh, tôi chọn overcast. Không tính lỗi (không rõ). | |

## Quyết định
Lỗi nặng: **2**   Lỗi chính: **8 / 52 nhãn = 15,4 %**   Lỗi nhẹ: **0**   Ca chờ lead: **3** (không đổi kết luận)  
Quyết định (Release / Hold / Rework): **Rework**  
Lý do (theo luật của phiếu): còn 2 lỗi nặng QC1-02 (A08 thiếu L1, A10 thiếu R1 — vạch thấy rõ, không thuộc diện miễn); riêng tỉ lệ lỗi chính 15,4 % cũng vượt ngưỡng 5 %. Các ca mơ hồ không ảnh hưởng kết luận nên không ra Hold.

Ghi chú lint toàn lô (không tính vào tỉ lệ vì ngoài mẫu): còn QC1-02 ở A07 (L1), A12 (R1), A14 (R1) — nên rà lại trước khi nộp lại; A05, A06 có thể xin miễn nếu coach xác nhận không thấy vạch.

Loại lỗi: bỏ sót = thiếu nhãn phải có; thừa = gán cái không phải đối tượng; sai phạm vi = hình lệch, sai chiều, dừng sai chỗ, tràn vùng. Ba loại này theo cách chia lỗi gán nhãn của ISO/IEC 5259-4 (mục 8.4.2); "sai thuộc tính" và "lỗi file" là khóa học thêm. Cách xếp mức: [thang mức lỗi](../docs/qc_severity_road_v1.0.md).
