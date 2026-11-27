# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Repo chỉ chứa số đã tổng hợp, script và bảng gắn nhãn (mỗi review trích ≤2 câu). Data thô nằm trong `evidence/raw/` — thư mục này **không commit** (`.gitignore`); chạy lại script là có.

Nhóm đào hai nguồn: **(A) CFPB Consumer Complaint Database** (khiếu nại có nhãn sẵn của cơ quan nhà nước Mỹ) và **(B) review Google Play** của app ví / ngân hàng ở Việt Nam, Mỹ, Anh (nhóm tự gắn nhãn tay). Mentor đã xác nhận được dùng data nhiều nước, không chỉ Việt Nam.

**Khai thật về thứ tự làm (27/11/2026):** trước khi viết file này, nhóm đã đếm thử bằng từ khoá trên review Google Play và xem số CFPB của hai khoảng thời gian để chọn hướng trong Track E (xem `evidence/hypothesis.md`). Số đếm thử bằng từ khoá **không** dùng làm bằng chứng. Bằng chứng chính thức là (A) số đếm theo nhãn của CFPB và (B) mẫu review gắn nhãn tay theo định nghĩa ghi ở §1 dưới đây, trước khi gắn nhãn.

---

## 1. Cách đếm — viết TRƯỚC khi chạy

### (A) CFPB

- **Data:** CFPB Consumer Complaint Database, lọc *Date received* 27/11/2025 → 27/11/2026 và *Product* = *Money transfer, virtual currency, or money service*. Tải ngày 27/11/2026 (database cập nhật lần cuối 26/11/2026).
- **Link bộ lọc:** https://www.consumerfinance.gov/data-research/consumer-complaints/search/?dateRange=1y&date_received_max=2026-11-27&date_received_min=2025-11-27&page=1&product=Money%20transfer%2C%20virtual%20currency%2C%20or%20money%20service&searchField=all&size=25&sort=created_date_desc
- **Cách tải:** mở link trên → *Download data* → *Filtered dataset* → CSV → lưu vào `evidence/raw/`.
- **Đếm gì:** số khiếu nại theo cột `Issue` (nhãn do CFPB gắn, nhóm không gắn lại).
- **Mẫu số:** mọi khiếu nại trong bộ lọc (N = 38.899).
- **Nhãn coi là liên quan hướng E3:** *Fraud or scam* · *Unauthorized transactions or other transaction problem* · *Trouble accessing funds in your mobile or digital wallet*.
- **Script:** `python evidence/scripts/count_cfpb.py evidence/raw/<file>.csv`

### (B) Review Google Play

- **Data:** 1.000 review mới nhất mỗi app, mọi mức sao, lấy ngày 27/11/2026 bằng `evidence/scripts/scrape_reviews.py` (thư viện `google-play-scraper`). Không lưu tên người viết.
  - VN (tiếng Việt, cửa hàng VN): MoMo, ZaloPay, MB Bank, Vietcombank, Techcombank, VietinBank, BIDV, TPBank
  - Mỹ (tiếng Anh): Cash App, Chime, Venmo, PayPal · Anh (tiếng Anh): Revolut, Monzo, Wise
  - Tổng 15.000 review. Ngày review mỗi app khác nhau (app ít review thì 1.000 review trải dài hơn), sớm nhất 30/05/2026, muộn nhất 26/11/2026.
- **Cách chọn mẫu** (`evidence/scripts/sample_reviews.py`):
  - Chỉ giữ review **1–2 sao**, nội dung **dài hơn 20 ký tự** (bỏ các review chỉ có "tệ", "ok"). Mẫu nghiêng về phía phàn nàn — đây là chủ ý, vì đang đếm *loại* phàn nàn.
  - Lấy **ngẫu nhiên 200 review VN + 200 review Mỹ/Anh = 400 review**, seed 42. Chạy lại script ra đúng 400 review này.
  - Mỗi review trích tối đa 2 câu vào `evidence/reviews_labeled.csv`.
- **Mẫu số:** N = 400 (và N = 200 cho từng nhóm thị trường), **kể cả review không liên quan**.
- **Nhãn** — mỗi review có thể mang nhiều nhãn, điền `1` vào cột tương ứng:

  | Cột | Gắn `1` khi review nói về… | Không gắn khi… |
  |---|---|---|
  | `nhan_khoa_giu` | Tài khoản, ví hoặc giao dịch **bị app/ngân hàng khoá, đóng băng, tạm giữ, chặn** — người dùng không chuyển hoặc rút được tiền của mình | Không đăng nhập được vì lỗi app, quên mật khẩu, xác thực khuôn mặt thất bại (đó là lỗi kỹ thuật, không phải bị giữ) |
  | `nhan_lua_dao` | Bị **lừa đảo**, giao dịch **không phải do mình làm**, bị **chiếm tài khoản**, mất tiền vì kẻ gian | Chỉ chửi app là "lừa đảo" vì thu phí, quảng cáo, khuyến mãi không như hứa |
  | `nhan_ho_tro_kem` | Hỗ trợ **chậm, không trả lời, trả lời chung chung**, chatbot/AI không hiểu, bắt chờ nhiều ngày, đẩy qua lại | Chỉ nói app tệ mà không nhắc tới kênh hỗ trợ |
  | `nhan_khac` | Không thuộc ba nhãn trên (lag, lỗi app, phí, quảng cáo, giao diện, khen…) | Đã gắn ít nhất một trong ba nhãn trên |

  Ví dụ: *"bị khoá ví lúc đang gấp, chat 12 tiếng không ai trả lời"* → `nhan_khoa_giu = 1` và `nhan_ho_tro_kem = 1`.

  **Quy tắc ranh giới — làm rõ ngày 27/11/2026, SAU khi đã gắn nhãn nháp, khi Cường kiểm lại phát hiện 4 cặp review giống nhau mà nhãn khác nhau; áp lại cho cả 400 review:**
  1. `nhan_khoa_giu` chỉ khi người dùng nói app / ngân hàng **hạn chế, chặn, treo "đang xử lý"** việc dùng tiền hoặc tài khoản. Nói app **lỗi, không chạy** → `nhan_khac`. Giao dịch **lỗi mà vẫn bị trừ tiền, chưa hoàn** cũng là `nhan_khac` (đó là hướng H1 đã loại, không phải bị giữ).
  2. `nhan_lua_dao` chỉ khi review kể **việc đã xảy ra với chính người viết** (bị lừa, mất tiền, bị chiếm tài khoản). Cảnh báo chung chung hoặc hành vi chưa thành → không gắn.
  3. Cáo buộc nhân viên / bên khác lấy tiền chỉ gắn `nhan_lua_dao` khi review **mô tả một giao dịch / lần mất tiền cụ thể**.

  Áp lại cho cả file: **2 dòng đổi** — stt 308 (bỏ `lua_dao` → `khac`) và stt 384 (bỏ `lua_dao`, giữ `ho_tro_kem`). Các cặp 305/391, 52/92, 46/174 giữ nguyên vì đã khớp quy tắc.
- **Người gắn nhãn:** Claude (trợ lý AI) gắn **nhãn nháp** cho cả 400 review theo đúng định nghĩa trên; ca khó quyết có lý do ghi ở cột `ghi_chu`. Nguyễn Thế Cường **đã đọc lại cả 400/400 dòng** (27/11/2026), làm rõ 3 quy tắc ranh giới ở trên và sửa 2 dòng — đây là bản dùng để đếm. Nguyễn Thị Thu Hà gắn độc lập 40 review (stt 1–20 và 201–220) **không nhìn nhãn nháp** để so; lệch ≥ 8/40 review thì viết lại định nghĩa nhãn rồi gắn lại — kết quả khớp **37/40** (xem dưới bảng kết quả). Việc dùng AI ghi trong `docs/ai-usage.md`.
- **Script đếm:** `python evidence/scripts/count_labels.py`

### Chạy lại từ đầu

```
python -m pip install google-play-scraper
python evidence/scripts/scrape_reviews.py      # → evidence/raw/reviews_raw.csv
python evidence/scripts/sample_reviews.py      # → evidence/reviews_labeled.csv
python evidence/scripts/count_labels.py        # sau khi gắn nhãn
python evidence/scripts/count_cfpb.py evidence/raw/<file CFPB>.csv
```

Lưu ý: review mới liên tục được thêm, nên chạy lại `scrape_reviews.py` vào ngày khác sẽ ra tập review khác. Bảng gắn nhãn đã commit là bản dùng để chấm.

---

## 2. Đọc trước, đếm sau

- **CFPB:** đã đọc từ điển cột và 25 khiếu nại mới nhất trên trang tìm kiếm. Mỗi dòng là một khiếu nại, có `Product`, `Sub-product`, `Issue`, `Sub-issue`, `Company`, `Company response to consumer`. Với dữ liệu này, cột lời kể (`Consumer complaint narrative`) và `Sub-issue` đều trống.
- **Review Google Play:** khi đọc thử review 1–2 sao, các *kiểu* phàn nàn thấy được:
  - lỗi đăng nhập, xác thực khuôn mặt / OTP, đổi điện thoại (rất nhiều ở app ngân hàng VN)
  - app lag, văng, bảo trì
  - tiền bị trừ mà giao dịch chưa tới, phải chờ hoặc không hoàn
  - tài khoản / ví bị khoá, đóng băng, giữ tiền (nhiều ở app Mỹ)
  - bị lừa, giao dịch trái phép, bị chiếm tài khoản (nhiều ở app Mỹ)
  - hỗ trợ chậm, chatbot trả lời lạc ý
  - phí, tự gia hạn, quảng cáo

---

## 3. Kết quả

### (A) CFPB — N = 38.899 khiếu nại, ngày nhận 27/11/2025 → 25/11/2026

| Issue (nhãn CFPB) | x / N | % | Ghi chú |
|---|---|---|---|
| Fraud or scam | 11.467 / 38.899 | 29,5% | lừa đảo |
| Unauthorized transactions or other transaction problem | 7.234 / 38.899 | 18,6% | giao dịch không phải do mình làm |
| Other transaction problem | 6.070 / 38.899 | 15,6% | nhãn chung chung |
| Trouble accessing funds in your mobile or digital wallet | 4.140 / 38.899 | 10,6% | không dùng được tiền trong ví |
| Money was not available when promised | 2.956 / 38.899 | 7,6% | |
| Managing, opening, or closing your mobile wallet account | 2.688 / 38.899 | 6,9% | |
| Problem with customer service | 600 / 38.899 | 1,5% | |
| 9 nhãn còn lại | mỗi nhãn ≤ 1.064 | ≤ 2,7% | |
| **Fraud or scam + Unauthorized** | **18.701 / 38.899** | **48,1%** | |
| **Ba nhãn E3 cộng lại** | **22.841 / 38.899** | **58,7%** | |

- Công ty bị khiếu nại nhiều nhất ở ba nhãn E3: PayPal 6.839 · Block (Cash App) 6.784 · Chime 1.374 · Wells Fargo 1.049 · JPMorgan Chase 1.002.
- Phản hồi của công ty: Closed with explanation 31.379 · Closed with monetary relief 3.246 · Closed with non-monetary relief 2.551 · In progress 1.466 · Untimely response 257.
- **Đối chiếu, cả năm 2025** (lấy qua API ngày 27/11/2026, cùng bộ lọc Product): N = 84.619; Fraud or scam 11.179 (13,2%); Unauthorized 5.758 (6,8%); Trouble accessing funds 3.038 (3,6%). Năm 2025 nhãn chung chung *Other transaction problem* chiếm 53.893 (63,7%), nên các nhãn cụ thể bị pha loãng. Nhóm chọn **12 tháng gần nhất làm số chính** vì là data mới nhất, và báo cả hai khoảng để người đọc tự so.

### (B) Review Google Play — N = 400 · nhãn nháp của Claude, **Cường đã kiểm 400/400, sửa 2 dòng** (27/11/2026)

| Đếm gì | VN (N = 200) | Mỹ/Anh (N = 200) | Cả mẫu (N = 400) |
|---|---|---|---|
| `nhan_khoa_giu` | 10/200 (5,0%) | 28/200 (14,0%) | 38/400 (9,5%) |
| `nhan_lua_dao` | 3/200 (1,5%) | 8/200 (4,0%) | 11/400 (2,8%) |
| `nhan_khoa_giu` HOẶC `nhan_lua_dao` | 13/200 (6,5%) | 35/200 (17,5%) | 48/400 (12,0%) |
| `nhan_ho_tro_kem` | 14/200 (7,0%) | 39/200 (19,5%) | 53/400 (13,2%) |
| `nhan_khac` | 176/200 (88,0%) | 134/200 (67,0%) | 310/400 (77,5%) |
| Độ khớp giữa hai người gắn nhãn (40 review) | 20/20 | 17/20 | **37/40** (lệch 3 < ngưỡng 8 → giữ định nghĩa) |

So với giả thuyết (`evidence/hypothesis.md`, ngưỡng `khoa_giu HOẶC lua_dao` ≥ 10% trong mẫu 1–2 sao): **cả mẫu 12,0% → đạt**; nhưng **riêng VN chỉ 6,5% → dưới ngưỡng**, Mỹ/Anh 17,5%. (Trước khi kiểm: cả mẫu 12,5%, Mỹ/Anh 18,5%.) Pain này rõ ở thị trường Mỹ/Anh hơn ở VN; review VN 1–2 sao chủ yếu là lỗi đăng nhập, xác thực, lag (nằm trong `nhan_khac`). Phải kiểm lại bằng phỏng vấn ở VN.

**Gắn nhãn độc lập (Nguyễn Thị Thu Hà, 40 review stt 1–20 và 201–220, không nhìn nhãn nháp; `python evidence/scripts/compare_labels.py`):** khớp **37/40**. Theo nhãn: `khoa_giu` 38/40 · `lua_dao` 40/40 · `ho_tro_kem` 39/40 · `khac` 38/40. Ba review lệch đều thuộc Mỹ/Anh:
- stt 203 (*"Won't let me pay anyone"*) và stt 205 (*"someone sent me Money this morning and I still haven't received it"*): bảng chính gắn `khac`, Hà gắn `khoa_giu`. Cả hai câu không nói rõ ví chặn hay giữ, nên bảng chính theo quy tắc "không nói rõ thì không gắn". Nếu tính theo Hà, `khoa_giu HOẶC lua_dao` ở Mỹ/Anh tăng từ 35 lên 37/200 → **số chính có thể đang hơi thấp, không bị thổi lên**.
- stt 204: bảng chính gắn `khoa_giu` + `ho_tro_kem` ("they are no help at all"), Hà chỉ gắn `khoa_giu` (có ghi "kèm hỗ trợ kém" ở `ghi_chu`). Hà gắn mỗi review đúng 1 nhãn, trong khi định nghĩa cho phép nhiều nhãn → cần nói rõ hơn ở hướng dẫn gắn nhãn.

---

## 4. Ví dụ cụ thể (trích ≤ 2 câu, bỏ tên người viết)

1. *"nhưng cskh không có ai hỗ trợ qua kênh chat, ticket mở hơn 12 tiếng không thấy phản hồi. tiền bị momo giữ không thể rút"* — MoMo, Google Play VN, 1★, 23/11/2026
2. *"không bảo mật tốt cho tài khoản người dùng, trừ tiền không rõ nguyên nhân, không hỗ trợ tốt cho người bị lừa đảo"* — MoMo, Google Play VN, 1★, 24/11/2026
3. *"ngân hàng phong toả tk của khách hàng mà ko thông báo cho khách hàng."* — MB Bank, Google Play VN, 1★, 26/11/2026
4. *"rất là rườm rà rắc rối, đánh giá nửa của 1 sao, tài khoản bị khoá ngay lúc cần ck cho shipper"* — BIDV, Google Play VN, 1★, 22/11/2026
5. *"chuyển tiền thì trừ tiền nhưng báo lỗi xong không chuyển tiền quá,gọi cskh thì AI trả lời???"* — MB Bank, Google Play VN, 1★, 23/11/2026
6. *"they are complicit with scammers and thieves. had over $8000 stolen and all they said was "there is nothing we can do""* — Cash App, Google Play US, 1★, 26/11/2026
7. *"They can suspend your account without any warning. Ive been in good standing for years then all of a sudden my account has been frozen"* — Cash App, Google Play US, 1★, 24/11/2026

Link nguồn: trang Google Play của từng app (danh sách package id ở `evidence/scripts/scrape_reviews.py`), xem ngày 27/11/2026. Ví dụ lấy từ tập 15.000 review; sau khi gắn nhãn sẽ bổ sung ví dụ từ chính mẫu 400 review.

---

## 5. Giới hạn của data

- **CFPB là thị trường Mỹ** và chỉ gồm người chịu bỏ công nộp khiếu nại lên cơ quan nhà nước. Số này cho thấy lừa đảo / giao dịch trái phép là nhóm khiếu nại lớn nhất của ví điện tử ở Mỹ, **không** cho biết tỉ lệ ở Việt Nam.
- **CFPB không có lời kể** cho dữ liệu này, nên không biết người khiếu nại đã liên hệ hỗ trợ ra sao. Có 1.466 khiếu nại (3,8%) còn "In progress"; tải lại ngày khác số có thể nhích nhẹ.
- **Review là người đang bực** viết: % trong review 1–2 sao không phải % của mọi người dùng, chỉ là % *trong số phàn nàn*.
- Mỗi app 1.000 review mới nhất nên **khoảng thời gian khác nhau giữa các app** (vài ngày tới vài tháng), app nhiều review mới chiếm phần lớn mẫu.
- Data cho biết người ta phàn nàn **gì**, không cho biết **vì sao** và họ đã xử lý thế nào.

→ **Kiểm lại bằng phỏng vấn ≥ 3 người dùng ví ở Việt Nam, ngoài nhóm** (`evidence/interviews/`): lần gần nhất bị giữ giao dịch hoặc nhận cuộc gọi / tin nhắn giục chuyển tiền là khi nào, đã liên hệ hỗ trợ thế nào, mất bao lâu.
