# Working principles

**Transfer learning.** Each model starts from a COCO-pretrained checkpoint and is fine-tuned. Pretraining makes a small dataset workable, but it is not a regulariser: with unchanged hyper-parameters pretrained models can still overfit (He et al., 2019).

**Single-stage anchor-free detection.** The network predicts, for each location on several feature-map scales, class scores and box coordinates in one pass. Losses combine a box-regression term, a classification term and (YOLOv8/11/12) a distribution-focal term; YOLO26 removes the distribution-focal term.

**Metrics.**
* *Precision / recall*: here the class means at the confidence that maximises the mean F1 curve (Ultralytics convention); the tables' F1 is the harmonic mean of these two means.
* *mAP@50*: mean average precision at IoU 0.50. *mAP@50:95*: average over IoU 0.50 to 0.95 in steps of 0.05; it rewards tight boxes.
* *Fitness* used for `best.pt`: 0.1·mAP@50 + 0.9·mAP@50:95 on the validation split.

**Early stopping.** Training stops after 25 epochs without fitness improvement; the checkpoint with the best validation fitness is kept. With 20 validation images this selection is noisy.

**Bootstrap.** Resample the test images with replacement 2 000 times, recompute the metrics on each resample, and report the 2.5–97.5 percentile range. The same resamples are used for all models, so model differences are paired. This measures test-sampling variance only, not training-seed variance.

**Leakage audit.** Roboflow names augmented copies `<stem>.rf.<hash>`; the stem identifies the source photograph. A split is leak-free when no stem occurs in two splits.
