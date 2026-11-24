"""
Grupo 4 del Diccionario Maestro: D07 Referencias y relaciones, D13 Actores y partes,
D14 Procedimiento y estado procesal. Incluye REL_TYPES (vocabulario de tipos de relación).
Principio rector (arquitectura v3, sección D): una referencia es un hecho textual; una relación es un
vínculo jurídico. Detectar una cita NUNCA crea por sí sola una relación sustantiva.
"""

FIELDS = []


def F(id, tech, func, dim, profiles, unit, defn, just, dtype, card, values, example, origin, method,
      evidence, extraction, validation, applicability, prio, mode, review, privacy, deps, funcs, stage,
      risk, obs="Sin observaciones adicionales.", countries="ALL", country_status="Común", pending="No"):
    FIELDS.append(dict(id=id, tech=tech, func=func, dim=dim, profiles=profiles, unit=unit, defn=defn,
                       just=just, dtype=dtype, card=card, values=values, example=example, origin=origin,
                       method=method, evidence=evidence, extraction=extraction, validation=validation,
                       applicability=applicability, prio=prio, mode=mode, review=review, privacy=privacy,
                       deps=deps, funcs=funcs, obs=obs, stage=stage, risk=risk, countries=countries,
                       country_status=country_status, pending=pending))


NA_SYS = "No aplica: valor generado por el sistema."
NA_EVID_SYS = "No aplica: generado por el sistema; se registra la ejecución."
NA_EVID_CALC = "Regla de cálculo aplicada y afirmaciones de entrada (hereda su evidencia)."
NA_EX_CALC = "No aplica: no se extrae; se calcula en E7 con la regla indicada en Validación."
ALL_REF = "Todas las categorías y países; toda unidad estructural o sección funcional que contenga una mención a otro documento."

# =====================================================================================
# D07 — REFERENCIAS (unidad 'Referencia')
# =====================================================================================
F("MDJ-D07-001", "id_referencia", "Identificador de la referencia", "D07", "UNI", "Referencia",
  "Identificador persistente y opaco de cada mención detectada de otro documento o de una parte de él.",
  "Permite resolver, corregir y auditar cada cita sin releer el documento y vincularla a las relaciones que la usan.",
  "Identificador", "1 obligatorio", NA_SYS, "REF-7f3a91c2", "Generado por sistema", "Generado por sistema",
  NA_EVID_SYS, "Se asigna al registrar la referencia en E4; nunca se reutiliza.",
  "Único en el repositorio; inmutable.", ALL_REF, "P0", "A", "No", "Ninguna",
  "Ejecución de E4", "F11; F12; F16", "Sistema", "R3")

F("MDJ-D07-002", "referencia_unidad_origen", "Unidad de origen de la referencia", "D07", "UNI", "Referencia",
  "Unidad estructural o fragmento textual del documento de origen en el que aparece la mención.",
  "Las relaciones se predican entre unidades, no entre documentos completos; sin la unidad de origen no hay trazabilidad fina.",
  "Referencia", "1 obligatorio", "Referencia a una Unidad estructural (o Fragmento textual) existente.",
  "Considerando 12 de la Sentencia X (ID UE-…)", "Explícito en documento", "Extracción directa",
  "Ancla de la mención dentro de la unidad.",
  "Asignar la unidad estructural más fina que contiene completamente la cadena citada, según la segmentación de E2.",
  "La unidad debe pertenecer a la misma obra que la manifestación anclada y contener la evidencia.",
  ALL_REF, "P0", "A", "No", "Ninguna", "Segmentación E2; MDJ-D07-005", "F11; F12; F15", "E4", "R2")

F("MDJ-D07-003", "referencia_ubicacion", "Ubicación funcional de la referencia", "D07", "UNI", "Referencia",
  "Sección funcional del documento de origen donde aparece la mención (vistos, antecedentes, alegaciones de parte, fundamentos, parte resolutiva, voto separado, nota al pie, bibliografía, cuerpo normativo, etc.).",
  "Es la señal principal para distinguir una cita formal de un uso decisivo; condiciona qué relaciones pueden derivarse.",
  "Enum", "1 obligatorio", "CAT-405 Ubicación de la referencia", "fundamentos",
  "Normalizado por regla", "Extracción directa + Normalización", "Ruta estructural de la unidad de origen.",
  "Heredar la sección funcional asignada en E2 a la unidad de origen; si la mención está en nota al pie o bibliografía, usar ese valor.",
  "Valor del catálogo; coherente con el tipo de unidad de origen (p. ej., 'parte resolutiva' solo en jurisprudencia o actos).",
  ALL_REF, "P0", "A", "No", "Ninguna", "MDJ-D07-002; clasificación de secciones de E2",
  "F07; F08; F11", "E4", "R2")

F("MDJ-D07-004", "referencia_cadena_literal", "Cadena literal de la mención", "D07", "UNI", "Referencia",
  "Texto exacto con el que el documento de origen menciona el documento o la disposición referida, tal como aparece.",
  "Conserva el hecho primario; permite reintentar la resolución cuando el corpus crezca sin releer el documento.",
  "String", "1 obligatorio", "Texto libre transcrito (sin normalizar).",
  "artículo 22, inciso b), de la Ley N.° 29783", "Explícito en documento", "Extracción directa",
  "Coincidencia literal verificable con el texto de la manifestación.",
  "Copiar la mención completa desde el primer elemento identificador hasta el último (tipo, número, disposición); no incluir texto argumentativo.",
  "Debe coincidir carácter a carácter con el tramo anclado; longitud ≤ 500 caracteres.",
  ALL_REF, "P0", "A", "No", "Ninguna", "MDJ-D07-005", "F11; F15; F16", "E4", "R1")

F("MDJ-D07-005", "referencia_evidencia", "Ancla de evidencia de la referencia", "D07", "UNI", "Referencia",
  "Posición inicial y final de la mención en el texto normalizado de la manifestación.",
  "Hace verificable la referencia y permite mostrarla resaltada al usuario.",
  "Ancla de evidencia", "1 obligatorio", "Objeto {manifestación, inicio, fin, hash del texto}.",
  "{M-12, 10452, 10498, sha256:…}", "Explícito en documento", "Extracción directa",
  "Tramo de texto de la manifestación.",
  "Registrar las posiciones del tramo exacto de MDJ-D07-004 sobre el texto normalizado de E0.",
  "inicio < fin; el texto entre posiciones debe ser idéntico a la cadena literal.",
  ALL_REF, "P0", "A", "No", "Ninguna", "Texto normalizado E0", "F15; F16", "E4", "R1")

F("MDJ-D07-006", "referencia_tipo", "Tipo de referencia", "D07", "UNI", "Referencia",
  "Clase del documento mencionado: normativa, jurisprudencial, acto administrativo, doctrinal o cita textual/transcripción.",
  "Determina los componentes mínimos que se extraen y la estrategia de resolución.",
  "Enum", "1 obligatorio", "CAT-401 Tipo de referencia", "normativa", "Normalizado por regla",
  "Clasificación", "Cadena literal.",
  "Asignar según los elementos de la cadena (tipo de norma, órgano jurisdiccional, entidad administrativa, autor/año) y, para tipo 5, por la presencia de transcripción delimitada (comillas, bloque) atribuida a otro documento.",
  "Valor del catálogo. Una transcripción se registra como tipo 5 y además genera una referencia del tipo de su fuente (1–4).",
  ALL_REF, "P0", "A", "No", "Ninguna", "MDJ-D07-004", "F03; F11; F12", "E4", "R2")

# ---- Componentes de referencia normativa
F("MDJ-D07-007", "ref_norm_tipo_norma", "Tipo de norma mencionado", "D07", "UNI", "Referencia",
  "Denominación del tipo de norma tal como aparece en la cita (ley, decreto supremo, decreto legislativo, DFL, DNU, decisión andina, etc.).",
  "Componente mínimo para resolver la cita contra el catálogo de tipos documentales del país.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se normaliza contra el catálogo de tipos documentales por país (Entidad: tipo documental).",
  "Decreto Supremo", "Explícito en documento", "Extracción directa + Normalización", "Cadena literal.",
  "Extraer la denominación del tipo; si la cita usa alias (\"la LPAG\") dejar vacío este campo y registrar el alias en MDJ-D07-012.",
  "Obligatorio si referencia_tipo = normativa y la cadena contiene el tipo; debe mapear a un tipo del país o quedar como 'no catalogado'.",
  "Referencias de tipo normativa, todas las categorías.", "P0", "A", "No", "Ninguna",
  "MDJ-D07-006; catálogo de tipos documentales por país", "F03; F11", "E4", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D07-008", "ref_norm_numero", "Número de la norma mencionada", "D07", "UNI", "Referencia",
  "Número oficial de la norma tal como aparece en la cita, sin el año.",
  "Identificador principal para resolver la cita.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se conserva formato original (p. ej., 29783, 004-2019-JUS, 1.234).",
  "29783", "Explícito en documento", "Extracción directa", "Cadena literal.",
  "Tomar el número que sigue al tipo de norma; separar el año si va unido (\"004-2019-JUS\" se conserva entero y además se llena MDJ-D07-009).",
  "Debe aparecer literalmente en la cadena; validación de formato con patrones por país y tipo.",
  "Referencias normativas con número.", "P0", "A", "No", "Ninguna", "MDJ-D07-004", "F03; F11", "E4", "R1",
  country_status="Catálogo por país")

F("MDJ-D07-009", "ref_norm_anio", "Año de la norma mencionada", "D07", "UNI", "Referencia",
  "Año de emisión o publicación de la norma si la cita lo indica.",
  "Desambigua números que se repiten en distintos años (decretos, resoluciones).",
  "Integer", "0..1 opcional", "Año de 4 dígitos.", "2019", "Explícito en documento",
  "Extracción directa + Normalización", "Cadena literal.",
  "Extraer el año explícito (\"de 2019\", \"/2019\", \"-2019-\"); no inferirlo de la fecha del documento de origen.",
  "1800 ≤ año ≤ año de emisión del documento de origen.",
  "Referencias normativas con año explícito.", "P0", "A", "No", "Ninguna", "MDJ-D07-004", "F03; F11", "E4", "R2")

F("MDJ-D07-010", "ref_norm_jurisdiccion", "Jurisdicción de la norma mencionada", "D07", "UNI", "Referencia",
  "País o pseudo jurisdicción (CAN, SIDH, MERCOSUR) de la norma citada, explícita o, si no se indica, la del documento de origen marcada como presunta.",
  "Evita resolver citas a normas extranjeras o comunitarias contra el corpus nacional.",
  "Código ISO", "1 obligatorio", "CAT-001 País y jurisdicción", "CAN", "Normalizado por regla",
  "Normalización + Inferencia", "Cadena literal o contexto de la cita.",
  "Si la cita nombra país u organismo (\"Decisión 486 de la Comunidad Andina\") usar ese valor; si no, asumir la jurisdicción del origen y marcar 'presunta'.",
  "Valor del catálogo; si se presume, la afirmación lleva modo 'Inferido por modelo'.",
  "Referencias normativas.", "P0", "A", "No", "Ninguna", "MDJ-D07-004", "F09; F11", "E4", "R2")

F("MDJ-D07-011", "ref_norm_emisor_mencionado", "Emisor mencionado en la cita normativa", "D07", "UNI", "Referencia",
  "Autoridad emisora citada junto a la norma, cuando consta (ministerio, municipalidad, superintendencia).",
  "Necesario para resolver normas infralegales con números repetidos entre entidades.",
  "String", "0..1 opcional", "Texto transcrito; se normaliza contra Entidad: organismo u órgano en la resolución.",
  "Ministerio de Trabajo y Promoción del Empleo", "Explícito en documento", "Extracción directa",
  "Cadena literal.", "Extraer la entidad nombrada en la misma cita; no tomarla de otra parte del documento.",
  "Debe aparecer en la cadena o inmediatamente contigua (misma oración).",
  "Referencias normativas infralegales.", "P1", "A", "No", "Ninguna", "MDJ-D07-004", "F11", "E4", "R2")

F("MDJ-D07-012", "ref_norm_alias", "Alias o denominación abreviada citada", "D07", "UNI", "Referencia",
  "Nombre corto, sigla o denominación usual con que se cita la norma (\"el Código Civil\", \"la LPAG\", \"el Estatuto Tributario\").",
  "Gran parte de las citas no usan número; el alias es la única vía de resolución.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se resuelve contra la tabla de alias por país y periodo (catálogo D, curado).",
  "la LPAG", "Explícito en documento", "Extracción directa", "Cadena literal.",
  "Extraer el alias tal cual; si el documento define el alias (\"en adelante, la Ley\"), registrar la definición como evidencia adicional.",
  "Obligatorio cuando no hay número; el alias debe aparecer literalmente.",
  "Referencias normativas sin número o con alias.", "P0", "A", "No", "Ninguna",
  "Tabla de alias por país (fuente curada)", "F03; F11; F15", "E4", "R2",
  country_status="Catálogo por país",
  obs="Los alias cambian de referente en el tiempo (p. ej., un código sustituido por otro); la resolución usa la fecha del documento de origen.")

F("MDJ-D07-013", "ref_norm_disposicion_citada", "Disposición citada", "D07", "UNI", "Referencia",
  "Ruta de la disposición mencionada hasta el nivel más fino indicado (artículo, párrafo, inciso, numeral, literal, disposición complementaria).",
  "Las relaciones y la jurisprudencia por artículo dependen de identificar la unidad exacta citada.",
  "Array", "0..n", "Lista ordenada de pares {nivel estructural, rótulo} (niveles según catálogo de niveles estructurales).",
  "[{artículo, 22}, {inciso, b}]", "Explícito en documento", "Extracción directa + Normalización", "Cadena literal.",
  "Descomponer la cita en niveles; si cita varios artículos (\"arts. 20 a 25\") registrar una referencia por artículo o un rango explícito marcado como rango.",
  "Cada rótulo debe aparecer en la cadena; los niveles deben respetar el orden jerárquico.",
  "Referencias normativas que mencionan disposiciones.", "P0", "A", "No", "Ninguna",
  "MDJ-D07-004; catálogo de niveles estructurales (D05)", "F06; F11; F15", "E4", "R1")

F("MDJ-D07-014", "ref_norm_indicacion_version", "Indicación de versión en la cita", "D07", "UNI", "Referencia",
  "Si la cita señala expresamente la versión del texto citado (texto original, modificado por una norma, vigente a una fecha) o no lo indica.",
  "Prevalece sobre la regla de versión por fecha de origen para resolver el fragmento exacto citado.",
  "Enum", "1 obligatorio", "CAT-422 Indicación de versión en la cita", "modificado_por_norma",
  "Explícito en documento", "Extracción directa + Normalización", "Cadena literal o contigua.",
  "Buscar expresiones como \"texto original\", \"modificado por\", \"vigente al momento de los hechos\", \"antes de su modificación\" en la misma oración de la cita.",
  "Si el valor es distinto de 'no indicada', debe existir evidencia literal.",
  "Referencias normativas.", "P1", "A", "No", "Ninguna", "MDJ-D07-004", "F06; F11", "E4", "R2")

F("MDJ-D07-015", "ref_norm_detalle_version", "Detalle de versión indicada", "D07", "UNI", "Referencia",
  "Texto literal que precisa la versión citada (norma modificatoria o fecha) cuando la indicación no es 'no indicada'.",
  "Permite resolver el fragmento textual exacto en la línea de vida de la disposición.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito.",
  "modificado por el artículo 2 de la Ley N.° 30709", "Explícito en documento", "Extracción directa",
  "Cadena contigua a la referencia.", "Copiar la expresión que precisa la versión; si menciona otra norma, generar además una referencia normativa a esa norma.",
  "Obligatorio si MDJ-D07-014 ≠ 'no indicada'.", "Referencias normativas con versión indicada.",
  "P1", "A", "No", "Ninguna", "MDJ-D07-014", "F06; F11", "E4", "R2")

# ---- Componentes de referencia jurisprudencial
F("MDJ-D07-016", "ref_jur_organo_mencionado", "Órgano jurisdiccional mencionado", "D07", "UNI", "Referencia",
  "Tribunal, corte o sala nombrada en la cita jurisprudencial.",
  "Componente necesario para resolver la cita y para calcular la fuerza del precedente invocado.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se normaliza contra Entidad: organismo u órgano.",
  "Sala de Derecho Constitucional y Social Permanente de la Corte Suprema", "Explícito en documento",
  "Extracción directa + Normalización", "Cadena literal.",
  "Extraer el órgano nombrado en la cita o deducible del formato inequívoco del identificador (p. ej., prefijos de la Corte Constitucional colombiana); en este último caso marcar modo normalizado.",
  "Obligatorio si referencia_tipo = jurisprudencial y consta; normalización con candidato único o queda 'no resuelto'.",
  "Referencias jurisprudenciales.", "P0", "A", "No", "Ninguna", "MDJ-D07-006", "F07; F08; F11", "E4", "R2",
  country_status="Catálogo por país")

F("MDJ-D07-017", "ref_jur_tipo_resolucion", "Tipo de resolución judicial mencionada", "D07", "UNI", "Referencia",
  "Clase de pronunciamiento citado según su denominación original (sentencia, casación, auto, tesis, sentencia de unificación, recurso, etc.).",
  "Distingue citas de sentencias, tesis o autos, cuya fuerza y resolución difieren.",
  "String", "0..1 opcional", "Texto transcrito; se normaliza contra el catálogo de tipos documentales del país.",
  "Casación", "Explícito en documento", "Extracción directa + Normalización", "Cadena literal.",
  "Extraer la denominación del pronunciamiento citado.", "Debe aparecer en la cadena o derivarse del identificador con regla documentada.",
  "Referencias jurisprudenciales.", "P0", "A", "No", "Ninguna", "MDJ-D07-006", "F07; F08; F11", "E4", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D07-018", "ref_jur_identificador", "Identificador oficial de la resolución citada", "D07", "UNI", "Referencia",
  "Número, rol, expediente, código o registro con el que se cita la resolución (incluye registro digital de tesis, rol, número de casación, código de sentencia).",
  "Clave principal de resolución de citas jurisprudenciales.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se conserva el formato original.",
  "T-760/08", "Explícito en documento", "Extracción directa", "Cadena literal.",
  "Extraer el identificador completo con su prefijo, número y año tal como figura.",
  "Debe aparecer literalmente; validación por patrón del país y tipo cuando exista.",
  "Referencias jurisprudenciales.", "P0", "A", "No", "Ninguna", "MDJ-D07-004", "F07; F08; F11", "E4", "R1",
  country_status="Catálogo por país")

F("MDJ-D07-019", "ref_jur_fecha", "Fecha de la resolución citada", "D07", "UNI", "Referencia",
  "Fecha de emisión de la resolución citada cuando la cita la incluye.",
  "Desambigua resoluciones y permite verificar la resolución contra el corpus.",
  "Fecha parcial", "0..1 opcional", "ISO 8601 (AAAA, AAAA-MM o AAAA-MM-DD).", "2008-07-31",
  "Explícito en documento", "Extracción directa + Normalización", "Cadena literal.",
  "Extraer la fecha que acompaña la cita; no tomar la fecha de publicación del repertorio.",
  "Fecha válida y anterior o igual a la emisión del documento de origen.",
  "Referencias jurisprudenciales con fecha.", "P1", "A", "No", "Ninguna", "MDJ-D07-004", "F07; F11", "E4", "R2")

F("MDJ-D07-020", "ref_jur_fundamento_citado", "Fundamento o considerando citado", "D07", "UNI", "Referencia",
  "Fundamento, considerando o párrafo específico de la resolución citada, si la cita lo indica.",
  "Permite vincular el uso del criterio con la unidad exacta de la resolución citada (ratio frente a obiter).",
  "Array", "0..n", "Lista de rótulos de unidades (fundamento, considerando, párrafo).",
  "[fundamento 12, fundamento 14]", "Explícito en documento", "Extracción directa", "Cadena literal.",
  "Extraer los números de fundamento, considerando o párrafo indicados en la cita.",
  "Cada rótulo debe aparecer en la cadena.", "Referencias jurisprudenciales.", "P1", "A", "No", "Ninguna",
  "MDJ-D07-018", "F07; F08", "E4", "R2")

F("MDJ-D07-021", "ref_jur_invocada_como_precedente", "Invocación expresa como precedente", "D07", "UNI", "Referencia",
  "Indica si el texto de origen invoca expresamente la resolución citada como precedente, jurisprudencia vinculante, doctrina obligatoria o criterio de observancia obligatoria.",
  "Hecho primario para el cálculo de fuerza y de relaciones de seguimiento; no equivale a que lo sea.",
  "Boolean", "1 obligatorio", "true/false", "true", "Explícito en documento", "Extracción directa",
  "Tramo donde se invoca el carácter de precedente.",
  "true solo si el texto usa una expresión de invocación (\"precedente vinculante\", \"jurisprudencia obligatoria\", \"de observancia obligatoria\", \"sentencia de unificación\"); en otro caso false.",
  "Si true, evidencia literal obligatoria. El carácter real de precedente se calcula en D17 por reglas de país.",
  "Referencias jurisprudenciales y a actos de tribunales administrativos.", "P1", "A", "Condicionado",
  "Ninguna", "MDJ-D07-018", "F07; F08", "E4", "R1",
  obs="Revisión humana cuando alimenta el cálculo de precedente (DEC-25).", pending="DEC-25")

F("MDJ-D07-022", "ref_jur_nombre_caso", "Nombre popular del caso citado", "D07", "UNI", "Referencia",
  "Denominación usual con que se cita el caso (\"caso Sánchez\", \"Fallo X\"), cuando sustituye o acompaña al identificador.",
  "Algunas citas solo usan el nombre del caso; es la única vía de resolución.",
  "String", "0..1 opcional", "Texto transcrito.", "caso Barrios Altos", "Explícito en documento",
  "Extracción directa", "Cadena literal.",
  "Extraer el nombre del caso; si incluye nombre de persona natural, conservarlo solo en la cadena literal y no estructurarlo como parte.",
  "Debe aparecer literalmente.", "Referencias jurisprudenciales.", "P1", "A", "No",
  "Puede contener datos personales", "MDJ-D07-004", "F07; F11", "E4", "R2", pending="DEC-18")

# ---- Componentes de referencia a acto administrativo
F("MDJ-D07-023", "ref_adm_entidad_mencionada", "Entidad emisora del acto citado", "D07", "UNI", "Referencia",
  "Entidad pública que emitió el acto administrativo citado.",
  "Los números de actos se repiten entre entidades; la entidad es imprescindible para resolver.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se normaliza contra Entidad: organismo u órgano.",
  "Superintendencia Nacional de Fiscalización Laboral", "Explícito en documento",
  "Extracción directa + Normalización", "Cadena literal o contigua.",
  "Extraer la entidad nombrada en la cita o en la oración; si el acto es del propio emisor del documento (\"la presente\", \"nuestra Resolución\"), usar el emisor del origen marcando normalizado.",
  "Obligatorio si referencia_tipo = acto administrativo.", "Referencias a actos administrativos.",
  "P0", "A", "No", "Ninguna", "MDJ-D07-006", "F11", "E4", "R2", country_status="Catálogo por país")

F("MDJ-D07-024", "ref_adm_tipo_acto", "Tipo de acto citado", "D07", "UNI", "Referencia",
  "Denominación original del acto citado (resolución, oficio, concepto, dictamen, circular, informe, acuerdo).",
  "Necesario para resolver y para distinguir actos decisorios de pronunciamientos interpretativos.",
  "String", "0..1 opcional", "Texto transcrito; se normaliza contra el catálogo de tipos documentales del país.",
  "Resolución de Intendencia", "Explícito en documento", "Extracción directa + Normalización",
  "Cadena literal.", "Extraer la denominación del acto tal como aparece.", "Debe aparecer en la cadena.",
  "Referencias a actos administrativos.", "P0", "A", "No", "Ninguna", "MDJ-D07-006", "F11", "E4", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D07-025", "ref_adm_numero", "Número del acto citado", "D07", "UNI", "Referencia",
  "Número oficial del acto citado, con su formato original.", "Clave de resolución de la cita.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito.", "0123-2023-SUNAFIL/ILM",
  "Explícito en documento", "Extracción directa", "Cadena literal.",
  "Extraer el número completo con siglas y año.", "Debe aparecer literalmente.",
  "Referencias a actos administrativos con número.", "P0", "A", "No", "Ninguna", "MDJ-D07-004", "F11", "E4", "R1")

F("MDJ-D07-026", "ref_adm_fecha", "Fecha del acto citado", "D07", "UNI", "Referencia",
  "Fecha de emisión o notificación del acto citado cuando la cita la indica, con su tipo.",
  "Desambigua actos y ordena la cadena del procedimiento.", "Fecha parcial", "0..1 opcional",
  "ISO 8601.", "2023-05-14", "Explícito en documento", "Extracción directa + Normalización",
  "Cadena literal o contigua.", "Extraer la fecha que acompaña la cita del acto; si dice 'notificada el', registrarlo en observaciones de la afirmación.",
  "Fecha válida ≤ fecha del documento de origen.", "Referencias a actos administrativos.", "P1", "A", "No",
  "Ninguna", "MDJ-D07-004", "F11", "E4", "R2")

F("MDJ-D07-027", "ref_adm_es_acto_impugnado", "Acto citado es el impugnado", "D07", "JUR; ADM", "Referencia",
  "Indica si el acto o resolución citada es el objeto de la impugnación, recurso o demanda que resuelve el documento de origen.",
  "Hecho primario del proceso: permite construir la cadena procesal y las relaciones anula/confirma.",
  "Boolean", "1 obligatorio", "true/false", "true", "Explícito en documento", "Extracción directa + Inferencia",
  "Tramo de antecedentes o parte resolutiva que identifica el acto impugnado.",
  "true si el texto lo identifica como impugnado, recurrido, materia de la demanda o del recurso; si se infiere sin expresión literal, marcar inferido.",
  "Si true, evidencia en antecedentes o parte resolutiva; a lo sumo un acto impugnado principal por recurso.",
  "Referencias a actos y resoluciones en jurisprudencia y actos administrativos recursivos.", "P0", "A",
  "Condicionado", "Ninguna", "MDJ-D07-003", "F07; F11; F12", "E4", "R1",
  obs="Revisión si la marca proviene de inferencia y alimenta relaciones de cadena procesal.")

# ---- Componentes de referencia doctrinal
F("MDJ-D07-028", "ref_doc_cadena_bibliografica", "Cadena bibliográfica citada", "D07", "UNI", "Referencia",
  "Texto completo de la referencia doctrinal o bibliográfica (nota al pie, entrada de bibliografía o mención en el cuerpo).",
  "Conserva la cita para análisis bibliográfico posterior sin releer el documento.",
  "Texto largo", "0..1 obligatorio condicionado", "Texto transcrito.",
  "GARCÍA, J. (2015). La prescripción tributaria. Lima: Ed. X, p. 45.", "Explícito en documento",
  "Extracción directa", "Cadena literal.", "Copiar la entrada completa hasta el final de la referencia (incluidas páginas).",
  "Obligatorio si referencia_tipo = doctrinal; coincidencia literal.", "Referencias doctrinales en todas las categorías.",
  "P1", "A", "No", "Ninguna", "MDJ-D07-006", "F04; F11", "E4", "R3")

F("MDJ-D07-029", "ref_doc_autor_anio", "Autor y año reconocidos en la cita doctrinal", "D07", "UNI", "Referencia",
  "Apellido(s) del autor y año de la obra reconocibles en la cadena bibliográfica.",
  "Mínimo necesario para agrupar citas doctrinales y medir influencia sin análisis completo.",
  "Objeto", "0..1 opcional", "{autores: [apellidos], anio}", "{[García], 2015}", "Explícito en documento",
  "Extracción directa + Normalización", "Cadena literal.",
  "Extraer apellidos tal como aparecen y el año; no completar nombres de pila.",
  "Cada apellido y el año deben aparecer en la cadena.", "Referencias doctrinales.", "P1", "A", "No",
  "Ninguna", "MDJ-D07-028", "F04; F11", "E4", "R3",
  obs="Los autores de doctrina publicada no se tratan como datos personales sensibles; se limitan a la atribución.")

F("MDJ-D07-030", "ref_doc_analisis_bibliografico", "Análisis bibliográfico detallado", "D07", "UNI", "Referencia",
  "Descomposición estructurada de la referencia doctrinal: título, obra mayor, revista, volumen, editorial, edición, páginas, DOI.",
  "Permite resolver la cita contra el corpus doctrinal y construir métricas de influencia.",
  "Objeto", "0..1 opcional", "{titulo, contenedor, volumen, numero, editorial, edicion, paginas, doi}",
  "{La prescripción tributaria, —, —, —, Ed. X, 2.ª, 45, —}", "Normalizado por regla",
  "Normalización + Inferencia", "Cadena bibliográfica conservada.",
  "Procesar la cadena guardada con un analizador bibliográfico; no releer el documento.",
  "Cada componente debe estar contenido en la cadena; DOI con patrón válido.",
  "Referencias doctrinales.", "P3", "C", "No", "Ninguna", "MDJ-D07-028", "F04; F11", "Posterior (C)", "R3")

# ---- Citas textuales
F("MDJ-D07-031", "cita_textual_limites", "Límites del texto transcrito", "D07", "UNI", "Referencia",
  "Posiciones de inicio y fin del tramo transcrito de otro documento (texto entre comillas o en bloque atribuido).",
  "Marca el contenido ajeno para que no se clasifique ni genere efectos como propio del documento de origen.",
  "Ancla de evidencia", "0..1 obligatorio condicionado", "Objeto {manifestación, inicio, fin}.",
  "{M-12, 20410, 21390}", "Explícito en documento", "Extracción directa", "Tramo transcrito.",
  "Delimitar desde la apertura hasta el cierre de la transcripción (comillas, sangría, bloque); si no hay cierre claro, marcar 'indeterminado'.",
  "Obligatorio si referencia_tipo = cita textual; inicio < fin; no debe exceder la unidad de origen.",
  "Referencias de tipo cita textual.", "P1", "A", "No", "Ninguna", "MDJ-D07-006", "F05; F13; F15; F16", "E4", "R2")

F("MDJ-D07-032", "cita_textual_atribucion", "Fuente atribuida a la transcripción", "D07", "UNI", "Referencia",
  "Referencia (tipo 1–4) a la que el documento atribuye el texto transcrito.",
  "Permite verificar la transcripción y saber qué versión del documento se citó.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a otra Referencia del mismo documento.",
  "REF-7f3a91c2", "Explícito en documento", "Extracción directa", "Mención que introduce o cierra la transcripción.",
  "Vincular con la referencia normativa, jurisprudencial, de acto o doctrinal que introduce la transcripción; si no se atribuye, valor 'no atribuida'.",
  "Debe apuntar a una referencia existente del mismo origen.", "Referencias de tipo cita textual.",
  "P1", "A", "No", "Ninguna", "MDJ-D07-031", "F11; F15", "E4", "R2")

F("MDJ-D07-033", "cita_textual_contenido_ajeno", "Marca de contenido ajeno", "D07", "UNI", "Fragmento textual",
  "Indica que un tramo del fragmento es transcripción de otro documento y debe excluirse de la clasificación y de la extracción de efectos propios.",
  "Evita que una sentencia 'genere' las obligaciones del artículo que transcribe o se clasifique por él.",
  "Boolean", "1 obligatorio", "true/false", "true", "Derivado por cálculo", "Cálculo", NA_EVID_CALC,
  NA_EX_CALC, "true si el fragmento contiene al menos un tramo de MDJ-D07-031; las etapas E5 y P2 excluyen esos tramos.",
  "Todos los fragmentos.", "P1", "B", "No", "Ninguna", "MDJ-D07-031", "F13; F16", "E7", "R2")

F("MDJ-D07-034", "cita_textual_verificacion", "Verificación de la transcripción contra el original", "D07", "UNI", "Referencia",
  "Resultado de comparar el texto transcrito con el fragmento textual de destino.",
  "Detecta transcripciones erróneas o de versiones anteriores; base para identificar la versión citada.",
  "Enum", "0..1 opcional", "CAT-423 Verificación de cita textual", "coincide_version_anterior",
  "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Comparación con similitud ≥ umbral contra cada versión del destino; resultado 'no verificable' si el destino no está resuelto a unidad.",
  "Citas textuales con destino resuelto.", "P2", "B", "No", "Ninguna", "MDJ-D07-031; MDJ-D07-038",
  "F06; F15; F16", "E7", "R2")

F("MDJ-D07-035", "cita_textual_version_citada", "Versión efectivamente transcrita", "D07", "UNI", "Referencia",
  "Fragmento textual del destino cuyo texto coincide con la transcripción.",
  "Permite advertir que un criterio se formuló sobre un texto ya modificado.",
  "Referencia", "0..1 opcional", "Referencia a Fragmento textual.", "FT-… (art. 22, versión 2018)",
  "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Solo si MDJ-D07-034 indica coincidencia con una versión concreta.", "Citas textuales verificadas.",
  "P2", "B", "No", "Ninguna", "MDJ-D07-034", "F06; F07; F15", "E7", "R2")

# ---- Resolución
F("MDJ-D07-036", "referencia_destino_identificado", "Componentes de destino identificados", "D07", "UNI", "Referencia",
  "Conjunto normalizado de componentes reconocidos en la cita (tipo, número, año, órgano, entidad, disposición) antes de buscar en el corpus.",
  "Separa lo que dice la cita de lo que Juztina logra resolver; permite reintentar la resolución.",
  "Objeto", "1 obligatorio", "Objeto con los componentes D07-007…D07-029 aplicables, normalizados.",
  "{tipo: ley, numero: 29783, jurisdiccion: PE, disposicion: [art 22]}", "Normalizado por regla",
  "Normalización", "Componentes extraídos.",
  "Componer a partir de los campos de componentes; aplicar normalización de formatos por país.",
  "Al menos un componente identificador (número, identificador, alias o cadena bibliográfica).",
  ALL_REF, "P0", "A", "No", "Ninguna", "MDJ-D07-007 a MDJ-D07-029", "F11; F16", "E4", "R2")

F("MDJ-D07-037", "referencia_estado_resolucion", "Estado de resolución de la referencia", "D07", "UNI", "Referencia",
  "Resultado de buscar el destino en el corpus: resuelta a unidad, resuelta a obra, ambigua, fuera del corpus, no identificable, inconsistente en origen o pendiente.",
  "Hace explícito lo que no se pudo vincular y habilita su resolución posterior sin releer.",
  "Enum", "1 obligatorio", "CAT-403 Estado de resolución", "resuelta_a_unidad", "Derivado por cálculo",
  "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Se recalcula cada vez que cambia el corpus o la tabla de alias; 'pendiente' hasta la primera resolución.",
  ALL_REF, "P0", "B", "No", "Ninguna", "MDJ-D07-036; índice de identificadores del corpus",
  "F11; F12; F16", "E7", "R2")

F("MDJ-D07-038", "referencia_destino_resuelto", "Destino resuelto", "D07", "UNI", "Referencia",
  "Obra, versión, unidad estructural o fragmento del corpus al que apunta la referencia.",
  "Convierte la cita en un enlace navegable y en insumo de relaciones.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Obra, Versión, Unidad estructural o Fragmento textual.",
  "UE-… (Ley 29783, art. 22)", "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Obligatorio si el estado es 'resuelta a unidad' o 'resuelta a obra'; el destino debe existir en el corpus.",
  ALL_REF, "P0", "B", "Condicionado", "Ninguna", "MDJ-D07-036; MDJ-D07-037", "F11; F12; F15", "E7", "R2",
  obs="Revisión humana solo si el destino alimenta una relación R1.")

F("MDJ-D07-039", "referencia_granularidad_destino", "Granularidad del destino", "D07", "UNI", "Referencia",
  "Nivel al que se logró resolver el destino: obra, versión, unidad estructural o subunidad.",
  "Indica la precisión del enlace y si puede usarse para jurisprudencia por artículo.",
  "Enum", "0..1 obligatorio condicionado", "CAT-404 Granularidad del destino", "unidad_estructural",
  "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Coherente con el tipo de destino resuelto.", ALL_REF, "P0", "B", "No", "Ninguna", "MDJ-D07-038",
  "F11; F16", "E7", "R3")

F("MDJ-D07-040", "referencia_version_destino", "Versión de destino", "D07", "UNI", "Referencia",
  "Fragmento textual o versión del destino que estaba vigente a la fecha de emisión del documento de origen, salvo indicación expresa de otra versión en la cita.",
  "Permite saber qué texto interpretó o aplicó la jurisprudencia y advertir cuando ya cambió.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Versión o Fragmento textual.",
  "FT-… (art. 22, texto 2016–2019)", "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Regla: versión con intervalo que contiene la fecha de emisión del origen; si MDJ-D07-014 ≠ 'no indicada', usar la versión indicada. Si la línea de vida es incompleta, estado 'indeterminado'.",
  "Referencias normativas resueltas a unidad.", "P1", "B", "No", "Ninguna",
  "MDJ-D07-038; MDJ-D07-014; líneas de vida (D03); fecha de emisión del origen", "F06; F07; F15", "E7", "R2",
  pending="DEC-32")

F("MDJ-D07-041", "referencia_regla_version_destino", "Regla usada para la versión de destino", "D07", "UNI", "Referencia",
  "Criterio aplicado para fijar la versión de destino: fecha del documento de origen, indicación expresa de la cita o no determinable.",
  "Hace auditable la elección de versión.", "Enum", "0..1 obligatorio condicionado",
  "fecha_origen | indicacion_expresa | no_determinable", "fecha_origen", "Derivado por cálculo",
  "Cálculo", NA_EVID_CALC, NA_EX_CALC, "Obligatorio si existe MDJ-D07-040.",
  "Referencias normativas resueltas.", "P1", "B", "No", "Ninguna", "MDJ-D07-040", "F16", "E7", "R3")

F("MDJ-D07-042", "referencia_candidatos", "Candidatos de destino en ambigüedad", "D07", "UNI", "Referencia",
  "Lista de obras o unidades candidatas cuando la referencia es ambigua.",
  "Permite resolver la ambigüedad por curaduría o con más contexto sin repetir la búsqueda.",
  "Array de referencias", "0..n", "Referencias a Obra o Unidad estructural con puntaje de coincidencia.",
  "[DS 004-2019-JUS, DS 004-2019-EM]", "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Obligatorio con ≥ 2 elementos si el estado es 'ambigua'.", "Referencias ambiguas.", "P1", "B",
  "Condicionado", "Ninguna", "MDJ-D07-037", "F11; F16", "E7", "R2",
  obs="Va a revisión humana si la referencia sostiene una relación R1.")

F("MDJ-D07-043", "referencia_motivo_no_resolucion", "Motivo de no resolución", "D07", "UNI", "Referencia",
  "Causa por la que la referencia no se resolvió a unidad: destino fuera del corpus, alias desconocido, disposición inexistente en la versión, datos insuficientes, error del origen.",
  "Orienta la ampliación del corpus y de la tabla de alias.", "Enum", "0..1 obligatorio condicionado",
  "CAT-430 Motivo de no resolución", "fuera_del_corpus", "Derivado por cálculo", "Cálculo", NA_EVID_CALC,
  NA_EX_CALC, "Obligatorio si el estado no es 'resuelta a unidad'.", "Referencias no resueltas o resueltas solo a obra.",
  "P1", "B", "No", "Ninguna", "MDJ-D07-037", "F16; F18", "E7", "R3")

F("MDJ-D07-044", "referencia_funcion", "Función de la referencia en el origen", "D07", "UNI", "Referencia",
  "Papel que cumple la mención en el razonamiento del documento de origen: base legal formal, fundamento decisivo, transcripción, alegación de parte, contraste, antecedente histórico u operación normativa.",
  "Filtro que impide convertir una cita en relación sustantiva; base para relaciones interpretativas.",
  "Enum", "1 obligatorio", "CAT-402 Función de la referencia", "fundamento_decisivo", "Inferido por modelo",
  "Inferencia", "Unidad de origen y su sección funcional.",
  "Clasificar según la sección y el uso: listas en vistos o base legal → base legal formal; mención en alegaciones de parte → alegación; fórmula modificatoria → operación normativa (transcrito); mención que sostiene la conclusión en fundamentos → fundamento decisivo.",
  "Valor del catálogo; 'operación normativa' exige fórmula operativa literal; 'fundamento decisivo' exige ubicación en fundamentos o parte resolutiva.",
  ALL_REF, "P1", "A", "No", "Ninguna", "MDJ-D07-003", "F07; F08; F11", "E4", "R2",
  obs="La función 'operación normativa' se obtiene por transcripción y puede adelantarse a P0 junto con E6.")

F("MDJ-D07-045", "referencia_en_voto_separado", "Referencia en voto separado", "D07", "JUR; ADM", "Referencia",
  "Indica si la referencia aparece en un voto singular, disidente, salvamento o aclaración de voto, y no en la decisión de mayoría.",
  "Impide atribuir a la mayoría citas o criterios que solo sostiene un voto separado.",
  "Boolean", "1 obligatorio", "true/false", "false", "Derivado por cálculo", "Cálculo", NA_EVID_CALC,
  NA_EX_CALC, "true si la unidad de origen es una sección funcional de voto separado.",
  "Referencias en jurisprudencia y resoluciones colegiadas.", "P1", "B", "No", "Ninguna",
  "MDJ-D07-002; sección funcional (D05)", "F07; F08", "E7", "R2")

# =====================================================================================
# D07 — RELACIONES (unidad 'Relación')
# =====================================================================================
ALL_REL = "Todas las categorías; según el tipo de relación (ver REL_TYPES, hoja Relaciones y referencias)."

F("MDJ-D07-050", "id_relacion", "Identificador de la relación", "D07", "UNI", "Relación",
  "Identificador persistente de cada vínculo jurídico registrado entre dos unidades de registro.",
  "Permite auditar, revisar y revocar relaciones de forma individual.", "Identificador", "1 obligatorio",
  NA_SYS, "REL-0c91d2aa", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Se asigna al crear la relación en E6 o E7, o al curarla.", "Único e inmutable.", ALL_REL, "P0", "A",
  "No", "Ninguna", "Ejecución E6/E7", "F11; F12; F16", "Sistema", "R3")

F("MDJ-D07-051", "relacion_unidad_origen", "Unidad de origen de la relación", "D07", "UNI", "Relación",
  "Unidad de registro desde la cual se establece el vínculo (p. ej., el artículo de la norma modificatoria; el considerando que interpreta).",
  "Las relaciones se predican entre unidades para permitir vigencia y jurisprudencia por disposición.",
  "Referencia", "1 obligatorio", "Referencia a Obra, Versión, Unidad estructural, Fragmento textual o Proceso, según REL_TYPES.origin_units.",
  "UE-… (Ley 30709, art. 2)", "Explícito en documento", "Extracción directa", "Ancla en la unidad de origen.",
  "Para relaciones transcritas, la unidad que contiene la fórmula operativa o el punto resolutivo; para interpretadas, el fundamento que expresa la operación.",
  "El tipo de unidad debe estar permitido para el tipo de relación.", ALL_REL, "P0", "A", "No", "Ninguna",
  "MDJ-D07-053", "F11; F12", "E6", "R2")

F("MDJ-D07-052", "relacion_unidad_destino", "Unidad de destino de la relación", "D07", "UNI", "Relación",
  "Unidad de registro sobre la que recae el vínculo (la disposición modificada, la resolución revocada, el precedente seguido).",
  "Completa el enlace y permite consultas inversas.", "Referencia", "1 obligatorio",
  "Referencia a una unidad de registro permitida por REL_TYPES.target_units.", "UE-… (Ley 29783, art. 22)",
  "Derivado por cálculo", "Cálculo", "Destino resuelto de la referencia de soporte.",
  "Tomar el destino resuelto de la(s) referencia(s) de soporte; si la referencia no está resuelta, la relación queda en estado 'candidata' con destino pendiente.",
  "Debe existir; si la referencia de soporte es ambigua, la relación no se activa.", ALL_REL, "P0", "B", "No",
  "Ninguna", "MDJ-D07-038; MDJ-D07-055", "F11; F12", "E7", "R2")

F("MDJ-D07-053", "relacion_tipo", "Tipo de relación", "D07", "UNI", "Relación",
  "Tipo del vínculo jurídico, de un vocabulario cerrado (modifica, deroga expresamente, interpreta, revoca, se aparta, etc.).",
  "Núcleo semántico del grafo jurídico; determina qué cálculos alimenta.", "Enum", "1 obligatorio",
  "CAT-406 Tipo de relación (ver hoja Relaciones y referencias)", "modifica", "Normalizado por regla",
  "Extracción directa + Clasificación",
  "Fórmula operativa o expresión del fundamento.",
  "Transcritas: mapear el verbo operativo literal (\"modifícase\", \"derógase\", \"declárase fundado… nula\") al tipo. Interpretadas: aplicar la regla del tipo en REL_TYPES. Nunca crear una relación sustantiva solo porque exista una cita.",
  "Valor del catálogo; compatible con las unidades de origen/destino y con el modo de obtención.", ALL_REL,
  "P0", "A", "Condicionado", "Ninguna", "REL_TYPES", "F05; F06; F07; F08; F11; F12", "E6", "R1",
  obs="P0 para familias operativa, control y procesal; P2 para interpretativas (ver prioridad por tipo en REL_TYPES).")

F("MDJ-D07-054", "relacion_familia", "Familia de la relación", "D07", "UNI", "Relación",
  "Agrupación del tipo de relación (operación normativa, desarrollo normativo, control de validez, cadena procesal, uso normativo, uso de precedentes, estructural, doctrinal, aplicabilidad, citación, derivada).",
  "Facilita filtros y reglas comunes por familia.", "Enum", "1 obligatorio", "CAT-424 Familia de relación",
  "operacion_normativa", "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Se deriva del tipo según REL_TYPES; no se asigna de forma independiente.", ALL_REL, "P0", "B", "No",
  "Ninguna", "MDJ-D07-053", "F03; F11; F12", "E7", "R3")

F("MDJ-D07-055", "relacion_modo_obtencion", "Modo de obtención de la relación", "D07", "UNI", "Relación",
  "Cómo se obtuvo la relación: transcrita de una fórmula expresa, interpretada por el modelo, calculada por regla o curada por una persona.",
  "Separa relaciones explícitas de inferidas; condiciona su uso en vigencia y precedentes.", "Enum",
  "1 obligatorio", "CAT-407 Modo de obtención de la relación", "transcrita", "Generado por sistema",
  "Generado por sistema", "Registro de la etapa que la produjo.",
  "Lo asigna la etapa: E6 → transcrita; perfil P2 interpretativo → interpretada; E7 → calculada; curaduría → curada.",
  "Debe ser compatible con REL_TYPES.origin_mode del tipo.", ALL_REL, "P0", "A", "No", "Ninguna",
  "MDJ-D07-053", "F11; F16", "Sistema", "R2")

F("MDJ-D07-056", "relacion_referencias_soporte", "Referencias de soporte", "D07", "UNI", "Relación",
  "Referencias detectadas en las que se apoya la relación.",
  "Si una referencia se corrige o se resuelve de otro modo, la relación se recalcula.", "Array de referencias",
  "0..n", "Referencias a Referencia.", "[REF-7f3a91c2]", "Generado por sistema", "Generado por sistema",
  NA_EVID_SYS, "Registrar todas las referencias que identifican el destino de la relación.",
  "Obligatorio ≥ 1 salvo relaciones calculadas sin cita (inversas, pertenencia al mismo proceso).",
  ALL_REL, "P0", "A", "No", "Ninguna", "MDJ-D07-001", "F11; F16", "E6", "R2")

F("MDJ-D07-057", "relacion_evidencia", "Evidencia de la relación", "D07", "UNI", "Relación",
  "Ancla(s) del tramo que expresa el vínculo: la fórmula operativa, el punto resolutivo o el pasaje del fundamento que aplica, interpreta o se aparta.",
  "Una relación sin evidencia no es verificable ni presentable al usuario.", "Ancla de evidencia", "1..n",
  "Objeto {manifestación, inicio, fin} por tramo.", "{M-40, 3301, 3420}", "Explícito en documento",
  "Extracción directa", "Tramo que expresa la operación (distinto de la sola cadena citada para relaciones interpretadas).",
  "Para interpretadas, anclar el pasaje que subsume o fija el sentido, no solo la mención.",
  "Verificación literal; para relaciones interpretadas la evidencia debe estar en fundamentos o parte resolutiva.",
  ALL_REL, "P0", "A", "No", "Ninguna", "MDJ-D07-051", "F15; F16", "E6", "R1")

F("MDJ-D07-058", "relacion_seccion_evidencia", "Sección de la evidencia de la relación", "D07", "UNI", "Relación",
  "Sección funcional donde se ubica la evidencia principal de la relación.",
  "Control de calidad: relaciones de uso derivadas de vistos o alegaciones se rechazan.", "Enum",
  "1 obligatorio", "CAT-405 Ubicación de la referencia", "parte_resolutiva", "Derivado por cálculo", "Cálculo",
  NA_EVID_CALC, NA_EX_CALC, "Se deriva de la unidad que contiene la evidencia.", ALL_REL, "P0", "B", "No",
  "Ninguna", "MDJ-D07-057", "F16", "E7", "R2")

F("MDJ-D07-059", "relacion_fecha_efecto_inicio", "Fecha desde la que la relación produce efecto", "D07", "UNI", "Relación",
  "Fecha jurídica desde la cual produce efecto el vínculo (entrada en vigor de la modificación, fecha de la sentencia que anula, etc.).",
  "Indispensable para reconstruir versiones y responder preguntas en una fecha dada.", "Fecha", "0..1 obligatorio condicionado",
  "ISO 8601.", "2018-01-01", "Explícito en documento", "Extracción directa + Normalización",
  "Fórmula de vigencia expresa o fecha del documento de origen.",
  "Si la norma fija fecha de efecto para la operación, transcribirla; si no, dejar 'no encontrado' y calcular en D03 con la regla de entrada en vigor del país (marcando 'calculado').",
  "Obligatorio para familias operativa y control; nunca anterior a la emisión salvo retroactividad expresa con evidencia.",
  "Relaciones operativas, de control y procesales.", "P0", "A", "Condicionado", "Ninguna",
  "Eventos temporales (D03)", "F05; F06", "E6", "R1", pending="DEC-17")

F("MDJ-D07-060", "relacion_fecha_efecto_fin", "Fecha hasta la que la relación produce efecto", "D07", "UNI", "Relación",
  "Fecha en que el vínculo deja de producir efecto (fin de una suspensión, término de una prórroga, revocación de la decisión que anuló).",
  "Permite relaciones temporales (suspensiones, prórrogas) y su reversión.", "Fecha", "0..1 opcional",
  "ISO 8601.", "2024-06-30", "Explícito en documento", "Extracción directa + Normalización",
  "Plazo expreso o evento posterior.", "Transcribir el término expreso; si se deriva de un evento posterior, calcular.",
  "≥ fecha de inicio.", "Relaciones temporales (suspende, prorroga) y relaciones revertidas.", "P1", "A",
  "No", "Ninguna", "MDJ-D07-059", "F05; F06", "E6", "R2")

F("MDJ-D07-061", "relacion_calificador", "Calificador jurídico de la relación", "D07", "UNI", "Relación",
  "Matiz jurídico del vínculo: parcial, total, condicionada, diferida, con efectos retroactivos, en voto separado, presunta, etc.",
  "Evita tratar como total una derogación parcial o como simple una exequibilidad condicionada.",
  "Enum múltiple", "0..n", "CAT-408 Calificador de la relación", "[parcial, diferida]",
  "Explícito en documento", "Extracción directa + Normalización", "Tramo que expresa el matiz.",
  "Extraer las expresiones que limitan el alcance (\"en el extremo\", \"en cuanto\", \"en el entendido de que\", \"a partir de\").",
  "Cada calificador con evidencia literal, salvo 'presunta' (lo asigna la regla).", ALL_REL, "P1", "A",
  "Condicionado", "Ninguna", "MDJ-D07-057", "F05; F06; F07", "E6", "R1")

F("MDJ-D07-062", "relacion_texto_condicion", "Texto de la condición o alcance", "D07", "UNI", "Relación",
  "Texto literal de la condición interpretativa (exequibilidad condicionada), del extremo afectado (nulidad parcial) o del alcance de la operación.",
  "Las condiciones interpretativas obligatorias cambian la lectura de la norma sin cambiar su texto.",
  "Texto largo", "0..1 obligatorio condicionado", "Texto transcrito.",
  "en el entendido de que el plazo se computa en días hábiles", "Explícito en documento", "Extracción directa",
  "Tramo de la parte resolutiva.", "Transcribir el pasaje que fija la condición o el extremo.",
  "Obligatorio si el calificador incluye 'condicionada' o 'parcial'.", "Relaciones de control y procesales.",
  "P0", "A", "Sí", "Ninguna", "MDJ-D07-061", "F05; F06; F07; F15", "E6", "R1",
  country_status="Pendiente validación nacional", pending="DEC-17",
  obs="La forma y efectos de la exequibilidad condicionada y figuras análogas deben validarse por país.")

F("MDJ-D07-063", "relacion_estado", "Estado de la relación", "D07", "UNI", "Relación",
  "Situación del vínculo: activa, candidata (falta resolver destino o revisión), rechazada, revertida (p. ej., la decisión que anuló fue revocada) o sustituida.",
  "Solo las relaciones activas alimentan vigencia, precedentes y el grafo público.", "Enum", "1 obligatorio",
  "CAT-409 Estado de la relación", "activa", "Derivado por cálculo", "Cálculo + Revisión humana",
  NA_EVID_CALC, NA_EX_CALC,
  "candidata si destino no resuelto, modo interpretado sin umbral o R1 sin revisión; activa en otro caso; revertida si existe relación posterior que la deja sin efecto.",
  ALL_REL, "P0", "B", "Condicionado", "Ninguna", "MDJ-D07-052; MDJ-D07-055; capa de procedencia",
  "F05; F06; F11; F12; F16", "E7", "R1")

F("MDJ-D07-064", "relacion_alimenta_calculos", "Cálculos que alimenta la relación", "D07", "UNI", "Relación",
  "Cálculos posteriores que usan esta relación: vigencia, texto consolidado, carácter de precedente, cadena procesal, resultado final, ninguno.",
  "Hace explícito el impacto de un error y prioriza la revisión.", "Enum múltiple", "1..n",
  "CAT-425 Cálculo alimentado", "[vigencia, texto_consolidado]", "Derivado por cálculo", "Cálculo",
  NA_EVID_CALC, NA_EX_CALC, "Se deriva de REL_TYPES.feeds del tipo; solo relaciones activas alimentan.",
  ALL_REL, "P0", "B", "No", "Ninguna", "MDJ-D07-053; MDJ-D07-063", "F06; F08; F16", "E7", "R2")

F("MDJ-D07-065", "relacion_es_inversa", "Relación inversa calculada", "D07", "UNI", "Relación",
  "Indica si el registro es la inversa calculada de otra relación (p. ej., 'es modificada por').",
  "Permite navegar el grafo en ambos sentidos sin duplicar la evidencia ni la revisión.", "Boolean",
  "1 obligatorio", "true/false", "false", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "true para relaciones creadas por la regla de inversión; heredan estado de la directa.",
  "Si true, debe existir MDJ-D07-066.", ALL_REL, "P1", "B", "No", "Ninguna", "MDJ-D07-053", "F11; F12", "E7", "R3")

F("MDJ-D07-066", "relacion_directa", "Relación directa de la que deriva", "D07", "UNI", "Relación",
  "Relación original de la que es inversa o derivada un registro calculado.",
  "Trazabilidad: la inversa no tiene evidencia propia.", "Referencia", "0..1 obligatorio condicionado",
  "Referencia a Relación.", "REL-0c91d2aa", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Se asigna al calcular la inversa.", "Obligatorio si MDJ-D07-065 = true.", ALL_REL, "P1", "B", "No",
  "Ninguna", "MDJ-D07-065", "F16", "E7", "R3")

F("MDJ-D07-067", "relacion_punto_resolutivo", "Punto resolutivo que contiene la relación", "D07", "JUR; ADM", "Relación",
  "Unidad del punto resolutivo concreto en el que se declara la relación procesal o de control.",
  "Una resolución puede confirmar un extremo y revocar otro; la relación se ata a cada punto.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Unidad estructural (sección funcional: punto resolutivo).",
  "UE-… (punto resolutivo 2)", "Explícito en documento", "Extracción directa", "Punto resolutivo.",
  "Asociar la relación al punto resolutivo que la declara.", "Obligatorio para familias control y procesal.",
  "Relaciones de control y de cadena procesal.", "P0", "A", "No", "Ninguna", "MDJ-D14-020", "F07; F11", "E6", "R1")

F("MDJ-D07-068", "relacion_conflicto", "Conflicto con otra relación o fuente", "D07", "UNI", "Relación",
  "Marca de discrepancia entre esta relación y otra relación o una fuente externa (p. ej., la fuente oficial consolidada no registra la modificación).",
  "Regla: ante discrepancias se conservan ambas fuentes con marca; nunca se elige en silencio.", "Array de referencias",
  "0..n", "Referencias a Relación o a afirmación importada en conflicto.", "[REL-…, IMP-…]",
  "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Se marca cuando dos relaciones activas incompatibles recaen sobre el mismo destino e intervalo, o contradicen una fuente oficial.",
  ALL_REL, "P1", "B", "Sí", "Ninguna", "MDJ-D07-063", "F06; F16", "E8", "R1")

F("MDJ-D07-069", "relacion_resultado_uso_precedente", "Fundamento del uso del precedente", "D07", "JUR; ADM", "Relación",
  "Para relaciones sigue, reitera, distingue, se aparta o unifica: el criterio o regla del precedente que se usa y cómo se usa, en una frase con plantilla fija.",
  "Las relaciones de precedente sin el criterio concreto no permiten análisis de líneas jurisprudenciales.",
  "Texto largo", "0..1 obligatorio condicionado", "Plantilla: \"[Origen] [operación] el criterio de [destino] según el cual […] porque […]\".",
  "La Sala se aparta del criterio de la Casación X según el cual el plazo es de caducidad, porque…",
  "Inferido por modelo", "Inferencia", "Pasaje del fundamento que expresa la operación.",
  "Redactar con la plantilla a partir del pasaje anclado; no agregar razones no contenidas en el texto.",
  "Obligatorio para familia uso de precedentes; la evidencia debe estar en fundamentos.",
  "Jurisprudencia y resoluciones de tribunales administrativos.", "P2", "C", "Sí", "Ninguna",
  "MDJ-D07-053; problemas jurídicos (D05)", "F07; F08", "Posterior (C)", "R1", pending="DEC-25")

# =====================================================================================
# D13 — ACTORES Y PARTES
# =====================================================================================
PARTES_APL = "Jurisprudencia y actos administrativos (y laudos, si se incorporan: DEC-07)."

F("MDJ-D13-001", "id_parte", "Identificador de la parte o actor", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Identificador persistente de cada registro de interviniente (parte, tercero, administrado, funcionario o autor) en una obra o proceso.",
  "Permite referenciar roles sin depender de nombres y aplicar la política de datos personales.",
  "Identificador", "1 obligatorio", NA_SYS, "PTE-93ab", "Generado por sistema", "Generado por sistema",
  NA_EVID_SYS, "Se asigna al registrar el interviniente en E3.", "Único e inmutable.", PARTES_APL, "P1", "A",
  "No", "Ninguna", "Ejecución E3", "F07; F17", "Sistema", "R3")

F("MDJ-D13-002", "parte_unidad_sujeto", "Unidad a la que pertenece la parte", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Obra (resolución) o proceso al que se vincula el interviniente.",
  "Las partes son del proceso; su rol puede cambiar por instancia y resolución.", "Referencia", "1 obligatorio",
  "Referencia a Obra o Proceso.", "OB-… (Casación X)", "Generado por sistema", "Generado por sistema",
  NA_EVID_SYS, "Vincular a la obra donde se identificó; agregar al proceso en E7.",
  "Debe existir la unidad.", PARTES_APL, "P1", "A", "No", "Ninguna", "Obra; Proceso", "F07", "Sistema", "R3")

F("MDJ-D13-003", "parte_rol_procesal", "Rol procesal o procedimental", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Posición del interviniente en el proceso o procedimiento: demandante, demandado, administrado, denunciante, tercero, Ministerio Público, procuraduría, etc.",
  "Base del análisis de resultados por tipo de litigante y de la cadena procesal.", "Enum", "1 obligatorio",
  "CAT-410 Rol procesal", "demandante", "Normalizado por regla", "Extracción directa + Normalización",
  "Tramo del encabezado o antecedentes que asigna el rol.",
  "Extraer la denominación original del rol (\"accionante\", \"recurrente\", \"administrado\") y mapearla al catálogo; conservar la denominación original en observaciones de la afirmación.",
  "Valor del catálogo con evidencia literal; incompatible con 'parte_rol_recursal' contradictorio en la misma resolución.",
  PARTES_APL, "P1", "A", "No", "Ninguna", "MDJ-D13-001", "F07; F14", "E3", "R2",
  country_status="Catálogo por país")

F("MDJ-D13-004", "parte_rol_recursal", "Rol en el recurso que se resuelve", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Posición del interviniente en el recurso o impugnación concreta: recurrente, recurrido, apelante, apelado, adherido.",
  "En instancias de revisión el demandante puede ser recurrido; invertir roles distorsiona el resultado.",
  "Enum", "0..1 obligatorio condicionado", "CAT-410 Rol procesal (valores recursales)", "recurrido",
  "Normalizado por regla", "Extracción directa + Normalización", "Tramo que identifica al recurrente.",
  "Extraer solo si la resolución resuelve un recurso; no deducirlo del rol en primera instancia.",
  "Obligatorio si la resolución resuelve un recurso (D14).", PARTES_APL, "P1", "A", "No", "Ninguna",
  "MDJ-D13-003; MDJ-D14-015", "F07; F14", "E3", "R1")

F("MDJ-D13-005", "parte_tipo", "Tipo de parte", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Naturaleza del interviniente: persona natural, persona jurídica privada, entidad pública, colectivo o comunidad, anonimizada o no determinable.",
  "Habilita el análisis sin identificar personas y decide qué datos pueden estructurarse.", "Enum", "1 obligatorio",
  "CAT-411 Tipo de parte", "persona_juridica_privada", "Inferido por modelo", "Clasificación",
  "Denominación de la parte en el texto.",
  "Clasificar por la forma de la denominación (razón social, siglas societarias, nombre de entidad pública, nombres y apellidos, iniciales).",
  "Valor del catálogo; si hay iniciales o siglas de anonimización → 'anonimizada'.", PARTES_APL, "P0", "A",
  "No", "Puede contener datos personales", "MDJ-D13-001", "F07; F14; F17", "E3", "R2",
  obs="P0 porque condiciona la aplicación de la política de datos personales.", pending="DEC-18")

F("MDJ-D13-006", "parte_denominacion_no_natural", "Denominación de persona jurídica o entidad pública", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Razón social o nombre de la entidad que interviene, solo cuando la parte no es persona natural.",
  "Permite búsquedas por empresa o entidad y análisis sectorial sin tratar datos de personas naturales.",
  "String", "0..1 obligatorio condicionado", "Texto transcrito.", "Compañía Minera X S.A.A.",
  "Explícito en documento", "Extracción directa", "Tramo con la denominación.",
  "Transcribir la denominación tal como aparece; prohibido llenar si parte_tipo = persona natural o anonimizada.",
  "Obligatorio si parte_tipo ∈ {persona jurídica privada, entidad pública}; vacío ('no aplica') en otro caso.",
  PARTES_APL, "P1", "A", "No", "Ninguna", "MDJ-D13-005", "F03; F07; F10", "E3", "R2")

F("MDJ-D13-007", "parte_entidad_normalizada", "Entidad normalizada de la parte", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Vínculo de la parte con el registro maestro de organismos (entidad pública) o de personas jurídicas.",
  "Unifica variantes de nombre (siglas, denominaciones antiguas) para búsquedas y estadísticas.", "Referencia",
  "0..1 opcional", "Referencia a Entidad: organismo u órgano o Entidad: persona (jurídica).", "ORG-SUNAT",
  "Derivado por cálculo", "Cálculo + Revisión humana", "Denominación transcrita y regla de resolución.",
  NA_EX_CALC, "Coincidencia única con el registro maestro; variantes nuevas a revisión.",
  PARTES_APL, "P1", "B", "Condicionado", "Ninguna", "MDJ-D13-006", "F03; F10; F12", "E7", "R2",
  pending="DEC-33")

F("MDJ-D13-008", "parte_contiene_nombre_persona_natural", "Presencia de nombre de persona natural", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Indica si el texto identifica a esta parte con nombre de persona natural (no iniciales), sin estructurar el nombre.",
  "Insumo obligatorio para aplicar anonimización y controles de exposición.", "Boolean", "1 obligatorio",
  "true/false", "true", "Explícito en documento", "Extracción directa", "Ancla del nombre (no se copia el valor).",
  "Marcar true si la parte aparece con nombres y apellidos; guardar solo el ancla, nunca el nombre en un campo estructurado.",
  "Si true, debe existir ancla; el ancla se usa solo por procesos de anonimización.", PARTES_APL, "P0", "A",
  "No", "Dato personal", "MDJ-D13-005", "F17", "E3", "R1", pending="DEC-18")

F("MDJ-D13-009", "parte_anonimizada_en_fuente", "Parte anonimizada en la fuente", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Indica si la fuente ya oculta la identidad de la parte (iniciales, siglas, 'NN', expresión de reserva).",
  "Evita reidentificar y documenta el cumplimiento de reglas de anonimización de la fuente.", "Boolean",
  "1 obligatorio", "true/false", "true", "Explícito en documento", "Extracción directa", "Tramo con la forma anonimizada.",
  "true si la parte aparece con iniciales, siglas o mención de reserva.", "Coherente con parte_tipo = anonimizada.",
  PARTES_APL, "P0", "A", "No", "Puede contener datos personales", "MDJ-D13-005", "F17", "E3", "R2",
  pending="DEC-18")

F("MDJ-D13-010", "parte_condicion_proteccion", "Condición de protección especial de la parte", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Indicador de que la parte pertenece a una categoría protegida mencionada en el texto: menor de edad, víctima de violencia, persona con discapacidad, paciente, pueblo indígena, etc.",
  "Activa reglas reforzadas de anonimización y permite análisis por grupo protegido sin identificar personas.",
  "Enum múltiple", "0..n", "CAT-428 Condición de protección especial", "[menor_de_edad]", "Explícito en documento",
  "Extracción directa + Clasificación", "Tramo que menciona la condición.",
  "Marcar solo condiciones afirmadas en el texto respecto de esa parte; no inferir por indicios.",
  "Cada valor con evidencia literal.", PARTES_APL, "P0", "A", "No", "Dato personal sensible", "MDJ-D13-001",
  "F17; F04", "E3", "R1", pending="DEC-18",
  obs="Se complementa con los indicadores de datos sensibles a nivel de obra (D16).")

F("MDJ-D13-011", "parte_pluralidad", "Número de personas en la posición", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Cantidad de personas o entidades que ocupan el mismo rol cuando se agrupan (\"y otros\", litisconsorcio).",
  "Contexto para acciones colectivas y para no confundir un registro con una sola persona.", "Integer",
  "0..1 opcional", "Entero ≥ 1 o 'indeterminado'.", "12", "Explícito en documento", "Extracción directa",
  "Tramo que enumera o cuantifica.", "Contar solo si el texto enumera o indica número; 'y otros' → indeterminado.",
  "≥ 1.", PARTES_APL, "P2", "A", "No", "Ninguna", "MDJ-D13-003", "F07", "E3", "R3")

F("MDJ-D13-012", "parte_nombre_persona_natural", "Nombre de persona natural (excluido)", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Nombre y apellidos de una parte, tercero o testigo persona natural en un campo estructurado.",
  "Se documenta para dejar expresa su exclusión: estructurarlo crea un índice consultable de personas.",
  "String", "0..1 opcional", "No aplica: no se almacena en el alcance inicial.", "No aplica",
  "Explícito en documento", "Extracción directa", "No aplica: no se extrae.",
  "No extraer. El texto publicado se conserva en la manifestación; solo se registra MDJ-D13-008.",
  "Cualquier valor en este campo es un error de proceso.", PARTES_APL, "Fuera de alcance", "X", "Sí",
  "Dato personal", "DEC-18", "F17", "E3", "R1", pending="DEC-18; DEC-19",
  obs="Exclusión de la arquitectura v3 (clase X). Solo una decisión legal expresa por país puede reabrirlo.")

F("MDJ-D13-013", "parte_documento_identidad", "Documento de identidad de persona natural (excluido)", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Número de documento de identidad (DNI, cédula, RUN, CURP, etc.) de una persona natural.",
  "Se documenta para prohibir su estructuración; no tiene finalidad jurídica en Juztina que lo justifique.",
  "String", "0..1 opcional", "No aplica: no se almacena.", "No aplica", "Explícito en documento",
  "Extracción directa", "No aplica: no se extrae.",
  "No extraer; registrar su presencia como indicador de dato personal en D16.",
  "Cualquier valor es un error de proceso.", PARTES_APL, "Fuera de alcance", "X", "Sí", "Dato personal sensible",
  "DEC-18", "F17", "E3", "R1", pending="DEC-18")

F("MDJ-D13-014", "abogado_patrocinante", "Abogado patrocinante (excluido)", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Nombre del abogado o apoderado que representa a una parte.",
  "Excluido del alcance inicial: persona natural en rol profesional y valor comercial incierto.",
  "String", "0..1 opcional", "No aplica: no se almacena en el alcance inicial.", "No aplica",
  "Explícito en documento", "Extracción directa", "No aplica: no se extrae.",
  "No extraer en la pasada; reevaluar con decisión de producto y legal.", "Cualquier valor es un error de proceso.",
  PARTES_APL, "Fuera de alcance", "X", "Sí", "Dato personal", "DEC-18", "F17", "E3", "R2", pending="DEC-18")

# ---- Funcionarios y autoridades firmantes
F("MDJ-D13-015", "actor_funcionario_rol", "Rol del funcionario o magistrado", "D13", "JUR; ADM; NOR", "Afirmación compuesta: parte o actor",
  "Función del servidor público en el documento: magistrado ponente, integrante del colegiado, juez, secretario, funcionario emisor o firmante, refrendante.",
  "Distingue autoría institucional de la actuación individual; base para composición del colegiado.", "Enum",
  "1 obligatorio", "CAT-412 Rol del actor institucional", "magistrado_ponente", "Explícito en documento",
  "Extracción directa + Normalización", "Tramo de firma, encabezado o mención del ponente.",
  "Extraer de firmas, encabezados (\"Magistrado ponente\", \"Vocal ponente\") y refrendos.",
  "Valor del catálogo con evidencia.", "Jurisprudencia, actos administrativos y normativa (refrendos).", "P1",
  "A", "No", "Dato de funcionario público", "MDJ-D13-001", "F07; F08", "E3", "R2",
  country_status="Catálogo por país")

F("MDJ-D13-016", "actor_funcionario_nombre", "Nombre del funcionario o magistrado", "D13", "JUR; ADM; NOR", "Afirmación compuesta: parte o actor",
  "Nombre del servidor público que actúa en ejercicio de su función (ponente, integrante, firmante).",
  "Identifica la autoría de la decisión y la composición del colegiado; su uso para estadísticas individuales es una decisión aparte (DEC-19).",
  "String", "0..1 obligatorio condicionado", "Texto transcrito; se normaliza contra Entidad: persona (funcionarios).",
  "Juan Pérez Gómez", "Explícito en documento", "Extracción directa", "Tramo de firma o encabezado.",
  "Transcribir el nombre tal como aparece en firma o encabezado; no completar nombres faltantes.",
  "Debe aparecer literalmente; no se usa para perfiles analíticos sin DEC-19.", "Jurisprudencia, actos y normativa.",
  "P1", "A", "No", "Dato de funcionario público", "MDJ-D13-015", "F07; F08", "E3", "R2", pending="DEC-19")

F("MDJ-D13-017", "actor_funcionario_cargo", "Cargo declarado del funcionario", "D13", "JUR; ADM; NOR", "Afirmación compuesta: parte o actor",
  "Cargo con que firma o actúa el funcionario (Ministro de Economía, Intendente, Vocal Supremo).",
  "Permite verificar competencia y resolver el órgano emisor.", "String", "0..1 opcional", "Texto transcrito.",
  "Intendente Regional", "Explícito en documento", "Extracción directa", "Tramo de firma.",
  "Transcribir el cargo de la línea de firma.", "Debe aparecer literalmente.", "Jurisprudencia, actos y normativa.",
  "P2", "A", "No", "Dato de funcionario público", "MDJ-D13-016", "F04", "E3", "R3")

F("MDJ-D13-018", "actor_funcionario_organo", "Órgano en que actúa el funcionario", "D13", "JUR; ADM; NOR", "Afirmación compuesta: parte o actor",
  "Órgano o sala en la que actúa el funcionario al momento del documento.", "Composición de salas y trazabilidad institucional.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: organismo u órgano.", "ORG-…-SALA2",
  "Normalizado por regla", "Normalización", "Encabezado o firma.", "Tomar el órgano del encabezado de la resolución.",
  "Debe coincidir con el órgano emisor o productor de la obra salvo firma por delegación.", "Jurisprudencia, actos y normativa.",
  "P2", "A", "No", "Ninguna", "MDJ-D13-015", "F07", "E3", "R3")

F("MDJ-D13-019", "actor_sentido_voto", "Sentido del voto del magistrado", "D13", "JUR; ADM", "Afirmación compuesta: parte o actor",
  "Posición del integrante del colegiado: con la mayoría, voto concurrente o aclaración, voto singular o disidente, salvamento parcial.",
  "Base para identificar votos separados y la solidez de la mayoría.", "Enum", "0..1 obligatorio condicionado",
  "CAT-427 Sentido del voto", "disidente", "Explícito en documento", "Extracción directa + Normalización",
  "Rótulo o encabezado del voto separado.", "Asignar según rótulos (\"voto singular\", \"salvamento de voto\", \"aclaración de voto\").",
  "Obligatorio para integrantes de colegiados cuando existe sección de voto separado.", "Resoluciones colegiadas.",
  "P1", "A", "No", "Dato de funcionario público", "MDJ-D13-015", "F07; F08", "E3", "R2",
  country_status="Catálogo por país")

# ---- Autores de doctrina
F("MDJ-D13-020", "autor_nombre", "Nombre del autor", "D13", "DOC", "Afirmación compuesta: parte o actor",
  "Nombre del autor de la obra doctrinal tal como figura en ella.",
  "Atribución obligatoria de la doctrina y señal de autoridad.", "String", "1 obligatorio", "Texto transcrito.",
  "María Rodríguez Salas", "Explícito en documento", "Extracción directa", "Portada, encabezado o metadatos de la publicación.",
  "Transcribir cada autor en el orden de la obra.", "Debe aparecer en la obra o en los metadatos de la fuente.",
  "Doctrina.", "P0", "A", "No", "Dato personal", "MDJ-D13-001", "F03; F04", "E3", "R2",
  obs="Dato personal tratado con la finalidad de atribución de una obra publicada.")

F("MDJ-D13-021", "autor_orden", "Orden de autoría", "D13", "DOC", "Afirmación compuesta: parte o actor",
  "Posición del autor en la lista de autores.", "Preserva la cita correcta de la obra.", "Integer",
  "1 obligatorio", "Entero ≥ 1.", "2", "Explícito en documento", "Extracción directa", "Lista de autores.",
  "Numerar según el orden de aparición.", "Secuencia continua sin repeticiones dentro de la obra.", "Doctrina.",
  "P1", "A", "No", "Ninguna", "MDJ-D13-020", "F04", "E3", "R3")

F("MDJ-D13-022", "autor_afiliacion", "Afiliación institucional del autor", "D13", "DOC", "Afirmación compuesta: parte o actor",
  "Institución declarada por el autor en la obra (universidad, centro, estudio, entidad).",
  "Señal objetiva de procedencia y base de la jurisdicción de origen de la doctrina.", "String", "0..n",
  "Texto transcrito; se normaliza contra Entidad: organismo u órgano cuando sea institución pública o académica registrada.",
  "Pontificia Universidad Católica del Perú", "Explícito en documento", "Extracción directa", "Nota de autor o encabezado.",
  "Transcribir la afiliación declarada en la obra; no buscarla en fuentes externas.", "Debe aparecer en la obra.",
  "Doctrina.", "P1", "A", "No", "Dato personal", "MDJ-D13-020", "F04; F09", "E3", "R3")

F("MDJ-D13-023", "autor_identificador_externo", "Identificador académico del autor", "D13", "DOC", "Afirmación compuesta: parte o actor",
  "Identificador persistente del autor (p. ej., ORCID) si figura en la obra o en la fuente.",
  "Desambigua autores homónimos.", "String", "0..1 opcional", "Formato del identificador (ORCID: 0000-0000-0000-0000).",
  "0000-0002-1825-0097", "Explícito en documento", "Extracción directa", "Mención en la obra o metadatos de la fuente.",
  "Extraer solo si aparece; no buscar externamente en la pasada.", "Patrón y dígito de control válidos.", "Doctrina.",
  "P2", "A", "No", "Dato personal", "MDJ-D13-020", "F04", "E3", "R3")

# ---- Entidad: persona (mínima según política)
PERS_APL = "Registro maestro de personas admitidas por la política: autores de doctrina, funcionarios en ejercicio y personas jurídicas privadas."

F("MDJ-D13-030", "id_persona", "Identificador de persona", "D13", "UNI", "Entidad: persona",
  "Identificador persistente del registro maestro de persona admitida por la política de datos.",
  "Unifica variantes de nombre de autores, funcionarios y personas jurídicas.", "Identificador", "1 obligatorio",
  NA_SYS, "PER-00412", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Se crea al consolidar actores en E7 o por curaduría.", "Único e inmutable.", PERS_APL, "P1", "B", "No",
  "Dato personal", "MDJ-D13-001", "F03; F12; F17", "E7", "R3", pending="DEC-18")

F("MDJ-D13-031", "persona_clase", "Clase de persona registrada", "D13", "UNI", "Entidad: persona",
  "Clase del registro maestro: autor de doctrina, funcionario público, persona jurídica privada.",
  "Restringe el registro maestro a las clases admitidas por la política; las personas naturales partes no se registran.",
  "Enum", "1 obligatorio", "autor | funcionario | persona_juridica_privada", "funcionario",
  "Normalizado por regla", "Normalización", "Rol de origen.", "Derivar de los roles en que aparece la persona.",
  "Prohibido crear registros para personas naturales que solo son partes o terceros.", PERS_APL, "P1", "B", "No",
  "Dato personal", "MDJ-D13-030", "F17", "E7", "R2", pending="DEC-18")

F("MDJ-D13-032", "persona_denominacion_preferente", "Denominación preferente", "D13", "UNI", "Entidad: persona",
  "Nombre normalizado de la persona registrada.", "Etiqueta única para búsquedas y presentación.", "String",
  "1 obligatorio", "Texto normalizado.", "Rodríguez Salas, María", "Curado por persona", "Normalización + Revisión humana",
  "Variantes observadas.", "Seleccionar la forma más completa observada; confirmar en curaduría si hay homónimos.",
  "Única por persona; sin duplicados exactos.", PERS_APL, "P1", "B", "Condicionado", "Dato personal",
  "MDJ-D13-030", "F03; F04", "Curaduría", "R2")

F("MDJ-D13-033", "persona_variantes", "Variantes de nombre", "D13", "UNI", "Entidad: persona",
  "Formas alternativas con que aparece la persona (iniciales, apellidos invertidos, razón social anterior, siglas).",
  "Permite reconocer la misma persona en distintos documentos.", "Array", "0..n", "Lista de cadenas.",
  "[M. Rodríguez, Rodríguez S., María]", "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Sin duplicados; cada variante observada en al menos un documento.", PERS_APL, "P2", "B", "No", "Dato personal",
  "MDJ-D13-032", "F03", "E7", "R3")

F("MDJ-D13-034", "persona_juridica_identificador_tributario", "Identificador tributario de persona jurídica", "D13", "UNI", "Entidad: persona",
  "Número de identificación tributaria (RUC, NIT, RUT, CUIT, RFC) de una persona jurídica privada, cuando figura en el documento.",
  "Clave auxiliar para unificar empresas; solo para personas jurídicas.", "String", "0..1 opcional",
  "Formato por país.", "20100047218", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo con el número.", "Extraer solo si la parte es persona jurídica; prohibido para personas naturales.",
  "Patrón y dígito verificador por país; coherente con persona_clase = persona_juridica_privada.",
  "Personas jurídicas privadas.", "P2", "A", "No", "Ninguna", "MDJ-D13-031", "F10; F12", "E3", "R2",
  country_status="Catálogo por país", pending="DEC-33")

# =====================================================================================
# D14 — PROCEDIMIENTO Y ESTADO PROCESAL
# =====================================================================================
PROC_APL = "Jurisprudencia y actos administrativos que forman parte de un proceso o procedimiento."

F("MDJ-D14-001", "id_proceso", "Identificador del proceso", "D14", "JUR; ADM", "Proceso",
  "Identificador persistente del expediente judicial o procedimiento administrativo que agrupa varias obras.",
  "Permite reconstruir la cadena de instancias y el resultado final del caso.", "Identificador", "1 obligatorio",
  NA_SYS, "PRC-5512", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Se crea al identificar un expediente en E3 y se consolida en E7.", "Único; un proceso por expediente y órgano de origen.",
  PROC_APL, "P0", "A", "No", "Ninguna", "MDJ-D14-002", "F07; F11; F12", "Sistema", "R3")

F("MDJ-D14-002", "proceso_numero_expediente_literal", "Número de expediente (literal)", "D14", "JUR; ADM", "Proceso",
  "Número de expediente, rol, radicado o causa tal como aparece en la resolución.",
  "Hecho primario para agrupar resoluciones del mismo caso; no se puede reconstruir sin releer.", "String", "1..n",
  "Texto transcrito.", "03456-2019-0-1801-JR-LA-01", "Explícito en documento", "Extracción directa",
  "Encabezado o sumilla.", "Transcribir cada número de expediente o radicación que figure (puede haber varios por instancia).",
  "Coincidencia literal.", PROC_APL, "P0", "A", "No", "Ninguna", "MDJ-D14-001", "F03; F07; F11", "E3", "R1",
  country_status="Catálogo por país")

F("MDJ-D14-003", "proceso_numero_expediente_normalizado", "Número de expediente normalizado", "D14", "JUR; ADM", "Proceso",
  "Forma normalizada del número de expediente según el patrón del país y órgano, usada para agrupar.",
  "Variantes de formato impiden reconocer el mismo proceso entre instancias.", "String", "0..1 opcional",
  "Patrón por país y órgano.", "03456-2019-1801-JR-LA", "Normalizado por regla", "Normalización",
  "Regla de normalización aplicada.", "Aplicar el patrón del país (eliminar espacios, unificar separadores y ceros).",
  "Debe ajustarse al patrón; si no hay patrón validado, 'indeterminado'.", PROC_APL, "P1", "B", "No", "Ninguna",
  "MDJ-D14-002", "F07; F11", "E7", "R2", country_status="Pendiente validación nacional")

F("MDJ-D14-004", "proceso_tipo", "Tipo de proceso", "D14", "JUR; ADM", "Proceso",
  "Clase del proceso: judicial, procedimiento administrativo, arbitral o de conciliación.",
  "Determina perfiles y relaciones aplicables.", "Enum", "1 obligatorio", "CAT-426 Tipo de proceso", "judicial",
  "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Se deriva de la naturaleza jurídica de las obras del proceso.", PROC_APL, "P0", "B", "No", "Ninguna",
  "Naturaleza jurídica (D04)", "F07", "E7", "R3", pending="DEC-07")

F("MDJ-D14-005", "proceso_organo_origen", "Órgano o entidad de origen del proceso", "D14", "JUR; ADM", "Proceso",
  "Órgano jurisdiccional o entidad administrativa ante la cual se inició el proceso.",
  "Parte de la identidad del proceso y punto de partida de la cadena de instancias.", "Referencia", "0..1 opcional",
  "Referencia a Entidad: organismo u órgano.", "ORG-…-JUZGADO-LAB-1", "Explícito en documento",
  "Extracción directa + Normalización", "Antecedentes.", "Extraer el órgano de primera instancia o entidad de inicio mencionado en antecedentes.",
  "Normalización con candidato único.", PROC_APL, "P1", "A", "No", "Ninguna", "MDJ-D14-001", "F07", "E3", "R2")

F("MDJ-D14-006", "proceso_fuero", "Fuero o jurisdicción procesal", "D14", "JUR; ADM", "Proceso",
  "Rama jurisdiccional en la que se tramita: ordinaria, contencioso administrativa, constitucional, especial (penal militar, electoral, JEP, indígena, etc.) o vía administrativa.",
  "Varios países tienen jurisdicciones separadas; el fuero condiciona fuerza y vías.", "Enum", "1 obligatorio",
  "CAT-416 Fuero o jurisdicción procesal", "contencioso_administrativa", "Normalizado por regla", "Normalización",
  "Órgano emisor.", "Derivar del órgano emisor normalizado y de la vía; confirmar con el texto si es ambiguo.",
  "Valor del catálogo; compatible con el órgano.", PROC_APL, "P1", "A", "No", "Ninguna",
  "MDJ-D14-005; órgano emisor (D02)", "F03; F07", "E3", "R2", country_status="Catálogo por país")

F("MDJ-D14-007", "proceso_via_procesal_original", "Vía procesal (denominación original)", "D14", "JUR; ADM", "Proceso",
  "Nombre del proceso o vía según el ordenamiento del país (proceso de amparo, acción de tutela, recurso de protección, juicio de amparo indirecto, proceso contencioso administrativo, proceso abreviado laboral).",
  "Conserva la institución original sin forzar equivalencias.", "String", "1 obligatorio",
  "Texto transcrito; se normaliza contra el catálogo de vías por país.", "proceso de amparo", "Explícito en documento",
  "Extracción directa", "Sumilla, encabezado o antecedentes.", "Transcribir la denominación de la vía tal como la usa el documento.",
  "Coincidencia literal; mapeo al catálogo nacional o 'no catalogado'.", PROC_APL, "P0", "A", "No", "Ninguna",
  "MDJ-D14-001", "F03; F07; F09", "E3", "R2", country_status="Catálogo por país", pending="DEC-14")

F("MDJ-D14-008", "proceso_via_funcion_pivote", "Función pivote de la vía", "D14", "JUR; ADM", "Proceso",
  "Función común de la vía procesal: proceso ordinario de conocimiento, proceso sumario, garantía jurisdiccional de derechos, control abstracto, control de legalidad, ejecución, cautelar, penal, procedimiento administrativo.",
  "Permite comparar entre países sin afirmar equivalencia jurídica.", "Enum", "1 obligatorio",
  "CAT-413 Función pivote de la vía procesal", "garantia_jurisdiccional_derechos", "Normalizado por regla",
  "Normalización", "Mapeo vía original → pivote del catálogo.", "Aplicar la tabla de correspondencias por país (semejanza funcional).",
  "Mapeo existente y validado; si no, 'pendiente'.", PROC_APL, "P1", "B", "No", "Ninguna", "MDJ-D14-007",
  "F09; F07", "E7", "R2", country_status="Pendiente validación nacional", pending="DEC-14")

F("MDJ-D14-009", "proceso_materia_procesal", "Materia procesal declarada", "D14", "JUR; ADM", "Proceso",
  "Materia o especialidad de la causa según la organización judicial o administrativa (civil, penal, laboral, familia, contencioso administrativo, tributario, comercial, constitucional), como la declara el documento o el órgano.",
  "Dato organizativo distinto de la clasificación temática (D06): refleja el fuero y la especialidad del órgano.",
  "Enum", "0..1 opcional", "CAT-417 Materia procesal", "laboral", "Explícito en documento",
  "Extracción directa + Normalización", "Encabezado (\"materia:\") o especialidad del órgano.",
  "Extraer el rótulo de materia del encabezado si existe; si no, derivar de la especialidad del órgano marcando normalizado.",
  "Valor del catálogo.", PROC_APL, "P1", "A", "No", "Ninguna", "MDJ-D14-005", "F01; F03; F07", "E3", "R2",
  country_status="Catálogo por país",
  obs="No reemplaza la clasificación por facetas; un proceso laboral puede tener principal constitucional.")

F("MDJ-D14-010", "resolucion_instancia", "Instancia de la resolución", "D14", "JUR; ADM", "Obra",
  "Nivel de conocimiento en que se dicta la resolución: única, primera, segunda/apelación, casación o revisión extraordinaria, constitucional, administrativa de primera instancia, de reconsideración/apelación administrativa.",
  "Imprescindible para ordenar la cadena procesal y para la fuerza del pronunciamiento.", "Enum", "1 obligatorio",
  "CAT-414 Instancia", "casacion", "Normalizado por regla", "Extracción directa + Normalización",
  "Encabezado o tipo de recurso resuelto.", "Determinar por el órgano y el recurso resuelto; registrar la denominación original en la afirmación.",
  "Compatible con el órgano y con el recurso resuelto.", PROC_APL, "P0", "A", "No", "Ninguna",
  "Órgano emisor (D02); MDJ-D14-015", "F03; F07; F08", "E3", "R2", country_status="Catálogo por país")

F("MDJ-D14-011", "resolucion_etapa_procesal", "Etapa procesal de la resolución", "D14", "JUR; ADM", "Obra",
  "Momento del proceso en que se dicta: admisión, cautelar, saneamiento, fondo, impugnación, ejecución, incidente, archivo.",
  "Distingue decisiones de fondo de autos de trámite o incidentales.", "Enum", "0..1 opcional",
  "CAT-418 Etapa procesal", "fondo", "Inferido por modelo", "Clasificación", "Parte resolutiva y objeto de la resolución.",
  "Clasificar por lo que decide la parte resolutiva (admite, concede medida, resuelve fondo, ejecuta).",
  "Valor del catálogo con evidencia en parte resolutiva.", PROC_APL, "P1", "A", "No", "Ninguna",
  "Parte resolutiva (D05)", "F07", "E3", "R2")

F("MDJ-D14-012", "pretensiones_planteadas", "Pretensiones planteadas", "D14", "JUR; ADM", "Obra",
  "Lista de pretensiones o petitorios de las partes que la resolución identifica como materia de decisión.",
  "Base para medir qué se pidió frente a qué se concedió y para análisis por tipo de demanda.", "Array",
  "0..n", "Objetos {texto literal, parte que la formula (rol), tipo normalizado}.",
  "[{\"se declare nulo el despido y se ordene la reposición\", demandante, nulidad_y_reposicion}]",
  "Explícito en documento", "Extracción directa", "Antecedentes o sección de petitorio.",
  "Transcribir cada pretensión tal como la resume la resolución; no reconstruir pretensiones no enunciadas.",
  "Cada pretensión con evidencia; el rol debe existir entre las partes.", PROC_APL, "P1", "A", "No",
  "Puede contener datos personales", "MDJ-D13-003", "F07; F14", "E3", "R2")

F("MDJ-D14-013", "pretension_tipo", "Tipo de pretensión", "D14", "JUR; ADM", "Obra",
  "Clasificación normalizada de cada pretensión: nulidad, indemnización, pago de suma, reposición, declarativa, constitutiva, cumplimiento, cautelar, protección de derecho fundamental, revisión de sanción, etc.",
  "Permite comparar resultados por tipo de pretensión.", "Enum múltiple", "0..n", "CAT-419 Tipo de pretensión",
  "[nulidad, reposicion]", "Inferido por modelo", "Clasificación", "Texto de la pretensión.",
  "Clasificar cada pretensión de MDJ-D14-012.", "Valores del catálogo.", PROC_APL, "P2", "C", "No", "Ninguna",
  "MDJ-D14-012", "F07; F14", "Posterior (C)", "R2")

F("MDJ-D14-014", "recurso_interpuesto_original", "Recurso o medio impugnatorio resuelto (denominación original)", "D14", "JUR; ADM", "Obra",
  "Nombre del recurso que la resolución resuelve (apelación, casación, nulidad, reconsideración, queja, revisión, recurso extraordinario).",
  "Hecho primario de la cadena procesal.", "String", "0..1 obligatorio condicionado", "Texto transcrito.",
  "recurso de casación", "Explícito en documento", "Extracción directa", "Encabezado o parte resolutiva.",
  "Transcribir el recurso resuelto; si la resolución no resuelve recurso, 'no aplica'.",
  "Obligatorio si la instancia es de revisión.", PROC_APL, "P0", "A", "No", "Ninguna", "MDJ-D14-010",
  "F07; F11", "E3", "R2", country_status="Catálogo por país")

F("MDJ-D14-015", "recurso_interpuesto_funcion", "Función del recurso resuelto", "D14", "JUR; ADM", "Obra",
  "Función común del recurso: impugnación ordinaria, impugnación extraordinaria, impugnación de legalidad, revisión constitucional, impugnación administrativa, queja.",
  "Comparación entre países y ordenación de la cadena procesal.", "Enum", "0..1 obligatorio condicionado",
  "CAT-420 Función del recurso", "impugnacion_extraordinaria", "Normalizado por regla", "Normalización",
  "Mapeo recurso original → función.", "Aplicar la tabla de correspondencias por país.",
  "Mapeo existente; si no, 'pendiente'.", PROC_APL, "P1", "B", "No", "Ninguna", "MDJ-D14-014", "F07; F09", "E7",
  "R2", country_status="Pendiente validación nacional", pending="DEC-14")

F("MDJ-D14-016", "recurso_interpuesto_por", "Parte que interpone el recurso", "D14", "JUR; ADM", "Obra",
  "Rol de la parte que interpuso el recurso resuelto.", "Necesario para saber quién gana o pierde en cada instancia.",
  "Enum", "0..1 obligatorio condicionado", "CAT-410 Rol procesal", "demandado", "Explícito en documento",
  "Extracción directa + Normalización", "Tramo que identifica al recurrente.", "Extraer el rol (no el nombre) del recurrente.",
  "Debe corresponder a una parte registrada.", PROC_APL, "P1", "A", "No", "Ninguna", "MDJ-D13-004", "F07; F14", "E3", "R1")

F("MDJ-D14-017", "resolucion_impugnada", "Resolución o acto impugnado", "D14", "JUR; ADM", "Obra",
  "Referencia a la resolución judicial o acto administrativo que es objeto del recurso o de la demanda que se resuelve.",
  "Eslabón de la cadena procesal: permite saber qué resolución se confirma, revoca o anula.", "Referencia",
  "0..1 obligatorio condicionado", "Referencia a Referencia (marcada como acto impugnado, MDJ-D07-027).", "REF-…",
  "Explícito en documento", "Extracción directa", "Antecedentes o parte resolutiva.",
  "Vincular a la referencia con MDJ-D07-027 = true.", "Obligatorio si la resolución resuelve un recurso o demanda contra un acto.",
  PROC_APL, "P0", "A", "No", "Ninguna", "MDJ-D07-027", "F07; F11; F12", "E3", "R1")

F("MDJ-D14-018", "sentido_fallo_literal", "Fórmula literal del fallo", "D14", "JUR; ADM", "Obra",
  "Fórmula decisoria principal tal como aparece en la parte resolutiva (\"Declarar FUNDADO…\", \"CASARON…\", \"Se confirma…\").",
  "Hecho primario no reconstruible; base del sentido normalizado y de las relaciones procesales.", "Texto largo",
  "0..1 obligatorio condicionado", "Texto transcrito.", "Declararon FUNDADO el recurso de casación…",
  "Explícito en documento", "Extracción directa", "Parte resolutiva.",
  "Transcribir el verbo decisorio y su objeto de cada punto resolutivo principal; si hay varios puntos, ver MDJ-D14-020.",
  "Debe estar en la sección parte resolutiva.", PROC_APL, "P0", "A", "No", "Puede contener datos personales",
  "Parte resolutiva delimitada (D05)", "F07; F08; F14", "E3", "R1")

F("MDJ-D14-019", "sentido_fallo_normalizado", "Sentido normalizado del fallo", "D14", "JUR; ADM", "Obra",
  "Resultado principal normalizado de la resolución: fundado, infundado, fundado en parte, improcedente, inadmisible, confirma, revoca, anula, casa, no casa, archiva, sanciona, absuelve, etc.",
  "Permite estadística de resultados y la cadena procesal.", "Enum", "0..1 obligatorio condicionado",
  "CAT-415 Sentido del fallo", "fundado", "Normalizado por regla", "Normalización + Clasificación",
  "Fórmula literal del fallo.", "Mapear el verbo decisorio literal al catálogo; si hay varios puntos con resultados distintos → 'mixto' y detalle por punto.",
  "Valor del catálogo coherente con la fórmula literal.", PROC_APL, "P1", "A", "Condicionado", "Ninguna",
  "MDJ-D14-018", "F07; F08; F14", "E3", "R1", country_status="Catálogo por país",
  obs="Revisión humana cuando se usa para el resultado final del proceso o contingencias.")

F("MDJ-D14-020", "sentido_fallo_por_punto", "Sentido por punto resolutivo", "D14", "JUR; ADM", "Unidad estructural",
  "Resultado normalizado de cada punto resolutivo (cada punto es una unidad estructural de la parte resolutiva).",
  "Las resoluciones confirman un extremo y revocan otro; el resultado global oculta esa diferencia.", "Enum",
  "1 obligatorio", "CAT-415 Sentido del fallo", "revoca", "Normalizado por regla", "Extracción directa + Normalización",
  "Texto del punto resolutivo.", "Para cada punto resolutivo, mapear su verbo decisorio.", "Valor del catálogo con evidencia en el punto.",
  "Puntos resolutivos de jurisprudencia y actos.", "P1", "A", "No", "Ninguna", "Segmentación de parte resolutiva (D05)",
  "F07; F14", "E3", "R1")

F("MDJ-D14-021", "resolucion_punto_resolutivo_objeto", "Objeto del punto resolutivo", "D14", "JUR; ADM", "Unidad estructural",
  "Extremo o pretensión a que se refiere cada punto resolutivo (p. ej., 'pago de horas extras', 'multa', 'reposición').",
  "Relaciona resultado y pretensión; insumo de contingencias.", "String", "0..1 opcional", "Texto transcrito breve.",
  "extremo referido a la indemnización por despido", "Explícito en documento", "Extracción directa", "Texto del punto resolutivo.",
  "Transcribir la expresión que delimita el extremo decidido.", "Debe estar contenido en el punto.",
  "Puntos resolutivos.", "P1", "A", "No", "Ninguna", "MDJ-D14-020", "F07; F14", "E3", "R2")

F("MDJ-D14-022", "resolucion_votacion", "Resultado de la votación", "D14", "JUR; ADM", "Obra",
  "Forma de adopción de la decisión en colegiados: unanimidad, mayoría y, si consta, el conteo.",
  "Hecho primario para reglas de precedente que exigen votación calificada y para medir consenso.", "Objeto",
  "0..1 opcional", "{modalidad: unanimidad|mayoria|no_indicada, votos_a_favor, votos_en_contra}",
  "{mayoria, 4, 1}", "Explícito en documento", "Extracción directa + Normalización",
  "Mención de votación o firmas y votos separados.", "Extraer la modalidad expresa (\"por unanimidad\", \"por mayoría\") y el conteo si aparece; no deducir conteos de las firmas sin regla.",
  "Coherente con los votos separados registrados.", "Resoluciones colegiadas.", "P1", "A", "No", "Ninguna",
  "MDJ-D13-019", "F07; F08", "E3", "R2", pending="DEC-25")

F("MDJ-D14-023", "resolucion_tiene_votos_separados", "Existencia de votos separados", "D14", "JUR; ADM", "Obra",
  "Indica si la resolución incluye votos singulares, disidentes, salvamentos o aclaraciones.",
  "Señal de controversia y requisito para no atribuir a la mayoría lo que dice un voto.", "Boolean", "1 obligatorio",
  "true/false", "true", "Explícito en documento", "Extracción directa", "Rótulo de la sección de voto.",
  "true si la segmentación identifica alguna sección de voto separado.", "Coherente con D05.", "Resoluciones colegiadas.",
  "P0", "A", "No", "Ninguna", "Segmentación E2", "F07; F08", "E2", "R2")

F("MDJ-D14-024", "resolucion_firmeza_declarada", "Firmeza declarada en el documento", "D14", "JUR; ADM", "Obra",
  "Indica si el documento declara que la resolución quedó firme, consentida, ejecutoriada o que agota la vía.",
  "Hecho primario para calcular el estado de firmeza.", "Boolean", "0..1 opcional", "true/false", "true",
  "Explícito en documento", "Extracción directa", "Tramo con la declaración.", "Marcar true solo con declaración expresa.",
  "Si true, evidencia literal.", PROC_APL, "P1", "A", "No", "Ninguna", "Ninguna", "F07; F14", "E3", "R1")

F("MDJ-D14-025", "resolucion_estado_firmeza", "Estado de firmeza calculado", "D14", "JUR; ADM", "Obra",
  "Conclusión sobre si la resolución está firme, impugnada, revocada o anulada, o si no puede determinarse con el corpus disponible.",
  "Evita presentar como definitiva una resolución revocada; sin el corpus completo, se informa la incertidumbre.",
  "Enum", "1 obligatorio", "CAT-429 Estado de firmeza", "revocada", "Conclusión jurídica por reglas", "Cálculo",
  NA_EVID_CALC, NA_EX_CALC,
  "Reglas: revocada/anulada si existe relación activa revoca/anula hacia ella; firme si firmeza declarada o resolución de última instancia sin recurso posterior conocido marcando 'según corpus'; en otro caso 'no determinable'.",
  PROC_APL, "P1", "B", "Condicionado", "Ninguna", "MDJ-D14-024; relaciones de cadena procesal",
  "F07; F08; F14", "E7", "R1", country_status="Pendiente validación nacional", pending="DEC-17",
  obs="Valor con fecha de corte; nunca se presenta como certeza si proviene de ausencia de información.")

F("MDJ-D14-026", "adm_agota_via_administrativa", "Agotamiento de la vía administrativa", "D14", "ADM", "Obra",
  "Indica si el acto declara que con él se agota la vía administrativa.",
  "Determina la posibilidad de impugnación judicial y la firmeza administrativa.", "Boolean", "0..1 opcional",
  "true/false", "true", "Explícito en documento", "Extracción directa", "Tramo con la declaración.",
  "Marcar true solo con declaración expresa (\"da por agotada la vía administrativa\").", "Evidencia literal si true.",
  "Actos administrativos.", "P1", "A", "No", "Ninguna", "Ninguna", "F07; F11", "E3", "R1",
  country_status="Catálogo por país")

F("MDJ-D14-027", "recursos_indicados", "Recursos y plazos indicados en la resolución", "D14", "JUR; ADM", "Obra",
  "Recursos que la resolución informa que proceden contra ella, con plazo y órgano ante el que se interponen.",
  "Información práctica para el usuario y para el cálculo de firmeza.", "Array", "0..n",
  "Objetos {recurso (texto), plazo (número), unidad (días hábiles/calendario/meses), órgano}.",
  "[{reconsideración, 15, días hábiles, la misma entidad}]", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo con la indicación de recursos.", "Transcribir solo recursos y plazos expresamente indicados; no completar con la ley.",
  "Plazo > 0; unidad del catálogo.", "Actos administrativos y resoluciones judiciales que indican recursos.", "P2", "A",
  "No", "Ninguna", "Ninguna", "F02; F07", "E3", "R2")

F("MDJ-D14-028", "procedimiento_administrativo_tipo", "Tipo de procedimiento administrativo", "D14", "ADM", "Proceso",
  "Clase del procedimiento administrativo: sancionador, de fiscalización, trilateral, reclamación o queja, recursivo, de autorización o licencia, de contratación pública, consulta, de oficio, otro.",
  "Organiza el análisis de actos por tipo de procedimiento.", "Enum", "1 obligatorio",
  "CAT-421 Tipo de procedimiento administrativo", "sancionador", "Inferido por modelo", "Clasificación",
  "Objeto y antecedentes del acto.", "Clasificar por el objeto declarado (imposición de sanción, otorgamiento de licencia, resolución de reclamo).",
  "Valor del catálogo con evidencia.", "Actos administrativos.", "P1", "A", "No", "Ninguna",
  "Naturaleza jurídica (D04)", "F03; F07; F13", "E3", "R2", country_status="Catálogo por país")

F("MDJ-D14-029", "procedimiento_denominacion_original", "Denominación original del procedimiento", "D14", "ADM", "Proceso",
  "Nombre del procedimiento según la norma o la entidad (procedimiento administrativo sancionador, procedimiento trilateral, procedimiento de reclamación tributaria).",
  "Conserva la institución nacional sin forzar equivalencias.", "String", "0..1 opcional", "Texto transcrito.",
  "procedimiento de reclamación tributaria", "Explícito en documento", "Extracción directa", "Tramo con la denominación.",
  "Transcribir la denominación del procedimiento si se menciona.", "Coincidencia literal.", "Actos administrativos.",
  "P2", "A", "No", "Ninguna", "MDJ-D14-028", "F09", "E3", "R3", country_status="Catálogo por país")

F("MDJ-D14-030", "proceso_fecha_inicio", "Fecha de inicio del proceso", "D14", "JUR; ADM", "Proceso",
  "Fecha de presentación de la demanda, denuncia, solicitud o inicio de oficio, si se menciona.",
  "Permite medir duración de procesos y ordenar cronologías.", "Fecha parcial", "0..1 opcional", "ISO 8601.",
  "2019-03-11", "Explícito en documento", "Extracción directa + Normalización", "Antecedentes.",
  "Extraer la fecha de inicio expresa; no deducirla del número de expediente.", "≤ fecha de la resolución.",
  PROC_APL, "P2", "A", "No", "Ninguna", "MDJ-D14-001", "F07", "E3", "R2")

F("MDJ-D14-031", "proceso_duracion_dias", "Duración del proceso hasta la resolución", "D14", "JUR; ADM", "Proceso",
  "Días entre el inicio del proceso y la última resolución conocida.", "Análisis de tiempos de resolución.",
  "Integer", "0..1 opcional", "Entero ≥ 0.", "1430", "Derivado por cálculo", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Solo si existen ambas fechas; se marca 'según corpus'.", PROC_APL, "P3", "B", "No", "Ninguna",
  "MDJ-D14-030; fechas de resoluciones (D03)", "F07", "E7", "R3")

F("MDJ-D14-032", "proceso_resultado_final", "Resultado final del proceso", "D14", "JUR; ADM", "Proceso",
  "Conclusión sobre el resultado del caso a partir de la cadena de resoluciones conocidas: favorable al demandante/administrado, desfavorable, parcial, pendiente o no determinable.",
  "Una sola resolución puede no reflejar el resultado del caso (revocaciones posteriores).", "Enum", "1 obligatorio",
  "CAT-415 Sentido del fallo (subconjunto de resultado final)", "parcialmente_favorable_demandante",
  "Conclusión jurídica por reglas", "Cálculo", NA_EVID_CALC, NA_EX_CALC,
  "Regla sobre la última resolución firme o la última conocida de la cadena; con fecha de corte y marca 'según corpus'.",
  PROC_APL, "P2", "B", "Condicionado", "Ninguna", "MDJ-D14-019; MDJ-D14-025; relaciones procesales",
  "F07; F14", "E7", "R1", pending="DEC-17")

F("MDJ-D14-033", "proceso_resolucion_final", "Resolución final conocida", "D14", "JUR; ADM", "Proceso",
  "Referencia a la última resolución de la cadena procesal conocida en el corpus.", "Punto de entrada para mostrar el estado actual del caso.",
  "Referencia", "0..1 opcional", "Referencia a Obra.", "OB-… (Casación 1234-2021)", "Derivado por cálculo", "Cálculo",
  NA_EVID_CALC, NA_EX_CALC, "Ordenar resoluciones del proceso por instancia y fecha.", PROC_APL, "P2", "B", "No",
  "Ninguna", "MDJ-D14-010; fechas (D03)", "F07; F11", "E7", "R2")

F("MDJ-D14-034", "resolucion_medida_cautelar", "Decisión sobre medida cautelar", "D14", "JUR; ADM", "Obra",
  "Indica si la resolución concede, deniega, modifica o levanta una medida cautelar o provisional.",
  "Distingue decisiones provisionales de decisiones de fondo.", "Enum", "0..1 opcional",
  "concede | deniega | modifica | levanta | no_aplica", "concede", "Explícito en documento",
  "Extracción directa + Normalización", "Parte resolutiva.", "Mapear la fórmula resolutiva sobre la medida.",
  "Evidencia en parte resolutiva.", PROC_APL, "P2", "A", "No", "Ninguna", "MDJ-D14-018", "F07", "E3", "R2")

F("MDJ-D14-035", "proceso_institucion_arbitral", "Institución administradora del arbitraje", "D14", "JUR", "Proceso",
  "Centro o institución que administra el arbitraje y reglamento aplicado, para laudos.",
  "Contexto necesario si se incorporan laudos (repositorios mapeados para Bolivia).", "Objeto", "0..1 obligatorio condicionado",
  "{institucion (Entidad: organismo u órgano), reglamento (texto)}", "{CIADI, Reglas de Arbitraje}",
  "Explícito en documento", "Extracción directa + Normalización", "Encabezado del laudo.",
  "Extraer la institución y el reglamento declarados.", "Solo si naturaleza = decisión arbitral.",
  "Laudos arbitrales (si se incorporan).", "P2", "A", "No", "Ninguna", "Naturaleza jurídica (D04)", "F07; F04", "E3",
  "R2", pending="DEC-07")

F("MDJ-D14-036", "resolucion_reenvio", "Ordena nuevo pronunciamiento", "D14", "JUR; ADM", "Obra",
  "Indica si la resolución anula y ordena al órgano inferior o a la entidad emitir un nuevo pronunciamiento.",
  "La cadena procesal continúa; el resultado no es definitivo.", "Boolean", "0..1 opcional", "true/false", "true",
  "Explícito en documento", "Extracción directa", "Parte resolutiva.", "true con fórmula expresa (\"ordena emitir nuevo pronunciamiento\", \"devuélvase\").",
  "Evidencia literal si true.", PROC_APL, "P1", "A", "No", "Ninguna", "MDJ-D14-018", "F07", "E3", "R2")


# =====================================================================================
# REL_TYPES — vocabulario de tipos de relación (CAT-406)
# =====================================================================================
REL_TYPES = []


def R(code, name, family, direction, inverse, origin_units, target_units, origin_mode, evidence, rule,
      prio, risk, feeds, symmetric, transitive, categories, notes="Sin notas."):
    REL_TYPES.append(dict(code=code, name=name, family=family, direction=direction, inverse=inverse,
                          origin_units=origin_units, target_units=target_units, origin_mode=origin_mode,
                          evidence=evidence, rule=rule, prio=prio, risk=risk, feeds=feeds,
                          symmetric=symmetric, transitive=transitive, categories=categories, notes=notes))


UE = "Unidad estructural"
UEO = "Obra; Unidad estructural"
ALLC = "NOR; JUR; ADM; DOC"

# --- Citación (no sustantivas)
R("cita_normativa", "Cita normativa", "citacion", "Unidad que menciona → norma o disposición mencionada", "citada_por",
  UE, "Obra; Versión; Unidad estructural", "Calculada", "Cadena literal de la referencia",
  "Se crea por cada referencia normativa resuelta. No implica aplicación ni interpretación.", "P0", "R3",
  "Métricas de citación", "No", "No", ALLC, "Proyección de la referencia al grafo; no es relación sustantiva.")
R("cita_jurisprudencial", "Cita jurisprudencial", "citacion", "Unidad que menciona → resolución mencionada", "citada_por",
  UE, "Obra; Unidad estructural", "Calculada", "Cadena literal", "Por cada referencia jurisprudencial resuelta.",
  "P0", "R3", "Métricas de citación", "No", "No", ALLC)
R("cita_acto_administrativo", "Cita de acto administrativo", "citacion", "Unidad que menciona → acto mencionado", "citado_por",
  UE, "Obra; Unidad estructural", "Calculada", "Cadena literal", "Por cada referencia a acto resuelta.", "P0", "R3",
  "Métricas de citación", "No", "No", ALLC)
R("cita_doctrinal", "Cita doctrinal", "citacion", "Unidad que menciona → obra doctrinal", "citada_por",
  UE, "Obra", "Calculada", "Cadena bibliográfica", "Solo si la referencia doctrinal se resuelve contra el corpus doctrinal.",
  "P1", "R3", "Métricas de influencia doctrinal", "No", "No", ALLC)
R("transcribe", "Referencia literal (transcribe)", "citacion", "Unidad que transcribe → unidad transcrita", "transcrita_en",
  "Fragmento textual", "Fragmento textual; Unidad estructural", "Calculada", "Límites de la cita textual y su atribución",
  "Se crea al verificar la transcripción; marca contenido ajeno. Nunca implica interpretar ni aplicar.", "P1", "R2",
  "Versión citada; exclusión de clasificación", "No", "No", ALLC)

# --- Operaciones normativas
R("modifica", "Modifica", "operacion_normativa", "Disposición modificatoria → disposición modificada", "es_modificada_por",
  UE, UE, "Transcrita", "Fórmula operativa (\"modifícase\", \"reformase\", \"queda redactado\") y destino",
  "Crea un nuevo fragmento textual del destino con el nuevo texto; fecha de efecto expresa o calculada.", "P0", "R1",
  "Vigencia; texto consolidado; línea de vida", "No", "No", "NOR; ADM",
  "Aplica a actos generales que modifican otros actos generales.")
R("sustituye_texto", "Sustituye el texto", "operacion_normativa", "Disposición → disposición cuyo texto se reemplaza íntegramente", "texto_sustituido_por",
  UE, UE, "Transcrita", "Fórmula \"sustitúyese\" y nuevo texto",
  "Misma unidad, nuevo fragmento; si sustituye un bloque con nueva numeración, ver continuidad (D05).", "P0", "R1",
  "Vigencia; texto consolidado; continuidad", "No", "No", "NOR; ADM")
R("incorpora", "Incorpora", "operacion_normativa", "Disposición → nueva unidad incorporada", "incorporada_por",
  UE, UE, "Transcrita", "Fórmula \"incorpórase\", \"adiciónase\" y rótulo nuevo",
  "Crea una unidad estructural nueva con ubicación declarada.", "P0", "R1", "Línea de vida; texto consolidado",
  "No", "No", "NOR; ADM")
R("deroga_expresamente", "Deroga expresamente", "operacion_normativa", "Disposición derogatoria → obra o unidad derogada", "derogada_expresamente_por",
  UE, UEO, "Transcrita", "Fórmula derogatoria con destino determinado",
  "Solo con destino identificado; las cláusulas genéricas no crean esta relación.", "P0", "R1", "Vigencia",
  "No", "No", "NOR; ADM")
R("derogacion_generica", "Cláusula derogatoria genérica", "operacion_normativa", "Disposición → (sin destino determinado)", "No aplica",
  UE, "No aplica", "Transcrita", "Fórmula \"derógase toda disposición que se oponga\"",
  "Se registra como evento sin destino; no cambia el estado de ninguna norma concreta.", "P0", "R1",
  "Ninguno (solo alerta)", "No", "No", "NOR; ADM",
  "Se modela como relación sin destino para conservar el hecho primario.")
R("posible_derogacion_tacita", "Posible derogación tácita", "tacita", "Norma posterior → norma posiblemente incompatible", "posiblemente_derogada_tacitamente_por",
  UE, UE, "Interpretada", "Ambos textos", "Solo alerta para revisión; nunca alimenta vigencia sin curaduría.",
  "Fuera de alcance", "R1", "Ninguno", "No", "No", "NOR",
  "Clase X como proceso masivo; puede crearse por curaduría.")
R("renumera", "Renumera", "operacion_normativa", "Disposición → unidad renumerada", "renumerada_por",
  UE, UE, "Transcrita", "Fórmula de renumeración con rótulo anterior y nuevo", "Misma unidad, nuevo rótulo.",
  "P0", "R1", "Línea de vida; resolución de citas", "No", "No", "NOR; ADM")
R("reubica", "Reubica", "operacion_normativa", "Disposición → unidad trasladada", "reubicada_por",
  UE, UE, "Transcrita", "Fórmula de traslado con nueva ruta", "Misma unidad, nueva ruta jerárquica.", "P0", "R2",
  "Línea de vida", "No", "No", "NOR; ADM")
R("suspende", "Suspende", "operacion_normativa", "Norma o resolución → unidad suspendida", "suspendida_por",
  "Unidad estructural; Obra", UEO, "Transcrita", "Fórmula de suspensión y plazo",
  "Cambia estado sin nuevo texto; fechas de inicio y fin.", "P0", "R1", "Vigencia", "No", "No", "NOR; JUR; ADM")
R("prorroga", "Prorroga", "operacion_normativa", "Disposición → plazo o vigencia prorrogada", "prorrogada_por",
  UE, UE, "Transcrita", "Fórmula de prórroga y nuevo plazo", "Extiende un plazo o vigencia temporal.", "P0", "R1",
  "Vigencia", "No", "No", "NOR; ADM")
R("rectifica", "Rectifica (fe de erratas)", "operacion_normativa", "Fe de erratas → unidad rectificada", "rectificada_por",
  "Obra; Unidad estructural", UE, "Transcrita", "Texto \"donde dice / debe decir\"",
  "Nuevo fragmento marcado como rectificación; fecha de efecto por regla de país.", "P0", "R1",
  "Texto consolidado; vigencia", "No", "No", "NOR; ADM", "DEC-34.")
R("restablece", "Restablece vigencia", "operacion_normativa", "Norma → unidad cuya vigencia se restablece expresamente", "restablecida_por",
  UE, UE, "Transcrita", "Fórmula expresa de restablecimiento",
  "Solo con fórmula expresa; la reviviscencia tácita no se presume.", "P0", "R1", "Vigencia", "No", "No", "NOR",
  "Reglas de reviviscencia por país: DEC-17.")
R("ordena_refunde", "Ordena o refunde", "operacion_normativa", "Texto ordenado/refundido → obra compilada", "ordenada_en",
  "Obra", "Obra", "Transcrita", "Declaración del acto compilador",
  "El texto ordenado es obra propia; sus unidades se vinculan por 'corresponde a'.", "P0", "R1",
  "Línea de vida; resolución de citas", "No", "No", "NOR", "Rango y efectos: DEC-04.")

# --- Desarrollo normativo
R("reglamenta", "Reglamenta", "desarrollo_normativo", "Norma reglamentaria → norma reglamentada", "reglamentada_por",
  UEO, UEO, "Transcrita", "Declaración expresa de reglamentar (\"reglaméntase\", \"aprueba el reglamento de\")",
  "Solo con declaración expresa; sin ella, puede ser candidata interpretada.", "P1", "R2",
  "Detección de normas pendientes de reglamentar", "No", "No", "NOR; ADM")
R("desarrolla", "Desarrolla", "desarrollo_normativo", "Norma → norma cuyo contenido desarrolla o complementa", "desarrollada_por",
  UEO, UEO, "Interpretada", "Pasaje que remite o complementa",
  "Exige remisión o declaración de desarrollo; no por similitud temática.", "P2", "R2", "Ninguno", "No", "No", "NOR; ADM")
R("delega", "Delega facultades", "desarrollo_normativo", "Ley autoritativa → norma dictada por delegación", "dictada_por_delegacion_de",
  UEO, "Obra", "Transcrita", "Mención de la ley autoritativa en la norma delegada",
  "La norma delegada declara la habilitación.", "P1", "R2", "Ninguno", "No", "No", "NOR")
R("transpone_aplica_comunitaria", "Desarrolla norma comunitaria", "desarrollo_normativo", "Norma nacional → norma comunitaria desarrollada", "desarrollada_nacionalmente_por",
  UEO, UEO, "Transcrita", "Declaración expresa", "Solo con declaración expresa.", "P2", "R2", "Ninguno", "No", "No", "NOR")

# --- Estructurales (continuidad; detalle de grados en D05)
R("corresponde_a", "Corresponde a", "estructural", "Unidad de una obra → unidad de otra obra con contenido correspondiente", "corresponde_a",
  UE, UE, "Transcrita", "Tabla de correspondencias o declaración expresa",
  "Entre obras distintas (texto ordenado y norma compilada). Por similitud solo como candidata.", "P0", "R2",
  "Resolución de citas; línea de vida", "Sí", "No", "NOR")
R("se_divide_en", "Se divide en", "estructural", "Unidad que se extingue → unidades sucesoras", "procede_de_division_de",
  UE, UE, "Transcrita", "Operaciones de la norma modificatoria o tabla",
  "Declarada, presunta o curada alimentan cálculos; inferida solo candidata.", "P0", "R1", "Línea de vida; vigencia",
  "No", "No", "NOR; ADM")
R("se_fusiona_en", "Se fusiona en", "estructural", "Unidades que se extinguen → unidad que las absorbe", "absorbe_a",
  UE, UE, "Transcrita", "Operaciones de la norma modificatoria", "Igual criterio que división.", "P0", "R1",
  "Línea de vida; vigencia", "No", "No", "NOR; ADM")
R("sustituida_por_unidad", "Es sustituida por (sin continuidad)", "estructural", "Unidad extinguida → unidad nueva que la reemplaza", "sustituye_a_unidad",
  UE, UE, "Transcrita", "Sustitución de bloque sin continuidad declarada ni presunta",
  "Cuando no hay continuidad de identidad.", "P0", "R1", "Línea de vida", "No", "No", "NOR; ADM")
R("deriva_de_unidad", "Deriva de (unidad)", "estructural", "Unidad nueva → unidad de la que toma contenido", "origina",
  UE, UE, "Transcrita", "Declaración o tabla; si por similitud, interpretada",
  "La unidad origen sigue existiendo.", "P1", "R2", "Línea de vida", "No", "No", "NOR; ADM")

# --- Control de validez
R("declara_inconstitucional", "Declara inconstitucional o inexequible", "control_validez", "Punto resolutivo → disposición", "declarada_inconstitucional_por",
  UE, UE, "Transcrita", "Punto resolutivo", "Efectos temporales y alcance por regla de país.", "P0", "R1", "Vigencia",
  "No", "No", "JUR", "DEC-17.")
R("declara_exequible", "Declara exequible o constitucional", "control_validez", "Punto resolutivo → disposición", "declarada_exequible_por",
  UE, UE, "Transcrita", "Punto resolutivo", "Puede tener efecto de cosa juzgada constitucional según país.", "P0", "R2",
  "Fuerza (D17)", "No", "No", "JUR")
R("declara_exequible_condicionada", "Declara exequible condicionadamente", "control_validez", "Punto resolutivo → disposición", "condicionada_por",
  UE, UE, "Transcrita", "Punto resolutivo con condición",
  "Registrar texto de la condición (MDJ-D07-062); fija lectura obligatoria sin cambiar texto.", "P0", "R1",
  "Vigencia (lectura obligatoria)", "No", "No", "JUR", "Figura propia de algunos ordenamientos; validar por país.")
R("declara_nula_ilegal", "Declara nula o ilegal (norma infralegal)", "control_validez", "Punto resolutivo → disposición reglamentaria", "declarada_nula_por",
  UE, UE, "Transcrita", "Punto resolutivo", "Control de legalidad de reglamentos.", "P0", "R1", "Vigencia", "No", "No", "JUR")
R("inaplica", "Inaplica (control difuso)", "control_validez", "Fundamento o punto resolutivo → disposición", "inaplicada_por",
  UE, UE, "Interpretada", "Pasaje que inaplica al caso",
  "Efecto en el caso; no afecta vigencia general.", "P2", "R1", "Ninguno", "No", "No", "JUR; ADM")

# --- Cadena procesal
R("confirma", "Confirma", "cadena_procesal", "Resolución → resolución o acto confirmado", "confirmada_por",
  "Obra; Unidad estructural", "Obra", "Transcrita", "Punto resolutivo", "Puede ser parcial (por extremo).", "P1", "R1",
  "Cadena procesal; firmeza; resultado final", "No", "No", "JUR; ADM")
R("revoca", "Revoca", "cadena_procesal", "Resolución → resolución o acto revocado", "revocada_por",
  "Obra; Unidad estructural", "Obra", "Transcrita", "Punto resolutivo", "Puede ser parcial.", "P1", "R1",
  "Cadena procesal; firmeza; resultado final", "No", "No", "JUR; ADM")
R("anula", "Anula o declara nula", "cadena_procesal", "Resolución → resolución o acto anulado", "anulada_por",
  "Obra; Unidad estructural", "Obra", "Transcrita", "Punto resolutivo", "Incluye nulidad de actos administrativos por jueces.",
  "P0", "R1", "Cadena procesal; firmeza; resultado final", "No", "No", "JUR; ADM")
R("casa", "Casa", "cadena_procesal", "Sentencia de casación → sentencia casada", "casada_por",
  "Obra", "Obra", "Transcrita", "Punto resolutivo", "Denominación varía por país.", "P1", "R1",
  "Cadena procesal; resultado final", "No", "No", "JUR")
R("no_casa", "No casa / declara infundada la casación", "cadena_procesal", "Sentencia de casación → sentencia recurrida", "no_casada_por",
  "Obra", "Obra", "Transcrita", "Punto resolutivo", "La recurrida queda firme según reglas.", "P1", "R1",
  "Cadena procesal; firmeza", "No", "No", "JUR")
R("declara_improcedente_recurso", "Declara improcedente o inadmisible", "cadena_procesal", "Resolución → recurso o resolución recurrida", "recurso_declarado_improcedente_por",
  "Obra", "Obra", "Transcrita", "Punto resolutivo", "No resuelve el fondo.", "P1", "R2", "Cadena procesal; firmeza",
  "No", "No", "JUR; ADM")
R("resuelve_recurso_contra", "Resuelve recurso contra", "cadena_procesal", "Resolución → resolución o acto impugnado", "recurrida_ante",
  "Obra", "Obra", "Transcrita", "Identificación del acto impugnado", "Base de la cadena; independiente del sentido.",
  "P0", "R2", "Cadena procesal", "No", "No", "JUR; ADM")
R("acumula", "Acumula", "cadena_procesal", "Proceso → proceso acumulado", "acumulado_a",
  "Proceso", "Proceso", "Transcrita", "Resolución de acumulación", "Solo con declaración expresa.", "P2", "R2",
  "Cadena procesal", "No", "No", "JUR; ADM")
R("pertenece_mismo_proceso", "Pertenece al mismo proceso", "cadena_procesal", "Resolución ↔ resolución del mismo expediente", "pertenece_mismo_proceso",
  "Obra", "Obra", "Calculada", "Número de expediente normalizado", "Se calcula por expediente y órgano de origen.",
  "P1", "R2", "Cadena procesal", "Sí", "Sí", "JUR; ADM")
R("reemplaza_resolucion", "Reemplaza (sentencia de reemplazo)", "cadena_procesal", "Resolución → resolución anulada a la que sustituye", "reemplazada_por",
  "Obra", "Obra", "Transcrita", "Declaración expresa", "Figura de algunos países; validar.", "P1", "R1",
  "Cadena procesal; resultado final", "No", "No", "JUR", "Pendiente validación nacional.")

# --- Uso normativo en la decisión
R("aplica", "Aplica", "uso_normativo", "Fundamento → disposición aplicada", "aplicada_en",
  UE, UE, "Interpretada", "Pasaje que subsume los hechos o usa la consecuencia jurídica",
  "Exige subsunción o uso de la consecuencia; mencionar no basta. Referencia con función 'fundamento decisivo'.",
  "P2", "R2", "Jurisprudencia por artículo", "No", "No", "JUR; ADM")
R("interpreta", "Interpreta", "uso_normativo", "Fundamento → disposición interpretada", "interpretada_en",
  UE, UE, "Interpretada", "Pasaje que fija sentido o alcance",
  "Exige que el fundamento fije el sentido; versión de destino = la vigente al origen.", "P2", "R2",
  "Jurisprudencia por artículo; advertencias de versión", "No", "No", "JUR; ADM; DOC")

# --- Uso de precedentes
R("invoca_precedente", "Invoca como precedente", "uso_precedentes", "Fundamento → resolución invocada como precedente", "invocada_como_precedente_en",
  UE, "Obra; Unidad estructural", "Transcrita", "Expresión de invocación", "Basado en MDJ-D07-021 = true.", "P1", "R1",
  "Carácter de precedente; red de precedentes", "No", "No", "JUR; ADM")
R("sigue", "Sigue el criterio", "uso_precedentes", "Fundamento → resolución cuyo criterio sigue", "seguida_por",
  UE, "Obra; Unidad estructural", "Interpretada", "Pasaje que adopta el criterio", "Requiere identificar el criterio (MDJ-D07-069).",
  "P2", "R2", "Líneas jurisprudenciales", "No", "No", "JUR; ADM")
R("reitera", "Reitera", "uso_precedentes", "Resolución → resolución con mismo criterio reiterado", "reiterada_por",
  UE, "Obra; Unidad estructural", "Interpretada", "Declaración de reiteración", "Relevante para jurisprudencia por reiteración.",
  "P2", "R1", "Carácter de precedente (reglas de país)", "No", "No", "JUR", "DEC-25.")
R("distingue", "Distingue", "uso_precedentes", "Fundamento → precedente que no aplica por diferencias", "distinguida_por",
  UE, "Obra; Unidad estructural", "Interpretada", "Pasaje que distingue", "Exige expresión de diferencia de supuestos.",
  "P2", "R2", "Líneas jurisprudenciales", "No", "No", "JUR; ADM")
R("se_aparta", "Se aparta del criterio", "uso_precedentes", "Fundamento → precedente del que se aparta", "apartada_por",
  UE, "Obra; Unidad estructural", "Interpretada", "Pasaje de apartamiento",
  "Siempre a revisión humana (R1); puede afectar vigencia del precedente.", "P2", "R1", "Carácter de precedente",
  "No", "No", "JUR; ADM")
R("unifica", "Unifica criterio", "uso_precedentes", "Resolución de unificación → resoluciones o criterios unificados", "unificada_por",
  "Obra", "Obra; Unidad estructural", "Transcrita", "Declaración de unificación", "Según mecanismo de cada país.", "P1", "R1",
  "Carácter de precedente", "No", "No", "JUR", "DEC-25.")
R("resuelve_contradiccion", "Resuelve contradicción de criterios", "uso_precedentes", "Resolución → resoluciones contradictorias", "contradiccion_resuelta_por",
  "Obra", "Obra", "Transcrita", "Declaración expresa", "Mecanismo propio de algunos países.", "P1", "R1",
  "Carácter de precedente", "No", "No", "JUR", "DEC-25.")
R("contradice", "Contradice", "uso_precedentes", "Resolución ↔ resolución con criterio contrario", "contradice",
  "Obra; Unidad estructural", "Obra; Unidad estructural", "Interpretada", "Ambos pasajes",
  "Solo candidata para revisión; no se infiere masivamente.", "P3", "R1", "Ninguno", "Sí", "No", "JUR; ADM")
R("supera_precedente", "Supera o modifica el precedente", "uso_precedentes", "Resolución → precedente superado", "superado_por",
  "Obra", "Obra; Unidad estructural", "Transcrita", "Declaración expresa", "Afecta la vigencia del precedente.", "P1", "R1",
  "Carácter de precedente", "No", "No", "JUR", "DEC-25.")
R("deriva_de_tesis", "Deriva de (tesis o sumilla oficial)", "uso_precedentes", "Tesis o criterio extractado → resolución de origen", "origina_tesis",
  "Obra", "Obra", "Transcrita", "Datos de precedente en la tesis", "La tesis es obra propia.", "P1", "R2",
  "Carácter de precedente", "No", "No", "JUR", "Particular de algunos países (p. ej., MX).")

# --- Doctrina
R("comenta", "Comenta", "doctrinal", "Obra doctrinal → documento comentado", "comentada_por",
  "Obra; Unidad estructural", "Obra; Unidad estructural", "Interpretada", "Sección que analiza el destino",
  "El destino debe ser objeto de análisis, no solo cita.", "P3", "R3", "Ninguno", "No", "No", "DOC")
R("critica", "Critica", "doctrinal", "Obra doctrinal → documento criticado", "criticada_por",
  "Obra; Unidad estructural", "Obra; Unidad estructural", "Interpretada", "Pasaje crítico", "Postura expresa.",
  "P3", "R3", "Ninguno", "No", "No", "DOC")
R("sistematiza", "Sistematiza", "doctrinal", "Obra → conjunto de resoluciones o normas sistematizadas", "sistematizada_por",
  "Obra", "Obra", "Interpretada", "Declaración de objeto", "Revistas jurisprudenciales y compilaciones.", "P3", "R3",
  "Ninguno", "No", "No", "DOC")
R("propone_reforma", "Propone reforma de", "doctrinal", "Obra doctrinal → norma cuya reforma propone", "reforma_propuesta_por",
  "Obra; Unidad estructural", UEO, "Interpretada", "Pasaje propositivo", "Postura expresa.", "P3", "R3", "Ninguno",
  "No", "No", "DOC")

# --- Aplicabilidad supranacional
R("aplica_en", "Aplica en (supranacional)", "aplicabilidad", "Norma o decisión supranacional → país", "recibe_aplicacion_de",
  "Obra", "Entidad: territorio o jurisdicción", "Curada", "Fuente de vinculación y fechas",
  "Curada por especialista; con intervalo de vigencia.", "P1", "R2", "Búsqueda por país", "No", "No", "NOR; JUR",
  "DEC-30.")

# --- Derivadas (inversas y agregadas)
R("inversa_calculada", "Inversa calculada", "derivada", "Destino → origen de una relación directa", "No aplica",
  "Cualquiera", "Cualquiera", "Calculada", "Hereda la de la relación directa",
  "Se genera para toda relación activa; hereda estado y no tiene revisión propia.", "P1", "R3", "Navegación del grafo",
  "No", "No", ALLC, "Nombre concreto según la columna 'inverse' del tipo directo.")
R("jurisprudencia_sobre", "Tiene jurisprudencia", "derivada", "Disposición → resoluciones que la aplican o interpretan", "No aplica",
  UE, "Obra", "Calculada", "Agregado de aplica/interpreta", "Agregación de relaciones activas.", "P2", "R2",
  "Jurisprudencia por artículo", "No", "No", "NOR")


# =====================================================================================
# CATÁLOGOS (CAT-400..CAT-499)
# =====================================================================================
def V(code, label, definition, parent="", synonyms="", country="ALL", notes="", status="Propuesto"):
    return dict(code=code, label=label, definition=definition, parent=parent, synonyms=synonyms,
                country=country, notes=notes, status=status)


CATALOGS = [
    dict(cat_id="CAT-401", cat_name="Tipo de referencia", cat_def="Clase del documento mencionado en una referencia.", values=[
        V("normativa", "Normativa", "Mención de una norma o de una disposición normativa."),
        V("jurisprudencial", "Jurisprudencial", "Mención de una resolución judicial, tesis o precedente."),
        V("acto_administrativo", "Acto administrativo", "Mención de un acto administrativo o pronunciamiento de entidad pública."),
        V("doctrinal", "Doctrinal o bibliográfica", "Mención de una obra doctrinal o fuente bibliográfica."),
        V("cita_textual", "Cita textual o transcripción", "Tramo transcrito atribuido a otro documento; genera además una referencia del tipo de su fuente."),
    ]),
    dict(cat_id="CAT-402", cat_name="Función de la referencia", cat_def="Papel de la mención en el razonamiento del documento de origen.", values=[
        V("base_legal_formal", "Base legal formal", "Enumeración de normas habilitantes o aplicables (vistos, base legal) sin uso argumentativo."),
        V("fundamento_decisivo", "Fundamento decisivo", "La mención sostiene la conclusión del fundamento o del punto resolutivo."),
        V("transcripcion", "Transcripción", "Se reproduce el texto del documento citado."),
        V("alegacion_parte", "Alegación de parte", "La mención forma parte de lo alegado por una parte y no de lo decidido."),
        V("contraste", "Contraste", "Se cita para diferenciar o descartar."),
        V("antecedente_historico", "Antecedente histórico", "Se menciona como antecedente normativo o jurisprudencial."),
        V("operacion_normativa", "Operación normativa", "La mención es el destino de una fórmula operativa (modifica, deroga, incorpora…)."),
        V("cita_de_autoridad", "Cita de autoridad", "Se invoca doctrina o jurisprudencia como respaldo sin aplicarla al caso."),
    ]),
    dict(cat_id="CAT-403", cat_name="Estado de resolución de la referencia", cat_def="Resultado de buscar el destino de una referencia en el corpus.", values=[
        V("resuelta_a_unidad", "Resuelta a unidad", "Destino identificado hasta la disposición o sección citada."),
        V("resuelta_a_obra", "Resuelta a obra", "Obra identificada; la cita no precisa unidad o la unidad no existe en esa versión."),
        V("ambigua", "Ambigua", "Varios candidatos; se conservan todos."),
        V("fuera_del_corpus", "Fuera del corpus", "Destino bien identificado pero ausente de la base."),
        V("no_identificable", "No identificable", "La mención no permite identificar el destino."),
        V("inconsistente_en_origen", "Inconsistente en origen", "La cita apunta a algo inexistente en cualquier versión (error del documento)."),
        V("pendiente", "Pendiente", "Aún no procesada."),
    ]),
    dict(cat_id="CAT-404", cat_name="Granularidad del destino", cat_def="Nivel al que se resolvió el destino de una referencia.", values=[
        V("obra", "Obra", "Resuelta al documento completo."),
        V("version", "Versión", "Resuelta a una versión concreta de la obra."),
        V("unidad_estructural", "Unidad estructural", "Resuelta a la disposición o sección citada."),
        V("subunidad", "Subunidad", "Resuelta a un nivel inferior al artículo (inciso, numeral, literal)."),
    ]),
    dict(cat_id="CAT-405", cat_name="Ubicación de la referencia", cat_def="Sección funcional del documento de origen donde aparece una mención o la evidencia de una relación.", values=[
        V("titulo_sumilla", "Título o sumilla", "Título, sumilla o encabezado del documento."),
        V("preambulo_vistos", "Preámbulo, vistos o base legal", "Sección introductoria que enumera la base normativa."),
        V("considerandos_exposicion", "Considerandos o exposición", "Motivación previa en normas y actos generales."),
        V("cuerpo_normativo", "Cuerpo normativo", "Articulado de una norma o acto general."),
        V("disposiciones_complementarias", "Disposiciones complementarias, transitorias o finales", "Disposiciones fuera del articulado principal."),
        V("antecedentes", "Antecedentes", "Relato del proceso o procedimiento."),
        V("hechos", "Hechos", "Hechos probados o relevantes."),
        V("alegaciones_parte", "Alegaciones de parte", "Resumen de posiciones de las partes."),
        V("fundamentos", "Fundamentos", "Fundamentos jurídicos del órgano."),
        V("parte_resolutiva", "Parte resolutiva", "Puntos resolutivos o fallo."),
        V("voto_separado", "Voto separado", "Voto singular, disidente, salvamento o aclaración."),
        V("nota_pie", "Nota al pie", "Nota al pie o al final."),
        V("bibliografia", "Bibliografía", "Lista de referencias bibliográficas."),
        V("anexo", "Anexo", "Anexo del documento."),
        V("cuerpo_doctrinal", "Cuerpo de la obra doctrinal", "Texto principal de la doctrina."),
    ]),
    dict(cat_id="CAT-406", cat_name="Tipo de relación", cat_def="Vocabulario cerrado de tipos de relación jurídica y documental; detalle en la hoja Relaciones y referencias.",
         values=[V(r["code"], r["name"], f"{r['direction']}. {r['rule']}", parent=r["family"],
                   notes=f"Inversa: {r['inverse']}. Modo: {r['origin_mode']}. Prioridad: {r['prio']}. Riesgo: {r['risk']}.")
                 for r in REL_TYPES]),
    dict(cat_id="CAT-407", cat_name="Modo de obtención de la relación", cat_def="Cómo se obtuvo una relación.", values=[
        V("transcrita", "Transcrita", "Obtenida de una fórmula expresa del documento (operativa o resolutiva)."),
        V("interpretada", "Interpretada", "Obtenida por análisis del modelo con evidencia del pasaje."),
        V("calculada", "Calculada", "Obtenida por regla a partir de otras afirmaciones."),
        V("curada", "Curada", "Fijada o confirmada por una persona."),
    ]),
    dict(cat_id="CAT-408", cat_name="Calificador de la relación", cat_def="Matiz jurídico del vínculo.", values=[
        V("total", "Total", "Afecta íntegramente al destino."),
        V("parcial", "Parcial", "Afecta un extremo o parte del destino."),
        V("condicionada", "Condicionada", "Sujeta a condición interpretativa o fáctica."),
        V("diferida", "Diferida", "Efectos a partir de una fecha posterior."),
        V("retroactiva", "Retroactiva", "Efectos anteriores a la emisión, declarados expresamente."),
        V("temporal", "Temporal", "Con plazo de fin."),
        V("en_voto_separado", "En voto separado", "Expresada solo en un voto separado."),
        V("presunta", "Presunta", "Establecida por regla de continuidad presunta (solo estructurales)."),
    ]),
    dict(cat_id="CAT-409", cat_name="Estado de la relación", cat_def="Situación de una relación en el grafo.", values=[
        V("activa", "Activa", "Validada para uso; alimenta cálculos si su tipo lo prevé."),
        V("candidata", "Candidata", "Destino no resuelto, confianza insuficiente o R1 sin revisión."),
        V("rechazada", "Rechazada", "Descartada por revisión o control."),
        V("revertida", "Revertida", "Dejada sin efecto por una relación posterior (p. ej., la anulación fue revocada)."),
        V("sustituida", "Sustituida", "Reemplazada por una relación corregida."),
    ]),
    dict(cat_id="CAT-410", cat_name="Rol procesal", cat_def="Posición de un interviniente en el proceso, procedimiento o recurso. La denominación original se conserva en la afirmación.", values=[
        V("demandante", "Demandante o accionante", "Quien inicia el proceso judicial.", synonyms="actor; accionante; demandante; solicitante"),
        V("demandado", "Demandado o accionado", "Contra quien se dirige la demanda.", synonyms="accionado; emplazado"),
        V("administrado", "Administrado", "Persona sujeta al procedimiento administrativo."),
        V("denunciante", "Denunciante o reclamante", "Quien denuncia o reclama ante la entidad."),
        V("denunciado", "Denunciado o investigado", "Persona investigada en procedimiento sancionador o penal."),
        V("imputado", "Imputado o procesado", "Persona procesada penalmente.", synonyms="acusado; procesado"),
        V("agraviado", "Agraviado o víctima", "Persona afectada por el hecho.", synonyms="víctima; ofendido"),
        V("tercero", "Tercero interviniente", "Tercero con interés que interviene."),
        V("ministerio_publico", "Ministerio Público o Fiscalía", "Órgano persecutor o dictaminador."),
        V("procuraduria", "Procuraduría o defensa del Estado", "Representación judicial del Estado."),
        V("defensoria", "Defensoría del Pueblo", "Interviniente institucional de defensa de derechos."),
        V("amicus", "Amicus curiae", "Tercero que aporta opinión."),
        V("recurrente", "Recurrente", "Quien interpone el recurso que se resuelve.", parent="recursal"),
        V("recurrido", "Recurrido", "Parte contraria en el recurso.", parent="recursal"),
        V("apelante", "Apelante", "Quien apela.", parent="recursal"),
        V("apelado", "Apelado", "Parte contraria en apelación.", parent="recursal"),
        V("adherido", "Adherido", "Quien se adhiere a un recurso.", parent="recursal"),
        V("autoridad_demandada", "Autoridad o entidad demandada", "Entidad pública demandada en procesos contra la administración."),
        V("otro", "Otro", "Rol no catalogado; se conserva la denominación original."),
    ]),
    dict(cat_id="CAT-411", cat_name="Tipo de parte", cat_def="Naturaleza del interviniente.", values=[
        V("persona_natural", "Persona natural", "Individuo identificado por nombre."),
        V("persona_juridica_privada", "Persona jurídica privada", "Sociedad, asociación, fundación u otra persona jurídica de derecho privado."),
        V("entidad_publica", "Entidad pública", "Órgano u organismo del Estado o empresa pública."),
        V("colectivo_comunidad", "Colectivo o comunidad", "Comunidad, pueblo, sindicato u otro colectivo."),
        V("anonimizada", "Anonimizada", "Identidad ocultada en la fuente."),
        V("no_determinable", "No determinable", "No es posible determinar el tipo."),
    ]),
    dict(cat_id="CAT-412", cat_name="Rol del actor institucional", cat_def="Función de un servidor público en el documento.", values=[
        V("magistrado_ponente", "Magistrado o vocal ponente", "Redactor de la ponencia."),
        V("integrante_colegiado", "Integrante del colegiado", "Miembro que suscribe la decisión."),
        V("juez_unipersonal", "Juez unipersonal", "Juez que resuelve en órgano unipersonal."),
        V("secretario", "Secretario o relator", "Fedatario del órgano."),
        V("funcionario_emisor", "Funcionario emisor", "Autoridad que suscribe el acto."),
        V("refrendante", "Refrendante", "Autoridad que refrenda una norma."),
        V("arbitro", "Árbitro", "Integrante de un tribunal arbitral."),
    ]),
    dict(cat_id="CAT-413", cat_name="Función pivote de la vía procesal", cat_def="Función común de vías procesales de distintos países (semejanza funcional, no equivalencia jurídica).", values=[
        V("conocimiento_ordinario", "Proceso de conocimiento ordinario", "Vía plena de cognición."),
        V("sumario_abreviado", "Proceso sumario o abreviado", "Vía de cognición limitada o plazos reducidos."),
        V("garantia_jurisdiccional_derechos", "Garantía jurisdiccional de derechos fundamentales", "Amparo, tutela, acción o recurso de protección y análogos."),
        V("habeas_corpus", "Garantía de libertad personal", "Hábeas corpus y análogos (incluye el 'recurso de amparo' chileno)."),
        V("control_abstracto", "Control abstracto de constitucionalidad", "Acción de inconstitucionalidad y análogas."),
        V("control_legalidad_reglamentos", "Control de legalidad de normas infralegales", "Acción popular, nulidad de reglamentos y análogas."),
        V("contencioso_administrativo", "Impugnación de actuaciones administrativas", "Vía judicial contra actos de la Administración."),
        V("ejecucion", "Ejecución", "Vía de cumplimiento de títulos."),
        V("cautelar", "Cautelar", "Vía o incidente cautelar autónomo."),
        V("penal", "Penal", "Proceso penal en cualquiera de sus etapas."),
        V("procedimiento_administrativo", "Procedimiento administrativo", "Vía ante la Administración."),
        V("arbitral", "Arbitral", "Procedimiento arbitral."),
        V("otro", "Otro", "Vía no catalogada."),
    ]),
    dict(cat_id="CAT-414", cat_name="Instancia", cat_def="Nivel de conocimiento en que se dicta una resolución.", values=[
        V("unica", "Única instancia", "Órgano que conoce en instancia única."),
        V("primera", "Primera instancia", "Primer conocimiento."),
        V("segunda", "Segunda instancia o apelación", "Revisión ordinaria."),
        V("casacion", "Casación o revisión extraordinaria", "Revisión extraordinaria por tribunal supremo o corte."),
        V("constitucional", "Instancia constitucional", "Tribunal o corte constitucional en procesos de garantía o control."),
        V("administrativa_primera", "Administrativa de primera instancia", "Decisión inicial de la entidad."),
        V("administrativa_revision", "Administrativa de revisión", "Reconsideración, apelación o tribunal administrativo."),
        V("arbitral", "Arbitral", "Tribunal arbitral."),
        V("supranacional", "Supranacional", "Corte o tribunal internacional o comunitario."),
    ]),
    dict(cat_id="CAT-415", cat_name="Sentido del fallo", cat_def="Resultado normalizado de una resolución o punto resolutivo; la fórmula original se conserva en MDJ-D14-018.", values=[
        V("fundado", "Fundado / estimado", "Se acoge la pretensión o recurso.", synonyms="ha lugar; acoge; estima; procedente"),
        V("fundado_en_parte", "Fundado en parte", "Se acoge parcialmente."),
        V("infundado", "Infundado / desestimado", "Se rechaza en el fondo.", synonyms="no ha lugar; desestima; rechaza"),
        V("improcedente", "Improcedente", "No se analiza el fondo por falta de presupuestos."),
        V("inadmisible", "Inadmisible", "Defectos formales subsanables o no."),
        V("confirma", "Confirma", "Se mantiene la resolución recurrida."),
        V("revoca", "Revoca", "Se deja sin efecto y se resuelve en sentido distinto."),
        V("anula", "Anula / nulidad", "Se declara nula la resolución o acto."),
        V("casa", "Casa", "Se casa la sentencia recurrida."),
        V("no_casa", "No casa", "Se desestima la casación."),
        V("sanciona", "Sanciona", "Se impone sanción administrativa o disciplinaria."),
        V("archiva", "Archiva / absuelve", "Se archiva o absuelve.", synonyms="absuelve; sobresee; archiva"),
        V("condena", "Condena", "Se condena penalmente o al pago."),
        V("concluye_sin_fondo", "Concluye sin pronunciamiento de fondo", "Desistimiento, abandono, transacción, sustracción de la materia."),
        V("mixto", "Mixto", "Puntos resolutivos con resultados distintos."),
        V("favorable_demandante", "Favorable al demandante/administrado", "Resultado final del proceso (solo MDJ-D14-032).", parent="resultado_final"),
        V("desfavorable_demandante", "Desfavorable al demandante/administrado", "Resultado final del proceso.", parent="resultado_final"),
        V("parcialmente_favorable_demandante", "Parcialmente favorable", "Resultado final del proceso.", parent="resultado_final"),
        V("pendiente", "Pendiente", "Proceso sin resolución final conocida.", parent="resultado_final"),
        V("no_determinable", "No determinable", "No se puede determinar con el corpus.", parent="resultado_final"),
    ]),
    dict(cat_id="CAT-416", cat_name="Fuero o jurisdicción procesal", cat_def="Rama jurisdiccional o vía en la que se tramita el proceso.", values=[
        V("ordinaria", "Ordinaria", "Jurisdicción ordinaria (civil, penal, laboral, familia, comercial)."),
        V("contencioso_administrativa", "Contencioso administrativa", "Jurisdicción o especialidad que controla a la Administración."),
        V("constitucional", "Constitucional", "Tribunal o corte constitucional o sala constitucional."),
        V("electoral", "Electoral", "Justicia electoral."),
        V("militar_policial", "Militar o policial", "Fuero militar o policial."),
        V("especial_transicional", "Especial transicional", "Jurisdicciones especiales transicionales (p. ej., JEP en CO).", country="CO"),
        V("indigena", "Indígena", "Jurisdicción indígena reconocida.", country="BO; EC; CO", notes="DEC-30"),
        V("administrativa", "Vía administrativa", "Procedimiento ante la Administración."),
        V("arbitral", "Arbitral", "Arbitraje."),
        V("supranacional", "Supranacional", "Tribunales internacionales o comunitarios."),
    ]),
    dict(cat_id="CAT-417", cat_name="Materia procesal", cat_def="Especialidad organizativa de la causa según el órgano; distinta de la clasificación temática.", values=[
        V(c, c.replace("_", " ").capitalize(), f"Causa tramitada como materia {c.replace('_', ' ')} según la organización del órgano.")
        for c in ["civil", "comercial", "penal", "laboral", "familia", "contencioso_administrativo", "tributario",
                  "constitucional", "agrario", "minero_ambiental", "electoral", "otra"]
    ]),
    dict(cat_id="CAT-418", cat_name="Etapa procesal", cat_def="Momento del proceso en que se dicta una resolución.", values=[
        V("admision", "Admisión", "Decide la admisión a trámite."),
        V("cautelar", "Cautelar", "Decide medidas cautelares o provisionales."),
        V("saneamiento", "Saneamiento o excepciones", "Resuelve excepciones o defectos procesales."),
        V("fondo", "Fondo", "Resuelve la controversia."),
        V("impugnacion", "Impugnación", "Resuelve un recurso."),
        V("ejecucion", "Ejecución", "Cumplimiento de lo resuelto."),
        V("incidente", "Incidente", "Cuestión incidental."),
        V("conclusion_anticipada", "Conclusión anticipada", "Archivo, desistimiento, abandono, transacción."),
    ]),
    dict(cat_id="CAT-419", cat_name="Tipo de pretensión", cat_def="Clasificación normalizada de pretensiones.", values=[
        V(c, l, d) for c, l, d in [
            ("nulidad", "Nulidad", "Nulidad de acto, contrato o resolución."),
            ("indemnizacion", "Indemnización", "Reparación de daños."),
            ("pago_suma", "Pago de suma de dinero", "Cobro de obligación dineraria."),
            ("reposicion", "Reposición o reincorporación", "Restitución en un puesto o situación."),
            ("declarativa", "Declarativa", "Declaración de un derecho o situación."),
            ("constitutiva", "Constitutiva", "Creación, modificación o extinción de una situación jurídica."),
            ("cumplimiento", "Cumplimiento", "Cumplimiento de obligación o de acto."),
            ("proteccion_derecho_fundamental", "Protección de derecho fundamental", "Tutela de un derecho fundamental."),
            ("revision_sancion", "Revisión de sanción", "Impugnación de una sanción."),
            ("devolucion_tributaria", "Devolución o impugnación tributaria", "Controversia sobre deuda o devolución tributaria."),
            ("cautelar", "Cautelar", "Medida cautelar."),
            ("penal", "Pretensión penal o reparación civil", "Pretensión punitiva o reparación en proceso penal."),
            ("otra", "Otra", "No catalogada."),
        ]
    ]),
    dict(cat_id="CAT-420", cat_name="Función del recurso", cat_def="Función común de los recursos o medios impugnatorios.", values=[
        V("impugnacion_ordinaria", "Impugnación ordinaria", "Apelación y análogos."),
        V("impugnacion_extraordinaria", "Impugnación extraordinaria", "Casación, recurso extraordinario y análogos."),
        V("revision_constitucional", "Revisión constitucional", "Recursos ante tribunal constitucional."),
        V("impugnacion_administrativa", "Impugnación administrativa", "Reconsideración, apelación, revisión administrativa."),
        V("queja", "Queja", "Recurso contra la denegatoria de otro."),
        V("nulidad", "Nulidad procesal", "Pedido de nulidad de actos procesales."),
        V("aclaracion", "Aclaración o corrección", "Pedido de aclaración de la propia resolución."),
    ]),
    dict(cat_id="CAT-421", cat_name="Tipo de procedimiento administrativo", cat_def="Clase de procedimiento administrativo.", values=[
        V(c, l, d) for c, l, d in [
            ("sancionador", "Sancionador", "Determinación de infracciones e imposición de sanciones."),
            ("fiscalizacion", "Fiscalización", "Verificación de cumplimiento."),
            ("trilateral", "Trilateral", "Controversia entre administrados ante la entidad."),
            ("reclamacion_queja", "Reclamación o queja", "Reclamo del administrado."),
            ("recursivo", "Recursivo", "Resolución de recursos administrativos."),
            ("autorizacion_licencia", "Autorización o licencia", "Otorgamiento de títulos habilitantes."),
            ("contratacion_publica", "Contratación pública", "Procedimientos de selección y ejecución contractual."),
            ("consulta", "Consulta", "Absolución de consultas (pronunciamientos interpretativos)."),
            ("tributario", "Tributario", "Determinación, cobranza o devolución tributaria."),
            ("disciplinario", "Disciplinario", "Responsabilidad de servidores públicos."),
            ("otro", "Otro", "No catalogado."),
        ]
    ]),
    dict(cat_id="CAT-422", cat_name="Indicación de versión en la cita", cat_def="Si la cita normativa precisa la versión del texto.", values=[
        V("no_indicada", "No indicada", "La cita no precisa versión."),
        V("texto_original", "Texto original", "Cita el texto original."),
        V("modificado_por_norma", "Modificado por norma", "Cita la versión modificada por una norma indicada."),
        V("vigente_a_fecha", "Vigente a una fecha", "Cita la versión vigente a una fecha o momento (\"al momento de los hechos\")."),
        V("anterior_a_modificacion", "Anterior a modificación", "Cita la versión previa a una modificación."),
    ]),
    dict(cat_id="CAT-423", cat_name="Verificación de cita textual", cat_def="Resultado de comparar una transcripción con el original.", values=[
        V("coincide_version_vigente_origen", "Coincide con la versión vigente al origen", "Transcripción fiel de la versión esperada."),
        V("coincide_version_anterior", "Coincide con una versión anterior", "Transcribe un texto ya modificado a la fecha del origen."),
        V("coincide_otra_version", "Coincide con otra versión", "Coincide con versión distinta de la esperada."),
        V("difiere", "Difiere", "No coincide con ninguna versión conocida."),
        V("no_verificable", "No verificable", "Destino no resuelto a unidad o sin texto."),
    ]),
    dict(cat_id="CAT-424", cat_name="Familia de relación", cat_def="Agrupación de tipos de relación.", values=[
        V(c, l, d) for c, l, d in [
            ("citacion", "Citación", "Proyección de referencias; no sustantiva."),
            ("operacion_normativa", "Operación normativa", "Modificaciones, derogaciones y operaciones expresas sobre normas."),
            ("desarrollo_normativo", "Desarrollo normativo", "Reglamentación, delegación, desarrollo."),
            ("estructural", "Estructural", "Continuidad, división, fusión y correspondencias."),
            ("control_validez", "Control de validez", "Inconstitucionalidad, nulidad, inaplicación."),
            ("cadena_procesal", "Cadena procesal", "Relaciones entre resoluciones de un proceso."),
            ("uso_normativo", "Uso normativo", "Aplicación e interpretación."),
            ("uso_precedentes", "Uso de precedentes", "Seguimiento, apartamiento, unificación."),
            ("doctrinal", "Doctrinal", "Comentario, crítica, sistematización."),
            ("aplicabilidad", "Aplicabilidad", "Aplicabilidad supranacional por país."),
            ("tacita", "Tácita", "Relaciones por incompatibilidad, solo alerta."),
            ("derivada", "Derivada", "Inversas y agregados calculados."),
        ]
    ]),
    dict(cat_id="CAT-425", cat_name="Cálculo alimentado", cat_def="Cálculos posteriores que usan una relación.", values=[
        V(c, l, d) for c, l, d in [
            ("vigencia", "Vigencia", "Estado de vigencia de unidades."),
            ("texto_consolidado", "Texto consolidado", "Reconstrucción de versiones."),
            ("linea_de_vida", "Línea de vida", "Historia de identidad de unidades."),
            ("precedente", "Carácter de precedente", "Cálculo de fuerza vinculante (D17)."),
            ("cadena_procesal", "Cadena procesal", "Orden de resoluciones del proceso."),
            ("firmeza", "Firmeza", "Estado de firmeza de resoluciones."),
            ("resultado_final", "Resultado final", "Resultado del proceso."),
            ("metricas_citacion", "Métricas de citación", "Conteos y centralidad."),
            ("ninguno", "Ninguno", "No alimenta cálculos."),
        ]
    ]),
    dict(cat_id="CAT-426", cat_name="Tipo de proceso", cat_def="Clase de proceso agrupador.", values=[
        V("judicial", "Judicial", "Proceso ante órgano jurisdiccional."),
        V("administrativo", "Procedimiento administrativo", "Procedimiento ante entidad."),
        V("arbitral", "Arbitral", "Arbitraje.", notes="DEC-07"),
        V("conciliacion", "Conciliación", "Procedimiento conciliatorio.", notes="DEC-07"),
    ]),
    dict(cat_id="CAT-427", cat_name="Sentido del voto", cat_def="Posición de un integrante de colegiado.", values=[
        V("mayoria", "Con la mayoría", "Suscribe la decisión sin voto separado."),
        V("concurrente", "Concurrente o aclaración", "Comparte la decisión con fundamentos propios.", synonyms="aclaración de voto; fundamento de voto"),
        V("disidente", "Disidente o singular", "No comparte la decisión.", synonyms="voto singular; salvamento de voto; voto en discordia"),
        V("disidente_parcial", "Disidente parcial", "Discrepa de un extremo."),
    ]),
    dict(cat_id="CAT-428", cat_name="Condición de protección especial de la parte", cat_def="Categorías que activan protección reforzada de datos.", values=[
        V(c, l, d) for c, l, d in [
            ("menor_de_edad", "Menor de edad", "Niña, niño o adolescente."),
            ("victima_violencia", "Víctima de violencia", "Violencia de género, familiar o sexual."),
            ("persona_discapacidad", "Persona con discapacidad", "Discapacidad mencionada."),
            ("paciente_salud", "Paciente o dato de salud", "Condición de salud mencionada."),
            ("pueblo_indigena", "Pueblo indígena o comunidad", "Pertenencia a pueblo indígena o comunidad."),
            ("persona_privada_libertad", "Persona privada de libertad", "Condición de detención."),
            ("migrante_refugiado", "Migrante o refugiado", "Condición migratoria."),
            ("adulto_mayor", "Adulto mayor", "Persona adulta mayor."),
        ]
    ]),
    dict(cat_id="CAT-429", cat_name="Estado de firmeza", cat_def="Conclusión sobre la firmeza de una resolución con el corpus disponible.", values=[
        V("firme_declarada", "Firme (declarada)", "El documento declara la firmeza."),
        V("firme_segun_corpus", "Firme según corpus", "Última instancia sin recurso posterior conocido."),
        V("impugnada", "Impugnada", "Existe recurso posterior pendiente o conocido."),
        V("revocada", "Revocada", "Revocada por resolución posterior."),
        V("anulada", "Anulada", "Anulada por resolución posterior."),
        V("no_determinable", "No determinable", "Información insuficiente."),
    ]),
    dict(cat_id="CAT-430", cat_name="Motivo de no resolución", cat_def="Causa por la que una referencia no se resolvió a unidad.", values=[
        V("fuera_del_corpus", "Destino fuera del corpus", "Documento no incorporado."),
        V("alias_desconocido", "Alias desconocido", "Alias no registrado en la tabla."),
        V("unidad_inexistente_en_version", "Unidad inexistente en la versión", "La disposición no existe en la versión de destino."),
        V("datos_insuficientes", "Datos insuficientes", "Faltan componentes para identificar."),
        V("error_en_origen", "Error en el documento de origen", "La cita es materialmente errónea."),
        V("linea_de_vida_incompleta", "Línea de vida incompleta", "No se puede determinar la versión."),
    ]),
]
