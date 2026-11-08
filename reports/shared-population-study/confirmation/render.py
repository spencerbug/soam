"""Render already computed E1 statistics; no fitting or new evaluation inputs."""
import json
import time
started_cpu, started_wall = time.process_time(), time.perf_counter()
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from soam.shared.models import manifest, ROOT

p=ROOT/'reports/shared-population-study/confirmation'
s=json.loads((p/'statistics.json').read_text())
a=json.loads((p/'audit.json').read_text())
r=json.loads((p/'result.json').read_text())
protocol=manifest(); families=[row['id'] for row in protocol['models']]
refs=protocol['comparisons']['required_references']
f=lambda x:f'{x:.6f}'
ci=lambda d:f"{f(d['mean'])} [{f(d['lower95'])}, {f(d['upper95'])}]"
lines=['## Model errors and resource differences','',
       'NMSE means and ordinary 95% paired-root bootstrap intervals. Episodes are averaged within root. T32 is an exact no-fit equality diagnostic and is excluded from superiority contrasts.','',
       '| Model | Parameters | Allocated / active neural units | Free-8 NMSE [95% CI] | Final recall NMSE [95% CI] | Free-32 NMSE [95% CI] | Grounded-32 NMSE [95% CI] |',
       '| --- | ---: | ---: | --- | --- | --- | --- |']
for family in [*families,'T32']:
    data=s['model_statistics']['S32' if family=='T32' else family]
    if family=='T32': params='3,868 tied'; available=64; active=32
    else:
        m=next(m for m in protocol['models'] if m['id']==family)
        params=f"{m['expected_trainable_scalars']:,}"; available=m['state_floats_including_role']-2; active=m['width_per_bank']
    lines.append(f"| {family} | {params} | {available} / {active} | "+' | '.join(ci(data[k]) for k in ('free8_nmse','recall_final','free32_nmse','grounded32_nmse'))+' |')
lines += ['', 'Two non-neural role flags are additional to every row. All fitted readouts are counted. T32 shares S32 parameter objects; its two state banks do not imply an unavoidable memory penalty over lazy single-role allocation. No exact simultaneous parameter/state/compute match is claimed.','',
          '## Primary benefit and recall guardrails','',
          'Positive relative gain favours S32. Required gain: mean ≥0.10, adjusted lower bound >0 and interval width ≤0.20 against **every** reference. Recall contrasts require adjusted upper bounds ≤0.005 NMSE. The seven contrasts share the frozen multiplicity adjustment.','',
          '| Contrast | Mean | Adjusted interval | Ordinary 95% interval | Adjusted width | Criterion |',
          '| --- | ---: | --- | --- | ---: | --- |']
u=s['utility']
for i,label in enumerate([f'S32 gain over {j}' for j in refs]+['S32 final − S32 recall-only','S32 final − D25 final recall']):
    if i<5:
        passes=u['mean'][i]>=.1 and u['lower'][i]>0 and u['width'][i]<=.2
        precise=u['upper'][i]<.1 and u['width'][i]<=.2
        verdict='Pass' if passes else 'Precise no practical benefit' if precise else 'Does not pass; precision/margin limits retained'
    else:
        verdict='Pass' if u['upper'][i]<=.005 else 'Recall degradation failure' if u['lower'][i]>.005 else 'Inconclusive guardrail'
    lines.append(f"| {label} | {f(u['mean'][i])} | [{f(u['lower'][i])}, {f(u['upper'][i])}] | [{f(u['ordinary_lower'][i])}, {f(u['ordinary_upper'][i])}] | {f(u['width'][i])} | {verdict} |")
lines += ['', '## Causal overlap and direction','',
          'The six contrasts share the separately frozen adjustment. Positive adjusted lower bounds are required. The four NMSE contrasts also require width ≤0.02; the two relative contrasts require width ≤0.20. A point estimate below its minimum alone is not a precise failure.','',
          '| Contrast | Practical minimum | Mean | Adjusted interval | Ordinary 95% interval | Width | Outcome |',
          '| --- | ---: | ---: | --- | --- | ---: | --- |']
c=s['causal']
labels=['Targeted full − intact recall','Targeted full − intact free-8','Full − readout-only recall','Full − readout-only free-8','Shifted-action relative free-8 increase','Zero-A relative free-8 increase']
for i,(label,minimum) in enumerate(zip(labels,[.005,.005,.002,.002,.1,.1])):
    verdict='Pass' if s['causal_pass'][i] else 'Precise failure' if s['causal_precise_failure'][i] else 'Unresolved'
    lines.append(f"| {label} | {minimum} | {f(c['mean'][i])} | [{f(c['lower'][i])}, {f(c['upper'][i])}] | [{f(c['ordinary_lower'][i])}, {f(c['ordinary_upper'][i])}] | {f(c['width'][i])} | {verdict} |")
lines += ['', '## All lesion and direction controls','',
          'Ordinary 95% paired-root intervals below are descriptive controls; they do not enlarge the preregistered test family. Random sets are reported individually; targeted lesions need not exceed random lesions.','',
          '| Condition | Error increase over intact [95% CI] |','| --- | --- |']
for name,d in s['absolute_diagnostic_effects'].items(): lines.append(f'| {name} | {ci(d)} |')
lines += ['', '| Transition control | Relative error increase over intact S32 [95% CI] |','| --- | --- |']
for name,d in s['relative_diagnostic_effects'].items(): lines.append(f'| {name} | {ci(d)} |')
lines += ['', 'SYM32 is independently fitted; zero-A removes asymmetry from the fitted S32 copy. Their effects answer different questions. All absolute diagnostic means, including targeted/readout/random lesions, D16 and T32 bank masks, zero cue and all recovery paths, appear in the linked machine-readable statistics.','',
          '## Cue dependence and finite-horizon recovery','',
          '| Recall path | Endpoint NMSE [95% CI] |','| --- | --- |']
for name in ('S32-recall_final','zero_cue','perturb','zero_S','zero_S_perturb'):
    lines.append(f"| {name} | {ci(s['diagnostic_statistics'][name]['recall_nmse'])} |")
lines += ['', '| Recovery criterion | Mean | Ordinary 95% interval | Frozen threshold |','| --- | ---: | --- | --- |']
thresholds={'halving_fraction':'≥0.90','halving_advantage':'≥0.20 over S=0', 'perturbed_recall_nmse':'≤0.02', 'false_recovery_fraction':'≤0.05 (recall error >0.05)', 'feature_variance_ratio':'[0.8, 1.2]'}
for key,threshold in thresholds.items():
    d=s['recovery']['intervals'][key]
    lines.append(f"| {key} | {f(d['mean'][0])} | [{f(d['lower'][0])}, {f(d['upper'][0])}] | {threshold} |")
lines += ['', f"Frozen recovery classification: **{s['recovery']['outcome']}**. Recovery is separate from the utility gate and is limited to ten-step trajectory recovery, not global attraction or Lyapunov stability.",'',
          '| Step | S32 hidden RMS distance ratio [95% CI] | S=0 ratio [95% CI] |', '| ---: | --- | --- |']
for i in range(10):
    lines.append(f"| {i+1} | {ci(s['recovery_curves']['distance_ratios_by_episode'][i])} | {ci(s['recovery_curves']['zero_S_distance_ratios_by_episode'][i])} |")
lines += ['', '## Root-level primary results and failures','',
          '| Root | S32 free-8 | D25 | D16 | G28 | G32 | L12 | SYM32 | S32 pre-recall | S32 final recall | Fits/cells failed |',
          '| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for i,root in enumerate(protocol['streams']['confirmation_roots']):
    errors=[s['model_statistics'][family]['free8_nmse']['root_values'][i] for family in families]
    pre=s['model_statistics']['S32']['recall_pre']['root_values'][i]
    final=s['model_statistics']['S32']['recall_final']['root_values'][i]
    lines.append(f'| {root} | '+' | '.join(f(v) for v in [*errors,pre,final])+' | 0 / 0 |')
(p/'tables.md').write_text('\n'.join(lines)+'\n')

plt.rcParams.update({'font.size':10, 'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,2,figsize=(12,4.4),gridspec_kw={'width_ratios':[1.3,1]})
for ax,idx,names,scale in [(axes[0],range(5),refs,100),(axes[1],range(5,7),['Final − recall-only','Final − D25'],1)]:
    for y,i in enumerate(idx):
        ax.hlines(y,u['lower'][i]*scale,u['upper'][i]*scale,color='#8798ad',lw=2)
        ax.hlines(y,u['ordinary_lower'][i]*scale,u['ordinary_upper'][i]*scale,color='#244a74',lw=5)
        ax.plot(u['mean'][i]*scale,y,'o',color='#102b46',ms=5)
    ax.set_yticks(range(len(names)),names); ax.invert_yaxis(); ax.axvline(0,color='#999999',lw=.8)
    ax.grid(axis='x',alpha=.2); ax.set_ylim(len(names)-.5,-.5)
axes[0].axvline(10,color='#3c7c65',ls='--',lw=1.2,label='10% practical benefit')
axes[0].set_xlabel('S32 relative error reduction (%)'); axes[0].set_title('Required comparisons')
axes[1].axvline(.005,color='#b1554d',ls='--',lw=1.2,label='0.005 guardrail')
axes[1].set_xlabel('Recall NMSE increase'); axes[1].set_title('Recall guardrails')
for ax in axes: ax.legend(loc='best',frameon=False,fontsize=9)
fig.suptitle('E1 confirmation: ten paired roots; frozen v1 + A1',fontweight='bold')
fig.text(.5,.01,'Thin intervals: adjusted seven-contrast family; thick intervals: ordinary 95%. Repeat is not an extra root.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.035,1,.95))
fig.savefig(p/'primary-and-guardrails.png',dpi=180)
fig.savefig(p/'primary-and-guardrails.svg')
plt.close(fig)
print(p/'tables.md')

ledger=json.loads((p/'audit-ledger.json').read_text())
render_cpu=time.process_time()-started_cpu; render_wall=time.perf_counter()-started_wall
ledger['render_cpu_seconds']=render_cpu; ledger['render_wall_seconds']=render_wall
ledger['cpu_seconds']+=render_cpu; ledger['wall_seconds']+=render_wall
ledger['overhead_cpu_seconds']=ledger['cpu_seconds']-ledger['development_cpu_seconds']-sum(ledger['phase_cpu_seconds'].values())
from soam.platform.runner import rss_bytes
ledger['peak_rss_bytes']=max(ledger['peak_rss_bytes'],rss_bytes())
assert ledger['cpu_seconds']<=14400 and ledger['wall_seconds']<=28800
assert ledger['overhead_cpu_seconds']<=1200 and ledger['peak_rss_bytes']<=2*1024**3
(p/'render.py').write_bytes(Path(__file__).read_bytes())
reserved_files=['tables.md','primary-and-guardrails.png','primary-and-guardrails.svg','render.py','audit-ledger.json']
assert sum((p/name).stat().st_size for name in reserved_files)<ledger['report_reserve_bytes']
(p/'report-ledger.json').write_text(json.dumps(ledger,indent=2,sort_keys=True)+'\n')
