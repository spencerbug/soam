# Study D paired results

All means average ten independent fitted roots.

| Model | D1 J | One-shot | D2 old error | Retention change | Old accuracy | Unknown accepted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NOWRITE | 0.988019 | 0.988019 | 1.026705 | +0.000000 | 0.046 | 0.000 |
| KV | 0.000601 | 0.001313 | 0.000165 | +0.000000 | 1.000 | 0.000 |
| REG | 0.000658 | 0.001364 | 0.055064 | +0.051113 | 0.871 | 0.321 |
| FAST | 0.001274 | 0.001380 | 1.486512 | +1.395732 | 0.060 | 0.905 |

| Model | Persistent bytes | Writable bytes | Recall mean µs | Write mean µs |
| --- | ---: | ---: | ---: | ---: |
| NOWRITE | 1048 | 8 | 17.61 | 23.52 |
| KV | 7448 | 6408 | 33.12 | 40.22 |
| REG | 4120 | 3080 | 58.82 | 29.44 |
| FAST | 4120 | 3080 | 34.69 | 37.44 |

Persistent bytes include shared core and scalar settings. KV preallocates 32 rows;
only eight are occupied in D2. No exact resource match is claimed. FAST and REG
have equal numerical persistent bytes. Recall times are serial cue-to-association
calls (three warmups, twenty samples/root); writes include validation and accounting.
Core action advances are identical. Profiling and scientific orchestration are charged.
Python/Torch object overhead is in process RSS, not tensor bytes.
