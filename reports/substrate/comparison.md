# Substrate results

Mean ± sample standard deviation across seeds; a single seed has no estimated spread. NMSE is MSE divided by target feature energy.

## substrate

Source commit: `e861742bd3c2393d7870461771e55bb5f9cd3199`. Source SHA-256: `2764fbb82a0b3e3c1d4cbcf650b1fae8a2c91b17f76f870002fe9dcc28b5d259`.

| Model | Seeds | Parameters | Grounded NMSE | Free NMSE | Switching NMSE | Long NMSE | Perturbation final gap ratio | Train seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| additive | 3 | 2892 | 0.0084 ± 0.0009 | 0.0678 ± 0.0062 | 0.0630 ± 0.0231 | 0.1537 ± 0.0457 | 0.1875 ± 0.0224 | 3.4659 ± 0.0786 |
| gated | 3 | 3012 | 0.0083 ± 0.0010 | 0.0670 ± 0.0078 | 0.0657 ± 0.0202 | 0.1654 ± 0.0373 | 0.1916 ± 0.0225 | 4.1834 ± 0.0168 |
| low_rank | 3 | 3224 | 0.0091 ± 0.0017 | 0.0654 ± 0.0202 | 0.0596 ± 0.0185 | 0.1596 ± 0.0436 | 0.1666 ± 0.0011 | 4.6006 ± 0.0204 |
| separate | 3 | 2812 | 0.0046 ± 0.0002 | 0.0950 ± 0.0192 | 0.0703 ± 0.0019 | 0.2472 ± 0.0735 | 0.2046 ± 0.0058 | 5.5495 ± 0.0398 |

Perturbation gap is relative to an unperturbed model rollout, not a proof of return to the correct world trajectory. Separate cores share sensory initialization/readout and have their total parameter count matched to additive. Gated and low-rank variants retain additional parameters. See per-seed metrics for persistence references, invalid rates, prefix errors, and data exposure.

