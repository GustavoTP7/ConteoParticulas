import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cánepa - Lógica Exacta", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        'Campo', 'Combinación', 'Fase', 'Area', 'Perim', 'SxD', 'Vol_Mezcla'
    ])

# --- SIDEBAR: INGRESO ---
with st.sidebar:
    st.title("📥 Registro")
    campo = st.number_input("Campo", min_value=1, step=1)
    combo = st.text_input("Mezcla (ej: GGs/ef)").lower()
    vol_m = st.number_input("% Vol de la Mezcla", min_value=0.0, format="%.2f")
    
    if combo and '/' in combo:
        minerales = combo.split('/')
        with st.form("form_p"):
            m1 = minerales[0]
            st.markdown(f"**Mineral A: {m1}**")
            a1 = st.number_input(f"Área {m1}", min_value=0.0)
            p1 = st.number_input(f"Perímetro {m1}", min_value=0.0)
            
            # El mineral B es el complemento (Lógica de tu nota)
            m2 = minerales[1]
            a2 = 100.0 - a1
            p2 = 100.0 - p1
            
            if st.form_submit_button("Registrar"):
                # Guardamos ambos minerales de la partícula
                rows = [
                    {'Campo': campo, 'Combinación': combo, 'Fase': m1.upper(), 'Area': a1, 'Perim': p1, 'SxD': a1*p1, 'Vol_Mezcla': vol_m},
                    {'Campo': campo, 'Combinación': combo, 'Fase': m2.upper(), 'Area': a2, 'Perim': p2, 'SxD': a2*p2, 'Vol_Mezcla': vol_m}
                ]
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame(rows)], ignore_index=True)
                st.toast("Guardado")

# --- PRINCIPAL: CÁLCULOS PASO A PASO ---
st.title("📊 Reporte con Lógica de Nota Manuscrita")

if not st.session_state.db.empty:
    df = st.session_state.db
    
    # 1. Agrupamos por Mezcla para los cálculos finales
    for cb in df['Combinación'].unique():
        st.subheader(f"Análisis Mezcla: {cb}")
        df_cb = df[df['Combinación'] == cb]
        
        # Paso A: Sumar Áreas totales (Ej: 140 + 460 = 600)
        area_total_mezcla = df_cb['Area'].sum()
        
        resumen_final = []
        for m in cb.split('/'):
            fase = m.upper()
            datos_fase = df_cb[df_cb['Fase'] == fase]
            
            suma_area = datos_fase['Area'].sum()
            suma_sxd = datos_fase['SxD'].sum()
            vol_mezcla = datos_fase['Vol_Mezcla'].iloc[0]
            
            # Paso B: % de participación (Ej: 140 -> 23.3%)
            porcentaje_participacion = (suma_area / area_total_mezcla) if area_total_mezcla > 0 else 0
            
            # Paso C: % Volumen real (Ej: 23.3% de 1.44 = 0.336)
            vol_real = porcentaje_participacion * vol_mezcla
            
            # Paso D: G.L (Suma SxD / Suma Áreas totales de la mezcla)
            # Nota: Según tu foto, divides entre el total acumulado (600 en tu ejemplo)
            gl = suma_sxd / area_total_mezcla if area_total_mezcla > 0 else 0
            
            resumen_final.append({
                'Mineral': fase,
                'Suma Area': suma_area,
                '% Partic.': f"{porcentaje_participacion*100:.1f}%",
                '% Vol Real': round(vol_real, 3),
                'Suma SxD': suma_sxd,
                'G.L. Final': round(gl, 2)
            })
            
        st.table(pd.DataFrame(resumen_final))
        st.caption(f"Suma total de áreas en esta mezcla: {area_total_mezcla}")
    
    st.divider()
    st.subheader("Historial Completo")
    st.dataframe(df)
