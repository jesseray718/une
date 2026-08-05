import os,sys,math,json
UNE_ROOT=os.environ.get('UNE_ROOT','os.path.expanduser("~") + "/"une')
sys.path.insert(0,os.path.join(UNE_ROOT,'src'))
from permaculture_map import PERMACULTURE_PRINCIPLES
from une.axioms import check_function
def stats_for(principle):
    chain = PERMACULTURE_PRINCIPLES[principle]['chain']
    L = len(chain)
    highest_order_log10 = L * math.log10(L) if L>0 else 0.0
    highest_order_approx = 10**(highest_order_log10 - int(highest_order_log10))
    exponent = int(highest_order_log10)
    return {'principle':principle,'L':L,'highest_order_log10':highest_order_log10,'highest_order_approx_mantissa':highest_order_approx,'highest_order_exponent':exponent}
def build_web():
    nodes = {}
    for p in PERMACULTURE_PRINCIPLES:
        nodes[p]=stats_for(p)
    adj = {}
    for a in nodes:
        adj[a]=[]
        La=nodes[a]['L']
        for b in nodes:
            Lb=nodes[b]['L']
            cond = 'L_a>=L_b' if La>=Lb else 'L_a<L_b'
            adj[a].append({'to':b,'condition':cond})
    return {'nodes':nodes,'edges':adj}
def numeric_summary():
    s=0.0
    for p in PERMACULTURE_PRINCIPLES:
        L=len(PERMACULTURE_PRINCIPLES[p]['chain'])
        if L>0:
            s += L * math.log10(L)
    return float(s)
def write_outputs(outdir):
    web=build_web()
    dot_lines=["digraph permaculture_web {","  rankdir=LR;","  node [shape=box];"]
    for p,v in web['nodes'].items():
        lab = p.replace('"','\\"') + "\\nL=" + str(v['L']) + "\\n10^" + str(int(v['highest_order_log10']))
        dot_lines.append('  "%s" [label="%s"];' % (p,lab))
    for a,edges in web['edges'].items():
        for e in edges:
            dot_lines.append('  "%s" -> "%s" [label="%s"];' % (a,e['to'],e['condition']))
    dot_lines.append('}')
    os.makedirs(outdir,exist_ok=True)
    dotp=os.path.join(outdir,'permaculture_web.dot')
    jpath=os.path.join(outdir,'permaculture_web.json')
    with open(dotp,'w') as f:
        f.write("\n".join(dot_lines))
    with open(jpath,'w') as f:
        json.dump(web,f,indent=2)
    return dotp,jpath
if __name__=='__main__':
    outdir=os.path.join(UNE_ROOT,'session_seeds')
    dotp,jpath = write_outputs(outdir)
    res = check_function(numeric_summary)
    print(res)
    print(dotp)
    print(jpath)
