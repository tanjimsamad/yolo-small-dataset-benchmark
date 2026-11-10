# Why small datasets fail and why these models overfit

Summary of the argument in the report (section 6), with the evidence from this project.

| Cause | Mechanism | Evidence here |
|---|---|---|
| Few independent samples | Offline copies add robustness, not new scenes | 489 files = 163 photographs; 677 training boxes |
| Capacity vs data | 9–11 M-parameter networks can memorise even random labels (Zhang et al., 2017) | train box loss 0.11–0.29 vs validation 1.0–1.6 |
| Repeated identical pixels | Online augmentation off, so each epoch repeats the same images | design choice, no ablation |
| Noisy selection | Stopping and checkpointing on 27 validation boxes | epoch-to-epoch swings up to 0.07–0.19 mAP@50:95; best epochs 8–47 |
| Noisy evaluation | One missed box = 3.4 recall points on test | bootstrap CIs about ±0.1 |
| Pretraining is not regularisation | He et al., 2019 | validation plateaus within 8–47 epochs |

What would help, in order: more independent photographs; cross-validation over photographs; several seeds per model; online augmentation on (with an ablation); a larger held-out set. See report section 8.
