# Khai báo sử dụng AI

Công cụ: OpenAI Codex, hỗ trợ theo yêu cầu thực hiện hướng dẫn trong `docs/`.

Phạm vi hỗ trợ:

- Đọc CHECKPOINTS, RULES, RUBRIC và SUBMISSION để chuẩn bị phần bắt buộc.
- Thực thi smoke test, pytest, runner và notebook bằng công cụ trên máy người dùng.
- Sửa NB1 để assertion dùng cờ bắt lỗi thật thay cho giá trị True gán sẵn.
- Bổ sung NB4 bảng Gold đầy đủ và assertions kiểm tra 3 model/ngày,
  p50 ≤ p95, cost dương, error_rate trong [0, 1]. Không hạ ngưỡng rubric.
- Viết script thực thi notebook/lưu output và render output thành ảnh PNG.
- Soạn phần giải thích notebook, báo cáo kết quả và reflection dựa trên output NB7.

Output được sinh từ code thực thi; AI không viết số liệu giả vào output cells.
Ảnh bằng chứng là render trực tiếp từ log kernel, không giả làm screenshot UI.
Dữ liệu dùng generator của đề bài, không đưa dữ liệu cá nhân thực vào lab.

Reflection được AI hỗ trợ biên soạn từ kết quả NB7. Người nộp đã xác nhận
tự chạy lại và kiểm tra kết quả hệ thống trong cuộc trao đổi này. Ghi nhận này
dựa trên xác nhận của người nộp; log do Codex tạo được lưu riêng trong logs/.
