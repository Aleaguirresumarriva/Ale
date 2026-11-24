"""Campos de D3 (Temporalidad y vigencia) y D5 (Contenido y estructura). Grupo 2."""
from esquema import CAMPO_CLAVES

EX = "Explícito en documento"; NR = "Normalizado por regla"; IN = "Inferido por modelo"
DC = "Derivado por cálculo"; CJ = "Conclusión jurídica por reglas"; FE = "Fuente externa"
GS = "Generado por sistema"; CP = "Curado por persona"
ED = "Extracción directa"; NO = "Normalización"; CL = "Clasificación"; IF = "Inferencia"
CA = "Cálculo"; EE = "Enriquecimiento externo"; RH = "Revisión humana"; SI = "Generado por sistema"

EV = "Afirmación compuesta: evento temporal"
OP = "Afirmación compuesta: operación modificatoria"
UE = "Unidad estructural"; FT = "Fragmento textual"

FIELDS = []

def mk(id, tech, func, prof, unit, dtype, card, defn, just, values, example, origin, method,
       evidence, extraction, validation, prio, mode, stage, risk, funcs, review="No",
       privacy="Ninguna", deps="No aplica: campo autónomo", obs="Sin observaciones adicionales.",
       appl=None, countries="ALL", cs="Común", pending="No"):
    d = dict(id=id, tech=tech, func=func, dim=id.split("-")[1], profiles=prof, unit=unit, defn=defn,
             just=just, dtype=dtype, card=card, values=values, example=example, origin=origin,
             method=method, evidence=evidence, extraction=extraction, validation=validation,
             applicability=appl or f"Perfiles {prof}; todos los países salvo indicación en Estado por país.",
             prio=prio, mode=mode, review=review, privacy=privacy, deps=deps, funcs=funcs, obs=obs,
             stage=stage, risk=risk, countries=countries, country_status=cs, pending=pending)
    assert list(d) == [k for k, _ in CAMPO_CLAVES]
    FIELDS.append(d)

ANCLA = "Ancla al tramo literal en la manifestación (posición inicial y final) y sección donde aparece."
NA_VAL = "No aplica: valor libre o fecha; se valida por formato."
FECHA_VAL = "Fecha ISO 8601 válida; no posterior a la fecha de captura salvo fechas de efecto futuras; coherente con las demás fechas de la obra."

# =====================================================================
# D03 — TEMPORALIDAD Y VIGENCIA
# =====================================================================
# --- Fechas documentales de la obra ---
mk("MDJ-D03-001", "fecha_emision", "Fecha de emisión o expedición", "UNI", "Obra", "Fecha parcial", "0..1 obligatorio condicionado",
   "Fecha en que el emisor dicta, firma o expide el acto o resolución; en doctrina, fecha de cierre o redacción si consta.",
   "Fecha documental básica para identificar, ordenar y resolver la versión de destino de las citas.",
   NA_VAL, "2011-08-19", EX, ED + " + " + NO, ANCLA,
   "Tomar la fecha del encabezado, del lugar y fecha previo a las firmas o de la fórmula de expedición ('Dado en…'). Si hay varias, preferir la de firma del emisor. No usar la fecha de publicación.",
   FECHA_VAL + " Debe ser ≤ fecha de publicación cuando ambas existan.", "P0", "A", "E3", "R2", "F03; F04; F06; F11; F15",
   obs="Obligatoria en normativa, jurisprudencia y actos; opcional en doctrina (usar fecha de publicación).")
mk("MDJ-D03-002", "fecha_aprobacion_organo", "Fecha de aprobación por el órgano deliberante", "NOR", "Obra", "Fecha", "0..1 opcional",
   "Fecha en que el órgano legislativo o colegiado aprueba el texto, distinta de la promulgación por el Ejecutivo.",
   "Permite reconstruir el procedimiento de producción normativa y distinguir fechas que los usuarios confunden.",
   NA_VAL, "2011-07-14", EX, ED + " + " + NO, ANCLA,
   "Extraer solo si el texto la declara (p. ej., 'aprobada por el Congreso el…', 'dada en la Sala de Sesiones…').",
   FECHA_VAL + " Debe ser ≤ fecha de promulgación.", "P1", "A", "E3", "R3", "F04; F06",
   obs="La denominación del acto ('sanción', 'aprobación') varía por país; no se normaliza el término, solo la fecha.",
   cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-003", "fecha_promulgacion", "Fecha de promulgación o sanción ejecutiva", "NOR", "Obra", "Fecha", "0..1 opcional",
   "Fecha en que la autoridad competente promulga o sanciona la norma para su publicación, según la terminología del país.",
   "Hito jurídico distinto de la emisión y de la publicación; algunos regímenes computan plazos desde él.",
   NA_VAL, "2011-08-19", EX, ED + " + " + NO, ANCLA,
   "Extraer de la fórmula promulgatoria ('Por tanto: mando se publique y cumpla', 'promúlguese') y su fecha.",
   FECHA_VAL, "P1", "A", "E3", "R3", "F04; F06",
   obs="En algunos países 'sanción' designa la aprobación legislativa y no la promulgación: el término original se conserva en observaciones de la afirmación.",
   cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-004", "fecha_publicacion", "Fecha de publicación", "UNI", "Obra", "Fecha parcial", "0..1 obligatorio condicionado",
   "Fecha en que la obra se publica en el medio oficial (normativa, actos generales) o en el medio editorial (doctrina, jurisprudencia publicada).",
   "Hito que suele determinar la entrada en vigor y la oponibilidad; dato de búsqueda frecuente.",
   NA_VAL, "2011-08-20", EX, ED + " + " + NO, "Ancla al dato en el texto o al encabezado de la edición del diario o revista; si viene de la fuente, registro de fuente externa.",
   "Tomar la fecha de la edición del diario oficial o publicación que contiene la obra; en doctrina, fecha o año del número de la revista o edición del libro.",
   FECHA_VAL + " Debe ser ≥ fecha de emisión.", "P0", "A", "E3", "R2", "F03; F05; F06; F15",
   deps="MDJ-D03-001", obs="Para doctrina admite precisión de año o mes (ver MDJ-D03-006). El medio de publicación se registra en D2.")
mk("MDJ-D03-005", "fecha_notificacion_declarada", "Fecha de notificación declarada", "JUR; ADM", "Obra", "Fecha", "0..n",
   "Fecha o fechas de notificación de la resolución o acto que constan en el propio documento o en sus constancias.",
   "Cómputo de plazos de impugnación y de firmeza; análisis procesal.",
   NA_VAL, "2023-03-02", EX, ED + " + " + NO, ANCLA,
   "Extraer solo fechas de notificación expresas en el documento (cédula, constancia, cargo). No inferir desde la emisión.",
   FECHA_VAL + " Debe ser ≥ fecha de emisión.", "P2", "A", "E3", "R2", "F07; F14",
   privacy="Puede contener datos personales", obs="Si la constancia identifica al notificado, aplicar la política de datos personales (DEC-18).", pending="DEC-18")
mk("MDJ-D03-006", "precision_fecha_publicacion", "Precisión de la fecha de publicación", "UNI", "Obra", "Enum", "1 obligatorio",
   "Nivel de precisión con que se conoce la fecha de publicación: día, mes, año o desconocida.",
   "Evita presentar como exacta una fecha aproximada (frecuente en doctrina y fuentes antiguas).",
   "CAT-219 Precisión de fecha", "anio", NR, NO, "Regla aplicada sobre MDJ-D03-004.",
   "Asignar según los componentes efectivamente presentes en la fecha extraída.",
   "Valor del catálogo; 'dia' solo si MDJ-D03-004 tiene día.", "P0", "A", "E3", "R3", "F03; F16", deps="MDJ-D03-004")
mk("MDJ-D03-007", "fecha_firmeza", "Fecha de firmeza o ejecutoria", "JUR; ADM", "Obra", "Fecha", "0..1 opcional",
   "Fecha desde la que la resolución o acto queda firme, consentido o ejecutoriado, cuando consta expresamente.",
   "Determina si un pronunciamiento es definitivo y desde cuándo produce cosa juzgada o firmeza administrativa.",
   NA_VAL, "2023-04-15", EX, ED + " + " + NO, "Ancla a la constancia o resolución que declara la firmeza; si proviene de otra obra, relación con esa obra.",
   "Extraer de constancias o resoluciones que declaran firme o ejecutoriada la decisión. No calcular a partir de plazos en esta etapa.",
   FECHA_VAL + " Debe ser ≥ fecha de notificación cuando exista.", "P1", "A", "E3", "R1", "F07; F08; F14",
   review="Condicionado", obs="La firmeza calculada por vencimiento de plazos es una conclusión jurídica (MDJ-D03-044).")
mk("MDJ-D03-008", "fecha_entrada_vigor_expresa", "Fecha de entrada en vigor expresa", "NOR; ADM", "Obra", "Fecha", "0..1 opcional",
   "Fecha calendario de entrada en vigor fijada expresamente por la propia obra.",
   "Hecho primario no reconstruible sin leer las disposiciones finales; base del cálculo de vigencia.",
   NA_VAL, "2012-01-01", EX, ED + " + " + NO, ANCLA,
   "Buscar en disposiciones finales, transitorias o artículo de vigencia fórmulas como 'entrará en vigor el…', 'rige a partir del…'. Registrar también el evento en MDJ-D03-015.",
   FECHA_VAL + " Si es anterior a la publicación, marcar retroactividad (MDJ-D03-022).", "P0", "A", "E3", "R1", "F05; F06; F02",
   appl="Normativa y actos administrativos de alcance general.")
mk("MDJ-D03-009", "base_computo_entrada_vigor", "Base de cómputo de la entrada en vigor", "NOR; ADM", "Obra", "Enum", "1 obligatorio",
   "Criterio que determina la entrada en vigor: fecha expresa, desde la publicación, plazo desde la publicación, condicionada a reglamentación, a un evento, o regla supletoria del país.",
   "Separa la regla de vigencia declarada del cálculo posterior; indica cuándo aplicar reglas nacionales.",
   "CAT-220 Base de cómputo de la entrada en vigor", "plazo_desde_publicacion", EX, ED + " + " + CL, ANCLA,
   "Clasificar la fórmula de vigencia hallada. Si no hay fórmula, asignar 'regla_supletoria' y estado de campo 'no encontrado' para la fórmula.",
   "Valor del catálogo; si es 'fecha_expresa', MDJ-D03-008 debe tener valor; si es 'plazo_desde_publicacion', MDJ-D03-010 debe tener valor.", "P0", "A", "E3", "R1", "F05; F06",
   deps="MDJ-D03-008; MDJ-D03-010", appl="Normativa y actos administrativos de alcance general.")
mk("MDJ-D03-010", "texto_vacatio_legis", "Fórmula de vacatio o plazo de entrada en vigor", "NOR; ADM", "Obra", "String", "0..1 opcional",
   "Texto literal que fija el plazo entre publicación y entrada en vigor o la condición de la que depende.",
   "Conserva la fuente exacta del cómputo para recalcular si cambian las reglas de cómputo de plazos.",
   NA_VAL, "a los noventa días calendario de su publicación", EX, ED, ANCLA,
   "Copiar literalmente la expresión del plazo o condición, sin interpretarla.",
   "Debe coincidir literalmente con el texto anclado.", "P0", "A", "E3", "R2", "F05; F06",
   appl="Normativa y actos administrativos de alcance general.")
mk("MDJ-D03-011", "fecha_entrada_vigor_calculada", "Fecha de entrada en vigor calculada", "NOR; ADM", "Obra", "Fecha", "0..1 opcional",
   "Fecha de entrada en vigor obtenida aplicando la base de cómputo y, en su defecto, la regla supletoria del país.",
   "Necesaria para el cálculo de vigencia y para las alertas; se separa del dato expreso.",
   NA_VAL, "2011-11-18", CJ, CA, "Regla aplicada (ID y versión) y campos de entrada (MDJ-D03-004, -009, -010).",
   "No se extrae. Se calcula con reglas versionadas por país; si la regla del país no está validada, estado de campo 'indeterminado'.",
   FECHA_VAL + " Igual a MDJ-D03-008 cuando la base es 'fecha_expresa'.", "P0", "B", "E7", "R1", "F05; F06; F02",
   review="Condicionado", deps="MDJ-D03-004; MDJ-D03-008; MDJ-D03-009; MDJ-D03-010",
   obs="Cómputo de días hábiles o calendario y reglas supletorias son Derecho de cada país.", cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-012", "naturaleza_temporal_norma", "Naturaleza temporal de la norma", "NOR; ADM", "Obra", "Enum", "1 obligatorio",
   "Indica si la obra es permanente, temporal con plazo, temporal condicionada a un evento o de vigencia diferida.",
   "Identifica normas que pierden vigencia sin derogación expresa (p. ej., normas temporales o de emergencia).",
   "CAT-217 Naturaleza temporal de la norma", "temporal_con_plazo", IN, CL, ANCLA,
   "Asignar 'temporal' solo si la obra fija un término o condición de vigencia; por defecto 'permanente' con estado de campo 'no encontrado' para el término.",
   "Si es temporal con plazo, MDJ-D03-013 debe tener valor.", "P1", "A", "E3", "R2", "F05; F06",
   appl="Normativa y actos administrativos de alcance general.")
mk("MDJ-D03-013", "fecha_fin_vigencia_expresa", "Fecha de término de vigencia expresa", "NOR; ADM", "Obra", "Fecha", "0..1 opcional",
   "Fecha o plazo final de vigencia fijado por la propia obra (normas temporales, de emergencia, presupuestarias).",
   "Hecho primario necesario para no presentar como vigente una norma agotada.",
   NA_VAL, "2020-12-31", EX, ED + " + " + NO, ANCLA,
   "Extraer de fórmulas como 'regirá hasta el…', 'por el plazo de… días'. Si es plazo, registrar el texto en observaciones de la afirmación y calcular después.",
   FECHA_VAL + " Debe ser > fecha de entrada en vigor.", "P0", "A", "E3", "R1", "F05; F06", deps="MDJ-D03-012")
mk("MDJ-D03-014", "periodo_aplicacion_declarado", "Periodo o ejercicio de aplicación declarado", "NOR; ADM", "Obra", "Intervalo de fechas", "0..1 opcional",
   "Periodo al que la obra declara aplicarse (ejercicio fiscal, campaña, año presupuestario), distinto de su vigencia formal.",
   "Leyes de presupuesto, tributarias anuales y actos periódicos se buscan por periodo de aplicación.",
   NA_VAL, "2024-01-01/2024-12-31", EX, ED + " + " + NO, ANCLA,
   "Extraer cuando la obra declare 'para el año fiscal…', 'ejercicio…', 'periodo…'.",
   "Intervalo válido; inicio ≤ fin.", "P1", "A", "E3", "R2", "F03; F10; F13",
   obs="Coordinar con el ámbito temporal de D8 para evitar duplicidad: aquí solo el periodo declarado de la obra completa.")

# --- Evento temporal (afirmación compuesta) ---
mk("MDJ-D03-015", "evento_tipo", "Tipo de evento temporal", "UNI", EV, "Enum", "1 obligatorio",
   "Clase del hito jurídico o documental registrado: publicación, entrada en vigor, modificación, derogación expresa o genérica, suspensión, declaración de inconstitucionalidad, rectificación, entre otros.",
   "Los eventos son los hechos primarios de los que se calcula la vigencia; su tipo determina la regla aplicable.",
   "CAT-201 Tipo de evento temporal", "derogacion_expresa", EX, ED + " + " + CL, ANCLA,
   "Registrar un evento por cada fórmula operativa o hito fechado identificado en la obra o en otra obra que la afecta.",
   "Valor del catálogo; coherente con el verbo de la operación cuando existe (MDJ-D03-027).", "P0", "A", "E3", "R1", "F05; F06; F11; F12")
mk("MDJ-D03-016", "evento_unidad_afectada", "Unidad afectada por el evento", "UNI", EV, "Referencia", "0..1 obligatorio condicionado",
   "Obra, versión o unidad estructural sobre la que recae el evento (p. ej., el literal derogado).",
   "Permite registrar el evento en el nivel exacto al que apunta la operación, no en el documento completo.",
   "Referencia a Obra o Unidad estructural", "UE-000781 (art. 22, Ley X)", DC, CA, "Referencia resuelta + ancla del destino literal.",
   "Se completa al resolver el destino literal (MDJ-D03-029). Vacío con estado 'indeterminado' si el destino es genérico o ambiguo.",
   "Debe existir en la base; su nivel debe coincidir con el nivel indicado en el destino literal.", "P0", "B", "E7", "R1", "F05; F06; F11; F12",
   deps="MDJ-D03-029; MDJ-D03-030")
mk("MDJ-D03-017", "evento_fecha_efecto", "Fecha de efecto del evento", "UNI", EV, "Fecha", "0..1 obligatorio condicionado",
   "Fecha jurídica desde la que el evento produce efecto (tiempo jurídico).",
   "Eje del modelo bitemporal: permite responder qué regía en una fecha dada.",
   NA_VAL, "2016-07-01", EX, ED + " + " + NO, ANCLA,
   "Extraer la fecha de efecto expresa; si no existe, dejar estado 'no encontrado' y calcularla en MDJ-D03-018.",
   FECHA_VAL, "P0", "A", "E3", "R1", "F05; F06")
mk("MDJ-D03-018", "evento_fecha_efecto_calculada", "Fecha de efecto calculada del evento", "UNI", EV, "Fecha", "0..1 opcional",
   "Fecha de efecto obtenida por regla cuando el evento no declara fecha propia (p. ej., entrada en vigor de la norma que lo contiene).",
   "Completa la línea de vida sin presentar como expresa una fecha deducida.",
   NA_VAL, "2016-06-25", CJ, CA, "Regla aplicada y eventos de entrada en vigor de la obra fuente.",
   "Calcular desde la entrada en vigor de la obra fuente del evento según reglas de país.",
   FECHA_VAL, "P0", "B", "E7", "R1", "F05; F06", review="Condicionado",
   deps="MDJ-D03-017; MDJ-D03-011; MDJ-D03-023", cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-019", "evento_fecha_fin_efecto", "Fecha de fin de efecto del evento", "UNI", EV, "Fecha", "0..1 opcional",
   "Fecha en que cesa el efecto de un evento temporal (fin de una suspensión, término de una prórroga).",
   "Permite cerrar intervalos de estado sin crear eventos ficticios.",
   NA_VAL, "2021-03-31", EX, ED + " + " + NO, ANCLA,
   "Extraer solo cuando el evento declara su término.", FECHA_VAL + " Debe ser > fecha de efecto.", "P1", "A", "E3", "R1", "F05; F06")
mk("MDJ-D03-020", "evento_precision_fecha", "Precisión de la fecha del evento", "UNI", EV, "Enum", "1 obligatorio",
   "Precisión con que se conoce la fecha del evento.", "Evita falsas precisiones en eventos tomados de notas editoriales.",
   "CAT-219 Precisión de fecha", "dia", NR, NO, "Regla aplicada.", "Asignar según los componentes de la fecha.",
   "Valor del catálogo.", "P0", "A", "E3", "R3", "F16")
mk("MDJ-D03-021", "evento_texto_literal", "Texto literal del evento", "UNI", EV, "Texto largo", "1 obligatorio",
   "Fórmula o enunciado exacto que expresa el evento.", "Evidencia primaria auditable; permite reinterpretar sin releer la obra.",
   NA_VAL, "Derógase el literal c) del artículo 22 de la Ley N.° …", EX, ED, ANCLA,
   "Copiar el enunciado completo que contiene el verbo operativo y su destino.",
   "Debe coincidir literalmente con el tramo anclado (verificación de cadena).", "P0", "A", "E3", "R1", "F05; F06; F15; F16")
mk("MDJ-D03-022", "evento_retroactivo", "Evento con efecto retroactivo declarado", "UNI", EV, "Boolean", "1 obligatorio",
   "Indica si el texto declara que el evento produce efectos antes de su publicación o entrada en vigor.",
   "La retroactividad altera la reconstrucción histórica del Derecho aplicable.",
   "Sí / No", "No", EX, ED + " + " + CL, ANCLA,
   "Marcar 'Sí' solo con declaración expresa ('con eficacia desde…', 'retroactivamente'). Sin declaración: 'No'.",
   "Si es 'Sí', la fecha de efecto debe ser anterior a la de publicación de la obra fuente.", "P0", "A", "E3", "R1", "F05; F06")
mk("MDJ-D03-023", "evento_obra_fuente", "Obra que origina el evento", "UNI", EV, "Referencia", "1 obligatorio",
   "Obra y unidad estructural que contienen el enunciado del evento (p. ej., la norma derogante y su artículo).",
   "Trazabilidad: cada cambio de estado remite a la disposición que lo produjo.",
   "Referencia a Obra y Unidad estructural", "Ley Y, art. 2", GS, SI, "Identidad de la unidad donde se extrajo el enunciado.",
   "Asignar automáticamente la unidad de la que se extrajo el evento.", "Debe existir y contener la evidencia del evento.", "P0", "A", "E3", "R1", "F06; F11; F12")
mk("MDJ-D03-024", "evento_destino_determinado", "Evento con destino determinado", "NOR; ADM", EV, "Boolean", "1 obligatorio",
   "Indica si el evento identifica su destino (obra o unidad concreta) o es genérico, como 'deróganse las disposiciones que se opongan'.",
   "Las cláusulas derogatorias genéricas no deben cambiar el estado de ninguna norma concreta.",
   "Sí / No", "No", EX, CL, ANCLA,
   "Marcar 'No' cuando la fórmula no nombra obra o disposición identificable.",
   "Si es 'No', MDJ-D03-016 debe quedar vacío y el evento no alimenta el cálculo de vigencia.", "P0", "A", "E3", "R1", "F05; F06")
mk("MDJ-D03-025", "evento_tipo_fuente", "Tipo de fuente del evento", "UNI", EV, "Enum", "1 obligatorio",
   "Procedencia del dato del evento: documento oficial que lo contiene, nota editorial de un texto consolidado, fuente oficial externa o curaduría.",
   "Separa eventos oficiales de eventos tomados de anotaciones editoriales, que no tienen el mismo valor.",
   "CAT-221 Tipo de fuente del evento", "nota_editorial_consolidado", NR, NO, "Identificación de la manifestación y del tipo de texto.",
   "Asignar según la manifestación de la que se extrajo el evento.", "Valor del catálogo; coherente con el tipo de texto de la versión.", "P0", "A", "E3", "R2", "F05; F06; F16",
   deps="MDJ-D03-051")
mk("MDJ-D03-026", "evento_fecha_registro", "Fecha de registro del evento en Juztina", "UNI", EV, "Datetime", "1 obligatorio",
   "Momento en que Juztina registró el evento (tiempo de registro del modelo bitemporal).",
   "Permite auditar qué mostraba Juztina en una fecha dada, distinto del tiempo jurídico.",
   NA_VAL, "2027-02-10T14:32:00Z", GS, SI, "No aplica: generado por el sistema.",
   "Asignar al persistir el evento.", "Datetime UTC válido; no modificable.", "P0", "A", "Sistema", "R3", "F16")

# --- Operación modificatoria (afirmación compuesta) ---
mk("MDJ-D03-027", "operacion_verbo", "Verbo de la operación modificatoria", "NOR; ADM", OP, "Enum", "1 obligatorio",
   "Operación jurídica que una disposición realiza sobre otra: modifica, sustituye, incorpora, deroga, renumera, reubica, suspende, prorroga, rectifica, ordena o refunde.",
   "Hecho primario del que dependen la identidad de las unidades, las versiones y la vigencia.",
   "CAT-202 Verbo de operación modificatoria", "incorpora", EX, ED + " + " + CL, ANCLA,
   "Identificar en la unidad de la norma modificatoria el verbo operativo y normalizarlo al catálogo; una afirmación por cada operación.",
   "Valor del catálogo; el verbo literal anclado debe corresponder semánticamente.", "P0", "A", "E6", "R1", "F05; F06; F11; F12",
   appl="Normativa y actos administrativos de alcance general que modifican otros textos.")
mk("MDJ-D03-028", "operacion_verbo_literal", "Verbo literal de la operación", "NOR; ADM", OP, "String", "1 obligatorio",
   "Forma exacta del verbo operativo usada en el texto ('Modifícase', 'Adiciónase', 'Sustitúyese').",
   "Conserva la expresión original para validar la normalización y para reglas nacionales.",
   NA_VAL, "Incorpórase", EX, ED, ANCLA, "Copiar el verbo tal como aparece.", "Coincidencia literal con la evidencia.", "P0", "A", "E6", "R2", "F16")
mk("MDJ-D03-029", "operacion_destino_literal", "Destino literal de la operación", "NOR; ADM", OP, "String", "1 obligatorio",
   "Designación textual de la obra y disposición afectadas, tal como aparece.",
   "Base para resolver el destino; se conserva aunque el destino no esté en la base.",
   NA_VAL, "literal c) del artículo 22 de la Ley N.° 29783", EX, ED, ANCLA,
   "Copiar la designación completa del destino, incluidos niveles inferiores (párrafo, inciso, literal).",
   "Coincidencia literal con la evidencia.", "P0", "A", "E6", "R1", "F05; F06; F11")
mk("MDJ-D03-030", "operacion_nivel_destino", "Nivel estructural del destino", "NOR; ADM", OP, "Enum", "1 obligatorio",
   "Nivel estructural al que apunta la operación (obra, título, artículo, párrafo, inciso, literal…).",
   "La operación se registra en el nivel exacto afectado, no en el artículo o la obra completa.",
   "CAT-208 Nivel estructural", "literal", NR, NO, ANCLA,
   "Normalizar el nivel más fino mencionado en el destino literal.", "Valor del catálogo.", "P0", "A", "E6", "R2", "F05; F06", deps="MDJ-D03-029")
mk("MDJ-D03-031", "operacion_destino_resuelto", "Destino resuelto de la operación", "NOR; ADM", OP, "Referencia", "0..1 obligatorio condicionado",
   "Obra y unidad estructural de la base que corresponden al destino literal, en la versión vigente a la fecha de efecto.",
   "Une la operación con la unidad afectada para generar versiones y eventos.",
   "Referencia a Obra o Unidad estructural", "UE-000781", DC, CA, "Regla de resolución aplicada y destino literal.",
   "Resolver con el motor de referencias (D7); si no se resuelve, conservar el literal con estado de resolución.",
   "La unidad debe existir en la versión vigente a la fecha de efecto.", "P0", "B", "E7", "R1", "F05; F06; F11; F12",
   deps="MDJ-D03-029; MDJ-D03-030; MDJ-D03-035")
mk("MDJ-D03-032", "operacion_nuevo_texto_ancla", "Nuevo texto introducido por la operación", "NOR; ADM", OP, "Ancla de evidencia", "0..1 obligatorio condicionado",
   "Límites exactos del texto que la operación introduce o con el que sustituye al anterior.",
   "Permite reconstruir versiones sin releer la norma modificatoria.",
   NA_VAL, "Manifestación M-55, caracteres 10 412–11 980", EX, ED, "Ancla de inicio y fin del nuevo texto.",
   "Delimitar el texto entre comillas o bloque que sigue a 'queda redactado de la siguiente manera'. Obligatorio para modifica, sustituye e incorpora.",
   "El tramo debe existir en la manifestación y no incluir la fórmula operativa.", "P0", "A", "E6", "R1", "F06; F15",
   obs="El texto se almacena una sola vez en el fragmento textual de la unidad modificatoria; aquí solo el ancla.")
mk("MDJ-D03-033", "operacion_nuevo_rotulo", "Nuevo rótulo asignado", "NOR; ADM", OP, "String", "0..1 obligatorio condicionado",
   "Rótulo que la operación asigna a la unidad incorporada, renumerada o sustituida ('Artículo 22-A', 'Artículo 5 Bis').",
   "Necesario para la identidad estructural y la continuidad.",
   NA_VAL, "Artículo 22-A", EX, ED, ANCLA,
   "Extraer cuando la operación incorpora, renumera o sustituye con rótulo distinto.",
   "Debe aparecer literalmente en la evidencia.", "P0", "A", "E6", "R1", "F06", deps="MDJ-D03-027")
mk("MDJ-D03-034", "operacion_nueva_ubicacion_literal", "Ubicación declarada de la unidad", "NOR; ADM", OP, "String", "0..1 opcional",
   "Indicación textual del lugar donde se inserta o reubica la unidad ('después del artículo 22', 'en el Capítulo IV').",
   "Permite colocar la unidad en la ruta jerárquica correcta de la nueva versión.",
   NA_VAL, "en el Capítulo IV del Título II", EX, ED, ANCLA,
   "Extraer en incorporaciones y reubicaciones.", "Coincidencia literal con la evidencia.", "P0", "A", "E6", "R2", "F06")
mk("MDJ-D03-035", "operacion_fecha_efecto_expresa", "Fecha de efecto expresa de la operación", "NOR; ADM", OP, "Fecha", "0..1 opcional",
   "Fecha de efecto que la operación declara para sí, distinta de la de la norma que la contiene.",
   "Hay operaciones con vigencia diferida o retroactiva dentro de una misma norma.",
   NA_VAL, "2025-01-01", EX, ED + " + " + NO, ANCLA, "Extraer solo si la operación declara su propia fecha.", FECHA_VAL, "P0", "A", "E6", "R1", "F05; F06")
mk("MDJ-D03-036", "operacion_orden", "Orden de la operación en la norma", "NOR; ADM", OP, "Integer", "1 obligatorio",
   "Posición secuencial de la operación dentro de la norma modificatoria.",
   "Varias operaciones de una misma norma sobre la misma unidad deben aplicarse en orden.",
   NA_VAL, "3", GS, SI, "Posición de la evidencia.", "Asignar por orden de aparición.", "Entero ≥ 1, único por obra fuente.", "P0", "A", "E6", "R3", "F06")
mk("MDJ-D03-037", "correspondencias_declaradas", "Tabla de correspondencias declarada", "NOR", "Obra", "Array", "0..n",
   "Pares rótulo anterior → rótulo nuevo declarados por la propia norma (tabla de correspondencias de textos ordenados, códigos o renumeraciones).",
   "Única fuente de continuidad declarada en reordenaciones masivas; no reconstruible con confianza después.",
   NA_VAL, "[{'origen':'Art. 22','destino':'Art. 25'}]", EX, ED, "Ancla a la tabla o anexo de correspondencias.",
   "Extraer filas completas de la tabla de correspondencias cuando exista; no inferir pares ausentes.",
   "Cada rótulo debe existir en la obra de origen o destino correspondiente.", "P0", "A", "E6", "R1", "F06; F11",
   obs="Rango y efectos de los textos ordenados se validan por país.", cs="Condicionado", pending="DEC-04")

# --- Estado de vigencia (conclusión calculada) ---
mk("MDJ-D03-038", "estado_vigencia_unidad", "Estado de vigencia de la unidad", "NOR; ADM", UE, "Enum", "1 obligatorio",
   "Situación jurídica calculada de la unidad estructural a la fecha de corte: aún no vigente, vigente, vigente con modificaciones, parcialmente derogada, derogada, suspendida, expulsada o inexequible, exequible condicionada o indeterminada.",
   "Responde '¿esto rige?' a nivel de disposición; nunca se extrae directamente del documento.",
   "CAT-203 Estado de vigencia", "vigente_con_modificaciones", CJ, CA, "Eventos fundantes (MDJ-D03-041) y regla aplicada.",
   "No se extrae. Se calcula aplicando reglas versionadas a los eventos con destino determinado; los eventos inferidos o genéricos no alimentan el cálculo.",
   "Coherente con los eventos fundantes; 'indeterminada' si faltan reglas de país validadas o eventos esenciales.", "P0", "B", "E7", "R1",
   "F01; F02; F05; F06; F13; F15", review="Condicionado", deps="MDJ-D03-015; MDJ-D03-016; MDJ-D03-017; MDJ-D03-024",
   obs="Sin fuente oficial se presenta como 'sin derogación registrada en Juztina al [fecha]', no como 'vigente'.",
   cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-039", "estado_vigencia_obra", "Estado de vigencia agregado de la obra", "NOR; ADM", "Obra", "Enum", "1 obligatorio",
   "Síntesis del estado de las unidades de la obra (p. ej., vigente con unidades derogadas).",
   "Filtro rápido de búsqueda; no reemplaza el estado por unidad.",
   "CAT-203 Estado de vigencia", "parcialmente_derogada", CJ, CA, "Estados de las unidades y regla de agregación.",
   "Calcular desde los estados de las unidades: derogada solo si todas lo están o hay derogación total expresa.",
   "Coherente con los estados de las unidades.", "P0", "B", "E7", "R1", "F03; F05; F06", review="Condicionado",
   deps="MDJ-D03-038", cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-040", "estado_vigencia_fuente", "Fuente del estado de vigencia", "NOR; ADM", UE, "Enum", "1 obligatorio",
   "Origen del estado: importado de fuente oficial, calculado por Juztina, revisado por persona, importado de fuente editorial o desconocido.",
   "Determina cómo se presenta el estado al usuario y su fiabilidad.",
   "CAT-204 Fuente del estado de vigencia", "calculado", GS, SI, "Registro de la regla o fuente usada.",
   "Asignar al calcular o importar el estado.", "Valor del catálogo.", "P0", "B", "E7", "R1", "F02; F05; F16", deps="MDJ-D03-038")
mk("MDJ-D03-041", "estado_vigencia_eventos_fundantes", "Eventos que fundan el estado de vigencia", "NOR; ADM", UE, "Array de referencias", "0..n",
   "Lista de eventos y operaciones que determinan el estado calculado.",
   "Hace auditable la conclusión jurídica y permite mostrar su respaldo.",
   "Referencias a afirmaciones de evento", "[EV-1201, EV-1388]", DC, CA, "Referencias a eventos con su evidencia.",
   "Registrar todos los eventos usados por la regla.", "Cada referencia debe existir y tener destino determinado.", "P0", "B", "E7", "R1", "F05; F06; F16", deps="MDJ-D03-038")
mk("MDJ-D03-042", "estado_vigencia_fecha_corte", "Fecha de corte del estado de vigencia", "NOR; ADM", UE, "Fecha", "1 obligatorio",
   "Fecha hasta la cual se consideraron eventos registrados para calcular el estado.",
   "La completitud del corpus no está garantizada: el estado vale a una fecha de corte.",
   NA_VAL, "2027-03-31", GS, SI, "No aplica: generado por el sistema.", "Asignar al ejecutar el cálculo.", FECHA_VAL, "P0", "B", "E7", "R1", "F02; F05", deps="MDJ-D03-038")
mk("MDJ-D03-043", "estado_vigencia_respaldo_oficial", "Estado respaldado por fuente oficial", "NOR; ADM", UE, "Boolean", "1 obligatorio",
   "Indica si el estado coincide con una fuente oficial consolidada consultada.",
   "Regla de presentación: sin respaldo oficial se muestra 'sin derogación registrada en Juztina al [fecha]'.",
   "Sí / No", "No", DC, CA + " + " + EE, "Fuente oficial consultada y fecha.", "Comparar el estado calculado con la fuente oficial disponible del país.",
   "Si 'Sí', debe existir referencia a la fuente consultada.", "P1", "B", "E7", "R1", "F02; F05; F16",
   deps="MDJ-D03-038", cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-044", "firmeza_calculada", "Firmeza calculada", "JUR; ADM", "Obra", "Enum", "0..1 opcional",
   "Conclusión sobre si la resolución o acto está firme, impugnado o indeterminado, a partir de la cadena procesal registrada.",
   "Complementa la firmeza declarada cuando no consta; necesaria para valorar el pronunciamiento.",
   "Firme / Impugnado / Revocado o anulado / Indeterminado", "Indeterminado", CJ, CA, "Relaciones procesales registradas y regla aplicada.",
   "Calcular desde la cadena procesal (D7, D14) y plazos validados; sin datos suficientes, 'Indeterminado'.",
   "Coherente con relaciones 'revoca', 'anula', 'confirma' registradas.", "P2", "B", "E7", "R1", "F07; F08", review="Condicionado",
   deps="MDJ-D03-007", cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-045", "condicion_interpretativa_vinculante", "Condición interpretativa impuesta por control de constitucionalidad", "NOR", UE, "Texto largo", "0..n",
   "Lectura obligatoria fijada por una decisión de control (p. ej., exequibilidad condicionada o sentencia interpretativa) que no cambia la letra de la disposición.",
   "Sin ella, el usuario leería un texto cuya aplicación está condicionada.",
   NA_VAL, "Exequible en el entendido de que…", EX, ED, "Ancla a la parte resolutiva de la decisión de control.",
   "Extraer de la parte resolutiva de la decisión de control y vincularla a la unidad afectada.",
   "Debe existir relación de control (D7) entre la decisión y la unidad.", "P0", "A", "E6", "R1", "F02; F05; F08",
   review="Condicionado", obs="Figura con nombre y efectos propios por país; no se equiparan.", cs="Condicionado", pending="DEC-17")
mk("MDJ-D03-046", "alerta_posible_derogacion_tacita", "Alerta de posible derogación tácita", "NOR", UE, "Array de referencias", "0..n",
   "Unidades posteriores posiblemente incompatibles con esta unidad, detectadas por análisis de contenido.",
   "Orienta la curaduría; nunca alimenta el estado de vigencia.",
   "Referencias a unidades estructurales", "[UE-55102]", IN, IF, "Ancla a ambos textos comparados.",
   "Fuera del alcance inicial como proceso masivo; solo a demanda sobre unidades priorizadas.",
   "Toda alerta exige revisión antes de convertirse en relación efectiva.", "Fuera de alcance", "X", "Posterior (C)", "R1", "F05; F16",
   review="Sí", obs="Excluido de la pasada por la arquitectura v3 (clase X).")

# --- Versiones y completitud ---
mk("MDJ-D03-047", "version_id", "Identificador de la versión", "UNI", "Versión", "Identificador", "1 obligatorio",
   "Identificador persistente de la versión de la obra (texto completo vigente en un intervalo).",
   "Permite citar y recuperar el texto exacto de una fecha.", "No aplica: generado por el sistema", "V-0004521-03", GS, SI,
   "No aplica: generado por el sistema.", "Asignar al crear la versión (observada o reconstruida).", "Único; nunca reutilizado.", "P0", "A", "E2", "R3", "F06; F15; F16")
mk("MDJ-D03-048", "version_fecha_inicio", "Inicio del intervalo de la versión", "UNI", "Versión", "Fecha", "1 obligatorio",
   "Fecha jurídica desde la que rige el texto de la versión.", "Base para responder qué decía la obra en una fecha.",
   NA_VAL, "2016-07-01", DC, CA, "Evento originante.", "Igual a la fecha de efecto del evento que origina la versión; para la original, la entrada en vigor.",
   FECHA_VAL, "P0", "B", "E7", "R1", "F06; F15", deps="MDJ-D03-050; MDJ-D03-017; MDJ-D03-011")
mk("MDJ-D03-049", "version_fecha_fin", "Fin del intervalo de la versión", "UNI", "Versión", "Fecha", "0..1 opcional",
   "Fecha jurídica hasta la que rigió el texto; vacío si es la versión actual.", "Cierra intervalos para consultas históricas.",
   NA_VAL, "2019-03-14", DC, CA, "Evento de la versión siguiente.", "Fecha de inicio de la versión siguiente menos un día, o fecha de derogación total.",
   "Debe ser > inicio; no solapar con otras versiones de la misma obra.", "P0", "B", "E7", "R1", "F06; F15", deps="MDJ-D03-048")
mk("MDJ-D03-050", "version_eventos_originantes", "Eventos que originan la versión", "UNI", "Versión", "Array de referencias", "1..n",
   "Eventos u operaciones cuyo efecto crea esta versión (publicación original, modificaciones, rectificaciones).",
   "Trazabilidad entre versiones y normas modificatorias.", "Referencias a eventos u operaciones", "[OP-3321]", DC, CA, "Referencias con evidencia.",
   "Registrar todos los eventos con la misma fecha de efecto que cambian el texto.", "Cada referencia debe existir.", "P0", "B", "E7", "R1", "F06; F11; F12")
mk("MDJ-D03-051", "version_tipo_texto", "Tipo de texto de la versión", "UNI", "Versión", "Enum", "1 obligatorio",
   "Naturaleza del texto: original publicado, consolidado oficial, consolidado editorial, compilación oficial o versión reconstruida por Juztina.",
   "El valor jurídico y la confiabilidad dependen del tipo de texto.", "CAT-205 Tipo de texto", "consolidado_editorial", NR, CL,
   "Identificación de la manifestación y su fuente.", "Asignar según la fuente y las marcas del texto (notas de modificación, sellos oficiales).",
   "Valor del catálogo; 'reconstruida' solo si se generó aplicando operaciones.", "P0", "A", "E1", "R2", "F02; F06; F16", cs="Catálogo por país", pending="DEC-32")
mk("MDJ-D03-052", "version_condicion_observacion", "Condición de observación de la versión", "UNI", "Versión", "Enum", "1 obligatorio",
   "Indica si Juztina tiene una manifestación de la versión, si la reconstruyó aplicando operaciones o si solo conoce su existencia.",
   "Evita presentar textos reconstruidos como si fueran documentos observados.", "CAT-222 Condición de observación de la versión", "reconstruida",
   GS, SI, "No aplica: generado por el sistema.", "Asignar al crear la versión.", "Si 'observada', debe tener al menos una manifestación.", "P0", "B", "E7", "R2", "F06; F15; F16")
mk("MDJ-D03-053", "version_es_rectificacion", "Versión originada por rectificación", "NOR; ADM", "Versión", "Boolean", "1 obligatorio",
   "Indica si la versión proviene de una fe de erratas o rectificación de errores materiales.",
   "Su fecha de efecto sigue reglas propias de cada país.", "Sí / No", "No", DC, CA, "Evento de rectificación.",
   "Derivar del tipo de evento originante.", "Coherente con MDJ-D03-050.", "P1", "B", "E7", "R1", "F06",
   obs="La fecha de efecto de una fe de erratas depende del país.", cs="Pendiente validación nacional", pending="DEC-34")
mk("MDJ-D03-054", "completitud_historica", "Completitud histórica de la obra", "NOR; ADM", "Obra", "Enum", "1 obligatorio",
   "Grado en que Juztina dispone de la historia textual de la obra: completa, parcial, solo texto vigente consolidado, solo texto original o desconocida.",
   "Condiciona la fiabilidad de las líneas de vida y de las consultas históricas.", "CAT-206 Completitud histórica", "solo_consolidado_vigente",
   DC, CA, "Versiones y manifestaciones disponibles.", "Calcular desde las versiones observadas y eventos registrados.",
   "Valor del catálogo.", "P0", "B", "E7", "R2", "F06; F16", pending="DEC-32")
mk("MDJ-D03-055", "fecha_captura_fuente", "Fecha de captura en la fuente", "UNI", "Manifestación", "Datetime", "1 obligatorio",
   "Momento en que Juztina obtuvo el archivo de su fuente.", "Separa el tiempo de registro del tiempo jurídico; necesaria para saber qué consolidado se capturó.",
   NA_VAL, "2026-10-02T08:10:00Z", GS, SI, "No aplica: generado por el sistema.", "Registrar al ingerir el archivo; si se desconoce, usar la fecha de ingreso y marcar estado 'indeterminado'.",
   "Datetime UTC válido.", "P0", "A", "E0", "R3", "F16",
   obs="Coordinar con los datos de incorporación de D1 para no duplicar: este campo es la captura en la fuente, no la carga al repositorio.")
mk("MDJ-D03-056", "fecha_ultima_verificacion_fuente", "Última verificación contra la fuente", "UNI", "Manifestación", "Datetime", "0..1 opcional",
   "Momento en que se comprobó por última vez que la fuente no cambió el documento.",
   "Los consolidados oficiales y editoriales se actualizan; permite detectar textos desactualizados.",
   NA_VAL, "2027-01-15T09:00:00Z", GS, SI + " + " + EE, "Registro de la consulta a la fuente.", "Registrar en cada verificación periódica.", "Datetime ≥ fecha de captura.", "P2", "D", "Sistema", "R3", "F05; F16")
mk("MDJ-D03-057", "linea_vida_unidad", "Línea de vida de la unidad", "NOR; ADM", UE, "Array", "1..n",
   "Secuencia de tramos de la unidad: intervalo, rótulo, ruta, fragmento vigente, estado y evento que abrió cada tramo.",
   "Representa la historia de una disposición con trazabilidad entre versiones.",
   NA_VAL, "[{'desde':'2011-08-20','rotulo':'Art. 22','fragmento':'FT-1','evento':'EV-10'}, …]", DC, CA,
   "Referencias a eventos, operaciones y fragmentos.", "Construir desde versiones, operaciones y eventos estructurales.",
   "Tramos contiguos y sin solapamiento; cada tramo con evento originante.", "P0", "B", "E7", "R1", "F05; F06; F12; F15",
   deps="MDJ-D03-038; MDJ-D05-004; MDJ-D05-020; MDJ-D05-025")
mk("MDJ-D03-058", "fecha_plazo_reglamentacion_texto", "Plazo de reglamentación declarado", "NOR", UE, "String", "0..1 opcional",
   "Texto literal que fija el plazo para dictar el reglamento de la unidad u obra.",
   "Permite alertas de normas pendientes de reglamentar y detectar lagunas.",
   NA_VAL, "en un plazo de sesenta días hábiles", EX, ED, ANCLA,
   "Extraer de fórmulas 'El Poder Ejecutivo reglamentará… en el plazo de…'.", "Coincidencia literal.", "P0", "A", "E3", "R2", "F05; F13")
mk("MDJ-D03-059", "requiere_reglamentacion", "Requiere reglamentación declarada", "NOR", UE, "Boolean", "1 obligatorio",
   "Indica si la unidad u obra declara expresamente que será reglamentada o que su aplicación depende de un reglamento.",
   "Base para detectar normas pendientes de reglamentar y vigencias diferidas.", "Sí / No", "Sí", EX, CL, ANCLA,
   "Marcar 'Sí' con remisión expresa a reglamentación.", "Si 'Sí', debe existir evidencia.", "P1", "A", "E3", "R2", "F05; F13")
mk("MDJ-D03-060", "fecha_limite_reglamentacion_calculada", "Fecha límite de reglamentación calculada", "NOR", UE, "Fecha", "0..1 opcional",
   "Fecha en que vence el plazo de reglamentación, calculada desde el plazo declarado.",
   "Alerta de incumplimiento del deber de reglamentar.", NA_VAL, "2012-02-15", CJ, CA, "Regla de cómputo aplicada.",
   "Calcular con reglas de cómputo de plazos del país.", FECHA_VAL, "P2", "B", "E7", "R2", "F05", deps="MDJ-D03-058; MDJ-D03-011",
   cs="Pendiente validación nacional", pending="DEC-17")
mk("MDJ-D03-061", "unidad_fecha_nacimiento", "Fecha de nacimiento de la unidad", "NOR; ADM", UE, "Fecha", "1 obligatorio",
   "Fecha jurídica desde la que existe la unidad (publicación original o incorporación).", "Delimita la línea de vida.",
   NA_VAL, "2021-05-10", DC, CA, "Evento de nacimiento.", "Tomar la fecha de efecto del evento estructural de nacimiento.", FECHA_VAL, "P0", "B", "E7", "R1", "F06", deps="MDJ-D05-020")
mk("MDJ-D03-062", "unidad_fecha_extincion", "Fecha de extinción de la unidad", "NOR; ADM", UE, "Fecha", "0..1 opcional",
   "Fecha desde la que la unidad deja de existir por derogación, división, fusión o sustitución sin continuidad.",
   "Cierra la línea de vida; distinta de la suspensión.", NA_VAL, "2024-06-01", CJ, CA, "Eventos fundantes.",
   "Calcular desde eventos de derogación o estructurales con destino determinado.", FECHA_VAL + " Debe ser > nacimiento.", "P0", "B", "E7", "R1", "F05; F06",
   review="Condicionado", deps="MDJ-D03-061; MDJ-D03-038", pending="DEC-17")

# =====================================================================
# D05 — CONTENIDO Y ESTRUCTURA
# =====================================================================
mk("MDJ-D05-001", "unidad_id", "Identificador persistente de la unidad estructural", "UNI", UE, "Identificador", "1 obligatorio",
   "Identificador opaco asignado al nacer la unidad, independiente de su rótulo y ubicación.",
   "Preserva la identidad de la disposición ante renumeraciones y reubicaciones.", "No aplica: generado por el sistema", "UE-000781",
   GS, SI, "No aplica: generado por el sistema.", "Asignar al identificar una unidad nueva; reutilizar el existente cuando la continuidad sea declarada, presunta o curada.",
   "Único y nunca reutilizado; no derivado del rótulo.", "P0", "A", "E2", "R2", "F06; F11; F12; F15", deps="MDJ-D05-023; MDJ-D05-024")
mk("MDJ-D05-002", "unidad_obra", "Obra a la que pertenece la unidad", "UNI", UE, "Referencia", "1 obligatorio",
   "Obra que contiene la unidad estructural.", "Ancla la unidad a su obra para herencia de metadatos.", "Referencia a Obra", "OB-0004521",
   GS, SI, "No aplica: generado por el sistema.", "Asignar al segmentar.", "Debe existir.", "P0", "A", "E2", "R3", "F03; F11")
mk("MDJ-D05-003", "unidad_clase", "Clase de unidad estructural", "UNI", UE, "Enum", "1 obligatorio",
   "División rotulada (identificada por su rótulo) o sección funcional (identificada por su función en el razonamiento).",
   "Determina cómo se identifica y se sigue la unidad.", "CAT-207 Clase de unidad estructural", "division_rotulada", NR, CL,
   "Rótulo o marcador de sección en el texto.", "Asignar 'division_rotulada' si el texto la numera o nombra; 'seccion_funcional' si se identifica por su función.",
   "Valor del catálogo.", "P0", "A", "E2", "R2", "F03; F16")
mk("MDJ-D05-004", "rotulo", "Rótulo de la unidad", "UNI", FT, "String", "0..1 obligatorio condicionado",
   "Designación textual de la unidad en la versión ('Artículo 22', 'Art. 5 Bis', 'fracción IV', 'Considerando 14').",
   "Atributo por versión necesario para mostrar y resolver citas; cambia sin cambiar la identidad.",
   NA_VAL, "Artículo 22-A", EX, ED, ANCLA, "Copiar el rótulo tal como aparece en el texto.",
   "Coincidencia literal; obligatorio en divisiones rotuladas.", "P0", "A", "E2", "R2", "F03; F11; F15")
mk("MDJ-D05-005", "rotulo_normalizado", "Rótulo normalizado", "UNI", FT, "String", "0..1 obligatorio condicionado",
   "Forma canónica del rótulo para comparar y resolver referencias (tipo de nivel, número, sufijo).",
   "Resuelve variantes ('Art. 22-A', 'artículo 22 A', 'art. 22a') y sufijos bis, ter, quáter.",
   NA_VAL, "articulo_22_a", NR, NO, "Regla de normalización aplicada.", "Aplicar reglas de normalización por país (sufijos, ordinales, números romanos).",
   "Patrón <nivel>_<número>[_<sufijo>]; único entre hermanos de la misma versión.", "P0", "A", "E2", "R2", "F03; F11", deps="MDJ-D05-004", cs="Catálogo por país")
mk("MDJ-D05-006", "epigrafe", "Epígrafe o sumilla del rótulo", "UNI", FT, "String", "0..1 opcional",
   "Título breve que acompaña al rótulo ('Artículo 22.- Despido nulo').", "Contexto de búsqueda y lectura; cambia entre versiones.",
   NA_VAL, "Despido nulo", EX, ED, ANCLA, "Extraer el texto inmediatamente posterior al rótulo y anterior al cuerpo, si existe.",
   "Coincidencia literal.", "P0", "A", "E2", "R3", "F03; F15")
mk("MDJ-D05-007", "nivel_estructural", "Nivel estructural", "UNI", FT, "Enum", "1 obligatorio",
   "Tipo de división en la jerarquía interna: libro, título, capítulo, sección, artículo, párrafo, inciso, numeral, literal, fracción, parágrafo, considerando, anexo, entre otros.",
   "Permite aplicar criterios de granularidad por nivel.", "CAT-208 Nivel estructural", "literal", NR, CL, ANCLA,
   "Asignar según el marcador del rótulo y la convención del país.", "Valor del catálogo.", "P0", "A", "E2", "R2", "F03; F16", cs="Catálogo por país")
mk("MDJ-D05-008", "ruta_jerarquica", "Ruta jerárquica", "UNI", FT, "Array de referencias", "1 obligatorio",
   "Secuencia de unidades ancestro desde la raíz de la obra hasta la unidad en la versión.",
   "Reconstruye el contexto del fragmento en el documento original.", "Referencias a unidades estructurales", "[Título II, Capítulo I, Art. 22]",
   DC, CA, "Árbol de segmentación.", "Derivar del árbol de unidades de la versión.", "Debe formar una cadena sin ciclos que termina en la unidad.", "P0", "A", "E2", "R2", "F02; F03; F15")
mk("MDJ-D05-009", "unidad_padre", "Unidad padre", "UNI", FT, "Referencia", "0..1 obligatorio condicionado",
   "Unidad inmediatamente superior en la versión.", "Navegación y herencia.", "Referencia a unidad estructural", "UE-000700", DC, CA,
   "Árbol de segmentación.", "Derivar del árbol.", "Vacío solo en la raíz.", "P0", "A", "E2", "R3", "F03")
mk("MDJ-D05-010", "posicion_ordinal", "Posición ordinal", "UNI", FT, "Integer", "1 obligatorio",
   "Orden de la unidad entre sus hermanas en la versión.", "Reconstruye el orden de lectura.", NA_VAL, "7", GS, SI,
   "Posición en el texto.", "Asignar por orden de aparición.", "Entero ≥ 1, único entre hermanas.", "P0", "A", "E2", "R3", "F15")
mk("MDJ-D05-011", "profundidad", "Profundidad en el árbol", "UNI", FT, "Integer", "1 obligatorio",
   "Número de niveles entre la raíz y la unidad.", "Filtros y reglas de granularidad.", NA_VAL, "4", DC, CA, "Ruta jerárquica.",
   "Contar elementos de la ruta.", "Igual a la longitud de MDJ-D05-008.", "P1", "B", "E7", "R3", "F16", deps="MDJ-D05-008")
mk("MDJ-D05-012", "seccion_funcional_tipo", "Tipo de sección funcional", "JUR; ADM; DOC; NOR", UE, "Enum", "0..1 obligatorio condicionado",
   "Función de la sección en el documento: vistos, antecedentes, hechos, problema jurídico, fundamentos de hecho, fundamentos de derecho, parte resolutiva, voto, introducción, conclusiones, bibliografía, considerandos de una norma, entre otras.",
   "Condiciona qué perfiles se aplican y qué evidencia es decisiva para clasificar y relacionar.",
   "CAT-209 Tipo de sección funcional", "fundamentos_de_derecho", IN, CL, ANCLA,
   "Identificar por encabezados explícitos ('VISTOS', 'CONSIDERANDO', 'SE RESUELVE') y, si faltan, por la función del texto.",
   "Obligatorio en secciones funcionales; cada obra JUR o ADM contenciosa debe tener al menos una parte resolutiva o estado 'indeterminado'.",
   "P0", "A", "E2", "R2", "F07; F08; F15", appl="Secciones funcionales de jurisprudencia, actos, doctrina y preámbulos normativos.")
mk("MDJ-D05-013", "seccion_rotulo_original", "Encabezado original de la sección", "JUR; ADM; DOC; NOR", UE, "String", "0..1 opcional",
   "Encabezado literal de la sección ('CONSIDERANDO:', 'FUNDAMENTOS', 'SE RESUELVE:').", "Valida la clasificación funcional y conserva la terminología del país.",
   NA_VAL, "SE RESUELVE:", EX, ED, ANCLA, "Copiar el encabezado si existe.", "Coincidencia literal.", "P0", "A", "E2", "R3", "F16")
mk("MDJ-D05-014", "unidad_anclas", "Anclas de la unidad en la manifestación", "UNI", FT, "Ancla de evidencia", "1..n",
   "Posiciones inicial y final del texto de la unidad en cada manifestación de la versión.",
   "Base de toda evidencia y de la reconstrucción del contexto; rehacerlas exige releer.", NA_VAL, "M-55: 10 412–11 980", GS, SI,
   "No aplica: es el ancla misma.", "Registrar al segmentar sobre el texto normalizado de la manifestación.",
   "Las anclas de hermanas no se solapan; contenidas en el ancla del padre.", "P0", "A", "E2", "R2", "F15; F16", deps="MDJ-D05-015")
mk("MDJ-D05-015", "fragmento_id", "Identificador del fragmento textual", "UNI", FT, "Identificador", "1 obligatorio",
   "Identificador del texto de una unidad en una versión.", "Permite citar el texto exacto de una fecha.", "No aplica: generado por el sistema",
   "FT-000781-03", GS, SI, "No aplica: generado por el sistema.", "Asignar al crear el fragmento.", "Único; uno por par unidad–versión con texto distinto.", "P0", "A", "E2", "R3", "F06; F15")
mk("MDJ-D05-016", "fragmento_texto_normalizado", "Texto normalizado del fragmento", "UNI", FT, "Texto largo", "1 obligatorio",
   "Texto de la unidad en la versión, con normalización técnica (espacios, guiones, saltos) sin alterar el contenido.",
   "Insumo técnico para la extracción posterior por fragmentos (clase C) y la recuperación.", NA_VAL, "Artículo 22.- …", EX, ED + " + " + NO,
   "Anclas de la unidad.", "Obtener del texto normalizado de la manifestación entre las anclas.", "Hash recalculable igual a MDJ-D05-017.",
   "P0", "A", "E2", "R2", "F02; F15", privacy="Puede contener datos personales", obs="Su conservación como insumo depende de DEC-24; se almacena una sola vez.", pending="DEC-24")
mk("MDJ-D05-017", "fragmento_hash", "Huella del contenido del fragmento", "UNI", FT, "Hash", "1 obligatorio",
   "Huella criptográfica del texto normalizado.", "Detecta cambios de contenido entre versiones y duplicados.", NA_VAL, "sha256:9f2c…", GS, SI,
   "No aplica: generado por el sistema.", "Calcular SHA-256 del texto normalizado.", "Reproducible.", "P0", "A", "E2", "R3", "F06; F16", deps="MDJ-D05-016")
mk("MDJ-D05-018", "fragmento_marcado_derogado", "Marca textual de unidad derogada", "NOR", FT, "Boolean", "1 obligatorio",
   "Indica si el texto consolidado muestra la unidad solo como rótulo con una marca de derogación ('(Derogado)').",
   "Hecho textual que alerta sobre una derogación aunque falte el evento; no es conclusión de vigencia.",
   "Sí / No", "Sí", EX, ED, ANCLA, "Detectar rótulos sin cuerpo seguidos de marcas de derogación.", "Si 'Sí', debe existir evidencia.", "P0", "A", "E2", "R2", "F05; F06")
mk("MDJ-D05-019", "tramos_contenido_ajeno", "Tramos de contenido transcrito ajeno", "UNI", FT, "Array", "0..n",
   "Anclas de los tramos del fragmento que transcriben texto de otro documento.",
   "Evita clasificar o extraer efectos del contenido transcrito como si fuera propio.", NA_VAL, "[{'inicio':120,'fin':890,'referencia':'RF-77'}]",
   EX, ED, "Anclas de los tramos y referencia atribuida (D7).", "Delimitar texto entre comillas o en bloque atribuido a otra fuente.",
   "Cada tramo dentro del fragmento y vinculado a una referencia.", "P1", "A", "E4", "R2", "F15; F16",
   obs="La referencia y su verificación se definen en D7.")

# --- Eventos estructurales y continuidad ---
mk("MDJ-D05-020", "evento_estructural_tipo", "Tipo de evento estructural", "NOR; ADM", EV, "Enum", "1 obligatorio",
   "Cambio de estructura que afecta a la unidad: nacimiento por publicación o incorporación, renumeración, reubicación, cambio de epígrafe, división, fusión, sustitución sin continuidad, extinción.",
   "Distingue cambios de estructura de cambios de contenido.", "CAT-210 Evento estructural", "renumeracion", DC, CA,
   "Operación modificatoria de origen o comparación de versiones.", "Derivar de las operaciones transcritas; si proviene de comparación de versiones, marcarlo con continuidad inferida.",
   "Valor del catálogo; coherente con la operación de origen.", "P0", "B", "E7", "R1", "F06; F12", deps="MDJ-D03-027")
mk("MDJ-D05-021", "unidad_rotulo_inicial", "Rótulo de nacimiento", "NOR; ADM", UE, "String", "1 obligatorio",
   "Rótulo que tenía la unidad al nacer.", "Ayuda a reconocer la disposición en citas antiguas.", NA_VAL, "Artículo 22", DC, CA,
   "Primer fragmento de la unidad.", "Tomar el rótulo del primer tramo de la línea de vida.", "Igual al rótulo del primer fragmento.", "P0", "B", "E7", "R3", "F11; F15")
mk("MDJ-D05-022", "unidad_evento_nacimiento", "Evento de nacimiento de la unidad", "NOR; ADM", UE, "Referencia", "1 obligatorio",
   "Publicación original o incorporación que dio origen a la unidad.", "Trazabilidad del origen de cada disposición.",
   "Referencia a evento u operación", "OP-3321", DC, CA, "Evento con evidencia.", "Vincular al evento estructural de nacimiento.", "Debe existir.", "P0", "B", "E7", "R2", "F06")
mk("MDJ-D05-023", "continuidad_tipo", "Tipo de relación estructural con otra unidad", "NOR; ADM", UE, "Enum", "0..n",
   "Relación con otra unidad cuando no hay identidad: se divide en, se fusiona en, es sustituida por, deriva de, corresponde a (otra obra).",
   "Representa división, fusión y sustitución sin forzar identidad.", "CAT-212 Relación estructural entre unidades", "deriva_de", DC, CA,
   "Operaciones y tablas de correspondencia.", "Derivar de operaciones declaradas, reglas de continuidad presunta o curaduría.",
   "Cada valor con unidad relacionada (MDJ-D05-024) y grado (MDJ-D05-025).", "P0", "B", "E7", "R1", "F06; F11; F12",
   obs="La relación general se modela en D7; aquí se registra como dato de la unidad para la línea de vida.", pending="DEC-03")
mk("MDJ-D05-024", "continuidad_unidad_relacionada", "Unidad relacionada estructuralmente", "NOR; ADM", UE, "Array de referencias", "0..n",
   "Unidad o unidades con las que existe la relación estructural.", "Navegación entre predecesoras y sucesoras.",
   "Referencias a unidades estructurales", "[UE-000802]", DC, CA, "Ídem MDJ-D05-023.", "Registrar junto con el tipo.", "Deben existir.", "P0", "B", "E7", "R1", "F06; F12", deps="MDJ-D05-023")
mk("MDJ-D05-025", "continuidad_grado", "Grado de continuidad", "NOR; ADM", UE, "Enum", "1 obligatorio",
   "Certeza de la identidad o relación estructural: declarada, presunta, inferida, curada o no determinada.",
   "Solo declarada, presunta y curada alimentan vigencia y consolidados.", "CAT-211 Grado de continuidad", "presunta", DC, CA,
   "Regla aplicada o curaduría.", "Declarada si la norma o tabla lo dice; presunta si aplica la regla de mismo rótulo validada por país; inferida por similitud; curada tras revisión.",
   "Inferida nunca alimenta cálculos sin revisión.", "P0", "B", "E7", "R1", "F06; F16", review="Condicionado",
   cs="Pendiente validación nacional", pending="DEC-03")
mk("MDJ-D05-026", "candidatas_continuidad_inferida", "Candidatas de continuidad inferida", "NOR", UE, "Array de referencias", "0..n",
   "Unidades nacidas o extinguidas en la misma operación con contenido similar, propuestas como posible división o fusión.",
   "Apoya la curaduría sin afirmar continuidad.", "Referencias a unidades estructurales", "[UE-000803]", IN, IF,
   "Ambos fragmentos comparados y métrica de similitud.", "Comparar fragmentos sobre unidades extinguidas y nacidas por la misma norma.",
   "Toda candidata requiere revisión.", "P2", "C", "Posterior (C)", "R1", "F06; F16", review="Sí")
mk("MDJ-D05-027", "correspondencia_otra_obra", "Correspondencia con unidad de otra obra", "NOR", UE, "Array de referencias", "0..n",
   "Unidades de otra obra (compilación, texto ordenado o refundido) que corresponden a esta unidad.",
   "Vincula textos ordenados con las obras compiladas sin confundir identidades.", "Referencias a unidades estructurales", "[UE-090011]",
   DC, CA, "Tabla de correspondencias o curaduría.", "Derivar de MDJ-D03-037 o de curaduría.", "Deben pertenecer a obras distintas.", "P1", "B", "E7", "R1", "F06; F11",
   deps="MDJ-D03-037", cs="Condicionado", pending="DEC-04")

# --- Segmentos y contexto ---
mk("MDJ-D05-028", "segmentos", "Segmentos del fragmento", "UNI", FT, "Array", "1..n",
   "Lista de segmentos técnicos (párrafo, oración, ítem, celda, nota, bloque de procesamiento) con su tipo, orden y ancla.",
   "Contenedores de evidencia y unidades de lectura del modelo; no reciben metadatos jurídicos propios.",
   "Tipos de CAT-216 Tipo de segmento", "[{'tipo':'parrafo','orden':1,'ancla':'10412-10870'}]", GS, SI, "Anclas.",
   "Dividir el fragmento según el tipo de segmento.", "Segmentos contiguos que cubren el fragmento.", "P0", "A", "E2", "R3", "F15; F16", deps="MDJ-D05-014")
mk("MDJ-D05-029", "contexto_epigrafes_ancestros", "Contexto de epígrafes ancestros", "UNI", FT, "Array", "0..n",
   "Rótulos y epígrafes de los ancestros, en orden, para mostrar el contexto del fragmento.",
   "Recupera el contexto al presentar un inciso o literal aislado.", NA_VAL, "['Título II – Del contrato', 'Capítulo I – Extinción']",
   DC, CA, "Ruta jerárquica.", "Componer desde la ruta y los epígrafes.", "Coherente con MDJ-D05-008.", "P1", "B", "E7", "R3", "F02; F15", deps="MDJ-D05-008; MDJ-D05-006")
mk("MDJ-D05-030", "alineacion_fragmentos_asistente", "Fragmentos del asistente alineados", "UNI", FT, "Array de referencias", "0..n",
   "Identificadores de los fragmentos (chunks) que hoy usa el asistente y que se superponen con la unidad.",
   "Permite usar los nuevos metadatos en la recuperación actual sin rehacerla.", "No aplica: identificadores del sistema actual", "[chunk-88123]",
   DC, CA, "Superposición de anclas.", "Calcular por superposición de posiciones de texto.", "Superposición > 0.", "P1", "B", "E7", "R3", "F01; F02",
   cs="Común", pending="DEC-09")
mk("MDJ-D05-031", "nivel_clasificacion_aplicable", "Unidad clasificable", "UNI", UE, "Boolean", "1 obligatorio",
   "Indica si la unidad está en el nivel en que se aplica la clasificación temática según los criterios de granularidad.",
   "Controla costo y sobreclasificación.", "Sí / No", "Sí", DC, CA, "Regla de granularidad aplicada.",
   "Sí por defecto en artículo, problema jurídico, infracción y sección de primer nivel de doctrina; desciende si los ítems tienen materias heterogéneas.",
   "Coherente con la regla de granularidad por categoría.", "P0", "B", "E7", "R2", "F01; F16", deps="MDJ-D05-007; MDJ-D05-012")
mk("MDJ-D05-032", "efecto_juridico_autonomo", "Unidad con efecto jurídico autónomo", "NOR; ADM", UE, "Boolean", "1 obligatorio",
   "Indica si la unidad enuncia un efecto jurídico propio (obligación, sanción, derecho) que justifica extraer efectos a su nivel.",
   "Define el nivel de extracción de D8 y D9 (p. ej., numerales de un catálogo de infracciones).", "Sí / No", "Sí", IN, CL, ANCLA,
   "Marcar 'Sí' cuando la unidad contiene una consecuencia jurídica completa sin depender del texto de sus hermanas.",
   "Si 'Sí' en una unidad inferior al artículo, debe existir evidencia de la consecuencia.", "P1", "A", "E3", "R2", "F13; F14")

# --- Disposiciones, anexos, tablas ---
mk("MDJ-D05-033", "disposicion_accesoria_tipo", "Tipo de disposición complementaria, transitoria o final", "NOR", UE, "Enum", "0..1 obligatorio condicionado",
   "Clase de disposición accesoria según su rótulo: complementaria final, transitoria, modificatoria, derogatoria, adicional u otra.",
   "Concentran efectos temporales y operaciones sobre otras normas.", "CAT-213 Tipo de disposición accesoria", "complementaria_derogatoria",
   NR, CL, ANCLA, "Normalizar desde el rótulo de la disposición.", "Valor del catálogo; obligatorio cuando el nivel es 'disposición'.",
   "P0", "A", "E2", "R2", "F05; F06", cs="Catálogo por país", pending="DEC-08")
mk("MDJ-D05-034", "anexo_tipo_contenido", "Tipo de contenido del anexo", "NOR; ADM; JUR", UE, "Enum múltiple", "0..n",
   "Naturaleza del contenido de un anexo o bloque no textual: tabla, cuadro, formulario, plano, mapa, gráfico, imagen, fórmula, lista.",
   "Muchas normas regulatorias viven en sus anexos; permite saber qué existe aunque no se extraiga.", "CAT-214 Tipo de contenido no textual", "tabla",
   IN, CL, "Ancla al anexo.", "Detectar el tipo predominante del anexo.", "Valor del catálogo.", "P0", "A", "E2", "R3", "F03; F13; F16")
mk("MDJ-D05-035", "anexo_texto_disponible", "Anexo con texto disponible", "NOR; ADM; JUR", UE, "Boolean", "1 obligatorio",
   "Indica si el contenido del anexo está en la manifestación como texto aprovechable o solo como imagen o referencia externa.",
   "Evita afirmar ausencia de contenido cuando el anexo no se pudo leer.", "Sí / No", "No", DC, CA, "Calidad de texto del tramo.",
   "Derivar de la calidad del texto del anexo.", "Si 'No', los campos de contenido del anexo deben quedar 'indeterminado'.", "P0", "A", "E0", "R3", "F16")
mk("MDJ-D05-036", "anexo_publicado_por_separado", "Anexo publicado en otro medio", "NOR; ADM", UE, "Boolean", "1 obligatorio",
   "Indica si el texto remite a un anexo publicado en otro lugar (portal institucional, separata).",
   "Señala contenido normativo ausente del corpus.", "Sí / No", "Sí", EX, ED, ANCLA,
   "Detectar fórmulas como 'el anexo se publica en el portal…'.", "Si 'Sí', registrar la referencia en D7.", "P1", "A", "E3", "R2", "F05; F16")
mk("MDJ-D05-037", "contiene_tabla", "Fragmento con tabla o cuadro", "UNI", FT, "Boolean", "1 obligatorio",
   "Indica si el fragmento contiene una tabla o cuadro.", "Las tablas concentran escalas de sanciones, tasas y plazos.", "Sí / No", "Sí", DC, CA,
   "Estructura detectada.", "Detectar estructura tabular en el texto o en el formato de origen.", "Coherente con el formato de origen.", "P0", "A", "E2", "R3", "F13; F14; F16")
mk("MDJ-D05-038", "tabla_estructurada", "Tabla estructurada", "UNI", FT, "Objeto", "0..n",
   "Representación en filas y columnas de una tabla del fragmento, con encabezados y anclas por celda.",
   "Permite extraer valores (montos, plazos, tasas) sin releer el documento.", NA_VAL, "{'encabezados':['Infracción','Multa (UIT)'],'filas':[…]}",
   EX, ED, "Anclas por celda.", "Reconstruir la tabla preservando encabezados; no inventar celdas vacías.",
   "Número de celdas por fila coherente con los encabezados.", "P2", "C", "Posterior (C)", "R2", "F13; F14", deps="MDJ-D05-037")

# --- Contenido de normativa ---
mk("MDJ-D05-039", "objeto_declarado_unidad", "Unidad que declara el objeto o finalidad", "NOR; ADM", "Obra", "Referencia", "0..1 opcional",
   "Unidad estructural donde la obra declara su objeto, finalidad o ámbito ('Artículo 1.- Objeto').",
   "Base para la clasificación agregada de la obra y para resúmenes fieles.", "Referencia a unidad estructural", "UE-000701", IN, CL,
   ANCLA, "Identificar la unidad con epígrafe u oración de objeto o finalidad.", "Debe pertenecer a la obra.", "P1", "A", "E3", "R2", "F01; F04")
mk("MDJ-D05-040", "objeto_finalidad_resumen", "Resumen del objeto o finalidad", "NOR; ADM; JUR", "Obra", "Texto largo", "0..1 opcional",
   "Enunciado breve del objeto de la obra redactado por el modelo a partir de la unidad de objeto o de la parte resolutiva.",
   "Ayuda a búsqueda y lectura; claramente marcado como inferido.", NA_VAL, "Regula el régimen de seguridad y salud en el trabajo…", IN, IF,
   "Ancla a la unidad de objeto o a la parte resolutiva.", "Redactar sin añadir información ausente del texto.", "Cada afirmación del resumen debe estar sustentada en la evidencia.",
   "P2", "C", "Posterior (C)", "R3", "F01; F02; F03", deps="MDJ-D05-039")
mk("MDJ-D05-041", "considerandos_preambulo_presentes", "Preámbulo o considerandos de la norma", "NOR; ADM", "Obra", "Boolean", "1 obligatorio",
   "Indica si la obra contiene considerandos, exposición de motivos incorporada o preámbulo.",
   "Fuente de interpretación finalista; delimita secciones no dispositivas.", "Sí / No", "Sí", EX, ED, ANCLA,
   "Detectar secciones 'CONSIDERANDO', 'VISTO', exposición de motivos dentro del texto.", "Si 'Sí', debe existir una sección funcional correspondiente.", "P0", "A", "E2", "R3", "F04")
mk("MDJ-D05-042", "numero_articulos", "Número de artículos de la versión", "NOR; ADM", "Versión", "Integer", "1 obligatorio",
   "Cantidad de unidades de nivel artículo en la versión, incluidas las disposiciones accesorias.",
   "Control de completitud de la segmentación y dato de presentación.", NA_VAL, "103", DC, CA, "Unidades de la versión.",
   "Contar unidades de nivel artículo y disposición.", "Coherente con la numeración continua (control de calidad D11).", "P1", "B", "E7", "R3", "F16")
mk("MDJ-D05-043", "indice_estructural", "Índice estructural de la versión", "UNI", "Versión", "Array", "1 obligatorio",
   "Árbol de unidades de la versión con rótulos y epígrafes, sin texto.", "Navegación del documento y control de calidad.", NA_VAL,
   "[{'Título I':[{'Art. 1':'Objeto'}, …]}]", DC, CA, "Unidades de la versión.", "Componer desde las unidades.", "Coherente con las rutas.", "P1", "B", "E7", "R3", "F02; F03", deps="MDJ-D05-008")

# --- Contenido de jurisprudencia y actos ---
mk("MDJ-D05-044", "sumilla_oficial", "Sumilla oficial", "JUR; ADM", "Obra", "Texto largo", "0..1 opcional",
   "Resumen o sumilla que la propia resolución o su publicación oficial incluye.", "Es un resumen oficial, distinto del generado.",
   NA_VAL, "Se declara fundada la demanda de amparo por…", EX, ED, ANCLA, "Extraer si consta en el encabezado o en la publicación oficial.",
   "Coincidencia literal.", "P1", "A", "E3", "R2", "F03; F07", obs="Las tesis y criterios extractados con identidad propia son obras (D4), no sumillas.")
mk("MDJ-D05-045", "parte_resolutiva_unidad", "Unidad de la parte resolutiva", "JUR; ADM", "Obra", "Referencia", "0..1 obligatorio condicionado",
   "Sección funcional que contiene la decisión.", "Hecho primario delimitado: de ella salen sentido del fallo, montos y relaciones de control.",
   "Referencia a unidad estructural", "UE-55021", IN, CL, ANCLA, "Identificar por encabezado ('SE RESUELVE', 'FALLA', 'RESUELVE') o por fórmulas decisorias.",
   "Obligatoria en resoluciones; si no se encuentra, estado 'indeterminado' y marca de completitud.", "P0", "A", "E2", "R1", "F07; F08; F14", deps="MDJ-D05-012")
mk("MDJ-D05-046", "punto_resolutivo_numero", "Número del punto resolutivo", "JUR; ADM", UE, "String", "0..1 opcional",
   "Rótulo u ordinal del punto dentro de la parte resolutiva ('PRIMERO', '2.').", "Permite citar y vincular cada decisión.", NA_VAL, "SEGUNDO",
   EX, ED, ANCLA, "Copiar el ordinal tal como aparece.", "Único dentro de la parte resolutiva.", "P0", "A", "E2", "R2", "F07; F15")
mk("MDJ-D05-047", "punto_resolutivo_problema", "Problema jurídico al que responde el punto resolutivo", "JUR; ADM", UE, "Referencia", "0..1 opcional",
   "Unidad de problema jurídico que el punto resolutivo resuelve.", "Une decisión y razonamiento para precedentes y análisis.",
   "Referencia a unidad estructural", "UE-55011", IN, IF, "Anclas en ambos tramos.", "Vincular por correspondencia de contenido.",
   "Ambas unidades en la misma obra.", "P2", "C", "Posterior (C)", "R2", "F07; F08", review="Condicionado", deps="MDJ-D05-048")
mk("MDJ-D05-048", "problema_juridico_enunciado", "Enunciado del problema jurídico", "JUR; ADM", UE, "Texto largo", "0..1 obligatorio condicionado",
   "Pregunta jurídica que la sección resuelve, formulada a partir del texto.", "Unidad de clasificación y de precedente en jurisprudencia.",
   NA_VAL, "¿Procede la reposición de una trabajadora despedida por su embarazo?", IN, IF, "Ancla al tramo donde se plantea o resuelve.",
   "Usar la formulación expresa si existe; si no, formularla de modo neutro sin anticipar la respuesta.",
   "Debe estar respaldada por evidencia en fundamentos o resolución.", "P2", "C", "Posterior (C)", "R2", "F07; F08; F15", review="Condicionado")
mk("MDJ-D05-049", "problema_juridico_orden", "Orden del problema jurídico", "JUR; ADM", UE, "Integer", "0..1 obligatorio condicionado",
   "Posición del problema jurídico dentro de la resolución.", "Ordena y vincula problemas, fundamentos y puntos resolutivos.", NA_VAL, "2", GS, SI,
   "Posición en el texto.", "Asignar por orden de tratamiento.", "Entero ≥ 1.", "P1", "A", "E2", "R3", "F07")
mk("MDJ-D05-050", "problema_juridico_formulacion_expresa", "Problema jurídico formulado expresamente", "JUR; ADM", UE, "Boolean", "1 obligatorio",
   "Indica si la resolución enuncia el problema jurídico (p. ej., 'corresponde determinar si…') o si se infiere.",
   "Distingue el dato explícito de la formulación del modelo.", "Sí / No", "Sí", EX, ED + " + " + CL, ANCLA,
   "Marcar 'Sí' con fórmulas de delimitación expresa.", "Si 'Sí', debe existir evidencia literal.", "P1", "A", "E2", "R2", "F07; F16")
mk("MDJ-D05-051", "fundamentos_vinculados_problema", "Fundamentos vinculados al problema", "JUR; ADM", UE, "Array de referencias", "0..n",
   "Unidades de fundamentos que razonan sobre el problema jurídico.", "Delimita la evidencia decisiva para clasificación y ratio.",
   "Referencias a unidades estructurales", "[UE-55012, UE-55013]", IN, IF, "Anclas.", "Vincular cada fundamento al problema que trata.",
   "Misma obra; sin fundamentos huérfanos cuando hay problemas identificados.", "P2", "C", "Posterior (C)", "R2", "F07; F08")
mk("MDJ-D05-052", "ratio_decidendi_enunciado", "Enunciado de la razón decisoria", "JUR; ADM", UE, "Texto largo", "0..1 opcional",
   "Regla o criterio que sustenta la decisión del problema jurídico, formulada a partir de los fundamentos.",
   "Base del análisis de precedentes; siempre inferida y revisable.", NA_VAL, "El despido de una trabajadora gestante sin causa probada se presume discriminatorio…",
   IN, IF, "Anclas a los fundamentos decisivos.", "Formular la regla general aplicada, citando los fundamentos que la sustentan.",
   "Cada elemento de la regla debe tener evidencia; no confundir con obiter.", "P2", "C", "Posterior (C)", "R1", "F07; F08; F04", review="Sí",
   obs="Su fuerza como precedente se determina en D17 con reglas de país.")
mk("MDJ-D05-053", "fundamento_es_obiter", "Fundamento marcado como obiter dictum", "JUR", UE, "Boolean", "0..1 opcional",
   "Indica si la unidad de fundamentos contiene razonamiento no necesario para la decisión.", "Evita atribuir fuerza a consideraciones incidentales.",
   "Sí / No", "No", IN, CL, "Ancla al fundamento.", "Marcar 'Sí' cuando el razonamiento no sostiene ningún punto resolutivo.", "Coherente con MDJ-D05-047.",
   "P2", "C", "Posterior (C)", "R1", "F07; F08", review="Sí")
mk("MDJ-D05-054", "hechos_relevantes_resumen", "Resumen de hechos relevantes", "JUR; ADM", "Obra", "Texto largo", "0..1 opcional",
   "Síntesis de los hechos determinantes para la decisión, según la sección de hechos o antecedentes.", "Búsqueda por supuestos fácticos y análisis de casos.",
   NA_VAL, "La demandante fue cesada al tercer mes de embarazo…", IN, IF, "Ancla a hechos o antecedentes.", "Resumir sin datos personales identificables.",
   "Sin nombres de personas naturales; cada hecho con evidencia.", "P2", "C", "Posterior (C)", "R2", "F07; F04", privacy="Puede contener datos personales", pending="DEC-18")
mk("MDJ-D05-055", "voto_tipo", "Tipo de voto", "JUR; ADM", UE, "Enum", "0..1 obligatorio condicionado",
   "Clase de voto separado: singular, discordante o salvamento, concurrente, aclaración o fundamento de voto.",
   "Los votos no forman parte de la decisión mayoritaria ni de la ratio.", "CAT-215 Tipo de voto", "salvamento_de_voto", EX, ED + " + " + CL, ANCLA,
   "Identificar por encabezado del voto y normalizar.", "Obligatorio en secciones funcionales de tipo voto.", "P0", "A", "E2", "R2", "F07; F08",
   cs="Catálogo por país", pending="DEC-25")
mk("MDJ-D05-056", "voto_autor", "Autor del voto", "JUR; ADM", UE, "Referencia", "0..1 opcional",
   "Magistrado o integrante que emite el voto separado.", "Análisis de posiciones dentro de órganos colegiados.", "Referencia a Entidad: persona",
   "PER-0091", EX, ED + " + " + NO, ANCLA, "Extraer el nombre del encabezado o firma del voto y resolverlo contra el registro de personas.",
   "Debe integrar la composición del órgano (D13).", "P1", "A", "E3", "R2", "F07", privacy="Dato de funcionario público",
   obs="Uso en estadísticas individuales sujeto a DEC-19.", pending="DEC-19")

# --- Doctrina ---
mk("MDJ-D05-057", "resumen_autor", "Resumen del autor", "DOC", "Obra", "Texto largo", "0..1 opcional",
   "Resumen o abstract publicado con la obra doctrinal.", "Descripción autorizada del contenido.", NA_VAL, "El artículo analiza…", EX, ED, ANCLA,
   "Extraer el bloque 'Resumen' o 'Abstract' en el idioma original.", "Coincidencia literal.", "P1", "A", "E3", "R3", "F03; F04",
   privacy="Restricción de acceso o derechos", obs="Su reproducción está sujeta a DEC-27.", pending="DEC-27")
mk("MDJ-D05-058", "palabras_clave_autor", "Palabras clave del autor", "DOC", "Obra", "Array", "0..n",
   "Palabras clave declaradas por el autor o la revista.", "Señal para clasificación y búsqueda; no reemplaza la taxonomía.", NA_VAL,
   "['despido', 'maternidad']", EX, ED, ANCLA, "Extraer la lista 'Palabras clave' o 'Keywords'.", "Coincidencia literal de cada término.", "P1", "A", "E3", "R3", "F03")
mk("MDJ-D05-059", "nota_al_pie_llamada", "Llamada de la nota al pie", "DOC; JUR", UE, "Ancla de evidencia", "0..1 obligatorio condicionado",
   "Posición en el cuerpo del texto de la llamada que remite a la nota.", "Vincula la nota con el pasaje que apoya; evita clasificar por notas.",
   NA_VAL, "M-91: 5 220", EX, ED, "Ancla de la llamada.", "Detectar el número de llamada y su nota correspondiente.", "Cada nota con su llamada única.", "P1", "A", "E2", "R3", "F15")
mk("MDJ-D05-060", "resumen_generado", "Resumen generado", "UNI", "Obra", "Texto largo", "0..1 opcional",
   "Resumen de la obra producido por el modelo, marcado como inferido.", "Lectura rápida en el asistente y la búsqueda.", NA_VAL, "La resolución sanciona…",
   IN, IF, "Anclas a las unidades resumidas.", "Generar a partir de unidades ya segmentadas, sin añadir información.", "Cada oración trazable a evidencia.",
   "P3", "C", "Posterior (C)", "R3", "F02; F03", privacy="Puede contener datos personales", pending="DEC-18; DEC-27")


# =====================================================================
# CATÁLOGOS (CAT-201..CAT-222)
# =====================================================================
def V(code, label, definition, **kw):
    d = dict(code=code, label=label, definition=definition); d.update(kw); return d

SEMILLA = "Semilla — pendiente de validación nacional"
CATALOGS = [
 dict(cat_id="CAT-201", cat_name="Tipo de evento temporal", cat_def="Hitos documentales y jurídicos que se registran como eventos fechados.", values=[
   V("emision", "Emisión o expedición", "Dictado o firma del acto."),
   V("aprobacion", "Aprobación por órgano deliberante", "Aprobación del texto por el órgano colegiado."),
   V("promulgacion", "Promulgación o sanción ejecutiva", "Acto que ordena publicar y cumplir la norma.", status=SEMILLA),
   V("publicacion", "Publicación", "Difusión en el medio oficial o editorial."),
   V("notificacion", "Notificación", "Comunicación formal a los interesados."),
   V("entrada_en_vigor", "Entrada en vigor", "Inicio de la obligatoriedad."),
   V("firmeza", "Firmeza o ejecutoria", "La decisión deja de ser impugnable."),
   V("modificacion", "Modificación", "Cambio de texto de una unidad."),
   V("sustitucion_textual", "Sustitución textual", "Reemplazo íntegro del texto de una unidad conservando su identidad."),
   V("incorporacion", "Incorporación", "Nacimiento de una unidad nueva."),
   V("derogacion_expresa", "Derogación expresa", "Supresión declarada de una unidad u obra determinada."),
   V("derogacion_generica", "Derogación genérica", "Cláusula que deroga lo que se oponga, sin destino determinado; no altera estados."),
   V("suspension", "Suspensión", "Privación temporal de efectos."),
   V("levantamiento_suspension", "Levantamiento de suspensión", "Fin de una suspensión."),
   V("declaracion_inconstitucionalidad", "Declaración de inconstitucionalidad o inexequibilidad", "Decisión de control que expulsa o inaplica con efectos generales.", status=SEMILLA),
   V("exequibilidad_condicionada", "Exequibilidad condicionada o sentencia interpretativa", "Decisión de control que impone una lectura obligatoria.", status=SEMILLA),
   V("nulidad_ilegalidad", "Nulidad o ilegalidad declarada", "Decisión judicial que invalida un acto o reglamento."),
   V("prorroga", "Prórroga", "Extensión del plazo de vigencia."),
   V("vencimiento_plazo", "Vencimiento de plazo de vigencia", "Fin de una norma temporal por cumplimiento de su término."),
   V("rectificacion", "Rectificación o fe de erratas", "Corrección de errores materiales del texto publicado.", status=SEMILLA),
   V("restablecimiento", "Restablecimiento o reviviscencia", "Recuperación de vigencia de un texto derogado; su procedencia depende del país.", status=SEMILLA),
   V("plazo_reglamentacion", "Plazo de reglamentación", "Término fijado para dictar el reglamento."),
 ]),
 dict(cat_id="CAT-202", cat_name="Verbo de operación modificatoria", cat_def="Operaciones jurídicas que una disposición realiza sobre otra.", values=[
   V("modifica", "Modifica", "Cambia parte o todo el texto conservando la unidad.", synonyms="modifícase; refórmase; queda redactado"),
   V("sustituye", "Sustituye", "Reemplaza el texto de una unidad o bloque.", synonyms="sustitúyese; reemplázase"),
   V("incorpora", "Incorpora o adiciona", "Crea una unidad nueva.", synonyms="incorpórase; adiciónase; agrégase"),
   V("deroga", "Deroga", "Suprime una unidad u obra.", synonyms="derógase; déjase sin efecto"),
   V("renumera", "Renumera", "Cambia el rótulo conservando la unidad."),
   V("reubica", "Reubica", "Cambia la ubicación conservando la unidad."),
   V("suspende", "Suspende", "Priva temporalmente de efectos."),
   V("prorroga", "Prorroga", "Extiende un plazo de vigencia."),
   V("restablece", "Restablece", "Devuelve vigencia a un texto; requiere regla nacional.", status=SEMILLA),
   V("rectifica", "Rectifica", "Corrige errores materiales."),
   V("ordena_refunde", "Ordena o refunde", "Compila y reordena el texto de otra obra en una obra propia.", status=SEMILLA),
 ]),
 dict(cat_id="CAT-203", cat_name="Estado de vigencia", cat_def="Estados calculados de unidades y obras a una fecha de corte.", values=[
   V("aun_no_vigente", "Aún no vigente", "Publicada pero con entrada en vigor futura."),
   V("vigente", "Vigente", "Rige sin modificaciones registradas; sin fuente oficial se presenta como 'sin derogación registrada'."),
   V("vigente_con_modificaciones", "Vigente con modificaciones", "Rige con texto modificado."),
   V("parcialmente_derogada", "Parcialmente derogada", "Algunas subunidades derogadas."),
   V("derogada", "Derogada", "Suprimida por derogación con destino determinado."),
   V("suspendida", "Suspendida", "Efectos suspendidos temporalmente."),
   V("expulsada_inexequible", "Expulsada o inexequible", "Declarada inconstitucional o ilegal con efectos generales.", status=SEMILLA),
   V("exequible_condicionada", "Exequible condicionada", "Rige con lectura obligatoria impuesta.", status=SEMILLA),
   V("indeterminada", "Indeterminada", "Faltan reglas validadas o eventos para concluir."),
 ]),
 dict(cat_id="CAT-204", cat_name="Fuente del estado de vigencia", cat_def="Origen del estado de vigencia presentado.", values=[
   V("oficial_importado", "Importado de fuente oficial", "Tomado de una fuente oficial consolidada."),
   V("calculado", "Calculado por Juztina", "Obtenido por reglas sobre eventos registrados."),
   V("revisado", "Revisado por persona", "Confirmado o corregido por un revisor."),
   V("editorial_importado", "Importado de fuente editorial", "Tomado de anotaciones de un consolidado no oficial."),
   V("desconocido", "Desconocido", "Sin fuente identificable."),
 ]),
 dict(cat_id="CAT-205", cat_name="Tipo de texto", cat_def="Naturaleza del texto de una versión.", values=[
   V("original_publicado", "Original publicado", "Texto tal como se publicó por primera vez."),
   V("consolidado_oficial", "Consolidado oficial", "Texto actualizado por una fuente oficial."),
   V("consolidado_editorial", "Consolidado editorial", "Texto actualizado por un editor no oficial."),
   V("compilacion_oficial", "Compilación oficial", "Texto ordenado, único ordenado o refundido aprobado como acto propio.", status=SEMILLA),
   V("reconstruido", "Reconstruido por Juztina", "Obtenido aplicando operaciones registradas."),
 ]),
 dict(cat_id="CAT-206", cat_name="Completitud histórica", cat_def="Grado de disponibilidad de la historia textual de una obra.", values=[
   V("completa", "Completa", "Todas las versiones observadas o reconstruidas con eventos completos."),
   V("parcial", "Parcial", "Faltan versiones o eventos intermedios."),
   V("solo_consolidado_vigente", "Solo texto consolidado vigente", "Únicamente el texto actual."),
   V("solo_original", "Solo texto original", "Únicamente el texto publicado originalmente."),
   V("desconocida", "Desconocida", "No se puede determinar."),
 ]),
 dict(cat_id="CAT-207", cat_name="Clase de unidad estructural", cat_def="Forma de identificar una unidad estructural.", values=[
   V("division_rotulada", "División rotulada", "Parte numerada o nombrada por el propio texto."),
   V("seccion_funcional", "Sección funcional", "Parte identificada por su función en el razonamiento."),
 ]),
 dict(cat_id="CAT-208", cat_name="Nivel estructural", cat_def="Niveles de la jerarquía interna de una obra. Semilla común con variantes nacionales.", values=[
   V("obra", "Obra completa", "Raíz del árbol."),
   V("libro", "Libro", "División mayor de códigos."), V("parte", "Parte", "División mayor."),
   V("titulo", "Título", "División de primer o segundo nivel.", parent="libro"),
   V("capitulo", "Capítulo", "División intermedia.", parent="titulo"),
   V("seccion", "Sección", "División intermedia.", parent="capitulo"),
   V("subseccion", "Subsección", "División intermedia.", parent="seccion"),
   V("articulo", "Artículo", "Unidad dispositiva básica."),
   V("disposicion", "Disposición complementaria, transitoria o final", "Unidad dispositiva accesoria.", status=SEMILLA),
   V("parrafo", "Párrafo o apartado", "Subdivisión del artículo.", parent="articulo"),
   V("paragrafo", "Parágrafo", "Subdivisión usada en algunos países (p. ej., CO).", country="CO", status=SEMILLA),
   V("inciso", "Inciso", "Subdivisión; su alcance varía por país.", status=SEMILLA),
   V("numeral", "Numeral", "Subdivisión numerada."),
   V("literal", "Literal", "Subdivisión con letras."),
   V("fraccion", "Fracción", "Subdivisión con números romanos (p. ej., MX).", country="MX", status=SEMILLA),
   V("item", "Ítem de lista", "Elemento de lista no rotulado como inciso."),
   V("anexo", "Anexo", "Contenido anexo a la obra."),
   V("considerando", "Considerando", "Unidad de preámbulo o motivación."),
   V("fundamento_numerado", "Fundamento numerado", "Párrafo numerado de una resolución."),
   V("punto_resolutivo", "Punto resolutivo", "Unidad de la parte resolutiva."),
   V("nota_al_pie", "Nota al pie", "Nota vinculada a una llamada."),
 ]),
 dict(cat_id="CAT-209", cat_name="Tipo de sección funcional", cat_def="Funciones de las secciones en el documento.", values=[
   V("encabezado", "Encabezado", "Identificación de la resolución, partes y órgano."),
   V("vistos", "Vistos o base legal", "Enumeración de antecedentes documentales y normas."),
   V("antecedentes", "Antecedentes", "Historia procesal o del procedimiento."),
   V("hechos", "Hechos", "Relato fáctico."),
   V("pretensiones", "Pretensiones", "Lo pedido por las partes."),
   V("alegaciones", "Alegaciones de parte", "Argumentos de las partes."),
   V("problema_juridico", "Problema jurídico", "Cuestión jurídica delimitada."),
   V("fundamentos_de_hecho", "Fundamentos de hecho", "Valoración probatoria y hechos probados."),
   V("fundamentos_de_derecho", "Fundamentos de derecho", "Razonamiento jurídico."),
   V("parte_resolutiva", "Parte resolutiva", "Decisión."),
   V("voto", "Voto separado", "Voto singular, discordante, concurrente o aclaración."),
   V("firmas", "Firmas", "Bloque de firmas."),
   V("considerandos_norma", "Considerandos de la norma", "Preámbulo motivador de normas o actos generales."),
   V("exposicion_motivos", "Exposición de motivos incorporada", "Motivación incluida en el texto publicado."),
   V("introduccion", "Introducción", "Sección introductoria de doctrina."),
   V("desarrollo", "Desarrollo", "Cuerpo de doctrina."),
   V("conclusiones", "Conclusiones", "Cierre de doctrina."),
   V("bibliografia", "Bibliografía", "Lista de referencias."),
   V("resumen", "Resumen o abstract", "Resumen del autor."),
 ]),
 dict(cat_id="CAT-210", cat_name="Evento estructural", cat_def="Cambios de estructura de una unidad.", values=[
   V("nacimiento_publicacion", "Nacimiento por publicación original", "La unidad existe desde la obra original."),
   V("nacimiento_incorporacion", "Nacimiento por incorporación", "La unidad nace por operación de incorporación."),
   V("renumeracion", "Renumeración", "Cambio de rótulo de la misma unidad."),
   V("reubicacion", "Reubicación", "Cambio de ruta de la misma unidad."),
   V("cambio_epigrafe", "Cambio de epígrafe", "Cambio del título breve."),
   V("division", "División", "La unidad se extingue o continúa y origina otras."),
   V("fusion", "Fusión", "Varias unidades confluyen en una."),
   V("sustitucion_sin_continuidad", "Sustitución sin continuidad", "Bloque reemplazado por unidades nuevas."),
   V("extincion", "Extinción", "Fin de la unidad por derogación."),
 ]),
 dict(cat_id="CAT-211", cat_name="Grado de continuidad", cat_def="Certeza de la identidad o relación estructural.", values=[
   V("declarada", "Declarada", "Establecida por la norma o tabla oficial."),
   V("presunta", "Presunta", "Regla de mismo rótulo validada por país.", status=SEMILLA),
   V("inferida", "Inferida", "Similitud de contenido; solo candidata."),
   V("curada", "Curada", "Confirmada por revisor."),
   V("no_determinada", "No determinada", "Sin elementos suficientes."),
 ]),
 dict(cat_id="CAT-212", cat_name="Relación estructural entre unidades", cat_def="Relaciones entre unidades distintas.", values=[
   V("se_divide_en", "Se divide en", "1 → N."), V("se_fusiona_en", "Se fusiona en", "N → 1."),
   V("es_sustituida_por", "Es sustituida por", "Sin continuidad de identidad."),
   V("deriva_de", "Deriva de", "Unidad nueva que toma contenido de otra que sigue existiendo."),
   V("corresponde_a", "Corresponde a", "Entre unidades de obras distintas."),
 ]),
 dict(cat_id="CAT-213", cat_name="Tipo de disposición accesoria", cat_def="Clases de disposiciones accesorias de normas. Semilla.", values=[
   V("complementaria_final", "Complementaria final", "Disposición final complementaria.", status=SEMILLA),
   V("complementaria_transitoria", "Complementaria transitoria", "Régimen transitorio.", status=SEMILLA),
   V("complementaria_modificatoria", "Complementaria modificatoria", "Modifica otras normas.", status=SEMILLA),
   V("complementaria_derogatoria", "Complementaria derogatoria", "Deroga otras normas.", status=SEMILLA),
   V("transitoria", "Transitoria", "Artículos o disposiciones transitorias.", status=SEMILLA),
   V("final", "Final", "Disposiciones finales.", status=SEMILLA),
   V("adicional", "Adicional", "Disposiciones adicionales.", status=SEMILLA),
   V("derogatoria", "Derogatoria", "Disposición derogatoria.", status=SEMILLA),
 ]),
 dict(cat_id="CAT-214", cat_name="Tipo de contenido no textual", cat_def="Contenido de anexos y bloques no textuales.", values=[
   V("tabla", "Tabla", "Datos en filas y columnas."), V("cuadro", "Cuadro", "Tabla con formato libre."),
   V("formulario", "Formulario", "Modelo para completar."), V("plano", "Plano", "Representación técnica."),
   V("mapa", "Mapa", "Representación territorial."), V("grafico", "Gráfico", "Representación visual de datos."),
   V("imagen", "Imagen", "Ilustración o escaneo."), V("formula", "Fórmula", "Expresión matemática."),
   V("lista", "Lista", "Enumeración."),
 ]),
 dict(cat_id="CAT-215", cat_name="Tipo de voto", cat_def="Clases de votos separados. Semilla; nombres y efectos varían por país.", values=[
   V("voto_singular", "Voto singular", "Voto propio de un integrante.", status=SEMILLA),
   V("voto_discordante", "Voto discordante o en discordia", "Discrepa del fallo.", status=SEMILLA),
   V("salvamento_de_voto", "Salvamento de voto", "Discrepancia (terminología usada p. ej. en CO).", country="CO", status=SEMILLA),
   V("aclaracion_de_voto", "Aclaración de voto", "Comparte el fallo con precisiones.", status=SEMILLA),
   V("voto_concurrente", "Voto concurrente", "Coincide con el fallo por otras razones.", status=SEMILLA),
   V("fundamento_de_voto", "Fundamento de voto", "Razones adicionales.", status=SEMILLA),
 ]),
 dict(cat_id="CAT-216", cat_name="Tipo de segmento", cat_def="Tipos técnicos de segmento.", values=[
   V("parrafo", "Párrafo", "Bloque separado por saltos."), V("oracion", "Oración", "Unidad sintáctica."),
   V("item_lista", "Ítem de lista", "Elemento de enumeración."), V("celda_tabla", "Celda de tabla", "Celda individual."),
   V("nota", "Nota", "Texto de nota."), V("bloque_procesamiento", "Bloque de procesamiento", "Fragmento técnico para el modelo."),
 ]),
 dict(cat_id="CAT-217", cat_name="Naturaleza temporal de la norma", cat_def="Carácter temporal de la vigencia de una obra.", values=[
   V("permanente", "Permanente", "Sin término declarado."),
   V("temporal_con_plazo", "Temporal con plazo", "Rige hasta una fecha o plazo."),
   V("temporal_condicionada", "Temporal condicionada", "Rige hasta un evento."),
   V("vigencia_diferida", "Vigencia diferida", "Entrada en vigor posterior y condicionada."),
 ]),
 dict(cat_id="CAT-219", cat_name="Precisión de fecha", cat_def="Precisión de una fecha registrada.", values=[
   V("dia", "Día", "Fecha completa."), V("mes", "Mes", "Mes y año."), V("anio", "Año", "Solo año."), V("desconocida", "Desconocida", "No se conoce."),
 ]),
 dict(cat_id="CAT-220", cat_name="Base de cómputo de la entrada en vigor", cat_def="Criterio que fija la entrada en vigor.", values=[
   V("fecha_expresa", "Fecha expresa", "Fecha calendario declarada."),
   V("desde_publicacion", "Desde la publicación", "Rige desde su publicación o el día siguiente según el texto."),
   V("plazo_desde_publicacion", "Plazo desde la publicación", "Rige tras un plazo declarado."),
   V("condicionada_reglamentacion", "Condicionada a reglamentación", "Rige con la publicación del reglamento."),
   V("condicionada_evento", "Condicionada a un evento", "Rige con otro hecho."),
   V("regla_supletoria", "Regla supletoria del país", "Sin fórmula; aplica la regla general del país.", status=SEMILLA),
 ]),
 dict(cat_id="CAT-221", cat_name="Tipo de fuente del evento", cat_def="Procedencia del dato de un evento temporal.", values=[
   V("documento_oficial", "Documento oficial", "Extraído del texto oficial que contiene el evento."),
   V("nota_editorial_consolidado", "Nota editorial de consolidado", "Tomado de anotaciones de un texto consolidado."),
   V("fuente_oficial_externa", "Fuente oficial externa", "Registro oficial consultado."),
   V("curaduria", "Curaduría", "Registrado por un revisor."),
 ]),
 dict(cat_id="CAT-222", cat_name="Condición de observación de la versión", cat_def="Cómo conoce Juztina una versión.", values=[
   V("observada", "Observada", "Existe una manifestación con ese texto."),
   V("reconstruida", "Reconstruida", "Generada aplicando operaciones registradas."),
   V("referida_sin_texto", "Referida sin texto", "Se sabe que existió pero no hay texto."),
 ]),
]
