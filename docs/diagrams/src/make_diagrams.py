#!/usr/bin/env python3
"""
Generates the four SVG diagrams used in README.md, ARCHITECTURE.md and the report.

Run:  python docs/diagrams/src/make_diagrams.py
Output: docs/diagrams/*.svg   (plain, editable SVG; edit this file and re-run, or open the
SVGs directly in Inkscape / diagrams.net.)

Every number printed in a diagram is taken from the project's own files:
  data/annotation_audit.csv, data/class_distribution.csv, reports/yolo_compatibility.csv,
  runs/*/args.yaml, runs/*/results.csv, reports/comparison_visualizations/*.csv
and from the image-name audit described in docs/DATASET.md.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1]
FONT = "Segoe UI, Helvetica, Arial, sans-serif"
INK = "#1a202c"
MUTED = "#4a5568"

STYLE = {                       # fill, stroke  (colour is never the only cue: shapes and labels differ too)
    "data":  ("#E8F1FB", "#2B6CB0"),
    "proc":  ("#F1F5F9", "#475569"),
    "model": ("#FFF4E0", "#B7791F"),
    "eval":  ("#E9F7EF", "#2F855A"),
    "warn":  ("#FDECEC", "#C53030"),
    "note":  ("#FFFFFF", "#718096"),
}


class Svg:
    def __init__(self, w, h, title, desc):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d" font-family="{FONT}">',
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>',
            '<defs>'
            f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            '<marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#C53030"/></marker>'
            '</defs>',
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>',
        ]

    def text(self, x, y, s, size=15, weight="400", anchor="start", fill=INK, italic=False):
        st = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'fill="{fill}"{st}>{escape(s)}</text>')

    def box(self, x, y, w, h, title, lines=(), kind="proc", tsize=16, lsize=13.5, dashed=False, rx=10):
        f, s = STYLE[kind]
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="2"{dash}/>')
        cy = y + 8 + tsize
        self.text(x + w / 2, cy, title, tsize, "700", "middle")
        cy += 6
        for ln in lines:
            cy += lsize + 5
            self.text(x + w / 2, cy, ln, lsize, "400", "middle", MUTED)

    def band(self, x, y, w, h, label):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#FAFBFC" stroke="#CBD5E0" stroke-width="1.5"/>')
        self.text(x + 16, y + 26, label, 15, "700", fill="#2D3748")

    def arrow(self, pts, label=None, lpos=None, red=False, dashed=False):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        col = "#C53030" if red else MUTED
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"{dash} marker-end="url(#{"ahr" if red else "ah"})"/>')
        if label:
            lx, ly = lpos if lpos else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2 - 8)
            self.text(lx, ly, label, 12.5, "400", "middle", col, italic=True)

    def save(self, name):
        (OUT / name).write_text("\n".join(self.parts + ["</svg>"]), encoding="utf-8")
        print("wrote", OUT / name)


# --------------------------------------------------------------------------------------
# 1. End-to-end pipeline
# --------------------------------------------------------------------------------------
def pipeline():
    s = Svg(1500, 900, "End-to-end benchmark pipeline",
            "Data preparation, training of four YOLO small models with one recipe, and evaluation with bootstrap confidence intervals.")
    s.text(40, 40, "Project pipeline: four YOLO small models, one small custom dataset", 22, "700")

    s.band(20, 62, 1460, 230, "1  Data preparation")
    xs = [40, 345, 650, 955, 1245]
    s.box(xs[0], 105, 255, 150, "Roboflow project", ["Fault_Detection_Model v2", "bounding-box annotation", "2 classes: Good, Miss_Print"], "data")
    s.box(xs[1], 105, 255, 150, "Four YOLO exports", ["v8, v11, v12, v26 .zip", "SHA-256 of every image and", "label file compared: identical"], "proc")
    s.box(xs[2], 105, 255, 150, "data/canonical", ["1,060 files (530 images", "+ 530 label files)", "extracted once, read-only"], "data")
    s.box(xs[3], 105, 255, 150, "Annotation audit", ["checks class ids and [0,1] range;", "6 polygon labels converted", "to boxes (train split)"], "proc")
    s.box(xs[4], 105, 215, 150, "detection_ready", ["train 489 images", "valid 20 · test 21", "data.yaml (nc = 2)"], "data")
    for a, b in zip(xs[:-1], xs[1:]):
        s.arrow([(a + (255), 180), (b - 4, 180)])

    s.band(20, 320, 1460, 250, "2  Training")
    s.box(40, 365, 255, 170, "EDA + compatibility", ["class balance, box size, all", "images 640 x 640; all four", "checkpoints load (READY)"], "proc")
    s.box(345, 365, 215, 170, "Smoke test", ["YOLOv8s, 2 epochs,", "checks GPU, paths,", "data.yaml, memory"], "proc")
    models = [("YOLOv8s", "11.2 M params"), ("YOLO11s", "9.5 M params"), ("YOLO12s", "9.3 M params"), ("YOLO26s", "10.0 M params")]
    mx = [610, 785, 960, 1135]
    for (n, p), x in zip(models, mx):
        s.box(x, 365, 160, 105, n, ["COCO-pretrained", p], "model")
    s.box(610, 485, 685, 66, "Identical recipe for all four", ["AdamW lr 0.001 · batch 4 · 640 px · patience 25 · seed 42 · online augmentation off"], "note", tsize=14.5, lsize=13, dashed=True)
    s.box(1320, 365, 140, 170, "Early stop", ["best epoch +", "25 epochs", "(8s: 26 → 51)"], "warn", lsize=12.5)
    s.arrow([(xs[4] + 107, 255), (xs[4] + 107, 300), (167, 300), (167, 360)])
    s.arrow([(295, 450), (341, 450)])
    s.arrow([(560, 417), (606, 417)])
    s.arrow([(1295, 417), (1316, 417)])

    s.band(20, 598, 1460, 280, "3  Evaluation")
    s.box(40, 645, 255, 150, "best.pt per model", ["checkpoint with the best", "validation fitness", "(20-image valid split)"], "model")
    s.box(345, 645, 255, 150, "Single test pass", ["model.val(split='test')", "21 images · 29 boxes", "never used for training"], "eval")
    s.box(650, 645, 275, 150, "Metrics", ["Precision, Recall, F1,", "mAP@50, mAP@50:95,", "per class + PR / F1 / confusion"], "eval")
    s.box(975, 645, 255, 150, "Bootstrap CIs", ["2,000 image resamples,", "paired model differences", "scripts/bootstrap_test_ci.py"], "eval")
    s.box(1280, 645, 180, 150, "Outputs", ["reports/ figures", "results/ tables", "report PDF"], "data")
    s.arrow([(952, 551), (952, 580), (167, 580), (167, 640)])
    for a, b in [(295, 341), (600, 646), (925, 971), (1230, 1276)]:
        s.arrow([(a, 720), (b - 2, 720)])
    s.text(750, 842, "Test split is touched once per model; the validation split steers early stopping and checkpoint choice.", 14, "400", "middle", MUTED, italic=True)
    s.text(750, 864, "Numbers shown come from args.yaml, results.csv, yolo_compatibility.csv and annotation_audit.csv in this repository.", 13, "400", "middle", MUTED, italic=True)
    s.save("01_pipeline.svg")


# --------------------------------------------------------------------------------------
# 2. Dataset split and augmentation flow
# --------------------------------------------------------------------------------------
def dataset_flow():
    s = Svg(1500, 725, "Dataset construction, splitting and offline augmentation",
            "204 original photographs are split before augmentation; only the 163 training photographs are tripled by Roboflow, giving 489 training images. Validation and test contain one image per photograph.")
    s.text(40, 40, "Where the 530 images come from, and how many are independent", 22, "700")

    s.box(40, 80, 300, 130, "204 original photographs", ["pharmaceutical carton photographed", "on different surfaces and angles,", "labelled with boxes in Roboflow"], "data")
    s.box(430, 80, 300, 130, "Split by photograph", ["163 train · 20 valid · 21 test", "no photograph appears in", "two splits (0 shared name stems)"], "proc")
    s.arrow([(340, 145), (426, 145)])

    # three lanes
    s.box(820, 60, 330, 90, "train: 163 photographs", ["Roboflow offline augmentation: 3 images", "per photograph (rotation, noise seen)"], "model")
    s.box(820, 165, 330, 70, "valid: 20 photographs", ["not augmented (one image each)"], "eval", lsize=13)
    s.box(820, 250, 330, 70, "test: 21 photographs", ["not augmented (one image each)"], "eval", lsize=13)
    s.arrow([(730, 135), (766, 135), (766, 105), (816, 105)])
    s.arrow([(730, 145), (766, 145), (766, 200), (816, 200)])
    s.arrow([(730, 155), (750, 155), (750, 285), (816, 285)])

    s.box(1230, 60, 240, 90, "489 images", ["677 objects", "371 Good · 306 Miss_Print"], "model", lsize=13)
    s.box(1230, 165, 240, 70, "20 images", ["27 objects (15 / 12)"], "eval", lsize=13)
    s.box(1230, 250, 240, 70, "21 images", ["29 objects (14 / 15)"], "eval", lsize=13)
    for y in (105, 200, 285):
        s.arrow([(1150, y), (1226, y)])

    # effective sample size
    s.band(20, 360, 1460, 335, "What this means for learning and for evaluation")
    s.box(40, 410, 430, 112, "Effective training set", ["489 files, but only 163 distinct scenes:", "the 3 copies of a photograph share", "the same object, background and label"], "warn")
    s.box(535, 410, 430, 112, "Validation: 20 images", ["27 boxes decide early stopping and", "which epoch becomes best.pt;", "one missed box moves recall by 3.7 points"], "warn")
    s.box(1030, 410, 430, 112, "Test: 21 images", ["29 boxes give every metric;", "one missed box moves recall by 3.4 points", "95 % CI of mAP@50:95 is about ±0.1"], "warn")
    s.arrow([(255, 522), (255, 572)], red=True)
    s.arrow([(750, 522), (750, 572)], red=True)
    s.arrow([(1245, 522), (1245, 572)], red=True)
    s.box(40, 575, 430, 95, "Risk: memorisation", ["train loss keeps falling while", "validation loss stalls (figure A)"], "note", lsize=13.5, dashed=True)
    s.box(535, 575, 430, 95, "Risk: noisy model selection", ["largest epoch-to-epoch jump in val", "mAP@50:95: 0.07-0.19 per model"], "note", lsize=13.5, dashed=True)
    s.box(1030, 575, 430, 95, "Risk: unstable ranking", ["12s and 26s are not separable;", "8s and 11s are not separable"], "note", lsize=13.5, dashed=True)
    s.save("02_dataset_split_augmentation.svg")


# --------------------------------------------------------------------------------------
# 3. Training and evaluation workflow for one model
# --------------------------------------------------------------------------------------
def training_workflow():
    s = Svg(1500, 820, "Training and evaluation workflow for one model",
            "Pretrained weights are fine-tuned for up to 100 epochs; each epoch is validated on the 20-image validation split; early stopping and best-checkpoint selection both use that split; the test split is evaluated once.")
    s.text(40, 40, "Training loop and where the data splits are used (repeated for each of the four models)", 22, "700")

    s.box(40, 90, 250, 120, "Pretrained weights", ["yolov8s / yolo11s /", "yolo12s / yolo26s .pt", "(COCO, 80 classes)"], "model")
    s.box(350, 90, 250, 120, "Replace head", ["2 classes: Good, Miss_Print;", "class head re-initialised,", "other matching layers kept"], "proc")
    s.box(660, 90, 270, 120, "Train epoch", ["489 images, batch 4,", "box + cls (+ dfl) loss,", "AdamW lr 0.001, 640 px"], "model")
    s.box(990, 90, 270, 120, "Validate epoch", ["20 images / 27 boxes", "P, R, mAP@50, mAP@50:95", "val losses"], "eval")
    s.box(1310, 90, 150, 120, "Save", ["last.pt every", "epoch; best.pt on", "best fitness"], "data", lsize=12.5)
    s.arrow([(290, 150), (346, 150)])
    s.arrow([(600, 150), (656, 150)])
    s.arrow([(930, 150), (986, 150)])
    s.arrow([(1260, 150), (1306, 150)])

    # loop back (drawn above the row so no lines cross)
    s.arrow([(1385, 90), (1385, 66), (795, 66), (795, 86)], "next epoch (up to 100)", (1090, 60))

    s.box(660, 320, 600, 120, "Early stopping check", ["patience 25: stop when fitness has not improved for 25 epochs", "run lengths: YOLOv8s 51 (best 26) · YOLO11s 33 (best 8)", "YOLO12s 72 (best 47) · YOLO26s 64 (best 39)"], "warn", lsize=13)
    s.arrow([(1125, 214), (1125, 316)], "fitness each epoch", (1195, 270))
    s.box(40, 320, 540, 120, "What is held fixed across models", ["data, seed 42, optimizer AdamW, lr0 0.001, batch 4, image size 640,", "patience 25, online augmentation off (mosaic, flips, HSV, scale = 0),", "no hyper-parameter search; one run per model"], "note", lsize=13, dashed=True)

    s.band(20, 480, 1460, 300, "After training")
    s.box(40, 525, 270, 120, "best.pt", ["epoch with highest validation", "fitness (0.1 mAP@50 +", "0.9 mAP@50:95)"], "model")
    s.box(370, 525, 300, 120, "Test evaluation (once)", ["21 images / 29 boxes", "model.val(split='test')", "conf 0.001, IoU 0.7, 640 px"], "eval")
    s.box(730, 525, 330, 120, "Point estimates", ["P, R, F1, mAP@50,", "mAP@50:95, per-class table,", "PR / F1 / confusion plots"], "eval")
    s.box(1120, 525, 340, 120, "Uncertainty", ["bootstrap over 21 images:", "95 % CI and paired differences", "between models"], "eval")
    s.arrow([(310, 585), (366, 585)])
    s.arrow([(670, 585), (726, 585)])
    s.arrow([(1060, 585), (1116, 585)])
    s.arrow([(795, 440), (795, 470), (175, 470), (175, 521)], "stop: keep best.pt", (480, 462))
    s.box(40, 690, 1420, 70, "Selection effect to keep in mind", ["The validation split chooses both the stopping point and best.pt, so its scores are optimistic; only the test split is an unbiased (but very noisy) estimate."], "warn", tsize=15, lsize=13.5)
    s.save("03_training_evaluation_workflow.svg")


# --------------------------------------------------------------------------------------
# 4. Overfitting mechanism (causal chain with measured evidence)
# --------------------------------------------------------------------------------------
def overfitting():
    s = Svg(1500, 720, "Why a small dataset leads to overfitting and unreliable rankings",
            "Causal chain from few independent photographs and a high-capacity pretrained detector to memorisation, noisy validation and wide test intervals, with the measured evidence from this project.")
    s.text(40, 40, "Mechanism of overfitting on this dataset, with measured evidence", 22, "700")

    s.box(40, 80, 400, 112, "Few independent samples", ["163 training photographs (489 files),", "677 boxes in 2 classes;", "Ultralytics advises ≥1,500 images/class"], "data")
    s.box(550, 80, 400, 112, "High-capacity model", ["9.3-11.2 M parameters,", "pretrained on COCO;", "online augmentation switched off"], "model")
    s.box(1060, 80, 400, 112, "Repeated exposure", ["the same pixels in every epoch;", "3 near-identical copies of each scene;", "batch of 4 gives noisy updates"], "proc")
    s.arrow([(440, 136), (546, 136)])
    s.arrow([(950, 136), (1056, 136)])

    s.box(40, 255, 400, 112, "Memorisation", ["train box loss, YOLOv8s: 1.47 → 0.11", "train box loss, YOLO12s: 1.52 → 0.11", "training loss falls on every curve"], "warn", lsize=13)
    s.box(550, 255, 400, 112, "Generalisation gap", ["val box loss stays 1.0-1.3:", "YOLOv8s min 1.10 (epoch 12), last 1.31", "YOLO11s min 1.04 (22), last 1.46"], "warn", lsize=13)
    s.box(1060, 255, 400, 112, "Early best epoch", ["best checkpoint comes early:", "YOLO11s epoch 8 of 33,", "YOLOv8s epoch 26 of 51"], "warn", lsize=13)
    s.arrow([(240, 192), (240, 251)], red=True)
    s.arrow([(750, 192), (750, 251)], red=True)
    s.arrow([(1260, 192), (1260, 251)], red=True)

    s.box(40, 430, 700, 112, "Noisy validation signal (20 images, 27 boxes)", ["val mAP@50:95 of YOLOv8s ranges 0.49-0.65 after the first 5 epochs;", "early stopping and best.pt rest on this curve, so the", "chosen checkpoint is partly selected by luck"], "warn", lsize=13)
    s.box(800, 430, 660, 112, "Noisy test signal (21 images, 29 boxes)", ["95 % bootstrap CI of mAP@50:95: YOLOv8s 0.43-0.71,", "YOLO11s 0.50-0.72, YOLO12s 0.63-0.81, YOLO26s 0.60-0.77;", "12s minus 26s = 0.035, CI -0.02 to +0.10"], "warn", lsize=13)
    s.arrow([(240, 367), (240, 426)], red=True)
    s.arrow([(650, 367), (650, 426)], red=True)
    s.arrow([(1260, 367), (1260, 426)], red=True)

    s.box(40, 590, 1420, 100, "Consequence", ["High training accuracy does not show that the model has learned the defect; a ranking built on 29 test boxes is a hypothesis, not a result.", "Fixes: more independent photographs, stronger online augmentation, k-fold or repeated runs, larger validation/test sets, frozen early layers."], "note", tsize=16, lsize=14, dashed=True)
    s.arrow([(390, 542), (390, 586)], red=True)
    s.arrow([(1130, 542), (1130, 586)], red=True)
    s.save("04_overfitting_mechanism.svg")


if __name__ == "__main__":
    pipeline()
    dataset_flow()
    training_workflow()
    overfitting()
