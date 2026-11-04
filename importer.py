"""Lee una hoja de registro (p.ej. CAB+140) tal como la interpreta el VBA."""
import openpyxl, warnings
warnings.filterwarnings('ignore')

BO = 67  # primera columna de bloques de detalle

def _num(x):
    if x is None: return 0.0
    if isinstance(x,(int,float)): return float(x)
    s=str(x).strip().replace(',','.')
    out=''
    for ch in s:
        if ch.isdigit() or ch in '.-' : out+=ch
        else: break
    try: return float(out)
    except: return 0.0

def leer_hoja(path, hoja):
    wb=openpyxl.load_workbook(path,data_only=True)
    ws=wb[hoja]
    g=lambda r,c: ws.cell(r,c).value
    libres=[]            # (punto, mineral, conteo)
    for r in range(6,301):
        b=g(r,2)
        if b not in (None,''):
            libres.append((g(r,1), str(b).strip(), _num(g(r,3))))
    tam_libres=[]        # (mineral, tam, cant)
    rmax=ws.max_row
    for r in range(305,rmax+1):
        a=g(r,1)
        if a not in (None,''):
            tam_libres.append((str(a).strip(), _num(g(r,2)), _num(g(r,3))))
    # total C global (cols C,E,G...BK filas 6-300)
    totalC=0.0
    for r in range(6,301):
        for c in range(3,64,2):
            totalC+=_num(g(r,c))
    # bloques de detalle BO.. step13
    bloques={}           # mineral -> lista de particulas dict
    for col in range(BO,340,13):
        mineral=g(6,col+2)
        if mineral in (None,''): continue
        mineral=str(mineral).strip()
        parts=[]
        for r in range(6,151):
            if g(r,col+2) in (None,''): continue
            parts.append(dict(
                punto=g(r,col), registro=g(r,col+1), mineral=str(g(r,col+2)).strip(),
                area=_num(g(r,col+3)), perimetro=_num(g(r,col+4)), cantidad=_num(g(r,col+5)),
                asociacion=('' if g(r,col+7) in (None,'') else str(g(r,col+7)).strip()),
                inter=('' if g(r,col+8) in (None,'') else str(g(r,col+8)).strip().upper()),
                tam=_num(g(r,col+9)) ))
        bloques[mineral]=dict(col=col, particulas=parts)
    return dict(libres=libres, tam_libres=tam_libres, totalC=totalC, bloques=bloques, ws=ws)
