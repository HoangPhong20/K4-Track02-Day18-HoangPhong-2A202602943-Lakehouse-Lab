"""Validate preserved notebook outputs and submission artifacts."""
from pathlib import Path
import hashlib
import json
import nbformat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission"

if __name__ == "__main__":
    files = sorted((OUT / "notebooks").glob("*.ipynb"))
    assert len(files) == 8
    rows = []
    for file in files:
        nb = nbformat.read(file, as_version=4)
        nbformat.validate(nb)
        code = [c for c in nb.cells if c.cell_type == "code"]
        assert all(c.execution_count is not None for c in code), file
        assert not any(o.output_type == "error" for c in code for o in c.get("outputs", [])), file
        assert list((OUT / "screenshots").glob(file.stem + "_*.png")), file
        text = "\n\n".join(o.get("text", o.get("data", {}).get("text/plain", ""))
                            for c in code for o in c.get("outputs", []))
        assert text == (OUT / "logs" / (file.stem + ".txt")).read_text(encoding="utf-8"), file
        assert "Path.cwd().parents" in code[0].source, file
        rows.append({"notebook": file.name, "code_cells": len(code),
                     "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
    words = len((OUT / "REFLECTION.md").read_text(encoding="utf-8").split())
    assert words <= 200, words
    for name in ("INFO.md", "AI_USAGE.md", "RESULTS.md", "requirements.lock.txt", "execution.json"):
        assert (OUT / name).is_file(), name
    report = {"notebooks": rows, "png_count": len(list((OUT / "screenshots").glob("*.png"))),
              "reflection_words": words}
    (OUT / "validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Validated {len(rows)} executed notebooks, {report['png_count']} images; reflection {words}/200 words")
