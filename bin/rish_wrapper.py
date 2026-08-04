#!/data/data/com.termux/files/usr/bin/python3
import subprocess, sys, json, re

_last_good = {}

def rish_run(cmd, timeout=5):
    try:
        proc = subprocess.run(
            ["rish", "-c", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode == 0, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return False, "", "Error: 'rish' not found."
    except subprocess.TimeoutExpired:
        return False, "", "Error: rish timed out."
    except Exception as e:
        return False, "", str(e)

def parse_dumpsys_battery(output):
    data = {}
    curr_match = re.search(r'current\s+now:\s*(-?\d+)', output)
    if not curr_match:
        curr_match = re.search(r'current_avg:\s*(-?\d+)', output)
    if curr_match:
        data['current_uA'] = int(curr_match.group(1))

    volt_match = re.search(r'^\s*voltage:\s*(\d+)', output, re.MULTILINE)
    if volt_match:
        data['voltage_mV'] = int(volt_match.group(1))

    level_match = re.search(r'^\s*level:\s*(\d+)', output, re.MULTILINE)
    if level_match:
        data['level'] = int(level_match.group(1))

    temp_match = re.search(r'^\s*temperature:\s*(\d+)', output, re.MULTILINE)
    if temp_match:
        data['temp_dC'] = int(temp_match.group(1))

    return data if data else None

def get_battery_telemetry():
    global _last_good
    success, output, err = rish_run("dumpsys battery")
    if not success:
        return _last_good if _last_good else {"error": "dumpsys failed", "details": err}

    parsed = parse_dumpsys_battery(output)
    if not parsed:
        return _last_good if _last_good else {"error": "Could not parse dumpsys"}

    # Merge with last good (fill gaps from missed fields)
    merged = dict(_last_good)
    merged.update(parsed)
    _last_good = merged

    if 'current_uA' in merged and 'voltage_mV' in merged:
        v_volts = merged['voltage_mV'] / 1000.0
        i_amps = merged['current_uA'] / 1e6
        merged['power_watts'] = v_volts * i_amps

    try:
        merged['timestamp'] = subprocess.check_output(
            ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]
        ).decode().strip()
    except:
        merged['timestamp'] = "unknown"

    return merged

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ok, out, err = rish_run(sys.argv[1])
        print(json.dumps({"ok": ok, "out": out, "err": err}))
    else:
        data = get_battery_telemetry()
        print(json.dumps(data, indent=2))
