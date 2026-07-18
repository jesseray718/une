def expose_monopoly(extraction_rate: float, human_impact: float):
    return {"exploitation_score": round(extraction_rate * human_impact, 3), "redistribute": extraction_rate > 0.6}

def redistribute_to_commons(monopoly_value: float, ledger):
    joules = monopoly_value * 1000  # convert to joules equivalent
    ledger.add(joules, {"type":"redistribution", "source":"monopoly", "target":"commons"})
    return {"joules_moved": joules, "new_ledger_total": ledger.total_joules()}
