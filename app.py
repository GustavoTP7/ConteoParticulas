import streamlit as st
import pandas as pd

# -----------------------------
# Estado inicial
# -----------------------------
if "registro_libres" not in st.session_state:
    st.session_state.registro_libres = pd.DataFrame(columns=["Campo", "Mineral", "Cantidad"])

if "registro_mixtos" not in st.session_state:
    st.session_state.registro_mixtos = pd.DataFrame()

if "campo_actual" not in st.session_state:
    st.session_state.campo_actual = 1

if "mixto_widgets" not in st.session_state:
    st.session_state.mixto_widgets = {}

# -----------------------------
# Layout principal
# -----------------------------
st.set_page_config(layout="wide")

col_barra, col_tabla = st.columns([1, 2])

# =====================================================
# BARRA LATERAL — REGISTRO
# =====================================================
with col_barra:
    st.header("Registro")

    # ---------- LIBRES ----------
    st.subheader("Partículas libres")

    mineral = st.text_input("Mineral")
    cantidad = st.number_input("Cantidad", min_value=0, step=1)

    if st.button("Agregar libre"):
        if mineral and cantidad > 0:
            nueva = pd.DataFrame([{
                "Campo": st.session_state.campo_actual,
                "Mineral": mineral.capitalize(),
                "Cantidad": cantidad
            }])

            st.session_state.registro_libres = pd.concat(
                [st.session_state.registro_libres, nueva],
                ignore_index=True
            )

            st.session_state.campo_actual += 1
            st.success("Libre agregado")
        else:
            st.warning("Datos inválidos")

    st.divider()

    # ---------- MIXTOS ----------
    st.subheader("Partículas mixtas")

    combinacion = st.text_input("Combinación (ej: ef/py)")

    if st.button("Generar campos"):
        if "/" in combinacion:
            minerales = [m.strip() for m in combinacion.lower().split("/")]
            st.session_state.mixto_widgets = {
                m: {"area": 0.0, "peri": 0.0}
                for m in minerales[:-1]
            }
        else:
            st.warning("Formato inválido")

    # Inputs dinámicos
    total_area = 0
    total_peri = 0

    for m in st.session_state.mixto_widgets:
        a = st.number_input(f"{m} Area", 0.0, 100.0, key=f"a_{m}")
        p = st.number_input(f"{m} Perímetro", 0.0, 100.0, key=f"p_{m}")

        st.session_state.mixto_widgets[m]["area"] = a
        st.session_state.mixto_widgets[m]["peri"] = p

        total_area += a
        total_peri += p

    if st.button("Guardar mixto"):
        if combinacion and st.session_state.mixto_widgets:
            minerales = combinacion.lower().split("/")
            ultimo = minerales[-1]

            if total_area <= 100 and total_peri <= 100:
                fila = {
                    "Campo": st.session_state.campo_actual,
                    "Cantidad": 1,
                    "Combinación": combinacion.lower()
                }

                for m, vals in st.session_state.mixto_widgets.items():
                    fila[f"{m}_Area"] = vals["area"]
                    fila[f"{m}_Perim"] = vals["peri"]

                fila[f"{ultimo}_Area"] = 100 - total_area
                fila[f"{ultimo}_Perim"] = 100 - total_peri

                st.session_state.registro_mixtos = pd.concat(
                    [st.session_state.registro_mixtos, pd.DataFrame([fila])],
                    ignore_index=True
                )

                st.session_state.campo_actual += 1
                st.session_state.mixto_widgets = {}

                st.success("Mixto guardado")
            else:
                st.error("Totales exceden 100%")
        else:
            st.warning("Primero genere los campos")

# =====================================================
# PANEL GRANDE — TABLAS
# =====================================================
with col_tabla:
    st.header("Resumen")

    # ---------- LIBRES ----------
    st.subheader("Libres")

    df_lib = st.session_state.registro_libres

    if not df_lib.empty:
        total = df_lib["Cantidad"].sum()
        total_row = pd.DataFrame([{
            "Campo": "TOTAL",
            "Mineral": "",
            "Cantidad": total
        }])

        st.dataframe(pd.concat([df_lib, total_row], ignore_index=True))
    else:
        st.info("No hay libres")

    # ---------- MIXTOS ----------
    st.subheader("Mixtos")

    df_mix = st.session_state.registro_mixtos

    if not df_mix.empty:
        total_mix = len(df_mix)
        total_row = pd.DataFrame([{"Campo": "TOTAL", "Cantidad": total_mix}])

        st.dataframe(pd.concat([df_mix, total_row], ignore_index=True))
    else:
        st.info("No hay mixtos")
