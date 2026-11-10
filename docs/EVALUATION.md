# Evaluation protocol

1. Validation split: evaluated every epoch by Ultralytics; used for early stopping and `best.pt` choice.
2. Test split: evaluated once per `best.pt` (`scripts/evaluate.py` or the notebook). Tables: `results/tables/`.
3. Uncertainty: `scripts/bootstrap_test_ci.py` (2 000 image-level resamples, seed 42) -> `results/bootstrap/` (`bootstrap_ci.csv`, `paired_differences.csv`, `bootstrap_summary.json`, forest plot).
4. Figures: `scripts/make_analysis_figures.py` -> `figures/analysis/`.

Known numerical note: re-evaluating on CPU reproduced the logged test metrics to four decimals except YOLO26s mAP@50:95 (0.6925 CPU vs 0.6969 logged on GPU). Bootstrap intervals use the CPU values.

Operating-point counts (confidence ≥ 0.25, IoU 0.5): YOLOv8s TP 23 / FP 3 / FN 6; YOLO11s 26 / 6 / 3; YOLO12s 26 / 0 / 3; YOLO26s 26 / 1 / 3.

What is not measured: training-seed variance, inference latency, robustness to other products, lighting or cameras.
