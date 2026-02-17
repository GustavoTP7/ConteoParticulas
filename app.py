import streamlit as st
import pandas as pd


def mostrar_resumen(libres, mixtos):

    st.header("📋 Resumen de Registro de Partículas")

    # =====================================================
    # 🔵 LIBRES
    # =====================================================

    st.subheader("🔹 Libres")

    if libres:
        df_libres = pd.DataFrame(libres)

        # contador por mineral
        conteo_libres = (
            df_libres.groupby("Mineral")["Cantidad"]
            .sum()
            .reset_index()
        )

        st.markdown("### Conteo de libres")
        st.dataframe(conteo_libres, use_container_width=True)

        st.markdown("### Detalle libres")
        st.dataframe(df_libres, use_container_width=True)

    else:
        st.info("No hay partículas libres registradas.")

    st.divider()

    # =====================================================
    # 🟠 MIXTOS
    # =====================================================

    st.subheader("🔸 Mixtos")

    if mixtos:

        df_mix = pd.DataFrame(mixtos)

        # ===== contador por combinación =====
        conteo_mix = (
            df_mix["Combinación"]
            .value_counts()
            .reset_index()
        )
        conteo_mix.columns = ["Combinación", "Cantidad"]

        st.markdown("### Conteo de mixtos")
        st.dataframe(conteo_mix, use_container_width=True)

        st.divider()

        # ===== tablas separadas por combinación =====
        st.markdown("### Detalle por combinación")

        for comb in df_mix["Combinación"].unique():

            sub_df = df_mix[df_mix["Combinación"] == comb].copy()

            # eliminar columnas vacías → evita NaN
            sub_df = sub_df.dropna(axis=1, how="all")

            st.markdown(f"#### 🔹 {comb}")
            st.dataframe(sub_df, use_container_width=True)

    else:
        st.info("No hay partículas mixtas registradas.")
