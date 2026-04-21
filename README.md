# Opis

Aplicacion web para el proyecto opis, desarrollada con Streamlit.

Permite cargar archivos SAC, visualizar formas de onda, espectros y ubicar epicentros de forma interactiva.

---

## Requisitos

- Python 3.10 o superior
- obspy
- streamlit
- plotly
- numpy

## Instalacion

```bash
git clone https://github.com/Verohdez07/opis.git
cd opis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

Luego abrir en el navegador: http://localhost:8501

## Estructura

```
opis/
├── app.py              interfaz principal
└── modules/
    ├── io.py           carga de archivos SAC
    ├── plotting.py     graficos con plotly
    ├── picking.py      deteccion de fases P y S
```

## Estado actual

- Carga de archivos SAC via obspy
- Visualizacion de forma de onda, espectro
- Mapa de epicentro con coordenadas manuales
- Picking e inversion pendientes de implementar

## Notas

Los archivos SAC no se suben al repositorio (ver .gitignore).
Para probar la app se necesita un archivo SAC propio.
