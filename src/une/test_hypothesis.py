"""Property-based tests with Hypothesis."""
from hypothesis import given, strategies as st
from une.foundation_calc import labor_intensity, efficiency_ratio, time_to_place

@given(ph=st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False),
       vol=st.floats(min_value=0.001, max_value=1e6, allow_nan=False, allow_infinity=False))
def test_labor_intensity_always_non_negative(ph, vol):
    assert labor_intensity(ph, vol) >= 0.0

@given(a=st.floats(min_value=0.001, max_value=1e4, allow_nan=False, allow_infinity=False),
       b=st.floats(min_value=0.001, max_value=1e4, allow_nan=False, allow_infinity=False))
def test_efficiency_ratio_inverse(a, b):
    r1 = efficiency_ratio(a, b)
    r2 = efficiency_ratio(b, a)
    assert abs(r1 * r2 - 1.0) < 1e-6

@given(vol=st.floats(min_value=0.1, max_value=1e4, allow_nan=False, allow_infinity=False),
       rate=st.floats(min_value=0.1, max_value=1e3, allow_nan=False, allow_infinity=False))
def test_time_to_place_roundtrip(vol, rate):
    hours = time_to_place(vol, rate)
    assert abs(hours * rate - vol) < 1e-4
