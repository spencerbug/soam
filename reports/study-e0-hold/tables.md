# E0-HOLD v1: complete numerical tables

Formal NAV32 result: **negative declared joint fix**. All intervals use twenty independent paired roots. The primary family uses alpha=.05/13 per interval; control tables are descriptive 95% intervals.

## Confirmatory NAV32 family

| Quantity | Mean [adjusted interval] | Width | Requirement | Status |
| --- | --- | --- | --- | --- |
| absolute/free_nmse | 0.0365065 [0.032524, 0.0404439] | 0.00791993 | upper <= 0.05; width <= 0.04 | pass |
| absolute/grounded_nmse | 0.00805349 [0.00710608, 0.00927468] | 0.00216861 | upper <= 0.05; width <= 0.04 | pass |
| absolute/stationary_deg | 5.69773 [5.25935, 6.18261] | 0.923261 | upper <= 5.0; width <= 4.0 | negative |
| absolute/normal_ratio | 0.139958 [0.113728, 0.163648] | 0.0499208 | upper <= 0.5; width <= 0.4 | pass |
| absolute/normal_pose_deg | 0.221384 [0.196532, 0.244105] | 0.0475733 | upper <= 3.0; width <= 3.0 | pass |
| absolute/tangent_ratio | 0.982743 [0.977872, 0.987488] | 0.00961568 | lower >= 0.8 and upper <= 1.2; width <= 0.4 | pass |
| absolute/return_nmse | 0.00530636 [0.00490805, 0.00574642] | 0.00083837 | upper <= 0.05; width <= 0.04 | pass |
| gain/stationary_deg | 6.63463 [5.01706, 8.80467] | 3.78762 | lower >= 5.0; width <= 4.0 | pass |
| degradation/free_nmse | 0.00360598 [-0.0010272, 0.00673195] | 0.00775915 | upper <= 0.01; width <= 0.02 | pass |
| degradation/grounded_nmse | 0.00115804 [-0.00104343, 0.00267876] | 0.00372218 | upper <= 0.01; width <= 0.02 | pass |
| degradation/return_nmse | 0.00128296 [0.000913756, 0.00163179] | 0.000718033 | upper <= 0.01; width <= 0.02 | pass |
| degradation/normal_ratio | 0.0331174 [0.00731248, 0.0621835] | 0.0548711 | upper <= 0.05; width <= 0.1 | unresolved |
| degradation/normal_pose_deg | 0.035141 [0.0103173, 0.0590619] | 0.0487446 | upper <= 0.5; width <= 1.0 | pass |

## All model/arm endpoints (descriptive 95%)

| Model/arm | free_nmse | grounded_nmse | stationary_deg | normal_ratio | normal_pose_deg | tangent_ratio | return_nmse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NAV32/SHORT24 | 0.0329005 [0.0295632, 0.0371969] | 0.00689544 [0.00581089, 0.00826015] | 12.3324 [11.2445, 13.6428] | 0.10684 [0.0945697, 0.119538] | 0.186243 [0.177003, 0.195486] | 0.987359 [0.983262, 0.991063] | 0.00402339 [0.00377164, 0.00429183] |
| NAV32/LONG128 | 0.0365065 [0.0338843, 0.0392005] | 0.00805349 [0.00735645, 0.00884529] | 5.69773 [5.38681, 6.0163] | 0.139958 [0.122521, 0.156568] | 0.221384 [0.204545, 0.237333] | 0.982743 [0.979427, 0.986044] | 0.00530636 [0.00502794, 0.00560204] |
| SYM32/SHORT24 | 0.327634 [0.303794, 0.352675] | 0.0301367 [0.0288127, 0.0314533] | 17.0849 [15.5292, 18.7912] | 0.223715 [0.213173, 0.234865] | 0.87642 [0.831257, 0.925656] | 0.990595 [0.98527, 0.995265] | 0.0128774 [0.0118318, 0.0139723] |
| SYM32/LONG128 | 0.354281 [0.328374, 0.37977] | 0.0356162 [0.0338523, 0.0372869] | 5.38794 [5.07228, 5.70147] | 0.21948 [0.208644, 0.229673] | 0.652449 [0.630196, 0.675487] | 0.984764 [0.981605, 0.987671] | 0.0157859 [0.014418, 0.017217] |
| GRU32/SHORT24 | 0.0771703 [0.0682723, 0.0874571] | 0.00735498 [0.00699708, 0.00775162] | 12.9749 [11.2569, 14.8145] | 0.120523 [0.113435, 0.127281] | 0.986031 [0.953409, 1.01723] | 0.999761 [0.998878, 1.0006] | 0.0071584 [0.00679334, 0.00754419] |
| GRU32/LONG128 | 0.265815 [0.237733, 0.294108] | 0.0132893 [0.01235, 0.0143347] | 2.63115 [2.38296, 2.87429] | 0.119239 [0.113648, 0.124772] | 0.838072 [0.804717, 0.870595] | 0.99985 [0.999045, 1.00072] | 0.0122636 [0.0115378, 0.0130297] |
| PCA2/REFERENCE | 0.000568776 [0.000534997, 0.000609759] | 4.5372e-05 [4.14395e-05, 5.03748e-05] | 1.66684e-06 [1.58038e-06, 1.76415e-06] | 1 [1, 1] | 9.60871e-06 [7.9509e-06, 1.17784e-05] | 1 [1, 1] | 4.03087e-05 [3.73023e-05, 4.37565e-05] |

## Paired LONG128 minus SHORT24 (descriptive 95%)

| Model | free_nmse | grounded_nmse | stationary_deg | normal_ratio | normal_pose_deg | tangent_ratio | return_nmse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NAV32 | 0.00360598 [0.00067086, 0.00592524] | 0.00115804 [-0.000208432, 0.00226305] | -6.63463 [-8.05516, -5.4285] | 0.0331174 [0.0155364, 0.0519631] | 0.035141 [0.0186508, 0.0515727] | -0.00461644 [-0.00945553, 8.34246e-05] | 0.00128296 [0.00103356, 0.00153182] |
| SYM32 | 0.026647 [-0.0015387, 0.0533523] | 0.00547946 [0.00386384, 0.00711058] | -11.6969 [-13.3172, -10.1601] | -0.00423446 [-0.0169767, 0.00777109] | -0.223971 [-0.272848, -0.180757] | -0.00583062 [-0.011708, 0.000534356] | 0.00290854 [0.00181662, 0.0040831] |
| GRU32 | 0.188645 [0.164413, 0.213374] | 0.00593434 [0.00521388, 0.00675767] | -10.3437 [-12.1392, -8.65834] | -0.00128351 [-0.00660077, 0.00433345] | -0.147959 [-0.170517, -0.126687] | 8.89921e-05 [-0.00120727, 0.0014077] | 0.00510523 [0.00460612, 0.00562662] |

## Direction/speed diagnostics (root means; no confirmatory claim)

| Cell | Interpolation | Extrapolation | Positive constant action | Negative constant action |
| --- | --- | --- | --- | --- |
| NAV32/SHORT24 | 0.0306883 | 0.0328403 | 0.0384445 | 0.0364302 |
| NAV32/LONG128 | 0.0369944 | 0.0377133 | 0.0535167 | 0.052227 |
| SYM32/SHORT24 | 0.0895993 | 0.758702 | 1.55292 | 1.45803 |
| SYM32/LONG128 | 0.104007 | 0.767203 | 1.40658 | 1.49702 |
| GRU32/SHORT24 | 0.0301573 | 0.187609 | 0.0777692 | 0.0581635 |
| GRU32/LONG128 | 0.0859706 | 0.504425 | 0.697544 | 0.668857 |
| PCA2/REFERENCE | 0.000407857 | 0.000903689 | 0.000501483 | 0.000507971 |

## Resource and exposure means per fitted root

| Cell | Scalars / bytes | Active floats | Fit CPU s | Evaluation CPU s | Extra stationary transitions | Final 100 loss | Previous 100 loss |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NAV32/SHORT24 | 4044 / 16176 | 32 | 2.9008 | 0.0717 | 0.0 | 0.0308798 | 0.0329597 |
| NAV32/LONG128 | 4044 / 16176 | 32 | 9.6263 | 0.0723 | 501248.8 | 0.038609 | 0.0420363 |
| SYM32/SHORT24 | 4044 / 16176 | 32 | 2.8901 | 0.0715 | 0.0 | 0.0408989 | 0.043945 |
| SYM32/LONG128 | 4044 / 16176 | 32 | 9.5418 | 0.0718 | 501248.8 | 0.0461236 | 0.050601 |
| GRU32/SHORT24 | 5324 / 21296 | 32 | 2.8356 | 0.0767 | 0.0 | 0.0295213 | 0.0317592 |
| GRU32/LONG128 | 5324 / 21296 | 32 | 9.4985 | 0.0765 | 501248.8 | 0.0421591 | 0.0479763 |
| PCA2/REFERENCE | 52 / 208 | 6 | 0.4879 | 0.0872 | 0.0 | n/a | n/a |

Each neural fit has 19,200 original prefix episodes / 480,000 distinct original sensory snapshots and 600 optimizer updates. Extra stationary targets reuse existing supplied targets; they add no observations. PCA2 uses two passes over the original data and no optimizer steps. Model parameter counts include initializers/readouts/correction. The common fixed projection is 24 float32 values (96 bytes). Evaluation CPU includes geometry diagnostics and is not a production-latency benchmark.
