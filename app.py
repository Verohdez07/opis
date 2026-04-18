import streamlit as st

from modules.io import load_data, read_pz_files
from modules.plotting import plot_waveform, plot_epicenter_map
from modules.signal import remove_response_from_dict

st.set_page_config(page_title="Opis", layout="wide")
st.title("Opis - Analisis sismico")
st.divider()

if "data" not in st.session_state:
    st.session_state.data = None

with st.expander("Cargar archivo", expanded=True):
    uploaded_files = st.file_uploader("SAC", type=["sac"],accept_multiple_files=True)
    if uploaded_files is not None:
        component=[]
        for file in uploaded_files:
            try:
                component.append(load_data(file))
                st.success("Archivo cargado")
            except Exception as e:
                st.error(f"Error: {e}")
        st.session_state.data = component

data = st.session_state.data
# print(f"La variable data es {data}")
scale_mode = st.toggle("Escala normalizada", value=True)
col_left, col_right = st.columns([2, 1], gap="medium")

with col_left:
    if data:
        for comp in data:
            channel = comp["channel"]
            st.plotly_chart(
                plot_waveform(comp,scale_mode=scale_mode),
                width="stretch",
                key=f"wave_{channel}"
            )

with col_right:
    st.subheader("Acciones")

    if st.button("Quitar respuesta instrumental"):
        data_pz = read_pz_files(data[0]['station'])
        print(f"data_pz es : {data_pz}")
        for i in range(len(data)):
            data[i] = remove_response_from_dict(data[i], data_pz)
            
        print(f"Esta es data {data}")
        st.session_state.data = data
        st.success("Respuesta instrumental removida")

    if st.button("Obtener magnitud", width="stretch"):
        pass  # TODO

    if st.button("Guardar picks P y S", width="stretch"):
        pass  # TODO

    st.divider()

    st.subheader("Epicentro")

    if data and len(data) > 0:
        latitud = data[0]['sac']['stla']
        longitud = data[0]['sac']['stlo']

        lat = st.number_input("Latitud", value=float(latitud), step=0.1, format="%.4f")
        lon = st.number_input("Longitud", value=float(longitud), step=0.1, format="%.4f")

        st.plotly_chart(plot_epicenter_map(lat, lon), width="stretch")

    else:
        st.info("Carga archivos SAC para mostrar el epicentro")

    st.divider()

    st.subheader("Parametros")
    vp = st.slider("Vp (km/s)", min_value=1.0, max_value=10.0, value=6.0, step=0.1)
    t0 = st.slider("T0 (s)", min_value=0.0, max_value=120.0, value=0.0, step=0.5)
