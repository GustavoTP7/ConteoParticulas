"""Compara el motor Python contra los valores ya calculados en el Excel."""
import sys, openpyxl, warnings
warnings.filterwarnings('ignore')
from importer import leer_hoja, BO
from engine import calcular

def v(ws,r,c):
    x=ws.cell(r,c).value
    return float(x) if isinstance(x,(int,float)) else None

def cerca(a,b,tol=0.02):
    if a is None and b is None: return True
    if a is None or b is None: return abs((a or 0)-(b or 0))<=tol
    return abs(a-b)<=tol

def main(path,hoja):
    data=leer_hoja(path,hoja); res=calcular(data); ws=data['ws']
    print(f'totalC Python={data["totalC"]:.0f}  Excel(BL6)={v(ws,6,64):.0f}')
    ok=tot=0
    for mineral,bloque in data['bloques'].items():
        col=bloque['col']; r=res[mineral]
        checks=[
            ('%libre',   r['pct_libre'],    v(ws,156,col+3)),
            ('sumCLibre',r['sumCLibre'],    v(ws,156,col+4)),
            ('%asoc',    r['pct_asociado'], v(ws,161,col+3)),
            ('P81-100',  r['p_81_100'],     v(ws,157,col+3)),
            ('P50-80',   r['p_50_80'],      v(ws,158,col+3)),
            ('P21-49',   r['p_21_49'],      v(ws,159,col+3)),
            ('P0-20',    r['p_0_20'],       v(ws,160,col+3)),
            ('inter.S',  r['inter']['S'],   v(ws,202,col+5)),
            ('inter.D',  r['inter']['D'],   v(ws,202,col+9)),
            ('tamAsoc1', r['tam_asoc'][0],  v(ws,204,col+2)),
            ('tamLibre1',r['tam_libre'][0], v(ws,175,col+2)),
        ]
        # asociaciones GL/V vs fila156+
        for i,a in enumerate(r['asociaciones']):
            checks.append((f'GL[{a["asociacion"]}]', a['GL'], v(ws,156+i,col+8)))
            checks.append((f'V[{a["asociacion"]}]',  a['V'],  v(ws,156+i,col+9)))
        print(f'\n== {mineral} (col {col}) ==')
        for name,py,xl in checks:
            tot+=1; good=cerca(py,xl); ok+=good
            flag='OK ' if good else 'DIF'
            print(f'  [{flag}] {name:14} python={py!s:>10}  excel={xl!s:>10}')
    print(f'\n>>> {ok}/{tot} coinciden')

if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])
