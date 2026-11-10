# Dataset

* Source: Roboflow project `Fault_Detection_Model`, version 2; bounding-box annotations; images 640×640.
* Classes: `0 Good`, `1 Miss_Print` (pharmaceutical packaging cartons).
* Exports: YOLOv8, YOLO11, YOLO12 and YOLO26 formats; SHA-256 of every file was identical, so one copy (530 images + 530 label files) was used.

| Split | Photographs | Images | Boxes | Good / Miss_Print |
|---|---|---|---|---|
| train | 163 | 489 | 677 | 371 / 306 |
| valid | 20 | 20 | 27 | 15 / 12 |
| test | 21 | 21 | 29 | 14 / 15 |

Training files are three offline-augmented copies of each photograph (rotation with black borders, speckle noise seen in samples). Six training labels were polygons and were converted to enclosing boxes. Photograph counts are inferred from file-name stems.

Provenance of the rebuild is in `data/README.md`. The images are **not** distributed with this repository; check the Roboflow project's licence before sharing them.

Files: `data/annotation_audit.csv`, `data/class_distribution.csv`, `results/tables/bounding_box_statistics.csv`, `results/tables/image_statistics.csv`.
