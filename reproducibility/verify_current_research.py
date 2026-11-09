"""Check the 9 November configuration aggregates and reported comparisons."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / 'benchmarks' / name).open() as f:
        return list(csv.DictReader(f))


def close(a, b):
    assert math.isclose(float(a), float(b), rel_tol=1e-11, abs_tol=1e-10), 'Arithmetic mismatch'


def index(rows, unit):
    data = {(r[unit], r['method']): r for r in rows}
    assert len(data) == len(rows), 'Duplicate configuration/method'
    for r in rows:
        assert math.isfinite(float(r['RMSE'])) and float(r['RMSE']) > 0
        for key in ['NMSE', 'diagnostic_NMSE']:
            if r.get(key):
                assert math.isfinite(float(r[key])) and float(r[key]) >= 0
    return data


def check_comparison(row, data):
    units = sorted({unit for unit, method in data if method == row['candidate']})
    assert int(row['configurations']) == len(units)
    ratios = [float(data[unit, row['candidate']]['RMSE']) /
              float(data[unit, row['reference']]['RMSE']) for unit in units]
    geometric = math.exp(sum(math.log(x) for x in ratios) / len(ratios))
    close(row['geometric_RMSE_ratio'], geometric)
    close(row['RMSE_change_percent'], 100 * (geometric - 1))
    assert int(row['wins']) == sum(x < 1 for x in ratios)
    assert int(row['losses']) == sum(x > 1 for x in ratios)
    assert int(row['ties']) == sum(x == 1 for x in ratios)
    assert row['status'] == 'descriptive_no_CI'


def main():
    manifest = json.loads((ROOT / 'benchmarks/current-research-provenance.json').read_text())
    sources = {s['id'] for s in manifest['sources']}
    assert len(sources) == len(manifest['sources'])
    assert all(len(s['sha256']) == 64 for s in manifest['sources'])
    count = 0
    for item in manifest['exports']:
        path = (ROOT / item['file']).resolve()
        assert path.is_relative_to(ROOT)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
        with path.open() as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == item['data_rows']
        assert all(r['source_id'] in sources for r in rows)
        count += len(rows)

    pilot_rows = read('current-forecasting-pilot.csv')
    pilot = index(pilot_rows, 'config')
    assert len(pilot_rows) == 156
    methods = {r['method'] for r in pilot_rows}
    configs = {r['config'] for r in pilot_rows}
    assert len(methods) == 13 and len(configs) == 12
    for method in methods:
        rows = [r for r in pilot_rows if r['method'] == method]
        assert len(rows) == 12
        if method.startswith('published-'):
            assert all(r['origins'] == r['diagnostic_NMSE'] == '' for r in rows)
        else:
            assert sum(int(r['origins']) for r in rows) == 13952

    real_rows = read('current-forecasting-real-validation.csv')
    real = index(real_rows, 'config')
    assert len(real_rows) == 55 and len({r['method'] for r in real_rows}) == 11
    for method in {r['method'] for r in real_rows}:
        rows = [r for r in real_rows if r['method'] == method]
        assert len(rows) == 5 and sum(int(r['windows']) for r in rows) == 1720
    for r in real_rows:
        if r['SSE']:
            assert int(r['values']) > 0 and float(r['SSE']) >= 0
            close(float(r['RMSE']) ** 2, float(r['SSE']) / int(r['values']))

    comparisons = read('current-forecasting-comparisons.csv')
    assert len({(r['suite'], r['candidate'], r['reference']) for r in comparisons}) == len(comparisons)
    for r in comparisons:
        check_comparison(r, pilot if r['suite'] == 'gift-short-pilot' else real)
    selected = manifest['forecasting']['selected_state']
    assert selected == 'mixed-1812-4000'
    assert manifest['forecasting']['pilot_used_for_selection'] is False
    for state in ['mixed-1812-2000', 'mixed-1812-4000']:
        r = next(r for r in comparisons if r['suite'] == 'five-source-validation' and
                 r['candidate'] == state + '-adapted' and r['reference'] == state)
        assert float(r['RMSE_change_percent']) > 0 and int(r['losses']) == 3
    latest = next(r for r in comparisons if r['suite'] == 'gift-short-pilot' and
                  r['candidate'] == selected + '-adapted' and r['reference'] == 'seasonal-naive')
    assert f"{float(latest['RMSE_change_percent']):.2f}" == '-8.21'

    synthetic = read('current-synthetic-summary.csv')
    assert len(synthetic) == 12
    for r in synthetic:
        close(r['RMSE_change_percent'], 100 * (float(r['geometric_RMSE_ratio']) - 1))
        assert int(r['configurations']) == {'synthetic-pure': 280, 'synthetic-generator': 240,
                                            'synthetic-families': 144}[r['suite']]
        if r['wins']:
            assert sum(int(r[k]) for k in ['wins', 'losses', 'ties']) == int(r['configurations'])
        assert r['status'] == 'descriptive_no_CI'

    cc_rows = read('current-tabarena-results.csv')
    cc = index(cc_rows, 'dataset')
    assert len(cc_rows) == 208 and len({r['dataset'] for r in cc_rows}) == 13
    for r in cc_rows:
        assert int(r['training_rows']) > 0 and int(r['test_rows']) > 0
        assert int(r['original_features']) > 0 and r['NMSE']
        assert r['status'] == ('scored' if r['method'].startswith('CC-') else 'published_reference')
    summary = read('current-tabarena-summary.csv')
    assert len(summary) == 16
    for r in summary:
        check_comparison(r, cc)
        rows = [x for x in cc_rows if x['method'] == r['candidate']]
        close(r['macro_NMSE'], sum(float(x['NMSE']) for x in rows) / len(rows))
    latest_cc = next(r for r in summary if r['candidate'] == 'CC-150000' and r['reference'] == 'CC-133594')
    assert f"{float(latest_cc['RMSE_change_percent']):.3f}" == '0.714'
    for r in summary:
        if not r['reference'].startswith('CC-'):
            assert int(r['wins']) == 0 and int(r['losses']) == 13
    assert manifest['forecasting']['shared_optimizer_updates_during_evaluation'] == 0
    for figure in manifest.get('figures', []):
        path = (ROOT / figure['file']).resolve()
        assert path.is_relative_to(ROOT) and path.suffix == '.svg'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == figure['sha256']
        assert all(name.startswith('benchmarks/current-forecasting-') for name in figure['source_files'])
    print(f'PASS: current research; {len(manifest["exports"])} table hashes, {count} aggregate rows, '
          f'{len(comparisons)} forecasting comparisons and {len(summary)} tabular comparisons.')
    print('Scope: aggregate consistency; no model inference or bootstrap regeneration.')


if __name__ == '__main__':
    main()
