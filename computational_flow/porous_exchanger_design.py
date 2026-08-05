#!/usr/bin/env python3
"""
porous_exchanger_design.py  v2 (corrected)
Volumetric wet-media exchanger sizing for AeroCement / OpenRoot
Geometries: STRAIGHT CHANNELS | N-START SPIRAL (Dean, Ito+Dravid) | OPEN BED
Fixes vs v1: coil radius R_HELIX added; true helix path length;
Ito friction + Dravid Nu (published, with validity ranges); NTU uses
true helical wetted area; optimizer finds shortest passive spiral block.
Stdlib only. Termux-safe. Edit constants, run.
"""

import math

# ---------------- EDITABLE CONSTANTS ----------------
Q_AIR    = 0.18      # m3/s design airflow
T_IN     = 35.0      # C air entering block
T_MATRIX = 16.0      # C wet matrix temp
RHO_A    = 1.16
MU_A     = 1.85e-5
CP_A     = 1005.0
K_A      = 0.026
PR       = 0.71

# straight channels
D_CH     = 0.010
PHI      = 0.50
L_CH     = 2.0
FACE_CH  = 0.36

# N-start spiral channels
D_SP     = 0.010     # channel bore diameter (m)
PHI_SP   = 0.45      # open flow-area fraction of face
L_SP     = 2.0       # axial block length (m) -- optimizer also scans this
FACE_SP  = 0.36      # block face area (m2)
PITCH    = 0.080     # axial advance per full turn (m)
R_HELIX  = 0.020     # COIL radius: axis to channel centerline (m)  << NEW
N_START  = 5         # parallel starts (packing choice; physics-neutral)

# spiral optimizer targets
NTU_MIN  = 3.0       # 95% effectiveness floor
L_SCAN_LO, L_SCAN_HI, L_STEP = 0.05, 2.0, 0.01

# open bed
EPS      = 0.30
DP       = 0.005
L_BED    = 0.5
FACE_BED = 9.0

# stack
H_STACK  = 6.0
DT_STACK = 25.0
T_K      = 305.0

# water / soil
R_PORE   = 25e-6
COS_THETA = 0.8
Q_EVAP   = 1000.0
H_FG     = 2.45e6
K_SOIL   = 1.5
SOIL_AREA = 20.0
SOIL_DT  = 10.0
FAN_ETA  = 0.5
# ----------------------------------------------------

def stack_pa():
    return RHO_A * 9.81 * H_STACK * (DT_STACK / T_K)

def channels():
    u = (Q_AIR / FACE_CH) / PHI
    re = RHO_A * u * D_CH / MU_A
    if re < 2300:
        dp = 32.0 * MU_A * L_CH * u / (D_CH ** 2)
        nu, regime = 3.66, "laminar"
    else:
        f = 0.316 * re ** -0.25
        dp = f * (L_CH / D_CH) * 0.5 * RHO_A * u * u
        nu, regime = 0.023 * re ** 0.8 * PR ** 0.4, "turbulent"
    dp += 1.5 * 0.5 * RHO_A * u * u
    h = nu * K_A / D_CH
    a_v = 4.0 * PHI / D_CH
    vol = FACE_CH * L_CH
    ntu = h * a_v * vol / (RHO_A * Q_AIR * CP_A)
    return dict(name="STRAIGHT CHANNELS", u=u, re=re, regime=regime,
                dp=dp, a_v=a_v, vol=vol, ntu=ntu)

def spiral_geom():
    """True helix geometry from coil radius + pitch."""
    b = PITCH / (2.0 * math.pi)
    rc = R_HELIX + (b * b) / R_HELIX          # curvature radius of helix
    stretch = math.sqrt(1.0 + (2.0 * math.pi * R_HELIX / PITCH) ** 2)
    return rc, stretch                         # L_helix = L_axial * stretch

def ito_friction_ratio(de):
    """Ito (1959) laminar curved-pipe friction multiplier, De > \\~13.5."""
    if de <= 13.5:
        return 1.0
    a = 1.729 / de
    core = math.sqrt(1.0 + a) - math.sqrt(a)
    return 0.1033 * math.sqrt(de) * core ** -3

def dravid_nu(de):
    """Dravid (1971) laminar helical Nu, valid 50 < De < 2000."""
    if de < 50.0:
        # gentle blend to straight-pipe value below validity range
        return 3.66 * (1.0 + (de / 50.0) * (0.76 * math.sqrt(50.0)
                       * PR ** 0.175 / 3.66 - 1.0))
    return 0.76 * math.sqrt(de) * PR ** 0.175

def spiral_channels(l_axial=None):
    L = L_SP if l_axial is None else l_axial
    u = (Q_AIR / FACE_SP) / PHI_SP
    re = RHO_A * u * D_SP / MU_A
    rc, stretch = spiral_geom()
    l_helix = L * stretch
    de = re * math.sqrt(D_SP / (2.0 * rc))
    if re < 2300:
        f = (64.0 / re) * ito_friction_ratio(de)
        nu = dravid_nu(de)
        regime = "laminar+Dean (Ito/Dravid)"
    else:
        f = 0.316 * re ** -0.25
        nu = 0.023 * re ** 0.8 * PR ** 0.4
        regime = "turbulent"
    dp = f * (l_helix / D_SP) * 0.5 * RHO_A * u * u
    dp += 1.5 * 0.5 * RHO_A * u * u
    h = nu * K_A / D_SP
    a_v = 4.0 * PHI_SP / D_SP                 # per face-projected volume
    vol = FACE_SP * L
    ntu = h * a_v * vol * stretch / (RHO_A * Q_AIR * CP_A)  # true wetted area
    return dict(name="%d-START SPIRAL" % N_START, u=u, re=re, regime=regime,
                dp=dp, a_v=a_v, vol=vol, ntu=ntu, De=round(de, 1),
                L=L, L_helix=l_helix)

def bed():
    u = Q_AIR / FACE_BED
    visc = 150.0 * MU_A * (1 - EPS) ** 2 / (EPS ** 3 * DP ** 2) * u
    iner = 1.75 * RHO_A * (1 - EPS) / (EPS ** 3 * DP) * u * u
    dp = (visc + iner) * L_BED
    re = RHO_A * u * DP / (MU_A * (1 - EPS))
    nu = 2.0 + 1.1 * (re ** 0.6) * (PR ** (1.0 / 3.0))
    h = nu * K_A / DP
    a_v = 6.0 * (1 - EPS) / DP
    vol = FACE_BED * L_BED
    ntu = h * a_v * vol / (RHO_A * Q_AIR * CP_A)
    return dict(name="OPEN BED", u=u, re=re, regime="Ergun", dp=dp,
                a_v=a_v, vol=vol, ntu=ntu)

def optimize_spiral(avail):
    """Shortest axial length with NTU>=NTU_MIN; flag if passive (dp<=stack)."""
    best_passive, best_any = None, None
    L = L_SCAN_LO
    while L <= L_SCAN_HI + 1e-9:
        g = spiral_channels(L)
        if g["ntu"] >= NTU_MIN:
            if best_any is None:
                best_any = g
            if g["dp"] <= avail and best_passive is None:
                best_passive = g
            if best_passive is not None:
                break
        L += L_STEP
    return best_passive, best_any

def report(g, avail):
    eff = 1.0 - math.exp(-g["ntu"])
    t_out = T_MATRIX + (T_IN - T_MATRIX) * math.exp(-g["ntu"])
    ok = g["dp"] <= avail
    fan_w = 0.0 if ok else Q_AIR * g["dp"] / FAN_ETA
    print("\n== %s ==" % g["name"])
    if "L" in g:
        print(" axial L      : %8.2f m   (helical path %.2f m)"
              % (g["L"], g["L_helix"]))
    print(" a_v          : %8.0f m2/m3" % g["a_v"])
    print(" volume       : %8.2f m3" % g["vol"])
    print(" air velocity : %8.2f m/s  Re=%.0f (%s)"
          % (g["u"], g["re"], g["regime"]))
    if "De" in g:
        print(" Dean number  : %8.1f" % g["De"])
    print(" pressure drop: %8.1f Pa   vs stack %.1f Pa -> %s"
          % (g["dp"], avail, "PASSIVE OK" if ok else "NEEDS FAN"))
    if not ok:
        print(" fan power    : %8.1f W" % fan_w)
    print(" NTU / eff    : %8.2f / %.1f%%" % (g["ntu"], eff * 100))
    print(" T out        : %8.2f C" % t_out)

def water_soil():
    h_cap = 2.0 * 0.072 * COS_THETA / (1000.0 * 9.81 * R_PORE)
    lph = Q_EVAP / H_FG * 3600.0
    q_soil = K_SOIL * SOIL_DT / 0.25 * SOIL_AREA
    print("\n== WATER / SOIL ==")
    print(" capillary rise : %.2f m" % h_cap)
    print(" water use      : %.2f L/h @ %.0f W evap" % (lph, Q_EVAP))
    print(" soil capacity  : approx %.0f W sustained" % q_soil)
    print(" rule: NTU past \\~5 buys nothing but dP; soil interface is the cap")

if __name__ == "__main__":
    avail = stack_pa()
    print("Stack pressure available: %.1f Pa  (H=%.1f m, dT=%.0f K)"
          % (avail, H_STACK, DT_STACK))
    report(channels(), avail)
    report(spiral_channels(), avail)
    report(bed(), avail)
    bp, ba = optimize_spiral(avail)
    print("\n== SPIRAL OPTIMIZER (NTU >= %.1f) ==" % NTU_MIN)
    if bp:
        print(" shortest PASSIVE block:")
        report(bp, avail)
    elif ba:
        print(" no passive solution in scan; shortest meeting NTU:")
        report(ba, avail)
        print(" -> widen FACE_SP (lower velocity) or raise H_STACK to go passive")
    water_soil()
