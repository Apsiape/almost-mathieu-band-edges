"""Independent finite-span spectral certificates; no submission code imports.
Uses direct tridiagonal LDL solves and constrained inertia, with Arb throughout
certification. Float eigensolvers choose test locations only.
"""
import os,sys,json,time,math,hashlib
os.environ.update({k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']})
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu,eigsh,LinearOperator
from flint import arb,arb_mat,acb_mat,ctx
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get("CERT_OUTPUT_DIR",str(ROOT/"rerun")))
OUT.mkdir(parents=True,exist_ok=True)
SRC=ROOT/'inputs'
ctx.prec=512
ctx.threads=1
A=arb

def outward(x,places=12):
    scale=10**places
    lo=int((x*scale).lower().floor().unique_fmpz())
    hi=int((x*scale).upper().ceil().unique_fmpz())
    def fmt(n):
        sg='-' if n<0 else ''; n=abs(n)
        return f'{sg}{n//scale}.{n%scale:0{places}d}'
    return [fmt(lo),fmt(hi)]

def sign(x):
    if x>0:return 1
    if x<0:return -1
    raise ArithmeticError('Unresolved interval sign')

def clamp(v):
    if v<0:return -clamp(-v)
    if v<A(1)/4:return v
    if v>A(9)/20:return A(3)/8
    t=(v-A(1)/4)*5
    return A(1)/4+(t**3-2*t**2+t)/5+(-2*t**3+3*t**2)/8

def frozen(lam,p,q,t,k):
    B=np.diag(2*lam*np.cos(2*np.pi*((np.arange(q)*p%q)/q+t))).astype(complex)
    for i in range(q-1):B[i,i+1]=B[i+1,i]=1
    B[q-1,0]=np.exp(1j*k);B[0,q-1]=np.exp(-1j*k)
    return B

def make_frame(lam,p,q,delta,jcells):
    sites=np.arange(-64*q,64*q);cell=sites//q;res=sites%q
    vectors=[]
    for j in jcells:
        phase=delta*(j-.3);w=np.zeros(len(sites),complex)
        for ell in range(128):
            k=2*np.pi*ell/128
            _,V=np.linalg.eigh(frozen(lam,p,q,phase,k))
            v=V[:,-1];v*=v[0].conjugate()/abs(v[0])
            w+=np.exp(1j*k*cell)*v[res]/128
        assert max(abs(w.imag))<1e-11
        w=w.real
        cut=int(max(abs(sites[(abs(w)>=max(abs(w))*1e-13)&(abs(sites)<=10*q)])))
        mask=abs(sites)<=cut
        vectors.append((int(j*q-cut),w[mask].copy()))
    return vectors

def norm_data(lam,p,q,b):
    B=acb_mat(q,q)
    for i in range(q):
        B[i,i]=2*lam*(2*A.pi()*A((i*p)%q)/q).cos()
        B[i,(i+1)%q]+=1;B[(i+1)%q,i]+=1
    eigen=list(B.eig(algorithm='rump'))
    re=sorted([z.real for z in eigen],key=lambda x:float(x.mid()))
    assert all(re[-1]>z for z in re[:-1])
    pp=A(1)
    for z in re[:-1]:pp*=re[-1]-z
    mp=A(lam)**q*(-A(b)*q/8).exp()
    m0=2*mp/(9*A.pi()**2*pp)
    return re[-1],pp,mp,m0

def make_case(mode,index):
    if mode=='original':
        lam,q,b,fam=[(2,13,'.33','cont'),(2,13,'.33','box'),(2,21,'.28','cont'),(2,21,'.28','box'),(3,34,'.25','cont'),(3,34,'.25','box')][index]
        tag=f'{fam}_l{lam}_q{q}_b{float(b):.2f}'
        d=json.loads((SRC/f'e2_{tag}.json').read_text())
        delta=float.fromhex(d['delta']);lo=d['mlo'];hi=d['mhi']
        f=np.load(SRC/f'frame_{tag}.npz');vecs=[];pos=0
        for start,length in zip(f['starts'],f['lens']):
            vecs.append((int(start),f['data'][pos:pos+length].copy()));pos+=length
        assert pos==len(f['data'])
        rounding='original submitted exact dyadic delta'
    else:
        lam,q=5,21;b=['.28','.33'][index//2];fam=['cont','box'][index%2]
        tag=f'{fam}_l{lam}_q{q}_b{float(b):.2f}'
        exact=(-A(b)*q).exp();delta=float(exact.mid())
        prev=np.nextafter(delta,-np.inf);nxt=np.nextafter(delta,np.inf)
        assert exact>(A(float(prev))+A(delta))/2 and exact<(A(delta)+A(float(nxt)))/2
        rounding='Arb-certified nearest binary64 to exact exp(-b*q)'
        tf=(-A(b)*q/16).exp()/(2*A.pi()*q)
        radius=A(9)/(20*A(delta))+4*q if fam=='cont' else A(1)/(2*A(delta))
        lo=int((A(3*q)/10-radius).ceil().unique_fmpz());hi=int((A(3*q)/10+radius).floor().unique_fmpz())
        jl=int((A(3)/10-tf/A(delta)).ceil().unique_fmpz());jh=int((A(3)/10+tf/A(delta)).floor().unique_fmpz())
        if '--generate-frame' in sys.argv:
            vecs=make_frame(lam,13,q,delta,list(range(jl,jh+1)))
        else:
            f=np.load(SRC/f'oos_{index}_frame.npz');vecs=[];pos=0
            for start,length in zip(f['starts'],f['lens']):
                vecs.append((int(start),f['data'][pos:pos+length].copy()));pos+=length
            assert pos==len(f['data'])
    p={13:8,21:13,34:21}[q]
    truncated=[]
    for start,v in vecs:
        a=max(start,lo);e=min(start+len(v),hi+1)
        assert e>a
        truncated.append((a-lo,v[a-start:e-start].copy()))
    return dict(lam=lam,p=p,q=q,b=b,family=fam,tag=tag,delta=delta,mlo=lo,mhi=hi,rounding=rounding),truncated

def gram_guard(vec):
    k=len(vec);G=arb_mat(k,k)
    for i,(s,v) in enumerate(vec):
        for j,(t,w) in enumerate(vec):
            a=max(s,t);b=min(s+len(v),t+len(w))
            G[i,j]=sum((v[x-s]*w[x-t] for x in range(a,b)),A(0))
    dev=A(0)
    for i in range(k):
        r=sum((abs(G[i,j]-(1 if i==j else 0)) for j in range(k)),A(0))
        if r>dev:dev=r
    assert dev<1
    return dev

def inertia(E,potential,vec):
    n=len(potential);k=len(vec)
    piv=[];neg=0
    for i in range(n):
        d=E-potential[i]-(1/piv[-1] if i else 0)
        neg+=sign(d)<0;piv.append(d)
    S=arb_mat(k,k)
    for j,(start,v) in enumerate(vec):
        z=[A(0) for _ in range(n)]
        for i in range(start,n):
            z[i]=(v[i-start] if i<start+len(v) else A(0))+(z[i-1]/piv[i-1] if i else 0)
        for i in range(n-1,-1,-1):z[i]=(z[i]+(z[i+1] if i+1<n else 0))/piv[i]
        for i,(a,w) in enumerate(vec):S[i,j]=sum((w[t]*z[a+t] for t in range(len(w))),A(0))
    npos=0;discs=[]
    if k:
        mid=np.array([[float(S[i,j].mid()) for j in range(k)] for i in range(k)])
        _,Q=np.linalg.eigh((mid+mid.T)/2)
        T=arb_mat([[A(float(v)) for v in row] for row in Q])
        orth=T.transpose()*T
        for i in range(k):assert sum((abs(orth[i,j]-(i==j)) for j in range(k)),A(0))<1
        Sym=arb_mat([[(S[i,j]+S[j,i])/2 for j in range(k)] for i in range(k)])
        C=T.transpose()*Sym*T
        for i in range(k):
            r=sum((abs(C[i,j]) for j in range(k) if j!=i),A(0))
            if C[i,i]-r>0:npos+=1
            else:assert C[i,i]+r<0
            discs.append([outward(C[i,i]-r,8)[0],outward(C[i,i]+r,8)[1]])
    count=neg+npos-k
    assert 0<=count<=n-k
    return dict(nnegative_A=neg,npositive_S=npos,rank=k,nnegative_compression=count,congruence_discs=discs)

def main():
    t0=time.time();mode=sys.argv[1];index=int(sys.argv[2]);P,vfloat=make_case(mode,index)
    lam,p,q,b=P['lam'],P['p'],P['q'],P['b'];delta=A(P['delta']);lo,hi=P['mlo'],P['mhi'];n=hi-lo+1;k=len(vfloat)
    emax,pp,mp,m0=norm_data(lam,p,q,b)
    pot=[]
    for x in range(lo,hi+1):
        u=delta*(A(x)-A(3*q)/10)
        ph=(clamp(u) if P['family']=='cont' else u)/q
        pot.append(2*lam*(2*A.pi()*(A(x*p%q)/q+ph)).cos())
    vec=[(a,[A(float(x)) for x in v]) for a,v in vfloat]
    gram=gram_guard(vec)
    rows=[];cols=[];vals=[]
    for j,(a,v) in enumerate(vfloat):
        rows.extend(range(a,a+len(v)));cols.extend([j]*len(v));vals.extend(v)
    V=sp.csc_matrix((vals,(rows,cols)),shape=(n,k))
    H=sp.diags([np.ones(n-1),np.array([float(x.mid()) for x in pot]),np.ones(n-1)],[-1,0,1],format='csc')
    shift=float((emax-m0/2).mid())
    K=sp.bmat([[H-shift*sp.eye(n,format='csc'),V],[V.T,None]],format='csc')
    factor=splu(K)
    def solve(x):return factor.solve(np.concatenate([x,np.zeros(k)]))[:n]
    op=LinearOperator((n,n),matvec=solve,dtype=float)
    mu=eigsh(op,k=1,which='SA',tol=1e-11,return_eigenvectors=False,v0=np.linspace(1,2,n))[0]
    estimate=shift+1/mu;rho=(float(emax.mid())-estimate)/float(m0.mid())
    assert rho>0
    replay=None
    if '--replay-bracket' in sys.argv:
        suffix='_coarse' if mode=='oos' and 'coarse' in Path(__file__).name else ''
        replay=json.loads((ROOT/'certificates'/f'{mode}_{index}{suffix}.json').read_text())['outward_rho']
    tests={}
    for name,target in [('strict_one',1.000001),('lower',rho*.999),('upper',rho*1.001)]:
        if replay is not None and name in ['lower','upper']:
            target=A(replay[0 if name=='lower' else 1])
        else:
            target=A(float(target))
        E=emax-target*m0
        cert=inertia(E,pot,vec)
        cert.update(rho=outward((emax-E)/m0),energy=outward(E,16))
        tests[name]=cert
        print(P['tag'],name,cert['nnegative_compression'],cert['rho'],flush=True)
    assert tests['strict_one']['nnegative_compression']==0
    assert tests['lower']['nnegative_compression']==0 and tests['upper']['nnegative_compression']>0
    tf=(-A(b)*q/16).exp()/(2*A.pi()*q)
    jl=int((A(3)/10-tf/delta).ceil().unique_fmpz());jh=int((A(3)/10+tf/delta).floor().unique_fmpz())
    outj=min([jl-1,jh+1],key=lambda j:abs(j-.3))
    tout=abs(delta*(A(outj)-A(3)/10));g=2*A(lam)**q*(1-(2*A.pi()*q*tout).cos())
    pred=9*A.pi()**2/2*g/mp
    lower=A(replay[0] if replay else tests['lower']['rho'][0]);upper=A(replay[1] if replay else tests['upper']['rho'][1])
    out=dict(parameters={**P,'delta':P['delta'].hex()},N=n,k=k,precision_bits=ctx.prec,emax=outward(emax,16),Pprime=pp.str(35),m0=m0.str(35),gram_deviation=outward(gram,16),tests=tests,rho_bracket=[str(lower),str(upper)],outward_rho=replay if replay else [tests['lower']['rho'][0],tests['upper']['rho'][1]],predicted_edge=outward(pred),edge_factor=[outward(lower/pred)[0],outward(upper/pred)[1]],seconds=time.time()-t0,engine_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if mode=='oos':
        bands=[(60,85),(45,60)][index//2]
        assert lower>=bands[0] and upper<=bands[1]
        assert lower/pred>=A('.85') and upper/pred<=A('1.15')
        out['registered_individual_predictions_pass']=True
        np.savez(OUT/f'{mode}_{index}_frame.npz',starts=np.array([a+lo for a,v in vfloat]),lens=np.array([len(v) for a,v in vfloat]),data=np.concatenate([v for a,v in vfloat]))
    (OUT/f'{mode}_{index}.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    print(json.dumps({x:out[x] for x in ['N','k','outward_rho','predicted_edge','edge_factor','seconds']}),flush=True)

if __name__=='__main__':main()
