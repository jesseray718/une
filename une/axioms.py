import time
def check_function(fn,*a,**k):
    if not callable(fn):
        raise TypeError("not callable")
    t0=time.time()
    r=fn(*a,**k)
    t=time.time()-t0
    if not isinstance(r,(int,float)):
        raise TypeError("result must be numeric")
    if t<=0:
        t=1e-9
    eta=r/t
    if eta<=0:
        raise AssertionError("η<=0")
    return {"result":r,"time":t,"eta":eta}
