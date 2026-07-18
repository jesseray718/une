import hashlib, time, json
from une.une_atomic_library import mass_equivalent

class JouleLedger:
    def __init__(self): self.chain = [{"index":0,"joules":0,"data":{},"prev":"0"*64,"hash":self._h(0,0,{}, "0"*64)}]
    def _h(self,i,j,d,p): return hashlib.sha256(f"{i}{j}{json.dumps(d,sort_keys=True)}{p}".encode()).hexdigest()
    def add(self, joules: float, data: dict):
        last = self.chain[-1]; i = len(self.chain)
        h = self._h(i, joules, data, last["hash"])
        block = {"index":i,"joules":joules,"data":data,"prev":last["hash"],"hash":h,"mass_eq":round(mass_equivalent(joules), 12)}
        self.chain.append(block); return block
    def verify(self): 
        for i in range(1,len(self.chain)):
            if self.chain[i]["prev"] != self.chain[i-1]["hash"]: return False
        return True
    def total_joules(self): return sum(b["joules"] for b in self.chain)
