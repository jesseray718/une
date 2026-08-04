def best_heat(k1=200.0,k2=1.0,T_total=0.01,A=0.01,deltaT=50.0,min_thickness=1e-6):
    a=1.0/k1; b=1.0/k2
    if b> a:
        t2 = min_thickness
        t1 = max(T_total - t2, min_thickness)
    else:
        t1 = min_thickness
        t2 = max(T_total - t1, min_thickness)
    denom = t1/k1 + t2/k2
    return float(A*deltaT/denom)
