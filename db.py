"""Base de datos SQLite: guarda muestras y sus partículas."""
import sqlite3, datetime, os

ESQUEMA="""
CREATE TABLE IF NOT EXISTS muestras(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT, hoja_origen TEXT, total_c REAL, fecha TEXT);
CREATE TABLE IF NOT EXISTS libres(
  muestra_id INT, punto TEXT, mineral TEXT, conteo REAL);
CREATE TABLE IF NOT EXISTS tam_libres(
  muestra_id INT, mineral TEXT, tam REAL, cant REAL);
CREATE TABLE IF NOT EXISTS particulas(
  muestra_id INT, punto TEXT, registro TEXT, mineral TEXT,
  area REAL, perimetro REAL, cantidad REAL,
  asociacion TEXT, inter TEXT, tam REAL);
"""

def conectar(ruta="metalurgia.db"):
    con=sqlite3.connect(ruta); con.executescript(ESQUEMA); return con

def guardar_muestra(con, data, nombre, hoja=""):
    cur=con.cursor()
    cur.execute("INSERT INTO muestras(nombre,hoja_origen,total_c,fecha) VALUES(?,?,?,?)",
                (nombre,hoja,data['totalC'],datetime.datetime.now().isoformat(timespec='seconds')))
    mid=cur.lastrowid
    cur.executemany("INSERT INTO libres VALUES(?,?,?,?)",
                    [(mid,str(p),m,c) for (p,m,c) in data['libres']])
    cur.executemany("INSERT INTO tam_libres VALUES(?,?,?,?)",
                    [(mid,m,t,c) for (m,t,c) in data['tam_libres']])
    filas=[]
    for mineral,b in data['bloques'].items():
        for p in b['particulas']:
            filas.append((mid,str(p['punto']),str(p['registro']),p['mineral'],
                          p['area'],p['perimetro'],p['cantidad'],p['asociacion'],p['inter'],p['tam']))
    cur.executemany("INSERT INTO particulas VALUES(?,?,?,?,?,?,?,?,?,?)",filas)
    con.commit(); return mid

def listar(con):
    return con.execute("SELECT id,nombre,hoja_origen,total_c,fecha FROM muestras ORDER BY id DESC").fetchall()

def cargar_muestra(con, mid):
    libres=[(p,m,c) for (p,m,c) in con.execute(
        "SELECT punto,mineral,conteo FROM libres WHERE muestra_id=?",(mid,))]
    tam=[(m,t,c) for (m,t,c) in con.execute(
        "SELECT mineral,tam,cant FROM tam_libres WHERE muestra_id=?",(mid,))]
    totalC=con.execute("SELECT total_c FROM muestras WHERE id=?",(mid,)).fetchone()[0]
    bloques={}
    for row in con.execute("""SELECT punto,registro,mineral,area,perimetro,cantidad,
             asociacion,inter,tam FROM particulas WHERE muestra_id=?""",(mid,)):
        pu,re,mi,ar,pe,ca,aso,it,tm=row
        bloques.setdefault(mi,dict(col=None,particulas=[]))['particulas'].append(
            dict(punto=pu,registro=re,mineral=mi,area=ar,perimetro=pe,cantidad=ca,
                 asociacion=aso,inter=it,tam=tm))
    return dict(libres=libres,tam_libres=tam,totalC=totalC,bloques=bloques,ws=None)
