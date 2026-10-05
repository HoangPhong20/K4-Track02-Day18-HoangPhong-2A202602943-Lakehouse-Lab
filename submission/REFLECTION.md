# Reflection

Anti-pattern được chọn là bỏ sót sự kiện xóa khi đồng bộ external vector index.
Với hệ thống RAG dùng tài liệu học tập, nội dung thường được cập nhật hoặc thu hồi,
trong khi pipeline dễ chỉ xử lý thêm mới. Embedding cũ có thể khiến câu trả lời
tiếp tục dựa trên tài liệu không còn hiệu lực.

Kết quả NB7 cho thấy sau khi xóa 8 document, bảng hiện tại trả 0 hit
nhưng index chưa đồng bộ vẫn trả 8 hit. Xóa thành công trong lakehouse vì vậy
chưa chứng minh dữ liệu đã biến mất khỏi đường retrieval.

Cách phòng tránh là dùng lakehouse làm nguồn dữ liệu chính, coi index là bản
dẫn xuất có thể rebuild. Consumer phải xử lý cả CDF delete events, lưu mốc đã
đồng bộ và xử lý lặp mà không làm sai trạng thái. Cần cảnh báo độ trễ, kiểm tra
document còn hiệu lực trước khi đưa vào prompt và kiểm thử xóa xuyên suốt từ
bảng đến index. Version cũ cũng cần retention phù hợp.

Tôi đã tự chạy lại và kiểm tra kết quả hệ thống. Codex hỗ trợ; xem
[AI_USAGE.md](AI_USAGE.md).
