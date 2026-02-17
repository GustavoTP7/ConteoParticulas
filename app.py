import streamlit as st
import pandas as pd

st.set_page_config(page_title="Registro de Partículas", layout="wide")

# =========================
# Inicialización de sesión
# =========================
if "libres" not in st.session_state:
    st.session_state.libres = []

if "mixtos" not in st.session_state:
    st.session_state.mixtos = []

if "contador_mixtos" not in st.session_state:
    st.session_state.contador_mixtos = {}

# =========================
# Título
# =========================
st.title("📋 Registro de Partículas")

# =====================================================
# REGISTRO — LIBRES
# =====================================================
st.header("➕ Registrar Partículas Libres")

col1, col2 = st.columns(2)

with col1:
    mineral = st.text_input("Mineral")

with col2:
    cantidad = st.number_input("Cantidad", min_value=0, step=1)

if st.button("Guardar libre"):

    if mineral and cantidad > 0:
        st.session_state.libres.append({
            "Mineral": mineral,
            "Cantidad": cantidad
        })
        st.success("Libre guardado")

# Mostrar libres
st.subheader("🔹 Libres")

if st.session_state.libres:
    df_libres = pd.DataFrame(st.session_state.libres)
    st.dataframe(df_libres, use_container_width=True)
else:
    st.info("No hay partículas libres")

# =====================================================
# REGISTRO — MIXTOS
# =====================================================
st.header("➕ Registrar Partículas Mixtas")

combo = st.text_input("Combinación (ej: py/ef/ggs)")

if combo:

    minerales = combo.split("/")

    st.write("Ingrese área y perímetro:")

    datos = {}

    for m in minerales:
        colA, colP = st.columns(2)

        with colA:
            area = st.number_input(f"{m} Área", key=f"{m}_area")

        with colP:
            perim = st.number_input(f"{m} Perímetro", key=f"{m}_perim")

        datos[m] = {
            "Area": area,
            "Perimetro": perim
        }

    if st.button("Guardar mixto"):

        fila = {"Combinación": combo}

        for m in datos:
            fila[f"{m}_Area"] = datos[m]["Area"]
            fila[f"{m}_Perim"] = datos[m]["Perimetro"]

        st.session_state.mixtos.append(fila)

        # contador
        st.session_state.contador_mixtos[combo] = (
            st.session_state.contador_mixtos.get(combo, 0) + 1
        )

        st.success("Mixto guardado")

# =====================================================
# MOSTRAR MIXTOS — SEPARADOS
# =====================================================
st.header("🔸 Mixtos")

if st.session_state.mixtos:

    df = pd.DataFrame(st.session_state.mixtos)

    for combinacion in df["Combinación"].unique():

        st.subheader(f"Combinación: {combinacion}")

        df_filtrado = df[df["Combinación"] == combinacion]

        st.dataframe(df_filtrado, use_container_width=True)

else:
    st.info("No hay partículas mixtas")

# =====================================================
# CONTEO MIXTOS
# =====================================================
st.header("📊 Conteo de Mixtos")

if st.session_state.contador_mixtos:

    df_count = pd.DataFrame([
        {"Combinación": k, "Cantidad": v}
        for k, v in st.session_state.contador_mixtos.items()
    ])

    st.dataframe(df_count, use_container_width=True)

else:
    st.info("Sin conteo aún")

# =====================================================
# LIMPIAR DATOS
# =====================================================
st.header("⚙ Opciones")

if st.button("Reiniciar todo"):
    st.session_state.libres = []
    st.session_state.mixtos = []
    st.session_state.contador_mixtos = {}
    st.success("Datos reiniciados")
