# Reproduce

Environment used originally: Windows 10, NVIDIA RTX 5060 Laptop GPU (7.9 GB), Python 3.11.3, PyTorch 2.11.0+cu128, Ultralytics 8.4.190. Re-evaluation and bootstrap were run on CPU.

1. `pip install -r requirements.txt`
2. Obtain the dataset from your Roboflow project (version 2), export in YOLO format, place it at `data/detection_ready/` with `train/ valid/ test/` each holding `images/` and `labels/`, and create `data/detection_ready/data.yaml` from `data/data.yaml.template`.
3. `python scripts/audit_split_leakage.py` should report 163 / 20 / 21 photographs and no overlap.
4. Train (≈ 8–12 s per epoch on the laptop GPU): `python scripts/train.py --model yolo26s.pt --name YOLO26s_LIVE`. Repeat for `yolov8s.pt`, `yolo11s.pt`, `yolo12s.pt`. YOLO12 needs a GPU generation supported by FlashAttention for the fast path.
5. Evaluate and bootstrap with `scripts/evaluate.py` and `scripts/bootstrap_test_ci.py` (see README).
6. Rebuild figures: `python scripts/make_analysis_figures.py`.
7. Rebuild the report: `cd report && pdflatex report && bibtex report && pdflatex report && pdflatex report`.

Expect small differences (GPU non-determinism, library versions). With a 29-box test set, a 0.004 change in mAP@50:95 is normal.
