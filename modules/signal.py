def remove_response_from_dict(comp, paz):
    from obspy import Trace
    import numpy as np

    tr = Trace(data=comp["amplitude"].astype(np.float64))
    tr.stats.sampling_rate = comp["sampling_rate"]

    tr.simulate(
        paz_remove=paz,
        remove_sensitivity=True,
        pre_filt=[0.04, 0.08, 20, 30]
    )

    comp["amplitude"] = tr.data
    return comp