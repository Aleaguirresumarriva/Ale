"""
Capa de lectura del diccionario maestro: hojas en lenguaje simple para equipos jurídicos y de producto.
Se genera desde los mismos datos que el anexo técnico; las cifras se calculan con fórmulas sobre él.
"""
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

AR = "Arial"
NAVY = "1F3864"; TEAL = "1F7A8C"; LIGHT = "E8F1F5"; SOFT = "F3F6FA"; GREY = "A6A6A6"
F_TITLE = Font(name=AR, size=18, bold=True, color=NAVY)
F_SUB = Font(name=AR, size=11, color="595959", italic=True)
F_H2 = Font(name=AR, size=12, bold=True, color=NAVY)
F_HDR = Font(name=AR, size=10, bold=True, color="FFFFFF")
F_BODY = Font(name=AR, size=10)
F_BOLD = Font(name=AR, size=10, bold=True)
F_BIG = Font(name=AR, size=22, bold=True, color=TEAL)
F_BOX = Font(name=AR, size=11, bold=True, color="FFFFFF")
F_LINK = Font(name=AR, size=10, color="0563C1", underline="single")
FILL_HDR = PatternFill("solid", fgColor=NAVY)
FILL_TEAL = PatternFill("solid", fgColor=TEAL)
FILL_BLOCK = PatternFill("solid", fgColor=LIGHT)
FILL_SOFT = PatternFill("solid", fgColor=SOFT)
THIN = Side(style="thin", color="D0D7DE")
BRD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)

BLOQUES = [  # (código de dimensión, nombre simple, pregunta que responde)
    ("D01", "Identificación del documento", "¿Qué documento es y cómo se encuentra?"),
    ("D02", "Quién lo emite y de dónde viene", "¿Quién lo dictó, quién lo custodia y dónde se publicó?"),
    ("D04", "Tipo de documento y rango", "¿Qué clase de documento es y qué jerarquía tiene?"),
    ("D03", "Fechas y vigencia", "¿Desde cuándo rige, hasta cuándo y qué lo cambió?"),
    ("D05", "Estructura y contenido", "¿Cómo está organizado por dentro (artículos, fundamentos, fallo)?"),
    ("D06", "Etiquetas por área del Derecho", "¿De qué materias jurídicas trata?"),
    ("D10", "Sector económico", "¿A qué industria o actividad se refiere?"),
    ("D07", "Citas y relaciones con otros documentos", "¿Qué otros documentos cita, aplica, modifica o revoca?"),
    ("D13", "Personas e instituciones que intervienen", "¿Quiénes son las partes, jueces, funcionarios o autores?"),
    ("D14", "Proceso y decisión", "¿En qué proceso o procedimiento está y qué se decidió?"),
    ("D17", "Peso jurídico", "¿Es precedente, es obligatorio, qué autoridad tiene?"),
    ("D08", "A quién afecta y qué efectos tiene", "¿A quién obliga, qué derechos, prohibiciones o sanciones crea?"),
    ("D09", "Montos y cifras", "¿Qué multas, indemnizaciones, tasas o límites contiene?"),
    ("D15", "Idioma y formato", "¿En qué idioma y formato está?"),
    ("D16", "Privacidad y derechos de uso", "¿Tiene datos personales o restricciones de uso?"),
    ("D11", "Calidad del documento", "¿El texto está completo y es legible?"),
    ("PRO", "Respaldo de cada dato (técnico)", "¿De qué parte del texto sale cada dato y quién lo validó?"),
    ("OPE", "Control del procesamiento (técnico)", "¿Qué se procesó, qué falta y qué quedó indeterminado?"),
]
TECNICOS = {"PRO", "OPE"}

COMO = {
    "Explícito en documento": "La IA lo lee en el texto",
    "Normalizado por regla": "La IA lo lee y lo estandariza",
    "Inferido por modelo": "La IA lo interpreta",
    "Derivado por cálculo": "Se calcula con otros datos",
    "Conclusión jurídica por reglas": "Lo concluye una regla jurídica validada",
    "Fuente externa": "Viene de una fuente externa",
    "Generado por sistema": "Lo genera el sistema",
    "Curado por persona": "Lo define o valida una persona",
}
IMPORTANCIA = {"P0": "Imprescindible", "P1": "Importante", "P2": "Análisis profundo", "P3": "Complementario",
               "Fuera de alcance": "No se extrae (decisión)"}
MOMENTO = {"A": "1ª lectura de la IA", "B": "Se calcula después", "C": "2ª etapa, sobre fragmentos",
           "D": "Fuente externa o curaduría", "X": "No se extrae"}
PAIS = {"Común": "Igual en los 7 países", "Catálogo por país": "Mismo dato; valores propios de cada país",
        "Pendiente validación nacional": "Por validar con abogado de cada país", "Condicionado": "Solo si la figura existe en el país",
        "Específico de país": "Solo en algunos países"}
CATEG = [("NOR", "Normativa", "C_Normativa", "Leyes, decretos, reglamentos, ordenanzas y demás normas."),
         ("JUR", "Jurisprudencia", "D_Jurisprudencia", "Sentencias, autos, casaciones, tesis y demás decisiones de jueces y tribunales."),
         ("ADM", "Actos administrativos", "E_Actos_administrativos", "Resoluciones, sanciones, conceptos, oficios y demás decisiones de la Administración."),
         ("DOC", "Doctrina", "F_Doctrina", "Artículos, libros, tesis y comentarios de autores.")]


def _c(ws, row, col, val, font=F_BODY, fill=None, align=WRAP, border=True):
    c = ws.cell(row=row, column=col, value=val)
    if not border and align is WRAP:
        align = Alignment(vertical="top", wrap_text=False)
    c.font = font; c.alignment = align
    if fill: c.fill = fill
    if border: c.border = BRD
    return c


def _hdr(ws, row, labels, widths=None):
    for j, lab in enumerate(labels, 1):
        _c(ws, row, j, lab, F_HDR, FILL_HDR, CEN)
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w


def _title(ws, title, subtitle):
    ws.sheet_view.showGridLines = False
    _c(ws, 1, 1, title, F_TITLE, border=False, align=Alignment(vertical="center"))
    _c(ws, 2, 1, subtitle, F_SUB, border=False, align=Alignment(vertical="top"))
    ws.row_dimensions[1].height = 30
    _c(ws, 1, 12, "← Inicio", F_LINK, border=False).hyperlink = "#'A_Inicio'!A1"


def _first_sentence(t):
    t = str(t).strip()
    for sep in (". ", "; "):
        if sep in t:
            return t.split(sep)[0].rstrip(".") + "."
    return t


def build(wb, FIELDS, TX, CATS, M, COL, LAST, counts):
    """Crea las hojas de lectura y devuelve sus nombres en orden."""
    by_dim = {}
    for f in FIELDS:
        by_dim.setdefault(f["dim"], []).append(f)
    prof = lambda f, code: ("UNI" in f["profiles"]) or (code in f["profiles"])
    names = []

    # ------------------------------------------------------------------ A Inicio
    ws = wb.create_sheet("A_Inicio"); names.append(ws.title)
    ws.sheet_view.showGridLines = False
    for j, w in enumerate([3, 22, 4, 22, 4, 22, 4, 22, 4, 22, 3, 14], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    _c(ws, 1, 2, "Juztina · Mapa de metadatos jurídicos", F_TITLE, border=False)
    _c(ws, 2, 2, "Qué va a leer la IA en cada documento, qué datos va a sacar y cómo esos datos alimentan los especialistas", F_SUB, border=False)
    steps = [("1. La base documental", "7 países\n4 tipos de documento"),
             ("2. La IA lee cada documento", "Por etapas: primero lo imprescindible, luego el análisis"),
             ("3. Saca metadatos", "=TEXT('12_Cobertura'!B{t},\"0\")&\" datos posibles en 18 bloques\"".format(t=counts["total_row"])),
             ("4. Le pone etiquetas", "=TEXT(COUNTA('G_Etiquetas'!H6:H400),\"0\")&\" etiquetas en 27 áreas del Derecho\""),
             ("5. Alimenta especialistas", "=TEXT(COUNTA('H_Especialistas'!A6:A100),\"0\")&\" especialistas (3 en producción)\"")]
    for k, (t, d) in enumerate(steps):
        col = 2 + 2 * k
        ws.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col)
        _c(ws, 4, col, t, F_BOX, FILL_TEAL, CEN)
        _c(ws, 5, col, d, F_BODY, FILL_BLOCK, CEN)
        if k < 4:
            _c(ws, 4, col + 1, "→", Font(name=AR, size=18, bold=True, color=TEAL), border=False, align=CEN)
    ws.row_dimensions[4].height = 34; ws.row_dimensions[5].height = 48
    # cifras clave
    _c(ws, 7, 2, "Cifras clave", F_H2, border=False)
    kp = [("Metadatos definidos", f"='12_Cobertura'!B{counts['total_row']}"),
          ("Se leen en la 1ª pasada", f"='12_Cobertura'!B{counts['total_row'] + 8}"),
          ("Etiquetas jurídicas", "=COUNTA('G_Etiquetas'!H6:H400)"),
          ("Especialistas", "=COUNTA('H_Especialistas'!A6:A100)"),
          ("Datos por validar", f"='12_Cobertura'!B{counts['total_row'] + 6}")]
    for k, (lab, fm) in enumerate(kp):
        col = 2 + 2 * k
        _c(ws, 8, col, fm, F_BIG, FILL_SOFT, CEN)
        _c(ws, 9, col, lab, F_BOLD, FILL_SOFT, CEN)
    ws.row_dimensions[8].height = 40
    # índice de lectura
    _c(ws, 11, 2, "Cómo leer este archivo (pestañas de color verde azulado)", F_H2, border=False)
    guide = [("B_Mapa_metadatos", "El panorama: cuántos datos se sacan de cada tipo de documento, por tema. Empiece aquí."),
             ("C_Normativa", "Los datos que se sacan de una norma, agrupados por tema."),
             ("D_Jurisprudencia", "Los datos que se sacan de una sentencia o resolución judicial."),
             ("E_Actos_administrativos", "Los datos que se sacan de un acto o resolución administrativa."),
             ("F_Doctrina", "Los datos que se sacan de un artículo, libro o tesis."),
             ("G_Etiquetas", "El árbol de etiquetas: áreas del Derecho, especialidades y subespecialidades."),
             ("H_Especialistas", "Los especialistas de Juztina y qué etiquetas usa cada uno."),
             ("I_Paises", "Qué cambia en cada país: nombres de normas, diarios oficiales, unidades de multa, precedentes."),
             ("J_Ejemplo", "Un documento de ejemplo con todos los datos que la IA sacaría."),
             ("K_Glosario", "Las palabras técnicas explicadas en una línea.")]
    for k, (sh, desc) in enumerate(guide, 12):
        _c(ws, k, 2, sh, F_LINK, FILL_SOFT).hyperlink = f"#'{sh}'!A1"
        ws.merge_cells(start_row=k, start_column=4, end_row=k, end_column=10)
        _c(ws, k, 4, desc, F_BODY, FILL_SOFT)
    r = 12 + len(guide) + 1
    _c(ws, r, 2, "Anexo técnico (pestañas grises)", F_H2, border=False)
    ws.merge_cells(start_row=r + 1, start_column=2, end_row=r + 1, end_column=10)
    _c(ws, r + 1, 2, ("Las pestañas grises numeradas (1 a 16) contienen el diccionario completo para el equipo técnico: "
                      "reglas de extracción y validación, catálogos, prioridades, relaciones y controles de calidad. "
                      "Todas las cifras de estas pestañas de lectura salen de ese anexo."), F_BODY, border=False,
       align=Alignment(wrap_text=True, vertical="top"))
    ws.row_dimensions[r + 1].height = 32

    # ------------------------------------------------------------------ B Mapa
    ws = wb.create_sheet("B_Mapa_metadatos"); names.append(ws.title)
    _title(ws, "Mapa de metadatos", "Cuántos datos se pueden sacar de cada tipo de documento, por tema. El color más intenso indica más datos.")
    _hdr(ws, 4, ["Tema", "¿Qué responde?", "Normativa", "Jurisprudencia", "Actos administrativos", "Doctrina", "Total del tema", "Dimensión técnica"],
         [36, 52, 13, 15, 15, 12, 13, 30])
    PCOL = {"NOR": "F", "JUR": "G", "ADM": "H", "DOC": "I"}
    P4 = "'4_Campos_por_perfil'"
    for i, (code, nombre, preg) in enumerate(BLOQUES, 5):
        dlabel = by_dim[code][0]["dim_label"] if code in by_dim else code
        _c(ws, i, 1, nombre, F_BOLD, FILL_SOFT if code in TECNICOS else None)
        _c(ws, i, 2, preg)
        for j, pc in enumerate(["NOR", "JUR", "ADM", "DOC"], 3):
            _c(ws, i, j, f"=COUNTIFS({P4}!$C$2:$C${LAST},$H{i},{P4}!${PCOL[pc]}$2:${PCOL[pc]}${LAST},\"●\")", F_BOLD, align=CEN)
        _c(ws, i, 7, f"=COUNTIF({M}!${COL['dim']}$2:${COL['dim']}${LAST},$H{i})", F_BOLD, align=CEN)
        _c(ws, i, 8, dlabel, Font(name=AR, size=9, color="7F7F7F"))
    last = 4 + len(BLOQUES)
    _c(ws, last + 1, 1, "Total de datos por tipo de documento", F_HDR, FILL_HDR)
    _c(ws, last + 1, 2, "Un mismo dato puede servir a varios tipos de documento", F_HDR, FILL_HDR)
    for j in range(3, 8):
        cl = get_column_letter(j)
        _c(ws, last + 1, j, f"=SUM({cl}5:{cl}{last})", F_HDR, FILL_HDR, CEN)
    ws.conditional_formatting.add(f"C5:F{last}", ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color="5B9BD5"))
    # importancia × tipo
    r0 = last + 4
    _c(ws, r0 - 1, 1, "¿Cuándo se obtienen? (por tipo de documento)", F_H2, border=False)
    _hdr(ws, r0, ["Momento", "Qué significa", "Normativa", "Jurisprudencia", "Actos administrativos", "Doctrina", "Total"])
    expl = {"A": "La IA lo saca al leer el documento completo, en la pasada masiva.",
            "B": "No hace falta volver a leer: se calcula con datos ya extraídos.",
            "C": "Se saca más adelante, leyendo solo los fragmentos ya identificados.",
            "D": "Viene de catálogos, fuentes oficiales o de una persona.",
            "X": "Se decidió no extraerlo por ahora (por ejemplo, nombres de personas)."}
    for i, m in enumerate(["A", "B", "C", "D", "X"], r0 + 1):
        _c(ws, i, 1, MOMENTO[m], F_BOLD); _c(ws, i, 2, expl[m])
        for j, pc in enumerate(["NOR", "JUR", "ADM", "DOC"], 3):
            _c(ws, i, j, f"=COUNTIFS({M}!${COL['mode']}$2:${COL['mode']}${LAST},\"{m}\",{P4}!${PCOL[pc]}$2:${PCOL[pc]}${LAST},\"●\")", F_BOLD, align=CEN)
        _c(ws, i, 7, f"=COUNTIF({M}!${COL['mode']}$2:${COL['mode']}${LAST},\"{m}\")", F_BOLD, align=CEN)
    r1 = r0 + 8
    _c(ws, r1 - 1, 1, "¿Cómo se obtienen?", F_H2, border=False)
    _hdr(ws, r1, ["Forma de obtención", "Qué significa", "Nº de datos"])
    expl2 = {"La IA lo lee en el texto": "Está escrito tal cual en el documento (número, fecha, nombre del tribunal).",
             "La IA lo lee y lo estandariza": "Está escrito, y se lleva a un formato común (fechas, nombres de entidades).",
             "La IA lo interpreta": "Requiere criterio (de qué materia trata, cuál es el problema jurídico).",
             "Se calcula con otros datos": "Se deduce de datos ya extraídos (versión vigente, totales).",
             "Lo concluye una regla jurídica validada": "Conclusiones como la vigencia o si es precedente; con reglas que validan abogados.",
             "Viene de una fuente externa": "Catálogos oficiales (códigos territoriales, unidades de valor).",
             "Lo genera el sistema": "Identificadores, fechas de proceso.",
             "Lo define o valida una persona": "Catálogos y validaciones del equipo jurídico."}
    for i, (orig, simple) in enumerate(COMO.items(), r1 + 1):
        _c(ws, i, 1, simple, F_BOLD); _c(ws, i, 2, expl2[simple])
        _c(ws, i, 3, f"=COUNTIF({M}!${COL['origin']}$2:${COL['origin']}${LAST},\"{orig}\")", F_BOLD, align=CEN)
    ws.freeze_panes = "A5"

    # ------------------------------------------------------------------ C–F Categorías
    for code, nombre, sh, desc in CATEG:
        ws = wb.create_sheet(sh); names.append(sh)
        _title(ws, f"{nombre}: qué datos se sacan", desc + " Use los botones + y − de la izquierda para abrir o cerrar cada tema. En gris: identificadores técnicos que genera el sistema.")
        _hdr(ws, 4, ["Dato", "Qué es", "Ejemplo", "¿Cómo se obtiene?", "¿Cuándo?", "Importancia", "¿Cambia por país?", "ID técnico"],
             [36, 58, 30, 26, 22, 18, 30, 14])
        ws.sheet_properties.outlinePr.summaryBelow = False
        r = 5
        for dcode, bname, preg in BLOQUES:
            fl = [f for f in by_dim.get(dcode, []) if prof(f, code)]
            if not fl:
                continue
            fl.sort(key=lambda f: (f["origin"] == "Generado por sistema", list(IMPORTANCIA).index(f["prio"]), f["id"]))
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
            _c(ws, r, 1, f"{bname}  ·  {len(fl)} datos  ·  {preg}", Font(name=AR, size=11, bold=True, color=NAVY), FILL_BLOCK)
            ws.row_dimensions[r].height = 22
            r += 1
            for f in fl:
                pais = PAIS[f["country_status"]] + ("" if f["countries"] == "ALL" else f" ({f['countries']})")
                vals = [f["func"], _first_sentence(f["defn"]), f["example"], COMO[f["origin"]], MOMENTO[f["mode"]],
                        IMPORTANCIA[f["prio"]], pais, f["id"]]
                sis = f["origin"] == "Generado por sistema"
                for j, v in enumerate(vals, 1):
                    fnt = Font(name=AR, size=10, color="8C8C8C", italic=True) if sis else (F_BOLD if j == 1 else F_BODY)
                    _c(ws, r, j, v, fnt)
                ws.row_dimensions[r].outlineLevel = 1
                if dcode in TECNICOS:
                    ws.row_dimensions[r].hidden = True
                r += 1
        ws.freeze_panes = "B5"

    # ------------------------------------------------------------------ G Etiquetas
    ws = wb.create_sheet("G_Etiquetas"); names.append(ws.title)
    _title(ws, "Etiquetas por área del Derecho", "Cada documento recibe todas las etiquetas de las materias que realmente trata. Las filas azules son las 27 áreas; ábralas con +.")
    _hdr(ws, 5, ["Área principal", "Especialidad", "Subespecialidad", "Tipo", "Qué incluye", "La usa el especialista", "También pertenece a", "ID"],
         [30, 38, 38, 18, 62, 26, 30, 14])
    _c(ws, 4, 1, "Tipo 'Rama': división clásica del Derecho. Tipo 'Sector': industria o práctica (Minero, Bancario, Moda…), que se asigna con una regla.", F_SUB, border=False)
    ws.sheet_properties.outlinePr.summaryBelow = False
    idx = {x["id"]: x for x in TX.ROWS}
    uso = {}
    for sp in TX.SPECIALISTS:
        for e in sp["etiquetas"].split("; "):
            uso.setdefault(e, []).append(sp["nombre"])
    def usado(x):
        cur, out = x, []
        while True:
            out += uso.get(cur["id"], [])
            if cur["padre"] == "—":
                break
            cur = idx[cur["padre"]]
        return ", ".join(dict.fromkeys(out)) or "—"
    r = 6
    for a in [x for x in TX.ROWS if x["nivel"] == 1]:
        fam = [a]
        for e in [x for x in TX.ROWS if x["nivel"] == 2 and x["padre"] == a["id"]]:
            fam.append(e); fam += [x for x in TX.ROWS if x["nivel"] == 3 and x["padre"] == e["id"]]
        for x in fam:
            col = x["nivel"]
            tipo = "Área" if x["nivel"] == 1 else ("Sector" if "sectorial" in x["tipo"] else "Rama")
            otros = "; ".join(idx[o]["nombre"] for o in x["otros"].split("; ")) if x["otros"] != "—" else "—"
            row = ["", "", "", tipo, x["incluye"], usado(x), otros, x["id"]]
            row[col - 1] = x["nombre"]
            fill = FILL_BLOCK if x["nivel"] == 1 else None
            for j, v in enumerate(row, 1):
                _c(ws, r, j, v, F_BOLD if (j == col or x["nivel"] == 1) else F_BODY, fill)
            if x["nivel"] > 1:
                ws.row_dimensions[r].outlineLevel = x["nivel"] - 1
            r += 1
    ws.freeze_panes = "A6"

    # ------------------------------------------------------------------ H Especialistas
    ws = wb.create_sheet("H_Especialistas"); names.append(ws.title)
    _title(ws, "Especialistas de Juztina", "Cada especialista toma los documentos que tienen sus etiquetas. Para crear uno nuevo basta con elegir etiquetas: no hay que volver a leer los documentos.")
    _hdr(ws, 5, ["Especialista", "Estado", "Toma los documentos etiquetados como…", "Etiquetas cubiertas (incluye las de abajo)", "Exige que la materia sea", "Observaciones"],
         [28, 15, 60, 16, 22, 60])
    def desc_count(eid):
        kids = [x for x in TX.ROWS if x["padre"] == eid]
        return 1 + sum(desc_count(k["id"]) for k in kids)
    for i, sp in enumerate(TX.SPECIALISTS, 6):
        ids = sp["etiquetas"].split("; ")
        nm = ", ".join(idx[e]["nombre"] for e in ids)
        fill = FILL_BLOCK if sp["estado"] == "En producción" else None
        vals = [sp["nombre"], sp["estado"], nm, sum(desc_count(e) for e in ids), sp["relevancia"].replace("Principal o secundaria", "Principal o secundaria").lower(),
                sp["nota"] if sp["nota"] != "—" else ""]
        for j, v in enumerate(vals, 1):
            _c(ws, i, j, v, F_BOLD if j == 1 else F_BODY, fill, CEN if j in (2, 4) else WRAP)
    ws.freeze_panes = "B6"

    # ------------------------------------------------------------------ I Países
    ws = wb.create_sheet("I_Paises"); names.append(ws.title)
    _title(ws, "Qué cambia en cada país", "La estructura de datos es la misma en los 7 países; cambian los nombres, los catálogos y las reglas. Todo lo de esta hoja está por validar con un abogado de cada país.")
    P = ["PE", "CO", "AR", "CL", "EC", "BO", "MX"]
    PN = {"PE": "Perú", "CO": "Colombia", "AR": "Argentina", "CL": "Chile", "EC": "Ecuador", "BO": "Bolivia", "MX": "México"}
    _hdr(ws, 4, ["Aspecto"] + [PN[p] for p in P], [30] + [26] * 7)
    catv = {c["cat_id"]: c["values"] for c in CATS}
    def seed(cid, p):
        vals = [v["label"] for v in catv.get(cid, []) if (v.get("country") or "") == p]
        return "; ".join(vals) or "Por definir"
    rows = [
        ("Diario oficial (ejemplo)", {"PE": "El Peruano", "CO": "Diario Oficial", "AR": "Boletín Oficial", "CL": "Diario Oficial",
                                      "EC": "Registro Oficial (y suplementos)", "BO": "Gaceta Oficial", "MX": "Diario Oficial de la Federación (DOF)"}),
        ("Ejemplos de tipos de documento", {p: seed("CAT-126", p) for p in P}),
        ("Rangos normativos", {p: seed("CAT-125", p) for p in P}),
        ("Unidad para multas y montos", {p: seed("CAT-508", p) for p in P}),
        ("Categorías de precedente", {p: seed("CAT-311", p) for p in P}),
        ("Organización territorial", {p: "; ".join(v["label"] for v in catv.get("CAT-601", []) if v.get("country") == p) or "Por definir" for p in P}),
        ("Códigos territoriales oficiales", {p: seed("CAT-602", p) for p in P}),
        ("Identificadores propios", {"PE": "Número de norma; número de casación", "CO": "Código de sentencia (C-, T-, SU-)", "AR": "Referencia en Fallos (CSJN)",
                                     "CL": "Rol", "EC": "Número de caso de la Corte Constitucional", "BO": "Número de sentencia constitucional (SCP)",
                                     "MX": "Registro digital del Semanario Judicial"}),
        ("Particularidades a tener en cuenta", {"PE": "Textos Únicos Ordenados con renumeración", "CO": "Exequibilidad condicionada; conceptos DIAN",
                                                "AR": "Sistema federal; Decretos de Necesidad y Urgencia", "CL": "DFL; dictámenes de la Contraloría; 'recurso de amparo' = hábeas corpus",
                                                "EC": "Leyes orgánicas y ordinarias; dólar como moneda", "BO": "Autonomías indígenas; jurisdicción indígena originaria campesina",
                                                "MX": "Sistema federal; tesis y jurisprudencia; reformas judiciales de 2021 y 2024"}),
    ]
    r = 5
    for lab, d in rows:
        _c(ws, r, 1, lab, F_BOLD, FILL_SOFT)
        for j, p in enumerate(P, 2):
            _c(ws, r, j, d.get(p, "Por definir"))
        r += 1
    _c(ws, r, 1, "Datos con particularidad en el país (fórmula)", F_BOLD, FILL_BLOCK)
    for j, p in enumerate(P, 2):
        cl = get_column_letter(5 + P.index(p))
        _c(ws, r, j, f"=COUNTIF('6_Aplicabilidad_pais'!${cl}$2:${cl}${LAST},\"<>No aplica\")-COUNTIF('6_Aplicabilidad_pais'!${cl}$2:${cl}${LAST},\"Común\")",
           F_BOLD, FILL_BLOCK, CEN)
    _c(ws, r + 2, 1, "Estado: semilla elaborada con conocimiento general, no verificada en fuentes oficiales. Requiere validación nacional (decisiones DEC-08, DEC-17, DEC-25, DEC-28, DEC-29).",
       F_SUB, border=False)
    ws.freeze_panes = "B5"

    # ------------------------------------------------------------------ J Ejemplo
    ws = wb.create_sheet("J_Ejemplo"); names.append(ws.title)
    _title(ws, "Ejemplo: lo que la IA sacaría de un documento", "Documento ficticio. Sirve para ver de una vez cómo se combinan datos, etiquetas y especialistas.")
    _hdr(ws, 4, ["Tema", "Dato", "Valor que extraería la IA", "¿Cómo se obtiene?", "ID técnico"], [30, 34, 60, 30, 14])
    EJ = [
        ("Identificación del documento", "Tipo de documento", "Sentencia de casación (Corte Suprema)", "La IA lo lee en el texto", "MDJ-D04-014"),
        ("Identificación del documento", "Número oficial", "Casación N.° 0000-2025 (ficticio)", "La IA lo lee en el texto", "MDJ-D01-006"),
        ("Identificación del documento", "País", "Perú", "La IA lo lee y lo estandariza", "MDJ-D01-004"),
        ("Quién lo emite y de dónde viene", "Órgano emisor", "Sala de Derecho Constitucional y Social (ficticio)", "La IA lo lee y lo estandariza", "MDJ-D02-002"),
        ("Fechas y vigencia", "Fecha de emisión", "2025-06-12", "La IA lo lee en el texto", "MDJ-D03-001"),
        ("Personas e instituciones", "Demandante", "Persona natural · su nombre NO se extrae (privacidad)", "La IA lo interpreta", "MDJ-D13-005"),
        ("Personas e instituciones", "Demandado", "Empresa textil S.A. (persona jurídica)", "La IA lo lee en el texto", "MDJ-D13-006"),
        ("Personas e instituciones", "Ponente", "Juez supremo (funcionario público)", "La IA lo lee en el texto", "MDJ-D13-015"),
        ("Proceso y decisión", "Pretensión", "Reposición por despido nulo por embarazo", "La IA lo interpreta", "MDJ-D14-013"),
        ("Proceso y decisión", "Sentido del fallo", "Fundado: casa la sentencia y ordena la reposición", "La IA lo lee y lo estandariza", "MDJ-D14-018"),
        ("Estructura y contenido", "Problema jurídico", "¿El despido de una trabajadora gestante es nulo si el empleador no prueba otra causa?", "La IA lo interpreta", "MDJ-D05-048"),
        ("Montos y cifras", "Monto ordenado", "S/ 18 500 por remuneraciones devengadas (rol: ordenado)", "La IA lo lee en el texto", "MDJ-D09-015"),
        ("Citas y relaciones", "Norma citada y relación", "Ley laboral, art. 29 → la sentencia lo APLICA (no solo lo cita)", "La IA lo interpreta", "MDJ-D07-053"),
        ("Peso jurídico", "¿Se declara precedente?", "No consta", "La IA lo lee en el texto", "MDJ-D17-001"),
        ("Etiquetas por área", "Etiqueta principal", "Laboral › Derecho individual › Despido y estabilidad laboral", "La IA lo interpreta", "MDJ-D06-021"),
        ("Etiquetas por área", "Etiqueta secundaria", "Derechos Humanos › Igualdad y no discriminación", "La IA lo interpreta", "MDJ-D06-006"),
        ("Sector económico", "Sector del caso", "Confección de prendas (contexto, no regula el sector)", "La IA lo interpreta", "MDJ-D10-007"),
        ("Privacidad y derechos de uso", "Datos sensibles", "Sí: embarazo (salud) → se protege en la consulta", "La IA lo interpreta", "MDJ-D16-011"),
        ("Especialistas", "Entra al especialista Laboral", "Sí (tiene la etiqueta Laboral)", "Se calcula con otros datos", "MDJ-OPE-009"),
        ("Especialistas", "Entra al especialista Moda", "No: la confección es solo el sector del caso y la materia es laboral", "Se calcula con otros datos", "MDJ-OPE-009"),
        ("Calidad del documento", "Texto completo y legible", "Sí (PDF nativo, sin OCR)", "Se calcula con otros datos", "MDJ-D11-011"),
    ]
    for i, row in enumerate(EJ, 5):
        fill = FILL_BLOCK if row[0] in ("Etiquetas por área", "Especialistas") else None
        for j, v in enumerate(row, 1):
            _c(ws, i, j, v, F_BOLD if j in (1, 2) else F_BODY, fill)
    ws.freeze_panes = "A5"

    # ------------------------------------------------------------------ K Glosario
    ws = wb.create_sheet("K_Glosario"); names.append(ws.title)
    _title(ws, "Glosario", "Las palabras del proyecto, en una línea.")
    _hdr(ws, 4, ["Palabra", "Qué significa"], [30, 110])
    G = [("Metadato", "Un dato sobre un documento: su número, su fecha, de qué trata, quién lo dictó, qué cita."),
         ("Etiqueta", "Un metadato especial que dice de qué materia trata el documento (Laboral, Minero…). Un documento puede tener varias."),
         ("Área principal", "Rama grande del Derecho (27 en total): Laboral, Civil, Tributario, Penal…"),
         ("Especialidad", "Parte de un área. Puede ser una rama clásica (Derecho colectivo del trabajo) o un sector (Minero, Bancario)."),
         ("Subespecialidad", "Tema más específico dentro de una especialidad (Despido, Crédito fiscal…)."),
         ("Etiqueta principal / secundaria", "Principal: el documento trata de eso en primer lugar. Secundaria: también lo resuelve, pero no es lo central."),
         ("Mención", "El documento solo nombra o cita algo de pasada. No genera etiqueta."),
         ("Especialista", "Un asistente de Juztina que trabaja con los documentos de ciertas etiquetas."),
         ("Obra", "El documento como acto jurídico (la Ley X), independiente del archivo en que esté."),
         ("Versión", "El texto de una norma en un periodo de tiempo; cambia cuando la norma se modifica."),
         ("Unidad estructural", "Una parte del documento: un artículo, un considerando, la parte resolutiva."),
         ("Manifestación", "El archivo concreto (PDF, HTML) que tiene Juztina."),
         ("Evidencia", "El pedazo exacto de texto del que sale cada dato. Permite verificarlo."),
         ("1ª lectura (pasada masiva)", "La lectura completa de toda la base que hará la IA una vez. Ahí se saca lo imprescindible."),
         ("Se calcula después", "Datos que no exigen volver a leer: se deducen de los ya extraídos (por ejemplo, si una norma sigue vigente)."),
         ("Catálogo", "Lista cerrada de valores permitidos para un dato (por ejemplo, la lista de países)."),
         ("Semilla / por validar", "Propuesta inicial que debe revisar un abogado del país o de la materia antes de usarse."),
         ("Prioridad P0–P3", "P0 imprescindible, P1 importante, P2 análisis profundo, P3 complementario."),
         ("ID técnico", "Código único de cada dato (MDJ-…) o etiqueta (CON-…). Nunca cambia."),
         ("Anexo técnico", "Las pestañas grises numeradas: el detalle para el equipo de ingeniería.")]
    for i, (a, b) in enumerate(G, 5):
        _c(ws, i, 1, a, F_BOLD); _c(ws, i, 2, b)

    for n in names:
        wb[n].sheet_properties.tabColor = TEAL
        wb[n].sheet_view.zoomScale = 100
    return names
