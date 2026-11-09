"""Verify the public aggregate export and local links using Python's standard library."""
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

def read_csv(name):
    return list(csv.DictReader((ROOT/'benchmarks'/name).open()))

def verify_64k_evidence(manifest, results):
    exposures = read_csv('source-data/pretraining-64k-exposure.csv')
    assert {r['architecture'] for r in exposures} == {'Tiny', 'CC'} and len(exposures)==2
    for r in exposures:
        assert int(r['optimizer_steps'])==64000, 'Incomplete 64K endpoint'
        assert int(r['presentations_through_32000'])==32000*8
        assert int(r['additional_presentations'])==32000*64
        assert int(r['cumulative_presentations'])==2304000
        assert int(r['presentations_through_32000'])+int(r['additional_presentations'])==int(r['cumulative_presentations'])
        assert int(r['parameters'])==manifest['evaluation_identifiers']['pretraining_64k']['parameter_counts'][r['architecture']]
        assert int(r['seed'])==manifest['evaluation_identifiers']['pretraining_64k']['training_seed_by_architecture'][r['architecture']]

    effects=read_csv('source-data/pretraining-64k-effects.csv')
    curves=read_csv('source-data/pretraining-64k-curves.csv')
    assert len(effects)==12 and len(curves)==348, 'Missing current synthetic measurements'
    for r in effects:
        model='TinyMind' if r['architecture']=='Tiny' else 'TinyMind-CC'
        q=[x for x in results if x['study']=='pretraining_64k' and x['candidate']==model and x['benchmark']==r['track']]
        assert len(q)==1, 'Missing/duplicate synthetic comparison'
        for step, key in [(32000,'nmse_32000'),(64000,'nmse_64000')]:
            points=[x for x in curves if x['architecture']==r['architecture'] and x['track']==r['track'] and int(x['step'])==step]
            assert len(points)==1 and abs(float(points[0]['nmse'])-float(r[key]))<1e-12, 'Curve/endpoint mismatch'
        for k, key in [('candidate_value','nmse_64000'),('reference_value','nmse_32000'),
                       ('error_reduction_percent','gain_percent'),('ci95_low_percent','ci95_low'),('ci95_high_percent','ci95_high')]:
            assert abs(float(q[0][k])-float(r[key]))<1e-12, 'Synthetic export mismatch'

    real=read_csv('source-data/pretraining-64k-real.csv')
    assert len(real)==8, 'Missing current real-data point contrasts'
    for r in real:
        model='TinyMind' if r['architecture']=='Tiny' else 'TinyMind-CC'
        q=[x for x in results if x['study']=='pretraining_64k_real' and x['candidate']==model and x['benchmark']==r['track']]
        assert len(q)==1 and float(q[0]['candidate_value'])==float(r['nmse_64000']) and float(q[0]['reference_value'])==float(r['nmse_32000']), 'Real point export mismatch'
        assert abs(100*(1-float(r['nmse_64000'])/float(r['nmse_32000']))-float(r['gain_percent']))<1e-10

    tab=read_csv('source-data/tabarena-lite-64k.csv')
    common=[r for r in tab if r['TinyMind_status']==r['TinyMind-CC_status']=='ok']
    assert len(tab)==13 and len(common)==11 and len({r['task_id'] for r in tab})==13
    for r in tab:
        for model in ['TinyMind','TinyMind-CC']:
            if r[model+'_status']=='ok':
                assert int(r['original_D'])<=32 and float(r[model+'_RMSE'])>0
                for reference in ['TabPFN-3.5','CatBoost','XGBoost']:
                    assert float(r[model+'_RMSE'])>float(r[reference+'_RMSE']), 'Baseline win claim no longer holds'
                    q=[x for x in results if x['study']=='tabarena_lite_64k' and x['benchmark']==r['dataset'] and
                       x['candidate']==model and x['reference']==reference]
                    assert len(q)==1 and float(q[0]['candidate_value'])==float(r[model+'_RMSE']) and float(q[0]['reference_value'])==float(r[reference+'_RMSE']), 'Dataset export mismatch'
            else:
                assert int(r['original_D'])>32 and not r[model+'_RMSE'] and not r[model+'_NMSE'], 'Unsupported score was substituted'
    assert {r['dataset'] for r in tab if r['TinyMind_status']!='ok'}=={'QSAR-TID-11','superconductivity'}
    assert sum(float(r['TinyMind_RMSE'])<float(r['TinyMind-CC_RMSE']) for r in common)==8
    assert sum(float(r['TinyMind-CC_RMSE'])<float(r['TinyMind_RMSE']) for r in common)==3
    for r in read_csv('source-data/tabarena-lite-64k-summary.csv'):
        ratios=[float(x[r['candidate']+'_RMSE'])/float(x[r['reference']+'_RMSE']) for x in common]
        gm=math.exp(sum(math.log(x) for x in ratios)/len(ratios))
        assert int(r['common_datasets'])==len(ratios)
        assert abs(gm-float(r['geometric_mean_relative_RMSE']))<1e-12, 'Geometric mean mismatch'
        assert abs(100*(gm-1)-float(r['relative_RMSE_gap_percent']))<1e-10, 'Relative gap mismatch'
        assert int(r['candidate_wins'])==sum(x<1 for x in ratios) and int(r['reference_wins'])==sum(x>1 for x in ratios)
        assert int(r['ties'])==sum(x==1 for x in ratios)
        q=[x for x in results if x['study']=='tabarena_lite_64k_summary' and x['candidate']==r['candidate'] and x['reference']==r['reference']]
        assert len(q)==1 and abs(float(q[0]['candidate_value'])-gm)<1e-12, 'Summary export mismatch'

def verify_70k_evidence(manifest, results):
    data=read_csv('source-data/failure-driven-70k.csv')
    summaries=read_csv('source-data/failure-driven-70k-summary.csv')
    assert len(data)==6 and len({r['dataset'] for r in data})==6 and len(summaries)==8
    evidence=manifest['evaluation_identifiers']['failure_driven_70k']
    assert evidence['end_step']==70000 and evidence['datasets_evaluated']==6
    assert evidence['cumulative_task_presentations_per_model']==2304000+6000*64
    assert evidence['TabPFN_3_5_evaluated'] is False and evidence['official_leaderboard_rank'] is None
    selected={'TinyMind':64000,'TinyMind-CC':70000}
    assert evidence['selected_steps']==selected
    for r in data:
        assert 4<=int(r['original_features'])<=12
        assert 0<int(r['support_rows'])<=64 and int(r['full_training_rows'])>=int(r['support_rows'])
        assert int(r['test_rows'])>0
        assert int(r['TinyMind_selected_step'])==64000 and int(r['CC_selected_step'])==70000
        for key,value in r.items():
            if key.endswith('_RMSE'):
                assert math.isfinite(float(value)) and float(value)>0, 'Invalid 70K RMSE'
    for prefix,regression in [('TinyMind','carData::Davis'),('CC','agridat::gartner.corn')]:
        failed={r['dataset'] for r in data if float(r[prefix+'_70000_RMSE'])>float(r[prefix+'_64000_RMSE'])}
        assert failed=={regression}, 'Dataset regression claim changed'
    assert len([r for r in results if r['study']=='failure_driven_70k'])==48
    assert len([r for r in results if r['study']=='failure_driven_70k_summary'])==8
    for summary in summaries:
        candidate,reference=summary['candidate'],summary['reference']
        ratios=[float(r[candidate])/float(r[reference]) for r in data]
        gm=math.exp(sum(math.log(x) for x in ratios)/6)
        reduction=100*(1-gm)
        assert abs(gm-float(summary['geometric_mean_RMSE_ratio']))<1e-12
        assert abs(reduction-float(summary['RMSE_reduction_percent']))<1e-10
        assert int(summary['candidate_wins'])==sum(x<1 for x in ratios)
        assert int(summary['reference_wins'])==sum(x>1 for x in ratios)
        assert int(summary['ties'])==sum(x==1 for x in ratios)
        assert int(summary['dataset_count'])==6
        locator=f'{candidate}/{reference};regime={summary["regime"]}'
        q=[r for r in results if r['study']=='failure_driven_70k_summary' and r['source_locator']==locator]
        assert len(q)==1 and abs(float(q[0]['candidate_value'])-gm)<1e-12
        for row in data:
            locator=f'dataset={row["dataset"]};{candidate};{reference}'
            q=[r for r in results if r['study']=='failure_driven_70k' and r['source_locator']==locator]
            assert len(q)==1
            assert float(q[0]['candidate_value'])==float(row[candidate]) and float(q[0]['reference_value'])==float(row[reference])
    cc=next(r for r in summaries if r['candidate']=='CC_70000_RMSE' and r['reference']=='CC_64000_RMSE')
    assert f'{float(cc["RMSE_reduction_percent"]):.2f}'=='9.61' and int(cc['candidate_wins'])==5
    text=(ROOT/'docs/archive/tinymind-through-2026-11-05.md').read_text()
    assert '9.61% relative to its 64K reference' in text
    assert 'six failure-driven evaluation datasets, not TabArena-Lite' in text

def markdown_anchors(path):
    # GitHub heading slugs for the headings used in this documentation.
    anchors=set(); seen={}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',path.read_text(),re.M):
        slug=re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-')
        count=seen.get(slug,0); seen[slug]=count+1
        anchors.add(slug if count==0 else f'{slug}-{count}')
    return anchors

def main():
    manifest = json.loads((ROOT/'benchmarks/provenance.json').read_text())
    sources = {s['id']: s for s in manifest['sources']}
    checked_rows = 0
    for export in manifest['exports']:
        path = (ROOT/export['file']).resolve()
        assert path.is_relative_to(ROOT), 'Export escapes repository'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==export['sha256'], f'Hash mismatch: {export["file"]}'
        rows=list(csv.DictReader(path.open()))
        assert len(rows)==export['data_rows'], f'Row count mismatch: {export["file"]}'
        for row in rows:
            assert row['source_id'] in sources, 'Unknown source identifier'
            for key in ('reference_source_id','parameter_source_id','support_source_id'):
                if key in row: assert row[key] in sources, 'Unknown secondary source identifier'
        checked_rows += len(rows)

    results=list(csv.DictReader((ROOT/'benchmarks/public-results.csv').open()))
    ids=set(); maximum_error=0.0
    for r in results:
        assert r['result_id'] not in ids, 'Duplicate result ID'
        ids.add(r['result_id'])
        vals={k:float(r[k]) for k in ['candidate_value','reference_value','error_reduction_percent']}
        assert all(math.isfinite(v) for v in vals.values()), 'Nonfinite metric'
        assert vals['reference_value']>0 and vals['candidate_value']>=0, 'Invalid squared error'
        calculated=100*(1-vals['candidate_value']/vals['reference_value'])
        err=abs(calculated-vals['error_reduction_percent'])
        maximum_error=max(maximum_error,err)
        assert err<1e-8, f'Arithmetic mismatch: {r["result_id"]}'
        assert int(r['paired_units'])>0, 'Missing comparison units'
        if int(r['bootstrap_replicates'])==0:
            assert r['status']=='descriptive' and r['study'] in {
                'pretraining_64k_real','tabarena_lite_64k','tabarena_lite_64k_summary',
                'failure_driven_70k','failure_driven_70k_summary'}, 'Unexplained missing uncertainty'
            assert r['ci95_low_percent']==r['ci95_high_percent']=='', 'Invented descriptive interval'
        else:
            assert int(r['bootstrap_replicates'])>0, 'Invalid bootstrap count'
            lo,hi=float(r['ci95_low_percent']),float(r['ci95_high_percent'])
            assert math.isfinite(lo) and math.isfinite(hi) and lo<=hi, 'Invalid interval'
        assert r['source_locator'] and r['comparison'] and r['metric'] and r['split'], 'Missing provenance/conditions'

    verify_64k_evidence(manifest,results)
    verify_70k_evidence(manifest,results)
    from verify_forecasting import main as verify_forecasting
    verify_forecasting()
    from verify_current_research import main as verify_current_research
    verify_current_research()
    links=0
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
            parts=target.strip('<>').split('#',1)
            local=unquote(parts[0])
            linked=(path.parent/local).resolve() if local else path
            assert linked.is_relative_to(ROOT), f'Link escapes repository: {path.name}'
            assert linked.exists(), f'Broken local link in {path.name}: {target}'
            if len(parts)==2 and linked.suffix=='.md':
                assert unquote(parts[1]) in markdown_anchors(linked), f'Broken heading link in {path.name}: {target}'
            links+=1
    print(f'PASS: {len(manifest["exports"])} CSV hashes, {checked_rows} aggregate rows, '
          f'{len(results)} comparisons, {links} local links; maximum arithmetic difference {maximum_error:.3g}.')
    print('Scope: public aggregate arithmetic/integrity; no model inference, training or bootstrap regeneration.')
    print('Earlier 64K evidence: exposure, synthetic endpoints and TabArena coverage/ratios agree.')
    print('Latest 70K evidence: six-dataset endpoint and both ML baseline regimes agree; CC improvement 9.61%, separate from TabArena-Lite.')

if __name__=='__main__':
    try:
        main()
    except (AssertionError,ValueError,KeyError) as exc:
        print('FAIL:',exc,file=sys.stderr)
        sys.exit(1)
