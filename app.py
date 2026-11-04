"""Centro de Inteligencia Metalúrgica — prototipo.
Ejecutar:  streamlit run app.py
"""
import streamlit as st, pandas as pd, tempfile, os
from importer import leer_hoja
from engine import calcular
import db, report

st.set_page_config(page_title="Inteligencia Metalúrgica", layout="wide")
st.title("🔬 Centro de Inteligencia Metalúrgica")
st.caption("Prototipo — motor validado 1:1 contra el Excel original")

con = db.conectar()

with st.sidebar:
    st.header("Datos")
    modo = st.radio("Origen", ["Importar Excel", "Abrir muestra guardada"])
    data = None; nombre = None
    if modo == "Importar Excel":
        up = st.file_uploader("Archivo .xlsm", type=["xlsm","xlsx"])
        if up:
            tmp = os.path.join(tempfile.gettempdir(), up.name)
            with open(tmp,"wb") as f: f.write(up.getbuffer())
            import openpyxl
            hojas = openpyxl.load_workbook(tmp, read_only=True).sheetnames
            hoja = st.selectbox("Hoja de registro", hojas)
            if st.button("Cargar y calcular", type="primary"):
                data = leer_hoja(tmp, hoja); nombre = f"{up.name} · {hoja}"
                st.session_state["data"] = data
                st.session_state["nombre"] = nombre
                if st.toggle("Guardar en la base de datos", value=True):
                    db.guardar_muestra(con, data, nombre, hoja)
                    st.success("Guardada en la base de datos")
    else:
        filas = db.listar(con)
        if filas:
            opt = {f"#{i} · {n} ({f})": i for i,n,h,tc,f in filas}
            sel = st.selectbox("Muestra", list(opt))
            if st.button("Abrir", type="primary"):
                data = db.cargar_muestra(con, opt[sel])
                st.session_state["data"] = data
                st.session_state["nombre"] = sel
        else:
            st.info("Aún no hay muestras guardadas.")

data = st.session_state.get("data")
nombre = st.session_state.get("nombre","")

if not data:
    st.info("← Importa un Excel o abre una muestra para empezar.")
    st.stop()

res = calcular(data)
rdf = report.resumen_df(res)
adf = report.asociaciones_df(res)

st.subheader(nombre)
c1,c2,c3 = st.columns(3)
c1.metric("Total de conteos (C)", f"{data['totalC']:.0f}")
c2.metric("Minerales", len(res))
c3.metric("Asociaciones", len(adf))

t1,t2,t3,t4 = st.tabs(["📊 Resumen","🔗 Asociaciones","📈 Gráficos","✔️ Validación"])

with t1:
    st.dataframe(rdf, use_container_width=True, hide_index=True)
with t2:
    st.dataframe(adf, use_container_width=True, hide_index=True)
with t3:
    st.markdown("**% Liberado por mineral**")
    st.bar_chart(rdf.set_index("Mineral")["% Libre"])
    st.markdown("**Grado de liberación (GL) por asociación**")
    if not adf.empty:
        st.bar_chart(adf.assign(etq=adf["Mineral"]+" · "+adf["Asociacion"]).set_index("etq")["GL"])
with t4:
    if data.get("ws") is not None:
        from validate import cerca
        ws = data["ws"]; rows=[]; ok=0; tot=0
        gv=lambda r,c:(lambda x: float(x) if isinstance(x,(int,float)) else None)(ws.cell(r,c).value)
        for mineral,b in data["bloques"].items():
            col=b["col"]; r=res[mineral]
            pares=[("% libre",r["pct_libre"],gv(156,col+3)),
                   ("GL 1ª asoc",(r["asociaciones"][0]["GL"] if r["asociaciones"] else 0),gv(156,col+8))]
            for nm,py,xl in pares:
                tot+=1; good=cerca(py,xl); ok+=good
                rows.append(dict(Mineral=mineral,Campo=nm,Python=round(py,3),
                                 Excel=(round(xl,3) if xl is not None else None),
                                 OK=("✅" if good else "❌")))
        st.write(f"**{ok}/{tot} valores coinciden con el Excel original**")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("La validación contra Excel solo aplica al importar (no al abrir desde la BD).")
