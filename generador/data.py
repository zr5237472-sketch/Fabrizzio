import datetime as dt
# ---------- Perfil / supuestos ----------
PERFIL = dict(sexo="Mujer", edad=25, talla_cm=165, peso0=64.5, peso_meta=61.0,
              pal=1.35, g_prot_kg=1.6, g_grasa_kg=0.8, piso_kcal=1500)
INICIO = dt.date(2026,10,12)  # lunes
# gramos por medida casera (editables en Excel)
MEDIDAS = {
 "rebanada": 25,   # g por rebanada de pan de molde
 "scoop": 25,      # g de avena hojuela cruda por scoop
 "cucharon": 70,   # g de arroz cocido por cucharon
 "papa": 150,      # g de papa pelada y sancochada por papa grande
 "palma": 150,     # g de proteina cruda por palma
}
# ---------- Base de alimentos (por 100 g) TPCA 2017/2019 INS-Peru ----------
# clave: (nombre, kcal, prot, grasa, carb, codigo TPCA, estado)
F = {
 "pan_molde":   ("Pan de molde",                       317, 6.8, 2.5,69.2,"A-47","listo"),
 "pan_frances": ("Pan francés fortificado",            277, 8.4, 0.2,62.9,"A-49","listo"),
 "avena":       ("Avena, hojuela cruda",               333,13.3, 4.0,72.2,"A-7","crudo"),
 "quinua_hoj":  ("Quinua, hojuelas de",                376,13.9, 7.4,63.1,"A-59","crudo"),
 "arroz":       ("Arroz pilado cocido",                115, 2.4, 0.1,25.2,"A-2","cocido"),
 "papa":        ("Papa blanca (pelada, sancochada)",    87, 2.1, 0.1,22.3,"U-19","cocido"),
 "papa_amar":   ("Papa amarilla sin cáscara",          101, 2.0, 0.4,23.3,"U-18","cocido"),
 "camote":      ("Camote amarillo sin cáscara",         95, 2.0, 0.0,23.4,"U-3","cocido"),
 "fideo":       ("Fideo tallarín sancochado",           90, 3.1, 0.0,21.3,"A-23","cocido"),
 "quinua_coc":  ("Quinua cocida",                       89, 2.8, 1.3,16.3,"A-53","cocido"),
 "pollo_pech":  ("Pollo, pechuga sin piel (cruda)",    108,19.2, 2.9, 0.0,"F-20","crudo"),
 "pollo_pulpa": ("Pollo, carne pulpa (cruda)",         119,21.4, 3.1, 0.0,"F-26","crudo"),
 "res_pulpa":   ("Res, carne pulpa (cruda)",           105,21.3, 1.6, 0.0,"F-35","crudo"),
 "tilapia":     ("Pescado tilapia (crudo)",             96,20.1, 1.7, 0.0,"E-77","crudo"),
 "trucha":      ("Pescado trucha (fresca)",            111,19.5, 3.1, 0.0,"E-83","crudo"),
 "bonito":      ("Pescado bonito (crudo)",             138,23.4, 4.2, 0.0,"E-27","crudo"),
 "merluza":     ("Pescado merluza (fresca)",            72,15.8, 0.5, 0.0,"E-57","crudo"),
 "atun_agua":   ("Atún enlatado en agua (escurrido)",  116,25.5, 0.8, 0.0,"E-20","listo"),
 "huevo":       ("Huevo entero sancochado",            145,12.8, 9.9, 0.0,"J-3","cocido"),
 "clara":       ("Clara de huevo sancochada",           55,11.9, 0.3, 0.0,"J-10","cocido"),
 "lenteja":     ("Lentejas chicas cocidas",             65, 6.4, 0.1,18.3,"T-53","cocido"),
 "garbanzo":    ("Garbanzo cocido",                    127, 6.9, 2.5,27.8,"T-43","cocido"),
 "queso":       ("Queso fresco de vaca",               264,17.5,20.1, 3.3,"G-14","listo"),
 "palta":       ("Palta (pulpa)",                      130, 1.7,12.5, 5.6,"C-55","crudo"),
 "lechuga":     ("Lechuga americana",                    7, 0.6, 0.1, 2.4,"B-53","crudo"),
 "tomate":      ("Tomate",                              15, 0.8, 0.2, 4.3,"B-79","crudo"),
 "zanahoria":   ("Zanahoria",                           19, 1.0, 0.3, 7.6,"B-85","crudo"),
 "brocoli":     ("Brócoli",                             32, 3.9, 1.3, 4.0,"B-21","crudo/vapor"),
 "pimiento":    ("Pimiento rojo",                       27, 1.2, 1.3, 4.6,"B-69","crudo"),
 "col":         ("Col crespa o repollo",                15, 1.5, 0.3, 4.9,"B-32","crudo"),
 "betarraga":   ("Betarraga",                           18, 2.0, 0.3, 5.4,"U-31","crudo/cocida"),
 "espinaca":    ("Espinaca blanca",                     24, 1.9, 0.6, 6.3,"B-44","crudo"),
 "vainita":     ("Vainitas",                            25, 2.4, 0.3, 8.1,"B-84","cocida"),
 "coliflor":    ("Coliflor sin tallo ni hojas",         17, 2.2, 0.6, 4.4,"B-38","crudo/vapor"),
 "cebolla":     ("Cebolla blanca",                      24, 0.9, 0.1, 7.4,"B-26","crudo"),
 "aceite":      ("Aceite de oliva (valor estándar, no TPCA)",884,0,100,0,"EST","—"),
}
# ---------- Ensaladas (g crudos) ----------
ENS = {
 "A": ("Fresca: lechuga + tomate + zanahoria", {"lechuga":80,"tomate":80,"zanahoria":40}),
 "B": ("Vapor: brócoli + zanahoria + pimiento",  {"brocoli":100,"zanahoria":50,"pimiento":50}),
 "C": ("Crujiente: col + betarraga + tomate", {"col":80,"betarraga":50,"tomate":70}),
 "D": ("Verde: espinaca + tomate + vainita",     {"espinaca":60,"tomate":70,"vainita":70}),
 "E": ("Suave: coliflor + lechuga + zanahoria",  {"coliflor":100,"lechuga":60,"zanahoria":40}),
}
# ---------- Porciones de proteina (g crudo salvo atun/huevo) ----------
PROT = {
 "pollo":  ("Pechuga de pollo a la plancha", {"pollo_pech":150}),
 "polloP": ("Pollo (muslo sin piel) al horno", {"pollo_pulpa":150}),
 "res":    ("Bistec de res magro (pulpa)", {"res_pulpa":140}),
 "tilapia":("Tilapia a la plancha", {"tilapia":150}),
 "trucha": ("Trucha al horno", {"trucha":150}),
 "bonito": ("Bonito a la plancha", {"bonito":130}),
 "merluza":("Merluza a la plancha", {"merluza":180}),
 "atun":   ("Atún en agua (1 lata escurrida)", {"atun_agua":120}),
 "huevo":  ("2 huevos + 3 claras sancochados", {"huevo":100,"clara":100}),
}
CARB = {
 "arroz": ("Arroz blanco (3 cucharones)",   {"arroz":210}),
 "papa":  ("Papa sancochada (2 grandes)",    {"papa":300}),
 "fideo": ("Fideos (cubren 1/3 del plato)",  {"fideo":250}),
 "camote":("Camote sancochado",              {"camote":250}),
}
# ---------- Menú semana 1 ----------
DIAS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
# (carb, prot, ens) almuerzo / cena ; grasa: palta o queso
MENU = [
 dict(alm=("arroz","pollo","A"), cen=("papa","tilapia","B"), grasa="palta"),
 dict(alm=("fideo","res","C"),   cen=("arroz","pollo","D"),  grasa="palta"),
 dict(alm=("papa","pollo","A"),  cen=("fideo","atun","E"),   grasa="queso"),
 dict(alm=("arroz","trucha","B"),cen=("papa","huevo","C"),   grasa="palta"),
 dict(alm=("fideo","polloP","D"),cen=("arroz","res","A"),    grasa="palta"),
 dict(alm=("papa","merluza","E"),cen=("arroz","pollo","B"),  grasa="queso"),
 dict(alm=("arroz","bonito","C"),cen=("fideo","atun","D"),   grasa="palta"),
]
PAN_DES, AV_DES, PAN_MER, AV_MER = 3,1,2,2
ACEITE_G = 5  # 1 cdta al dia (almuerzo)
GRASA = {"palta":{"palta":90}, "queso":{"queso":150}}

def macros(items):
    k=p=g=c=0
    for key,gr in items.items():
        _,kc,pr,gs,ch,_,_=F[key]; f=gr/100
        k+=kc*f;p+=pr*f;g+=gs*f;c+=ch*f
    return k,p,g,c
def add(*ms): return tuple(sum(x) for x in zip(*ms))
def merge(*ds):
    o={}
    for d in ds:
        for k,v in d.items(): o[k]=o.get(k,0)+v
    return o
def comida_items(d):
    des={"pan_molde":PAN_DES*MEDIDAS["rebanada"],"avena":AV_DES*MEDIDAS["scoop"]}
    mer={"pan_molde":PAN_MER*MEDIDAS["rebanada"],"avena":AV_MER*MEDIDAS["scoop"]}
    g=GRASA[d["grasa"]]
    if d["grasa"]=="palta":
        des=merge(des,{"palta":g["palta"]/2}); mer=merge(mer,{"palta":g["palta"]/2})
    else:
        des=merge(des,{"queso":g["queso"]/2}); mer=merge(mer,{"queso":g["queso"]/2})
    def la(t,oil):
        c,p,e=t
        it=merge(list(CARB[c][1].items()) and CARB[c][1],PROT[p][1],ENS[e][1])
        if oil: it=merge(it,{"aceite":ACEITE_G})
        return it
    return dict(des=des,alm=la(d["alm"],True),mer=mer,cen=la(d["cen"],False))
if __name__=="__main__":
    tot=[]
    for n,d in zip(DIAS,MENU):
        ci=comida_items(d); ms={k:macros(v) for k,v in ci.items()}
        t=add(*ms.values()); tot.append(t)
        print(n, {k:round(v[0]) for k,v in ms.items()}, "TOTAL kcal %.0f P %.0f G %.0f C %.0f"%t)
    avg=[sum(x)/7 for x in zip(*tot)]
    print("PROMEDIO kcal %.0f P %.0f G %.0f C %.0f"%tuple(avg))
    import datetime; print(INICIO.strftime("%A"))
