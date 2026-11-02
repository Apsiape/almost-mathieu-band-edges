"""Independent rational-width certificate engine. Arb transfer jets + Rolle brackets.
Numerical threads fixed to one; bounded by external process timeout; <100 MB arrays.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import sys,json,time,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from flint import arb,ctx
ctx.prec=4096
ctx.threads=1
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get("CERT_OUTPUT_DIR",str(ROOT/"rerun")))
OUT.mkdir(parents=True,exist_ok=True)

def potential(p,q,lam):
    return [2*lam*(arb.pi()*arb(4*j*p+1)/(2*q)).cos() for j in range(q)]

class Trace:
    def __init__(self,p,q,lam):
        self.q=q;self.lam=lam;self.v=potential(p,q,lam)
        self.target=2*arb(lam)**q+2
    def jet(self,x):
        # Matrix rows of transfer product; jets are actual derivatives.
        a,b,c,d=arb(1),arb(0),arb(0),arb(1)
        a1,b1,c1,d1=arb(0),arb(0),arb(0),arb(0)
        a2,b2,c2,d2=arb(0),arb(0),arb(0),arb(0)
        for v in self.v:
            t=x-v
            a2,b2,c2,d2=t*a2+2*a1-c2,t*b2+2*b1-d2,a2,b2
            a1,b1,c1,d1=t*a1+a-c1,t*b1+b-d1,a1,b1
            a,b,c,d=t*a-c,t*b-d,a,b
        return a+d,a1+d1,a2+d2
    def zeros_float(self,num):
        q=self.q
        v=np.array([float(z.mid()) for z in self.v])
        a=np.diag(v).astype(complex)
        a+=np.diag(np.ones(q-1),1)+np.diag(np.ones(q-1),-1)
        a[0,-1]=-1j;a[-1,0]=1j
        return eigh(a,subset_by_index=[q-num,q-1],eigvals_only=True,driver='evr')[::-1]

def certified_above(p,q,lam,E,theta_num,theta_den,kquarter):
    vv=[2*lam*(2*arb.pi()*(arb(j*p)/q+arb(theta_num)/theta_den)).cos()-E for j in range(q)]
    # Eliminate the path 0..q-2 while retaining the final vertex as a border.
    re=(arb.pi()*kquarter/2).cos();im=(arb.pi()*kquarter/2).sin()
    last=vv[-1];diag=vv[0];count=0
    for j in range(q-1):
        assert diag>0 or diag<0,('undecided LDL pivot',j)
        count+=int(diag>0)
        last-=(re*re+im*im)/diag
        if j<q-2:
            re,im=(arb(1) if j+1==q-2 else arb(0))-re/diag,-im/diag
            diag=vv[j+1]-1/diag
    assert last>0 or last<0
    return count+int(last>0)

def point(x):return x.mid()
def newton(f,x,component=0,maxiter=80):
    x=arb(str(x)) if isinstance(x,(float,int)) else x
    for _ in range(maxiter):
        j=f.jet(x); step=j[component]/j[component+1]
        xn=point(x-step)
        if abs(step)<arb('1e-240'):return xn
        x=xn
    raise RuntimeError('newton failed')

def find_edge(f,c,sign,side):
    v,_,v2=f.jet(c)
    radius=(-2*(sign*v-f.target)/(sign*v2)).sqrt()
    x=point(c+side*radius)
    for _ in range(40):
        v,v1,_=f.jet(x)
        dx=(sign*v-f.target)/(sign*v1)
        x=point(x-dx)
        if abs(dx)<radius*arb('1e-100'):break
    # Certified opposite signs at binary points; monotone branch follows Rolle.
    eps=radius*arb(2)**-70
    lo,hi=point(x-eps),point(x+eps)
    lv=sign*f.jet(lo)[0]-f.target;hv=sign*f.jet(hi)[0]-f.target
    assert (lv>0 and hv<0) or (lv<0 and hv>0),(f.q,side,str(lv),str(hv))
    return arb(lo.mid(),abs(hi-lo).upper()),lo,hi

def base_prediction(lam,p,q,pp,qq,D):
    f=Trace(p,q,lam)
    # target well value to leading order; top inverse branch
    target=2*arb(lam)**q*(arb.pi()*D*q/qq).cos()+2
    ev=f.zeros_float(1)[0]
    x=arb(str(ev))
    # first move to parent phase-union edge then the near-edge target
    for t in (f.target,target):
        for _ in range(30):
            v,v1,_=f.jet(x);step=(v-t)/v1;x=point(x-step)
            if abs(step)<arb('1e-200'):break
    pd=abs(f.jet(x)[1]);s=arb(1)
    for i in range(1,D):s*=abs(2*(arb.pi()*i*q/qq).sin())
    w=2/(pd*s*s*arb(lam)**(q*(D-1)))
    return dict(logw=str(w.log()),E=str(x),Pprime=str(pd),collapse_target='[0.95,1.10]')

def measure(lam,p,q,A,Ds):
    prevp,prevq=(5,8) if q==13 else (8,13)
    pp,qq=p*A+prevp,q*A+prevq
    f=Trace(pp,qq,lam);z=f.zeros_float(max(Ds)+1)
    parent=Trace(p,q,lam)
    result=[]
    for D in Ds:
        c=newton(f,(z[D-1]+z[D])/2,1)
        assert arb(str(z[D]))<c<arb(str(z[D-1]))
        val=f.jet(c)[0];sign=1 if val>0 else -1
        assert sign*val>f.target
        # Inner endpoints lie between consecutive zeros of the self-adjoint
        # theta=1/(4q), k=pi/2 fibre polynomial. Certified inertia and opposite
        # derivative signs fix the unique Rolle extremum/monotone edge branches.
        il=arb(str(z[D]))+arb('1e-10');ih=arb(str(z[D-1]))-arb('1e-10')
        assert il<c<ih
        assert certified_above(pp,qq,lam,il,1,4*qq,1)==D
        assert certified_above(pp,qq,lam,ih,1,4*qq,1)==D
        dl=f.jet(il)[1];dh=f.jet(ih)[1]
        assert (dl>0 and dh<0) or (dl<0 and dh>0)
        _,ll,lh=find_edge(f,c,sign,-1)
        _,rl,rh=find_edge(f,c,sign,1)
        w=arb((rl-lh).mid(),abs((rh-ll)-(rl-lh)).upper())
        assert w>0
        pd=abs(parent.jet(c)[1]);s=arb(1)
        for i in range(1,D):s*=abs(2*(arb.pi()*i*q/qq).sin())
        collapse=w*pd*s*s*arb(lam)**(q*(D-1))/2
        L=arb(lam).log();xn=2*arb(qq).log()/(q*L)
        counts=[certified_above(pp,qq,lam,c,*args) for args in [(0,1,0),(1,4*qq,1),(1,7,2)]]
        assert counts==[D,D,D],counts
        row=dict(lam=lam,p=p,q=q,A=A,pp=pp,qq=qq,D=D,logw=str(w.log()),width=str(w),centre=str(c),collapse=str(collapse),x=str(xn),R=str(-w.log()/(L*q*D)),counts=counts,edge_signs_certified=True)
        result.append(row)
        print(json.dumps({k:row[k] for k in ('lam','q','A','D','logw','collapse','counts')}),flush=True)
    return result

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='predict':
        pred=[]
        for A in (20,40):
            for D in (2,3):pred.append(dict(lam=5,q=21,A=A,D=D,**base_prediction(5,13,21,13*A+8,21*A+13,D)))
        (OUT/'preregistered_base.json').write_text(json.dumps(pred,indent=2))
        print(json.dumps(pred,indent=2))
    elif mode=='measure':
        lam,p,q,A=map(int,sys.argv[2:6]);Ds=list(map(int,sys.argv[6:]))
        res=measure(lam,p,q,A,Ds)
        (OUT/f'independent_{lam}_{q}_{A}.json').write_text(json.dumps(res,indent=2))
