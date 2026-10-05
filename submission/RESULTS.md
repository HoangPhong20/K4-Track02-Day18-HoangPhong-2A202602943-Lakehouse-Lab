# Đối chiếu kết quả với rubric

Số liệu lấy từ Jupyter notebooks đã thực thi trong `notebooks/`, với output
nguyên văn trong `logs/`. Thời gian và môi trường nằm ở `execution.json`.
Đây là đối chiếu kỹ thuật, không phải cam kết điểm được coach chấm.

| Notebook | Kết quả thực tế | Giải thích |
|---|---|---|
| [NB1](notebooks/01_delta_basics.ipynb) | 2 commit JSON; lỗi cast `thirty` sang Int64; tier được thêm; 2 nhóm tier | Enforcement chặn write thực tế; evolution opt-in. Output có tên log và JSON commit đầy đủ. |
| [NB2](notebooks/02_optimize_zorder.ipynb) | 200 → 55 file; 481,9 → 64,5 ms; speedup 7,5×; pruning 55× | Chỉ 1/55 khoảng min/max chứa user_id 4242. Timing phụ thuộc máy, cache và tải. |
| [NB3](notebooks/03_time_travel.ipynb) | MERGE 100.000 hàng: update 50.000, insert 50.000; 5 version; RESTORE v4 về trạng thái v2; score âm = 0 | RESTORE tạo transaction mới, giữ history. |
| [NB4](notebooks/04_medallion.ipynb) | Bronze 200.000; Silver 190.052; giảm 9.948; Gold 8 ngày × 3 model = 24 nhóm | Gold CSV đầy đủ; PASS p50 ≤ p95, cost dương, error_rate trong [0,1]. Giá token minh họa của lab. |
| [NB5](notebooks/05_iceberg_catalog.ipynb) | Catalog SQLite; day(ts); plan_files 10 → 1; pruning 10×; metadata:data 283,8%; field ID 4 giữ nguyên; specs [1,2]; 5.500 hàng đọc được | Metadata lớn vì file nhỏ, không suy ra overhead production. Rename giữ định danh field. |
| [NB6](notebooks/06_maintenance.ipynb) | Compaction 200 → 11 (18,18×); clustering skip 90%; vacuum thu hồi 16,1 MB; tìm/xóa 3 orphan đã cấy; checkpoint + _last_checkpoint; Iceberg 20 → 3 snapshots; sweep 17 manifest lists; 2.000 hàng còn nguyên | Expiry không đồng nghĩa xóa vật lý; orphan chưa commit cần sweep có age guard. |
| [NB7](notebooks/07_vectors_multimodal.ipynb) | Amplification 200×; int8 nhỏ 5,8×; recall@10 0,904; fidelity 1,000; SQL top-5 cùng topic; bảng 0 hit/index cũ 8 hit; 8 CDF deletes | Index chưa đồng bộ delete vẫn trả dữ liệu đã xóa. Quantization cần đánh giá trên mỗi corpus. |
| [NB8](notebooks/08_agents_provenance.ipynb) | 2 partition policy; pin v0 replay 1.578 bước; 5 list_tables/1 catalog read; input_required trước simulated delete; task completed; 4 bucket + UNCLASSIFIED; 334 hàng bị loại; subject 8 → 0 | Mô phỏng offline; replay so số bước; confirmation do caller truyền; provenance mapping không chứng minh quyền sử dụng dữ liệu thật. |

Smoke **9/9 PASS**, pytest **24/24 PASS**, runner **8/8 PASS**.
Xem [logs/](logs/) để kiểm tra nguyên văn kết quả.

Runner cũng PASS 8/8 với LAKEHOUSE_ROOT trỏ tới một vùng dữ liệu mới,
không dùng Bronze/corpus có sẵn: [run_all_clean.txt](logs/run_all_clean.txt).
Môi trường Python dùng venv đã có, không dựng lại dependencies từ đầu.

## Ảnh bằng chứng

[screenshots/](screenshots/) chứa ảnh render output kernel, chia trang và giữ
nguyên toàn bộ text. Mỗi header ghi nguồn log và “not a UI screenshot”.
NB1 có JSON commit; NB2 có stats và metric tổng kết; NB3 có RESTORE history;
NB4 có Gold CSV; NB5–NB8 có metrics và checks tương ứng.

## Việc còn cần người nộp hoàn tất

- Đọc lại giải thích và reflection; người nộp đã xác nhận tự chạy lại và kiểm tra kết quả.
- Bổ sung screenshot giao diện nếu coach yêu cầu đúng dạng ảnh chụp UI.
- Commit/push vào fork, mở PR, ghi commit SHA và gửi qua kênh lớp.
- Bonus tùy chọn chưa thực hiện.
