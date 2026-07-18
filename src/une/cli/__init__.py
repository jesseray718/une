import argparse,sys
from ..dense import eval
from ..une_atomic_library import *
from apps.credit_alliance.hub import H

def main():
    p=argparse.ArgumentParser(); p.add_argument("cmd"); p.add_argument("--E",type=float,default=1000); p.add_argument("--N",type=int,default=50); p.add_argument("--e",type=int,default=5); p.add_argument("--pool",type=float,default=1000)
    a=p.parse_args()
    if a.cmd=="eval": print(eval(a.E,3600,a.N,a.e))
    elif a.cmd=="hub":
        h=H("h1",a.N); [h.add(f"n{i}",50+ i*2, .9, .3) for i in range(a.N)]; print({"eff":round(h.eff(),2),"accel":round(h.accel(a.e),4),"payout0":h.pay("n0",a.pool),"tier0":h.tier("n0"),"game":h.game("n0")})
    elif a.cmd=="game": print("cooperative game theory active — use hub command")
if __name__=="__main__": main()
