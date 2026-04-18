import streamlit as st

from modules.io import load_data
from modules.plotting import plot_waveform, plot_spectrum, plot_spectrogram, plot_epicenter_map

st.set_page_config(page_title="Opis", layout="wide")
st.title("Opis - Analisis sismico")
st.divider()

if "data" not in st.session_state:
    st.session_state.data = None

with st.expander("Cargar archivo", expanded=True):
    uploaded = st.file_uploader("SAC", type=["sac"])
    if uploaded is not None:
        try:
            st.session_state.data = load_data(uploaded)
            st.success("Archivo cargado")
        except Exception as e:
            st.error(f"Error: {e}")

data = st.session_state.data

col_left, col_right = st.columns([3, 1], gap="medium")

with col_left:
    st.plotly_chart(plot_waveform(data), use_container_width=True)

    col_spec, col_specgram = st.columns(2, gap="small")
    with col_spec:
        st.plotly_chart(plot_spectrum(data), use_container_width=True)
    with col_specgram:
        st.plotly_chart(plot_spectrogram(data), use_container_width=True)

with col_right:
    st.subheader("Acciones")

    if st.button("Quitar respuesta instrumental", use_container_width=True):
        pass  # TODO

    if st.button("Obtener magnitud", use_container_width=True):
        pass  # TODO

    if st.button("Guardar picks P y S", use_container_width=True):
        pass  # TODO

    st.divider()

    st.subheader("Epicentro")
    lat = st.number_input("Latitud", value=0.0, step=0.1, format="%.2f")
    lon = st.number_input("Longitud", value=0.0, step=0.1, format="%.2f")
    st.plotly_chart(plot_epicenter_map(lat, lon), use_container_width=True)

    st.divider()

    st.subheader("Parametros")
    vp = st.slider("Vp (km/s)", min_value=1.0, max_value=10.0, value=6.0, step=0.1)
    t0 = st.slider("T0 (s)", min_value=0.0, max_value=120.0, value=0.0, step=0.5)
