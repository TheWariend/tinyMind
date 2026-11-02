"""Render audited public aggregate tables; no model code, inference or training."""
from pathlib import Path
import argparse
import csv
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/source-data'
TEAL, BLUE, PURPLE, RED = '#087f8c', '#2854a1', '#7553a8', '#bb5344'
INK, MUTED = '#172b45', '#52657b'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 12,
    'axes.titleweight': 'bold', 'axes.labelcolor': INK, 'text.color': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.edgecolor': '#d2dae4',
    'axes.spines.top': False, 'axes.spines.right': False,
    'svg.fonttype': 'path', 'svg.hashsalt': 'tinymind-20261101',
    'savefig.facecolor': 'white', 'figure.facecolor': 'white',
})

def read(name, source_data=True):
    p = DATA / name if source_data else ROOT / 'benchmarks' / name
    return list(csv.DictReader(p.open()))

RESULTS = read('public-results.csv', False)
def pick(**conditions):
    return [r for r in RESULTS if all(r[k] == str(v) for k, v in conditions.items())]

def axes_style(ax):
    ax.grid(axis='y', color='#e5ebf2', linewidth=.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)

def finish(fig, name, title, subtitle, source, preview_dir, left=.09):
    fig.suptitle(title, x=.065, y=.98, ha='left', fontsize=18, fontweight='bold')
    fig.text(.065, .895, subtitle, fontsize=10, color=MUTED)
    fig.text(.065, .025, source, fontsize=8, color=MUTED)
    fig.subplots_adjust(top=.80, bottom=.20, left=left, right=.97, wspace=.34, hspace=.60)
    svg_path = ROOT / 'figures' / (name + '.svg')
    fig.savefig(svg_path,
                metadata={'Date': None, 'Creator': 'TinyMind public aggregate renderer'})
    svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
    if preview_dir:
        fig.savefig(preview_dir / (name + '.png'), dpi=150)
    plt.close(fig)

def effects(preview_dir):
    fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.4))
    labels = [('familiar_allK','Familiar\nall K'), ('familiar_laterK','Familiar\nK16–64'),
              ('excluded','Excluded\nprograms'), ('structure','New\nstructure'), ('unseen_D','Unseen\nD6/12/24')]
    for ax, cand, ref, color in zip(axs, ['Tiny_Global','CC_G'], ['Tiny_Basis_current','CC_R'], [TEAL,PURPLE]):
        for seed, shift, marker in [('1811',-.12,'o'),('1877',.12,'D')]:
            q = pick(study='plateau_repair',split='final',candidate=cand,reference=ref,seed=seed)
            for i, (key, _) in enumerate(labels):
                r = next(r for r in q if r['benchmark']==key)
                y,lo,hi = [float(r[k]) for k in ['error_reduction_percent','ci95_low_percent','ci95_high_percent']]
                ax.errorbar(i+shift,y,yerr=[[y-lo],[hi-y]],fmt=marker,color=color,
                            markerfacecolor=color if seed=='1811' else 'white',capsize=3,ms=6,
                            label=seed if i==0 else None)
        ax.axhline(0,color=MUTED,lw=1)
        ax.set_xticks(range(len(labels)),[x[1] for x in labels])
        ax.set_ylim(-1.8,7.0)
        ax.set_ylabel('Query NMSE reduction (%)')
        ax.set_title(cand+' vs '+ref, pad=12)
        ax.legend(title='Training seed',fontsize=9,frameon=False)
        axes_style(ax)
    finish(fig,'matched-effects','Familiar gains; broad transfer remains open',
           'Historical 1 November study • independent final bank • 8K endpoints • paired 95% intervals • higher is better',
           'Source: benchmarks/public-results.csv • plateau_repair / final • exact scope and controls in benchmarks/results.md',preview_dir)

def original_training(preview_dir):
    data=read('fresh-experience-curves.csv')
    fig,axs=plt.subplots(1,2,figsize=(12.8,5.4))
    for ax,arch,color in zip(axs,['Tiny','CC'],[TEAL,PURPLE]):
        for seed,style,marker in [('1811','-','o'),('1877','--','D')]:
            steps=[];values=[]
            for step in [1000,4000,8000]:
                vals=[float(r['nmse']) for r in data if r['label']==f'{arch}_B_{seed}_{step}' and r['track']=='familiar']
                assert len(vals)==5,(arch,seed,step)
                steps.append(step/1000);values.append(sum(vals)/len(vals))
            ax.plot(steps,values,style,color=color,marker=marker,label=seed,lw=2.2)
            reduction=100*(1-values[-1]/values[-2])
            ax.annotate(f'{seed}: {reduction:+.2f}% from 4K to 8K',xy=(8,values[-1]),
                        xytext=(4.5,values[0]-(.017 if seed=='1811' else .052)),fontsize=9,color=color)
        ax.axvspan(4,8,color='#edf2f7',zorder=0)
        ax.set_title('TinyMind' if arch=='Tiny' else 'ColumnContext',pad=12)
        ax.set_xticks([1,4,8]);ax.set_xlabel('Total pretraining steps (thousands)')
        ax.set_ylabel('Familiar query NMSE (lower is better)')
        ax.legend(title='Training seed',frameon=False);axes_style(ax)
    finish(fig,'original-pretraining','Early progress, then a 4K plateau',
           'Historical 4K–8K study • each point averages K4/8/16/32/64 • later original-architecture training progressed to 64K',
           'Source: source-data/fresh-experience-curves.csv • Tiny_B / CC_B • same study bank; no cross-bank curve joins',preview_dir)

def plateau_training(preview_dir):
    data=read('plateau-curves.csv')
    fig,axs=plt.subplots(2,2,figsize=(12.8,8.0))
    for row,arch in enumerate(['Tiny','CC']):
        native='Tiny_R' if arch=='Tiny' else 'CC_R'
        candidate='Tiny_Global' if arch=='Tiny' else 'CC_G'
        for col,seed in enumerate(['1811','1877']):
            ax=axs[row,col]
            for label,color in [(native,MUTED),(candidate,TEAL if arch=='Tiny' else PURPLE)]:
                q=sorted([r for r in data if r['label']==label and r['seed']==seed and r['track']=='familiar'],key=lambda r:int(r['step']))
                assert [int(r['step']) for r in q]==[4000,6000,8000]
                ax.plot([int(r['step'])/1000 for r in q],[float(r['NMSE']) for r in q],
                        color=color,marker='o',lw=2,label=label)
            ax.set_title(f'{arch} • seed {seed}',pad=8);ax.set_xticks([4,6,8])
            ax.set_ylabel('Familiar query NMSE');ax.set_xlabel('Total steps (thousands)')
            ax.legend(frameon=False,fontsize=9);axes_style(ax)
    finish(fig,'plateau-repair','The original-lineage repair did not pass its gates',
           'Historical 1 November repair • same final bank • independently zoomed axes • gated 10K/12K not run • no promotion',
           'Source: source-data/plateau-curves.csv • Tiny candidate includes mathematical correction; this is not an isolated history effect',preview_dir)

def causal(preview_dir):
    fig,ax=plt.subplots(figsize=(12.0,5.0))
    modes=[('history_off','New retrieval\ndisabled'),('freeze_hidden','Hidden updates\nfrozen'),
           ('history_wrong_labels','Historical pairings\ncorrupted')]
    for seed,shift,color in [('1811',-.16,TEAL),('1877',.16,BLUE)]:
        for i,(mode,_) in enumerate(modes):
            r=pick(study='plateau_causal',candidate='Tiny_Global:'+mode,seed=seed,K='4/8/16/32/64')[0]
            y=-float(r['error_reduction_percent']);lo=-float(r['ci95_high_percent']);hi=-float(r['ci95_low_percent'])
            ax.bar(i+shift,y,width=.30,color=color,label=seed if i==0 else None)
            ax.errorbar(i+shift,y,yerr=[[y-lo],[hi-y]],fmt='none',ecolor=INK,capsize=4,lw=1)
            ax.text(i+shift,hi+.7,f'{y:.2f}%',ha='center',fontsize=9)
    ax.set_xticks(range(len(modes)),[m[1] for m in modes]);ax.set_ylim(0,29)
    ax.set_ylabel('Increase in familiar query NMSE (%)');axes_style(ax)
    ax.legend(title='Training seed',frameon=False,loc='upper left')
    finish(fig,'causal-evidence','Historical evidence and hidden updates matter',
           'Historical Tiny_Global • frozen 8K weights • familiar development bank • paired 95% intervals • greater means more damage',
           'Source: benchmarks/public-results.csv • plateau_causal • interventions can disrupt co-adaptation; they do not prove arbitrary rule invention',preview_dir)

def efficiency(preview_dir):
    data=read('transformer-efficiency.csv'); lookup={r['label']:r for r in data}
    fig,axs=plt.subplots(1,3,figsize=(13.4,5.2))
    groups=[('forward_MAC','Inference MACs\n(trillion)',1e12),
            ('max_cache_bytes_per_task','Maximum task cache\n(MiB)',1024**2),
            ('total','Adapt + 64 queries\n(ms/task)',1)]
    for ax,(field,title,scale) in zip(axs,groups):
        for j,prefix,color in [(0,'Column_',TEAL),(1,'Standard_',PURPLE)]:
            for i,seed in enumerate(['1301','1337']):
                r=lookup[prefix+seed]
                val=(float(r['adaptation_ms_per_function_support_budget'])+float(r['prediction_ms_per_64queries'])) if field=='total' else float(r[field])/scale
                x=j+(i-.5)*.28
                ax.bar(x,val,width=.25,color=color,alpha=1 if i==0 else .62)
                ax.text(x,val*1.03,f'{val:.2f}',ha='center',fontsize=9)
        ax.set_xticks([0,1],['ColumnContext','Transformer']);ax.set_ylabel(title)
        ax.set_ylim(0,ax.get_ylim()[1]*1.12);axes_style(ax)
    finish(fig,'efficiency','Compressed context saves compute and cache',
           'Historical matched study • seeds 1301 / 1337 • Apple M4 CPU, two threads • Transformer wins nonlinear all-K accuracy',
           'Source: source-data/transformer-efficiency.csv • MACs cover the inference bank; timings amortized, cache excludes shared weights',preview_dir)

def real_world(preview_dir):
    data=read('beijing-accuracy.csv');methods=sorted({r['method'] for r in data})
    labels={'TinyMind_default11':'TinyMind default11','TinyMind_CC_1301':'CC 1301','TinyMind_CC_1337':'CC 1337',
            'Standard_1301':'Transformer 1301','Persistence':'Persistence','KNN_distance5':'KNN5'}
    # Require actual saved identifiers so a naming mismatch never silently removes a method.
    assert set(labels).issubset(methods),methods
    fig,axs=plt.subplots(1,2,figsize=(13.0,5.4))
    colors=[BLUE,TEAL,PURPLE,MUTED,RED,'#a68622']
    for (method,label),color in zip(labels.items(),colors):
        q=sorted([r for r in data if r['method']==method],key=lambda r:int(r['K']))
        axs[0].plot([int(r['K']) for r in q],[float(r['NMSE']) for r in q],
                    label=label,color=color,lw=2,marker='o',ms=4)
    axs[0].set_xscale('log',base=2);axs[0].set_xticks([4,8,16,32,64],[4,8,16,32,64])
    axs[0].set_xlabel('Chronological support count K');axs[0].set_ylabel('Future-query NMSE')
    axs[0].legend(fontsize=8,ncol=2,frameon=False);axes_style(axs[0])
    subset=[(m,labels[m]) for m in labels]
    for i,((method,label),color) in enumerate(zip(subset,colors)):
        r=next(r for r in data if r['method']==method and r['K']=='64')
        v=float(r['NMSE']);axs[1].barh(i,v,color=color);axs[1].text(v+.012,i,f'{v:.3f}',va='center',fontsize=9)
    axs[1].set_yticks(range(len(subset)),[l for _,l in subset]);axs[1].invert_yaxis()
    axs[1].set_xlabel('K64 NMSE (lower is better)');axs[1].set_xlim(0,1.2)
    axs[1].grid(axis='x',color='#e5ebf2');axs[1].set_axisbelow(True)
    finish(fig,'real-world','Real-world transfer is mixed',
           'Historical Beijing 24-hour-ahead PM2.5 • 12 stations, 48 windows • selected methods; all 11 remain in the table',
           'Source: source-data/beijing-accuracy.csv • CC vs persistence is uncertain; more supports also add more recent evidence',preview_dir)

def curriculum(preview_dir):
    fig,ax=plt.subplots(figsize=(11.6,5.0))
    for seed,shift,color in [('1811',-.12,TEAL),('1877',.12,PURPLE)]:
        for i,family in enumerate(['Fourier1','composition']):
            r=pick(study='plateau_CC_curriculum',candidate='CC_D',seed=seed,benchmark=family)[0]
            y,lo,hi=[float(r[k]) for k in ['error_reduction_percent','ci95_low_percent','ci95_high_percent']]
            ax.errorbar(i+shift,y,yerr=[[y-lo],[hi-y]],fmt='o',color=color,ms=7,capsize=5,
                        label=seed if i==0 else None)
    ax.axhline(0,color=MUTED,lw=1);ax.set_xticks([0,1],['Single-component Fourier','Structured composition'])
    ax.set_xlim(-.45,1.45);ax.set_ylabel('Query NMSE reduction vs CC_R (%)');axes_style(ax)
    ax.legend(title='Training seed',frameon=False)
    finish(fig,'curriculum-subgroups','A narrow Fourier benefit; composition did not confirm',
           'Historical CC_D • final D4/K32–64 cases • exploratory unadjusted 95% intervals • broad primary gates failed',
           'Source: benchmarks/public-results.csv • plateau_CC_curriculum / CC_D • all D4 controlled families are exported',preview_dir)

def current_effects(preview_dir):
    data=read('pretraining-64k-effects.csv')
    tracks=['familiar','novel_relationships','excluded_operations','unseen_structure',
            'unseen_dimensions','expanded_robustness']
    labels=['Familiar','Novel relationships','Excluded operations','Unseen structure',
            'Unseen D6/12/24','Expanded robustness']
    fig,axs=plt.subplots(1,2,figsize=(14.4,6.4))
    for ax,arch,title,color,limits in zip(axs,['Tiny','CC'],
            ['TinyMind • seed 1877','TinyMind-CC • seed 1811'],[TEAL,PURPLE],[(-2,4),(-22,11)]):
        for i,track in enumerate(tracks):
            r=next(r for r in data if r['architecture']==arch and r['track']==track)
            value,lo,hi=[float(r[k]) for k in ['gain_percent','ci95_low','ci95_high']]
            ax.errorbar(value,i,xerr=[[value-lo],[hi-value]],fmt='o',color=color,ms=6,capsize=4)
            ax.annotate(f'{value:+.2f}%',(value,i),xytext=(0,10),textcoords='offset points',
                        ha='center',fontsize=9,color=color)
        ax.axvline(0,color=MUTED,lw=1)
        ax.set_yticks(range(len(tracks)),labels);ax.invert_yaxis()
        ax.set_ylim(5.6,-.7);ax.set_xlim(*limits)
        ax.set_title(title,pad=14);ax.set_xlabel('32K→64K query NMSE reduction (%)')
        ax.grid(axis='x',color='#e5ebf2');ax.set_axisbelow(True);ax.tick_params(length=0)
    finish(fig,'pretraining-64k-effects','64K progress includes gains and regressions',
           'Earlier 64K study • fixed endpoints • one selected parent per model • 2,000-resample 95% intervals • separate x-axis scales',
           'Source: source-data/pretraining-64k-effects.csv • whole functions, nested K4/8/16/32/64 • exploratory, unadjusted intervals',preview_dir,left=.13)

def current_curves(preview_dir):
    data=read('pretraining-64k-curves.csv')
    fig,axs=plt.subplots(1,3,figsize=(14.4,5.4))
    for ax,track,title in zip(axs,['familiar','unseen_structure','unseen_dimensions'],
            ['Familiar','Unseen structure','Unseen D6/12/24']):
        for arch,label,color in [('Tiny','TinyMind • 1877',TEAL),('CC','CC • 1811',PURPLE)]:
            q=sorted([r for r in data if r['architecture']==arch and r['track']==track],key=lambda r:int(r['step']))
            assert [int(r['step']) for r in q]==list(range(8000,64001,2000))
            ax.plot([int(r['step'])/1000 for r in q],[float(r['nmse']) for r in q],
                    color=color,lw=2,marker='o',ms=2.8,label=label)
        ax.axvline(32,color=MUTED,lw=1,ls='--')
        ax.axvspan(32,64,color='#edf2f7',zorder=0)
        ax.set_xticks([8,16,32,48,64]);ax.set_xlim(7,65)
        ax.set_title(title,pad=12);ax.set_xlabel('Cumulative optimizer steps (thousands)')
        ax.set_ylabel('Query NMSE (lower is better)')
        ax.legend(frameon=False,fontsize=9);axes_style(ax)
    finish(fig,'pretraining-64k-curves','The earlier plateau was not a permanent ceiling',
           'Earlier 8K–64K study • one confirmation bank • dashed line: changed 32K→64K continuation bundle • axes zoomed',
           'Source: source-data/pretraining-64k-curves.csv • K4/8/16/32/64 • no cross-bank joins or extrapolation; one trajectory per model',preview_dir)

def tabarena(preview_dir):
    data=[r for r in read('tabarena-lite-64k.csv') if r['TinyMind_status']==r['TinyMind-CC_status']=='ok']
    summaries=read('tabarena-lite-64k-summary.csv')
    labels=['QSAR fish','Concrete','Healthcare','Airfoil','Fiat 500','Wine','Miami housing',
            'Houses','Food delivery','Protein','Diamonds']
    assert len(data)==len(labels)==11
    fig,axs=plt.subplots(1,2,figsize=(13.8,8.3),gridspec_kw={'width_ratios':[2.6,1]})
    for model,label,color,shift in [('TinyMind','TinyMind',TEAL,-.18),('TinyMind-CC','TinyMind-CC',PURPLE,.18)]:
        ratios=[float(r[model+'_RMSE'])/float(r['TabPFN-3.5_RMSE']) for r in data]
        axs[0].barh([i+shift for i in range(len(data))],ratios,height=.32,color=color,label=label)
        for i,ratio in enumerate(ratios):
            axs[0].text(ratio+.05,i+shift,f'{ratio:.2f}',va='center',fontsize=8)
        r=next(r for r in summaries if r['candidate']==model and r['reference']=='TabPFN-3.5')
        value=float(r['geometric_mean_relative_RMSE'])
        i=0 if model=='TinyMind' else 1
        axs[1].bar(i,value,color=color,width=.58)
        axs[1].text(i,value+.05,f'{value:.3f}×\n+{float(r["relative_RMSE_gap_percent"]):.2f}%',
                    ha='center',va='bottom',fontsize=11,fontweight='bold',color=color)
    axs[0].set_yticks(range(len(data)),labels);axs[0].invert_yaxis()
    axs[0].set_xlim(0,5.7);axs[0].set_xlabel('Dataset RMSE / TabPFN 3.5 RMSE')
    axs[0].set_title('11 common datasets • lower is better',pad=14)
    axs[0].legend(frameon=False,ncol=2,fontsize=9,loc='lower right')
    axs[0].axvline(1,color=MUTED,lw=1,ls='--');axs[0].grid(axis='x',color='#e5ebf2')
    axs[1].set_xticks([0,1],['TinyMind','CC']);axs[1].set_ylim(0,2.3)
    axs[1].set_ylabel('Geometric-mean RMSE ratio');axs[1].set_title('Equal dataset weight',pad=14)
    axs[1].axhline(1,color=MUTED,lw=1,ls='--');axs[1].grid(axis='y',color='#e5ebf2')
    for ax in axs: ax.set_axisbelow(True);ax.tick_params(length=0)
    finish(fig,'tabarena-lite-64k','Synthetic progress has not closed the real-data gap',
           'Earlier 64K TabArena-Lite • split 0/0/0, 8×1 protocol • 11/13 coverage; D1024 and D81 unsupported • no CI or rank',
           'Source: source-data/tabarena-lite-64k.csv and summary • published fixed TabPFN 3.5 reference • full features/supports',preview_dir)

def failure_driven(preview_dir):
    data=read('failure-driven-70k.csv')
    summaries=read('failure-driven-70k-summary.csv')
    labels=['Yacht','Daily Demand','Metro Traffic','Davis','BudgetFood','gartner.corn']
    assert len(data)==6
    fig,axs=plt.subplots(1,2,figsize=(14.4,7.2))
    totals={}
    for model,label,color,shift in [('TinyMind','TinyMind',TEAL,-.18),('CC','CC',PURPLE,.18)]:
        values=[100*(1-float(r[model+'_70000_RMSE'])/float(r[model+'_64000_RMSE'])) for r in data]
        axs[0].barh([i+shift for i in range(6)],values,height=.32,color=color,label=label)
        for i,value in enumerate(values):
            axs[0].text(value+(.3 if value>=0 else -.3),i+shift,f'{value:+.2f}%',
                        ha='left' if value>=0 else 'right',va='center',fontsize=8,color=color)
        row=next(r for r in summaries if r['candidate']==model+'_70000_RMSE' and r['reference']==model+'_64000_RMSE')
        totals[model]=float(row['RMSE_reduction_percent'])
    axs[0].set_yticks(range(6),labels);axs[0].invert_yaxis();axs[0].set_xlim(-8,31)
    axs[0].set_xlabel('70K versus 64K RMSE reduction (%)')
    axs[0].set_title(f'Geometric mean: CC {totals["CC"]:+.2f}% / Tiny {totals["TinyMind"]:+.3f}%',pad=15)
    axs[0].legend(frameon=False,loc='lower right',ncol=2,fontsize=9)
    refs=[('CatBoost_matched_support_RMSE','CatBoost\nidentical support'),
          ('XGBoost_matched_support_RMSE','XGBoost\nidentical support'),
          ('CatBoost_full_training_RMSE','CatBoost\nfull training'),
          ('XGBoost_full_training_RMSE','XGBoost\nfull training')]
    for i,(reference,label) in enumerate(refs):
        r=next(r for r in summaries if r['candidate']=='CC_70000_RMSE' and r['reference']==reference)
        value=float(r['RMSE_reduction_percent'])
        axs[1].barh(i,value,color=PURPLE if value>0 else RED,height=.55)
        axs[1].text(value+(.4 if value>=0 else -.4),i,f'{value:+.2f}% • {r["candidate_wins"]}/6 wins',
                    ha='left' if value>=0 else 'right',va='center',fontsize=9)
    axs[1].set_yticks(range(4),[x[1] for x in refs]);axs[1].invert_yaxis()
    axs[1].set_xlim(-37,35);axs[1].set_xlabel('CC70K geometric-mean RMSE reduction (%)')
    axs[1].set_title('Traditional ML • both data regimes',pad=15)
    for ax in axs:
        ax.axvline(0,color=MUTED,lw=1)
        ax.grid(axis='x',color='#e5ebf2');ax.set_axisbelow(True);ax.tick_params(length=0)
    finish(fig,'failure-driven-70k','CC improves 9.61%; traditional ML comparison remains mixed',
           'Six failure-driven evaluation datasets • not TabArena-Lite • fixed test partitions • one seed per model • no confidence intervals',
           'Source: source-data/failure-driven-70k.csv and summary • positive reduction is better • full-training trees generally use more labels',preview_dir,left=.13)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-dir',type=Path,help='Optional PNG output for visual review')
    args=parser.parse_args()
    if args.preview_dir: args.preview_dir.mkdir(parents=True,exist_ok=True)
    for renderer in [effects,original_training,plateau_training,causal,efficiency,real_world,curriculum,
                     current_effects,current_curves,tabarena,failure_driven]:
        renderer(args.preview_dir)
    print('Rendered 11 numerical figures from public aggregates.')

if __name__=='__main__':
    main()
