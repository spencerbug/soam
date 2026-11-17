# Study C confirmation tables

Ten independent fitted roots; ordinary 95% root intervals.

| Model | Brier [95% CI] | Prior NMSE | Late Brier | Ambiguous Brier | Recovery steps | Retained scalars | Mean root p95 μs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PC16 | 0.20495 [0.20217, 0.20785] | 0.03786 | 0.06756 | 0.25814 | 10.47 | 17 | 108.17 |
| PC32 | 0.20266 [0.20032, 0.20527] | 0.03612 | 0.04502 | 0.26421 | 4.93 | 33 | 104.39 |
| TWO16 | 0.18447 [0.18418, 0.18483] | 0.03162 | 0.01895 | 0.25000 | 0.07 | 33 | 116.18 |
| ADAPT1-C | 0.18633 [0.18619, 0.18646] | 0.02586 | 0.01455 | 0.25000 | 0.00 | 8 | 410.09 |
| ADAPT1-M | 0.18476 [0.18459, 0.18493] | 0.02416 | 0.01446 | 0.25000 | 0.00 | 15 | 407.73 |
| FILTER2-C | 0.18639 [0.18623, 0.18652] | 0.02556 | 0.01446 | 0.25000 | 0.00 | 7 | 290.13 |
| FILTER2-M | 0.18501 [0.18486, 0.18516] | 0.02422 | 0.01443 | 0.25000 | 0.00 | 13 | 300.86 |
| NISEMP-C | 0.18648 [0.18631, 0.18661] | 0.07373 | 0.01437 | 0.25000 | 0.00 | 7 | 351.83 |
| NISEMP-M | 0.18643 [0.18614, 0.18669] | 0.03847 | 0.01538 | 0.25000 | 0.00 | 13 | 356.42 |

## Frozen comparisons

- TWO16 vs PC16: supported bounded benefit; Brier improvement 0.02048 [0.01684, 0.02453], family-adjusted.
- TWO16 vs PC32: supported bounded benefit; Brier improvement 0.01819 [0.01505, 0.02204], family-adjusted.
- ADAPT1-M vs ADAPT1-C: precise exclusion of declared practical benefit; Brier improvement 0.00157 [0.00136, 0.00183], family-adjusted.
- TWO16 vs ADAPT1-M: precise exclusion of declared practical benefit; Brier improvement 0.00029 [-0.00032, 0.00083], family-adjusted.
