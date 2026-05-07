import streamlit as st
import pandas as pd

st.set_page_config(page_title="Método Cánepa - Registro Mineralógico", layout="wide")

# --- ESTADO DE SESIÓN ---
if 'db_libres' not in st.session_state:
    st.session_state.db_libres = pd.DataFrame(columns=['Campo', 'Mineral', 'Cantidad'])
if 'db_mixtos' not in st.session_state:
    st.session_state.db_mixtos = pd.DataFrame()
if 'campo' not in st.session_state:
    st.session_state.campo = 1

# --- BARRA LATERAL (SIDEBAR): INGRESO DE DATOS ---
with st.sidebar:
    st.title("📥 Ingreso de Datos")
    st.session_state.campo = st.number_input("Campo / Partícula #", value=st.session_state.campo)
    
    st.divider()
    
    # Registro de Libres
    st.subheader("Partículas Libres")
    with st.form("form_libres", clear_on_submit=True):
        min_libre = st.text_input("Mineral", placeholder="Ej: Cp")
        cant_libre = st.number_input("Cantidad", min_value=1, value=1)
        if st.form_submit_button("➕ Agregar Libre"):
            nuevo = pd.DataFrame([{'Campo': st.session_state.campo, 'Mineral': min_libre.upper(), 'Cantidad': cant_libre}])
            st.session_state.db_libres = pd.concat([st.session_state.db_libres, nuevo], ignore_index=True)
            st.toast(f"Libre {min_libre} registrado")

    st.divider()

    # Registro de Mixtos
    st.subheader("Partículas Mixtas")
    combo = st.text_input("Combinación (Ej: GGs/ef)").lower()
    
    if combo and '/' in combo:
        minerales = combo.split('/')
        with st.form("form_mixtos", clear_on_submit=True):
            data_temp = {'Campo': st.session_state.campo, 'Combinación': combo}
            suma_a, suma_p = 0.0, 0.0
            
            for m in minerales[:-1]:
                st.markdown(f"**Mineral: {m}**")
                a_val = st.number_input(f"% Área {m}", min_value=0.0, max_value=100.0, key=f"{m}_a_side")
                p_val = st.number_input(f"% Perímetro {m}", min_value=0.0, max_value=100.0, key=f"{m}_p_side")
                
                data_temp[f'{m}_Area'] = a_val
                data_temp[f'{m}_Perim'] = p_val
                data_temp[f'{m}_SxD'] = a_val * p_val
                suma_a += a_val
                suma_p += p_val

            # Cálculo automático del complemento
            ultimo = minerales[-1]
            u_area = 100.0 - suma_a
            u_perim = 100.0 - suma_p
            data_temp[f'{ultimo}_Area'] = u_area
            data_temp[f'{ultimo}_Perim'] = u_perim
            data_temp[f'{ultimo}_SxD'] = u_area * u_perim
            
            st.caption(f"ℹ️ {ultimo}: {u_area}% Área | {u_perim}% Perímetro")
            
            if st.form_submit_button("💾 Guardar Mixto"):
                if suma_a > 100 or suma_p > 100:
                    st.error("Excede 100%")
                else:
                    st.session_state.db_mixtos = pd.concat([st.session_state.db_mixtos, pd.DataFrame([data_temp])], ignore_index=True)
                    st.toast("Mixto guardado")

    st.divider()
    if st.button("🗑️ Borrar Todo"):
        st.session_state.db_libres = pd.DataFrame(columns=['Campo', 'Mineral', 'Cantidad'])
        st.session_state.db_mixtos = pd.DataFrame()
        st.session_state.campo = 1
        st.rerun()

# --- ÁREA PRINCIPAL: REPORTE ---
st.title("📊 Reporte de Conteo Mineralógico")
st.markdown(f"**Método Cánepa** | Campo Actual: `{st.session_state.campo}`")

if st.session_state.db_libres.empty and st.session_state.db_mixtos.empty:
    st.info("Utiliza la barra lateral de la izquierda para comenzar a ingresar datos.")
else:
    # Mostramos el reporte en pestañas o secciones directas
    rep_mixtos, rep_libres = st.tabs(["💎 Partículas Mixtas", "🧊 Partículas Libres"])

    with rep_mixtos:
        if not st.session_state.db_mixtos.empty:
            st.subheader("Cálculo de Grado de Liberación (G.L.)")
            st.caption("Fórmula: Suma(SxD) / 600")
            
            # Agrupar y resumir por combinación
            for cb in st.session_state.db_mixtos['Combinación'].unique():
                df_cb = st.session_state.db_mixtos[st.session_state.db_mixtos['Combinación'] == cb]
                st.write(f"### Análisis Mezcla: `{cb}`")
                
                res_list = []
                for m in cb.split('/'):
                    total_sxd = df_cb[f'{m}_SxD'].sum()
                    res_list.append({
                        'Mineral': m,
                        'Suma Áreas': round(df_cb[f'{m}_Area'].sum(), 2),
                        'Suma SxD': round(total_sxd, 2),
                        'G.L. Ponderado': round(total_sxd / 600, 4)
                    })
                st.table(pd.DataFrame(res_list))
            
            st.divider()
            st.subheader("Historial de Registros Mixtos")
            cols_vista = [c for c in st.session_state.db_mixtos.columns if '_SxD' in c or c in ['Campo', 'Combinación']]
            st.dataframe(st.session_state.db_mixtos[cols_vista], use_container_width=True)
        else:
            st.write("No hay registros mixtos.")

    with rep_libres:
        if not st.session_state.db_libres.empty:
            st.subheader("Historial de Libres")
            st.dataframe(st.session_state.db_libres, use_container_width=True)
        else:
            st.write("No hay registros libres.")
