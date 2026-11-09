"""Render the current forecasting model's results and completed learning curve."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
BLUE = '#245edb'
TEAL = '#008b78'
ORANGE = '#c65a26'
INK = '#17263d'
MUTED = '#56667c'
GRID = '#e5eaf1'


def read(name):
    with (ROOT / 'benchmarks' / name).open() as f:
        return list(csv.DictReader(f))


def style(ax):
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, labelsize=10, colors=MUTED, pad=8)
    ax.set_axisbelow(True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-dir', type=Path, help='Optional directory for PNG previews')
    args = parser.parse_args()
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'path', 'svg.hashsalt': 'tinymind-forecasting',
                         'text.color': INK, 'axes.labelcolor': MUTED, 'font.size': 11})
    manifest_path = ROOT / 'benchmarks/current-research-provenance.json'
    manifest = json.loads(manifest_path.read_text())
    exports = {x['file']: x for x in manifest['exports']}
    for name in ['current-forecasting-pilot.csv', 'current-forecasting-comparisons.csv']:
        p = ROOT / 'benchmarks' / name
        assert hashlib.sha256(p.read_bytes()).hexdigest() == exports['benchmarks/' + name]['sha256']
    specifications = []

    def save(fig, name, sources, description):
        path = ROOT / 'figures' / (name + '.svg')
        fig.savefig(path, format='svg', metadata={'Date': None, 'Creator': 'TinyMind forecasting research'})
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
        if args.preview_dir:
            args.preview_dir.mkdir(parents=True, exist_ok=True)
            fig.savefig(args.preview_dir / (name + '.png'), dpi=160, facecolor='white')
        specifications.append({'file': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                               'source_files': ['benchmarks/' + s for s in sources], 'description': description})
        plt.close(fig)

    rows = read('current-forecasting-pilot.csv')
    indexed = {(r['config'], r['method']): float(r['RMSE']) for r in rows}
    configs = sorted({r['config'] for r in rows})
    values = [(c, 100 * (1 - indexed[c, 'mixed-1812-4000-adapted'] / indexed[c, 'seasonal-naive'])) for c in configs]
    values.sort(key=lambda x: x[1])
    labels = {'bitbrains_fast_storage/H/short': 'Bitbrains fast storage · hourly',
              'bitbrains_rnd/H/short': 'Bitbrains RND · hourly',
              'bizitobs_application/10S/short': 'BizIT application · 10 seconds',
              'bizitobs_service/10S/short': 'BizIT service · 10 seconds',
              'electricity/H/short': 'Electricity · hourly', 'ett1/15T/short': 'ETT1 · 15 minutes',
              'ett1/H/short': 'ETT1 · hourly', 'ett2/15T/short': 'ETT2 · 15 minutes',
              'ett2/H/short': 'ETT2 · hourly', 'jena_weather/10T/short': 'Jena weather · 10 minutes',
              'jena_weather/H/short': 'Jena weather · hourly', 'solar/H/short': 'Solar · hourly'}
    ratio = math.exp(sum(math.log(indexed[c, 'mixed-1812-4000-adapted'] / indexed[c, 'seasonal-naive']) for c in configs) / len(configs))
    assert f'{100 * (1 - ratio):.2f}' == '8.21'
    fig, ax = plt.subplots(figsize=(12, 7.6), facecolor='white')
    fig.subplots_adjust(left=.31, right=.94, bottom=.14, top=.76)
    style(ax)
    ax.grid(axis='x', color=GRID)
    ax.axvline(0, color='#8593a5', linewidth=1.2)
    ax.barh(range(len(values)), [v for _, v in values], height=.61,
            color=[BLUE if v > 0 else ORANGE for _, v in values])
    ax.set_yticks(range(len(values)), [labels[c] for c, _ in values])
    ax.set_xlim(min(v for _, v in values) - 10, max(v for _, v in values) + 10)
    for i, (_, value) in enumerate(values):
        ax.text(value + (1.5 if value > 0 else -1.5), i, f'{value:+.1f}%',
                ha='left' if value > 0 else 'right', va='center', fontsize=10, color=INK)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:g}%'))
    ax.set_xlabel('RMSE reduction versus seasonal naive · higher is better', labelpad=15)
    fig.text(.055, .94, 'Forecasts improve from experience', fontsize=24, weight='bold')
    fig.text(.055, .895, 'Current 4K core + learned experience · selected GIFT short-horizon pilot', fontsize=12, color=MUTED)
    fig.text(.055, .824, '8.21%', fontsize=30, color=BLUE, weight='bold')
    fig.text(.225, .83, 'lower geometric RMSE', fontsize=15, weight='bold')
    fig.text(.225, .797, '9 configuration wins · 3 regressions · 13,952 forecast origins', fontsize=11, color=MUTED)
    fig.text(.055, .035, 'Each configuration has equal weight in the geometric aggregate. All 12 configurations are shown.', fontsize=10, color=MUTED)
    save(fig, 'forecasting-current-results', ['current-forecasting-pilot.csv'],
         'Current experience-enabled 4K forecasting model; all 12 configuration RMSE reductions versus seasonal naive.')

    comparisons = read('current-forecasting-comparisons.csv')
    scores = {(r['suite'], r['candidate']): -float(r['RMSE_change_percent'])
              for r in comparisons if r['reference'] == 'seasonal-naive'}
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.7), facecolor='white')
    fig.subplots_adjust(left=.075, right=.965, top=.73, bottom=.25, wspace=.27)
    for ax, suite, title in zip(axes, ['five-source-validation', 'gift-short-pilot'],
                               ['Five-source real validation', '12-configuration forecasting pilot']):
        style(ax)
        ax.grid(axis='y', color=GRID)
        steps = [1000, 1500, 2000, 3000, 4000] if suite == 'five-source-validation' else [1000, 2000, 3000, 4000]
        core = [scores[suite, 'mixed-1812-' + str(step)] for step in steps]
        ax.plot([s / 1000 for s in steps], core, '-o', color=BLUE, linewidth=2.4, markersize=7, label='Forecasting core')
        experience = [scores[suite, 'mixed-1812-' + str(step) + '-adapted'] for step in [2000, 4000]]
        ax.scatter([2, 4], experience, marker='D', s=75, color=TEAL, zorder=4, label='Core + learned experience')
        ax.set_title(title, fontsize=14, weight='bold', pad=18)
        ax.set_xticks([1, 1.5, 2, 3, 4], ['1K', '1.5K', '2K', '3K', '4K'])
        ax.set_xlim(.8, 4.75)
        ax.set_xlabel('Completed core updates', labelpad=15)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:g}%'))
        if suite == 'five-source-validation':
            ax.set_ylim(30.5, 35.5)
            ax.set_ylabel('RMSE reduction versus naive · higher is better', labelpad=12)
            offsets = [(0, 10), (0, -22)]
        else:
            ax.set_ylim(-.5, 10.1)
            ax.axhline(0, color='#8593a5', linewidth=1)
            offsets = [(0, -21), (0, 11)]
        for value, offset, color in [(core[-1], offsets[0], BLUE), (experience[-1], offsets[1], TEAL)]:
            ax.annotate(f'{value:.2f}%', (4, value), xytext=offset, textcoords='offset points',
                        fontsize=11, color=color, weight='bold', ha='center')
    fig.text(.055, .935, 'Learning curve of the current model', fontsize=23, weight='bold')
    fig.text(.055, .882, 'One forecasting lineage · completed checkpoints · data seed 1812', fontsize=12, color=MUTED)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5, .1), ncol=2, frameon=False, fontsize=11)
    fig.text(.055, .065, 'Lines join measured core checkpoints; diamonds are separate experience-enabled evaluations.', fontsize=10, color=MUTED)
    fig.text(.055, .028, 'The 1.5K checkpoint has no pilot score. Shared neural weights are frozen during every evaluation.', fontsize=10, color=MUTED)
    save(fig, 'forecasting-learning-curves', ['current-forecasting-comparisons.csv'],
         'Current data-seed-1812 core curve at measured checkpoints; separate experience-enabled points at 2K and 4K.')
    manifest['figures'] = specifications
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print('Rendered two figures from the current forecasting model only.')


if __name__ == '__main__':
    main()
