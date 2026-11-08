"""Read-only audit/report extraction from completed frozen E1 artifacts. No fits."""
import csv
import hashlib
import io
import json
import time
audit_started_cpu, audit_started_wall = time.process_time(), time.perf_counter()
from pathlib import Path

import numpy as np
import torch

from soam.platform.core import fingerprint
from soam.platform.runner import read_arrays
from soam.shared.archive import InputStore, digest, identity
from soam.shared.continuation import ContinuationBudget, DEVELOPMENT, tree_identity
from soam.shared.data import initialization_seed, stream
from soam.shared.execution import FAMILIES, cell_inventory, same_outputs
from soam.shared.fitting import FitPlan, exposure_counts
from soam.shared.inference import paired_intervals
from soam.shared.models import ROOT, manifest
from soam.shared.runner import Config, restore_episodes
from soam.shared.study_summary import aggregate

torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)
p=ROOT/'runs/e1-confirmation-v1-a1'
out=ROOT/'reports/shared-population-study/confirmation'
status=json.loads((p/'status.json').read_text())
assert status['status']=='complete',status
result=json.loads((p/'result.json').read_text())
assert result['reproduction']['exact_repeat']
receipt=json.loads((ROOT/'runs/e1-confirmation-readiness-v1/readiness.json').read_text())
carried={**{k:status[k] for k in ('cpu_seconds','wall_seconds','artifact_bytes','peak_rss_bytes')},
         'development_cpu_seconds':receipt['carried']['development_cpu_seconds']}
carried['cpu_seconds'] += time.process_time()-audit_started_cpu
carried['wall_seconds'] += time.perf_counter()-audit_started_wall
attempts=json.loads(Path('/tmp/soam051-audit-attempts.json').read_text())
carried['cpu_seconds']+=sum(v['cpu_seconds_upper_charge'] for v in attempts)
carried['wall_seconds']+=sum(v['wall_seconds_upper_charge'] for v in attempts)
budget=ContinuationBudget(carried)
budget.phases=dict(status['phase_cpu_seconds'])
# Charge compact evidence in addition to run-owned archives, conservatively.
compact_roots=[ROOT/'reports/shared-population-study',ROOT/'reports/shared-population-harness',ROOT/'reports/e1-archive-a1']
budget.sizes['existing-compact-evidence']=sum(f.stat().st_size for folder in compact_roots for f in folder.rglob('*') if f.is_file())
budget.sizes['final-report-reserve']=2*1024**2
budget.check()
out.mkdir(parents=True,exist_ok=True)
assert not list(out.iterdir()), "Audit destination must be empty"
read=lambda f:json.loads(f.read_text())
protocol=manifest(); roots=protocol['streams']['confirmation_roots']
configs=receipt['development']['screen']['selected_configs']
resolved_config=read(p/'config.json'); captured=read(p/'provenance.json')
assert resolved_config['fixture'] is False and resolved_config['selected_configs']==configs
capture_hash=hashlib.sha256(json.dumps(Config(archive_revision='a1').to_dict(),sort_keys=True).encode()).hexdigest()
assert captured['config_sha256']==capture_hash
resolved_hash=hashlib.sha256(json.dumps(resolved_config,sort_keys=True).encode()).hexdigest()
normalization=read_arrays(p/'normalization.npz')
assert fingerprint(normalization)==fingerprint(read_arrays(DEVELOPMENT/'normalization.npz'))
variance=float(normalization['variance'])
store=InputStore(p/'input-objects')
objects={}
stream_origins={}
for obj in sorted(store.root.iterdir()):
    budget.check()
    store.verify(obj.name)
    assert identity(restore_episodes(obj))==obj.name,obj.name
    objects[obj.name]=digest(obj/'manifest.json')
    metadata=read(obj/'streams.json')
    keys=[list(packet.values())[0]['key'] for packet in metadata]
    first=keys[0]
    assert all(key[:4]==first[:4] and key[4]==first[4]+i and key[5]==first[5] for i,key in enumerate(keys))
    for packet in metadata:
      for component_name,value in packet.items():
        key=value['key']; assert key[-1].endswith('/'+component_name)
        assert value['seed']==stream(key[2],key[3],key[4],key[5])
    stream_origins[obj.name]=(first[2],first[3],first[4],first[5].rsplit('/',1)[0],len(metadata))
refs=list(p.rglob('input-ref.json'))
for ref in refs:
    budget.check()
    r=read(ref); assert objects[r['object']]==r['manifest_sha256'],str(ref)
    parts=ref.relative_to(p).parts; root=int(parts[1]); section=parts[2]
    if section=='fits':
        update,role=parts[5].split('-'); expected=('train',root,int(update)*16,role,16)
    elif section in ('selection-data','evaluation-data'):
        role,index=parts[3].rsplit('-',1)
        expected=(('development_diagnostic',401,int(index),'lesion-selection/'+role,1)
                  if section=='selection-data' else ('confirmation',root,int(index),role,1))
    else:
        assert section=='cells'
        name=parts[3]; index=int(name.rsplit('-',1)[1])
        if name.startswith('selection-'):
            expected=('development_diagnostic',401,index,'lesion-selection/'+name.split('-')[1],1)
        else:
            role='transition' if 'transition' in name or name.startswith(('action_shift-','zero_A-')) else 'recall'
            expected=('confirmation',root,index,role,1)
    assert stream_origins[r['object']]==expected,(ref,stream_origins[r['object']],expected)

all_fits=[]; root_summaries={}; cells_total=0; numerical_arrays=0; expected_exposure=exposure_counts(FitPlan())
isolation={k:{'episode_pairs':0,'prediction_arrays':0,'max_abs_difference':0.0} for k in ('T32_intact','T32_opposite_bank','D16_opposite_bank')}
fit_work={}; selected=[]; distinct_failures=[]; max_regrouping_difference=0.0
raw_models={family:[] for family in FAMILIES}
raw_diagnostics={}; numerical_hashes={}
for phase, seeds in [('confirmation',roots),('repeat',[11])]:
 for seed in seeds:
    budget.check()
    root=p/phase/str(seed)
    rr=read(root/'result.json'); inv=read(root/'inventory.json')
    assert rr['fits']==inv['fits'] and rr['cells']==inv['cells']
    assert set(rr['cells'])==set(cell_inventory()),(phase,seed)
    assert all(v['status']=='complete' for v in rr['cells'].values())
    assert all(v['status']=='complete' for v in rr['fits'].values())
    summary=read(root/'summary.json'); assert summary['complete']
    if phase=='confirmation': root_summaries[seed]=summary
    selection=read(root/'selection.json'); assert selection==rr['selection'] and selection['status']=='complete'
    assert selection['selection_split']=='development_diagnostic'
    assert (root/'selection.json').stat().st_mtime_ns <= min(f.stat().st_mtime_ns for f in (root/'evaluation-data').glob('*/input-ref.json'))
    selected.append({'phase':phase,'root':seed,'targeted':selection['targeted'],'random':selection['random'],'random_seed':selection['random_seed']})
    for family in FAMILIES:
        f=root/'fits'/family; rec=read(f/'fit.json')
        assert rec['initialization_seed']==initialization_seed('train',seed,family,configs[family])
        assert not rec['fixture_only'] and rec['exposure']==expected_exposure and len(rec['trace'])==400
        assert rec['cpu_seconds']<=90
        if family=='L12':
            assert rec['trace'][99]['L_records']==1600 and rec['trace'][-1]['L_records']==6400 and rec['trace'][-1]['B_pairs']==38400
        assert len(list((f/'data').glob('*/input-ref.json')))==700
        if family!='L12':
            for stage in ('recall','final'):
                groups=read(f/f'{stage}-optimizer.json')
                assert all(g['lr']==.003 and g['betas']==[.9,.999] and g['eps']==1e-8 and g['weight_decay']==0 for g in groups)
        for stage in ('recall','final'):
            a=read_arrays(f/f'{stage}.npz')
            assert all(torch.isfinite(v).all() for v in a.values())
        for name in f.glob('*.npz'):
            a=read_arrays(name); numerical_arrays+=len(a)
            assert all(torch.isfinite(v).all() for v in a.values())
            numerical_hashes[str(name.relative_to(p))]=fingerprint(a)
        all_fits.append({'phase':phase,'root':seed,'family':family,'config':configs[family],
                        'cpu_seconds':rec['cpu_seconds'],'initialization_seed':rec['initialization_seed'],
                        'exposure':rec['exposure'],'algorithm':rec['algorithm'], 'adam_updates':0 if family=='L12' else 400, 'ridge_solves':3 if family=='L12' else 0})
        if phase=='confirmation':
            m=summary['condition_means']
            raw_models[family].append({'root':seed, 'recall_pre':m[f'{family}-recall_pre']['recall_nmse'],
                'recall_final':m[f'{family}-recall_final']['recall_nmse'],
                **{k:m[f'{family}-transition'][k] for k in ['free8_nmse','free32_nmse','grounded32_nmse']}})
    metrics_by_condition={}; work=0
    for name, row in rr['cells'].items():
        budget.check()
        cell=root/'cells'/name; rec=read(cell/'record.json'); a=read_arrays(cell/'arrays.npz')
        assert rec['metrics']==row['metrics']
        assert fingerprint(a)==row['arrays_sha256']
        assert all(torch.isfinite(v).all() for v in a.values())
        numerical_arrays+=len(a)
        numerical_hashes[str((cell/'arrays.npz').relative_to(p))]=row['arrays_sha256']
        metrics_by_condition.setdefault(name.rsplit('-',1)[0],[]).append(rec['metrics'])
        assert rec['exposure']['fitting_updates']==0 and rec['exposure']['free_future_observation_reads']==0
        work+=rec['work']['linear_macs']
        # Verify stored metric reductions against frozen targets for all base cells.
        if any(name.startswith(f'{family}-') for family in FAMILIES):
            episode=store.restore(cell/'inputs')[0]
            targets=episode.targets.features[1:].double()
            per=(a['free_features'].double()-targets).square().mean((1,2))/variance
            assert per.tolist()==rec['metrics']['per_step_free_nmse']
            if rec['role']=='transition':
                assert per[:8].mean().item()==rec['metrics']['free8_nmse']
                g=(a['grounded_features'].double()-targets).square().mean((1,2))/variance
                assert g.mean().item()==rec['metrics']['grounded32_nmse']
            else:
                assert per[-1].item()==rec['metrics']['recall_nmse']
        cells_total+=1
    for condition, values in metrics_by_condition.items():
        for key in values[0]:
            actual=np.mean([v[key] for v in values],axis=0).tolist()
            expected=summary['condition_means'][condition][key]
            delta=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
            max_regrouping_difference=max(max_regrouping_difference,delta)
            assert np.allclose(actual,expected,rtol=0,atol=1e-12),(condition,key,delta)
    fit_work[f'{phase}/{seed}']={'evaluation_linear_macs':work}
    for role in ('recall','transition'):
      for index in range(20):
        suffix='recall_final' if role=='recall' else 'transition'
        s=read_arrays(root/'cells'/f'S32-{suffix}-{index}'/'arrays.npz')
        t=read_arrays(root/'cells'/f'T32-intact-{role}-{index}'/'arrays.npz')
        d=read_arrays(root/'cells'/f'D16-{suffix}-{index}'/'arrays.npz')
        opposite=1 if role=='recall' else 0
        tm=read_arrays(root/'cells'/f'T32-bank-{opposite}-{role}-{index}'/'arrays.npz')
        dm=read_arrays(root/'cells'/f'D16-bank-{opposite}-{role}-{index}'/'arrays.npz')
        for label,a,b in [('T32_intact',s,t),('T32_opposite_bank',t,tm),('D16_opposite_bank',d,dm)]:
            same_outputs(a,b)
            isolation[label]['episode_pairs']+=1
            isolation[label]['prediction_arrays']+=1+(role=='transition')
    if phase=='confirmation':
        raw_diagnostics[seed]=summary['condition_means']

assert len(all_fits)==77 and cells_total==25300
assert not list(p.rglob('failure.json'))
recomputed=aggregate(root_summaries)
for key in recomputed:
    stored=result[key]
    if key=='root_summaries': stored={int(k):v for k,v in stored.items()}
    assert recomputed[key]==stored,key
# Independently reconstruct fixed bootstrap indices and all primary/causal bounds.
from soam.shared.data import stream
rng=np.random.Generator(np.random.PCG64(stream('inference',8675309,0,'inference-resampling')))
indices=rng.integers(0,10,size=(10000,10))
for key,n in [('utility',7),('causal',6)]:
    values=np.array(result[key+'_root_contrasts']); samples=values[indices].mean(1)
    interval=np.quantile(samples,[.05/(2*n),1-.05/(2*n)],axis=0,method='linear')
    assert np.array_equal(interval[0],result[key]['lower']) and np.array_equal(interval[1],result[key]['upper'])

def interval(values):
    v=np.array(values,dtype=float); d=paired_intervals(v.reshape(10,1),family_size=1)
    return {'mean':d['mean'][0],'lower95':d['lower'][0],'upper95':d['upper'][0],
            'sd_across_roots':float(v.std(ddof=1)), 'root_values':v.tolist()}
model_stats={f:{k:interval([r[k] for r in rows]) for k in rows[0] if k!='root'} for f,rows in raw_models.items()}
diag_stats={}
# Include every scalar diagnostic and base result, all roots. Selection scores remain archived.
for condition, metrics in raw_diagnostics[roots[0]].items():
    if condition.startswith('selection-'): continue
    diag_stats[condition]={k:interval([raw_diagnostics[seed][condition][k] for seed in roots])
                           for k,v in metrics.items() if isinstance(v,(float,int))}
relative_effects={}; absolute_effects={}
for role,metric,base in [('recall','recall_nmse','S32-recall_final'),('transition','free8_nmse','S32-transition')]:
    for mode in ['targeted','readout',*[f'random-{i}' for i in range(4)]]:
        absolute_effects[f'{mode}-{role}']=interval([raw_diagnostics[s][f'{mode}-{role}'][metric]-raw_diagnostics[s][base][metric] for s in roots])
for role,metric in [('recall','recall_nmse'),('transition','free8_nmse')]:
    for bank in (0,1):
        base='D16-recall_final' if role=='recall' else 'D16-transition'
        absolute_effects[f'D16-bank-{bank}-{role}']=interval([raw_diagnostics[s][f'D16-bank-{bank}-{role}'][metric]-raw_diagnostics[s][base][metric] for s in roots])
        absolute_effects[f'T32-bank-{bank}-{role}']=interval([raw_diagnostics[s][f'T32-bank-{bank}-{role}'][metric]-raw_diagnostics[s][f'T32-intact-{role}'][metric] for s in roots])
for mode in ('SYM32-transition','action_shift','zero_A'):
    relative_effects[mode]=interval([(raw_diagnostics[s][mode]['free8_nmse']-raw_diagnostics[s]['S32-transition']['free8_nmse'])/max(raw_diagnostics[s]['S32-transition']['free8_nmse'],1e-6) for s in roots])
recovery_curves={}
for key in ('distance_ratios_by_episode','zero_S_distance_ratios_by_episode'):
    per_root=np.array([root_summaries[s]['recovery'][key] for s in roots]).mean(1)
    recovery_curves[key]=[interval(per_root[:,t]) for t in range(10)]

# Exact repeat revalidated directly, not merely a status flag.
from soam.shared.execution import compare_repeat
repeat=compare_repeat(p/'confirmation/11',p/'repeat/11',store,budget.check)
assert repeat==read(p/'reproduction.json')
archive_identity=tree_identity(p)
new_bytes=archive_identity['bytes']
# status is sampled before its final rewrite; reconcile exact physical writes.
counted_new=budget.sizes['carried-artifacts']-(receipt['carried']['artifact_bytes']+tree_identity(ROOT/'runs/e1-confirmation-readiness-v1')['bytes']+65536)
physical_delta=max(0,new_bytes-counted_new)
budget.sizes['physical-status-and-claim-reconciliation']=physical_delta

audit={'completed_confirmation_fits':70,'completed_repeat_fits':7,'completed_cells':cells_total,
       'full_study_fits':119,'full_study_cells':27820,'failed_fits':0,'failed_cells':0,'retries':0,
       'unique_input_objects':len(objects),'input_references':len(refs),'finite_numerical_arrays_checked':numerical_arrays,
       'raw_archive':archive_identity,'isolation':isolation,'reproduction':repeat,
       'capture_wrapper_config_sha256':capture_hash,'resolved_study_config_sha256':resolved_hash,'resolved_config_file_sha256':digest(p/'config.json'),
       'config_hash_note':'raw provenance config_sha256 hashes the capture wrapper; actual scientific config is separately archived and audited',
       'source_commit':read(p/'provenance.json')['commit'],'source_sha256':read(p/'provenance.json')['source_sha256'],
       'protocol_sha256':read(p/'provenance.json')['protocol_sha256'],'manifest_sha256':read(p/'provenance.json')['manifest_sha256'],
       'normalization_variance':variance,'metric_reductions_verified':True,'root_aggregation_verified':True,
       'bootstrap_intervals_verified':True,'max_root_mean_regrouping_difference':max_regrouping_difference,'all_reference_stream_boundaries_verified':True,'selection_freeze_precedes_confirmation_references':True,'selection_records':selected,'evaluation_work':fit_work,
       'representative_resources':{family:read(p/'confirmation/11/cells'/f'{family}-recall_final-0'/'record.json')['resources'] for family in [*FAMILIES,'T32'] if family != 'T32'},
       'fit_cpu_sum':sum(r['cpu_seconds'] for r in all_fits),'fit_cpu_max':max(r['cpu_seconds'] for r in all_fits)}
statistics={'outcome':result['outcome'],'model_statistics':model_stats,'diagnostic_statistics':diag_stats,
            'absolute_diagnostic_effects':absolute_effects,'relative_diagnostic_effects':relative_effects,
            'recovery_curves':recovery_curves,'utility':result['utility'],'causal':result['causal'],
            'recovery':result['recovery'],'utility_pass':result['utility_pass'],'guardrail_pass':result['guardrail_pass'],
            'causal_pass':result['causal_pass'],'causal_precise_failure':result['causal_precise_failure']}
for name,value in [('audit-attempts.json',attempts),('audit.json',audit),('statistics.json',statistics),('fit-records.json',all_fits),
                   ('root-model-means.json',raw_models),('root-condition-means.json',raw_diagnostics),
                   ('numerical-sha256.json',numerical_hashes)]: budget.json(out/name,value)
for name in ('config.json','provenance.json','inventory.json','reproduction.json','result.json','status.json'):
    budget.write(out/name,(p/name).read_bytes())
budget.write(out/'analysis.py',Path(__file__).read_bytes())
# Final ledger includes this audit and the conservative reserved report/plot bytes.
budget.check()
ledger={'phase_cpu_seconds':status['phase_cpu_seconds'],'development_cpu_seconds':carried['development_cpu_seconds'],
        'audit_cpu_seconds':budget.measurements()['cpu_seconds']-status['cpu_seconds'],
        'audit_wall_seconds':budget.measurements()['wall_seconds']-status['wall_seconds'],
        'report_reserve_bytes':2*1024**2, 'preexisting_compact_bytes':budget.sizes['existing-compact-evidence'],
        'physical_reconciliation_bytes':physical_delta, 'accounting':'runner carry + existing compact evidence + new evidence + report reserve; no earlier allocation removed',
        **budget.measurements()}
budget.json(out/'audit-ledger.json',ledger)
print(json.dumps({'outcome':result['outcome'],'fits':77,'cells':cells_total,'audit':audit['raw_archive'],
                  'ledger':ledger,'reproduction':repeat},indent=2))
