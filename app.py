import streamlit as st

from modules.io import load_data, read_pz_files, save_picks
from modules.plotting import plot_waveform, plot_epicenter_map
from modules.signal import remove_response_from_dict

st.set_page_config(page_title="Opis", layout="wide")
st.title("Opis - Analisis sismico")
st.divider()

if "data" not in st.session_state:
    st.session_state.data = None
if "loaded_files" not in st.session_state:
    st.session_state.loaded_files = []
if "picks" not in st.session_state:
    st.session_state.picks = {"P": None, "S": None}

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
        p_pick = st.session_state.picks["P"]
        s_pick = st.session_state.picks["S"]
        for comp in data:
            channel = comp["channel"]
            st.plotly_chart(
                plot_waveform(comp, p_pick=p_pick, s_pick=s_pick),
                width="stretch",
                key=f"wave_{channel}"
            )

with col_right:
    st.subheader("Acciones")

    if st.button("Quitar respuesta instrumental", disabled=no_data, use_container_width=True):
        data_pz = read_pz_files(data[0]['station'])
        for i in range(len(data)):
            data[i] = remove_response_from_dict(data[i], data_pz)
        st.session_state.data = data
        st.rerun()

    if st.button("Guardar picks P y S", disabled=no_data, use_container_width=True):
        picks = st.session_state.picks
        if picks["P"] is None and picks["S"] is None:
            st.warning("No hay picks para guardar.")
        else:
            station = data[0]["station"]
            starttime = data[0]["starttime"]
            filepath = save_picks(station, starttime, picks)
            st.success(f"Picks guardados en: {filepath}")

    if st.button("Calcular el epicentro", disabled=no_data, use_container_width=True):
        pass  # TODO

    if no_data:
        st.caption("Carga archivos SAC para habilitar las acciones.")

    st.divider()

    st.subheader("Picks manuales")

    if data:
        from datetime import timedelta

        starttime = data[0]["starttime"]
        base_time = starttime.datetime  # datetime UTC de inicio

        st.caption(f"Inicio de traza: {base_time.strftime('%H:%M:%S')} UTC")

        def tiempo_a_segundos(tiempo_str, base):
            try:
                partes = tiempo_str.strip().split(":")
                h = int(partes[0])
                m = int(partes[1])
                s_ms = partes[2].split(".")
                s = int(s_ms[0])
                if len(s_ms) > 1:
                    frac = s_ms[1].ljust(6, "0")[:6]
                    us = int(frac)
                else:
                    us = 0
                t = base.replace(hour=h, minute=m, second=s, microsecond=us)
                delta = (t - base).total_seconds()
                return delta
            except Exception:
                return None

        activar_p = st.checkbox("Fase P", value=st.session_state.picks["P"] is not None)
        if activar_p:
            if st.session_state.picks["P"] is not None:
                t_p = base_time + timedelta(seconds=st.session_state.picks["P"])
                ms_p = t_p.microsecond // 1000
                default_p = t_p.strftime(f"%H:%M:%S.") + f"{ms_p:03d}"
            else:
                default_p = base_time.strftime("%H:%M:%S.000")
            texto_p = st.text_input("Hora P (HH:MM:SS.mmm)", value=default_p, key="input_p")
            segundos_p = tiempo_a_segundos(texto_p, base_time)
            if segundos_p is not None and segundos_p >= 0:
                st.session_state.picks["P"] = segundos_p
            else:
                st.warning("Formato inválido. Usa HH:MM:SS.mmm")
        else:
            st.session_state.picks["P"] = None

        activar_s = st.checkbox("Fase S", value=st.session_state.picks["S"] is not None)
        if activar_s:
            if st.session_state.picks["S"] is not None:
                t_s = base_time + timedelta(seconds=st.session_state.picks["S"])
                ms_s = t_s.microsecond // 1000
                default_s = t_s.strftime(f"%H:%M:%S.") + f"{ms_s:03d}"
            else:
                default_s = base_time.strftime("%H:%M:%S.000")
            texto_s = st.text_input("Hora S (HH:MM:SS.mmm)", value=default_s, key="input_s")
            segundos_s = tiempo_a_segundos(texto_s, base_time)
            if segundos_s is not None and segundos_s >= 0:
                st.session_state.picks["S"] = segundos_s
            else:
                st.warning("Formato inválido. Usa HH:MM:SS.mmm")
        else:
            st.session_state.picks["S"] = None

        if st.session_state.picks["P"] is None and st.session_state.picks["S"] is None:
            st.caption("Activa una fase e ingresa la hora exacta.")
    else:
        st.info("Carga archivos SAC para hacer picks.")

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
