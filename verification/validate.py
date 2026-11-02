"""Compare regenerated certificates with archived claims and reported scope."""
import os,json,hashlib,re,argparse
from pathlib import Path
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
from flint import arb,ctx
ctx.prec=4096;ctx.threads=1
ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def outward(value,places=12):
    x=arb(value);scale=10**places
    lo=int((x.lower()*scale).floor().unique_fmpz());hi=int((x.upper()*scale).ceil().unique_fmpz())
    def fmt(n):return ('-' if n<0 else '')+str(abs(n)//scale)+'.'+str(abs(n)%scale).zfill(places)
    return [fmt(lo),fmt(hi)]
def canonical(d):
    if isinstance(d,list):return [canonical(x) for x in d]
    if isinstance(d,dict):return {k:canonical(v) for k,v in d.items() if k not in ['seconds','script_sha256','engine_sha256']}
    return d
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--section',type=int,choices=[4,5,6],action='append')
    selected=ap.parse_args().section or [4,5,6]
    results=json.loads((ROOT/'RERUN-RESULTS.json').read_text()) if (ROOT/'RERUN-RESULTS.json').exists() else {}
    for section in selected:
        folder=ROOT/f'section-{section}';runs=read(folder/'rerun/runs.json')
        assert all(x['status']=='completed' and x['exit_code']==0 and x['threads']==1 and x['timeout_seconds']==1200 for x in runs)
        results[str(section)]=dict(processes=len(runs),seconds=round(sum(x['seconds'] for x in runs),6),maximum_process_seconds=max(x['seconds'] for x in runs),skipped=0)
    if 4 in selected:
        r=ROOT/'section-4';rows=[]
        for p in sorted((r/'certificates').glob('independent_*.json')):
            old=read(p);new=read(r/'rerun'/p.name);assert new==old,p.name
            rows+=new
        assert len(rows)==23 and sum(x['lam']==5 for x in rows)==4
        assert read(r/'certificates/preregistered_base.json')==read(r/'rerun/preregistered_base.json')
        old=read(r/'certificates/summary.json');new=read(r/'rerun/summary.json')
        for key in ['rows','original_rows','out_of_sample_rows','slopes','increments']:assert old[key]==new[key],key
        original=[x for x in rows if x['lam']!=5];oos=[x for x in rows if x['lam']==5]
        assert all(arb(x['collapse'])>=arb('1.0045') and arb(x['collapse'])<=arb('1.0558') for x in original)
        assert all(arb(x['collapse'])>=arb('.95') and arb(x['collapse'])<=arb('1.10') for x in oos)
        assert all(x['counts']==[x['D']]*3 and x['edge_signs_certified'] for x in rows)
        fail=[x for x in new['slopes'] if (x['lam'],x['q'],x['D'])==(3,13,5)][0]
        assert abs(arb(fail['slope'])-8)>arb('.25')
        witness=[x for x in new['increments'] if (x['lam'],x['q'],x['A'],x['D'])==(2,21,10,2)][0]
        assert abs(arb(witness['residual']))>arb('.0061')
        assert all(abs(arb(x['residual']))<arb('.00660') for x in new['increments'] if x['lam']!=5)
        original_log=min(original,key=lambda x:float(arb(x['logw']).mid()))['logw']
        results['4'].update(status='reproduced',widths=23,original=19,out_of_sample=4,scientific_outputs='exact JSON equality',smallest_original_log_width=outward(original_log),failed_D5_slope=outward(fail['slope']),false_increment_bound='.0061',safe_original_increment_bound='.00660')
    if 5 in selected:
        r=ROOT/'section-5'
        labels=[f'original_{i}' for i in [4,5,6,7,9,10]]+['oos_0','oos_1']
        expected={'original_4':'.6610','original_5':'.6845','original_6':'.6326','original_7':'.6810','original_9':'.6858','original_10':'.6604'}
        for label in labels:
            old=read(r/'certificates'/(label+'.json'));new=read(r/'rerun'/(label+'.json'))
            assert canonical(old)==canonical(new),label
            assert new['all_windows_resolved'] and new['residuals_verified']
            if label in expected:assert abs(arb(new['gamma'])-arb(expected[label]))<arb('.002')
            else:assert all(new['predictions'])
        for i in [0,1]:
            old=read(r/'excluded'/f'oos_{i}_rounding_invalid.json');new=read(r/'rerun/rounding-excluded'/f'oos_{i}.json')
            assert canonical(old)==canonical(new)
        results['5'].update(status='reproduced',accepted_certificates=8,original=6,out_of_sample=2,scientific_outputs='exact JSON equality except elapsed time and adapted script hashes',excluded_rounding_trials='reproduced; remain excluded',excluded_window_trials='preserved as invalid, not rerun with accepted convention')
    if 6 in selected:
        r=ROOT/'section-6'
        for mode,count in [('original',6),('oos',4)]:
            for i in range(count):
                old=read(r/'certificates'/f'{mode}_{i}.json');new=read(r/'rerun'/f'{mode}_{i}.json')
                assert old['outward_rho']==new['outward_rho']
                for key in ['N','k','precision_bits','parameters','emax','Pprime','m0','gram_deviation','predicted_edge','edge_factor']:
                    assert old[key]==new[key],(mode,i,key)
                assert arb(new['gram_deviation'][1])<1
                assert new['tests']['strict_one']['nnegative_compression']==0
                assert new['tests']['lower']['nnegative_compression']==0
                assert new['tests']['upper']['nnegative_compression']>0
                assert arb(new['tests']['strict_one']['rho'][0])>1
                for name,endpoint in [('lower',new['outward_rho'][0]),('upper',new['outward_rho'][1])]:
                    lo,hi=map(arb,new['tests'][name]['rho']);assert lo<=arb(endpoint) and hi>=arb(endpoint)
                for test in new['tests'].values():
                    for lo,hi in test['congruence_discs']:assert arb(lo)>0 or arb(hi)<0
                if mode=='oos':assert new['registered_individual_predictions_pass']
        for i in range(4):
            old=read(r/'certificates'/f'oos_{i}_coarse.json');new=read(r/'rerun/coarse'/f'oos_{i}.json')
            assert old['outward_rho']==new['outward_rho']
            assert new['tests']['lower']['nnegative_compression']==0 and new['tests']['upper']['nnegative_compression']>0
        pair_bounds=[]
        for i in [0,2]:
            a=read(r/'rerun'/f'oos_{i}.json');b=read(r/'rerun'/f'oos_{i+1}.json')
            al,ah=map(arb,a['outward_rho']);bl,bh=map(arb,b['outward_rho'])
            bound=max(ah-bl,bh-al);assert bound<arb('.05')
            pair_bounds.append(dict(b=a['parameters']['b'],absolute_difference_upper=outward(bound)))
        results['6'].update(status='within enclosure',accepted_certificates=10,original=6,out_of_sample=4,coarse_out_of_sample=4,scientific_outputs='archived decimal bracket endpoints independently recertified by interval inertia',pair_bounds=pair_bounds)
    for p in ROOT.rglob('*.py'):compile(p.read_text(encoding='utf-8-sig'),p.name,'exec')
    (ROOT/'RERUN-RESULTS.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()

