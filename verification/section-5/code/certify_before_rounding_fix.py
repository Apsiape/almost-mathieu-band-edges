"""Independent finite-span AMO Green certificates. Never imports submitted code."""
import os, json, sys, math, time, hashlib
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']: os.environ[name]='1'
from pathlib import Path
from flint import arb, arb_mat, acb_mat, ctx
import numpy as np
from scipy.linalg import eigh
ctx.threads=1
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('CERT_OUTPUT_DIR',str(ROOT/'rerun')))
OUT.mkdir(parents=True,exist_ok=True)
INPUT=ROOT/'inputs/original_cases.json'
def exact_float(x):
    u,v=float(x).as_integer_ratio(); return arb(u)/v
def exact_hex(x): return exact_float(float.fromhex(x))
def trace_derivative(E,lam,p,q,phase=0):
    a,b,c,d=arb(1),arb(0),arb(0),arb(1)
    da,db,dc,dd=arb(0),arb(0),arb(0),arb(0)
    for n in range(q):
        z=E-2*lam*(2*arb.pi()*(arb(n*p)/q+phase)).cos()
        a,b,c,d,da,db,dc,dd=z*a-c,z*b-d,a,b,a+z*da-dc,b+z*db-dd,da,db
    return a+d,da+dd
def base(lam,p,q):
    # Certify ALL eigenvalues; the unique largest enclosure selects Emax.
    A=acb_mat(q,q)
    for n in range(q):
        A[n,n]=2*lam*(2*arb.pi()*arb(n*p)/q).cos()
        A[n,(n-1)%q]+=1; A[n,(n+1)%q]+=1
    vals=A.eig(multiple=True)
    vals=sorted(vals,key=lambda v:float(v.real.mid()))
    E=vals[-1].real
    assert all(E.lower()>v.real.upper() for v in vals[:-1])
    assert all(v.imag.contains(0) for v in vals)
    tr,dp=trace_derivative(E,lam,p,q)
    assert (tr-2).contains(0) and dp.lower()>0
    return E,dp

def fresh_case(lam=5,p=13,q=21,b=.28):
    delta=math.exp(-b*q); xi=b/4; tfr=math.exp(-xi*q/4)/(2*math.pi*q)
    theta=-.3*delta; eps=delta/q; alpha=p/q+eps
    J=list(range(math.ceil(.3-tfr/delta),math.floor(.3+tfr/delta)+1))
    lo=(min(J)-10)*q-q//2; hi=(max(J)+11)*q-q//2-1
    centres=[]; frames=[]
    # Enumerate anchors directly; do not import the object's frame builder.
    for nu in range(math.floor(q*(theta+lo*eps))-3,math.ceil(q*(theta+hi*eps))+4):
        anchor=(-pow(p,-1,q)*nu)%q
        for j in range(math.ceil((lo-anchor)/q),math.floor((hi-anchor)/q)+1):
            c=j*q+anchor; t=theta-nu/q+c*eps
            if abs(t)>tfr: continue
            # Boundary gauge: last-to-first hopping exp(ik). Its eigenvector,
            # anchored at site zero, is exp(ik*s/q)*u_uniform(s).
            K=128; sites=np.arange(-10*q,10*q+1); sample=np.zeros(len(sites),complex)
            for k in 2*np.pi*np.arange(K)/K:
                diag=2*lam*np.cos(2*np.pi*(np.arange(q)*p/q+t))
                mat=np.diag(diag.astype(complex))+np.diag(np.ones(q-1),1)+np.diag(np.ones(q-1),-1)
                mat[-1,0]=np.exp(1j*k); mat[0,-1]=np.exp(-1j*k)
                _,v=eigh(mat,subset_by_index=[q-1,q-1],driver='evr')
                u=v[:,0]; u*=np.conj(u[0])/abs(u[0])
                sample+=np.exp(1j*k*np.floor_divide(sites,q))*u[np.mod(sites,q)]/K
            assert np.max(abs(sample.imag))<1e-12
            vals=sample.real; threshold=np.max(abs(vals))*1e-13
            cut=max(abs(int(s)) for s,w in zip(sites,vals) if abs(w)>=threshold)
            w=vals[abs(sites)<=cut]
            frames.append(dict(nu=nu,j=j,c=c,t=t,start=c-cut,w=[float(x).hex() for x in w]))
            centres.append(c)
    return dict(lam=lam,p=p,q=q,b=b,xi=xi,delta=delta.hex(),theta=theta.hex(),J=J,x_lo=lo,x_hi=hi,N=hi-lo+1,F=len(frames),frames=frames,frame_centres=centres,sources=[0])

def make_delta(case):
    val=case['delta']; return exact_hex(val) if isinstance(val,str) and ('0x' in val) else exact_float(float(val))
def green(case,E,source):
    lam,p,q=case['lam'],case['p'],case['q']; lo,hi=case['x_lo'],case['x_hi']; N=hi-lo+1
    delta=make_delta(case)
    theta=exact_hex(case['theta']) if '0x' in str(case['theta']) else exact_float(float(case['theta']))
    # Original input alpha is an exact binary64 value, as encoded in cases.json.
    # This follows the submitted data's definition; new cases use exact p/q+delta/q.
    if 'alpha' in case:
        alpha=exact_hex(case['alpha']) if '0x' in str(case['alpha']) else exact_float(float(case['alpha']))
    else: alpha=arb(p)/q+delta/q
    diag=[E-2*lam*(2*arb.pi()*(alpha*x+theta)).cos() for x in range(lo,hi+1)]
    V=[[arb(0) for k in case['frames']] for n in range(N)]
    for k,frame in enumerate(case['frames']):
        for i,w in enumerate(frame['w']):
            n=frame['start']+i-lo
            if 0<=n<N: V[n][k]=exact_hex(w)
    F=len(case['frames']); B=[[arb(int(n==source-lo))]+V[n][:] for n in range(N)]
    piv=diag[:]
    # A has off-diagonal -1. All pivots must be certified nonzero.
    for n in range(1,N):
        assert not piv[n-1].contains(0)
        f=1/piv[n-1]; piv[n]-=f
        B[n]=[x+f*y for x,y in zip(B[n],B[n-1])]
    assert not piv[-1].contains(0)
    B[-1]=[x/piv[-1] for x in B[-1]]
    for n in range(N-2,-1,-1): B[n]=[(x+y)/piv[n] for x,y in zip(B[n],B[n+1])]
    if F:
        M=arb_mat([[sum((V[n][i]*B[n][j+1] for n in range(N)),arb(0)) for j in range(F)] for i in range(F)])
        rhs=arb_mat([[sum((V[n][i]*B[n][0] for n in range(N)),arb(0))] for i in range(F)])
        coeff=M.solve(rhs)
        g=[B[n][0]-sum((B[n][i+1]*coeff[i,0] for i in range(F)),arb(0)) for n in range(N)]
        for i in range(F): assert sum((V[n][i]*g[n] for n in range(N)),arb(0)).contains(0)
    else: coeff=arb_mat(0,1);g=[row[0] for row in B]
    for n in range(N):
        r=diag[n]*g[n]-(g[n-1] if n else 0)-(g[n+1] if n<N-1 else 0)
        r+=sum((V[n][i]*coeff[i,0] for i in range(F)),arb(0))-int(n==source-lo)
        assert r.contains(0)
    return g

def max_ball(values):
    # A rigorous enclosure of the maximum, including switching maximizers.
    lower=max(v.abs_lower() for v in values); upper=max(v.abs_upper() for v in values)
    return arb((lower+upper)/2,(upper-lower)/2)
def profile(case,g,E,source):
    lo,hi=case['x_lo'],case['x_hi'];q=case['q'];J=case['J']
    rates=[]; mind=10**9; argmin=None
    for side in [-1,1]:
        sidepoints=[x for x in range(lo,hi+1) if side*(x-source)>=0]
        seq=[abs(g[x-lo]) for x in sidepoints]
        if side<0: seq=seq[::-1]
        tails=[None]*len(seq); bestlo=arb(0);besthi=arb(0)
        for d in range(len(seq)-1,-1,-1):
            bestlo=max(bestlo,seq[d].abs_lower());besthi=max(besthi,seq[d].abs_upper())
            tails[d]=arb((bestlo+besthi)/2,(besthi-bestlo)/2)
        # Frame edge is the centre of the extreme included frame cell;
        # outer statistic begins at that frame edge (or q when no frame exists).
        edge=(max(J)*q+q//2 if side>0 else min(J)*q-q//2) if J else source
        start=max(q,abs(edge-source)) if J else q
        stop=len(seq)-1-5*q
        for d in range(start,stop+1):
            assert tails[d].lower()>0 and tails[d+2*q].lower()>0, 'Unresolved window rejected'
            rate=(tails[d].log()-tails[d+2*q].log())/(2*q)
            rates.append(rate)
            if float(rate.mid())<mind: mind=float(rate.mid());argmin=[side,d]
    assert rates
    lower=min(v.lower() for v in rates);upper=min(v.upper() for v in rates)
    gamma=arb((lower+upper)/2,(upper-lower)/2)
    delta=make_delta(case);theta=exact_hex(case['theta']) if '0x' in str(case['theta']) else exact_float(float(case['theta']))
    floqs=[]
    for j in range(math.ceil(lo/q),math.floor(hi/q)+1):
        cell_a=j*q-q//2; cell_b=cell_a+q
        if any(cell_a<=cc<cell_b for cc in case['frame_centres']): continue
        fmin=min(J)*q-q//2 if J else source-q
        fmax=max(J)*q+q//2 if J else source+q
        if not(j*q<=fmin or j*q>=fmax): continue
        if not(lo+3*q<=j*q<=hi+1-3*q): continue
        t=theta+j*delta
        tr,_=trace_derivative(E,case['lam'],case['p'],q,t)
        if tr.abs_lower()>2: floqs.append((abs(tr)/2).acosh()/q)
    gF=None
    if floqs:
        low=min(z.lower() for z in floqs);up=min(z.upper() for z in floqs);gF=arb((low+up)/2,(up-low)/2)
    return gamma,gF,argmin,len(rates)

def main():
    mode=sys.argv[1]; idx=int(sys.argv[2]); ctx.prec=int(sys.argv[3]) if len(sys.argv)>3 else 4096
    if mode=='original': case=json.loads(INPUT.read_text())[str(idx)]; label='original_'+str(idx)
    else:
        label='oos_'+str(idx)
        case=fresh_case(b=[.28,.33][idx]) if '--generate-frame' in sys.argv else json.loads((ROOT/('excluded' if 'before_rounding' in Path(__file__).name else 'inputs')/(label+('_rounding_invalid_input.json' if 'before_rounding' in Path(__file__).name else '_input.json'))).read_text())
        (OUT/(label+'_input.json')).write_text(json.dumps(case))
    t=time.monotonic();Emax,dp=base(case['lam'],case['p'],case['q'])
    xi=arb(str(case['b']))/4
    m0=2*arb(case['lam'])**case['q']*(-xi*case['q']/2).exp()/(9*arb.pi()**2*dp)
    E=exact_hex(case['E']['minus']) if mode=='original' else Emax-m0/8
    assert (E-Emax).abs_upper() < m0.lower()/4
    g=green(case,E,0);gamma,gF,argmin,num=profile(case,g,E,0)
    target=arb(case['lam']).log()-xi
    data=dict(label=label,lambda_=case['lam'],q=case['q'],b=case['b'],N=case['N'],F=case['F'],precision=ctx.prec,Emax=Emax.str(60),Pprime=dp.str(60),m0=m0.str(60),E=E.str(60),gamma=gamma.str(40),target=target.str(40),shortfall=(target-gamma).str(40),gF=None if gF is None else gF.str(40),argmin=argmin,windows=num,seconds=time.monotonic()-t,residuals_verified=True,all_windows_resolved=True,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if mode!='original':
        data['predictions']=[bool(gamma.lower()>=arb('1.50') and gamma.upper()<=arb('1.75')),bool((gamma-target+arb('.02')).lower()>=0),bool(gF is not None and (gamma-gF).abs_upper()<=arb('.06'))]
    (OUT/(label+'.json')).write_text(json.dumps(data,indent=2));print(json.dumps(data),flush=True)
if __name__=='__main__': main()


