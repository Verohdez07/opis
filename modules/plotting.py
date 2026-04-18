import numpy as np
import plotly.graph_objects as go


def plot_waveform(data, p_pick=None, s_pick=None):
    fig = go.Figure()

    if data is not None:
        fig.add_trace(go.Scatter(x=data["time"], y=data["amplitude"],
                                 mode="lines", line=dict(color="#2196F3", width=1)))
        if p_pick is not None:
            fig.add_vline(x=p_pick, line_color="#4CAF50", line_dash="dash",
                          annotation_text="P", annotation_font_color="#4CAF50")
        if s_pick is not None:
            fig.add_vline(x=s_pick, line_color="#F44336", line_dash="dash",
                          annotation_text="S", annotation_font_color="#F44336")

    fig.update_layout(title="Forma de onda", xaxis_title="Tiempo (s)",
                      yaxis_title="Amplitud", template="plotly_dark",
                      height=350, margin=dict(l=50, r=20, t=40, b=40))
    return fig


def plot_spectrum(data):
    fig = go.Figure()

    if data is not None:
        n = len(data["amplitude"])
        freqs = np.fft.rfftfreq(n, d=1.0 / data["sampling_rate"])
        amp = np.abs(np.fft.rfft(data["amplitude"])) / n
        fig.add_trace(go.Scatter(x=freqs, y=amp, mode="lines",
                                 line=dict(color="#9C27B0", width=1.5)))

    fig.update_layout(title="Espectro", xaxis_title="Frecuencia (Hz)",
                      yaxis_title="Amplitud", xaxis_type="log", yaxis_type="log",
                      template="plotly_dark", height=280,
                      margin=dict(l=50, r=20, t=40, b=40))
    return fig


def plot_spectrogram(data):
    fig = go.Figure()

    fig.update_layout(title="Otra figura", xaxis_title="Tiempo (s)",
                      yaxis_title="Frecuencia (Hz)", template="plotly_dark",
                      height=280, margin=dict(l=50, r=20, t=40, b=40))
    return fig


def plot_epicenter_map(lat=0.0, lon=0.0):
    fig = go.Figure(go.Scattergeo(
        lat=[lat], lon=[lon],
        mode="markers",
        marker=dict(size=12, color="red", symbol="star"),
    ))
    fig.update_geos(
        showland=True, landcolor="#2d2d2d",
        showocean=True, oceancolor="#1a3a5c",
        showcountries=True, countrycolor="#555",
        projection_type="natural earth",
        center=dict(lat=lat, lon=lon),
        lataxis_range=[lat - 10, lat + 10],
        lonaxis_range=[lon - 10, lon + 10],
    )
    fig.update_layout(template="plotly_dark", height=280,
                      margin=dict(l=0, r=0, t=10, b=0))
    return fig
