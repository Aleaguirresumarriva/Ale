"""
Construye el Diccionario Maestro de Metadatos Jurídicos de Juztina (Etapa 2).
Uso:  python3 construir_excel.py   (desde esta carpeta)
Entrada: esquema.py, catalogos_nucleo.py, campos_g1.py ... campos_g5.py
Salida:  ../Juztina_Diccionario_Maestro_Metadatos_v1.0.xlsx  y  ../fuente/estadisticas.json
"""
import importlib.util, json, os, re, sys
from collections import Counter, defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import esquema as E
import catalogos_nucleo as CN

OUT = os.path.join(HERE, "..", "Juztina_Diccionario_Maestro_Metadatos_v1.0.xlsx")
VERSION = "1.0"
FECHA = "2026-11-24"

# ----------------------------------------------------------------------------- carga
def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

FIELDS, CATS, RELS, SRC = [], list(CN.CATALOGS), [], {}
for g in range(1, 7):
    p = os.path.join(HERE, f"campos_g{g}.py")
    if not os.path.exists(p):
        print("AVISO: falta", p); continue
    m = load(p)
    for f in m.FIELDS:
        SRC[f["id"]] = f"g{g}"
    FIELDS += m.FIELDS
    CATS += getattr(m, "CATALOGS", [])
    RELS += getattr(m, "REL_TYPES", [])
META = CN.meta_catalogs()

# ----------------------------------------------------------------------------- integración (ver integracion.py)
import integracion as IG
import taxonomia as TX
def redirect(text):
    for old, (new, _) in IG.RETIRADOS.items():
        text = text.replace(old, new)
    for old, (new, _) in IG.CAT_RETIRADOS.items():
        text = text.replace(old, new)
    return text
FIELDS = [f for f in FIELDS if f["id"] not in IG.RETIRADOS]
for f in FIELDS:
    for k in list(f):
        if isinstance(f[k], str):
            f[k] = redirect(f[k])
    if f["deps"]:
        seen, toks = set(), []
        for t in f["deps"].split("; "):
            if t not in seen:
                seen.add(t); toks.append(t)
        f["deps"] = "; ".join(toks)
    if f["id"] in IG.AJUSTES:
        f.update(IG.AJUSTES[f["id"]])
R1_AJUSTADOS = [f["id"] for f in FIELDS if IG.aplicar_regla_r1(f)]
print("Regla R1 aplicada a", len(R1_AJUSTADOS), "campos")
CATS = [c for c in CATS if c["cat_id"] not in IG.CAT_RETIRADOS]
for c in CATS:
    c["cat_def"] = redirect(c["cat_def"])
    for v in c["values"]:
        for k in ("definition", "notes", "parent", "synonyms"):
            if isinstance(v.get(k), str):
                v[k] = redirect(v[k])
    if c["cat_id"] in IG.CAT_RENOMBRES:
        c["cat_name"] = IG.CAT_RENOMBRES[c["cat_id"]]
    if c["cat_id"] in IG.CAT_NOTAS:
        c["cat_def"] += IG.CAT_NOTAS[c["cat_id"]]
    c["values"] += [dict(v, parent="", synonyms="", country="", status=CN.DEF, notes="Integración")
                    for v in IG.CAT_VALORES_AGREGADOS.get(c["cat_id"], [])]
for rel in RELS:
    for k in list(rel):
        if isinstance(rel[k], str):
            rel[k] = redirect(rel[k])

DIM_ORDER = list(E.DIMENSIONES)
FIELDS.sort(key=lambda f: (DIM_ORDER.index(f["id"].split("-")[1]), f["id"]))
for f in FIELDS:  # dimensión: se guarda la etiqueta legible
    f["dim_label"] = E.DIMENSIONES[f["dim"]]

# ----------------------------------------------------------------------------- QC en Python
qc = []
ids = Counter(f["id"] for f in FIELDS); techs = Counter(f["tech"] for f in FIELDS)
qc.append(("IDs de campo duplicados", sum(1 for v in ids.values() if v > 1)))
qc.append(("Nombres técnicos duplicados", sum(1 for v in techs.values() if v > 1)))
funcnames = Counter(f["func"].strip().lower() for f in FIELDS)
qc.append(("Nombres funcionales duplicados", sum(1 for v in funcnames.values() if v > 1)))
cat_ids = Counter(c["cat_id"] for c in CATS + META)
qc.append(("IDs de catálogo duplicados", sum(1 for v in cat_ids.values() if v > 1)))
known = set(cat_ids) | set(IG.CAT_RETIRADOS) | {"CAT-330", "CAT-331"}  # retirados (menciones históricas) y catálogos con hoja propia (5b, 5c)
bad_refs = sorted({(f["id"], r) for f in FIELDS for k in ("values", "validation", "extraction", "obs", "applicability", "deps")
                   for r in re.findall(r"CAT-\d{3}", str(f[k])) if r not in known})
qc.append(("Referencias a catálogos inexistentes", len(bad_refs)))
fids = set(ids)
bad_field_refs = sorted({(f["id"], r) for f in FIELDS for k in ("deps", "obs", "extraction", "validation")
                         for r in re.findall(r"MDJ-(?:D\d\d|PRO|OPE)-\d{3}", str(f[k])) if r not in fids})
qc.append(("Referencias a campos inexistentes", len(bad_field_refs)))
rel_codes = Counter(r["code"] for r in RELS)
qc.append(("Códigos de relación duplicados", sum(1 for v in rel_codes.values() if v > 1)))
empty_vals = sum(1 for c in CATS for v in c["values"] if not (v.get("code") and v.get("label") and v.get("definition")))
qc.append(("Valores de catálogo sin código, etiqueta o definición", empty_vals))
val_dups = sum(1 for c in CATS for k, n in Counter(v["code"] for v in c["values"]).items() if n > 1)
qc.append(("Códigos duplicados dentro de un catálogo", val_dups))
for label, n in qc:
    print(f"QC {label}: {n}")
if bad_refs: print("  refs catálogo:", bad_refs[:30])
if bad_field_refs: print("  refs campo:", bad_field_refs[:30])

# ----------------------------------------------------------------------------- estilos
ARIAL = "Arial"
HDR_FILL = PatternFill("solid", fgColor="1F3864")
SUB_FILL = PatternFill("solid", fgColor="D9E1F2")
TITLE_FONT = Font(name=ARIAL, size=14, bold=True, color="1F3864")
H2_FONT = Font(name=ARIAL, size=11, bold=True, color="1F3864")
HDR_FONT = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
BODY = Font(name=ARIAL, size=10)
BOLD = Font(name=ARIAL, size=10, bold=True)
LINK = Font(name=ARIAL, size=10, color="008000")  # vínculos a otra hoja (convención)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

wb = Workbook()
wb.remove(wb.active)
M = "'2_Diccionario_maestro'"

def sheet(name):
    return wb.create_sheet(name)

def header(ws, row, labels, widths=None):
    for i, lab in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = CENTER; c.border = BORDER
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w

def body(c, bold=False, center=False, font=None):
    c.font = font or (BOLD if bold else BODY)
    c.alignment = CENTER if center else WRAP
    c.border = BORDER

def finish(ws, hdr_row, last_col, last_row, freeze_col="B"):
    ws.freeze_panes = f"{freeze_col}{hdr_row + 1}"
    ws.auto_filter.ref = f"A{hdr_row}:{get_column_letter(last_col)}{max(last_row, hdr_row + 1)}"

def lk(col, r, idcol="A"):
    """Fórmula de búsqueda en el maestro por ID."""
    return f"=INDEX({M}!${col}:${col},MATCH(${idcol}{r},{M}!$A:$A,0))"

# ----------------------------------------------------------------------------- columnas del maestro
MCOLS = [k for k, _ in E.CAMPO_CLAVES]
MLAB = [l for _, l in E.CAMPO_CLAVES]
COL = {k: get_column_letter(i + 1) for i, k in enumerate(MCOLS)}
N = len(FIELDS)
LAST = N + 1  # última fila de datos en el maestro

# ============================================================================ 16 Listas (validación)
lst = sheet("16_Listas")
LISTS = {
    "dim": list(E.DIMENSIONES.values()), "unit": E.UNIDADES, "dtype": E.TIPOS_DATO, "card": E.CARDINALIDADES,
    "origin": E.ORIGENES, "prio": E.PRIORIDADES, "mode": E.MODOS, "review": E.REVISION, "privacy": E.PRIVACIDAD,
    "stage": E.ETAPAS, "risk": E.RIESGOS, "country_status": E.ESTADO_PAIS,
}
list_ref = {}
for j, (k, vals) in enumerate(LISTS.items(), 1):
    cl = get_column_letter(j)
    lst.cell(row=1, column=j, value=k)
    for i, v in enumerate(vals, 2):
        lst.cell(row=i, column=j, value=v)
    list_ref[k] = f"'16_Listas'!${cl}$2:${cl}${len(vals) + 1}"
header(lst, 1, list(LISTS.keys()), [28] * len(LISTS))

# ============================================================================ 2 Diccionario maestro
ms = sheet("2_Diccionario_maestro")
WIDTHS = dict(id=15, tech=30, func=32, dim=24, profiles=14, unit=26, defn=50, just=44, dtype=14, card=16,
              values=40, example=30, origin=22, method=22, evidence=36, extraction=55, validation=50,
              applicability=36, prio=10, mode=9, review=11, privacy=20, deps=34, funcs=20, obs=44,
              stage=11, risk=8, countries=16, country_status=18, pending=16)
header(ms, 1, MLAB, [WIDTHS[k] for k in MCOLS])
for r, f in enumerate(FIELDS, 2):
    for i, k in enumerate(MCOLS, 1):
        v = f["dim_label"] if k == "dim" else f[k]
        body(ms.cell(row=r, column=i, value=v), bold=(k == "id"))
finish(ms, 1, len(MCOLS), LAST, freeze_col="D")
ms.row_dimensions[1].height = 32
for k in LISTS:
    dv = DataValidation(type="list", formula1=f"={list_ref[k]}", allow_blank=False,
                        error="Valor fuera del vocabulario controlado", errorTitle="Valor no permitido", showErrorMessage=True)
    ms.add_data_validation(dv)
    dv.add(f"{COL[k]}2:{COL[k]}{LAST + 200}")

# ============================================================================ 1 README (se rellena al final)
readme = wb.create_sheet("1_README", 0)

# ============================================================================ 3 Campos universales
def is_universal(f):
    p = f["profiles"].split("; ")
    return "UNI" in p or all(x in p for x in ("NOR", "JUR", "ADM", "DOC"))
UNIV = [f for f in FIELDS if is_universal(f)]
us = sheet("3_Campos_universales")
us["A1"] = "Campos universales: aplicables a las cuatro categorías documentales"; us["A1"].font = TITLE_FONT
us["A2"] = ("Todas las columnas salvo el ID se leen del diccionario maestro mediante fórmulas. "
            "La columna 'Condiciones de aplicación' y 'Excepciones u observaciones' indican cuándo un campo universal no se aplica.")
us["A2"].font = BODY
hdr = ["ID del campo", "Nombre técnico", "Nombre funcional", "Dimensión", "Unidad de registro", "Perfil documental",
       "Condiciones de aplicación", "Excepciones u observaciones", "Prioridad", "Modo"]
header(us, 4, hdr, [15, 30, 32, 24, 26, 14, 50, 50, 10, 8])
src = ["tech", "func", "dim", "unit", "profiles", "applicability", "obs", "prio", "mode"]
for r, f in enumerate(UNIV, 5):
    body(us.cell(row=r, column=1, value=f["id"]), bold=True)
    for j, k in enumerate(src, 2):
        body(us.cell(row=r, column=j, value=lk(COL[k], r)), font=LINK)
finish(us, 4, len(hdr), 4 + len(UNIV))

# ============================================================================ 4 Campos por perfil
ps = sheet("4_Campos_por_perfil")
hdr = ["ID del campo", "Nombre funcional", "Dimensión", "Unidad de registro", "Perfil documental",
       "Normativa", "Jurisprudencia", "Actos administrativos", "Doctrina", "Alcance del campo"]
header(ps, 1, hdr, [15, 34, 24, 26, 16, 12, 14, 14, 11, 22])
for r, f in enumerate(FIELDS, 2):
    body(ps.cell(row=r, column=1, value=f["id"]), bold=True)
    for j, k in enumerate(["func", "dim", "unit", "profiles"], 2):
        body(ps.cell(row=r, column=j, value=lk(COL[k], r)), font=LINK)
    for j, code in enumerate(["NOR", "JUR", "ADM", "DOC"], 6):
        body(ps.cell(row=r, column=j,
                     value=f'=IF(OR(ISNUMBER(SEARCH("UNI",$E{r})),ISNUMBER(SEARCH("{code}",$E{r}))),"●","")'), center=True)
    body(ps.cell(row=r, column=10, value=(f'=IF(COUNTIF(F{r}:I{r},"●")=4,"Universal",IF(COUNTIF(F{r}:I{r},"●")=1,'
                                          f'"Específico de perfil","Compartido"))')), center=True)
finish(ps, 1, len(hdr), LAST)

# ============================================================================ 5 Catálogos (valores) y 5a índice
cs = sheet("5_Catalogos")
hdr = ["ID del catálogo", "Nombre del catálogo", "ID del valor", "Código", "Etiqueta", "Definición", "Padre",
       "Sinónimos o denominaciones alternativas", "País", "Estado del valor", "Observaciones", "Versión", "Origen"]
header(cs, 1, hdr, [11, 30, 18, 14, 30, 60, 14, 30, 8, 30, 40, 8, 12])
r = 2
for c in CATS + META:
    origin = "núcleo" if c["cat_id"] < "CAT-100" else ("metacatálogo" if c["cat_id"] >= "CAT-900" else f"g{c['cat_id'][4]}")
    for v in c["values"]:
        vals = [c["cat_id"], c["cat_name"], f'{c["cat_id"]}.{v["code"]}', v["code"], v["label"], v["definition"],
                v.get("parent", "") or "—", v.get("synonyms", "") or "—", v.get("country", "") or "Todos",
                v.get("status", "") or CN.DEF, v.get("notes", "") or "—", VERSION, origin]
        for j, x in enumerate(vals, 1):
            body(cs.cell(row=r, column=j, value=x), bold=(j == 3))
        r += 1
CAT_LAST = r - 1
finish(cs, 1, len(hdr), CAT_LAST, freeze_col="D")

ci = sheet("5a_Indice_catalogos")
hdr = ["ID del catálogo", "Nombre", "Definición y condiciones de uso", "Nº de valores", "Valores semilla pendientes de validación",
       "Campos que lo referencian", "Origen"]
header(ci, 1, hdr, [11, 34, 70, 11, 16, 14, 12])
for r, c in enumerate(CATS + META, 2):
    origin = "núcleo" if c["cat_id"] < "CAT-100" else ("metacatálogo" if c["cat_id"] >= "CAT-900" else f"g{c['cat_id'][4]}")
    body(ci.cell(row=r, column=1, value=c["cat_id"]), bold=True)
    body(ci.cell(row=r, column=2, value=c["cat_name"]))
    body(ci.cell(row=r, column=3, value=c["cat_def"]))
    body(ci.cell(row=r, column=4, value=f"=COUNTIF('5_Catalogos'!$A$2:$A${CAT_LAST},A{r})"), center=True)
    body(ci.cell(row=r, column=5, value=f"=COUNTIFS('5_Catalogos'!$A$2:$A${CAT_LAST},A{r},'5_Catalogos'!$J$2:$J${CAT_LAST},\"Semilla*\")"), center=True)
    body(ci.cell(row=r, column=6, value=f'=COUNTIF({M}!${COL["values"]}$2:${COL["values"]}${LAST},"*"&A{r}&"*")'), center=True)
    body(ci.cell(row=r, column=7, value=origin), center=True)
r = len(CATS + META) + 2
for cid, cname, cdef, cnt in [
    ("CAT-330", "Taxonomía de etiquetas jurídicas (áreas, especialidades, subespecialidades)",
     "Etiquetas para clasificar unidades y obras; valores en la hoja 5b con jerarquía, inclusiones, exclusiones, indicadores y reglas. Semilla pendiente de validación (DEC-35).",
     "=COUNTIF('5b_Taxonomia_etiquetas'!$A$5:$A$400,\"CON-*\")"),
    ("CAT-331", "Especialistas de Juztina", "Especialistas actuales y potenciales definidos como selección de etiquetas de CAT-330; valores en la hoja 5c.",
     "=COUNTIF('5c_Especialistas_Juztina'!$A$5:$A$200,\"ESP-??\")")]:
    vals = [cid, cname, cdef, cnt, cnt, f'=COUNTIF({M}!${COL["values"]}$2:${COL["values"]}${LAST},"*"&A{r}&"*")', "taxonomía"]
    for j, x in enumerate(vals, 1):
        body(ci.cell(row=r, column=j, value=x), bold=(j == 1), center=(j in (4, 5, 6, 7)))
    r += 1
finish(ci, 1, len(hdr), r - 1)


# ============================================================================ 5b Taxonomía de etiquetas y 5c Especialistas
YELLOW = PatternFill("solid", fgColor="FFF2CC")
TX_IDX = {r["id"]: r for r in TX.ROWS}
ordered = []
for a in [r for r in TX.ROWS if r["nivel"] == 1]:
    ordered.append(a)
    for e in [r for r in TX.ROWS if r["nivel"] == 2 and r["padre"] == a["id"]]:
        ordered.append(e)
        ordered += [r for r in TX.ROWS if r["nivel"] == 3 and r["padre"] == e["id"]]
assert len(ordered) == len(TX.ROWS)
def area_of(r):
    while r["nivel"] > 1:
        r = TX_IDX[r["padre"]]
    return r["nombre"]
tx = sheet("5b_Taxonomia_etiquetas")
tx["A1"] = "Taxonomía de etiquetas jurídicas (CAT-330) · semilla v0.1 pendiente de validación"; tx["A1"].font = TITLE_FONT
tx["A2"] = ("Lista de etiquetas con que la IA marcará cada unidad (artículo, problema jurídico, punto resolutivo…) y, por agregación, cada obra. "
            "Un documento puede llevar tantas etiquetas como materias trate de verdad, cada una como principal o secundaria (MDJ-D06-006). "
            "Las celdas amarillas son para el equipo jurídico: marque cada fila y agregue al final las etiquetas que falten.")
tx["A2"].font = BODY; tx["A2"].alignment = WRAP; tx.merge_cells("A2:P2"); tx.row_dimensions[2].height = 44
TXH = ["ID de la etiqueta", "Nivel", "Tipo", "Etiqueta", "Área principal", "Padre (ID)", "Padre", "También pertenece a (IDs)",
       "Gran área (F1)", "Incluye", "Excluye", "Indicadores para la IA", "Denominaciones alternativas", "Sector vinculado",
       "Regla (etiquetas sectoriales)", "Especialista Juztina actual", "Nº de especialistas que la usan", "Estado",
       "Validación del equipo jurídico", "Comentarios"]
header(tx, 4, TXH, [14, 7, 20, 34, 26, 14, 28, 22, 22, 50, 40, 50, 24, 22, 40, 22, 12, 22, 20, 36])
TX_LAST_DATA = 4 + len(ordered)
for i, rw in enumerate(ordered, 5):
    vals = [rw["id"], rw["nivel"], rw["tipo"], rw["nombre"], area_of(rw), rw["padre"],
            (f'=IFERROR(INDEX($D$5:$D${TX_LAST_DATA},MATCH(F{i},$A$5:$A${TX_LAST_DATA},0)),"—")' if rw["padre"] != "—" else "—"),
            rw["otros"], rw["ga"], rw["incluye"], rw["excluye"], rw["indicadores"], rw["sinonimos"], rw["sector"], rw["regla"],
            rw["actual"], None, "Semilla — pendiente de validación (DEC-35)", "", ""]
    for j, x in enumerate(vals, 1):
        c = tx.cell(row=i, column=j, value=x)
        body(c, bold=(j in (1, 4) and rw["nivel"] == 1) or j == 1, center=(j in (2, 17)))
        if rw["nivel"] == 1:
            c.fill = SUB_FILL
    body(tx.cell(row=i, column=17, value=f"=COUNTIF('5c_Especialistas_Juztina'!$D$5:$D$200,\"*\"&A{i}&\"*\")"), center=True)
    if rw["nivel"] == 1:
        tx.cell(row=i, column=17).fill = SUB_FILL
    for j in (19, 20):
        tx.cell(row=i, column=j).fill = YELLOW
NEW_ROWS = 30
for k in range(1, NEW_ROWS + 1):
    i = TX_LAST_DATA + k
    for j in range(1, len(TXH) + 1):
        c = tx.cell(row=i, column=j, value=(f"NUEVA-{k:02d}" if j == 1 else ("Propuesta nueva" if j == 18 else None)))
        body(c); c.fill = YELLOW
TX_END = TX_LAST_DATA + NEW_ROWS
dvv = DataValidation(type="list", formula1='"OK,Falta subdividir,Sobra (eliminar),Renombrar,Mover a otra área,Fusionar con otra,Nueva etiqueta"', allow_blank=True)
tx.add_data_validation(dvv); dvv.add(f"S5:S{TX_END}")
dvn = DataValidation(type="list", formula1='"1,2,3"', allow_blank=True)
tx.add_data_validation(dvn); dvn.add(f"B{TX_LAST_DATA + 1}:B{TX_END}")
finish(tx, 4, len(TXH), TX_END, freeze_col="E")

es = sheet("5c_Especialistas_Juztina")
es["A1"] = "Especialistas de Juztina definidos como selección de etiquetas (CAT-331)"; es["A1"].font = TITLE_FONT
es["A2"] = ("Cada especialista toma las unidades y obras que tengan alguna de sus etiquetas (o una etiqueta descendiente) con la relevancia mínima indicada. "
            "Crear un especialista nuevo no exige reprocesar el corpus: basta con definir aquí sus etiquetas. Las celdas amarillas son para validación.")
es["A2"].font = BODY; es["A2"].alignment = WRAP; es.merge_cells("A2:L2"); es.row_dimensions[2].height = 36
ESH = ["ID", "Especialista", "Estado", "Etiquetas incluidas (IDs)", "Etiquetas incluidas (nombres)", "Nº de etiquetas directas",
       "Incluye etiquetas descendientes", "Relevancia mínima", "Etiquetas excluidas", "Regla de selección", "Observaciones",
       "Validación", "Comentarios"]
header(es, 4, ESH, [9, 26, 14, 36, 60, 11, 12, 18, 18, 70, 44, 18, 36])
for i, sp in enumerate(TX.SPECIALISTS, 5):
    names = "; ".join(TX_IDX[e]["nombre"] for e in sp["etiquetas"].split("; "))
    regla = (f"Incluir la unidad si tiene una asignación de clasificación (MDJ-D06-004/005/006) a {sp['etiquetas']} o a una etiqueta "
             f"descendiente, con relevancia {sp['relevancia'].lower()}. Incluir la obra si alguna de sus unidades cumple (MDJ-OPE-009). "
             "Para la normativa, excluir unidades con estado de vigencia 'derogada' salvo consultas históricas.")
    vals = [sp["id"], sp["nombre"], sp["estado"], sp["etiquetas"], names,
            f'=LEN(D{i})-LEN(SUBSTITUTE(D{i},";",""))+1', "Sí", sp["relevancia"], sp["excluye"], regla, sp["nota"], "", ""]
    for j, x in enumerate(vals, 1):
        body(es.cell(row=i, column=j, value=x), bold=(j in (1, 2)), center=(j in (3, 6, 7)))
    for j in (12, 13):
        es.cell(row=i, column=j).fill = YELLOW
ES_LAST = 4 + len(TX.SPECIALISTS)
for k in range(1, 16):
    i = ES_LAST + k
    for j in range(1, len(ESH) + 1):
        c = es.cell(row=i, column=j, value=(f"ESP-N{k:02d}" if j == 1 else ("Propuesta" if j == 3 else None)))
        body(c); c.fill = YELLOW
dve = DataValidation(type="list", formula1='"OK,Agregar etiquetas,Quitar etiquetas,Cambiar relevancia,Descartar"', allow_blank=True)
es.add_data_validation(dve); dve.add(f"L5:L{ES_LAST + 15}")
finish(es, 4, len(ESH), ES_LAST + 15, freeze_col="C")

# ============================================================================ 6 Aplicabilidad por país
cp = sheet("6_Aplicabilidad_pais")
hdr = ["ID del campo", "Nombre funcional", "Países", "Estado por país"] + E.PAISES + ["Validaciones pendientes"]
header(cp, 1, hdr, [15, 34, 16, 22] + [14] * 7 + [18])
for r, f in enumerate(FIELDS, 2):
    body(cp.cell(row=r, column=1, value=f["id"]), bold=True)
    for j, k in enumerate(["func", "countries", "country_status"], 2):
        body(cp.cell(row=r, column=j, value=lk(COL[k], r)), font=LINK)
    for j, pc in enumerate(E.PAISES, 5):
        body(cp.cell(row=r, column=j, value=f'=IF(OR($C{r}="ALL",ISNUMBER(SEARCH("{pc}",$C{r}))),$D{r},"No aplica")'), center=True)
    body(cp.cell(row=r, column=12, value=lk(COL["pending"], r)), font=LINK)
finish(cp, 1, len(hdr), LAST)

# ============================================================================ 13 Reglas generales (antes que 7 por la tabla de criterios)
rg = sheet("13_Reglas_generales")
rg["A1"] = "Reglas generales de extracción, validación y control"; rg["A1"].font = TITLE_FONT
RISK_CRIT = [
    ("R1", "Evidencia literal verificada por coincidencia exacta + acuerdo entre dos extracciones independientes + precisión de piloto ≥ meta R1 (DEC-20). Si no, cola de revisión; no alimenta cálculos de vigencia ni de precedentes."),
    ("R2", "Evidencia verificada + confianza calculada ≥ umbral calibrado en el piloto. Si no, se guarda como 'interpretado, baja confianza' y no se usa para filtrar especialistas."),
    ("R3", "Evidencia presente. Se guarda con su modo de origen y confianza."),
]
rg["A3"] = "Criterios de aceptación por clase de riesgo"; rg["A3"].font = H2_FONT
header(rg, 4, ["Clase", "Criterio de aceptación"], [10, 120])
for i, (k, v) in enumerate(RISK_CRIT, 5):
    body(rg.cell(row=i, column=1, value=k), bold=True, center=True); body(rg.cell(row=i, column=2, value=v))
RULES = [
 ("RG-01", "Cada campo declara modo de origen, clase de riesgo, etapa, prioridad y modo de adquisición."),
 ("RG-02", "Un valor 'Explícito en documento' o 'Normalizado por regla' sin evidencia literal verificada se descarta o se degrada a 'Inferido por modelo'."),
 ("RG-03", "Lo que dice el documento y lo que concluye Juztina van en campos distintos (p. ej., operación derogatoria transcrita frente a estado de vigencia calculado)."),
 ("RG-04", "Vigencia, carácter de precedente, especialidad de práctica, continuidad presunta y monto final se calculan con reglas versionadas. Las reglas de país no validadas no se ejecutan: su resultado queda 'Indeterminado'."),
 ("RG-05", "'No determinable' y 'No aplica' son respuestas válidas; su frecuencia se mide por campo. Una abstención cercana a cero en un campo difícil indica adivinación."),
 ("RG-06", "El modelo no completa con conocimiento externo: números, fechas, valores de unidades y nombres que no están en el texto provienen de catálogos."),
 ("RG-07", "Los campos con efecto jurídico usan vocabularios cerrados (hoja 5)."),
 ("RG-08", "Ante discrepancias entre fuentes, se conservan ambas con marca de conflicto; nunca se elige una en silencio."),
 ("RG-09", "La calidad del texto fija un techo de confianza; sin calidad suficiente no puede declararse 'No encontrado' (se usa 'Indeterminado')."),
 ("RG-10", "Las afirmaciones R1 pasan por revisión humana antes de alimentar cálculos."),
 ("RG-11", "Lo inferido se identifica como tal ante el usuario, con acceso a su evidencia."),
 ("RG-12", "Toda afirmación lleva su ejecución y es revocable en bloque."),
 ("RG-13", "Cada lote tiene muestra de control y criterio de detención."),
 ("RG-14", "Un campo que no alcanza su meta de precisión en el piloto no entra en la pasada masiva."),
 ("RG-15", "Una cita no genera por sí sola una relación sustantiva: 'aplica' exige subsunción en los fundamentos; 'interpreta' exige fijación de sentido."),
 ("RG-16", "Los tramos transcritos de otros documentos se marcan como contenido ajeno y no generan clasificación, efectos ni montos propios."),
 ("RG-17", "Clasificación sin topes numéricos: cada asignación principal o secundaria exige función jurídica, evidencia en sección decisiva y justificación con plantilla; un nodo y su ancestro no se asignan juntos."),
 ("RG-18", "Datos personales: minimización. Nombres de personas naturales fuera de campos estructurados en el alcance inicial (DEC-18); los indicadores de datos sensibles se extraen en P0."),
 ("RG-19", "Montos: nunca se sobrescribe el valor histórico; toda conversión o actualización es un campo calculado con regla, fuente y fecha."),
 ("RG-20", "Fechas: se distinguen fechas documentales, fechas de efecto jurídico y fechas de sistema (captura, procesamiento)."),
]
r0 = 5 + len(RISK_CRIT) + 1
rg.cell(row=r0, column=1, value="Reglas de control").font = H2_FONT
header(rg, r0 + 1, ["ID", "Regla"])
for i, (k, v) in enumerate(RULES, r0 + 2):
    body(rg.cell(row=i, column=1, value=k), bold=True, center=True); body(rg.cell(row=i, column=2, value=v))
r1 = r0 + 2 + len(RULES) + 1
rg.cell(row=r1, column=1, value="Estados de campo (CAT-006)").font = H2_FONT
header(rg, r1 + 1, ["Código", "Estado y condición"])
for i, v in enumerate(CN.CATALOGS[5]["values"], r1 + 2):
    body(rg.cell(row=i, column=1, value=v["code"]), bold=True, center=True)
    body(rg.cell(row=i, column=2, value=f'{v["label"]}: {v["definition"]}'))
RISK_RANGE = "'13_Reglas_generales'!$A$5:$B$7"

# ============================================================================ 7 Reglas de extracción y validación
rs = sheet("7_Reglas_extraccion")
hdr = ["ID del campo", "Nombre técnico", "Etapa", "Clase de riesgo", "Método de adquisición", "Regla de extracción",
       "Evidencia requerida", "Regla de validación", "Criterio de aceptación (por riesgo)", "Requiere revisión humana",
       "Excepciones y observaciones", "Dependencias"]
header(rs, 1, hdr, [15, 30, 10, 9, 22, 60, 36, 55, 55, 11, 44, 34])
srcs = ["tech", "stage", "risk", "method", "extraction", "evidence", "validation"]
for r, f in enumerate(FIELDS, 2):
    body(rs.cell(row=r, column=1, value=f["id"]), bold=True)
    for j, k in enumerate(srcs, 2):
        body(rs.cell(row=r, column=j, value=lk(COL[k], r)), font=LINK)
    body(rs.cell(row=r, column=9, value=f"=INDEX({RISK_RANGE},MATCH($D{r},'13_Reglas_generales'!$A$5:$A$7,0),2)"), font=LINK)
    for j, k in enumerate(["review", "obs", "deps"], 10):
        body(rs.cell(row=r, column=j, value=lk(COL[k], r)), font=LINK)
finish(rs, 1, len(hdr), LAST)

# ============================================================================ 8 Relaciones y 8a referencias
rl = sheet("8_Relaciones")
RK = ["code", "name", "family", "direction", "inverse", "origin_units", "target_units", "origin_mode", "evidence",
      "rule", "prio", "risk", "feeds", "symmetric", "transitive", "categories", "notes"]
RL = ["Código", "Tipo de relación", "Familia", "Direccionalidad (origen → destino)", "Inversa", "Unidades de origen",
      "Unidades de destino", "Modo de obtención", "Evidencia exigida", "Regla de identificación", "Prioridad", "Riesgo",
      "Alimenta cálculos", "Simétrica", "Transitiva", "Perfiles", "Observaciones"]
header(rl, 1, RL, [12, 26, 20, 34, 22, 22, 22, 14, 36, 55, 9, 8, 26, 9, 9, 14, 40])
for r, rel in enumerate(RELS, 2):
    for j, k in enumerate(RK, 1):
        body(rl.cell(row=r, column=j, value=rel.get(k, "—") or "—"), bold=(j == 1))
finish(rl, 1, len(RL), len(RELS) + 1)

rf = sheet("8a_Referencias")
rf["A1"] = "Referencias: tipos, información mínima y campos del diccionario"; rf["A1"].font = TITLE_FONT
REFT = [
 ("1", "Normativa", "Tipo de norma; número y año si constan; jurisdicción; alias usado; disposición citada hasta el nivel más fino; indicación de versión", "P0"),
 ("2", "Jurisprudencial", "Órgano; tipo de resolución; identificador oficial; fecha si consta; fundamento o considerando citado; invocación como precedente", "P0"),
 ("3", "Acto administrativo", "Entidad; tipo; número; fecha; si es el acto impugnado o recurrido", "P0 en jurisprudencia y actos (acto impugnado); P1 en los demás"),
 ("4", "Doctrinal o bibliográfica", "Cadena literal completa; autor y año si se reconocen; análisis bibliográfico detallado posterior", "P1 detección; P3 análisis"),
 ("5", "Cita textual o transcripción", "Límites exactos del texto transcrito; referencia a la que se atribuye; marca de contenido ajeno", "P1 límites; verificación calculada (B)"),
]
header(rf, 3, ["Tipo", "Nombre", "Información mínima", "Prioridad"], [8, 30, 90, 30])
for i, t in enumerate(REFT, 4):
    for j, x in enumerate(t, 1):
        body(rf.cell(row=i, column=j, value=x), bold=(j == 1))
REF_FIELDS = [f for f in FIELDS if f["unit"] in ("Referencia", "Relación")]
rr = 4 + len(REFT) + 2
rf.cell(row=rr - 1, column=1, value="Campos del diccionario sobre las unidades Referencia y Relación").font = H2_FONT
header(rf, rr, ["ID del campo", "Nombre funcional", "Unidad", "Definición"])
for i, f in enumerate(REF_FIELDS, rr + 1):
    body(rf.cell(row=i, column=1, value=f["id"]), bold=True)
    for j, k in enumerate(["func", "unit", "defn"], 2):
        body(rf.cell(row=i, column=j, value=lk(COL[k], i)), font=LINK)
rf.freeze_panes = "A4"

# ============================================================================ 9 Prioridad y estrategia
pr = sheet("9_Prioridad_procesamiento")
PO = {p: i for i, p in enumerate(E.PRIORIDADES)}; MO = {m: i for i, m in enumerate(E.MODOS)}
ORD = sorted(FIELDS, key=lambda f: (PO[f["prio"]], MO[f["mode"]], E.ETAPAS.index(f["stage"]), f["id"]))
hdr = ["ID del campo", "Nombre funcional", "Prioridad", "Modo de adquisición", "Etapa", "Origen del dato",
       "Conservar en el primer procesamiento", "Momento de obtención", "Depende de fuente externa", "Requiere revisión humana",
       "Validaciones pendientes"]
header(pr, 1, hdr, [15, 36, 10, 10, 11, 24, 14, 36, 13, 12, 18])
MOMENTO = ("=IF($D{r}=\"A\",\"Pasada masiva (lectura integral)\",IF($D{r}=\"B\",\"Cálculo posterior sobre campos extraídos\","
           "IF($D{r}=\"C\",\"Procesamiento posterior sobre fragmentos\",IF($D{r}=\"D\",\"Fuente externa o curaduría\","
           "\"Fuera del alcance inicial\"))))")
for r, f in enumerate(ORD, 2):
    body(pr.cell(row=r, column=1, value=f["id"]), bold=True)
    for j, k in enumerate(["func", "prio", "mode", "stage", "origin"], 2):
        body(pr.cell(row=r, column=j, value=lk(COL[k], r)), font=LINK)
    body(pr.cell(row=r, column=7, value=f'=IF($D{r}="A","Sí","No")'), center=True)
    body(pr.cell(row=r, column=8, value=MOMENTO.format(r=r)))
    body(pr.cell(row=r, column=9, value=f'=IF(OR($D{r}="D",$F{r}="Fuente externa"),"Sí","No")'), center=True)
    body(pr.cell(row=r, column=10, value=lk(COL["review"], r)), font=LINK)
    body(pr.cell(row=r, column=11, value=lk(COL["pending"], r)), font=LINK)
finish(pr, 1, len(hdr), LAST)

# ============================================================================ 10 Funcionalidades
fs = sheet("10_Funcionalidades")
FK = list(E.FUNCIONALIDADES)
hdr = ["ID del campo", "Nombre funcional", "Funcionalidades (texto)"] + [f"{k} {v}" for k, v in E.FUNCIONALIDADES.items()] + ["Nº de funcionalidades"]
header(fs, 1, hdr, [15, 34, 20] + [11] * len(FK) + [12])
NFCOL = get_column_letter(4 + len(FK))
fs.row_dimensions[1].height = 90
for r, f in enumerate(FIELDS, 2):
    body(fs.cell(row=r, column=1, value=f["id"]), bold=True)
    body(fs.cell(row=r, column=2, value=lk(COL["func"], r)), font=LINK)
    body(fs.cell(row=r, column=3, value=lk(COL["funcs"], r)), font=LINK)
    for j, k in enumerate(FK, 4):
        body(fs.cell(row=r, column=j, value=f'=IF(ISNUMBER(SEARCH("{k}",$C{r})),"●","")'), center=True)
    body(fs.cell(row=r, column=4 + len(FK), value=f'=COUNTIF(D{r}:{get_column_letter(3 + len(FK))}{r},"●")'), center=True)
tr = LAST + 1
body(fs.cell(row=tr, column=2, value="Total de campos por funcionalidad"), bold=True)
for j in range(4, 4 + len(FK)):
    cl = get_column_letter(j)
    body(fs.cell(row=tr, column=j, value=f'=COUNTIF({cl}2:{cl}{LAST},"●")'), bold=True, center=True)
finish(fs, 1, len(hdr), LAST)

# ============================================================================ 11 Pendientes
DEC_META = {
 "DEC-03": ("Jurídica por país", "Responsable jurídico de cada país", "Sin regla validada, la continuidad presunta queda 'Indeterminada' y no alimenta versiones reconstruidas."),
 "DEC-04": ("Jurídica por país", "Responsable jurídico de cada país", "El rango de TUO, textos ordenados y refundidos no se calcula; se conserva la relación 'ordena o refunde'."),
 "DEC-07": ("Producto", "Producto + especialistas por país", "Los tipos limítrofes se registran con naturaleza jurídica pero su colección queda provisional."),
 "DEC-08": ("Jurídica por país", "Responsable jurídico de cada país", "La naturaleza jurídica de tipos originales no mapeados queda 'Indeterminada'."),
 "DEC-09": ("Técnica", "Ingeniería", "Sin alineación, la recuperación del asistente no aprovecha la vigencia por unidad."),
 "DEC-11": ("Producto / técnica", "Comité taxonómico + ingeniería", "Sin umbrales, la alerta de sobreclasificación no se activa."),
 "DEC-12": ("Jurídica por materia", "Especialistas por materia", "La faceta F3 no se calcula hasta definir las reglas."),
 "DEC-13": ("Organizativa", "Dirección del proyecto", "Sin responsables, la taxonomía no puede publicarse en versión 1."),
 "DEC-14": ("Jurídica por país", "Responsables de los países involucrados", "Las correspondencias quedan como 'propuestas' y el asistente no afirma equivalencias."),
 "DEC-17": ("Jurídica por país + técnica", "Responsable jurídico de cada país + ingeniería", "El estado de vigencia se presenta solo como 'sin derogación registrada al [fecha]'."),
 "DEC-18": ("Legal y privacidad", "Área legal de Juztina por país", "Bloquea la definición final de los campos de partes y personas; mientras tanto rige la minimización."),
 "DEC-19": ("Producto + legal", "Producto y área legal", "Sin decisión, no se construyen métricas por magistrado."),
 "DEC-20": ("Producto", "Producto", "Sin metas, no puede decidirse qué campos entran en la pasada."),
 "DEC-22": ("Producto + técnica", "Producto e ingeniería", "Sin presupuesto y volumen no se fija el corte P1/P2."),
 "DEC-24": ("Técnica", "Ingeniería", "Sin insumos intermedios, la clase C exige releer documentos."),
 "DEC-25": ("Jurídica por país", "Responsable jurídico de cada país", "El carácter de precedente no se calcula; solo se conservan hechos primarios."),
 "DEC-26": ("Jurídica por país", "Responsable jurídico de cada país", "La fuerza de pronunciamientos interpretativos queda 'Indeterminada'."),
 "DEC-27": ("Legal", "Área legal", "Se limita el uso de doctrina protegida a metadatos y citas breves."),
 "DEC-28": ("Jurídica por país + técnica", "Responsable de país + ingeniería", "El ámbito territorial se registra con texto normalizado sin código oficial."),
 "DEC-29": ("Técnica + jurídica", "Ingeniería + responsable de país", "Las conversiones de unidades de valor a moneda no se calculan."),
 "DEC-30": ("Producto + jurídica", "Producto + especialistas", "Fuentes indígenas y supranacionales se modelan pero no se pueblan."),
 "DEC-31": ("Producto", "Producto", "Los campos territoriales subnacionales quedan condicionados a la cobertura real."),
 "DEC-32": ("Técnica", "Ingeniería", "Sin conocer la completitud histórica, la línea de vida se marca 'parcial'."),
 "DEC-33": ("Técnica + jurídica", "Ingeniería + responsable de país", "Los organismos se identifican sin clave auxiliar."),
 "DEC-34": ("Jurídica por país", "Responsable jurídico de cada país", "La fecha de efecto de fe de erratas queda 'Indeterminada'."),
 "DEC-35": ("Jurídica por materia + producto", "Especialistas por materia + producto", "Las etiquetas semilla se usan solo en el piloto; los especialistas nuevos no se publican hasta validar sus etiquetas."),
}
pd_ = sheet("11_Pendientes")
hdr = ["ID", "Decisión o validación pendiente", "Tipo de validación", "Responsable sugerido", "Nº de campos afectados",
       "IDs de campos afectados", "Catálogos afectados", "Impacto mientras no se resuelva", "Estado"]
header(pd_, 1, hdr, [9, 46, 22, 30, 12, 60, 30, 60, 12])
cat_by_dec = defaultdict(set)
for c in CATS:
    for v in c["values"]:
        for d in re.findall(r"DEC-\d\d", (v.get("notes", "") or "") + " " + (v.get("status", "") or "")):
            cat_by_dec[d].add(c["cat_id"])
    for d in re.findall(r"DEC-\d\d", c["cat_def"]):
        cat_by_dec[d].add(c["cat_id"])
for r, (d, desc) in enumerate(E.DECISIONES.items(), 2):
    t, resp, imp = DEC_META[d]
    affected = [f["id"] for f in FIELDS if d in f["pending"].split("; ")]
    vals = [d, desc, t, resp, f'=COUNTIF({M}!${COL["pending"]}$2:${COL["pending"]}${LAST},"*"&A{r}&"*")',
            "; ".join(affected) or "Ninguno", "; ".join(sorted(cat_by_dec[d])) or "—", imp, "Pendiente"]
    for j, x in enumerate(vals, 1):
        body(pd_.cell(row=r, column=j, value=x), bold=(j == 1), center=(j in (5, 9)))
nd = len(E.DECISIONES) + 1
r = nd + 2
pd_.cell(row=r, column=1, value="Valores de catálogo sembrados pendientes de validación nacional, por país").font = H2_FONT
header(pd_, r + 1, ["País", "Valores semilla pendientes"])
for i, pc in enumerate(E.PAISES + ["Todos"], r + 2):
    body(pd_.cell(row=i, column=1, value=pc), bold=True)
    body(pd_.cell(row=i, column=2, value=f"=COUNTIFS('5_Catalogos'!$I$2:$I${CAT_LAST},A{i},'5_Catalogos'!$J$2:$J${CAT_LAST},\"Semilla*\")"), center=True)
pd_.freeze_panes = "B2"; pd_.auto_filter.ref = f"A1:I{nd}"

# ============================================================================ 14 Unidades y etapas
ue = sheet("14_Unidades_y_etapas")
ue["A1"] = "Unidades de registro, afirmaciones compuestas, entidades de referencia y etapas"; ue["A1"].font = TITLE_FONT
UDEF = {
 "Obra": "Acto jurídico abstracto con identidad estable (p. ej., la Ley 29783 como tal). Identidad: jurisdicción + emisor + tipo original + identificador oficial.",
 "Versión": "Texto completo de la obra en un intervalo de tiempo; la origina un evento de cambio de texto.",
 "Manifestación": "Archivo concreto de una fuente concreta (hash + fuente + fecha de captura). Única unidad existente al iniciar la pasada.",
 "Unidad estructural": "Parte con identidad jurídica persistente e independiente del rótulo: división rotulada (artículo, inciso) o sección funcional (fundamentos, parte resolutiva).",
 "Fragmento textual": "Texto de una unidad estructural en una versión.",
 "Proceso": "Expediente judicial o procedimiento administrativo que agrupa varias obras.",
 "Afirmación": "Valor de un campo sobre una unidad, con evidencia, modo de origen, confianza, ejecución y estado de revisión.",
 "Referencia": "Afirmación de que un tramo del texto menciona otro documento o parte de él. Hecho textual.",
 "Relación": "Afirmación de un vínculo jurídico entre dos unidades de registro; no se deduce de la sola existencia de una cita.",
 "Evidencia": "Ancla a un tramo exacto del texto de una manifestación. Dependiente de una afirmación.",
 "Ejecución": "Registro de procedencia: etapa, perfil, versiones de esquema, taxonomía, instrucciones y modelo, lote y fecha.",
}
header(ue, 3, ["Unidad", "Clase", "Definición", "Nº de campos"], [44, 26, 90, 12])
for i, u in enumerate(E.UNIDADES, 4):
    cls = ("Afirmación compuesta (registro dependiente)" if u.startswith("Afirmación compuesta") else
           "Entidad de referencia" if u.startswith("Entidad:") else
           "Unidad de registro" if u in ("Obra", "Versión", "Manifestación", "Unidad estructural", "Fragmento textual", "Proceso") else
           "Afirmación / procedencia")
    d = UDEF.get(u, "Afirmación estructurada con subcampos propios, dependiente de la unidad de registro de la que se predica." if u.startswith("Afirmación compuesta")
                 else "Registro maestro de catálogo reutilizable; sus atributos se curan o importan.")
    body(ue.cell(row=i, column=1, value=u), bold=True); body(ue.cell(row=i, column=2, value=cls)); body(ue.cell(row=i, column=3, value=d))
    body(ue.cell(row=i, column=4, value=f'=COUNTIF({M}!${COL["unit"]}$2:${COL["unit"]}${LAST},A{i})'), center=True)
re0 = 4 + len(E.UNIDADES) + 2
ue.cell(row=re0 - 1, column=1, value="Etapas de procesamiento (CAT-008)").font = H2_FONT
header(ue, re0, ["Etapa", "Nombre", "Contenido", "Nº de campos"])
etv = {v["code"]: v for v in CN.CATALOGS[7]["values"]}
emap = {"Posterior (C)": "POST", "Curaduría": "CUR", "Sistema": "SIS"}
for i, st in enumerate(E.ETAPAS, re0 + 1):
    v = etv[emap.get(st, st)]
    body(ue.cell(row=i, column=1, value=st), bold=True); body(ue.cell(row=i, column=2, value=v["label"]))
    body(ue.cell(row=i, column=3, value=v["definition"]))
    body(ue.cell(row=i, column=4, value=f'=COUNTIF({M}!${COL["stage"]}$2:${COL["stage"]}${LAST},A{i})'), center=True)

# ============================================================================ 12 Cobertura
cv = sheet("12_Cobertura")
cv["A1"] = "Matriz de cobertura del inventario"; cv["A1"].font = TITLE_FONT
cv["A2"] = "Todas las cifras se calculan con fórmulas sobre el diccionario maestro y las hojas derivadas."; cv["A2"].font = BODY
cv.column_dimensions["A"].width = 52
for c_ in "BCDEFGHI":
    cv.column_dimensions[c_].width = 14
row = 4
def block(title, labels, formula_fn, extra_hdr=None):
    global row
    cv.cell(row=row, column=1, value=title).font = H2_FONT; row += 1
    header(cv, row, extra_hdr or ["Concepto", "Nº de campos"]); row += 1
    start = row
    for idx, lab in enumerate(labels):
        body(cv.cell(row=row, column=1, value=lab))
        vals = formula_fn(row, idx)
        for j, v in enumerate(vals if isinstance(vals, list) else [vals], 2):
            body(cv.cell(row=row, column=j, value=v), center=True)
        row += 1
    return start
rngM = lambda k: f'{M}!${COL[k]}$2:${COL[k]}${LAST}'
gen = [("Número total de campos", f'=COUNTA({rngM("id")})'),
       ("Campos universales (cuatro perfiles)", f"=COUNTIF('4_Campos_por_perfil'!$J$2:$J${LAST},\"Universal\")"),
       ("Campos compartidos por dos o tres perfiles", f"=COUNTIF('4_Campos_por_perfil'!$J$2:$J${LAST},\"Compartido\")"),
       ("Campos específicos de un solo perfil", f"=COUNTIF('4_Campos_por_perfil'!$J$2:$J${LAST},\"Específico de perfil\")"),
       ("Campos que requieren revisión humana (Sí)", f'=COUNTIF({rngM("review")},"Sí")'),
       ("Campos con revisión humana condicionada", f'=COUNTIF({rngM("review")},"Condicionado")'),
       ("Campos con validaciones o decisiones pendientes", f'=COUNTA({rngM("pending")})-COUNTIF({rngM("pending")},"No")'),
       ("Campos con datos personales o sensibles (cualquier nivel)", f'=COUNTA({rngM("privacy")})-COUNTIF({rngM("privacy")},"Ninguna")'),
       ("Campos a conservar en el primer procesamiento (modo A)", f'=COUNTIF({rngM("mode")},"A")'),
       ("Tipos de relación definidos", f"=COUNTA('8_Relaciones'!$A$2:$A${len(RELS) + 1})"),
       ("Catálogos definidos", f"=COUNTA('5a_Indice_catalogos'!$A$2:$A${len(CATS + META) + 1})"),
       ("Valores de catálogo", f"=COUNTA('5_Catalogos'!$C$2:$C${CAT_LAST})"),
       ("Valores de catálogo semilla pendientes de validación nacional", f"=COUNTIF('5_Catalogos'!$J$2:$J${CAT_LAST},\"Semilla*\")")]
cv.cell(row=row, column=1, value="Resumen general").font = H2_FONT; row += 1
header(cv, row, ["Concepto", "Valor"]); row += 1
TOTAL_ROW = row
for lab, fm in gen:
    body(cv.cell(row=row, column=1, value=lab)); body(cv.cell(row=row, column=2, value=fm), center=True); row += 1
row += 1
block("Campos por perfil documental (incluye universales)", ["Normativa", "Jurisprudencia", "Actos administrativos", "Doctrina"],
      lambda r, i: f"=COUNTIF('4_Campos_por_perfil'!${'FGHI'[i]}$2:${'FGHI'[i]}${LAST},\"●\")")
row += 1
block("Campos por dimensión", list(E.DIMENSIONES.values()), lambda r, i: f'=COUNTIF({rngM("dim")},A{r})')
row += 1
block("Campos por unidad de registro", E.UNIDADES, lambda r, i: f'=COUNTIF({rngM("unit")},A{r})')
row += 1
block("Campos por prioridad", E.PRIORIDADES, lambda r, i: f'=COUNTIF({rngM("prio")},A{r})')
row += 1
block("Campos por modo de adquisición", E.MODOS, lambda r, i: f'=COUNTIF({rngM("mode")},A{r})')
row += 1
block("Prioridad × modo de adquisición", E.PRIORIDADES,
      lambda r, i: [f'=COUNTIFS({rngM("prio")},$A{r},{rngM("mode")},"{m}")' for m in E.MODOS],
      extra_hdr=["Prioridad"] + [f"Modo {m}" for m in E.MODOS])
row += 1
block("Campos por origen del dato", E.ORIGENES, lambda r, i: f'=COUNTIF({rngM("origin")},A{r})')
row += 1
block("Campos por clase de riesgo", E.RIESGOS, lambda r, i: f'=COUNTIF({rngM("risk")},A{r})')
row += 1
block("Campos por sensibilidad y privacidad", E.PRIVACIDAD, lambda r, i: f'=COUNTIF({rngM("privacy")},A{r})')
row += 1
block("Taxonomía de etiquetas (hoja 5b)", ["Área principal", "Especialidad", "Especialidad sectorial o de práctica", "Subespecialidad"],
      lambda r, i: f"=COUNTIF('5b_Taxonomia_etiquetas'!$C$5:$C$400,A{r})", extra_hdr=["Tipo de etiqueta", "Nº de etiquetas"])
row += 1
block("Especialistas de Juztina (hoja 5c)", ["En producción", "Potencial", "Propuesta"],
      lambda r, i: f"=COUNTIF('5c_Especialistas_Juztina'!$C$5:$C$200,A{r})", extra_hdr=["Estado", "Nº de especialistas"])
row += 1
block("Campos por estado por país", E.ESTADO_PAIS, lambda r, i: f'=COUNTIF({rngM("country_status")},A{r})')
row += 1
PCOL = {pc: get_column_letter(5 + i) for i, pc in enumerate(E.PAISES)}
block("Cobertura por país y perfil (campos aplicables)", E.PAISES,
      lambda r, i: [f"=COUNTIF('6_Aplicabilidad_pais'!${PCOL[E.PAISES[i]]}$2:${PCOL[E.PAISES[i]]}${LAST},\"<>No aplica\")"]
      + [f"=COUNTIFS('6_Aplicabilidad_pais'!${PCOL[E.PAISES[i]]}$2:${PCOL[E.PAISES[i]]}${LAST},\"<>No aplica\","
         f"'4_Campos_por_perfil'!${pc_}$2:${pc_}${LAST},\"●\")" for pc_ in "FGHI"],
      extra_hdr=["País", "Total aplicable", "Normativa", "Jurisprudencia", "Actos administrativos", "Doctrina"])
row += 1
block("Campos pendientes de validación nacional por país", E.PAISES,
      lambda r, i: f"=COUNTIF('6_Aplicabilidad_pais'!${PCOL[E.PAISES[i]]}$2:${PCOL[E.PAISES[i]]}${LAST},\"Pendiente validación nacional\")")

# ============================================================================ 15 Control de calidad
qs = sheet("15_Control_calidad")
qs["A1"] = "Control de calidad del inventario"; qs["A1"].font = TITLE_FONT
qs["A2"] = ("Comprobaciones con fórmula (se recalculan al editar) y comprobaciones del script de construcción "
            "(valores fijados en la fecha de generación; se repiten al regenerar el libro).")
header(qs, 4, ["Comprobación", "Resultado", "Esperado", "Estado", "Método"], [70, 12, 10, 10, 30])
checks = [
 ("IDs de campo duplicados", f'=SUMPRODUCT((COUNTIF({rngM("id")},{rngM("id")})>1)*1)', 0),
 ("Nombres técnicos duplicados", f'=SUMPRODUCT((COUNTIF({rngM("tech")},{rngM("tech")})>1)*1)', 0),
 ("Celdas vacías en el diccionario maestro", f"=COUNTBLANK({M}!$A$2:${get_column_letter(len(MCOLS))}${LAST})", 0),
 ("Campos sin dimensión válida", f'=SUMPRODUCT(--ISNA(MATCH({rngM("dim")},{list_ref["dim"]},0)))', 0),
 ("Campos sin unidad de registro válida", f'=SUMPRODUCT(--ISNA(MATCH({rngM("unit")},{list_ref["unit"]},0)))', 0),
 ("Prioridades fuera de la arquitectura", f'=SUMPRODUCT(--ISNA(MATCH({rngM("prio")},{list_ref["prio"]},0)))', 0),
 ("Modos de adquisición fuera de la arquitectura", f'=SUMPRODUCT(--ISNA(MATCH({rngM("mode")},{list_ref["mode"]},0)))', 0),
 ("Modo X sin prioridad 'Fuera de alcance' o viceversa", f'=ABS(COUNTIF({rngM("mode")},"X")-COUNTIF({rngM("prio")},"Fuera de alcance"))', 0),
 ("Campos sin ninguna funcionalidad vinculada (deben coincidir con los que declaran 'No aplica')", f"=COUNTIF('10_Funcionalidades'!${NFCOL}$2:${NFCOL}${LAST},0)-COUNTIF({rngM('funcs')},\"No aplica*\")", 0),
 ("Valores de catálogo sin definición", f"=COUNTBLANK('5_Catalogos'!$F$2:$F${CAT_LAST})", 0),
]
r = 5
for lab, fm, exp in checks:
    body(qs.cell(row=r, column=1, value=lab)); body(qs.cell(row=r, column=2, value=fm), center=True)
    body(qs.cell(row=r, column=3, value=exp), center=True)
    body(qs.cell(row=r, column=4, value=f'=IF(ISNUMBER(C{r}),IF(B{r}=C{r},"OK","Revisar"),"Ver")'), center=True)
    body(qs.cell(row=r, column=5, value="Fórmula")); r += 1
for lab, n in qc:
    body(qs.cell(row=r, column=1, value=lab)); body(qs.cell(row=r, column=2, value=n), center=True)
    body(qs.cell(row=r, column=3, value=0), center=True)
    body(qs.cell(row=r, column=4, value=f'=IF(B{r}=C{r},"OK","Revisar")'), center=True)
    body(qs.cell(row=r, column=5, value=f"Script de construcción ({FECHA})")); r += 1
r += 1
qs.cell(row=r, column=1, value="IDs retirados durante la integración (reservados: no se reutilizan)").font = H2_FONT; r += 1
header(qs, r, ["ID retirado", "Sustituido por", "Motivo", "Tipo", "—"]); r += 1
for old, (new, why) in list(IG.RETIRADOS.items()) + list(IG.CAT_RETIRADOS.items()):
    vals = [old, new, why, "Catálogo" if old.startswith("CAT") else "Campo", "Reservado"]
    for j, x in enumerate(vals, 1):
        body(qs.cell(row=r, column=j, value=x), bold=(j == 1))
    r += 1
qs.freeze_panes = "A5"

# ============================================================================ README
rd = readme
rd.column_dimensions["A"].width = 30; rd.column_dimensions["B"].width = 120
rd["A1"] = f"Juztina — Diccionario maestro de metadatos jurídicos · versión {VERSION}"; rd["A1"].font = TITLE_FONT
rd["A2"] = f"Fecha de generación: {FECHA}. Etapa 2 del proyecto de arquitectura global de metadatos jurídicos."; rd["A2"].font = BODY
SECTIONS = [
 ("Propósito", [
  ("Qué es", "Diccionario maestro que define, campo por campo, qué información conservar, sobre qué unidad documental, de dónde obtenerla, cómo extraerla y validarla, qué evidencia guardar, qué prioridad tiene y qué funcionalidades habilita."),
  ("Qué no es", "No es el resultado de una extracción ni un esquema de base de datos de producción. No contiene datos del corpus. No valida reglas jurídicas nacionales."),
  ("Fuente obligatoria", "Arquitectura conceptual de metadatos jurídicos, versión 3 (final), pestaña 'Versión 3 · final' del documento de arquitectura en Claude Docs. Las decisiones allí cerradas no se modifican aquí."),
  ("Alcance", "Siete países (PE, CO, AR, CL, EC, BO, MX), cuatro categorías (normativa, jurisprudencia, actos administrativos, doctrina), 16 dimensiones descriptivas más las capas de procedencia y operativa."),
 ]),
 ("Convenciones", [
  ("ID del campo", "MDJ-<DIM>-<NNN>. DIM es la dimensión de alta (D01…D17, PRO, OPE). El ID es persistente: no cambia si el campo se renombra o reasigna de dimensión, no depende del orden de filas ni del país y nunca se reutiliza. Un campo retirado se marca como tal; no se borra."),
  ("Nombre técnico", "snake_case en español, sin tildes ni ñ (ñ → n), único en todo el diccionario. Se eligió español para alinear el vocabulario técnico con el jurídico."),
  ("Unidad de registro", "Una de las unidades de la arquitectura (obra, versión, manifestación, unidad estructural, fragmento textual, proceso), una afirmación compuesta (registro estructurado dependiente: evento, operación modificatoria, asignación de clasificación, parte, monto, efecto, estado de campo, revisión) o una entidad de referencia (catálogos maestros). Ver hoja 14."),
  ("Origen del dato", "Explícito en documento · Normalizado por regla · Inferido por modelo · Derivado por cálculo · Conclusión jurídica por reglas · Fuente externa · Generado por sistema · Curado por persona. Corresponde a los modos de origen de la arquitectura (CAT-005)."),
  ("Método de adquisición", "Extracción directa · Normalización · Clasificación · Inferencia · Cálculo · Enriquecimiento externo · Revisión humana · Generado por sistema (combinables con '+')."),
  ("Prioridad", "P0 Infraestructura · P1 Núcleo analítico · P2 Análisis profundo · P3 Enriquecimiento · Fuera de alcance (CAT-906)."),
  ("Modo de adquisición", "A en la pasada masiva · B calculable · C posterior sobre fragmentos · D fuente externa o curaduría · X fuera del alcance inicial (CAT-907)."),
  ("Clase de riesgo", "R1 alto · R2 medio · R3 bajo. Determina el criterio de aceptación (hoja 13)."),
  ("Países y estado por país", "'ALL' o lista de códigos ISO. Estado: Común · Catálogo por país · Específico de país · Condicionado · Pendiente validación nacional (CAT-908)."),
  ("Celdas sin contenido aplicable", "Se usa 'No aplica: <razón>'. Ninguna celda del diccionario maestro queda vacía."),
  ("Colores", "Encabezados azul oscuro. Texto verde: valor leído del diccionario maestro por fórmula. Las hojas derivadas no se editan: se edita el maestro."),
 ]),
 ("Hojas", [
  ("2_Diccionario_maestro", "Fuente central. Un registro por campo con todos los atributos. Listas desplegables en columnas controladas."),
  ("3_Campos_universales", "Campos aplicables a las cuatro categorías, con condiciones y excepciones (fórmulas sobre el maestro)."),
  ("4_Campos_por_perfil", "Aplicabilidad a normativa, jurisprudencia, actos y doctrina; alcance universal, compartido o específico."),
  ("5_Catalogos / 5a_Indice_catalogos", "Valores permitidos de cada vocabulario controlado con ID, definición, jerarquía, sinónimos, país, estado y versión; índice con conteos."),
  ("5b_Taxonomia_etiquetas", "LA LISTA DE ETIQUETAS: 27 áreas principales, especialidades dogmáticas y sectoriales (Minero, Bancario, Moda…) y subespecialidades, con qué incluye y excluye cada una, indicadores para la IA y columnas amarillas para validar o proponer etiquetas nuevas."),
  ("5c_Especialistas_Juztina", "Especialistas actuales (Laboral, Tributario, Consumidor) y potenciales, cada uno definido como un conjunto de etiquetas de la hoja 5b."),
  ("6_Aplicabilidad_pais", "Matriz campo × país calculada a partir de los atributos 'Países' y 'Estado por país'."),
  ("7_Reglas_extraccion", "Reglas de extracción y validación, evidencia, criterio de aceptación por riesgo y excepciones, por campo."),
  ("8_Relaciones / 8a_Referencias", "Tipos de relación con direccionalidad, inversa, modo, evidencia y reglas; tipos de referencia con información mínima."),
  ("9_Prioridad_procesamiento", "Campos ordenados por prioridad, modo y etapa; qué conservar en el primer procesamiento."),
  ("10_Funcionalidades", "Matriz campo × funcionalidad (F01–F18) con totales."),
  ("11_Pendientes", "Decisiones y validaciones pendientes con campos y catálogos afectados e impacto."),
  ("12_Cobertura", "Resumen cuantitativo calculado con fórmulas."),
  ("13_Reglas_generales", "Criterios de aceptación por riesgo, reglas de control y estados de campo."),
  ("14_Unidades_y_etapas", "Definición de unidades, afirmaciones compuestas, entidades y etapas, con conteos."),
  ("15_Control_calidad", "Comprobaciones de consistencia del inventario."),
  ("16_Listas", "Listas que alimentan los desplegables. No editar salvo para ampliar vocabularios meta."),
 ]),
 ("Advertencias", [
  ("Reglas nacionales", "Ninguna regla jurídica nacional está validada. Los valores sembrados por país llevan el estado 'Semilla — pendiente de validación nacional' y los campos afectados indican la decisión pendiente (hoja 11)."),
  ("Corpus", "No se conoce la composición real del corpus (volumen, formatos, OCR, completitud histórica). Ningún dato de este libro la presupone."),
  ("Regeneración", "El libro se genera con fuente/construir_excel.py a partir de los módulos de campos. Cambiar los módulos y regenerar es la vía recomendada para mantener la consistencia."),
 ]),
]
r = 4
for title, rows in SECTIONS:
    rd.cell(row=r, column=1, value=title).font = H2_FONT; r += 1
    for a, b in rows:
        body(rd.cell(row=r, column=1, value=a), bold=True); body(rd.cell(row=r, column=2, value=b)); r += 1
    r += 1
rd.cell(row=r, column=1, value="Cifras clave (calculadas)").font = H2_FONT; r += 1
for lab, ref in [("Total de campos", f"='12_Cobertura'!B{TOTAL_ROW}"), ("Campos en la pasada masiva (modo A)", f"='12_Cobertura'!B{TOTAL_ROW + 8}"),
                 ("Campos con validaciones pendientes", f"='12_Cobertura'!B{TOTAL_ROW + 6}"), ("Tipos de relación", f"='12_Cobertura'!B{TOTAL_ROW + 9}"),
                 ("Catálogos", f"='12_Cobertura'!B{TOTAL_ROW + 10}")]:
    body(rd.cell(row=r, column=1, value=lab), bold=True); body(rd.cell(row=r, column=2, value=ref), font=LINK); r += 1

# orden de hojas
order = ["1_README", "2_Diccionario_maestro", "3_Campos_universales", "4_Campos_por_perfil", "5_Catalogos", "5a_Indice_catalogos",
         "5b_Taxonomia_etiquetas", "5c_Especialistas_Juztina",
         "6_Aplicabilidad_pais", "7_Reglas_extraccion", "8_Relaciones", "8a_Referencias", "9_Prioridad_procesamiento",
         "10_Funcionalidades", "11_Pendientes", "12_Cobertura", "13_Reglas_generales", "14_Unidades_y_etapas",
         "15_Control_calidad", "16_Listas"]
wb._sheets = [wb[n] for n in order]
for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 90
wb.save(OUT)

# ----------------------------------------------------------------------------- estadísticas para los documentos
st = dict(
    total=N, universales=len(UNIV), relaciones=len(RELS), catalogos=len(CATS + META), valores=sum(len(c["values"]) for c in CATS + META),
    semillas=sum(1 for c in CATS for v in c["values"] if str(v.get("status", "")).startswith("Semilla")),
    por_dim=Counter(f["dim_label"] for f in FIELDS), por_unidad=Counter(f["unit"] for f in FIELDS),
    por_prio=Counter(f["prio"] for f in FIELDS), por_modo=Counter(f["mode"] for f in FIELDS),
    por_origen=Counter(f["origin"] for f in FIELDS), por_riesgo=Counter(f["risk"] for f in FIELDS),
    revision=Counter(f["review"] for f in FIELDS), privacidad=Counter(f["privacy"] for f in FIELDS),
    pais=Counter(f["country_status"] for f in FIELDS), pendientes=sum(1 for f in FIELDS if f["pending"] != "No"),
    por_perfil={p: sum(1 for f in FIELDS if p in f["profiles"] or "UNI" in f["profiles"]) for p in ("NOR", "JUR", "ADM", "DOC")},
    por_dec=Counter(d for f in FIELDS for d in f["pending"].split("; ") if d != "No"),
    qc=dict(qc), por_grupo=Counter(SRC[f["id"]] for f in FIELDS), retirados=len(IG.RETIRADOS), cat_retirados=len(IG.CAT_RETIRADOS),
    redactados=len(SRC), r1_ajustados=len(R1_AJUSTADOS), etiquetas=len(TX.ROWS),
    etiquetas_por_tipo=Counter(r["tipo"] for r in TX.ROWS), especialistas=len(TX.SPECIALISTS),
)
with open(os.path.join(HERE, "estadisticas.json"), "w", encoding="utf-8") as fh:
    json.dump(st, fh, ensure_ascii=False, indent=1, default=dict)
print("OK", OUT, "campos:", N)
