"""Convierte el resultado del motor en tablas (DataFrames) para mostrar."""
import pandas as pd

def resumen_df(res):
    filas=[]
    for mineral,r in res.items():
        filas.append(dict(
            Mineral=mineral,
            **{'% Libre':round(r['pct_libre'],2),
               '% Asociado':round(r['pct_asociado']*100,2),
               'P 81-100':round(r['p_81_100'],1),'P 50-80':round(r['p_50_80'],1),
               'P 21-49':round(r['p_21_49'],1),'P 0-20':round(r['p_0_20'],1),
               'Int S':round(r['inter']['S'],1),'Int C':round(r['inter']['C'],1),
               'Int V':round(r['inter']['V'],1),'Int E':round(r['inter']['E'],1),
               'Int D':round(r['inter']['D'],1)}))
    return pd.DataFrame(filas)

def asociaciones_df(res):
    filas=[]
    for mineral,r in res.items():
        for a in r['asociaciones']:
            filas.append(dict(Mineral=mineral,Asociacion=a['asociacion'],
                              GL=round(a['GL'],2),V=round(a['V'],4),
                              SumC=a['sumCAsoc']))
    return pd.DataFrame(filas)
