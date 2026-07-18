from .une_atomic_library import *
def eval(E,t=3600,N=50,e=5): b=E/t; return {"p":round(unified_effective_power(E,t,N),2),"a":round(unified_power_acceleration(E,t,N,epochs=e),4),"b":round(max(0,1-unified_effective_power(E,t,N)/(b*3)),3),"rec":"↑N/↑fractal" if max(0,1-unified_effective_power(E,t,N)/(b*3))>0.35 else "good"}
