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
        checked_rows += len(rows)

    results=list(csv.DictReader((ROOT/'benchmarks/public-results.csv').open()))
    ids=set(); maximum_error=0.0
    for r in results:
        assert r['result_id'] not in ids, 'Duplicate result ID'
        ids.add(r['result_id'])
        vals={k:float(r[k]) for k in ['candidate_value','reference_value',
                                     'error_reduction_percent','ci95_low_percent','ci95_high_percent']}
        assert all(math.isfinite(v) for v in vals.values()), 'Nonfinite metric'
        assert vals['reference_value']>0 and vals['candidate_value']>=0, 'Invalid squared error'
        calculated=100*(1-vals['candidate_value']/vals['reference_value'])
        err=abs(calculated-vals['error_reduction_percent'])
        maximum_error=max(maximum_error,err)
        assert err<1e-8, f'Arithmetic mismatch: {r["result_id"]}'
        assert vals['ci95_low_percent']<=vals['ci95_high_percent'], 'Reversed interval'
        assert int(r['paired_units'])>0 and int(r['bootstrap_replicates'])>0, 'Missing uncertainty conditions'
        assert r['source_locator'] and r['comparison'] and r['metric'] and r['split'], 'Missing provenance/conditions'

    links=0
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
            local=unquote(target.strip('<>').split('#')[0])
            if not local:continue
            linked=(path.parent/local).resolve()
            assert linked.is_relative_to(ROOT), f'Link escapes repository: {path.name}'
            assert linked.exists(), f'Broken local link in {path.name}: {target}'
            links+=1
    print(f'PASS: {len(manifest["exports"])} CSV hashes, {checked_rows} aggregate rows, '
          f'{len(results)} comparisons, {links} local links; maximum arithmetic difference {maximum_error:.3g}.')
    print('Scope: public aggregate arithmetic/integrity; no model inference, training or bootstrap regeneration.')

if __name__=='__main__':
    try:
        main()
    except (AssertionError,ValueError,KeyError) as exc:
        print('FAIL:',exc,file=sys.stderr)
        sys.exit(1)
