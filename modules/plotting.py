import numpy as np
import plotly.graph_objects as go


def plot_waveform(data, p_pick=None, s_pick=None, scale_mode=True):
    fig = go.Figure()

    y_label = "Amplitud"

    if data is not None:
        amp = data["amplitude"]

        if scale_mode:
            max_amp = np.max(np.abs(amp))
            if max_amp > 0:
                amp = amp / max_amp
            y_label = "Amplitud (normalizada)"
        else:
            y_label = "Amplitud (m/s)"

        fig.add_trace(go.Scatter(
            x=data["time"],
            y=amp,
            mode="lines",
            line=dict(color="#2196F3", width=1)
        ))

        if p_pick is not None:
            fig.add_vline(
                x=p_pick,
                line_color="#4CAF50",
                line_dash="dash",
                annotation_text="P",
                annotation_font_color="#4CAF50"
            )

        if s_pick is not None:
            fig.add_vline(
                x=s_pick,
                line_color="#F44336",
                line_dash="dash",
                annotation_text="S",
                annotation_font_color="#F44336"
            )

    fig.update_layout(
        title=f"{data['station']} - {data['channel']}" if data else "Sin datos",
        xaxis_title="Tiempo (s)",
        yaxis_title=y_label,
        template="plotly_dark",
        height=350,
        margin=dict(l=50, r=20, t=40, b=40)
    )

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
