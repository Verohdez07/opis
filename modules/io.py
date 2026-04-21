import tempfile
import os
import json


def load_data(file):
    from obspy import read

    # obspy necesita archivo en disco, no un buffer de streamlit
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sac") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
        
    try:
        st = read(tmp_path)
    finally:
        os.remove(tmp_path)

    tr = st[0]
    return {
        "time": tr.times(),
        "amplitude": tr.data.astype(float),
        "sampling_rate": tr.stats.sampling_rate,
        "station": tr.stats.station,
        "channel": tr.stats.channel,
        "network": tr.stats.network,
        "starttime": tr.stats.starttime,
        "sac": tr.stats.get("sac", {}),
        "response_removed": False,
    }


def read_pz_files(station, base_path="data/pz"):
    filename = f"{station}.PZ"
    filepath = os.path.join(base_path, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró archivo PZ para la estación {station}")

    poles = []
    zeros = []
    constant = None

    with open(filepath, "r") as f:
        lines = f.readlines()

    mode = None

    for line in lines:
        raw_line = line.strip()
        line = raw_line.lower()

        if not line or line.startswith("*"):
            continue

        if "zeros" in line:
            mode = "zeros"
            continue
        elif "poles" in line:
            mode = "poles"
            continue
        elif "constant" in line:
            constant = float(raw_line.split()[-1])
            continue

        parts = raw_line.split()

        if mode == "zeros":
            zeros.append(complex(float(parts[0]), float(parts[1])))

        elif mode == "poles":
            poles.append(complex(float(parts[0]), float(parts[1])))

    paz = {
        "poles": poles,
        "zeros": zeros,
        "gain": 1.0,
        "sensitivity": constant
    }

    return paz


def save_picks(station, starttime, picks, out_dir="data"):
    os.makedirs(out_dir, exist_ok=True)
    fecha = starttime.strftime("%Y%m%d_%H%M%S")
    filename = f"{station}_{fecha}_picks.json"
    filepath = os.path.join(out_dir, filename)

    payload = {
        "station": station,
        "starttime": starttime.isoformat(),
        "picks": {
            "P": picks["P"],
            "S": picks["S"]
        }
    }

    with open(filepath, "w") as f:
        json.dump(payload, f, indent=2)

    return filepath