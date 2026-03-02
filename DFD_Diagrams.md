# 2.5. Mô hình hóa tiến trình nghiệp vụ

## 2.5.1. Ký hiệu sử dụng

| STT | Ký hiệu | Giải thích |
| :---: | :---: | ----- |
| 1 | Hình chữ nhật | Tác nhân trong/ngoài |
| 2 | Hình chữ nhật bo tròn | Tiến trình |
| 3 | Mũi tên | Luồng dữ liệu |
| 4 | Hình trụ | Kho dữ liệu |

Quy ước trong sơ đồ Mermaid:
- `["Tên"]` — Tác nhân (hình chữ nhật)
- `("Tên")` — Tiến trình (hình bo tròn)
- `[("Tên")]` — Kho dữ liệu (hình trụ)
- `-->|"Mô tả"|` — Luồng dữ liệu (mũi tên có nhãn)

---

## 2.5.2. Sơ đồ luồng dữ liệu (DFD) mức ngữ cảnh

Sơ đồ luồng dữ liệu mức ngữ cảnh thể hiện tổng quát hệ thống quản lý tài chính cá nhân như một tiến trình trung tâm duy nhất, tương tác với hai tác nhân bên ngoài: **Người dùng** và **Quản trị hệ thống**.

```mermaid
flowchart LR
    ND["Người dùng"]
    P0("0. Hệ thống quản lý<br/>tài chính cá nhân")
    QT["Quản trị viên"]

    ND -->|"TT đăng ký, đăng nhập<br/>Dữ liệu giao dịch thu chi<br/>Cấu hình ví, ngân sách, mục tiêu<br/>Câu hỏi AI Chatbot"| P0

    P0 -->|"Kết quả xác thực<br/>Báo cáo thu chi, số dư ví<br/>Cảnh báo ngân sách, thông báo<br/>Phản hồi AI Chatbot"| ND

    QT -->|"TT đăng nhập quản trị<br/>Thao tác quản lý người dùng<br/>Cấu hình hệ thống"| P0

    P0 -->|"DS và trạng thái người dùng<br/>Thống kê tổng quan hệ thống<br/>Thống kê phản hồi AI"| QT
```

*Hình 2.4 Sơ đồ DFD mức ngữ cảnh*

**Mô tả luồng dữ liệu:**

| STT | Luồng | Mô tả |
|-----|-------|-------|
| 1 | Người dùng → Hệ thống | Thông tin đăng ký, đăng nhập; dữ liệu giao dịch thu chi; thông tin ví; cấu hình ngân sách, mục tiêu; câu hỏi gửi đến AI Chatbot |
| 2 | Hệ thống → Người dùng | Kết quả xác thực; báo cáo thu chi; số dư ví; cảnh báo vượt ngân sách; kết quả import; phản hồi và gợi ý từ AI Chatbot; thông báo hệ thống |
| 3 | Quản trị → Hệ thống | Thông tin đăng nhập quản trị; thao tác quản lý tài khoản người dùng; cấu hình danh mục hệ thống; cấu hình và giám sát AI Chatbot |
| 4 | Hệ thống → Quản trị | Danh sách và trạng thái người dùng; báo cáo thống kê tổng quan hệ thống; log hoạt động; trạng thái AI Chatbot |

---

## 2.5.3. DFD mức đỉnh

Sơ đồ luồng dữ liệu mức đỉnh phân rã tiến trình trung tâm "Hệ thống quản lý tài chính cá nhân" thành **8 tiến trình con** tương ứng với 8 nhóm chức năng đã xác định, cùng **9 kho dữ liệu**, 2 tác nhân bên ngoài và **các luồng liên tiến trình** (P13 điều phối giao dịch kích hoạt P08, P12).

```mermaid
flowchart TB
    %% === TÁC NHÂN ===
    ND["Người dùng"]
    QT["Quản trị viên"]
    HT["Hệ thống<br/>Scheduler"]

    %% === TIẾN TRÌNH ===
    P1("1.0<br/>Quản lý tài khoản")
    P2("2.0<br/>Quản lý ví")
    P3("3.0<br/>Quản lý thu chi")
    P4("4.0<br/>Quản lý ngân sách")
    P5("5.0<br/>Quản lý thông báo")
    P6("6.0<br/>Báo cáo thống kê")
    P7("7.0<br/>AI Chatbot")
    P8("8.0<br/>Quản lý hệ thống")

    %% === KHO DỮ LIỆU ===
    D1[("D1 Tài khoản")]
    D2[("D2 Ví")]
    D3[("D3 Giao dịch")]
    D4[("D4 Danh mục")]
    D5[("D5 Ngân sách")]
    D6[("D6 Mục tiêu")]
    D7[("D7 Thông báo")]
    D8[("D8 Cấu hình<br/>định kỳ")]
    D9[("D9 Lịch sử<br/>chat")]

    %% === LUỒNG: NGƯỜI DÙNG -> TIẾN TRÌNH ===
    ND -->|"TT đăng ký, đăng nhập"| P1
    ND -->|"TT ví, cấu hình"| P2
    ND -->|"Dữ liệu giao dịch, file Excel"| P3
    ND -->|"Cấu hình ngưỡng theo ví/DM"| P4
    ND -->|"Cấu hình thông báo"| P5
    ND -->|"Tiêu chí báo cáo"| P6
    ND -->|"Câu hỏi, yêu cầu phân tích"| P7

    %% === LUỒNG: TIẾN TRÌNH -> NGƯỜI DÙNG ===
    P1 -->|"Kết quả xác thực, OTP"| ND
    P2 -->|"DS ví, số dư"| ND
    P3 -->|"DS giao dịch, file Excel xuất"| ND
    P4 -->|"DS cảnh báo chi tiêu"| ND
    P5 -->|"DS thông báo"| ND
    P6 -->|"Biểu đồ, bảng thống kê"| ND
    P7 -->|"Phản hồi NLP, phân tích, tư vấn"| ND

    %% === LUỒNG: QUẢN TRỊ ===
    QT -->|"Thao tác quản lý ND, giám sát AI"| P8
    P8 -->|"DS người dùng, thống kê AI"| QT

    %% === LUỒNG: HỆ THỐNG SCHEDULER ===
    HT -->|"Kích hoạt GD định kỳ"| P3
    HT -->|"Kích hoạt gửi TB định kỳ"| P5

    %% === LUỒNG LIÊN TIẾN TRÌNH (P13 ĐIỀU PHỐI) ===
    P3 -.->|"GD mới → Kiểm tra ngân sách<br/>P13 điều phối"| P4
    P3 -.->|"GD mới → Cập nhật mục tiêu<br/>P08 tính % hoàn thành"| P1
    P4 -.->|"Cảnh báo vượt NS"| P5

    %% === LUỒNG: TIẾN TRÌNH <-> KHO DỮ LIỆU ===
    P1 <-->|"TT tài khoản"| D1
    P1 <-->|"Mục tiêu chung"| D6
    P2 <-->|"TT ví"| D2
    P2 <-->|"Cấu hình NS"| D5
    P2 <-->|"Mục tiêu theo ví"| D6
    P3 <-->|"Bản ghi GD"| D3
    P3 -->|"Cập nhật số dư"| D2
    P3 -->|"Đọc danh mục"| D4
    P3 <-->|"CH định kỳ"| D8
    P4 -->|"Đọc NS"| D5
    P4 -->|"Đọc GD"| D3
    P4 -->|"Lưu cảnh báo"| D7
    P5 <-->|"Thông báo"| D7
    P6 -->|"Đọc GD"| D3
    P6 -->|"Đọc ví"| D2
    P6 -->|"Đọc DM"| D4
    P7 -->|"Đọc GD"| D3
    P7 -->|"Đọc NS"| D5
    P7 -->|"Đọc MT"| D6
    P7 <-->|"Lịch sử chat"| D9
    P8 -->|"Đọc TT ND"| D1
    P8 -->|"Đọc phản hồi"| D9
```

*Hình 2.5 Sơ đồ DFD mức đỉnh*

**Danh sách tác nhân:**

| Ký hiệu | Tên | Mô tả |
|----------|-----|-------|
| ND | Người dùng | Cá nhân sử dụng hệ thống quản lý tài chính |
| QT | Quản trị viên | Người vận hành, giám sát hệ thống |
| HT | Hệ thống (Scheduler) | Bộ lập lịch tự động kích hoạt GD định kỳ (P11) và gửi thông báo (P16) |

**Danh sách kho dữ liệu:**

| Ký hiệu | Tên kho dữ liệu | Mô tả |
|----------|-----------------|-------|
| D1 | Tài khoản | Lưu trữ thông tin tài khoản người dùng, cấu hình cá nhân, mục tiêu |
| D2 | Ví | Thông tin ví tài chính, số dư hiện tại |
| D3 | Giao dịch | Các bản ghi giao dịch thu/chi (thủ công, import, định kỳ) |
| D4 | Danh mục | Danh mục phân loại giao dịch (Ăn uống, Di chuyển, ...) |
| D5 | Ngân sách | Cấu hình ngân sách chi tiêu theo ví/danh mục, ngưỡng cảnh báo |
| D6 | Mục tiêu | Mục tiêu tài chính chung và theo ví, tiến độ hoàn thành |
| D7 | Thông báo | Thông báo hệ thống, cảnh báo ngân sách, cấu hình gửi TB |
| D8 | Cấu hình định kỳ | Cấu hình giao dịch thu/chi cố định, trạng thái, thời điểm tiếp theo |
| D9 | Lịch sử chat | Lịch sử hội thoại AI Chatbot, câu hỏi và phản hồi |

**Luồng liên tiến trình (nét đứt):**

| Luồng | Mô tả | Quy trình liên quan |
|-------|-------|--------------------|
| 3.0 → 4.0 | Sau khi tạo giao dịch, kích hoạt kiểm tra ngân sách | P13 → P12 |
| 3.0 → 1.0 | Sau khi tạo giao dịch, cập nhật % hoàn thành mục tiêu | P13 → P08 |
| 4.0 → 5.0 | Khi vượt ngân sách, gửi cảnh báo ngay lập tức | P12 → P16 |

---

## 2.5.4. DFD mức dưới đỉnh

### 2.5.4.1. DFD mức 2 – Quản lý tài khoản

Phân rã tiến trình **1.0 Quản lý tài khoản** thành 4 tiến trình con tương ứng với các quy trình P01, P02, P03, P04.

```mermaid
flowchart TB
    ND["Người dùng"]
    D1[("D1 Tài khoản")]
    D6[("D6 Mục tiêu")]

    P11("1.1 Đăng ký<br/>tài khoản")
    P12("1.2 Đăng nhập")
    P13("1.3 Cập nhật<br/>thông tin")
    P14("1.4 Thiết lập<br/>mục tiêu")

    ND -->|"Email, mật khẩu, họ tên"| P11
    P11 -->|"Mã OTP"| ND
    P11 -->|"Kết quả đăng ký"| ND
    P11 -->|"Lưu TT tài khoản"| D1

    ND -->|"Email, mật khẩu"| P12
    P12 -->|"Đọc TT xác thực"| D1
    P12 -->|"Phiên đăng nhập"| ND

    ND -->|"TT cá nhân, tiền tệ, nghề nghiệp"| P13
    P13 -->|"Cập nhật TT"| D1
    P13 -->|"Kết quả cập nhật"| ND

    ND -->|"Tên MT, số tiền, thời hạn"| P14
    P14 -->|"Lưu mục tiêu"| D6
    P14 -->|"Kết quả thiết lập"| ND
```

*Hình 2.6 DFD mức 2 – Quản lý tài khoản*

---

### 2.5.4.2. DFD mức 2 – Quản lý ví

Phân rã tiến trình **2.0 Quản lý ví** thành 4 tiến trình con tương ứng với các quy trình P05, P06, P07.

```mermaid
flowchart TB
    ND["Người dùng"]
    D2[("D2 Ví")]
    D5[("D5 Ngân sách")]
    D6[("D6 Mục tiêu")]

    P21("2.1 Tạo ví")
    P22("2.2 Sửa ví")
    P23("2.3 Cấu hình<br/>ngân sách theo ví")
    P24("2.4 Cấu hình<br/>mục tiêu theo ví")

    ND -->|"Tên ví, số dư ban đầu"| P21
    P21 -->|"Lưu TT ví"| D2
    P21 -->|"Kết quả tạo ví"| ND

    ND -->|"TT ví cập nhật"| P22
    P22 <-->|"TT ví"| D2
    P22 -->|"Kết quả sửa ví"| ND

    ND -->|"Hạn mức, chu kỳ, ngưỡng"| P23
    P23 -->|"Đọc TT ví"| D2
    P23 -->|"Lưu cấu hình NS"| D5
    P23 -->|"Kết quả cấu hình"| ND

    ND -->|"Tên MT, số tiền, thời hạn, ví"| P24
    P24 -->|"Đọc TT ví"| D2
    P24 -->|"Lưu MT theo ví"| D6
    P24 -->|"Kết quả cấu hình"| ND
```

*Hình 2.7 DFD mức 2 – Quản lý ví*

---

### 2.5.4.3. DFD mức 2 – Quản lý thu chi

Phân rã tiến trình **3.0 Quản lý thu chi** thành 7 tiến trình con tương ứng với các quy trình P09, P10, P11, P13, P08, P12. Bao gồm tiến trình **3.6 Điều phối giao dịch (P13)** — tiến trình nội bộ tự động kích hoạt kiểm tra ngân sách và cập nhật mục tiêu sau mỗi giao dịch.

```mermaid
flowchart TB
    ND["Người dùng"]
    HT["Hệ thống<br/>Scheduler"]
    D2[("D2 Ví")]
    D3[("D3 Giao dịch")]
    D4[("D4 Danh mục")]
    D5[("D5 Ngân sách")]
    D6[("D6 Mục tiêu")]
    D7[("D7 Thông báo")]
    D8[("D8 Cấu hình<br/>định kỳ")]

    P31("3.1 Tạo giao dịch<br/>thủ công")
    P32("3.2 Import từ<br/>file Excel")
    P33("3.3 Cấu hình khoản<br/>thu chi cố định")
    P34("3.4 Xem DS<br/>giao dịch")
    P35("3.5 Xuất dữ liệu<br/>ra file Excel")
    P36("3.6 Điều phối<br/>giao dịch - P13")
    P37("3.7 Tạo GD định kỳ<br/>tự động - P11")

    %% === TẠO GIAO DỊCH THỦ CÔNG ===
    ND -->|"Số tiền, danh mục, ví, ngày, ghi chú"| P31
    P31 -->|"Đọc danh mục"| D4
    P31 -->|"Lưu giao dịch"| D3
    P31 -->|"Cập nhật số dư"| D2
    P31 -->|"Kết quả tạo GD"| ND
    P31 -.->|"GD thành công"| P36

    %% === IMPORT EXCEL ===
    ND -->|"File Excel"| P32
    P32 -->|"Đọc danh mục"| D4
    P32 -->|"Lưu giao dịch hợp lệ"| D3
    P32 -->|"Cập nhật số dư"| D2
    P32 -->|"Kết quả import, DS lỗi"| ND
    P32 -.->|"GD thành công"| P36

    %% === CẤU HÌNH ĐỊNH KỲ ===
    ND -->|"Ví, số tiền, DM, chu kỳ, trạng thái"| P33
    P33 -->|"Lưu cấu hình"| D8
    P33 -->|"Kết quả cấu hình"| ND

    %% === SCHEDULER TẠO GD TỰ ĐỘNG ===
    HT -->|"Kiểm tra CH đến hạn"| P37
    P37 -->|"Đọc CH active"| D8
    P37 -->|"Tạo GD tự động"| D3
    P37 -->|"Cập nhật số dư"| D2
    P37 -->|"Cập nhật thời điểm tiếp theo"| D8
    P37 -->|"TB giao dịch định kỳ"| D7
    P37 -.->|"GD thành công"| P36

    %% === ĐIỀU PHỐI GIAO DỊCH P13 ===
    P36 -->|"Đọc cấu hình NS"| D5
    P36 -->|"Đọc GD trong kỳ"| D3
    P36 -->|"Tạo cảnh báo NS"| D7
    P36 -->|"Đọc MT liên quan"| D6
    P36 -->|"Cập nhật % MT"| D6

    %% === XEM DS GIAO DỊCH ===
    ND -->|"Bộ lọc: thời gian, ví, DM, loại"| P34
    P34 -->|"Đọc giao dịch"| D3
    P34 -->|"DS giao dịch phân trang"| ND

    %% === XUẤT EXCEL ===
    ND -->|"Tiêu chí xuất"| P35
    P35 -->|"Đọc giao dịch"| D3
    P35 -->|"File Excel"| ND
```

*Hình 2.8 DFD mức 2 – Quản lý thu chi*

> **Ghi chú:** Nét đứt (`-.->`) thể hiện luồng kích hoạt nội bộ. Sau khi giao dịch được tạo thành công (từ 3.1, 3.2 hoặc 3.7), hệ thống tự động kích hoạt tiến trình **3.6 Điều phối giao dịch (P13)** để:
> - Kiểm tra cấu hình ngân sách → tạo cảnh báo nếu vượt ngưỡng (P12)
> - Kiểm tra mục tiêu tài chính → cập nhật % hoàn thành (P08)

---

### 2.5.4.4. DFD mức 2 – Quản lý ngân sách

Phân rã tiến trình **4.0 Quản lý ngân sách** thành 3 tiến trình con tương ứng với quy trình P12.

```mermaid
flowchart TB
    ND["Người dùng"]
    D3[("D3 Giao dịch")]
    D5[("D5 Ngân sách")]
    D7[("D7 Thông báo")]

    P41("4.1 Cấu hình ngưỡng<br/>CB theo ví")
    P42("4.2 Cấu hình ngưỡng<br/>CB theo danh mục")
    P43("4.3 Xem DS<br/>cảnh báo chi tiêu")

    ND -->|"Ví, ngưỡng cảnh báo"| P41
    P41 -->|"Lưu cấu hình"| D5
    P41 -->|"Đọc GD ví"| D3
    P41 -->|"Tạo cảnh báo"| D7
    P41 -->|"Kết quả cấu hình"| ND

    ND -->|"Danh mục, ngưỡng CB"| P42
    P42 -->|"Lưu cấu hình"| D5
    P42 -->|"Đọc GD theo DM"| D3
    P42 -->|"Tạo cảnh báo"| D7
    P42 -->|"Kết quả cấu hình"| ND

    ND -->|"Bộ lọc"| P43
    P43 -->|"Đọc cảnh báo"| D7
    P43 -->|"DS cảnh báo"| ND
```

*Hình 2.9 DFD mức 2 – Quản lý ngân sách*

---

### 2.5.4.5. DFD mức 2 – Quản lý thông báo

Phân rã tiến trình **5.0 Quản lý thông báo** thành 4 tiến trình con tương ứng với các quy trình P15, P16. Bao gồm tiến trình **5.4 Gửi thông báo tự động (P16)** — nhận cảnh báo từ tiến trình 4.0 và gửi TB theo lịch.

```mermaid
flowchart TB
    ND["Người dùng"]
    HT["Hệ thống<br/>Scheduler"]
    D3[("D3 Giao dịch")]
    D7[("D7 Thông báo")]

    P51("5.1 Bật/Tắt<br/>thông báo")
    P52("5.2 Cấu hình thời gian<br/>gửi thông báo")
    P53("5.3 Xem DS<br/>thông báo")
    P54("5.4 Gửi thông báo<br/>tự động - P16")

    ND -->|"Trạng thái bật/tắt"| P51
    P51 -->|"Cập nhật cấu hình"| D7
    P51 -->|"Kết quả cập nhật"| ND

    ND -->|"Tần suất, thời điểm, loại BC"| P52
    P52 -->|"Lưu cấu hình lịch"| D7
    P52 -->|"Kết quả cấu hình"| ND

    ND -->|"Bộ lọc: thời gian, loại, trạng thái"| P53
    P53 -->|"Đọc thông báo"| D7
    P53 -->|"DS thông báo phân trang"| ND

    HT -->|"Kiểm tra TB đến hạn"| P54
    P54 -->|"Đọc cấu hình gửi"| D7
    P54 -->|"Đọc dữ liệu BC"| D3
    P54 -->|"Lưu TB đã gửi"| D7
    P54 -->|"Email / TB nội bộ"| ND
```

*Hình 2.10 DFD mức 2 – Quản lý thông báo*

> **Ghi chú:** Tiến trình 5.4 xử lý hai loại thông báo:
> - **Thông báo theo lịch**: Gửi báo cáo định kỳ (tuần/tháng/quý/năm) theo cấu hình P15
> - **Thông báo tức thì**: Cảnh báo vượt ngân sách (từ P12), hoàn thành/quá hạn mục tiêu (từ P08) — gửi ngay không phụ thuộc lịch

---

### 2.5.4.6. DFD mức 2 – Quản lý báo cáo thống kê

Phân rã tiến trình **6.0 Báo cáo thống kê** thành 3 tiến trình con tương ứng với quy trình P14.

```mermaid
flowchart TB
    ND["Người dùng"]
    D2[("D2 Ví")]
    D3[("D3 Giao dịch")]
    D4[("D4 Danh mục")]

    P61("6.1 Báo cáo thống kê<br/>chi tiêu theo ví")
    P62("6.2 Báo cáo thống kê<br/>chi tiêu theo danh mục")
    P63("6.3 Báo cáo thống kê<br/>chi tiêu theo thời gian")

    ND -->|"Khoảng thời gian"| P61
    P61 -->|"Đọc giao dịch"| D3
    P61 -->|"Đọc TT ví"| D2
    P61 -->|"Biểu đồ, bảng TK"| ND

    ND -->|"Khoảng thời gian"| P62
    P62 -->|"Đọc giao dịch"| D3
    P62 -->|"Đọc danh mục"| D4
    P62 -->|"Biểu đồ, bảng TK"| ND

    ND -->|"Khoảng thời gian"| P63
    P63 -->|"Đọc giao dịch"| D3
    P63 -->|"Biểu đồ, bảng TK"| ND
```

*Hình 2.11 DFD mức 2 – Báo cáo thống kê*

---

### 2.5.4.7. DFD mức 2 – AI Chatbot

Phân rã tiến trình **7.0 AI Chatbot** thành 3 tiến trình con tương ứng với các quy trình P17, P18, P19.

```mermaid
flowchart TB
    ND["Người dùng"]
    D3[("D3 Giao dịch")]
    D5[("D5 Ngân sách")]
    D6[("D6 Mục tiêu")]
    D9[("D9 Lịch sử chat")]

    P71("7.1 Trả lời<br/>câu hỏi NLP")
    P72("7.2 Phân tích<br/>xu hướng chi tiêu")
    P73("7.3 Tư vấn<br/>tài chính")

    ND -->|"Câu hỏi"| P71
    P71 -->|"Truy vấn dữ liệu"| D3
    P71 <-->|"Lưu/đọc lịch sử"| D9
    P71 -->|"Câu trả lời NLP"| ND

    ND -->|"Yêu cầu phân tích"| P72
    P72 -->|"Đọc GD theo kỳ"| D3
    P72 -->|"Đọc ngân sách"| D5
    P72 <-->|"Lưu/đọc lịch sử"| D9
    P72 -->|"Kết quả phân tích"| ND

    ND -->|"Yêu cầu tư vấn"| P73
    P73 -->|"Đọc lịch sử GD"| D3
    P73 -->|"Đọc NS, MT"| D5
    P73 -->|"Đọc mục tiêu"| D6
    P73 <-->|"Lưu/đọc lịch sử"| D9
    P73 -->|"Nội dung tư vấn"| ND
```

*Hình 2.12 DFD mức 2 – AI Chatbot*

---

### 2.5.4.8. DFD mức 2 – Quản lý hệ thống

Phân rã tiến trình **8.0 Quản lý hệ thống** thành 2 tiến trình con.

```mermaid
flowchart TB
    QT["Quản trị viên"]
    D1[("D1 Tài khoản")]
    D9[("D9 Lịch sử chat")]

    P81("8.1 Thống kê<br/>danh sách người dùng")
    P82("8.2 Thống kê<br/>phản hồi AI Chatbot")

    QT -->|"Tiêu chí thống kê"| P81
    P81 -->|"Đọc TT người dùng"| D1
    P81 -->|"DS và trạng thái ND"| QT

    QT -->|"Tiêu chí thống kê"| P82
    P82 -->|"Đọc lịch sử chat"| D9
    P82 -->|"Báo cáo phản hồi AI"| QT
```

*Hình 2.13 DFD mức 2 – Quản lý hệ thống*

---

## Bảng tổng hợp ma trận Tiến trình – Kho dữ liệu

| Tiến trình | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1.0 QL Tài khoản | R/W | | | | | W | | | |
| 2.0 QL Ví | | R/W | | | W | W | | | |
| 3.0 QL Thu chi | | W | R/W | R | | | | R/W | |
| 4.0 QL Ngân sách | | | R | | R | | W | | |
| 5.0 QL Thông báo | | | | | | | R/W | | |
| 6.0 Báo cáo TK | | R | R | R | | | | | |
| 7.0 AI Chatbot | | | R | | R | R | | | R/W |
| 8.0 QL Hệ thống | R | | | | | | | | R |

*Bảng 2.3 Ma trận CRUD Tiến trình – Kho dữ liệu (R: Đọc, W: Ghi, R/W: Đọc/Ghi)*

---

# 2.4. Đặc tả chức năng

## 2.4.1. Chức năng Quản lý tài khoản

### 2.4.1.1. Đăng ký

| Tên chức năng | Đăng ký tài khoản |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng tạo mới tài khoản để sử dụng hệ thống quản lý tài chính cá nhân. Hệ thống hỗ trợ 2 phương thức: đăng ký bằng email và đăng ký bằng tài khoản Google |
| **Đầu vào** | - Với đăng ký bằng email: họ tên, địa chỉ email, mật khẩu, xác nhận mật khẩu, mã OTP xác thực - Với đăng ký bằng Google: xác nhận ủy quyền OAuth |
| **Đầu ra** | Tài khoản mới được tạo thành công và lưu vào CSDL |
| **Điều kiện trước** | - Email chưa tồn tại trong hệ thống - Người dùng chưa đăng nhập |
| **Điều kiện sau** | - Trường hợp thành công: Thông báo tạo tài khoản thành công, người dùng có thể đăng nhập - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân cụ thể (email đã tồn tại, OTP sai, mật khẩu không đủ mạnh) |
| **Ngoại lệ** | - Nếu email đã tồn tại trong hệ thống, hiển thị thông báo lỗi và yêu cầu nhập email khác - Nếu mã OTP sai hoặc hết hạn (quá 2 phút), hiển thị thông báo và cho phép gửi lại OTP - Nếu xác thực OAuth thất bại, hiển thị thông báo lỗi và yêu cầu thử lại |
| **Các yêu cầu đặc biệt** | - OTP có hiệu lực 2 phút và chỉ sử dụng một lần - Mật khẩu phải có tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt - Ghi log thời gian đăng ký để theo dõi |

*Bảng 2.4 Đặc tả chức năng Đăng ký tài khoản*

### 2.4.1.2. Đăng nhập

| Tên chức năng | Đăng nhập |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng truy cập hệ thống bằng tài khoản đã đăng ký trước đó |
| **Đầu vào** | Thông tin đăng nhập: email, mật khẩu |
| **Đầu ra** | Truy cập thành công vào giao diện Tổng quan hoặc thông báo lỗi |
| **Điều kiện trước** | - Người dùng đã có tài khoản hợp lệ trong hệ thống - Người dùng chưa đăng nhập |
| **Điều kiện sau** | - Trường hợp thành công: Phiên đăng nhập được tạo, lưu trạng thái đăng nhập và điều hướng vào trang tổng quan - Trường hợp thất bại: Hiển thị thông báo lỗi cụ thể (sai email hoặc sai mật khẩu) |
| **Ngoại lệ** | - Nếu email không tồn tại trong hệ thống, hiển thị thông báo "Email không tồn tại" - Nếu mật khẩu sai, hiển thị thông báo "Mật khẩu không đúng" - Nếu tài khoản bị khóa, hiển thị thông báo tương ứng |
| **Các yêu cầu đặc biệt** | - Phân quyền đăng nhập: phân biệt vai trò Người dùng và Quản trị viên - Ghi log thời gian đăng nhập để theo dõi và kiểm tra sau này |

*Bảng 2.5 Đặc tả chức năng Đăng nhập*

### 2.4.1.3. Cập nhật thông tin

| Tên chức năng | Cập nhật thông tin |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng cập nhật thông tin cá nhân và cấu hình ban đầu khi đăng nhập lần đầu |
| **Đầu vào** | Thông tin cá nhân: họ tên, ảnh đại diện, đơn vị tiền tệ mặc định, nghề nghiệp, mức lương/thu nhập hàng tháng |
| **Đầu ra** | Thông tin cá nhân được cập nhật thành công vào CSDL |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - Người dùng chưa có cập nhật thông tin lần nào |
| **Điều kiện sau** | - Trường hợp thành công: Thông báo cập nhật thành công, hệ thống ghi nhận thông tin mới - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân là các trường nhập không hợp lệ |
| **Ngoại lệ** | - Nếu thông tin nhập vào không hợp lệ hoặc thiếu trường bắt buộc, hiển thị thông báo lỗi cụ thể và yêu cầu nhập lại - Nếu mức lương nhập vào ≤ 0, hiển thị thông báo lỗi |
| **Các yêu cầu đặc biệt** | - Không cho phép bỏ trống các trường bắt buộc (đơn vị tiền tệ, nghề nghiệp) - Ghi log thời gian cập nhật để theo dõi |

*Bảng 2.6 Đặc tả chức năng Cập nhật thông tin*

### 2.4.1.4. Thiết lập mục tiêu

| Tên chức năng | Thiết lập mục tiêu |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng tạo mục tiêu tài chính tổng quát và theo dõi tiến độ thực hiện |
| **Đầu vào** | Thông tin mục tiêu: tên mục tiêu, số tiền mục tiêu, thời hạn hoàn thành, ví liên kết (tùy chọn), ghi chú |
| **Đầu ra** | Mục tiêu được tạo thành công và hiển thị trong danh sách mục tiêu |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Thông tin mục tiêu được lưu vào CSDL, khởi tạo trạng thái "Đang thực hiện" và % hoàn thành = 0% - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân cụ thể |
| **Ngoại lệ** | - Nếu số tiền mục tiêu ≤ 0, hiển thị thông báo "Số tiền phải lớn hơn 0" - Nếu thời hạn nhỏ hơn ngày hiện tại, hiển thị thông báo "Thời hạn không hợp lệ" - Nếu tên mục tiêu bị trùng, hiển thị cảnh báo |
| **Các yêu cầu đặc biệt** | - Hệ thống phải tự động tính toán và cập nhật % hoàn thành mục tiêu dựa trên số dư ví liên kết - Cần có giao diện trực quan hiển thị tiến độ mục tiêu (thanh progress bar) |

*Bảng 2.7 Đặc tả chức năng Thiết lập mục tiêu*

---

## 2.4.2. Chức năng Quản lý ví

### 2.4.2.1. Tạo ví

| Tên chức năng | Tạo ví |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng tạo ví tài chính để quản lý và theo dõi dòng tiền |
| **Đầu vào** | Thông tin ví: tên ví, số dư ban đầu, biểu tượng/màu sắc (tùy chọn), ghi chú |
| **Đầu ra** | Ví mới được tạo thành công và hiển thị trong danh sách ví |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Thông báo tạo ví thành công, ví mới hiển thị trong danh sách - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân cụ thể |
| **Ngoại lệ** | - Nếu số dư ban đầu < 0, hiển thị thông báo "Số dư không được âm" - Nếu tên ví bị trùng, hiển thị cảnh báo - Nếu thiếu thông tin bắt buộc (tên ví), hiển thị thông báo lỗi |
| **Các yêu cầu đặc biệt** | - Số dư phải ≥ 0 - Giao diện quản lý danh sách ví phải dễ sử dụng, hỗ trợ thao tác nhanh |

*Bảng 2.8 Đặc tả chức năng Tạo ví*

### 2.4.2.2. Sửa ví

| Tên chức năng | Sửa ví |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng chỉnh sửa thông tin ví đã tạo |
| **Đầu vào** | Thông tin ví cần cập nhật: tên ví, số dư điều chỉnh, biểu tượng/màu sắc, ghi chú |
| **Đầu ra** | Thông tin ví được cập nhật thành công vào CSDL |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - Ví phải tồn tại và thuộc quyền sở hữu của người dùng |
| **Điều kiện sau** | - Trường hợp thành công: Thông báo cập nhật ví thành công - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân cụ thể |
| **Ngoại lệ** | - Nếu ví không tồn tại trên hệ thống, hiển thị thông báo lỗi  - Nếu thông tin nhập không hợp lệ, hiển thị thông báo lỗi |
| **Các yêu cầu đặc biệt** | - Ghi log thời gian cập nhật thông tin ví để theo dõi - Nếu điều chỉnh số dư thủ công, hệ thống phải tạo giao dịch điều chỉnh tương ứng |

*Bảng 2.9 Đặc tả chức năng Sửa ví*

### 2.4.2.3. Cấu hình ngân sách chi tiêu cho ví

| Tên chức năng | Cấu hình ngân sách chi tiêu theo ví |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng thiết lập hạn mức chi tiêu cho từng ví theo chu kỳ thời gian |
| **Đầu vào** | Thông tin cấu hình: ví áp dụng, hạn mức chi tiêu (VNĐ), chu kỳ áp dụng (tháng/quý/năm), ngưỡng cảnh báo (%) |
| **Đầu ra** | Cấu hình ngân sách được lưu thành công vào CSDL |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - Ví phải tồn tại và thuộc quyền sở hữu của người dùng |
| **Điều kiện sau** | - Trường hợp thành công: Hệ thống bắt đầu giám sát chi tiêu theo hạn mức đã cấu hình - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân cụ thể |
| **Ngoại lệ** | - Nếu hạn mức ≤ 0, hiển thị thông báo "Hạn mức phải lớn hơn 0" - Nếu ví không tồn tại, hiển thị thông báo lỗi - Nếu ngưỡng cảnh báo không nằm trong khoảng 1-100%, hiển thị lỗi |
| **Các yêu cầu đặc biệt** | - Ngưỡng cảnh báo mặc định là 80% nếu người dùng không thiết lập - Ghi log thời gian cấu hình |

*Bảng 2.10 Đặc tả chức năng Cấu hình ngân sách chi tiêu cho ví*

### 2.4.2.4. Cấu hình mục tiêu cho ví

| Tên chức năng | Cấu hình mục tiêu theo ví |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng thiết lập mục tiêu tài chính và liên kết với một ví cụ thể để theo dõi |
| **Đầu vào** | Thông tin mục tiêu: tên mục tiêu, số tiền mục tiêu (VNĐ), thời hạn hoàn thành, ví áp dụng |
| **Đầu ra** | Mục tiêu được tạo, liên kết với ví và hiển thị trong danh sách |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - Ví phải tồn tại và thuộc quyền sở hữu của người dùng |
| **Điều kiện sau** | - Trường hợp thành công: Hệ thống theo dõi tiến độ mục tiêu, tự động cập nhật khi phát sinh giao dịch với ví liên kết - Trường hợp thất bại: Nhận thông báo lỗi |
| **Ngoại lệ** | - Nếu ví không tồn tại, hiển thị thông báo lỗi - Nếu số tiền mục tiêu ≤ 0, hiển thị thông báo lỗi - Nếu thời hạn nhỏ hơn ngày hiện tại, hiển thị lỗi |
| **Các yêu cầu đặc biệt** | - Tự động cập nhật % hoàn thành và trạng thái mục tiêu khi có giao dịch mới - Gửi thông báo khi mục tiêu đạt 100% hoặc quá hạn |

*Bảng 2.11 Đặc tả chức năng Cấu hình mục tiêu cho ví*

---

## 2.4.3. Chức năng Quản lý thu chi

### 2.4.3.1. Tạo giao dịch thủ công

| Tên chức năng | Tạo giao dịch thủ công |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng ghi nhận một khoản thu hoặc chi phát sinh vào hệ thống |
| **Đầu vào** | Thông tin giao dịch: loại giao dịch (thu/chi), số tiền, danh mục, ngày giao dịch, ví áp dụng, ghi chú (tùy chọn) |
| **Đầu ra** | Giao dịch được lưu vào CSDL, số dư ví được cập nhật |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - Ví phải tồn tại và thuộc quyền sở hữu |
| **Điều kiện sau** | - Trường hợp thành công: Giao dịch được lưu, số dư ví cập nhật, kích hoạt kiểm tra ngân sách (P13) - Trường hợp thất bại: Nhận thông báo lỗi và nguyên nhân cụ thể |
| **Ngoại lệ** | - Nếu số tiền ≤ 0, hiển thị thông báo "Số tiền phải lớn hơn 0" - Nếu ví không tồn tại, hiển thị lỗi - Nếu thiếu danh mục hoặc ví, hiển thị thông báo yêu cầu chọn |
| **Các yêu cầu đặc biệt** | - Sau khi tạo giao dịch thành công, hệ thống tự động kiểm tra ngân sách và tạo cảnh báo nếu vượt ngưỡng - Tự động cập nhật % hoàn thành mục tiêu nếu ví có liên kết mục tiêu |

*Bảng 2.12 Đặc tả chức năng Tạo giao dịch thủ công*

### 2.4.3.2. Tạo dữ liệu giao dịch từ file Excel

| Tên chức năng | Tạo dữ liệu giao dịch từ file Excel |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng nhập hàng loạt giao dịch từ file Excel theo mẫu chuẩn của hệ thống |
| **Đầu vào** | File Excel (.xlsx) đúng định dạng mẫu, chứa các cột: loại giao dịch, số tiền, danh mục, ngày, ví, ghi chú |
| **Đầu ra** | Danh sách giao dịch hợp lệ được lưu vào CSDL, danh sách dòng lỗi được hiển thị |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - File Excel đúng cấu trúc mẫu của hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Các giao dịch hợp lệ được lưu, số dư ví được cập nhật - Trường hợp thất bại: Hiển thị danh sách dòng lỗi với nguyên nhân cụ thể |
| **Ngoại lệ** | - Nếu file không đúng định dạng (.xlsx), hiển thị thông báo "File không đúng định dạng" - Nếu file có dòng dữ liệu không hợp lệ (số tiền âm, danh mục không tồn tại), hiển thị chi tiết từng dòng lỗi - Nếu file rỗng, hiển thị thông báo "Không có dữ liệu" |
| **Các yêu cầu đặc biệt** | - Hiển thị bản xem trước trước khi xác nhận lưu - Hỗ trợ tải file mẫu Excel từ hệ thống - Ghi log số lượng giao dịch import thành công và thất bại |

*Bảng 2.13 Đặc tả chức năng Tạo dữ liệu giao dịch từ file Excel*

### 2.4.3.3. Tạo khoản thu chi cố định

| Tên chức năng | Tạo khoản thu chi cố định |
| :---- | :---- |
| **Tác nhân** | Người dùng, Hệ thống (Scheduler) |
| **Mô tả** | Chức năng này cho phép người dùng cấu hình giao dịch định kỳ. Hệ thống tự động tạo giao dịch theo chu kỳ đã thiết lập |
| **Đầu vào** | Thông tin cấu hình: ví áp dụng, loại giao dịch (thu/chi), số tiền, danh mục, ngày bắt đầu, chu kỳ lặp (ngày/tuần/tháng/năm), trạng thái (bật/tắt) |
| **Đầu ra** | Cấu hình định kỳ được lưu; hệ thống tự động tạo giao dịch khi đến hạn |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống - Ví tồn tại và hợp lệ |
| **Điều kiện sau** | - Trường hợp thành công: Cấu hình được lưu vào CSDL; hệ thống tự động tạo giao dịch khi đến hạn và cập nhật số dư ví - Trường hợp thất bại: Nhận thông báo lỗi |
| **Ngoại lệ** | - Nếu ví không tồn tại, hiển thị thông báo lỗi - Nếu số tiền ≤ 0, hiển thị thông báo lỗi - Nếu hệ thống gặp lỗi khi thực thi tác vụ tự động, ghi log lỗi và gửi thông báo cho người dùng |
| **Các yêu cầu đặc biệt** | - Hệ thống phải hỗ trợ bật/tắt cấu hình định kỳ - Gửi thông báo cho người dùng sau mỗi lần tạo giao dịch tự động - Ghi log thời gian thực thi và kết quả |

*Bảng 2.14 Đặc tả chức năng Tạo khoản thu chi cố định*

### 2.4.3.4. Xem danh sách giao dịch theo bộ lọc

| Tên chức năng | Xem danh sách giao dịch theo bộ lọc |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng tra cứu và xem danh sách giao dịch đã ghi nhận theo các tiêu chí lọc |
| **Đầu vào** | Bộ lọc: khoảng thời gian (từ ngày – đến ngày), loại giao dịch (thu/chi/tất cả), danh mục, ví, từ khóa tìm kiếm |
| **Đầu ra** | Danh sách giao dịch phù hợp với tiêu chí lọc, phân trang |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Danh sách giao dịch được hiển thị trên giao diện - Trường hợp không có dữ liệu: Hiển thị thông báo "Không có giao dịch phù hợp" |
| **Ngoại lệ** | - Nếu không có dữ liệu phù hợp, hiển thị thông báo rỗng phù hợp |
| **Các yêu cầu đặc biệt** | - Hỗ trợ phân trang - Sắp xếp mặc định theo ngày giao dịch giảm dần - Giao diện phải hiển thị tổng thu, tổng chi trong khoảng thời gian đã lọc |

*Bảng 2.15 Đặc tả chức năng Xem danh sách giao dịch theo bộ lọc*

### 2.4.3.5. Xuất dữ liệu giao dịch ra file Excel

| Tên chức năng | Xuất dữ liệu giao dịch ra file Excel |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng xuất danh sách giao dịch ra file Excel để lưu trữ hoặc phân tích ngoại tuyến |
| **Đầu vào** | Bộ lọc: khoảng thời gian, loại giao dịch, danh mục, ví |
| **Đầu ra** | File Excel (.xlsx) chứa danh sách giao dịch theo bộ lọc |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Có dữ liệu giao dịch trong hệ thống phù hợp với bộ lọc |
| **Điều kiện sau** | - Trường hợp thành công: File Excel được tạo và tải về thiết bị - Trường hợp thất bại: Hiển thị thông báo lỗi |
| **Ngoại lệ** | - Nếu không có dữ liệu để xuất, hiển thị thông báo "Không có dữ liệu phù hợp" - Nếu xảy ra lỗi khi tạo file, hiển thị thông báo lỗi hệ thống |
| **Các yêu cầu đặc biệt** | - File xuất đúng định dạng mẫu của hệ thống - File phải có header rõ ràng và dữ liệu được format đúng kiểu |

*Bảng 2.16 Đặc tả chức năng Xuất dữ liệu giao dịch ra file Excel*

---

## 2.4.4. Chức năng Quản lý ngân sách

### 2.4.4.1. Cấu hình ngưỡng thông báo khi vượt quá chi tiêu theo ví

| Tên chức năng | Cấu hình ngưỡng cảnh báo chi tiêu theo ví |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng thiết lập ngưỡng phần trăm để hệ thống tự động tạo cảnh báo khi chi tiêu của một ví đạt hoặc vượt ngưỡng |
| **Đầu vào** | Thông tin cấu hình: ví áp dụng, hạn mức chi tiêu (VNĐ), chu kỳ (tháng/quý/năm), ngưỡng cảnh báo (%) |
| **Đầu ra** | Cấu hình ngưỡng được lưu thành công vào CSDL |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Ví tồn tại và thuộc quyền sở hữu |
| **Điều kiện sau** | - Trường hợp thành công: Hệ thống giám sát chi tiêu theo ví và tạo cảnh báo khi đạt ngưỡng - Trường hợp thất bại: Nhận thông báo lỗi |
| **Ngoại lệ** | - Nếu hạn mức ≤ 0, hiển thị "Hạn mức phải lớn hơn 0" - Nếu ví không tồn tại, hiển thị lỗi - Nếu ngưỡng ngoài khoảng 1-100%, hiển thị lỗi |
| **Các yêu cầu đặc biệt** | - Ngưỡng mặc định 80% - Hỗ trợ hai mức: "Sắp vượt" (đạt ngưỡng) và "Đã vượt" (đạt 100%) - Ghi log cấu hình |

*Bảng 2.17 Đặc tả chức năng Cấu hình ngưỡng CB theo ví*

### 2.4.4.2. Cấu hình ngưỡng thông báo khi vượt quá chi tiêu theo danh mục

| Tên chức năng | Cấu hình ngưỡng cảnh báo chi tiêu theo danh mục |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng thiết lập ngưỡng cảnh báo cho từng danh mục chi tiêu cụ thể |
| **Đầu vào** | Thông tin cấu hình: danh mục áp dụng, hạn mức chi tiêu (VNĐ), chu kỳ (tháng/quý/năm), ngưỡng cảnh báo (%) |
| **Đầu ra** | Cấu hình ngưỡng được lưu thành công vào CSDL |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Danh mục hợp lệ và tồn tại |
| **Điều kiện sau** | - Trường hợp thành công: Hệ thống giám sát chi tiêu theo danh mục và tạo cảnh báo khi đạt ngưỡng - Trường hợp thất bại: Nhận thông báo lỗi |
| **Ngoại lệ** | - Nếu hạn mức ≤ 0, hiển thị lỗi - Nếu danh mục không tồn tại, hiển thị lỗi |
| **Các yêu cầu đặc biệt** | - Tương tự cấu hình theo ví, ngưỡng mặc định 80% |

*Bảng 2.18 Đặc tả chức năng Cấu hình ngưỡng CB theo danh mục*

### 2.4.4.3. Xem danh sách cảnh báo chi tiêu theo bộ lọc

| Tên chức năng | Xem danh sách cảnh báo chi tiêu |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng xem lại các cảnh báo vượt ngân sách đã được hệ thống tạo |
| **Đầu vào** | Bộ lọc: khoảng thời gian, loại cảnh báo (sắp vượt/đã vượt), ví hoặc danh mục |
| **Đầu ra** | Danh sách cảnh báo chi tiêu phù hợp, phân trang |
| **Điều kiện trước** | - Người dùng đã đăng nhập |
| **Điều kiện sau** | - Trường hợp thành công: Danh sách cảnh báo hiển thị trên giao diện - Trường hợp không có dữ liệu: Hiển thị thông báo "Không có cảnh báo" |
| **Ngoại lệ** | - Nếu không có cảnh báo trong khoảng thời gian, hiển thị thông báo rỗng |
| **Các yêu cầu đặc biệt** | - Hiển thị rõ mức độ cảnh báo bằng màu sắc (vàng = sắp vượt 80%, đỏ = đã vượt 100%) - Hỗ trợ phân trang |

*Bảng 2.19 Đặc tả chức năng Xem danh sách cảnh báo chi tiêu*

---

## 2.4.5. Chức năng Quản lý thông báo

### 2.4.5.1. Bật tắt thông báo

| Tên chức năng | Bật/Tắt thông báo |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng kích hoạt hoặc vô hiệu hóa chức năng nhận thông báo từ hệ thống |
| **Đầu vào** | Trạng thái: bật hoặc tắt |
| **Đầu ra** | Cập nhật trạng thái cấu hình thông báo thành công |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Hệ thống ghi nhận trạng thái mới, áp dụng ngay lập tức - Trường hợp thất bại: Hiển thị thông báo lỗi hệ thống |
| **Ngoại lệ** | - Nếu xảy ra lỗi hệ thống khi cập nhật, hiển thị thông báo lỗi và giữ nguyên trạng thái cũ |
| **Các yêu cầu đặc biệt** | - Thay đổi có hiệu lực ngay lập tức - Ghi log thời gian thay đổi |

*Bảng 2.20 Đặc tả chức năng Bật/Tắt thông báo*

### 2.4.5.2. Cấu hình thời gian gửi thông báo

| Tên chức năng | Cấu hình thời gian gửi thông báo |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng thiết lập lịch gửi báo cáo và thông báo định kỳ |
| **Đầu vào** | Thông tin cấu hình: tần suất gửi (tuần/tháng/quý/năm), thời điểm gửi (ngày, giờ), loại báo cáo đính kèm |
| **Đầu ra** | Cấu hình lịch gửi thông báo được lưu thành công |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Chức năng thông báo đang được bật |
| **Điều kiện sau** | - Trường hợp thành công: Lịch gửi thông báo được lưu vào CSDL, Scheduler tự động thực thi - Trường hợp thất bại: Hiển thị thông báo lỗi |
| **Ngoại lệ** | - Nếu thời gian cấu hình không hợp lệ, hiển thị lỗi - Nếu cấu hình bị trùng lặp, hiển thị cảnh báo |
| **Các yêu cầu đặc biệt** | - Hệ thống Scheduler phải hỗ trợ xử lý tự động theo lịch - Ghi log mỗi lần gửi thông báo |

*Bảng 2.21 Đặc tả chức năng Cấu hình thời gian gửi thông báo*

### 2.4.5.3. Xem danh sách thông báo theo bộ lọc

| Tên chức năng | Xem danh sách thông báo |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng xem lại các thông báo đã nhận từ hệ thống theo tiêu chí lọc |
| **Đầu vào** | Bộ lọc: khoảng thời gian, loại thông báo (cảnh báo ngân sách, mục tiêu, định kỳ, hệ thống), trạng thái (đã đọc/chưa đọc) |
| **Đầu ra** | Danh sách thông báo phù hợp, phân trang |
| **Điều kiện trước** | - Người dùng đã đăng nhập |
| **Điều kiện sau** | - Trường hợp thành công: Danh sách thông báo hiển thị, trạng thái cập nhật thành "đã đọc" khi mở xem - Trường hợp không có dữ liệu: Hiển thị danh sách rỗng |
| **Ngoại lệ** | - Nếu không có thông báo phù hợp bộ lọc, hiển thị danh sách rỗng |
| **Các yêu cầu đặc biệt** | - Hỗ trợ phân trang - Hiển thị badge số thông báo chưa đọc trên icon thông báo |

*Bảng 2.22 Đặc tả chức năng Xem danh sách thông báo*

---

## 2.4.6. Chức năng Báo cáo thống kê

### 2.4.6.1. Xem báo cáo thống kê chi tiêu theo ví

| Tên chức năng | Báo cáo chi tiêu theo ví |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng xem thống kê tổng thu và tổng chi của từng ví trong khoảng thời gian xác định |
| **Đầu vào** | Khoảng thời gian cần xem (từ ngày – đến ngày) |
| **Đầu ra** | Biểu đồ trực quan và bảng thống kê theo từng ví |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Có dữ liệu giao dịch trong hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Báo cáo hiển thị trên giao diện với biểu đồ và số liệu - Trường hợp không có dữ liệu: Hiển thị thông báo "Chưa có dữ liệu" |
| **Ngoại lệ** | - Nếu không có dữ liệu trong khoảng thời gian đã chọn, hiển thị thông báo phù hợp |
| **Các yêu cầu đặc biệt** | - Hỗ trợ biểu đồ trực quan: cột, tròn, đường - Giao diện responsive, hiển thị tốt trên mobile |

*Bảng 2.23 Đặc tả chức năng Báo cáo chi tiêu theo ví*

### 2.4.6.2. Xem báo cáo thống kê chi tiêu theo danh mục

| Tên chức năng | Báo cáo chi tiêu theo danh mục |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng xem thống kê và phân tích mức chi tiêu theo từng danh mục |
| **Đầu vào** | Khoảng thời gian cần xem (từ ngày – đến ngày) |
| **Đầu ra** | Biểu đồ tròn/cột và bảng thống kê theo danh mục |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Có dữ liệu giao dịch |
| **Điều kiện sau** | - Trường hợp thành công: Báo cáo hiển thị trên giao diện - Trường hợp không có dữ liệu: Hiển thị thông báo |
| **Ngoại lệ** | - Nếu không có dữ liệu, hiển thị thông báo "Chưa có dữ liệu" |
| **Các yêu cầu đặc biệt** | - Tự động tính tỷ lệ phần trăm từng danh mục so với tổng chi - Biểu đồ tròn mặc định để trực quan hóa tỷ lệ |

*Bảng 2.24 Đặc tả chức năng Báo cáo chi tiêu theo danh mục*

### 2.4.6.3. Xem báo cáo thống kê chi tiêu theo thời gian

| Tên chức năng | Báo cáo chi tiêu theo thời gian |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng xem xu hướng thu chi theo ngày, tuần, tháng hoặc năm |
| **Đầu vào** | Khoảng thời gian cần xem, đơn vị thời gian (ngày/tuần/tháng/năm) |
| **Đầu ra** | Biểu đồ đường thể hiện xu hướng và bảng thống kê |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Có dữ liệu giao dịch |
| **Điều kiện sau** | - Trường hợp thành công: Báo cáo hiển thị trên giao diện - Trường hợp không có dữ liệu: Hiển thị thông báo |
| **Ngoại lệ** | - Nếu không có dữ liệu, hiển thị thông báo "Chưa có dữ liệu" |
| **Các yêu cầu đặc biệt** | - Biểu đồ đường mặc định, thể hiện xu hướng tăng/giảm chi tiêu - Hỗ trợ so sánh kỳ trước vs kỳ hiện tại |

*Bảng 2.25 Đặc tả chức năng Báo cáo chi tiêu theo thời gian*

---

## 2.4.7. AI Chatbot

### 2.4.7.1. Trả lời câu hỏi từ người dùng

| Tên chức năng | AI Chatbot trả lời câu hỏi |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép người dùng tra cứu thông tin tài chính cá nhân thông qua hội thoại bằng ngôn ngữ tự nhiên |
| **Đầu vào** | Nội dung câu hỏi dưới dạng văn bản tự nhiên (tiếng Việt) |
| **Đầu ra** | Câu trả lời bằng ngôn ngữ tự nhiên, có thể kèm số liệu minh họa |
| **Điều kiện trước** | - Người dùng đã đăng nhập vào hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Câu trả lời được hiển thị, lịch sử hội thoại được lưu - Trường hợp thất bại: Hiển thị thông báo "Tôi chưa hiểu câu hỏi, vui lòng thử lại" |
| **Ngoại lệ** | - Nếu không nhận diện được ý định câu hỏi, trả lời thông báo gợi ý câu hỏi mẫu - Nếu hệ thống AI gặp lỗi kết nối, hiển thị thông báo lỗi |
| **Các yêu cầu đặc biệt** | - Sử dụng NLP và RAG pipeline để xử lý câu hỏi - Lưu lịch sử hội thoại để cải thiện chất lượng phản hồi - Ghi log thời gian phản hồi để giám sát hiệu suất |

*Bảng 2.26 Đặc tả chức năng AI Chatbot trả lời câu hỏi*

### 2.4.7.2. Phân tích xu hướng chi tiêu

| Tên chức năng | Phân tích xu hướng chi tiêu |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép AI phân tích dữ liệu giao dịch để xác định xu hướng chi tiêu theo thời gian, so sánh các kỳ |
| **Đầu vào** | Yêu cầu phân tích từ người dùng, khoảng thời gian (tùy chọn) |
| **Đầu ra** | Nhận xét phân tích bằng ngôn ngữ tự nhiên kèm số liệu so sánh |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Có dữ liệu giao dịch đủ để phân tích (tối thiểu 2 kỳ) |
| **Điều kiện sau** | - Trường hợp thành công: Kết quả phân tích được hiển thị, lịch sử lưu lại - Trường hợp thất bại: Thông báo dữ liệu chưa đủ |
| **Ngoại lệ** | - Nếu dữ liệu không đủ để phân tích (ít hơn 2 kỳ), hiển thị thông báo yêu cầu bổ sung - Nếu AI gặp lỗi, hiển thị thông báo lỗi hệ thống |
| **Các yêu cầu đặc biệt** | - Sử dụng thuật toán thống kê hoặc AI để phân tích - Kết quả phải có so sánh kỳ trước vs kỳ hiện tại - Ghi log thời gian phản hồi |

*Bảng 2.27 Đặc tả chức năng Phân tích xu hướng chi tiêu*

### 2.4.7.3. Tư vấn tài chính dựa trên lịch sử

| Tên chức năng | Tư vấn tài chính |
| :---- | :---- |
| **Tác nhân** | Người dùng |
| **Mô tả** | Chức năng này cho phép AI đưa ra khuyến nghị tài chính cá nhân hóa dựa trên dữ liệu thu chi, ngân sách và mục tiêu của người dùng |
| **Đầu vào** | Yêu cầu tư vấn từ người dùng; hệ thống tự động truy xuất: lịch sử giao dịch, ngân sách, thu nhập, mục tiêu |
| **Đầu ra** | Nội dung tư vấn cá nhân hóa bằng ngôn ngữ tự nhiên |
| **Điều kiện trước** | - Người dùng đã đăng nhập - Có dữ liệu giao dịch trong hệ thống |
| **Điều kiện sau** | - Trường hợp thành công: Nội dung tư vấn được hiển thị, lịch sử lưu lại - Trường hợp thất bại: Thông báo dữ liệu chưa đủ |
| **Ngoại lệ** | - Nếu thiếu dữ liệu lịch sử, hiển thị thông báo gợi ý bổ sung dữ liệu - Nếu AI gặp lỗi, hiển thị thông báo lỗi hệ thống |
| **Các yêu cầu đặc biệt** | - Tư vấn phải dựa trên dữ liệu thực tế của người dùng, không phải chung chung - Ghi log để giám sát chất lượng tư vấn |

*Bảng 2.28 Đặc tả chức năng Tư vấn tài chính*

---

## 2.4.8. Chức năng Quản lý hệ thống

### 2.4.8.1. Thống kê danh sách người dùng

| Tên chức năng | Thống kê danh sách người dùng |
| :---- | :---- |
| **Tác nhân** | Quản trị viên |
| **Mô tả** | Chức năng này cho phép quản trị viên xem danh sách tài khoản người dùng và trạng thái hoạt động của từng tài khoản trong hệ thống |
| **Đầu vào** | Bộ lọc: trạng thái tài khoản (hoạt động/bị khóa), khoảng thời gian đăng ký (từ ngày – đến ngày), từ khóa tìm kiếm (email, họ tên) |
| **Đầu ra** | Danh sách người dùng kèm thông tin chi tiết: email, họ tên, ngày đăng ký, trạng thái, số lượng giao dịch, lần đăng nhập gần nhất |
| **Điều kiện trước** | - Quản trị viên đã đăng nhập với quyền admin |
| **Điều kiện sau** | - Trường hợp thành công: Danh sách người dùng hiển thị trên giao diện quản trị - Trường hợp không có dữ liệu: Hiển thị danh sách rỗng |
| **Ngoại lệ** | - Nếu không có người dùng phù hợp tiêu chí, hiển thị danh sách rỗng - Nếu quản trị viên không có quyền admin, từ chối truy cập |
| **Các yêu cầu đặc biệt** | - Hỗ trợ phân trang - Hỗ trợ xuất danh sách ra file Excel - Ghi log hoạt động quản trị |

*Bảng 2.29 Đặc tả chức năng Thống kê danh sách người dùng*

### 2.4.8.2. Thống kê phản hồi AI Chatbot

| Tên chức năng | Thống kê phản hồi AI Chatbot |
| :---- | :---- |
| **Tác nhân** | Quản trị viên |
| **Mô tả** | Chức năng này cho phép quản trị viên xem thống kê về hoạt động và chất lượng phản hồi của AI Chatbot để giám sát và cải thiện hiệu suất |
| **Đầu vào** | Bộ lọc: khoảng thời gian (từ ngày – đến ngày), loại câu hỏi (tra cứu/phân tích/tư vấn) |
| **Đầu ra** | Báo cáo thống kê: tổng số câu hỏi, tỷ lệ phản hồi thành công, thời gian phản hồi trung bình, danh sách câu hỏi phổ biến, biểu đồ trực quan |
| **Điều kiện trước** | - Quản trị viên đã đăng nhập với quyền admin |
| **Điều kiện sau** | - Trường hợp thành công: Báo cáo thống kê AI hiển thị trên giao diện quản trị - Trường hợp không có dữ liệu: Hiển thị thông báo "Chưa có dữ liệu chat" |
| **Ngoại lệ** | - Nếu không có dữ liệu chat trong khoảng thời gian, hiển thị thông báo phù hợp - Nếu quản trị viên không có quyền, từ chối truy cập |
| **Các yêu cầu đặc biệt** | - Hiển thị biểu đồ trực quan (cột, đường) - Hỗ trợ giám sát hiệu suất AI theo thời gian thực - Ghi log hoạt động tra cứu thống kê |

*Bảng 2.30 Đặc tả chức năng Thống kê phản hồi AI Chatbot*
