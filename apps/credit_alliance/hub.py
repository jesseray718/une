from une.une_atomic_library import cooperation_efficiency as f, unified_effective_power as p, unified_power_acceleration as a

class H:
    def __init__(self, hid, n=50): self.hid, self.n, self.d = hid, n, {}
    def add(self, nid, v, c=1.0, h=0.0, t="work"): 
        self.d.setdefault(nid, {"v":0,"c":1,"h":0,"hist":[]})["v"]+=v; self.d[nid]["c"]=max(.5,min(1,c)); self.d[nid]["h"]+=h; self.d[nid]["hist"].append((t,v))
    def s(self, nid): d=self.d.get(nid,{"v":0,"c":1,"h":0}); return (d["v"]*d["c"]*(1+d["h"]*.5))*f(len(self.d)or 1)
    def role(self, nid): return ["support","core","high"][min(2,int(self.s(nid)//80))]
    def tier(self, nid): return ["Bronze","Silver","Gold","Platinum"][min(3,int(self.s(nid)//60))]
    def pay(self, nid, pool): return round((self.s(nid)/max(sum(map(self.s,self.d)),1))*pool,2)
    def eff(self): return p(sum(map(self.s,self.d)),86400,len(self.d)) if self.d else 0
    def accel(self,e=5): return a(sum(map(self.s,self.d)),86400,len(self.d),epochs=e) if self.d else 0
    def game(self,nid): 
        coop=f(len(self.d)or 1); return {"stable":coop>2.8,"pay_coop":self.s(nid)*coop,"pay_defect":self.s(nid)*1.7,"strat":"cooperate" if coop>3 else "restructure"}
