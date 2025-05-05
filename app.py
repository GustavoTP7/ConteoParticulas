
import streamlit as st

st.title("🧪 Análisis de Partículas - Liberación y Mezclas")

modo = st.radio("Selecciona el modo de análisis:", ["Modo Simple", "Modo Doble"])

st.divider()

if modo == "Modo Simple":
    st.subheader("🔹 Modo Simple: Una sola medición por partícula")

    nombre = st.text_input("Nombre del componente (ej: CpCu)")
    num_particulas = st.number_input("Cantidad de partículas", min_value=1, step=1)
    total_particulas = st.number_input("Total de partículas analizadas", min_value=1, step=1)

    datos = []
    st.markdown("### Ingresa los datos por partícula (Largo y Alto)")
    for i in range(int(num_particulas)):
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input(f"Largo partícula {i+1}", key=f"L_{i}")
        with col2:
            H = st.number_input(f"Alto partícula {i+1}", key=f"H_{i}")
        datos.append((L, H))

    if st.button("Calcular"):
        SL = SJ = AS = AD = 0
        for L, H in datos:
            J = 100 - 10 * L
            K = 100 - 10 * H
            D = J * K
            SL += L * 10
            SJ += J
            AS += L * H * 100
            AD += D

        Q = SL / (SL + SJ)
        R = SJ / (SL + SJ)
        PO = 100 * num_particulas / total_particulas

        G1 = AS / (100 * num_particulas)
        G2 = AD / (100 * num_particulas)

        st.success("✅ Resultados")
        st.write(f"% MIXTO {nombre} = {PO:.2f}%")
        st.write(f"% ABUNDANCIA DE {nombre[:2]} = {Q * PO:.2f}%")
        st.write(f"% ABUNDANCIA DE {nombre[-2:]} = {R * PO:.2f}%")
        st.write(f"GL DE {nombre[:2]} = {G1:.2f}")
        st.write(f"GL DE {nombre[-2:]} = {G2:.2f}")

else:
    st.subheader("🔹 Modo Doble: Dos fases por partícula")

    nombre = st.text_input("Nombre del componente (ej: CpCu)", key="doble_nombre")
    num_particulas = st.number_input("Cantidad de partículas", min_value=1, step=1, key="doble_num")
    total_particulas = st.number_input("Total de partículas analizadas", min_value=1, step=1, key="doble_total")

    datos = []
    st.markdown("### Ingresa los datos por partícula (Fase 1 y Fase 2)")

    for i in range(int(num_particulas)):
        st.markdown(f"Partícula {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            L1 = st.number_input(f"Fase 1 - Largo", key=f"L1_{i}")
            A1 = st.number_input(f"Fase 1 - Alto", key=f"A1_{i}")
        with col2:
            L2 = st.number_input(f"Fase 2 - Largo", key=f"L2_{i}")
            A2 = st.number_input(f"Fase 2 - Alto", key=f"A2_{i}")
        datos.append((L1, A1, L2, A2))

    if st.button("Calcular", key="doble_calc"):
        SL = SA = SJ = AD = S4 = 0
        for L1, A1, L2, A2 in datos:
            S1 = L1 * A1
            S2 = L2 * A2

            SL += L1
            SA += A2
            AD += S2

            J = 100 - (L1 + L2)
            K = 100 - (A1 + A2)
            S3 = J * K
            SJ += J
            S4 += S3

        Q1 = SL / (SL + SA + SJ)
        R1 = SA / (SL + SA + SJ)
        T1 = SJ / (SL + SA + SJ)
        PO = 100 * num_particulas / total_particulas

        G1 = SL / num_particulas
        G2 = AD / (100 * num_particulas)
        G3 = S4 / (100 * num_particulas)

        st.success("✅ Resultados")
        st.write(f"% MIXTO {nombre} = {PO:.2f}%")
        st.write(f"% ABUNDANCIA DE {nombre[0]} = {Q1 * PO:.2f}%")
        st.write(f"% ABUNDANCIA DE {nombre[1]} = {R1 * PO:.2f}%")
        st.write(f"% ABUNDANCIA DE {nombre[2]} = {T1 * PO:.2f}%")
        st.write(f"GL DE {nombre[0]} = {G1:.2f}")
        st.write(f"GL DE {nombre[1]} = {G2:.2f}")
        st.write(f"GL DE {nombre[2]} = {G3:.2f}")
