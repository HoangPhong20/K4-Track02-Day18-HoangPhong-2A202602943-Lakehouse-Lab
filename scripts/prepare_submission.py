"""Execute Jupytext notebooks in real Jupyter kernels and preserve evidence.

Run from the repo root with .venv/Scripts/python.exe scripts/prepare_submission.py.
Generated outputs are never synthesized; kernel errors stop the run.
"""
from pathlib import Path
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone

import jupytext
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission"
NOTES = {
    "01": "Delta ghi transaction vào JSON log. Lỗi ghi age='thirty' là bằng chứng enforcement thực tế; schema_mode='merge' cho phép thêm tier và giữ các hàng cũ với tier NULL. Hai nhóm tier không có nghĩa mọi hàng đã được backfill.",
    "02": "Compaction giảm số file nhỏ; Z-order thu hẹp khoảng min/max user_id để query 4242 bỏ qua file không phù hợp. Pruning được tính bằng tổng file sau tối ưu chia số file có khoảng chứa mục tiêu. Thời gian phụ thuộc cache, SSD và tải CPU; rubric chấp nhận speedup hoặc pruning đạt ngưỡng.",
    "03": "MERGE xử lý 100.000 hàng theo khóa, vừa cập nhật vừa chèn. Đọc version cũ không thay đổi version hiện tại. RESTORE tạo commit mới trỏ tới trạng thái tốt, vì vậy history vẫn chứa MERGE và RESTORE; score < 0 bằng 0 xác nhận phục hồi dữ liệu hiện tại.",
    "04": "Bronze giữ payload thô và retries. Silver dedup theo request_id nên giảm số hàng. Gold tổng hợp theo ngày/model: p50/p95 là quantile latency, error_rate là tỷ lệ status khác ok, cost_usd tính từ tokens với bảng giá minh họa của lab. Bảng CSV đầy đủ và assertions bổ sung kiểm tra các nhóm và miền giá trị.",
    "05": "Catalog quản lý định danh và metadata bảng. Predicate lọc ts được chuyển qua day(ts) để plan_files chỉ chọn ngày liên quan. Rename giữ field ID 4 nên không viết lại file dữ liệu. Partition evolution giữ nhiều spec ID; reader dùng từng spec để đọc cả layout cũ và mới. Tỷ lệ metadata lớn trong lab do các file rất nhỏ.",
    "06": "Compaction và clustering xử lý hai vấn đề khác nhau: số file và độ chọn lọc stats. VACUUM thu hồi file có tombstone nhưng không thấy file chưa commit; orphan sweep cần tập file được tham chiếu và age guard. Snapshot expiry trong phiên bản PyIceberg đang chạy giảm snapshots nhưng cần sweep manifest lists vật lý. Retention 0 chỉ dùng ở scratch; checkpoint rút ngắn log replay.",
    "07": "Column pruning giúp query topic bỏ qua blob, còn đọc một blob inline phải chạm row group nên amplification cao. Quantization int8 giảm dung lượng, cần đánh giá cả recall theo doc ID và topic fidelity. SQL search đọc bảng hiện tại; external index cũ vẫn trả hàng đã xóa. CDF delete events cung cấp ID để index consumer evict; thí nghiệm này tái hiện lỗi, chưa triển khai consumer production.",
    "08": "Silver partition theo agent_version và Gold so sánh hai policy. Training run pin version để replay cùng dữ liệu; demo chỉ so số bước, chưa chứng minh nội dung bằng nhau. Cache đo list_tables (không phải tools/list), confirmation do caller truyền và task poll là mô phỏng offline. Bốn bucket chỉ là mapping minh họa; CC-BY không phải public domain. Xóa subject ở version hiện tại chưa xóa lịch sử hoặc model đã train.",
}


def main():
    (OUT / "notebooks").mkdir(parents=True, exist_ok=True)
    (OUT / "logs").mkdir(exist_ok=True)
    manifest = {"started_at": datetime.now(timezone.utc).isoformat(),
                "python": sys.version, "platform": platform.platform(), "notebooks": []}
    for source in sorted((ROOT / "notebooks").glob("[0-9]*.py")):
        print(f"Executing {source.name}", flush=True)
        nb = jupytext.read(source)
        nb.cells.insert(1, nbformat.v4.new_code_cell(
            "import sys\nfrom pathlib import Path\n"
            "repo = next(p for p in [Path.cwd(), *Path.cwd().parents]\n"
            "            if (p / 'notebooks' / '_setup.py').is_file()\n"
            "            and (p / 'scripts' / 'lakehouse.py').is_file())\n"
            "sys.path.insert(0, str(repo / 'notebooks'))\n"
            "print('Execution root:', repo)\n"))
        if source.name.startswith("01"):
            nb.cells.append(nbformat.v4.new_code_cell(
                "logs = sorted(Path(table_path).glob('_delta_log/*.json'))\n"
                "print('Delta JSON commits:', [p.name for p in logs])\n"
                "print('Commit JSON:', logs[0].name)\n"
                "print(logs[0].read_text(encoding='utf-8'))\n"))
        nb.cells.append(nbformat.v4.new_markdown_cell(
            "### Giải thích kết quả (bản nháp có AI hỗ trợ)\n\n" + NOTES[source.name[:2]]))
        nb.metadata.kernelspec = {"display_name": "Python 3 (ipykernel)",
                                  "language": "python", "name": "python3"}
        # Explicit interpreter prevents accidentally executing a global Python kernel.
        client = NotebookClient(nb, timeout=600, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}})
        client.create_kernel_manager()
        client.km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        client.execute()
        target = OUT / "notebooks" / (source.stem + ".ipynb")
        nbformat.write(nb, target)
        text = "\n\n".join(
            output.get("text", output.get("data", {}).get("text/plain", ""))
            for cell in nb.cells if cell.cell_type == "code"
            for output in cell.get("outputs", []))
        (OUT / "logs" / (source.stem + ".txt")).write_text(text, encoding="utf-8")
        manifest["notebooks"].append({"file": str(target.relative_to(ROOT)),
                                      "code_cells": sum(c.cell_type == "code" for c in nb.cells),
                                      "completed_at": datetime.now(timezone.utc).isoformat()})
        print(f"Saved {target.name}", flush=True)
    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    (OUT / "execution.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    packages = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                              check=True, capture_output=True, text=True)
    (OUT / "requirements.lock.txt").write_text(packages.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
