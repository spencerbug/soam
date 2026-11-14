# Study B2 confirmation tables

Ten independently fitted roots; ordinary95% paired-root bootstrap intervals. Frozen primary-family intervals are in `statistics.json`.

| Model | Ordinary J | Balanced C | Original corruption | Genuine change | Free32 |
| --- | --- | --- | --- | --- | --- |
| FILTER2 | 0.04394 [0.04263, 0.04526] | 0.23540 [0.22439, 0.24772] | 0.37082 [0.33934, 0.39812] | 0.05907 [0.05536, 0.06252] | 0.01340 [0.01250, 0.01424] |
| STABLE | 0.04394 [0.04263, 0.04526] | 0.23540 [0.22439, 0.24772] | 0.37082 [0.33934, 0.39812] | 0.05907 [0.05536, 0.06252] | 0.01340 [0.01250, 0.01424] |
| PC16 | 0.06395 [0.05913, 0.06866] | 0.14282 [0.13672, 0.14853] | 0.11048 [0.10451, 0.11623] | 0.10994 [0.10238, 0.11747] | 0.22458 [0.19737, 0.25249] |
| R100 | 0.01763 [0.01700, 0.01827] | 0.10651 [0.10200, 0.11092] | 0.10338 [0.09581, 0.11026] | 0.09986 [0.09366, 0.10549] | 0.01340 [0.01250, 0.01424] |
| NIS99 | 0.03159 [0.02853, 0.03475] | 0.02810 [0.02584, 0.03011] | 0.00228 [0.00221, 0.00236] | 0.54167 [0.49605, 0.58765] | 0.01340 [0.01250, 0.01424] |
| CHANNEL2 | 0.03526 [0.03423, 0.03625] | 0.16164 [0.15506, 0.16855] | 0.16240 [0.14522, 0.17783] | 0.06013 [0.05635, 0.06361] | 0.01340 [0.01250, 0.01424] |
| NISEMP | 0.04392 [0.04259, 0.04526] | 0.12918 [0.12328, 0.13451] | 0.01384 [0.00932, 0.01867] | 0.05907 [0.05536, 0.06252] | 0.01340 [0.01250, 0.01424] |
| ADAPT1 | 0.02034 [0.01979, 0.02087] | 0.11111 [0.10582, 0.11573] | 0.00613 [0.00527, 0.00724] | 0.05909 [0.05538, 0.06255] | 0.01340 [0.01250, 0.01424] |

## Expanded benchmark

| Model | Isolated | Two channels | Coherent snapshot | Sustained coherent | Dynamics | Heavy tails | Biased/correlated | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FILTER2 | 0.25215 | 0.13223 | 0.16821 | 0.53437 | 0.02131 | 0.08643 | 0.10359 | 0.00737 |
| STABLE | 0.25215 | 0.13223 | 0.16821 | 0.53437 | 0.02131 | 0.08643 | 0.10359 | 0.00737 |
| PC16 | 0.08233 | 0.07671 | 0.11960 | 0.44719 | 0.09380 | 0.07957 | 0.08389 | 0.09541 |
| R100 | 0.07979 | 0.04092 | 0.08021 | 0.37802 | 0.02862 | 0.02696 | 0.03632 | 0.00843 |
| NIS99 | 0.00233 | 0.00251 | 0.00730 | 0.15126 | 0.02437 | 0.02590 | 0.00515 | 0.00740 |
| CHANNEL2 | 0.12847 | 0.02187 | 0.15971 | 0.52557 | 0.02131 | 0.05064 | 0.08280 | 0.00737 |
| NISEMP | 0.00796 | 0.02114 | 0.16821 | 0.53437 | 0.02131 | 0.07050 | 0.08825 | 0.00737 |
| ADAPT1 | 0.00494 | 0.00687 | 0.16729 | 0.53331 | 0.02130 | 0.02895 | 0.03027 | 0.00736 |

## Real resources

| Model | Fitted scalars | Allocated persistent bytes | State/cov bytes | Counted linear MAC/step | CPU μs/step batch1 | CPU μs/step batch20 | Base fit CPU s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FILTER2 | 64 | 460 | 24 | 85.875 | 68.20 | 4.02 | 0.052 |
| STABLE | 64 | 920 | 48 | 125.375 | 86.76 | 4.86 | 0.052 |
| PC16 | 1340 | 5360 | 64 | 678.000 | 28.73 | 1.96 | 2.860 |
| R100 | 64 | 920 | 48 | 125.375 | 89.11 | 5.23 | 0.052 |
| NIS99 | 64 | 920 | 48 | 125.375 | 87.96 | 4.88 | 0.052 |
| CHANNEL2 | 64 | 920 | 48 | 155.375 | 102.39 | 5.80 | 0.052 |
| NISEMP | 64 | 920 | 48 | 125.375 | 89.17 | 5.00 | 0.052 |
| ADAPT1 | 64 | 920 | 56 | 149.375 | 102.78 | 5.82 | 0.052 |

MACs exclude solves/nonlinear/elementwise work. Schedule every4, same minimal inference driver, initialization included. These are a different accounting surface from historical Study B’s average over54 cells. Robust linear arithmetic is float64; original/neural float32. Detailed solve dimensions/call counts, p95/max times, hyperparameters and exposure are in `resources.json`. Each robust corrector reuses the same FILTER2 fit.

## Recovery and calibration

Recovery is onset-relative post-correction recovery; eight PRE-onset errors set its threshold. Censoring and fault-end recovery are in condition-statistics. NIS is pre-gating; ADAPT1 uses data-dependent R.

| Model | Change recovery steps | Change censoring | Clean rejection | High-noise rejection | Partial state95 coverage | High-noise state95 coverage |
| --- | --- | --- | --- | --- | --- | --- |
| FILTER2 | 0.8280 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.6675 |
| STABLE | 0.8280 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.6675 |
| PC16 | 6.9910 | 0.0010 | 0.0000 | 0.0000 | not modeled | not modeled |
| R100 | 12.2190 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.9775 |
| NIS99 | 13.6840 | 0.0000 | 0.0033 | 0.9973 | 1.0000 | 0.9704 |
| CHANNEL2 | 1.6520 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.7488 |
| NISEMP | 0.8280 | 0.0000 | 0.0133 | 0.0265 | 1.0000 | 0.6729 |
| ADAPT1 | 0.8960 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.9599 |
