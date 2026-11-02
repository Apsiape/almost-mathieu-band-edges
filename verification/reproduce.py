"""Serial rerun of only the archived numerical cases."""
import os, sys, json, time, subprocess, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
THREAD_KEYS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
for key in THREAD_KEYS:os.environ[key]='1'
def jobs(section):
    if section==4:
        yield 'prediction',['code/certify.py','predict'],''
        for args in json.loads((ROOT/'section-4/inputs/cases.json').read_text()):
            yield 'width_'+str(args[0])+'_'+str(args[2])+'_'+str(args[3]),['code/certify.py','measure',*map(str,args)],''
        yield 'analysis',['code/analyze.py'],''
    elif section==5:
        for i in [4,5,6,7,9,10]:
            yield f'original_{i}',['code/certify_before_rounding_fix.py','original',str(i),'4096'],''
        for i in [0,1]:
            yield f'oos_{i}',['code/certify.py','oos',str(i),'4096'],''
        for i in [0,1]:
            yield f'rounding_excluded_{i}',['code/certify_before_rounding_fix.py','oos',str(i),'4096'],'rounding-excluded'
    elif section==6:
        for i in range(6):
            yield f'original_{i}',['code/certify_coarse.py','original',str(i),'--replay-bracket'],''
        for i in range(4):
            yield f'oos_{i}',['code/certify.py','oos',str(i),'--replay-bracket'],''
        for i in range(4):
            yield f'coarse_{i}',['code/certify_coarse.py','oos',str(i),'--replay-bracket'],'coarse'
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--section',type=int,choices=[4,5,6],action='append')
    ns=ap.parse_args()
    for section in ns.section or [4,5,6]:
        folder=ROOT/f'section-{section}';out=folder/'rerun';out.mkdir(exist_ok=True)
        records=[]
        for label,args,subdir in jobs(section):
            dest=out/subdir;dest.mkdir(parents=True,exist_ok=True)
            env=os.environ.copy();env['CERT_OUTPUT_DIR']=str(dest)
            start=time.monotonic()
            try:
                p=subprocess.run([sys.executable,'-u','-B',*args],cwd=folder,env=env,capture_output=True,text=True,timeout=1200)
                status='completed' if p.returncode==0 else 'failed';rc=p.returncode
                stdout,stderr=p.stdout,p.stderr
            except subprocess.TimeoutExpired as exc:
                status='skipped';rc=None
                stdout=exc.stdout or '';stderr=exc.stderr or ''
                if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
                if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
            elapsed=time.monotonic()-start
            # Exception paths are unnecessary in a public numerical log.
            stdout=stdout.replace(str(ROOT),'.').replace(ROOT.as_posix(),'.')
            stderr=stderr.replace(str(ROOT),'.').replace(ROOT.as_posix(),'.')
            logs=out/'logs';logs.mkdir(exist_ok=True)
            (logs/(label+'.stdout.txt')).write_text(stdout,encoding='utf8')
            if stderr:(logs/(label+'.stderr.txt')).write_text(stderr,encoding='utf8')
            records.append(dict(label=label,command=['python','-u','-B',*args],working_directory=f'section-{section}',output_subdirectory=subdir or '.',timeout_seconds=1200,threads=1,status=status,exit_code=rc,seconds=round(elapsed,6)))
            (out/'runs.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf8')
            print(f'Section {section}: {label}: {status} ({elapsed:.3f} s)',flush=True)
            if status=='failed':
                print(stderr,flush=True)
                raise SystemExit(1)
    print('Reruns finished. Run python -B validate.py to check the archived claims.',flush=True)
if __name__=='__main__':main()

