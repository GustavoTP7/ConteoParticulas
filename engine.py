"""Motor de cálculo: réplica fiel de los resúmenes del VBA (ResumenGL, etc.)."""

def resumen_mineral(mineral, bloque, libres, tam_libres, totalC):
    parts=bloque['particulas']
    sumCLibre=sum(l[2] for l in libres if l[1]==mineral)
    # --- distribución por perímetro + asociaciones ---
    totalAC=0.0; s81=s50=s21=s0=0.0
    sumAPC={}; sumCAsoc={}; sumAC={}
    for p in parts:
        A,P,C=p['area'],p['perimetro'],p['cantidad']
        if A!=0 and C!=0:
            totalAC+=A*C
            if 81<=P<=100: s81+=A*C
            elif 50<=P<=80: s50+=A*C
            elif 21<=P<=49: s21+=A*C
            elif 0<=P<=20: s0+=A*C
        asoc=p['asociacion']
        if '/' not in asoc: asoc=''
        if asoc and asoc.upper() not in ('ASOCIACION','ASOCIACIÓN') and p['mineral']:
            sumAPC.setdefault(asoc,0.0); sumCAsoc.setdefault(asoc,0.0); sumAC.setdefault(asoc,0.0)
            sumAPC[asoc]+=A*P*C; sumCAsoc[asoc]+=C; sumAC[asoc]+=A*C
    r={}
    r['pct_libre']   = sumCLibre*100/totalC if totalC else 0
    r['sumCLibre']   = sumCLibre
    r['pct_asociado']= totalAC/totalC if totalC else 0
    if totalAC:
        r['p_81_100']=s81*100/totalAC; r['p_50_80']=s50*100/totalAC
        r['p_21_49']=s21*100/totalAC;  r['p_0_20']=s0*100/totalAC
    else:
        r['p_81_100']=r['p_50_80']=r['p_21_49']=r['p_0_20']=0.0
    r['asociaciones']=[]
    for k in sumAPC:
        r['asociaciones'].append(dict(
            asociacion=k, sumCAsoc=sumCAsoc[k],
            GL=sumAPC[k]/(sumCAsoc[k]*100) if sumCAsoc[k] else 0,
            V=sumAC[k]/totalC if totalC else 0))
    # --- intercrecimiento (fila202): %S,C,V,E,D ponderado por A*C ---
    tot=0.0; sE=sS=sD=sC=sV=0.0
    for p in parts:
        it=p['inter']; A=p['area']; C=p['cantidad']
        if it and A>0 and C>0:
            ac=A*C; tot+=ac
            if it=='E':sE+=ac
            elif it=='S':sS+=ac
            elif it=='D':sD+=ac
            elif it=='C':sC+=ac
            elif it=='V':sV+=ac
    r['inter']=({'S':sS*100/tot,'C':sC*100/tot,'V':sV*100/tot,'E':sE*100/tot,'D':sD*100/tot}
                if tot else {k:0.0 for k in 'SCVED'})
    # --- tamaños asociadas (204-207): por rango de tamaño ponderado A*C ---
    tot=0.0; t=[0.0]*4
    for p in parts:
        A,C,tm=p['area'],p['cantidad'],p['tam']
        if A>0 and C>0 and tm>0:
            ac=A*C; tot+=ac
            i=0 if tm<=20 else 1 if tm<=75 else 2 if tm<=106 else 3
            t[i]+=ac
    r['tam_asoc']=[x*100/tot for x in t] if tot else [0.0]*4
    # --- tamaños libres (175-178): por rango, ponderado por cantidad ---
    tot=0.0; t=[0.0]*4
    for (m,tm,c) in tam_libres:
        if m==mineral and tm>0 and c>0:
            tot+=c
            i=0 if tm<=20 else 1 if tm<=75 else 2 if tm<=106 else 3
            t[i]+=c
    r['tam_libre']=[x*100/tot for x in t] if tot else [0.0]*4
    return r

def calcular(data):
    out={}
    for mineral,bloque in data['bloques'].items():
        out[mineral]=resumen_mineral(mineral,bloque,data['libres'],data['tam_libres'],data['totalC'])
    return out
