def useful_from_samples(deltaT, shaft_joules, mass=0.05, cp=4184.0, capture_fraction=0.02):
    heat = mass * cp * float(deltaT)
    return float(shaft_joules + heat * capture_fraction)
