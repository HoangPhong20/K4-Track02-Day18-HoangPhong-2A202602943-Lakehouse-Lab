# Thông tin bài làm

- Họ tên: Hoàng Phong.
- MSSV: 2A202602943.
- Mã bài: K4-Track02-Day18.
- GitHub: HoangPhong20.
- Repo: https://github.com/HoangPhong20/K4-Track02-Day18-HoangPhong-2A202602943-Lakehouse-Lab
- Đường chạy: lightweight cho cả NB1–NB8; không dùng Spark.
- Python: CPython 3.11.9, Windows x64.
- Dependencies thực tế: [requirements.lock.txt](requirements.lock.txt).
- Thời gian chạy và nền tảng: [execution.json](execution.json).

## Tái lập

Chạy từ thư mục gốc repo trong PowerShell:

```powershell
$env:PYTHONUTF8 = '1'
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r submission/requirements.lock.txt
.venv/Scripts/python.exe scripts/verify_lite.py
.venv/Scripts/python.exe -m pytest
.venv/Scripts/python.exe scripts/run_all.py
.venv/Scripts/python.exe scripts/prepare_submission.py
.venv/Scripts/python.exe scripts/render_evidence.py
```

`prepare_submission.py` chạy từng cell trong Jupyter kernel thật, dừng nếu có lỗi,
lưu notebook có execution_count/output và trích nguyên output thành text.
Ảnh PNG trong `screenshots/` được render từ text output đã lưu, **không phải ảnh chụp
giao diện Jupyter/MinIO**. Máy chạy không có browser trong phiên điều khiển UI.
Người nộp cần bổ sung ảnh chụp giao diện nếu coach yêu cầu đúng dạng screenshot.

## Trạng thái nộp

Người nộp đã xác nhận tự chạy lại và kiểm tra kết quả hệ thống.
Bài có AI hỗ trợ; phạm vi được khai báo trong AI_USAGE.md.
Chưa commit/push hoặc mở PR. Chưa gửi qua kênh lớp. Chưa làm bonus tùy chọn.
