import numpy as np
import plotly.graph_objects as go
from datetime import timedelta


def plot_waveform(data, p_pick=None, s_pick=None):
    fig = go.Figure()

    if data is not None:
        # Crear eje X con timestamps absolutos
        starttime = data.get("starttime")
        if starttime:
            # Convertir tiempo relativo a datetime absoluto
            base_time = starttime.datetime
            time_abs = [base_time + timedelta(seconds=float(t)) for t in data["time"]]
            x_data = time_abs
            xaxis_title = "Tiempo"
        else:
            x_data = data["time"]
            xaxis_title = "Tiempo (s)"
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=data["amplitude"],
            mode="lines",
            line=dict(color="#2196F3", width=1)
        ))

        if p_pick is not None:
            if starttime:
                p_time = base_time + timedelta(seconds=float(p_pick))
                y_min = float(min(data["amplitude"]))
                y_max = float(max(data["amplitude"]))
                fig.add_trace(go.Scatter(
                    x=[p_time, p_time],
                    y=[y_min, y_max],
                    mode="lines",
                    line=dict(color="#4CAF50", dash="dash", width=1.5),
                    name="P"
                ))
            else:
                fig.add_vline(x=p_pick, line_color="#4CAF50", line_dash="dash",
                              annotation_text="P", annotation_font_color="#4CAF50")
        if s_pick is not None:
            if starttime:
                s_time = base_time + timedelta(seconds=float(s_pick))
                y_min = float(min(data["amplitude"]))
                y_max = float(max(data["amplitude"]))
                fig.add_trace(go.Scatter(
                    x=[s_time, s_time],
                    y=[y_min, y_max],
                    mode="lines",
                    line=dict(color="#F44336", dash="dash", width=1.5),
                    name="S"
                ))
            else:
                fig.add_vline(x=s_pick, line_color="#F44336", line_dash="dash",
                              annotation_text="S", annotation_font_color="#F44336")

        # Determinar etiqueta del eje Y según si se quitó respuesta
        response_removed = data.get("response_removed", False)
        yaxis_title = "Amplitud (mm)" if response_removed else "Cuentas"

    fig.update_layout(
        title=f"{data['station']} - {data['channel']}" if data else "Sin datos",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
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
