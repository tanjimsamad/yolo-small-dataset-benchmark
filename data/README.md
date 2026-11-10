# Data

The images and labels are not included. Rebuild them from the Roboflow project `Fault_Detection_Model`, version 2 (YOLO export).

Expected layout (create `data/detection_ready/data.yaml` from `data.yaml.template`):

```
data/detection_ready/
  data.yaml
  train/images  train/labels   # 489 images
  valid/images  valid/labels   # 20 images
  test/images   test/labels    # 21 images
```

Included here: `annotation_audit.csv` (counts per split, converted polygons) and `class_distribution.csv`.
Class ids: 0 = Good, 1 = Miss_Print. Confirm the order in your export.
