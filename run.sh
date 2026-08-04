#!/bin/sh
export UNE_ROOT=/data/data/com.termux/files/home/une
python3 - <<'PY'
import sys,os,importlib
sys.path.insert(0,os.path.join(os.environ['UNE_ROOT'],'src'))
sys.path.insert(0,os.path.join(os.environ['UNE_ROOT']))
from une.axioms import check_function
m=importlib.import_module('compute_joules')
res=check_function(m.sample,100.0)
print(res)
PY
