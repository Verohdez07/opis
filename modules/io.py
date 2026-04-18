import tempfile
import os


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
    }
