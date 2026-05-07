import streamlit as st
import pandas as pd

st.set_page_config(page_title="Método Cánepa - Automatizado", layout="wide")

# --- PERSISTENCIA DE DATOS ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['Campo', 'Mezcla', 'Fase', 'Area', 'Perim', 'SxD'])

# --- SIDEBAR: REGISTRO RÁPIDO ---
with st.sidebar:
    st.title("📥 Registro Manual")
    campo = st.number_input("Partícula #", min_value=1, step=1)
    mezcla = st.text_input("Mezcla (Ej: GGs/ef)").lower()
    
    # Factor de Volumen (El 1.44 de tu hoja)
    factor_vol = st.number_input("Factor % Vol (Ratio)", value=1.44, format="%.2f")
    
    if mezcla and '/' in mezcla:
        fases = mezcla.split('/')
        with st.form("form_registro"):
            f1 = fases[0]
            st.markdown(f"**Fase A: {f1}**")
            a1 = st.number_input(f"Área {f1}", min_value=0.0)
            p1 = st.number_input(f"Perímetro {f1}", min_value=0.0)
            
            # Complemento automático (Lógica Cánepa)
            f2 = fases[1]
            a2 = 100.0 - a1
            p2 = 100.0 - p1
            
            if st.form_submit_button("💾 Guardar Partícula"):
                nuevos_datos = [
                    {'Campo': campo, 'Mezcla': mezcla, 'Fase': f1.upper(), 'Area': a1, 'Perim': p1, 'SxD': a1*p1},
                    {'Campo': campo, 'Mezcla': mezcla, 'Fase': f2.upper(), 'Area': a2, 'Perim': p2, 'SxD': a2*p2}
                ]
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame(nuevos_datos)], ignore_index=True)
                st.toast("Registrado")

    if st.button("🗑️ Limpiar Base de Datos"):
        st.session_state.db = pd.DataFrame(columns=['Campo', 'Mezcla', 'Fase', 'Area', 'Perim', 'SxD'])
        st.rerun()

# --- ÁREA PRINCIPAL: CÁLCULOS SEGÚN TU HOJA ---
st.title("📊 Reporte de Resultados - Lógica Cánepa")

if st.session_state.db.empty:
    st.info("Ingresa datos en el panel izquierdo.")
else:
    for m_id in st.session_state.db['Mezcla'].unique():
        st.header(f"Mezcla: {m_id.upper()}")
        df_m = st.session_state.db[st.session_state.db['Mezcla'] == m_id]
        
        # 1. Suma de todas las áreas (Paso 1 de tu hoja: 140 + 460 = 600)
        area_total_sistema = df_m['Area'].sum()
        
        resumen_calculado = []
        for fase_nom in m_id.split('/'):
            fase_up = fase_nom.upper()
            df_fase = df_m[df_m['Fase'] == fase_up]
            
            s_area = df_fase['Area'].sum()
            s_sxd = df_fase['SxD'].sum()
            
            # 2. Porcentaje de Área (Paso 2: 140 -> 23.3%)
            p_area = (s_area / area_total_sistema) if area_total_sistema > 0 else 0
            
            # 3. % Volumen (Paso 3: 23.3% * 1.44 = 0.336)
            p_vol = p_area * factor_vol
            
            # 4. G.L Final (Suma SxD / Area Total Sistema)
            gl_final = s_sxd / area_total_sistema if area_total_sistema > 0 else 0
            
            resumen_calculado.append({
                'Especie': fase_up,
                'Suma Áreas': s_area,
                '% Área Rel.': f"{p_area*100:.1f}%",
                '% Vol Calc': round(p_vol, 3),
                'Suma SxD': s_sxd,
                'G.L. (SxD/SumArea)': round(gl_final, 2)
            })
            
        st.table(pd.DataFrame(resumen_calculado))
        st.write(f"**Suma Total de Áreas de la Mezcla:** {area_total_sistema}")
        st.divider()

    st.subheader("Historial de Partículas")
    st.dataframe(st.session_state.db)
