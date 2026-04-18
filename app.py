import streamlit as st

from modules.io import load_data, read_pz_files
from modules.plotting import plot_waveform, plot_epicenter_map
from modules.signal import remove_response_from_dict

st.set_page_config(page_title="Opis", layout="wide")
st.title("Opis - Analisis sismico")
st.divider()

if "data" not in st.session_state:
    st.session_state.data = None
if "loaded_files" not in st.session_state:
    st.session_state.loaded_files = []

with st.expander("Cargar archivo", expanded=True):
    uploaded_files = st.file_uploader("SAC", type=["sac"], accept_multiple_files=True)
    incoming = [f.name for f in uploaded_files] if uploaded_files else []
    if incoming and incoming != st.session_state.loaded_files:
        component = []
        for file in uploaded_files:
            try:
                component.append(load_data(file))
            except Exception as e:
                st.error(f"Error cargando {file.name}: {e}")
        if component:
            st.session_state.data = component
            st.session_state.loaded_files = incoming
            st.success(f"{len(component)} archivo(s) cargado(s)")

data = st.session_state.data
no_data = not data

col_left, col_right = st.columns([2, 1], gap="medium")

with col_left:
    if data:
        for comp in data:
            channel = comp["channel"]
            st.plotly_chart(
                plot_waveform(comp),
                width="stretch",
                key=f"wave_{channel}"
            )

with col_right:
    st.subheader("Acciones")

    if st.button("Quitar respuesta instrumental", width="stretch", disabled=no_data):
        data_pz = read_pz_files(data[0]['station'])
        for i in range(len(data)):
            data[i] = remove_response_from_dict(data[i], data_pz)
        st.session_state.data = data
        st.rerun()

    if st.button("Obtener magnitud", width="stretch", disabled=no_data):
        pass  # TODO

    if st.button("Guardar picks P y S", width="stretch", disabled=no_data):
        pass  # TODO

    if no_data:
        st.caption("Carga archivos SAC para habilitar las acciones.")

    st.divider()

    st.subheader("Epicentro")

    if data:
        latitud = data[0]['sac']['stla']
        longitud = data[0]['sac']['stlo']

        lat = st.number_input("Latitud", value=float(latitud), step=0.1, format="%.4f")
        lon = st.number_input("Longitud", value=float(longitud), step=0.1, format="%.4f")

        st.plotly_chart(plot_epicenter_map(lat, lon), width="stretch")
    else:
        st.info("Carga archivos SAC para mostrar el epicentro.")

    st.divider()

    st.subheader("Parametros")
    vp = st.slider("Vp (km/s)", min_value=1.0, max_value=10.0, value=6.0, step=0.1)
    t0 = st.slider("T0 (s)", min_value=0.0, max_value=120.0, value=0.0, step=0.5)
