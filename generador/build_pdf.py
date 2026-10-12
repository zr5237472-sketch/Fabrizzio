from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Wedge, String, Circle
from data import *

pdfmetrics.registerFont(TTFont("DV","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("DV",normal="DV",bold="DVB",italic="DVI",boldItalic="DVB")
GREEN=colors.HexColor("#2F6B4F"); LIGHT=colors.HexColor("#E8F1EC"); AMBER=colors.HexColor("#F2B84B")
ROSE=colors.HexColor("#E0786B"); LEAF=colors.HexColor("#7DB46C"); GREY=colors.HexColor("#F4F4F4"); LINE=colors.HexColor("#BFBFBF")
import os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
IMG=os.path.join(ROOT,"assets","plato_referencial.png")
def S(name,**k):
    base=dict(fontName="DV",fontSize=9,leading=12,textColor=colors.HexColor("#222222")); base.update(k)
    return ParagraphStyle(name,**base)
st=dict(h1=S("h1",fontName="DVB",fontSize=20,leading=24,textColor=GREEN), h2=S("h2",fontName="DVB",fontSize=13,leading=17,textColor=GREEN,spaceBefore=6,spaceAfter=4),
 b=S("b"), sm=S("sm",fontSize=7.5,leading=10), bi=S("bi",fontName="DVI",fontSize=8,leading=11,textColor=colors.HexColor("#555555")),
 th=S("th",fontName="DVB",fontSize=8.5,leading=11,textColor=colors.white,alignment=TA_CENTER), td=S("td",fontSize=8.5,leading=11),
 tdc=S("tdc",fontSize=8.5,leading=11,alignment=TA_CENTER), big=S("big",fontSize=11,leading=15), bl=S("bl",fontSize=10,leading=14),
 tdb=S("tdb",fontName="DVB",fontSize=8.5,leading=11), tdbc=S("tdbc",fontName="DVB",fontSize=8.5,leading=11,alignment=TA_CENTER))
def P(t,s="b"): return Paragraph(t,st[s])
def fm(x,d=0):
    s=f"{x:,.{d}f}"; return s.replace(",","§").replace(".",",").replace("§",".")
import re
NUM=re.compile(r"^[+\-−]?[\d.,]+$")
def tbl(data,widths,hdr=True,zebra=True,extra=None,pad=3,bold=()):
    rows=[]
    for i,r in enumerate(data):
        row=[]
        for c in r:
            if not isinstance(c,str): row.append(c); continue
            if hdr and i==0: row.append(P(c,"th"))
            elif i in bold: row.append(P(c,"tdbc" if NUM.match(c) else "tdb"))
            elif NUM.match(c): row.append(P(c,"tdc"))
            else: row.append(P(c,"td"))
        rows.append(row)
    t=Table(rows,colWidths=widths,repeatRows=1 if hdr else 0)
    sty=[("GRID",(0,0),(-1,-1),0.4,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),pad),("BOTTOMPADDING",(0,0),(-1,-1),pad),
         ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]
    if hdr: sty.append(("BACKGROUND",(0,0),(-1,0),GREEN))
    if zebra:
        for i in range(1,len(rows)):
            if i%2==0: sty.append(("BACKGROUND",(0,i),(-1,i),GREY))
    if extra: sty+=extra
    t.setStyle(TableStyle(sty)); return t

def plate(size=150):
    d=Drawing(size+10,size+10); cx=cy=(size+10)/2; r=size/2
    d.add(Circle(cx,cy,r+3,fillColor=colors.white,strokeColor=colors.HexColor("#999999"),strokeWidth=1.5))
    for a0,a1,col,txt,dx,dy in ((90,210,LEAF,"1/3\nEnsalada",-0.42,0.25),(210,330,AMBER,"1/3\nCarbohidrato",0,-0.55),(330,450,ROSE,"1/3\nProteína",0.42,0.25)):
        d.add(Wedge(cx,cy,r-6,a0,a1,fillColor=col,strokeColor=colors.white,strokeWidth=2))
    for txt,dx,dy in (("Ensalada",-0.45,0.2),("Carbohidrato",0,-0.58),("Proteína",0.45,0.2)):
        d.add(String(cx+dx*r,cy+dy*r,txt,fontName="DVB",fontSize=8,textAnchor="middle",fillColor=colors.HexColor("#222222")))
    for txt,dx,dy in (("1/3",-0.45,0.02),("1/3",0,-0.72),("1/3",0.45,0.02)):
        d.add(String(cx+dx*r,cy+dy*r,txt,fontName="DVB",fontSize=11,textAnchor="middle",fillColor=colors.HexColor("#222222")))
    return d

def mk(path,title_txt,landscape_=True):
    pg=landscape(A4) if landscape_ else A4
    doc=BaseDocTemplate(path,pagesize=pg,leftMargin=14*mm,rightMargin=14*mm,topMargin=14*mm,bottomMargin=15*mm,title=title_txt,author="Plan nutricional")
    fr=Frame(doc.leftMargin,doc.bottomMargin,pg[0]-doc.leftMargin-doc.rightMargin,pg[1]-doc.topMargin-doc.bottomMargin,id="f")
    def foot(c,d):
        c.saveState(); c.setFont("DV",7.5); c.setFillColor(colors.HexColor("#777777"))
        c.drawString(doc.leftMargin,8*mm,title_txt); c.drawRightString(pg[0]-doc.rightMargin,8*mm,f"Pág. {d.page}")
        c.setStrokeColor(GREEN); c.setLineWidth(1.2); c.line(doc.leftMargin,pg[1]-10*mm,pg[0]-doc.rightMargin,pg[1]-10*mm); c.restoreState()
    doc.addPageTemplates([PageTemplate(id="p",frames=[fr],onPage=foot)]); return doc,pg[0]-doc.leftMargin-doc.rightMargin

# ---------- helpers de descripcion ----------
def frac(g):
    return g
def desc_item(k,g):
    if k=="pan_molde": n=g/MEDIDAS["rebanada"]; return f"{n:g} rebanada{'s' if n>1 else ''} de pan de molde ({g:g} g)"
    if k=="avena": n=g/MEDIDAS["scoop"]; return f"{n:g} scoop{'s' if n>1 else ''} de avena ({g:g} g)"
    if k=="arroz": n=g/MEDIDAS["cucharon"]; return f"{n:g} cucharones de arroz blanco ({g:g} g cocido)"
    if k=="papa": n=g/MEDIDAS["papa"]; return f"{n:g} papas grandes sancochadas ({g:g} g)"
    if k=="fideo": return f"Fideos cocidos que cubran 1/3 del plato ({g:g} g)"
    if k=="palta": return f"{'¼' if g==45 else '½'} palta ({g:g} g de pulpa)"
    if k=="queso": return f"Queso fresco {g:g} g"
    if k=="aceite": return f"1 cdta de aceite de oliva ({g:g} g)"
    return None
def meal_lines(d,cm,ci):
    out=[]; items=dict(ci[cm])
    if cm in("des","mer"):
        for k in ("pan_molde","avena","palta","queso"):
            if k in items: out.append(desc_item(k,items[k]))
    else:
        c,p,e=d["alm" if cm=="alm" else "cen"]
        out.append(desc_item(c,items[{"arroz":"arroz","papa":"papa","fideo":"fideo"}[c]]))
        out.append(f"{PROT[p][0]} ({', '.join(f'{v:g} g' for v in PROT[p][1].values())}{' crudo' if p not in ('atun','huevo') else ''})".replace("(100 g, 100 g crudo)","(2 huevos + 3 claras)").replace("(100 g, 100 g)","(2 huevos + 3 claras)"))
        if p=="huevo": out[-1]="2 huevos + 3 claras sancochados"
        if p=="atun": out[-1]="Atún en agua: 1 lata escurrida (120 g)"
        out.append(f"Ensalada {ENS[e][0].split(':')[0].lower()}: {ENS[e][0].split(': ')[1]} ({sum(ENS[e][1].values())} g)")
        if "aceite" in items: out.append(desc_item("aceite",items["aceite"]))
    return out

DAYS=[]
for n,d in zip(DIAS,MENU):
    ci=comida_items(d); ms={k:macros(v) for k,v in ci.items()}
    DAYS.append((n,d,ci,ms,add(*ms.values())))
PROM=[sum(x[4][i] for x in DAYS)/7 for i in range(4)]
PESO0=PERFIL["peso0"]
def meta(week_start,week_end,sem):
    bmr=10*week_start+6.25*PERFIL["talla_cm"]-5*PERFIL["edad"]-161; get=bmr*PERFIL["pal"]
    dfc=(week_start-week_end)*7700/7; return bmr,get,dfc,max(PERFIL["piso_kcal"],round((get-dfc)/10)*10)
BMR,GET,DEF,META1=meta(64.5,64.3,1)
PROT_META=round(PESO0*PERFIL["g_prot_kg"])
COMIDAS=[("des","Desayuno"),("alm","Almuerzo"),("mer","Merienda"),("cen","Cena")]

# =============================== PDF TECNICO ===============================
def tecnico():
    doc,W=mk(os.path.join(ROOT,"Semana1_Tecnico_12-18oct.pdf"),"Plan nutricional · Semana 1 (12–18 oct) · Versión técnica")
    s=[]
    s.append(P("Plan nutricional · Semana 1","h1"))
    s.append(P("12 al 18 de octubre de 2026 · Versión técnica (cantidades, cálculos y justificación)","big"))
    s.append(Spacer(1,6))
    ficha=[["Dato","Valor","Dato","Valor"],
     ["Cliente","Mujer adulta","Peso inicial / objetivo semana 1",f"{fm(PESO0,1)} kg → 64,3 kg (−0,2 kg)"],
     ["Talla","165 cm","Meta a 12 semanas","61,0 kg sin afectar el rendimiento en gym"],
     ["Edad (supuesto)",f"{PERFIL['edad']} años — corregir si difiere","Actividad","Estudia + gym 2–3 días/sem (factor 1,35)"],
     ["Gasto basal (Mifflin-St Jeor)",f"{fm(BMR)} kcal","Gasto total estimado (GET)",f"{fm(GET)} kcal/día"],
     ["Meta calórica semana 1",f"{fm(META1)} kcal/día (déficit ≈ {fm(DEF)} kcal)","Plan de esta semana (promedio)",f"{fm(PROM[0])} kcal/día · P {fm(PROM[1])} g · G {fm(PROM[2])} g · C {fm(PROM[3])} g"]]
    s.append(tbl(ficha,[W*.2,W*.28,W*.22,W*.30])); s.append(Spacer(1,6))
    gap=PROM[0]-META1; perd=(GET-PROM[0])*7/7700
    s.append(P("<b>Lectura del plan.</b> El menú sigue la estructura pedida (desayuno, almuerzo, merienda, cena, 3 tomatodos y ½ palta o 150 g de queso). "
      f"Resulta en <b>{fm(PROM[0])} kcal/día</b> en promedio, <b>{fm(gap)} kcal sobre la meta</b> de {fm(META1)} kcal, por lo que se espera una baja de ≈ <b>{fm(perd,2)} kg</b> en la semana "
      "(más lo que se pierda por agua/glucógeno al ordenar los carbohidratos). Los días con queso (miércoles y sábado) suben ≈ +250 kcal frente a los días con palta. "
      f"Proteína promedio {fm(PROM[1])} g/día = <b>{fm(PROM[1]/PESO0,2)} g/kg</b>, adecuada para sostener la masa muscular mientras entrena.","b"))
    s.append(Spacer(1,4))
    s.append(P("Supuestos de medidas (verificar una vez con balanza)","h2"))
    med=[["Medida casera","Gramos","kcal","Proteína","Observación"],
     ["1 rebanada de pan de molde","25 g",fm(25*317/100),fm(25*6.8/100,1)+" g","Ajustar al pan que usa"],
     ["1 scoop de avena (hojuela cruda)","25 g",fm(25*333/100),fm(25*13.3/100,1)+" g","Scoop raso"],
     ["1 cucharón de arroz cocido","70 g",fm(70*115/100),fm(70*2.4/100,1)+" g","3 cucharones = 210 g"],
     ["1 papa grande (pelada, sancochada)","150 g",fm(150*87/100),fm(150*2.1/100,1)+" g","2 papas = 300 g"],
     ["1 palma de proteína","150 g crudo ≈ 115–120 g cocido",fm(150*108/100)+" (pollo)",fm(150*19.2/100,1)+" g (pollo)","Tamaño de la palma sin dedos"],
     ["1 tomatodo","800 ml","—","—","3 tomatodos ≈ 2,4 L"]]
    s.append(tbl(med,[W*.27,W*.2,W*.12,W*.14,W*.27]))
    s.append(Spacer(1,10))
    # --- plato
    s.append(P("Plato referencial: regla 1/3 – 1/3 – 1/3","h2"))
    d=plate(165)
    img=Image(IMG,width=60*mm,height=60*mm*427/380)
    txt=[P("<b>Almuerzo y cena</b> se arman igual:",bl:="bl") if False else P("<b>Almuerzo y cena</b> se arman igual:","bl"),
         P("• <b>1/3 carbohidrato</b>: 2 papas grandes (300 g) <b>o</b> 3 cucharones de arroz (210 g) <b>o</b> fideos que cubran la tercera parte (≈ 250 g cocido). ≈ 225–260 kcal.","bl"),
         P("• <b>1/3 proteína</b>: 1 palma (≈ 150 g crudo). ≈ 25–32 g de proteína, 130–205 kcal según el alimento.","bl"),
         P("• <b>1/3 ensalada</b>: ≈ 200 g de verduras (≈ 2 tazas) con limón y, en el almuerzo, 1 cdta de aceite de oliva. ≈ 25–55 kcal (+44 kcal del aceite).","bl"),
         Spacer(1,4),P("La foto de la derecha es el plato de referencia entregado: sirve para calibrar el tamaño. En ella falta la tercera parte de ensalada.","bi")]
    t=Table([[d,txt,[img,P("Plato referencial (tamaño)","sm")]]],colWidths=[W*.26,W*.48,W*.26])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")])); s.append(t)
    s.append(Spacer(1,10))
    # --- menu por dia
    s.append(P("Menú de la semana con cantidades y cálculo","h2"))
    s.append(P("Cada fila indica el alimento, la medida casera y su peso; kcal y macros calculados con la TPCA (INS-Perú). La palta/queso del día se reparte entre desayuno y merienda para untar el pan.","bi"))
    s.append(Spacer(1,4))
    for n,dd,ci,ms,tot in DAYS:
        rows=[[f"{n} · {'con queso' if dd['grasa']=='queso' else 'con palta'}","Detalle","kcal","P (g)","G (g)","C (g)"]]
        for cm,nm in COMIDAS:
            lines="<br/>".join("• "+x for x in meal_lines(dd,cm,ci))
            m=ms[cm]; rows.append([nm,P(lines,"td"),fm(m[0]),fm(m[1]),fm(m[2]),fm(m[3])])
        rows.append(["TOTAL DEL DÍA","",fm(tot[0]),fm(tot[1]),fm(tot[2]),fm(tot[3])])
        t=tbl(rows,[W*.14,W*.56,W*.075,W*.075,W*.075,W*.075],extra=[("BACKGROUND",(0,len(rows)-1),(-1,len(rows)-1),LIGHT)],pad=2,bold=(len(rows)-1,))
        # convertir celdas de texto fila total a negrita
        s.append(KeepTogether([t,Spacer(1,6)]))
    s.append(PageBreak())
    # --- resumen semanal
    s.append(P("Resumen semanal","h2"))
    rows=[["Día","Desayuno","Almuerzo","Merienda","Cena","Total kcal","Proteína (g)","Grasa (g)","Carbo (g)","vs meta ("+fm(META1)+")"]]
    for n,dd,ci,ms,tot in DAYS:
        rows.append([n,fm(ms['des'][0]),fm(ms['alm'][0]),fm(ms['mer'][0]),fm(ms['cen'][0]),fm(tot[0]),fm(tot[1]),fm(tot[2]),fm(tot[3]),f"{tot[0]-META1:+,.0f}".replace(",",".").replace("-","−")])
    rows.append(["Promedio","","","","",fm(PROM[0]),fm(PROM[1]),fm(PROM[2]),fm(PROM[3]),f"{PROM[0]-META1:+,.0f}".replace("-","−")])
    s.append(tbl(rows,[W*.12]+[W*.09]*4+[W*.1,W*.11,W*.1,W*.1,W*.09],extra=[("BACKGROUND",(0,len(rows)-1),(-1,len(rows)-1),LIGHT)],bold=(len(rows)-1,)))
    s.append(Spacer(1,8))
    s.append(P("¿Por qué agregamos cada elemento?","h2"))
    why=[["Elemento","Cantidad diaria","Aporte aprox.","Por qué está en el plan"],
     ["Pan de molde","3 rebanadas (des.) + 2 (mer.) = 125 g","≈ 396 kcal · 8,5 g P","Carbohidrato rápido y fácil de digerir; porción fija evita el exceso. La merienda funciona como pre-entreno (60–90 min antes del gym)."],
     ["Avena","1 scoop (des.) + 2 scoops (mer.) = 75 g","≈ 250 kcal · 10 g P","Fibra soluble (beta-glucano): saciedad y mejor digestión del carbohidrato; aporta 13 g de proteína/100 g, más que el pan."],
     ["1/3 carbohidrato (almuerzo y cena)","≈ 210–300 g cocido ×2","≈ 450–520 kcal","Repone glucógeno para entrenar sin pasarse. Papa, arroz y fideo son intercambiables porque aportan ≈ 225–260 kcal por 1/3 de plato."],
     ["1/3 proteína (almuerzo y cena)","≈ 150 g crudo ×2","≈ 50–62 g P","Con ≈ 25–32 g por comida se alcanza el umbral para estimular la síntesis muscular; protege la masa magra durante el déficit."],
     ["1/3 ensalada","≈ 200 g ×2","≈ 50–110 kcal","Volumen y saciedad con muy pocas kcal; fibra y micronutrientes. Variar colores y cocción mejora la tolerancia digestiva."],
     ["½ palta o 150 g queso fresco","90 g pulpa o 150 g","117 kcal (palta) · 396 kcal (queso)","Grasa saludable y vitaminas liposolubles; el queso suma calcio y 26 g de proteína pero ≈ 3,4 veces más kcal que la palta, por eso se limita a 2 días y se ajustará en semanas siguientes."],
     ["Aceite de oliva","1 cdta (5 g) en el almuerzo","44 kcal","Mejora la absorción de carotenos (zanahoria, tomate) y la palatabilidad; controlado para no inflar calorías."],
     ["Agua","3 tomatodos ≈ 2,4 L","0 kcal","Rendimiento, saciedad y tránsito intestinal con avena y verduras (más fibra)."]]
    s.append(tbl(why,[W*.18,W*.2,W*.17,W*.45]))
    s.append(PageBreak())
    # --- variedad
    s.append(P("Tabla de variedad: intercambios equivalentes","h2"))
    s.append(P("Si falta un alimento, se reemplaza por otro de la misma fila manteniendo la cantidad indicada (calorías y proteína equivalentes). Valores TPCA.","bi"))
    s.append(Spacer(1,4))
    def eq(items):
        out=[]
        for k,g,lab in items:
            kc,p,gs,c=macros({k:g}); out.append(f"<b>{lab}</b><br/>{g:g} g · {fm(kc)} kcal · P {fm(p,1)} g")
        return out
    carb=eq([("papa",300,"Papa blanca (2 grandes)"),("arroz",210,"Arroz (3 cucharones)"),("fideo",250,"Fideo sancochado"),("camote",250,"Camote sancochado"),("quinua_coc",270,"Quinua cocida")])
    prot=eq([("pollo_pech",150,"Pechuga de pollo"),("pollo_pulpa",150,"Muslo sin piel"),("res_pulpa",140,"Res pulpa (bistec)"),("tilapia",150,"Tilapia"),("trucha",150,"Trucha"),("bonito",130,"Bonito"),("merluza",180,"Merluza"),("atun_agua",120,"Atún en agua (1 lata)")])
    huevo=macros({"huevo":100,"clara":100}); 
    prot.append(f"<b>2 huevos + 3 claras</b><br/>200 g · {fm(huevo[0])} kcal · P {fm(huevo[1],1)} g")
    kk=macros({"pan_molde":75})
    des=[f"<b>Pan de molde (3 rebanadas)</b><br/>75 g · {fm(kk[0])} kcal",
         f"<b>Pan francés</b> (≈ 2 unidades chicas)<br/>86 g · {fm(macros({'pan_frances':86})[0])} kcal",
         f"<b>Avena (1 scoop)</b><br/>25 g · {fm(macros({'avena':25})[0])} kcal",
         f"<b>Hojuelas de quinua (1 scoop)</b><br/>22 g · {fm(macros({'quinua_hoj':22})[0])} kcal"]
    gr=[f"<b>½ palta</b><br/>90 g pulpa · {fm(macros({'palta':90})[0])} kcal",f"<b>Queso fresco</b><br/>150 g · {fm(macros({'queso':150})[0])} kcal · P 26 g"]
    veg=[f"<b>{v[0].split(':')[0]}</b><br/>{v[0].split(': ')[1]} · {sum(v[1].values())} g · {fm(macros(v[1])[0])} kcal" for v in ENS.values()]
    def row(label,lst,n=3):
        cells=[P(x,"td") for x in lst]; 
        while len(cells)%n: cells.append("")
        return label,[cells[i:i+n] for i in range(0,len(cells),n)]
    for label,lst,n,note in (("1/3 CARBOHIDRATO (almuerzo/cena)",carb,5,None),("1/3 PROTEÍNA (almuerzo/cena)",prot,3,"Opción vegetal: lentejas cocidas 300 g (≈195 kcal · P 19 g) o garbanzo cocido 250 g (≈ 318 kcal · P 17 g); al usarlas reducir el carbohidrato del plato a la mitad porque ya aportan carbohidratos."),
                             ("1/3 ENSALADA (almuerzo/cena)",veg,3,None),("DESAYUNO / MERIENDA (pan y avena)",des,4,"Mantener la cantidad de rebanadas/scoops; el pan francés y la quinua son alternativas si falta pan de molde o avena."),
                             ("GRASA DEL DÍA",gr,2,"El queso aporta ≈ 280 kcal más que la palta: no usarlo más de 2 veces por semana.")):
        cells=[P(x,"td") for x in lst]
        while len(cells)%n: cells.append("")
        data=[cells[i:i+n] for i in range(0,len(cells),n)]
        t=Table(data,colWidths=[W/n]*n); t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,-1),colors.white),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
        head=Table([[P(label,"th")]],colWidths=[W]); head.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2)]))
        blk=[head,t]
        if note: blk.append(P(note,"bi"))
        blk.append(Spacer(1,5)); s.append(KeepTogether(blk))
    s.append(PageBreak())
    # --- digestion
    s.append(P("Ensaladas y recomendaciones para mejorar la digestión","h2"))
    ens=[["Ensalada","Ingredientes (g)","Total","kcal","Cuándo / cocción"]]
    when={"A":"Cruda; ideal en días cálidos","B":"Brócoli al vapor 3–5 min; la zanahoria y el pimiento pueden ir crudos o ligeramente cocidos","C":"Cruda finamente picada o ligeramente salteada; si da gases, blanquear la col 1–2 min","D":"Vainita cocida, espinaca y tomate crudos","E":"Coliflor al vapor, el resto crudo"}
    for k,(n,it) in ENS.items():
        ens.append([f"{k}. {n}",", ".join(f"{F[x][0].split(' (')[0].lower()} {g} g" for x,g in it.items()),f"{sum(it.values())} g",fm(macros(it)[0]),when[k]])
    s.append(tbl(ens,[W*.24,W*.30,W*.07,W*.07,W*.32]))
    s.append(Spacer(1,6))
    tips=[("Empezar por la ensalada","Comerla primero y masticar 20–30 veces: la digestión comienza en la boca y la fibra llena antes."),
      ("Cocción suave de crucíferas","Brócoli, coliflor y col al vapor 3–5 min (o blanqueadas) producen menos gases que crudas; las hojas y el tomate pueden ir crudos."),
      ("Aumentar la fibra de forma gradual","Avena + pan + ensalada elevan la fibra: si hay hinchazón, reducir la ensalada cruda a 1½ tazas una semana y subir otra vez."),
      ("Agua entre comidas","Beber los 3 tomatodos repartidos en el día; durante la comida solo sorbos para no diluir los jugos digestivos."),
      ("Limón y aceite","Aliñar con limón y 1 cdta de aceite de oliva: más sabor y mejor absorción de carotenos; evitar aderezos con crema o mayonesa."),
      ("Pasos después de comer","Caminar 10 minutos tras almuerzo y cena favorece el tránsito y el control de la glucosa."),
      ("Infusiones","Manzanilla, anís o jengibre sin azúcar después de la cena ayudan a la sensación de pesadez."),
      ("Comer sin prisa y sin gaseosas","Sentarse a comer, evitar bebidas con gas, chicle y sorbetes: tragar aire aumenta la hinchazón."),
      ("Lavar y desinfectar","Lavar bien las verduras crudas para evitar molestias gastrointestinales."),
      ("Si persiste","Hinchazón, dolor o estreñimiento por más de 2 semanas: consultar con un profesional de salud.")]
    t=tbl([["Recomendación","Cómo aplicarla"]]+[[a,b] for a,b in tips],[W*.25,W*.75]); s.append(t)
    s.append(PageBreak())
    # --- proyeccion
    s.append(P("Proyección de 12 semanas y seguimiento","h2"))
    wts=[64.5,64.3,64.05,63.75,63.45,63.15,62.85,62.55,62.25,61.95,61.65,61.35,61.0]
    rows=[["Sem","Fechas","Peso objetivo fin de semana","Cambio","Meta kcal/día","Proteína (g)"]]
    import datetime as dt
    for w in range(1,13):
        a,b=wts[w-1],wts[w]; _,_,_,mk_=meta(a,b,w)
        f0=INICIO+dt.timedelta(days=7*(w-1)); f1=f0+dt.timedelta(days=6)
        rows.append([str(w),f"{f0:%d/%m} – {f1:%d/%m}",fm(b,2),f"−{fm(a-b,2)}",fm(mk_),fm(round(a*PERFIL['g_prot_kg']))])
    left=tbl(rows,[W*.06,W*.14,W*.17,W*.08,W*.1,W*.09],extra=[("ALIGN",(0,1),(-1,-1),"CENTER"),("BACKGROUND",(0,1),(-1,1),LIGHT)],pad=2)
    right=[P("<b>Cómo se mide el avance</b>","bl"),
      P("• Pesarse cada semana en ayunas, misma balanza y ropa. Meta de la semana 1: <b>64,3 kg</b>. Se decide con el promedio de 2 semanas (±0,5 kg por agua es normal).","b"),
      P("• El fin de semana se envían fotos de cada comida: se estiman cantidades y se vuelcan en el Excel de seguimiento, que muestra % de cumplimiento y cuántas kcal/proteína faltan o sobran.","b"),
      P("• El ritmo es gradual (0,20 → 0,25 → 0,30 kg/sem) porque venía de un consumo alto de carbohidratos y entrena: una baja brusca afectaría fuerza y recuperación.","b"),
      P("• Si el rendimiento en gym baja 2 semanas seguidas, se sube 150 kcal de carbohidrato antes de entrenar durante 1 semana.","b"),
      P("• Las calorías bajan solo con palancas pequeñas (queso 100 g, carbohidrato 1/4 en cena, etc.) descritas en el Excel, hoja Reglas.","b"),
      Spacer(1,4),P("Supuestos a confirmar: edad (25 años), peso por rebanada/scoop y días exactos de entrenamiento.","bi")]
    t=Table([[left,right]],colWidths=[W*.64,W*.36]); t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(1,0),(1,0),12)])); s.append(t)
    s.append(PageBreak())
    # --- anexo TPCA
    s.append(P("Anexo: valores TPCA utilizados (por 100 g)","h2"))
    s.append(P("Fuente: Tablas Peruanas de Composición de Alimentos, INS/CENAN (versión 2017, publicación 2019). El aceite de oliva es un valor estándar fuera de la TPCA.","bi"))
    rows=[["Alimento","Cód.","Estado","kcal","P (g)","G (g)","C (g)"]]
    for k,v in F.items(): rows.append([v[0],v[5],v[6].split("/")[0],fm(v[1]),fm(v[2],1),fm(v[3],1),fm(v[4],1)])
    half=(len(rows)-1+1)//2+1
    def mini(rr): return tbl([rows[0]]+rr,[W*.175,W*.05,W*.065,W*.04,W*.045,W*.05,W*.05],extra=[("ALIGN",(1,1),(-1,-1),"CENTER")],pad=1.5)
    t=Table([[mini(rows[1:half]),mini(rows[half:])]],colWidths=[W*.5,W*.5]); t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")])); s.append(t)
    doc.build(s)

# =============================== PDF CLIENTE ===============================
def cliente():
    doc,W=mk(os.path.join(ROOT,"Semana1_Cliente_12-18oct.pdf"),"Mi plan · Semana 1 (12–18 octubre)")
    s=[]
    s.append(P("Mi plan de alimentación","h1"))
    s.append(P("Semana 1 · del 12 al 18 de octubre · Meta de la semana: <b>64,3 kg</b>","big"))
    s.append(Spacer(1,6))
    d=plate(150)
    reglas=[P("<b>Almuerzo y cena: arma tu plato en tres partes</b>","bl"),
      P("<b>1/3 Carbohidrato</b> — 2 papas grandes <b>o</b> 3 cucharones de arroz <b>o</b> fideos que cubran esa tercera parte.","bl"),
      P("<b>1/3 Proteína</b> — 1 palma de tu mano (pollo, pescado, res, atún o huevos).","bl"),
      P("<b>1/3 Ensalada</b> — 2 tazas de verduras con limón.","bl"),
      Spacer(1,4),
      P("<b>Todos los días</b>: 3 tomatodos de agua · ½ palta <b>o</b> 150 g de queso fresco (repartido entre desayuno y merienda).","bl")]
    img=Image(IMG,width=50*mm,height=50*mm*427/380)
    t=Table([[d,reglas,[img,P("Tu plato de referencia","sm")]]],colWidths=[W*.25,W*.5,W*.25]); t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")])); s.append(t)
    s.append(Spacer(1,8))
    comidas=[["Comida","Qué comer"],
      ["Desayuno","3 rebanadas de pan de molde + 1 scoop de avena (+ ¼ palta o 75 g de queso fresco)"],
      ["Almuerzo","1/3 carbohidrato + 1/3 proteína + 1/3 ensalada, con 1 cdta de aceite de oliva"],
      ["Merienda","2 rebanadas de pan de molde + 2 scoops de avena (+ ¼ palta o 75 g de queso fresco)  ·  los días de gym, 60–90 min antes de entrenar"],
      ["Cena","1/3 carbohidrato + 1/3 proteína + 1/3 ensalada"]]
    s.append(tbl(comidas,[W*.15,W*.85],pad=5))
    s.append(Spacer(1,8))
    s.append(P("Cómo medir sin balanza","h2"))
    med=[["Medida","Cómo verla"],["Palma de proteína","Del tamaño y grosor de tu palma, sin contar los dedos (≈ 150 g crudo)."],
     ["Cucharón de arroz","Un cucharón de servir mediano, al ras. Tres cucharones = la tercera parte del plato."],
     ["Papa grande","Del tamaño de un puño grande, pelada. Dos papas = la tercera parte del plato."],
     ["Scoop de avena","Un scoop al ras, sin colmar."],["Tomatodo","3 al día: uno en la mañana, uno en la tarde y uno en la noche (más si entrenas)."]]
    s.append(tbl(med,[W*.2,W*.8],pad=3))
    s.append(PageBreak())
    # menu
    s.append(P("Menú de la semana","h2"))
    rows=[["Día","Desayuno","Almuerzo","Merienda","Cena","Palta o queso (total del día)"]]
    def short(c,p,e):
        cs={"arroz":"Arroz (3 cucharones)","papa":"Papas sancochadas (2 grandes)","fideo":"Fideos (1/3 del plato)"}[c]
        ps={"pollo":"Pechuga de pollo a la plancha","polloP":"Muslo de pollo sin piel al horno","res":"Bistec de res magro","tilapia":"Tilapia a la plancha","trucha":"Trucha al horno","bonito":"Bonito a la plancha","merluza":"Merluza a la plancha","atun":"Atún en agua (1 lata)","huevo":"2 huevos + 3 claras sancochados"}[p]
        es=ENS[e][0].split(": ")[0]+" ("+ENS[e][0].split(": ")[1]+")"
        return f"{cs}<br/>{ps}<br/>Ensalada {es.lower()}"
    for n,dd,ci,ms,tot in DAYS:
        ex="½ palta" if dd["grasa"]=="palta" else "150 g queso fresco"
        des="3 rebanadas pan de molde<br/>1 scoop de avena<br/>"+("¼ palta" if dd["grasa"]=="palta" else "75 g queso fresco")
        mer="2 rebanadas pan de molde<br/>2 scoops de avena<br/>"+("¼ palta" if dd["grasa"]=="palta" else "75 g queso fresco")
        rows.append([f"<b>{n}</b>",des,short(*dd["alm"]),mer,short(*dd["cen"]),f"{ex}<br/>Agua: ☐ ☐ ☐"])
    t=tbl(rows,[W*.09,W*.17,W*.24,W*.17,W*.21,W*.12],pad=3,extra=[("VALIGN",(0,1),(-1,-1),"TOP")])
    s.append(t)
    s.append(Spacer(1,3))
    s.append(P("Aceite de oliva: 1 cucharadita en la ensalada del almuerzo. Marca ☐ cada tomatodo terminado.","bi"))
    s.append(PageBreak())
    # variedad
    s.append(P("¿No tienes algún alimento? Cámbialo por otro de la misma fila","h2"))
    var=[["Elige uno (misma cantidad por plato)"],
     ]
    data=[["Grupo","Opciones intercambiables"],
     ["1/3 Carbohidrato","2 papas grandes (300 g) · 3 cucharones de arroz · fideos que cubran 1/3 del plato · camote sancochado (1 grande, 250 g) · quinua cocida (1½ tazas)"],
     ["1/3 Proteína<br/>(1 palma ≈ 150 g crudo)","Pechuga de pollo · muslo sin piel (150 g) · bistec de res magro (140 g) · tilapia · trucha (150 g) · bonito (130 g) · merluza (180 g, 1 filete grande) · atún en agua (1 lata) · 2 huevos + 3 claras"],
     ["Si no comes carne","Lentejas cocidas (1½ tazas) o garbanzos (1½ tazas): llevan carbohidrato, así que reduce a la mitad el arroz/papa/fideo del plato."],
     ["Ensalada (2 tazas)","Lechuga + tomate + zanahoria · brócoli al vapor + zanahoria + pimiento · col + betarraga + tomate · espinaca + tomate + vainita · coliflor al vapor + lechuga + zanahoria"],
     ["Pan de molde (3 rebanadas)","2 panes franceses chicos (≈ 85 g)"],
     ["Avena (1 scoop)","1 scoop de hojuelas de quinua (≈ 22 g)"],
     ["Grasa del día","½ palta (4 a 5 días) <b>o</b> 150 g de queso fresco (máximo 2 días a la semana)"]]
    s.append(tbl(data,[W*.2,W*.8],pad=5))
    s.append(Spacer(1,10))
    s.append(P("Consejos para digerir mejor la ensalada","h2"))
    tips=["Empieza el plato por la ensalada y mastica bien.","Brócoli, coliflor y col: al vapor 3–5 minutos, caen mejor que crudos.",
          "Aliña con limón y 1 cdta de aceite de oliva.","Toma el agua repartida en el día; durante la comida solo sorbos.",
          "Camina 10 minutos después del almuerzo y de la cena.","Una infusión de manzanilla, anís o jengibre sin azúcar después de cenar.",
          "Si te hincha, reduce la ensalada cruda a 1½ tazas por unos días y vuelve a subir."]
    s.append(tbl([["Consejo"]]+[[f"✓ {x}"] for x in tips],[W],pad=3))
    s.append(Spacer(1,8))
    s.append(P("<b>Fin de semana:</b> envía una foto de cada comida del sábado y domingo y tu peso en ayunas del domingo. Con eso ajustamos la siguiente semana.","bl"))
    doc.build(s)
tecnico(); cliente(); print("ok")
