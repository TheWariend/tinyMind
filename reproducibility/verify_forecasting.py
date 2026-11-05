"""Verify the arithmetic and integrity of public forecasting aggregates."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT/'benchmarks'/name).open() as f:return list(csv.DictReader(f))


def main():
    spec=json.loads((ROOT/'benchmarks/forecasting-provenance.json').read_text())
    assert spec['audit']['retained_audit_passed'] is True
    assert spec['evaluation']['official_leaderboard_rank'] is None
    assert spec['evaluation']['published_players_rerun'] is False
    assert spec['evaluation']['training_seeds']==1
    sources={s['id'] for s in spec['sources']};count=0
    for item in spec['exports']:
        path=(ROOT/item['file']).resolve()
        assert path.is_relative_to(ROOT)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        with path.open() as f:rows=list(csv.DictReader(f))
        assert len(rows)==item['data_rows']
        assert all(r['source_id'] in sources for r in rows)
        count+=len(rows)
    data=read('forecasting-pilot.csv')
    methods={'Frozen rolling forecaster','Fixed RLS','Fixed initial policy','Experience-adapted forecaster','Fixed NLMS'}
    tasks={r['task'] for r in data}
    assert len(data)==60 and len(tasks)==12 and {r['method'] for r in data}==methods
    indexed={(r['task'],r['method']):r for r in data};assert len(indexed)==60
    for method in methods:assert sum(int(r['origins']) for r in data if r['method']==method)==13952
    for r in data:
        assert math.isfinite(float(r['RMSE'])) and float(r['RMSE'])>0
        assert math.isfinite(float(r['diagnostic_NMSE'])) and float(r['diagnostic_NMSE'])>=0
        assert int(r['horizon'])>0
    refs=read('forecasting-reference-rmse.csv');reference={(r['task'],r['reference']):r for r in refs}
    assert len(reference)==len(refs)==84
    for r in refs:
        assert r['task'] in tasks and math.isfinite(float(r['RMSE'])) and float(r['RMSE'])>0
        if r['source_id']=='forecast-published-reference':
            assert r['published_source_url'].startswith('https://raw.githubusercontent.com/SalesforceAIResearch/gift-eval/')
    comparisons=read('forecasting-comparisons.csv');assert len(comparisons)==11
    assert len({r['reference'] for r in comparisons})==11
    for r in comparisons:
        label=r['reference'];ratios=[]
        for task in sorted(tasks):
            mine=float(indexed[(task,'Experience-adapted forecaster')]['RMSE'])
            other=indexed[(task,label)] if label in methods else reference[(task,label)]
            ratios.append(mine/float(other['RMSE']))
        gap=100*(math.exp(sum(math.log(x) for x in ratios)/len(ratios))-1)
        assert math.isclose(gap,float(r['geometric_RMSE_gap_percent']),rel_tol=1e-10,abs_tol=1e-9)
        assert int(r['wins'])==sum(x<1-1e-8 for x in ratios)
        assert int(r['losses'])==sum(x>1+1e-8 for x in ratios)
        assert int(r['ties'])==sum(abs(x-1)<=1e-8 for x in ratios)
        assert r['status']=='descriptive_one_seed_no_CI' and int(r['configurations'])==12
    own={r['reference']:r for r in comparisons}
    assert round(float(own['Frozen rolling forecaster']['geometric_RMSE_gap_percent']),2)==-7.33
    assert (int(own['Frozen rolling forecaster']['wins']),int(own['Frozen rolling forecaster']['losses']))==(12,0)
    assert round(float(own['Fixed RLS']['geometric_RMSE_gap_percent']),2)==-.20
    assert (int(own['Toto Open Base 1.0']['wins']),int(own['Toto Open Base 1.0']['losses']))==(3,9)
    synthetic=read('forecasting-synthetic.csv');retention=read('forecasting-retention.csv')
    assert len(synthetic)==10 and len(retention)==20
    assert {r['condition'] for r in synthetic}=={'unseen_instances','unseen_relationship_variants'}
    for r in synthetic:
        assert r['method'] in methods
        for k in ('mean_query_NMSE','observed_MSE_before','observed_MSE_after'):
            assert math.isfinite(float(r[k])) and float(r[k])>=0
        if r['method']!='Frozen rolling forecaster':assert int(r['wins'])+int(r['losses'])==128
    for r in retention:
        assert r['method'] in methods and r['sequence'] in ('AAA','ABA') and int(r['streams'])>0
        for k in ('geometric_old_relationship_RMSE_change_percent','old_query_MSE_after_A','old_query_MSE_after_B','old_query_MSE_after_return_A'):
            assert math.isfinite(float(r[k]))
    timing=read('forecasting-timing.csv');assert len(timing)==1
    t=timing[0]
    computed=100*(float(t['memory_write_seconds'])+float(t['memory_read_seconds']))/float(t['shared_rolling_forward_seconds'])
    assert math.isclose(computed,float(t['incremental_memory_overhead_percent']),abs_tol=1e-12)
    assert round(computed,2)==3.09
    print(f'Forecasting PASS: {len(spec["exports"])} hashes, {count} aggregate rows, 11 geometric comparisons, 12 configurations, 13,952 origins/method.')
    print('Scope: aggregate arithmetic and integrity; synthetic/retention summaries bind to retained audits, not replayed predictions.')


if __name__=='__main__':main()
