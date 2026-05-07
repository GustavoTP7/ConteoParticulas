import streamlit as st
import pandas as pd

st.set_page_config(page_title="Método Cánepa - Registro Mineralógico", layout="wide")

# Inicializar estados de sesión si no existen
if 'db_libres' not in st.session_state:
    st.session_state.db_libres = pd.DataFrame(columns=['Campo', 'Mineral', 'Cantidad'])
if 'db_mixtos' not in st.session_state:
    st.session_state.db_mixtos = pd.DataFrame()
if 'campo' not in st.session_state:
    st.session_state.campo = 1

st.title("🔬 Sistema de Conteo Mineralógico (Método Cánepa)")
st.sidebar.header("Control de Sesión")
st.session_state.campo = st.sidebar.number_input("Campo / Partícula #", value=st.session_state.campo)

tab1, tab2 = st.tabs(["➕ Registro de Datos", "📊 Reporte y Cálculos"])

with tab1:
    col1, col2 = st.columns(2)

    # --- SECCIÓN 1: PARTÍCULAS LIBRES ---
    with col1:
        st.subheader("Partículas Libres")
        with st.form("form_libres", clear_on_submit=True):
            min_libre = st.text_input("Mineral", placeholder="Ej: Cp")
            cant_libre = st.number_input("Cantidad (No. Partículas)", min_value=1, value=1)
            if st.form_submit_button("Agregar Libre"):
                nuevo = pd.DataFrame([{'Campo': st.session_state.campo, 'Mineral': min_libre.upper(), 'Cantidad': cant_libre}])
                st.session_state.db_libres = pd.concat([st.session_state.db_libres, nuevo], ignore_index=True)
                st.toast(f"Libre {min_libre} agregado al campo {st.session_state.campo}")

    # --- SECCIÓN 2: PARTÍCULAS MIXTAS ---
    with col2:
        st.subheader("Partículas Mixtas")
        combo = st.text_input("Combinación (separada por '/')", placeholder="Ej: GGs/ef").lower()
        
        if combo and '/' in combo:
            minerales = combo.split('/')
            with st.form("form_mixtos", clear_on_submit=True):
                data_temp = {'Campo': st.session_state.campo, 'Combinación': combo}
                suma_a, suma_p = 0.0, 0.0
                
                # Inputs para todos menos el último
                for m in minerales[:-1]:
                    st.write(f"**Mineral: {m}**")
                    c_a, c_p = st.columns(2)
                    a_val = c_a.number_input(f"% Área {m}", min_value=0.0, max_value=100.0, key=f"{m}_a_form")
                    p_val = c_p.number_input(f"% Perímetro {m}", min_value=0.0, max_value=100.0, key=f"{m}_p_form")
                    
                    data_temp[f'{m}_Area'] = a_val
                    data_temp[f'{m}_Perim'] = p_val
                    data_temp[f'{m}_SxD'] = a_val * p_val
                    suma_a += a_val
                    suma_p += p_val

                # Cálculo automático del complemento (Lógica Cánepa)
                ultimo = minerales[-1]
                u_area = 100.0 - suma_a
                u_perim = 100.0 - suma_p
                data_temp[f'{ultimo}_Area'] = u_area
                data_temp[f'{ultimo}_Perim'] = u_perim
                data_temp[f'{ultimo}_SxD'] = u_area * u_perim
                
                st.info(f"**{ultimo}** calculado: {u_area}% Área | {u_perim}% Perímetro")
                
                if st.form_submit_button("Guardar Mixto"):
                    if suma_a > 100 or suma_p > 100:
                        st.error("Error: La suma de áreas o perímetros excede el 100%")
                    else:
                        st.session_state.db_mixtos = pd.concat([st.session_state.db_mixtos, pd.DataFrame([data_temp])], ignore_index=True)
                        st.toast("Mixto guardado correctamente")

with tab2:
    if st.session_state.db_libres.empty and st.session_state.db_mixtos.empty:
        st.info("No hay datos registrados aún.")
    else:
        # Resumen General
        st.subheader("Datos de Partículas Mixtas (SxD)")
        if not st.session_state.db_mixtos.empty:
            cols_interes = [c for c in st.session_state.db_mixtos.columns if '_SxD' in c or c in ['Campo', 'Combinación']]
            st.dataframe(st.session_state.db_mixtos[cols_interes], use_container_width=True)

            st.divider()
            st.subheader("Cálculo de Grado de Liberación (G.L.)")
            st.write("Fórmula aplicada: $\sum (S \times D) / 600$")
            
            for cb in st.session_state.db_mixtos['Combinación'].unique():
                df_cb = st.session_state.db_mixtos[st.session_state.db_mixtos['Combinación'] == cb]
                st.markdown(f"**Resultados para Mezcla: `{cb}`**")
                res_list = []
                for m in cb.split('/'):
                    total_sxd = df_cb[f'{m}_SxD'].sum()
                    res_list.append({
                        'Mineral': m,
                        'Suma Áreas': df_cb[f'{m}_Area'].sum(),
                        'Suma SxD': total_sxd,
                        'G.L. (SxD/600)': round(total_sxd / 600, 4)
                    })
                st.table(pd.DataFrame(res_list))
        
        if not st.session_state.db_libres.empty:
            st.subheader("Partículas Libres Registradas")
            st.dataframe(st.session_state.db_libres, use_container_width=True)

# Botón de reinicio en el sidebar
if st.sidebar.button("🗑️ Borrar Todo"):
    st.session_state.db_libres = pd.DataFrame(columns=['Campo', 'Mineral', 'Cantidad'])
    st.session_state.db_mixtos = pd.DataFrame()
    st.session_state.campo = 1
    st.rerun()
