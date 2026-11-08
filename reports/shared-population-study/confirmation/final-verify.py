import time
started_cpu,started_wall=time.process_time(),time.perf_counter()
import json,hashlib,resource
from pathlib import Path
from soam.shared.continuation import current_calibration,audit_development
root=Path.cwd(); p=root/'reports/shared-population-study/confirmation'
cal,_,_=current_calibration(root/'runs/e1-continuation-calibration-v1')
dev=audit_development()
assert cal['source_sha256']=='b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9'
verified=[]
for folder in [root/'reports/shared-population-study/development',root/'reports/shared-population-study/continuation']:
 for name,expected in json.loads((folder/'sha256.json').read_text()).items():
  assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==expected,name
  verified.append(str((folder/name).relative_to(root)))
raw=root/'runs/e1-confirmation-v1-a1'
for name in ['config.json','provenance.json','inventory.json','reproduction.json','result.json','status.json']:
 assert (p/name).read_bytes()==(raw/name).read_bytes()
assert (root/'runs/e1-confirmation-readiness-v1/execution-claim.json').is_file()
s=json.loads((p/'statistics.json').read_text())
assert all(s['model_statistics'][f]['free8_nmse']['root_values'][i] < s['model_statistics']['S32']['free8_nmse']['root_values'][i] for f in ['G28','G32'] for i in range(10))
assert min(s['model_statistics'][f]['free8_nmse']['root_values'][i] for f in ['D25','D16','G28','G32','L12'] for i in range(10))>1e-6
# Explicitly check source changes did not leak into a reporting-only continuation.
assert json.loads((raw/'provenance.json').read_text())['source_files']==cal['source_files']
ledger=json.loads((p/'report-ledger.json').read_text())
verification_cpu=time.process_time()-started_cpu; verification_wall=time.perf_counter()-started_wall
ledger.update(final_verification_cpu_seconds=verification_cpu,final_verification_wall_seconds=verification_wall,
 final_metadata_cpu_wall_reserve_seconds=2.0,
 incomplete_reporting_attempt_charge_seconds=221,
 measured_peak_rss_note='scientific runner and successful audit measured; two incomplete reporting-only attempts have no separate RSS capture')
ledger['cpu_seconds']+=verification_cpu+2.0;ledger['wall_seconds']+=verification_wall+2.0
ledger['overhead_cpu_seconds']=ledger['cpu_seconds']-ledger['development_cpu_seconds']-sum(ledger['phase_cpu_seconds'].values())
ledger['peak_rss_bytes']=max(ledger['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
assert ledger['cpu_seconds']<14400 and ledger['wall_seconds']<28800 and ledger['overhead_cpu_seconds']<1200
assert ledger['artifact_bytes']<8*1024**3 and ledger['peak_rss_bytes']<2*1024**3
(p/'final-ledger.json').write_text(json.dumps(ledger,indent=2,sort_keys=True)+'\n')
verification={'baseline_test_command':'uv run pytest','baseline_test_result':'190 passed in 14.45s',
 'final_checks':['uv run python scripts/check_tickets.py: 62 tickets and 2 GitHub templates pass',
 'uv run ruff check soam/shared/execution.py soam/shared/continuation.py soam/shared/study_summary.py tests/test_shared_continuation.py: pass',
 'uv run ruff format --check soam/shared/execution.py soam/shared/continuation.py soam/shared/study_summary.py tests/test_shared_continuation.py: 4 files already formatted',
 'git diff --check: pass'],
 'current_calibration_source_verified':True,'development_archive':dev['archive'],
 'prior_checksums_verified':verified,'source_sha256':cal['source_sha256'],
 'compact_raw_result_copies_exact':True,'receipt_consumed':True,
 'all_required_reference_roots_above_floor':True,'both_grus_lower_primary_error_on_all_ten_roots':True,
 'figure_visually_reviewed':True,
 'audit_tolerance_note':'Only reordering of report means uses absolute 1e-12; observed max 6.661338147750939e-16. Bootstrap, repeat, T32 and bank isolation remain exact.',
 'qwen_read_only_procedure_extraction_job':'e37dd66cffd04625866499fcf7a04eba',
 'no_scientific_source_changes':True,'no_gate_review_or_fork_selected':True,'no_publication':True}
(p/'verification.json').write_text(json.dumps(verification,indent=2,sort_keys=True)+'\n')
(p/'final-verify.py').write_bytes(Path(__file__).read_bytes())
(p/'audit-final-timing.json').write_bytes(Path('/tmp/soam051-audit-final-timing.json').read_bytes())
print(json.dumps({'source':cal['source_sha256'],'development':dev['archive'],'ledger':ledger},indent=2))
