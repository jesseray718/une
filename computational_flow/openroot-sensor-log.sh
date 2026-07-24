#!/data/data/com.termux/files/usr/bin/bash
LOGFILE="/sdcard/openroot/sensors/flow_temp_shaft.csv"
mkdir -p "$(dirname "$LOGFILE")"

echo "timestamp,air_flow_m3min,deltaT_hot_C,deltaT_cold_C,shaft_rpm,compute_eta" >> "$LOGFILE"

while true; do
    ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Air flow (anemometer via GPIO or ultrasonic sensor)
    air_flow=$(grep -oP '\d+\.?\d*' /dev/sensors/air_flow 2>/dev/null || echo "0.5")
    
    # ΔT hot (thermocouple near rocket exhaust)
    delta_hot=$(grep -oP '-?\d+\.?\d*' /dev/sensors/temp_hot 2>/dev/null || echo "45")
    
    # ΔT cold (geothermal probe)
    delta_cold=$(grep -oP '-?\d+\.?\d*' /dev/sensors/temp_cold 2>/dev/null || echo "-15")
    
    # Shaft RPM (optical encoder on Stirling flywheel)
    rpm=$(grep -oP '\d+' /dev/sensors/rpm 2>/dev/null || echo "120")
    
    # Compute eta (from absorber.py metrics)
    eta=$(python3 -c "import json; c=json.load(open('/sdcard/openroot/context_bridge/context.json')); print(c.get('eta',0.42))" 2>/dev/null || echo "0.42")
    
    echo "$ts,$air_flow,$delta_hot,$delta_cold,$rpm,$eta" >> "$LOGFILE"
    sleep 10
done
