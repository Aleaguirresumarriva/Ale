"""
Campos del bloque G1: D01 Identificación, D02 Procedencia institucional y custodia,
D04 Naturaleza y tipología, D15 Lengua y forma.
Generado para el Diccionario Maestro de Metadatos Jurídicos de Juztina (Etapa 2).
"""

_PERF = {"UNI": "todas las categorías", "NOR": "normativa", "JUR": "jurisprudencia",
         "ADM": "actos administrativos", "DOC": "doctrina"}


def _aplic(profiles, countries, cond):
    perf = ", ".join(_PERF[p] for p in profiles.split("; "))
    paises = "los siete países" if countries == "ALL" else countries.replace("; ", ", ")
    txt = f"Perfiles: {perf}. Países: {paises}."
    return f"{txt} {cond}" if cond else txt


FIELDS = []


def F(id, tech, func, dim, profiles, unit, defn, just, dtype, card, values, example, origin, method,
      evidence, extraction, validation, prio, mode, deps, funcs, stage, risk, cond="",
      review="No", privacy="Ninguna", countries="ALL", country_status="Común", pending="No",
      obs="Sin observaciones adicionales."):
    FIELDS.append(dict(
        id=id, tech=tech, func=func, dim=dim, profiles=profiles, unit=unit, defn=defn, just=just,
        dtype=dtype, card=card, values=values, example=example, origin=origin, method=method,
        evidence=evidence, extraction=extraction, validation=validation,
        applicability=_aplic(profiles, countries, cond), prio=prio, mode=mode, review=review,
        privacy=privacy, deps=deps, funcs=funcs, obs=obs, stage=stage, risk=risk,
        countries=countries, country_status=country_status, pending=pending))


NA_VAL = "No aplica: valor libre sin vocabulario controlado."
NA_EVID_SYS = "No aplica: valor generado por el sistema; se registra la ejecución que lo creó."

# =====================================================================================
# D01 IDENTIFICACIÓN
# =====================================================================================
F("MDJ-D01-001", "id_obra", "Identificador de la obra", "D01", "UNI", "Obra",
  "Identificador persistente y opaco de la obra jurídica (el acto abstracto), asignado por Juztina al reconocerla por primera vez y nunca reutilizado.",
  "Es la clave de identidad estable a la que se vinculan versiones, manifestaciones, unidades, relaciones y clasificaciones; los identificadores oficiales son solo alias.",
  "Identificador", "1 obligatorio", "No aplica: identificador opaco (p. ej. UUID o secuencia con prefijo OBR-).",
  "OBR-7f3a9c21", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Asignar en E1 al confirmar una obra nueva tras la separación de obras y la deduplicación; si la obra ya existe, reutilizar su ID.",
  "Único en todo el repositorio; inmutable; nunca reasignado a otra obra aunque esta se fusione (queda redirigido).",
  "P0", "A", "MDJ-D01-025 Estado de deduplicación; separación de obras (E1)", "F02; F03; F11; F12; F16",
  "E1", "R3", obs="Una obra derogada o anulada conserva su identificador.")

F("MDJ-D01-002", "id_version", "Identificador de la versión", "D01", "UNI", "Versión",
  "Identificador persistente de una versión de la obra, es decir, del texto completo vigente en un intervalo y originado por un evento determinado.",
  "Permite citar y recuperar el texto exacto aplicable en una fecha y vincular la jurisprudencia con la versión que interpretó.",
  "Identificador", "1 obligatorio", "No aplica: identificador opaco con prefijo VER-.",
  "VER-7f3a9c21-0003", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Crear una versión por cada texto observado (manifestación) o reconstruido (aplicando operaciones modificatorias en E7). En jurisprudencia y doctrina normalmente existe una sola versión.",
  "Único; pertenece a una sola obra; no puede existir sin MDJ-D01-001.",
  "P0", "A", "MDJ-D01-001; eventos de vigencia (D03)", "F02; F06; F15; F16",
  "E1", "R3", obs="Las versiones reconstruidas se crean en E7 (clase B) a partir de operaciones modificatorias extraídas.")

F("MDJ-D01-003", "id_manifestacion", "Identificador de la manifestación", "D01", "UNI", "Manifestación",
  "Identificador persistente de un archivo concreto obtenido de una fuente concreta en una fecha concreta.",
  "Es la unidad que existe al iniciar la pasada; todas las anclas de evidencia se refieren a ella.",
  "Identificador", "1 obligatorio", "No aplica: identificador opaco con prefijo MAN-.",
  "MAN-000184233", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Asignar en E0 a cada archivo ingerido. Un archivo distinto (aunque tenga igual contenido) es otra manifestación.",
  "Único; inmutable; asociado a un hash (MDJ-D01-023).",
  "P0", "A", "MDJ-D01-023 Hash del contenido", "F15; F16",
  "E0", "R3")

F("MDJ-D01-004", "pais_jurisdiccion", "País o jurisdicción de la obra", "D01", "UNI", "Obra",
  "Ordenamiento jurídico al que pertenece la obra: país o pseudo jurisdicción supranacional (CAN, Sistema Interamericano, Mercosur).",
  "Es la primera condición para interpretar tipo, rango, fuerza y numeración; separa los siete corpus y las fuentes supranacionales.",
  "Código ISO", "1 obligatorio", "CAT-001 País y jurisdicción.",
  "PE", "Normalizado por regla", "Extracción directa + Normalización",
  "Encabezado, sello o emisor que identifica el ordenamiento; o la colección de origen en Juztina.",
  "Tomar el país de la colección de Juztina; confirmar con el emisor y el encabezado. Si el emisor es un órgano supranacional (Tribunal de Justicia de la CAN, Corte IDH), usar la pseudo jurisdicción.",
  "Valor de CAT-001; coherente con el país del organismo emisor (MDJ-D02-001); discrepancia con la colección se marca para revisión.",
  "P0", "A", "MDJ-D02-001 Organismo emisor", "F01; F02; F03; F09",
  "E1", "R2", cond="En doctrina indica la jurisdicción de origen de la publicación; la jurisdicción objeto del análisis es un campo distinto (D08).",
  obs="Para doctrina no confundir con la jurisdicción analizada.")

F("MDJ-D01-005", "entidad_territorial_jurisdiccion", "Entidad territorial de la jurisdicción", "D01", "NOR; JUR; ADM", "Obra",
  "Entidad subnacional (provincia, estado, departamento, región, municipio, entidad autónoma) a cuyo ordenamiento pertenece la obra cuando no es nacional.",
  "Distingue normas y decisiones subnacionales con igual número en distintos territorios (p. ej. leyes provinciales o estatales) y permite filtrar por territorio.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Entidad: territorio o jurisdicción (catálogo territorial por país).",
  "AR-M (Provincia de Mendoza)", "Normalizado por regla", "Extracción directa + Normalización",
  "Encabezado o denominación del emisor que nombra el territorio.",
  "Extraer el territorio del emisor o del encabezado (\"Ley Provincial N.°…\", \"Ordenanza Municipal de…\") y mapearlo al catálogo territorial. Dejar 'No aplicable' si la obra es nacional o supranacional.",
  "Obligatorio si el nivel de gobierno del emisor es subnacional; debe existir en el catálogo territorial del país de MDJ-D01-004.",
  "P0", "A", "MDJ-D01-004; MDJ-D02-001; catálogo territorial", "F03; F05; F09",
  "E1", "R2", cond="Solo si la obra pertenece a un ordenamiento subnacional.",
  country_status="Catálogo por país", pending="DEC-28; DEC-31")

F("MDJ-D01-006", "numero_oficial", "Número oficial tal como figura", "D01", "UNI", "Obra",
  "Número o código con el que el propio documento se identifica, transcrito literalmente (incluye prefijos, guiones, año y sufijos).",
  "Es el dato con el que los usuarios citan y buscan; conservar la forma literal permite verificar la evidencia y resolver citas.",
  "String", "0..1 obligatorio condicionado", NA_VAL,
  "004-2019-JUS", "Explícito en documento", "Extracción directa",
  "Tramo literal del encabezado o del título donde aparece el número.",
  "Extraer del encabezado el número que acompaña al tipo documental (\"Ley N.° 29783\", \"Sentencia T-760/08\", \"Rol N.° 1234-2020\"). No construirlo a partir de otros datos. Si el documento no tiene número, estado 'No encontrado'.",
  "Coincidencia literal con la evidencia; formato compatible con el patrón del tipo documental (MDJ-D04-031) o marca de discrepancia.",
  "P0", "A", "MDJ-D04-003 Tipo documental original", "F02; F03; F11; F15",
  "E1", "R1", cond="Obligatorio cuando el tipo documental se numera; en doctrina usualmente no aplica.",
  country_status="Catálogo por país")

F("MDJ-D01-007", "numero_oficial_normalizado", "Número oficial normalizado", "D01", "UNI", "Obra",
  "Forma canónica del número oficial según la plantilla del tipo documental y el país (sin variantes de puntuación, ceros ni abreviaturas).",
  "Permite deduplicar y resolver citas que escriben el mismo número de formas distintas (\"N° 29783\", \"Nº29783\", \"29.783\").",
  "String", "0..1 obligatorio condicionado", "No aplica: plantilla por tipo documental (MDJ-D04-031).",
  "29783", "Normalizado por regla", "Normalización",
  "Regla de normalización aplicada y evidencia de MDJ-D01-006.",
  "Aplicar la plantilla de numeración del tipo documental del país a MDJ-D01-006; eliminar símbolos de número, separadores de miles y espacios; conservar año y sufijos significativos (Bis, -A).",
  "Determinista y reproducible; dos obras del mismo país, emisor y tipo no pueden compartir número normalizado salvo excepción documentada.",
  "P0", "A", "MDJ-D01-006; MDJ-D04-031 Patrón de numeración", "F03; F11; F16",
  "E1", "R2", country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D01-008", "anio_numeracion", "Año de la numeración", "D01", "NOR; JUR; ADM", "Obra",
  "Año que forma parte del identificador oficial cuando el sistema de numeración se reinicia anualmente o lo incorpora.",
  "En muchos tipos el número se repite cada año; sin el año la identificación es ambigua.",
  "Integer", "0..1 obligatorio condicionado", "No aplica: año de cuatro cifras.",
  "2019", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo del número oficial que contiene el año.",
  "Extraer el año incluido en el número (\"004-2019-JUS\", \"T-760/08\" → 2008). No usar la fecha de emisión como sustituto.",
  "Entre 1800 y el año en curso; coherente con la fecha de emisión (diferencia máxima de un año, o marca de revisión).",
  "P0", "A", "MDJ-D01-006", "F03; F11",
  "E1", "R2", cond="Solo si la numeración del tipo incorpora el año.", country_status="Catálogo por país")

F("MDJ-D01-009", "identificadores_oficiales_adicionales", "Otros identificadores oficiales", "D01", "UNI", "Obra",
  "Lista tipada de identificadores oficiales distintos del número principal: registro digital, código de sentencia, número de expediente asociado en el encabezado, sumilla con clave, ECLI u otros.",
  "Las citas usan identificadores distintos según el país y la fuente; registrarlos como alias permite resolver referencias.",
  "Array", "0..n", "Cada elemento: tipo (CAT-101 Tipo de identificador oficial) + valor literal + valor normalizado.",
  "[{tipo: registro_digital_sjf, valor: '2021234'}]", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo literal de cada identificador.",
  "Detectar en encabezado, pie o recuadros los identificadores con etiqueta reconocible y tipificarlos con CAT-101. No duplicar MDJ-D01-006 ni el número de expediente de D14.",
  "Tipo válido en CAT-101; valor no vacío; un mismo par tipo-valor no puede pertenecer a dos obras.",
  "P0", "A", "MDJ-D01-006", "F03; F08; F11; F15",
  "E1", "R2", country_status="Catálogo por país",
  obs="El número de expediente como dato procesal se modela en D14; aquí solo si funciona como identificador de la obra.")

F("MDJ-D01-010", "titulo_oficial", "Título oficial", "D01", "UNI", "Obra",
  "Nombre o título que el documento se da a sí mismo, transcrito literalmente, sin el tipo ni el número.",
  "Es el dato principal de búsqueda y presentación; muchas normas se citan por su título.",
  "String", "0..1 obligatorio condicionado", NA_VAL,
  "Ley de Seguridad y Salud en el Trabajo", "Explícito en documento", "Extracción directa",
  "Tramo literal del título en el encabezado.",
  "Extraer el título que sigue al número en el encabezado. En jurisprudencia y actos sin título, estado 'No encontrado' (no generar uno). En doctrina, el título del trabajo.",
  "Coincidencia literal con la evidencia; longitud entre 3 y 1.000 caracteres.",
  "P0", "A", "Estructura del encabezado (E2)", "F02; F03; F04; F15",
  "E1", "R2")

F("MDJ-D01-011", "denominacion_oficial", "Denominación oficial completa", "D01", "UNI", "Obra",
  "Cadena completa con que el documento se identifica en su encabezado (tipo + número + título), transcrita literalmente.",
  "Conserva la forma oficial de cita y sirve de evidencia para tipo, número y título.",
  "String", "1 obligatorio", NA_VAL,
  "LEY N.° 29783, LEY DE SEGURIDAD Y SALUD EN EL TRABAJO", "Explícito en documento", "Extracción directa",
  "Tramo literal del encabezado.",
  "Transcribir el encabezado identificatorio del documento, sin vistos ni considerandos.",
  "Coincidencia literal con la manifestación; contiene el número oficial si existe.",
  "P0", "A", "Estructura del encabezado (E2)", "F03; F15",
  "E1", "R2")

F("MDJ-D01-012", "nombre_corto_o_sigla", "Nombres cortos y siglas", "D01", "NOR; JUR; ADM", "Obra",
  "Siglas o denominaciones abreviadas con que la obra es citada (por el propio texto o por la práctica).",
  "Las citas usan siglas (\"LPAG\", \"CPC\"); sin ellas no se resuelven muchas referencias.",
  "Array", "0..n", "Cada elemento: alias + ámbito (declarado por el propio texto / uso en la práctica).",
  "['LPAG']", "Explícito en documento", "Extracción directa",
  "Tramo donde el texto declara la sigla (\"en adelante, la Ley\") o fuente externa del alias.",
  "Extraer las siglas que el propio documento declara. Los alias de uso general se cargan por curaduría o desde las referencias de otros documentos (E7).",
  "No vacío; un alias puede ser ambiguo entre obras y se marca como tal en el catálogo de alias por país.",
  "P1", "A", "MDJ-D01-010", "F03; F11; F15",
  "E1", "R2", country_status="Catálogo por país",
  obs="Base del catálogo de alias que usa la resolución de referencias (D07).")

F("MDJ-D01-013", "nombre_popular", "Nombre popular o denominación de uso", "D01", "NOR; JUR; ADM", "Obra",
  "Nombre por el que la obra es conocida fuera de su título oficial (ley con nombre propio, caso conocido por el nombre de una parte o de un hecho).",
  "Los usuarios buscan y citan casos y leyes por su nombre popular.",
  "Array", "0..n", NA_VAL,
  "Caso Quiborax", "Fuente externa", "Enriquecimiento externo",
  "Fuente externa identificada o referencias de otros documentos que usan el nombre.",
  "No inferir del texto de la propia obra. Incorporar desde fuentes secundarias o desde referencias jurisprudenciales/doctrinales que lo usan (E7) y por curaduría.",
  "Cada valor con su fuente; si deriva de una parte persona natural, aplicar la política de datos personales.",
  "P3", "D", "Referencias (D07); política DEC-18", "F03; F04",
  "Curaduría", "R3", privacy="Puede contener datos personales", pending="DEC-18",
  obs="Cuando el nombre popular contenga el nombre de una persona natural, su uso depende de la política de datos personales.")

F("MDJ-D01-014", "cita_canonica", "Cita canónica de Juztina", "D01", "UNI", "Obra",
  "Cadena de cita normalizada que Juztina genera para la obra a partir de tipo, número, año, emisor y fecha, según la plantilla del país.",
  "Unifica la forma en que el asistente y la interfaz citan cada obra.",
  "String", "1 obligatorio", "No aplica: plantilla de cita por tipo documental y país.",
  "Ley N.° 29783 (Perú, 2011)", "Derivado por cálculo", "Cálculo",
  "Regla de plantilla aplicada y campos de insumo.",
  "Componer con la plantilla del tipo documental a partir de MDJ-D04-004, MDJ-D01-007, MDJ-D01-008, emisor y fecha.",
  "Reproducible; recalculada si cambia un insumo.",
  "P1", "B", "MDJ-D04-004; MDJ-D01-007; MDJ-D02-001; fecha de emisión (D03)", "F02; F15",
  "E7", "R3", country_status="Catálogo por país")

F("MDJ-D01-015", "subtitulo", "Subtítulo", "D01", "DOC", "Obra",
  "Subtítulo de una obra doctrinal, transcrito literalmente.",
  "Precisa el objeto de la obra y mejora la búsqueda bibliográfica.",
  "String", "0..1 opcional", NA_VAL, "Un análisis desde el Derecho comparado",
  "Explícito en documento", "Extracción directa", "Tramo literal de la portada o primera página.",
  "Extraer el texto que sigue al título separado por dos puntos, punto o en línea distinta en la portada.",
  "Coincidencia literal; no repite el título.", "P1", "A", "MDJ-D01-010", "F03; F04", "E3", "R3")

F("MDJ-D01-016", "doi", "DOI", "D01", "DOC", "Obra",
  "Identificador de objeto digital asignado a la obra doctrinal.",
  "Identificador persistente internacional que permite deduplicar y enlazar con bases bibliográficas.",
  "String", "0..1 opcional", "No aplica: sintaxis DOI (prefijo 10.xxxx/sufijo).",
  "10.5354/0719-2584.2020.12345", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo literal con el DOI.", "Buscar la cadena 'doi' o un patrón 10.\\d{4,9}/\\S+ en la primera página, pie o metadatos del PDF.",
  "Cumple la expresión regular de DOI; se normaliza en minúsculas sin prefijo URL.",
  "P1", "A", "No aplica: dato autónomo", "F03; F16", "E3", "R3")

F("MDJ-D01-017", "isbn", "ISBN", "D01", "DOC", "Obra",
  "Número internacional normalizado del libro o del libro que contiene el capítulo.",
  "Permite identificar libros y ediciones y deduplicar.",
  "String", "0..n", "No aplica: ISBN-10 o ISBN-13.", "978-612-4567-89-0",
  "Explícito en documento", "Extracción directa + Normalización", "Tramo literal con el ISBN.",
  "Buscar 'ISBN' en la página legal o portada; normalizar a ISBN-13 sin guiones.",
  "Dígito de control válido.", "P1", "A", "No aplica: dato autónomo", "F03; F16", "E3", "R3",
  obs="Una edición distinta tiene ISBN distinto: se asocia a la versión correspondiente (MDJ-D01-034).")

F("MDJ-D01-018", "uri_repositorio_academico", "Handle o URI de repositorio", "D01", "DOC", "Obra",
  "Identificador persistente asignado por un repositorio institucional (handle, URI, ARK) a tesis u obras académicas.",
  "Muchas tesis no tienen DOI; el handle es su identificador estable.",
  "URL", "0..1 opcional", NA_VAL, "http://repositorio.umsa.bo/handle/123456789/1234",
  "Explícito en documento", "Extracción directa", "Tramo literal o metadato de la fuente.",
  "Extraer de la página de la fuente o de la portada el identificador persistente del repositorio.",
  "URL sintácticamente válida.", "P2", "A", "MDJ-D02-013 Fuente de obtención", "F03; F16", "E3", "R3")

F("MDJ-D01-019", "id_en_fuente_origen", "Identificador en la fuente de origen", "D01", "UNI", "Manifestación",
  "Identificador que la fuente de donde se obtuvo el archivo asigna al documento en su propio sistema.",
  "Permite volver a la fuente, actualizar la copia y deduplicar entre capturas.",
  "String", "0..1 opcional", NA_VAL, "idNorma=1026995",
  "Fuente externa", "Enriquecimiento externo", "Metadato de la captura o URL de la fuente.",
  "Registrar el identificador presente en la URL o en los metadatos de la fuente al capturar.",
  "No vacío si la fuente lo provee; el par fuente-identificador es único.", "P0", "A", "MDJ-D02-013", "F16", "E0", "R3")

F("MDJ-D01-020", "id_legado_juztina", "Identificador en la base actual de Juztina", "D01", "UNI", "Manifestación",
  "Identificador del documento en la base de datos existente de Juztina antes de la pasada.",
  "Garantiza la trazabilidad con el sistema actual, los especialistas ya construidos y la migración.",
  "String", "1 obligatorio", NA_VAL, "doc_pe_000123456",
  "Fuente externa", "Enriquecimiento externo", "Registro de la base actual.",
  "Copiar el identificador del registro de origen en la base de Juztina al ingerir.",
  "Existe en la base actual; relación muchos a uno con obras permitida (duplicados legados).",
  "P0", "A", "Acceso a la base actual de Juztina", "F01; F16", "E0", "R3",
  obs="Formato real desconocido: no se dispone del esquema de la base actual.")

F("MDJ-D01-021", "url_oficial", "URL oficial", "D01", "UNI", "Manifestación",
  "Dirección web del documento en una fuente oficial (diario oficial, portal del emisor) cuando la manifestación proviene de ella o la cita.",
  "Permite verificar el texto contra la fuente oficial y ofrecer el enlace al usuario.",
  "URL", "0..1 opcional", NA_VAL, "https://busquedas.elperuano.pe/...",
  "Fuente externa", "Enriquecimiento externo", "Metadato de captura o fuente externa.",
  "Registrar la URL de la fuente oficial del documento; no confundir con la URL de captura si la copia vino de una fuente secundaria.",
  "URL válida; dominio perteneciente a una fuente con carácter oficial (MDJ-D02-043).",
  "P0", "A", "MDJ-D02-013; MDJ-D02-043", "F15; F16", "E0", "R3")

F("MDJ-D01-022", "url_captura", "URL de captura", "D01", "UNI", "Manifestación",
  "Dirección desde la que Juztina descargó efectivamente el archivo.",
  "Es parte de la procedencia de la copia y permite reproducir la captura.",
  "URL", "0..1 obligatorio condicionado", NA_VAL, "https://www.bcn.cl/leychile/navegar?idNorma=1026995",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Registrar la URL al capturar; si el documento proviene de carga manual o migración, estado 'No aplicable' con el método de captura.",
  "URL válida o método de captura distinto de descarga.", "P0", "A", "MDJ-D02-020 Método de captura", "F16", "E0", "R3")

F("MDJ-D01-023", "hash_contenido", "Hash del contenido", "D01", "UNI", "Manifestación",
  "Resumen criptográfico del archivo binario ingerido.",
  "Garantiza integridad, detecta duplicados exactos y fija la base de las anclas de evidencia.",
  "Hash", "1 obligatorio", "No aplica: SHA-256 en hexadecimal.", "9f86d081884c7d65...",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Calcular SHA-256 sobre el binario original antes de cualquier transformación.",
  "64 caracteres hexadecimales; recalculado coincide.", "P0", "A", "No aplica: se calcula sobre el archivo", "F16", "E0", "R3")

F("MDJ-D01-024", "nombre_archivo_original", "Nombre del archivo original", "D01", "UNI", "Manifestación",
  "Nombre del archivo tal como fue obtenido de la fuente o cargado.",
  "Suele contener pistas de identificación útiles para la separación y deduplicación y para la auditoría.",
  "String", "0..1 opcional", NA_VAL, "Ley_29783_SST.pdf",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Registrar al ingerir.", "No vacío si existe archivo.", "P0", "A", "No aplica: dato de ingesta", "F16", "E0", "R3")

F("MDJ-D01-025", "estado_deduplicacion", "Estado de deduplicación", "D01", "UNI", "Obra",
  "Resultado del proceso que determina si la obra es única o coincide con otra obra ya registrada.",
  "Evita contar, clasificar o citar dos veces el mismo acto obtenido de fuentes distintas.",
  "Enum", "1 obligatorio", "CAT-102 Estado de deduplicación.", "candidato_duplicado",
  "Derivado por cálculo", "Cálculo + Revisión humana", "Campos de identidad comparados y regla aplicada.",
  "Comparar país, emisor, tipo, número normalizado, año y fechas; coincidencia exacta = duplicado confirmado; coincidencia parcial = candidato.",
  "Valor de CAT-102; si 'fusionada', debe indicar la obra que prevalece (MDJ-D01-026).",
  "P0", "B", "MDJ-D01-004; MDJ-D01-007; MDJ-D01-008; MDJ-D02-001; MDJ-D04-004", "F16",
  "E7", "R2", review="Condicionado", obs="Revisión humana solo para candidatos con coincidencia parcial.")

F("MDJ-D01-026", "obras_candidatas_duplicado", "Obras candidatas a duplicado", "D01", "UNI", "Obra",
  "Obras que podrían ser el mismo acto según la regla de deduplicación, o la obra que prevalece tras una fusión.",
  "Hace auditable la deduplicación y permite redirigir identificadores.",
  "Array de referencias", "0..n", "Referencias a MDJ-D01-001.", "[OBR-11aa22bb]",
  "Derivado por cálculo", "Cálculo", "Regla de deduplicación y puntuación de coincidencia.",
  "Registrar las obras que superan el umbral de coincidencia, con su puntuación.",
  "Las referencias existen; ninguna apunta a la propia obra.", "P0", "B", "MDJ-D01-025", "F16", "E7", "R2")

F("MDJ-D01-027", "obras_en_manifestacion", "Obras contenidas en la manifestación", "D01", "UNI", "Manifestación",
  "Lista de obras identificadas dentro de un mismo archivo (p. ej. una edición del diario oficial con varias normas, una revista con varios artículos).",
  "La separación de obras es un paso P0: sin ella se clasifican y relacionan documentos inexistentes.",
  "Array de referencias", "1..n", "Referencias a MDJ-D01-001, en orden de aparición.", "[OBR-1, OBR-2, OBR-3]",
  "Inferido por modelo", "Extracción directa + Inferencia", "Límites de cada obra en la manifestación (anclas inicial y final).",
  "Detectar en E1 los encabezados de obra (tipo + número + emisor) y los cortes de página o sección; asignar a cada obra su tramo.",
  "Los tramos no se superponen y cubren el contenido sustantivo; cada obra tiene un encabezado identificable.",
  "P0", "A", "Texto normalizado (E0)", "F16", "E1", "R1", review="Condicionado",
  obs="Revisión humana cuando la separación tenga baja confianza o el número de obras sea atípico para la fuente.")

F("MDJ-D01-028", "rango_obra_en_manifestacion", "Ubicación de la obra en la manifestación", "D01", "UNI", "Manifestación",
  "Páginas y posiciones de texto inicial y final que ocupa cada obra dentro de la manifestación.",
  "Permite recortar el texto de la obra, anclar evidencias y mostrar la página exacta.",
  "Objeto", "1..n", "Objeto: id_obra, página inicial, página final, posición inicial, posición final.",
  "{obra: OBR-2, pag: 3-5, pos: 10233-24510}", "Explícito en documento", "Extracción directa",
  "Anclas de inicio y fin.", "Registrar junto con MDJ-D01-027 los límites de cada obra.",
  "Posiciones dentro del texto normalizado; sin superposición entre obras.", "P0", "A", "MDJ-D01-027", "F15; F16", "E1", "R2")

F("MDJ-D01-029", "denominacion_version", "Denominación de la versión", "D01", "NOR; ADM", "Versión",
  "Etiqueta legible que identifica la versión (texto original, texto modificado por una norma determinada, texto rectificado).",
  "Permite al usuario y al asistente saber qué texto está viendo y citar la versión.",
  "String", "1 obligatorio", "No aplica: plantilla 'Texto original' / 'Texto vigente desde [fecha] según [norma]'.",
  "Texto vigente desde 2016-07-14 según Ley N.° 30222", "Derivado por cálculo", "Cálculo",
  "Evento que origina la versión (D03).", "Componer a partir del evento que abre la versión y su norma de origen.",
  "Coherente con el intervalo y el evento de la versión.", "P1", "B", "MDJ-D01-002; eventos de vigencia (D03)", "F06; F15", "E7", "R2")

F("MDJ-D01-030", "publicacion_contenedora", "Publicación contenedora", "D01", "DOC", "Obra",
  "Revista, anuario o serie en la que se publicó la obra doctrinal.",
  "Es la base para citar el artículo y para evaluar la autoridad del medio.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Entidad: publicación o fuente.",
  "Revista Boliviana de Derecho", "Normalizado por regla", "Extracción directa + Normalización",
  "Tramo literal con el nombre de la revista (cabecera, pie, portada).",
  "Extraer el nombre de la revista de la cabecera, pie de página o primera página y vincularlo al catálogo de publicaciones; crear entrada nueva marcada como pendiente si no existe.",
  "Obligatorio si el tipo de publicación doctrinal es artículo de revista.",
  "P1", "A", "MDJ-D04-012 Tipo de publicación doctrinal", "F03; F04", "E3", "R2")

F("MDJ-D01-031", "obra_contenedora", "Obra contenedora (libro colectivo)", "D01", "DOC", "Obra",
  "Libro u obra colectiva de la que forma parte un capítulo o contribución.",
  "Permite identificar capítulos y vincularlos con el libro.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a MDJ-D01-001 de la obra contenedora.",
  "OBR-libro-0042", "Normalizado por regla", "Extracción directa + Normalización",
  "Tramo con 'En:' o la referencia al libro.", "Extraer la referencia al libro contenedor; crear la obra del libro si no existe.",
  "Obligatorio si el tipo es capítulo de libro.", "P2", "A", "MDJ-D04-012", "F03; F11", "E3", "R3")

F("MDJ-D01-032", "volumen", "Volumen", "D01", "DOC", "Obra",
  "Volumen de la publicación contenedora en que aparece la obra.", "Necesario para citar y localizar el artículo.",
  "String", "0..1 opcional", NA_VAL, "Vol. 3", "Explícito en documento", "Extracción directa",
  "Tramo literal.", "Extraer de la cabecera o portada del número.", "Coincidencia literal.", "P1", "A", "MDJ-D01-030", "F03; F15", "E3", "R3")

F("MDJ-D01-033", "numero_fasciculo", "Número o fascículo", "D01", "DOC", "Obra",
  "Número o fascículo de la publicación contenedora.", "Necesario para citar y localizar el artículo.",
  "String", "0..1 opcional", NA_VAL, "N.° 4", "Explícito en documento", "Extracción directa",
  "Tramo literal.", "Extraer de la cabecera o portada.", "Coincidencia literal.", "P1", "A", "MDJ-D01-030", "F03; F15", "E3", "R3")

F("MDJ-D01-034", "numero_edicion", "Número de edición", "D01", "DOC", "Versión",
  "Edición de un libro doctrinal a la que corresponde la versión.",
  "En doctrina las ediciones son versiones de la obra; distinguirlas evita citar contenido desactualizado.",
  "String", "0..1 opcional", NA_VAL, "3.ª edición actualizada", "Explícito en documento", "Extracción directa",
  "Tramo literal de la página legal.", "Extraer de la portada o página legal; las reimpresiones no son ediciones.",
  "Coincidencia literal; una reimpresión no crea versión.", "P1", "A", "MDJ-D01-002", "F03; F04", "E3", "R3")

F("MDJ-D01-035", "paginas_en_contenedor", "Páginas en la publicación contenedora", "D01", "DOC", "Obra",
  "Rango de páginas que ocupa la obra en la revista o el libro contenedor.", "Necesario para citar y verificar.",
  "String", "0..1 opcional", NA_VAL, "45-78", "Explícito en documento", "Extracción directa",
  "Tramo literal o numeración de páginas.", "Extraer del encabezado o de la numeración de páginas impresa.",
  "Página inicial menor o igual que la final.", "P2", "A", "MDJ-D01-030", "F15", "E3", "R3")

F("MDJ-D01-036", "coleccion_o_serie", "Colección o serie editorial", "D01", "DOC", "Obra",
  "Colección o serie editorial a la que pertenece un libro o documento de trabajo.", "Ayuda a agrupar y localizar obras.",
  "String", "0..1 opcional", NA_VAL, "Colección Derecho Público", "Explícito en documento", "Extracción directa",
  "Tramo literal.", "Extraer de la portada o página legal.", "Coincidencia literal.", "P3", "A", "No aplica: dato autónomo", "F03", "E3", "R3")

F("MDJ-D01-037", "lugar_edicion", "Lugar de edición", "D01", "DOC", "Versión",
  "Ciudad de edición de una obra doctrinal, según la página legal.", "Dato bibliográfico estándar para citas completas.",
  "String", "0..1 opcional", NA_VAL, "Santiago", "Explícito en documento", "Extracción directa",
  "Tramo literal.", "Extraer de la página legal o portada.", "Coincidencia literal.", "P3", "A", "No aplica: dato autónomo", "F15", "E3", "R3")

# =====================================================================================
# D02 PROCEDENCIA INSTITUCIONAL Y CUSTODIA
# =====================================================================================
F("MDJ-D02-001", "organismo_emisor", "Organismo emisor", "D02", "NOR; JUR; ADM", "Obra",
  "Entidad pública o institución a la que el ordenamiento atribuye el acto (quien lo dicta), normalizada al registro de organismos.",
  "Es criterio central de los especialistas actuales y de la fuerza jurídica; distinto del custodio y de la fuente de publicación.",
  "Referencia", "1 obligatorio", "Referencia a Entidad: organismo u órgano.", "ORG-PE-CONGRESO",
  "Normalizado por regla", "Extracción directa + Normalización",
  "Tramo literal con la denominación del emisor (MDJ-D02-003).",
  "Extraer la denominación del emisor del encabezado, sello o firma; mapear al registro considerando sus denominaciones históricas a la fecha de emisión. Para leyes, el emisor es el órgano legislativo; el promulgante va en MDJ-D02-008.",
  "Existe en el registro; el organismo estaba vigente a la fecha de emisión; país coherente con MDJ-D01-004.",
  "P0", "A", "MDJ-D02-003; registro de organismos; fecha de emisión (D03)", "F01; F02; F03; F07; F09",
  "E3", "R2", country_status="Catálogo por país", pending="DEC-33",
  obs="En doctrina la autoría institucional se registra en MDJ-D02-010/011; las personas autoras en D13.")

F("MDJ-D02-002", "organo_emisor", "Órgano interno emisor", "D02", "JUR; ADM", "Obra",
  "Órgano o dependencia dentro del organismo que dicta el acto (sala, sección, dirección, intendencia, tribunal administrativo).",
  "En tribunales y entidades grandes, el órgano interno determina la especialidad, la instancia y a veces la fuerza del pronunciamiento.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Entidad: organismo u órgano (nivel órgano, hijo del organismo emisor).",
  "ORG-PE-CSJ-SALA-CONST-SOC-2", "Normalizado por regla", "Extracción directa + Normalización",
  "Tramo literal con la denominación del órgano.",
  "Extraer la sala o dependencia del encabezado; mapear al registro como hijo de MDJ-D02-001 con la denominación vigente a la fecha.",
  "Debe ser descendiente de MDJ-D02-001 en la jerarquía de organismos.",
  "P0", "A", "MDJ-D02-001", "F01; F03; F07; F08",
  "E3", "R2", cond="Obligatorio cuando el emisor actúa a través de una sala o dependencia identificada.",
  country_status="Catálogo por país")

F("MDJ-D02-003", "denominacion_emisor_original", "Denominación literal del emisor", "D02", "UNI", "Obra",
  "Nombre del emisor tal como aparece en el documento.",
  "Es la evidencia de MDJ-D02-001 y permite detectar denominaciones nuevas o históricas.",
  "String", "1 obligatorio", NA_VAL, "SALA DE DERECHO CONSTITUCIONAL Y SOCIAL PERMANENTE",
  "Explícito en documento", "Extracción directa", "Tramo literal.",
  "Transcribir la denominación del emisor del encabezado o sello.", "Coincidencia literal con la manifestación.",
  "P0", "A", "No aplica: dato literal", "F16", "E3", "R2",
  cond="En doctrina, la institución editora si figura como responsable.")

F("MDJ-D02-004", "coemisores", "Organismos coemisores", "D02", "NOR; ADM", "Obra",
  "Otros organismos que dictan conjuntamente el acto (resoluciones o decretos conjuntos).",
  "Los actos conjuntos se pierden si solo se registra un emisor.",
  "Array de referencias", "0..n", "Referencias a Entidad: organismo u órgano.", "[ORG-CO-MINHACIENDA, ORG-CO-MINTRABAJO]",
  "Normalizado por regla", "Extracción directa + Normalización", "Tramo literal del encabezado o firmas.",
  "Extraer los organismos que figuran como coautores del acto en encabezado o fórmula de expedición; no incluir a quienes solo refrendan.",
  "Distintos de MDJ-D02-001; existentes en el registro.", "P1", "A", "MDJ-D02-001", "F01; F03", "E3", "R2",
  country_status="Catálogo por país")

F("MDJ-D02-005", "firmantes", "Firmantes", "D02", "NOR; JUR; ADM", "Obra",
  "Autoridades que firman el acto, con su cargo y rol de firma (promulga, refrenda, suscribe, certifica).",
  "Permite verificar la formación del acto, identificar refrendos ministeriales y la composición que decidió.",
  "Array", "0..n", "Cada elemento: persona (Entidad: persona, solo funcionarios), cargo literal, rol (CAT-103 Rol de firma).",
  "[{persona: PER-..., cargo: 'Ministra de Trabajo', rol: refrenda}]", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo literal del bloque de firmas.", "Extraer nombre y cargo del bloque de firmas; clasificar el rol con CAT-103.",
  "Cada firmante tiene cargo; rol válido; se aplican las reglas de minimización a personas que no sean funcionarios.",
  "P1", "A", "Política de datos personales (DEC-18)", "F03; F07; F17", "E3", "R2",
  privacy="Dato de funcionario público", pending="DEC-18; DEC-19",
  obs="Solo funcionarios en ejercicio de su cargo. Su uso para estadísticas individuales queda fuera del alcance inicial (DEC-19).")

F("MDJ-D02-006", "ponente", "Magistrado o vocal ponente", "D02", "JUR; ADM", "Obra",
  "Juez, magistrado o vocal designado como ponente o redactor de la resolución.",
  "Dato de identificación usual en la cita de sentencias y útil para el análisis jurisprudencial.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: persona (funcionario).", "PER-CO-MAG-0045",
  "Explícito en documento", "Extracción directa + Normalización", "Tramo literal ('Magistrado ponente', 'Vocal ponente').",
  "Extraer solo cuando el documento lo declara expresamente; no inferir del orden de firmas.",
  "Coincide con un firmante o con la composición del órgano.", "P1", "A", "MDJ-D02-005; MDJ-D02-007", "F03; F07", "E3", "R2",
  privacy="Dato de funcionario público", pending="DEC-19",
  obs="Uso en analítica individual de magistrados fuera del alcance inicial (DEC-19).")

F("MDJ-D02-007", "composicion_organo", "Composición del órgano que decide", "D02", "JUR; ADM", "Obra",
  "Magistrados, jueces o vocales que integran el órgano en la resolución, con su sentido de voto si consta.",
  "Necesario para determinar mayorías, quórum y requisitos de formación de precedentes.",
  "Array", "0..n", "Cada elemento: persona (funcionario) + sentido de voto (mayoría, singular, discordia, aclaración; catálogo de D17/D05).",
  "[{persona: PER-..., voto: mayoria}]", "Explícito en documento", "Extracción directa + Normalización",
  "Tramo literal de la integración y firmas.", "Extraer la lista de integrantes del encabezado o firmas; el sentido de voto solo si consta expresamente.",
  "Número de integrantes coherente con el tipo de órgano; sin duplicados.", "P1", "A", "MDJ-D02-002", "F07; F08", "E3", "R2",
  privacy="Dato de funcionario público", pending="DEC-19; DEC-25",
  obs="La votación y quórum como requisito del precedente se calcula en D17.")

F("MDJ-D02-008", "autoridad_promulgadora", "Autoridad que promulga", "D02", "NOR", "Obra",
  "Autoridad que promulga u ordena publicar una norma aprobada por otro órgano (p. ej. el Ejecutivo respecto de una ley del Congreso).",
  "Distingue el órgano que aprueba del que promulga, frecuente en leyes; relevante para fechas y fórmulas de promulgación.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: organismo u órgano.", "ORG-PE-PRESIDENCIA",
  "Normalizado por regla", "Extracción directa + Normalización", "Fórmula de promulgación literal.",
  "Extraer de la fórmula de promulgación ('Por tanto: mando se publique y cumpla') la autoridad que promulga.",
  "Distinta del emisor salvo que el ordenamiento las confunda.", "P2", "A", "MDJ-D02-001", "F06", "E3", "R2",
  cond="Solo normas aprobadas por un órgano y promulgadas por otro.", country_status="Catálogo por país")

F("MDJ-D02-009", "lugar_emision", "Lugar de emisión", "D02", "NOR; JUR; ADM", "Obra",
  "Ciudad o lugar donde se dicta el acto según el propio documento.",
  "Identifica la sede de órganos con presencia territorial y apoya la desambiguación de órganos homónimos.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: territorio o jurisdicción (localidad).", "Lima",
  "Explícito en documento", "Extracción directa + Normalización", "Tramo literal ('Lima, 12 de marzo de 2020').",
  "Extraer el lugar que precede a la fecha de emisión o a las firmas.", "Existe en el catálogo territorial del país.",
  "P2", "A", "Catálogo territorial (DEC-28)", "F03; F09", "E3", "R3", country_status="Catálogo por país", pending="DEC-28")

F("MDJ-D02-010", "editorial", "Editorial", "D02", "DOC", "Versión",
  "Casa editora responsable de la publicación de la obra doctrinal en una edición.",
  "Dato bibliográfico estándar y señal de procedencia de la doctrina.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: organismo u órgano (tipo editorial).", "ORG-CL-EDIT-0012",
  "Normalizado por regla", "Extracción directa + Normalización", "Tramo literal de la página legal.",
  "Extraer de la página legal o portada; mapear al registro.", "Existe en el registro de organismos.", "P1", "A", "No aplica: dato autónomo", "F03", "E3", "R3")

F("MDJ-D02-011", "institucion_academica", "Institución académica responsable", "D02", "DOC", "Obra",
  "Universidad, facultad, instituto o centro responsable de una tesis, documento de trabajo o revista académica.",
  "En tesis y revistas universitarias la institución es la autoría institucional relevante (los archivos de Bolivia se organizan así).",
  "Referencia", "0..1 opcional", "Referencia a Entidad: organismo u órgano (tipo universidad o centro).", "ORG-BO-UMSA",
  "Normalizado por regla", "Extracción directa + Normalización", "Tramo literal de la portada.",
  "Extraer de la portada de tesis o de la cabecera de la revista.", "Existe en el registro.", "P1", "A", "MDJ-D04-012", "F03; F04", "E3", "R3")

F("MDJ-D02-012", "programa_academico", "Programa o grado académico", "D02", "DOC", "Obra",
  "Programa, carrera o grado al que se presenta una tesis o trabajo académico.",
  "Distingue tesis de pregrado, maestría y doctorado y su especialidad.",
  "String", "0..1 opcional", NA_VAL, "Maestría en Derecho del Trabajo", "Explícito en documento", "Extracción directa",
  "Tramo literal de la portada.", "Extraer de la portada de la tesis.", "Coincidencia literal.", "P2", "A", "MDJ-D04-013", "F03", "E3", "R3",
  cond="Solo tesis y trabajos académicos.")

F("MDJ-D02-013", "fuente_obtencion", "Fuente de obtención", "D02", "UNI", "Manifestación",
  "Fuente (portal, repositorio, base de datos, diario oficial) de la que Juztina obtuvo el archivo.",
  "Determina la confiabilidad y las condiciones de uso de la copia y permite actualizarla.",
  "Referencia", "1 obligatorio", "Referencia a Entidad: publicación o fuente.", "FTE-CL-BCN-LEYCHILE",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Registrar al capturar o heredar de la base actual de Juztina; si se desconoce, 'Indeterminado'.",
  "Existe en el catálogo de fuentes.", "P0", "A", "Catálogo de fuentes", "F16; F17", "E0", "R2",
  obs="La base actual podría no registrar la fuente de todos los documentos: dato a verificar con ingeniería.")

F("MDJ-D02-014", "custodio", "Entidad custodio", "D02", "UNI", "Manifestación",
  "Institución que conserva o aloja el documento y facilita su acceso, cuando es distinta del emisor (p. ej. un centro que custodia laudos de tribunales arbitrales).",
  "La arquitectura exige distinguir emisor y custodio; es clave en laudos, actas y repositorios académicos.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: organismo u órgano.", "ORG-INT-CIADI",
  "Normalizado por regla", "Extracción directa + Normalización", "Fuente de captura o mención del custodio.",
  "Registrar la institución responsable del repositorio de donde proviene el archivo cuando no coincide con el emisor.",
  "Si coincide con el emisor, no se duplica (estado 'No aplicable').", "P1", "A", "MDJ-D02-013; MDJ-D02-001", "F16", "E0", "R3")

F("MDJ-D02-015", "publicacion_oficial", "Publicación oficial de la obra", "D02", "NOR; ADM", "Obra",
  "Diario, gaceta o boletín oficial en que se publicó la obra con efectos jurídicos.",
  "La publicación oficial condiciona la vigencia y es la fuente de verificación del texto.",
  "Referencia", "0..1 obligatorio condicionado", "Referencia a Entidad: publicación o fuente (tipo diario oficial).", "FTE-PE-ELPERUANO",
  "Explícito en documento", "Extracción directa + Normalización", "Tramo literal (cabecera del diario o mención de publicación).",
  "Extraer de la cabecera de la edición o de la nota de publicación; en textos consolidados, de la nota editorial (modo importado).",
  "Tipo de publicación = diario oficial; país coherente.", "P0", "A", "MDJ-D02-042 Tipo de publicación o fuente", "F05; F06; F15", "E3", "R2",
  cond="Normas y actos que se publican oficialmente.", country_status="Catálogo por país")

F("MDJ-D02-016", "edicion_publicacion_oficial", "Edición o suplemento de la publicación oficial", "D02", "NOR; ADM", "Obra",
  "Número de edición, suplemento, edición especial o tomo del diario oficial en que se publicó la obra.",
  "Identifica de forma inequívoca la publicación y permite verificarla.",
  "String", "0..1 opcional", NA_VAL, "Registro Oficial Suplemento 123",
  "Explícito en documento", "Extracción directa", "Tramo literal.",
  "Extraer de la cabecera o nota de publicación el número de edición y, si existe, suplemento o edición especial.",
  "Coincidencia literal.", "P1", "A", "MDJ-D02-015", "F15; F16", "E3", "R3", country_status="Catálogo por país", pending="DEC-17",
  obs="La estructura de ediciones y suplementos difiere por país y debe validarse.")

F("MDJ-D02-017", "pagina_publicacion_oficial", "Página en la publicación oficial", "D02", "NOR; ADM", "Obra",
  "Página o rango de páginas de la publicación oficial donde aparece la obra.", "Permite citar y verificar.",
  "String", "0..1 opcional", NA_VAL, "p. 15", "Explícito en documento", "Extracción directa", "Tramo literal o numeración.",
  "Extraer la numeración de página de la edición.", "Coincidencia literal.", "P2", "A", "MDJ-D02-015", "F15", "E3", "R3")

F("MDJ-D02-018", "tipo_texto_manifestacion", "Tipo de texto de la manifestación", "D02", "UNI", "Manifestación",
  "Indica si el archivo contiene el texto original publicado, un texto consolidado oficial, un consolidado editorial, una compilación oficial, un extracto o una traducción.",
  "Condiciona qué versión representa la manifestación y el modo de origen (oficial o editorial) de las notas de modificación.",
  "Enum", "1 obligatorio", "CAT-104 Tipo de texto de la manifestación.", "consolidado_editorial",
  "Inferido por modelo", "Clasificación", "Señales del texto (notas '(*) Modificado por…', cabecera de la fuente) y tipo de fuente.",
  "Clasificar con CAT-104 usando la fuente y la presencia de notas de modificación o de cabecera de diario oficial; si no es determinable, 'desconocido'.",
  "Coherente con el carácter oficial de la fuente (MDJ-D02-043).", "P0", "A", "MDJ-D02-013; MDJ-D02-043", "F05; F06; F16", "E0", "R1",
  review="Condicionado", obs="Determina si las notas de modificación se registran como evento importado de fuente editorial.")

F("MDJ-D02-019", "fecha_captura", "Fecha y hora de captura", "D02", "UNI", "Manifestación",
  "Momento en que Juztina obtuvo el archivo.", "Fecha de corte de lo que la copia puede reflejar; base del tiempo de registro.",
  "Datetime", "1 obligatorio", "No aplica: ISO 8601 con zona horaria.", "2026-09-29T21:09:15Z",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Registrar al capturar; en documentos legados, usar la fecha de incorporación disponible y marcar 'aproximada'.",
  "No posterior a la fecha de incorporación.", "P0", "A", "No aplica: dato de ingesta", "F05; F16", "E0", "R3")

F("MDJ-D02-020", "metodo_captura", "Método de captura", "D02", "UNI", "Manifestación",
  "Forma en que se obtuvo el archivo (descarga directa, API, rastreo web, carga manual, migración, digitalización).",
  "Explica la calidad esperada y la reproducibilidad de la captura.",
  "Enum", "1 obligatorio", "CAT-105 Método de captura.", "migracion_legada",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Registrar al ingerir.", "Valor de CAT-105.", "P0", "A", "No aplica: dato de ingesta", "F16", "E0", "R3")

F("MDJ-D02-021", "lote_incorporacion", "Lote de incorporación", "D02", "UNI", "Manifestación",
  "Identificador del lote o proceso de ingesta en que la manifestación entró al repositorio.",
  "Permite auditar e invalidar o reprocesar lotes completos.",
  "Identificador", "1 obligatorio", "No aplica: identificador de lote.", "LOTE-2026-11-PE-NOR-003",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS, "Asignar al ingerir.", "Existe en el registro de lotes.",
  "P0", "A", "No aplica: dato de ingesta", "F16", "E0", "R3")

F("MDJ-D02-022", "fecha_incorporacion", "Fecha de incorporación al repositorio", "D02", "UNI", "Manifestación",
  "Momento en que la manifestación quedó registrada en el repositorio de Juztina.",
  "Base del tiempo de registro en el modelo bitemporal (qué sabía Juztina y cuándo).",
  "Datetime", "1 obligatorio", "No aplica: ISO 8601.", "2026-11-30T10:00:00Z",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS, "Registrar al ingerir.", "No anterior a la fecha de captura.",
  "P0", "A", "MDJ-D02-019", "F05; F16", "E0", "R3")

F("MDJ-D02-023", "manifestacion_origen", "Manifestación de origen", "D02", "UNI", "Manifestación",
  "Manifestación de la que deriva esta (p. ej. texto extraído u OCR de un PDF, conversión de formato).",
  "Conserva la cadena de custodia entre el archivo original y sus derivados.",
  "Referencia", "0..1 opcional", "Referencia a MDJ-D01-003.", "MAN-000184232",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS, "Registrar cuando la manifestación se genera por transformación de otra.",
  "La referencia existe y no forma ciclos.", "P0", "A", "MDJ-D01-003", "F16", "E0", "R3")

F("MDJ-D02-024", "estado_enlace_fuente", "Estado del enlace de la fuente", "D02", "UNI", "Manifestación",
  "Resultado de la última verificación del enlace a la fuente (responde, no responde, redirige, retirado).",
  "Los mapas de fuentes de Bolivia muestran enlaces intermitentes; sin este dato no se sabe si la copia sigue disponible en origen.",
  "Enum", "0..1 opcional", "CAT-106 Estado del enlace.", "verificado_abre",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS, "Verificar periódicamente la URL de captura u oficial.",
  "Valor de CAT-106 con fecha (MDJ-D02-025).", "P2", "D", "MDJ-D01-021; MDJ-D01-022", "F16", "Sistema", "R3")

F("MDJ-D02-025", "fecha_verificacion_enlace", "Fecha de verificación del enlace", "D02", "UNI", "Manifestación",
  "Fecha de la última verificación del enlace a la fuente.", "Da vigencia al estado del enlace.",
  "Datetime", "0..1 opcional", "No aplica: ISO 8601.", "2026-09-29T00:00:00Z",
  "Generado por sistema", "Generado por sistema", NA_EVID_SYS, "Registrar con cada verificación.", "No futura.",
  "P2", "D", "MDJ-D02-024", "F16", "Sistema", "R3")

# --- Entidad: organismo u órgano ---
F("MDJ-D02-026", "nombre_oficial_organismo", "Nombre oficial del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Denominación oficial vigente del organismo u órgano.", "Valor de presentación y búsqueda de emisores, custodios y editoriales.",
  "String", "1 obligatorio", NA_VAL, "Superintendencia Nacional de Fiscalización Laboral", "Curado por persona", "Revisión humana",
  "Norma de creación o fuente oficial que la sustenta.", "Cargar por curaduría a partir de fuentes oficiales; los nombres detectados en E3 que no existan generan propuestas pendientes.",
  "Único dentro del país y periodo.", "P0", "D", "No aplica: entrada maestra", "F03; F18", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-13")

F("MDJ-D02-027", "siglas_organismo", "Siglas del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Siglas y abreviaturas usadas para el organismo.", "Necesarias para reconocer emisores y referencias (\"SUNAT\", \"SII\", \"DIAN\").",
  "Array", "0..n", NA_VAL, "['SUNAFIL']", "Curado por persona", "Revisión humana", "Fuente oficial.",
  "Cargar por curaduría; aceptar propuestas desde E3.", "Una sigla ambigua dentro del país se marca como tal.", "P0", "D", "MDJ-D02-026", "F03; F18", "Curaduría", "R2",
  country_status="Catálogo por país")

F("MDJ-D02-028", "denominaciones_historicas", "Denominaciones históricas", "D02", "UNI", "Entidad: organismo u órgano",
  "Nombres anteriores del organismo con su intervalo de uso.", "Las entidades cambian de nombre; sin historia no se reconoce al emisor de documentos antiguos.",
  "Array", "0..n", "Cada elemento: nombre + fecha desde + fecha hasta + norma que dispuso el cambio.",
  "[{nombre: 'Ministerio de Trabajo y Promoción Social', hasta: '2002-07-05'}]", "Curado por persona", "Revisión humana",
  "Norma que dispuso el cambio de denominación.", "Cargar por curaduría; las denominaciones detectadas sin correspondencia se proponen para revisión.",
  "Intervalos sin superposición.", "P0", "D", "MDJ-D02-026", "F03; F06; F18", "Curaduría", "R2", country_status="Catálogo por país")

F("MDJ-D02-029", "tipo_organismo", "Tipo funcional del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Categoría pivote que describe la función del organismo (legislativo, ministerio, regulador, tribunal, tribunal administrativo, gobierno subnacional, editorial, universidad…).",
  "Permite agrupar emisores comparables entre países sin afirmar equivalencia jurídica.",
  "Enum", "1 obligatorio", "CAT-107 Tipo funcional de organismo.", "regulador_sectorial", "Curado por persona", "Revisión humana",
  "Norma de creación o fuente oficial.", "Asignar por curaduría con la función principal del organismo.", "Valor de CAT-107.",
  "P0", "D", "MDJ-D02-026", "F01; F09; F10", "Curaduría", "R2", country_status="Pendiente validación nacional", pending="DEC-14")

F("MDJ-D02-030", "poder_publico", "Poder o rama pública", "D02", "UNI", "Entidad: organismo u órgano",
  "Poder del Estado o esfera a la que pertenece el organismo (legislativo, ejecutivo, judicial, autónomo, control, electoral, no estatal, supranacional).",
  "Necesario para el rango y la naturaleza de sus actos y para comparar.",
  "Enum", "1 obligatorio", "CAT-108 Poder público.", "judicial", "Curado por persona", "Revisión humana",
  "Fuente oficial.", "Asignar por curaduría.", "Valor de CAT-108.", "P0", "D", "MDJ-D02-026", "F03; F09", "Curaduría", "R2",
  country_status="Pendiente validación nacional")

F("MDJ-D02-031", "nivel_gobierno_organismo", "Nivel de gobierno del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Nivel territorial del organismo (nacional o federal, intermedio, local, autónomo, supranacional).",
  "Determina si sus actos son nacionales o subnacionales y su ámbito territorial.",
  "Enum", "1 obligatorio", "CAT-004 Nivel de gobierno.", "nacional", "Curado por persona", "Revisión humana",
  "Fuente oficial.", "Asignar por curaduría.", "Valor de CAT-004; coherente con MDJ-D02-032.", "P0", "D", "MDJ-D02-026", "F03; F05; F09", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-28")

F("MDJ-D02-032", "territorio_organismo", "Territorio del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Entidad territorial sobre la que el organismo ejerce competencia o en la que tiene su sede.",
  "Distingue órganos homónimos de distintos distritos o entidades subnacionales.",
  "Referencia", "1 obligatorio", "Referencia a Entidad: territorio o jurisdicción.", "PE-LIM", "Curado por persona", "Revisión humana",
  "Fuente oficial.", "Asignar por curaduría.", "Existe en el catálogo territorial.", "P0", "D", "Catálogo territorial", "F03; F09", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-28")

F("MDJ-D02-033", "organismo_superior", "Organismo superior", "D02", "UNI", "Entidad: organismo u órgano",
  "Organismo del que depende jerárquicamente el órgano (sala respecto de la corte, dirección respecto del ministerio).",
  "Construye la jerarquía institucional y permite agregar por organismo.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: organismo u órgano.", "ORG-PE-CSJ", "Curado por persona", "Revisión humana",
  "Fuente oficial (reglamento de organización).", "Asignar por curaduría.", "Sin ciclos en la jerarquía.", "P0", "D", "MDJ-D02-026", "F03; F12", "Curaduría", "R2",
  country_status="Catálogo por país")

F("MDJ-D02-034", "fecha_creacion_organismo", "Fecha de creación del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Fecha desde la que el organismo existe jurídicamente.", "Valida que un documento no se atribuya a un organismo inexistente a su fecha.",
  "Fecha parcial", "0..1 opcional", "No aplica: fecha ISO o año.", "2013-01-15", "Curado por persona", "Revisión humana",
  "Norma de creación.", "Cargar por curaduría.", "Anterior a la fecha de extinción.", "P1", "D", "MDJ-D02-026", "F18", "Curaduría", "R3", country_status="Catálogo por país")

F("MDJ-D02-035", "fecha_extincion_organismo", "Fecha de extinción del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Fecha en que el organismo dejó de existir o de ejercer funciones.", "Evita atribuir actos posteriores a un organismo extinto y orienta la sucesión.",
  "Fecha parcial", "0..1 opcional", "No aplica: fecha ISO o año.", "2002-07-05", "Curado por persona", "Revisión humana",
  "Norma de extinción.", "Cargar por curaduría.", "Posterior a la creación.", "P1", "D", "MDJ-D02-026", "F18", "Curaduría", "R3", country_status="Catálogo por país")

F("MDJ-D02-036", "sucesion_organismo", "Sucesión institucional", "D02", "UNI", "Entidad: organismo u órgano",
  "Organismos que suceden a este, con el tipo de sucesión (cambio de nombre, fusión, absorción, escisión).",
  "Permite seguir competencias y documentos a través de reorganizaciones administrativas.",
  "Array", "0..n", "Cada elemento: organismo sucesor + tipo (CAT-109 Tipo de sucesión institucional) + fecha + norma.",
  "[{sucesor: ORG-..., tipo: absorcion, fecha: 2013-01-15}]", "Curado por persona", "Revisión humana", "Norma que dispone la sucesión.",
  "Cargar por curaduría.", "Tipo válido; fecha coherente con la extinción.", "P1", "D", "MDJ-D02-035", "F06; F18", "Curaduría", "R2", country_status="Catálogo por país")

F("MDJ-D02-037", "competencias_materiales_organismo", "Competencias materiales del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Materias de la taxonomía sobre las que el organismo tiene competencia.",
  "Sustenta los especialistas actuales (que filtran por emisor) y la validación de clasificaciones.",
  "Array de referencias", "0..n", "Referencias a Entidad: concepto de taxonomía (facetas F2 y F5).", "[Laboral › Inspección del trabajo]",
  "Curado por persona", "Revisión humana", "Norma de creación o de funciones.", "Asignar por curaduría a partir de la norma de funciones.",
  "Conceptos activos de la taxonomía.", "P1", "D", "Taxonomía (D06)", "F01; F10; F18", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-13")

F("MDJ-D02-038", "grado_jurisdiccional_organo", "Grado o posición jurisdiccional del órgano", "D02", "JUR; ADM", "Entidad: organismo u órgano",
  "Posición del órgano en la estructura jurisdiccional o administrativa de revisión (primera instancia, apelación, casación o suprema, constitucional, última instancia administrativa, arbitral).",
  "Insumo para la instancia del pronunciamiento y para las reglas de precedente.",
  "Enum", "0..1 obligatorio condicionado", "CAT-110 Grado jurisdiccional del órgano.", "casacion_suprema", "Curado por persona", "Revisión humana",
  "Ley orgánica o reglamento del órgano.", "Asignar por curaduría.", "Valor de CAT-110.", "P1", "D", "MDJ-D02-026", "F07; F08", "Curaduría", "R2",
  cond="Solo órganos jurisdiccionales o de revisión administrativa.", country_status="Pendiente validación nacional", pending="DEC-25")

F("MDJ-D02-039", "clave_auxiliar_organismo", "Clave auxiliar del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Identificador oficial externo del organismo (registro tributario u otro) usado como clave auxiliar.",
  "Ayuda a deduplicar organismos y cruzar con fuentes externas.",
  "Array", "0..n", "Cada elemento: tipo de clave + valor.", "[{tipo: RUC, valor: '20555195444'}]", "Fuente externa", "Enriquecimiento externo",
  "Fuente externa identificada.", "Cargar desde registros oficiales cuando estén disponibles.", "Formato válido para el tipo de clave.",
  "P3", "D", "MDJ-D02-026", "F18", "Curaduría", "R3", country_status="Pendiente validación nacional", pending="DEC-33")

F("MDJ-D02-040", "url_institucional_organismo", "Sitio web oficial del organismo", "D02", "UNI", "Entidad: organismo u órgano",
  "Dirección web oficial del organismo.", "Permite verificar denominaciones y localizar fuentes oficiales.",
  "URL", "0..1 opcional", NA_VAL, "https://www.sunafil.gob.pe", "Curado por persona", "Revisión humana", "Fuente oficial.",
  "Cargar por curaduría.", "URL válida.", "P3", "D", "MDJ-D02-026", "F16; F18", "Curaduría", "R3")

# --- Entidad: publicación o fuente ---
F("MDJ-D02-041", "nombre_publicacion_fuente", "Nombre de la publicación o fuente", "D02", "UNI", "Entidad: publicación o fuente",
  "Nombre de la publicación (diario oficial, revista) o de la fuente digital (portal, repositorio, base de datos).",
  "Identifica publicaciones oficiales, revistas doctrinales y fuentes de obtención.",
  "String", "1 obligatorio", NA_VAL, "Diario Oficial El Peruano", "Curado por persona", "Revisión humana", "Fuente oficial o sitio de la publicación.",
  "Cargar por curaduría; propuestas desde E3 se revisan.", "Único por país y tipo.", "P0", "D", "No aplica: entrada maestra", "F03; F16; F18", "Curaduría", "R3",
  country_status="Catálogo por país")

F("MDJ-D02-042", "tipo_publicacion_fuente", "Tipo de publicación o fuente", "D02", "UNI", "Entidad: publicación o fuente",
  "Clase de publicación o fuente (diario oficial, boletín subnacional, repositorio oficial de normas, repositorio judicial, portal institucional, revista jurídica, repositorio académico, base comercial, índice).",
  "Necesario para distinguir publicación oficial de fuente de obtención y para evaluar confiabilidad.",
  "Enum", "1 obligatorio", "CAT-111 Tipo de publicación o fuente.", "diario_oficial", "Curado por persona", "Revisión humana", "Fuente oficial.",
  "Asignar por curaduría.", "Valor de CAT-111.", "P0", "D", "MDJ-D02-041", "F16; F18", "Curaduría", "R2")

F("MDJ-D02-043", "caracter_oficial_fuente", "Carácter oficial de la fuente", "D02", "UNI", "Entidad: publicación o fuente",
  "Indica si la fuente publica textos con valor oficial, oficial solo informativo o no oficial.",
  "Determina si un texto o una nota de modificación pueden tratarse como dato oficial o editorial.",
  "Enum", "1 obligatorio", "CAT-112 Carácter oficial de la fuente.", "oficial_informativo", "Curado por persona", "Revisión humana",
  "Norma o declaración de la fuente sobre su valor oficial.", "Asignar por curaduría; en caso de duda, 'no_determinado'.", "Valor de CAT-112.",
  "P0", "D", "MDJ-D02-041", "F05; F06; F16", "Curaduría", "R1", country_status="Pendiente validación nacional", pending="DEC-17",
  obs="El valor jurídico de las versiones electrónicas y de los consolidados oficiales debe validarlo cada país.")

F("MDJ-D02-044", "issn_publicacion", "ISSN e e-ISSN", "D02", "DOC", "Entidad: publicación o fuente",
  "Números ISSN impreso y electrónico de la revista.", "Identifican la revista de forma persistente y permiten cruzar con índices.",
  "Array", "0..n", "Cada elemento: tipo (impreso, electrónico) + valor ####-####.", "[{tipo: electronico, valor: '3007-5335'}]",
  "Explícito en documento", "Extracción directa + Normalización", "Tramo literal o fuente del índice.",
  "Extraer del pie o portada de la revista o de su sitio; curar en el catálogo.", "Dígito de control válido.", "P1", "A", "MDJ-D02-041", "F03; F16", "E3", "R3")

F("MDJ-D02-045", "periodicidad_publicacion", "Periodicidad", "D02", "DOC", "Entidad: publicación o fuente",
  "Frecuencia de aparición de la revista o publicación.", "Ayuda a detectar lagunas de cobertura y a planificar actualizaciones.",
  "Enum", "0..1 opcional", "CAT-113 Periodicidad.", "semestral", "Curado por persona", "Revisión humana", "Sitio de la publicación.",
  "Cargar por curaduría.", "Valor de CAT-113.", "P3", "D", "MDJ-D02-041", "F16", "Curaduría", "R3")

F("MDJ-D02-046", "entidad_responsable_publicacion", "Entidad responsable de la publicación", "D02", "UNI", "Entidad: publicación o fuente",
  "Organismo o institución que edita o administra la publicación o fuente.", "Vincula la fuente con su responsable institucional (p. ej. BCN para LeyChile).",
  "Referencia", "1 obligatorio", "Referencia a Entidad: organismo u órgano.", "ORG-CL-BCN", "Curado por persona", "Revisión humana", "Sitio de la fuente.",
  "Cargar por curaduría.", "Existe en el registro de organismos.", "P1", "D", "MDJ-D02-041", "F16; F18", "Curaduría", "R3")

F("MDJ-D02-047", "pais_publicacion", "País de la publicación o fuente", "D02", "UNI", "Entidad: publicación o fuente",
  "País o jurisdicción de la publicación o fuente.", "Agrupa fuentes por país y valida la coherencia con las obras.",
  "Código ISO", "1 obligatorio", "CAT-001 País y jurisdicción.", "CL", "Curado por persona", "Revisión humana", "Sitio de la fuente.",
  "Cargar por curaduría.", "Valor de CAT-001.", "P0", "D", "MDJ-D02-041", "F03; F16", "Curaduría", "R3")

F("MDJ-D02-048", "url_publicacion", "Sitio de la publicación o fuente", "D02", "UNI", "Entidad: publicación o fuente",
  "Dirección web principal de la publicación o fuente.", "Permite capturas futuras y verificación.",
  "URL", "0..1 opcional", NA_VAL, "https://www.bcn.cl/leychile", "Curado por persona", "Revisión humana", "Sitio de la fuente.",
  "Cargar por curaduría.", "URL válida.", "P2", "D", "MDJ-D02-041", "F16", "Curaduría", "R3")

F("MDJ-D02-049", "cobertura_temporal_fuente", "Cobertura temporal de la fuente", "D02", "UNI", "Entidad: publicación o fuente",
  "Periodo de documentos que la fuente cubre, según la propia fuente o la verificación de Juztina.",
  "Permite saber qué lagunas tiene el corpus y si una vigencia calculada puede estar incompleta.",
  "Intervalo de fechas", "0..1 opcional", "No aplica: intervalo ISO.", "1990-01-01/2026-09-29", "Curado por persona", "Revisión humana",
  "Declaración de la fuente o verificación.", "Cargar por curaduría.", "Inicio anterior al fin.", "P2", "D", "MDJ-D02-041", "F05; F16", "Curaduría", "R2",
  obs="Insumo para la advertencia de completitud del corpus en el cálculo de vigencia.")

# =====================================================================================
# D04 NATURALEZA Y TIPOLOGÍA
# =====================================================================================
F("MDJ-D04-001", "categoria_coleccion", "Categoría de colección", "D04", "UNI", "Obra",
  "Categoría de la colección de Juztina en que se guarda la obra: normativa, jurisprudencia, actos administrativos o doctrina.",
  "Organización operativa actual de la base; se conserva sin migrar documentos.",
  "Enum", "1 obligatorio", "CAT-002 Categoría de colección.", "actos_administrativos",
  "Fuente externa", "Enriquecimiento externo", "Registro de la base actual.",
  "Heredar de la colección de la base actual; para documentos nuevos, usar la categoría por defecto del tipo documental (MDJ-D04-021).",
  "Valor de CAT-002.", "P0", "A", "MDJ-D01-020; MDJ-D04-021", "F01; F02; F03", "E1", "R3", pending="DEC-07",
  obs="No expresa la naturaleza jurídica (MDJ-D04-002). La colección de los tipos limítrofes está pendiente (DEC-07).")

F("MDJ-D04-002", "naturaleza_juridica", "Naturaleza jurídica", "D04", "UNI", "Obra",
  "Qué es la obra jurídicamente, según el catálogo pivote de naturalezas (norma con rango de ley, decisión jurisdiccional, pronunciamiento interpretativo administrativo, decisión arbitral, doctrina académica…).",
  "Determina perfil documental, fuerza, efectos y relaciones posibles; permite consultas transversales a las colecciones.",
  "Enum", "1 obligatorio", "CAT-003 Naturaleza jurídica.", "pronunciamiento_interpretativo_administrativo",
  "Derivado por cálculo", "Cálculo + Inferencia", "Tipo documental aplicado y, si hubo inferencia, tramo que la sustenta.",
  "Calcular desde la naturaleza por defecto del tipo documental (MDJ-D04-022). Si el tipo es ambiguo o no catalogado, inferir con el texto y marcar como interpretado.",
  "Valor de CAT-003; si es inferido, requiere evidencia; coherente con el perfil documental aplicado.",
  "P1", "B", "MDJ-D04-004; MDJ-D04-022", "F01; F02; F03; F04; F08", "E7", "R2", review="Condicionado",
  country_status="Pendiente validación nacional", pending="DEC-07; DEC-08",
  obs="Revisión humana cuando la naturaleza se infiere y no proviene del mapeo validado del tipo.")

F("MDJ-D04-003", "tipo_documental_original", "Tipo documental tal como figura", "D04", "UNI", "Obra",
  "Denominación del tipo documental tal como aparece en el documento (\"Decreto de Urgencia\", \"Auto Supremo\", \"Oficio\").",
  "Es la evidencia del tipo normalizado y conserva la denominación original exigida por la arquitectura.",
  "String", "1 obligatorio", NA_VAL, "Decreto Supremo", "Explícito en documento", "Extracción directa",
  "Tramo literal del encabezado.", "Transcribir la palabra o expresión que denomina el tipo en el encabezado.",
  "Coincidencia literal.", "P0", "A", "Estructura del encabezado (E2)", "F03; F16", "E1", "R2")

F("MDJ-D04-004", "tipo_documental", "Tipo documental normalizado", "D04", "UNI", "Obra",
  "Tipo documental del país al que corresponde la obra, normalizado al catálogo de tipos documentales por país.",
  "Clave para naturaleza, rango, plantilla de numeración y fuerza; criterio de los especialistas actuales.",
  "Referencia", "1 obligatorio", "Referencia a Entidad: tipo documental (catálogo por país CAT-126).", "TD-PE-DECRETO-SUPREMO",
  "Normalizado por regla", "Normalización", "Evidencia de MDJ-D04-003 y regla de mapeo.",
  "Mapear MDJ-D04-003 a una entrada del catálogo del país y periodo usando denominaciones y variantes (MDJ-D04-019).",
  "Entrada existente del país de la obra y vigente a la fecha de emisión; si no existe, estado 'Indeterminado' y propuesta de nueva entrada.",
  "P0", "A", "MDJ-D04-003; MDJ-D01-004", "F01; F02; F03; F09", "E1", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D04-005", "subtipo_documental", "Subtipo documental", "D04", "UNI", "Obra",
  "Subtipo dentro del tipo documental del país (p. ej. sentencia de casación frente a sentencia de apelación; decreto reglamentario frente a decreto autónomo).",
  "Activa los perfiles de subtipo y distingue efectos y estructura.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: tipo documental (nivel hijo).", "TD-PE-SENT-CASACION",
  "Inferido por modelo", "Clasificación", "Tramo del encabezado o del objeto que lo sustenta.",
  "Clasificar entre los subtipos del tipo normalizado usando encabezado y objeto del acto.",
  "Debe ser hijo de MDJ-D04-004.", "P1", "A", "MDJ-D04-004", "F01; F03; F07", "E3", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D04-006", "tipo_pivote", "Tipo documental pivote", "D04", "UNI", "Obra",
  "Clase conceptual común asignada al tipo documental del país mediante el mapeo del catálogo.",
  "Permite encontrar instrumentos comparables entre países sin afirmar equivalencia jurídica.",
  "Referencia", "1 obligatorio", "CAT-114 Tipo documental pivote.", "norma_rango_ley_ejecutivo",
  "Derivado por cálculo", "Cálculo", "Mapeo del tipo documental (MDJ-D04-023).", "Copiar el pivote del tipo documental de la obra.",
  "Valor de CAT-114.", "P1", "B", "MDJ-D04-004; MDJ-D04-023", "F09; F03", "E7", "R2",
  country_status="Pendiente validación nacional", pending="DEC-14",
  obs="Va siempre acompañado del tipo de equivalencia del mapeo (MDJ-D04-024).")

F("MDJ-D04-007", "rango_normativo", "Rango normativo según el ordenamiento", "D04", "NOR; ADM", "Obra",
  "Rango que el ordenamiento del país asigna al tipo de la obra (constitucional, legal, reglamentario…), con la denominación nacional.",
  "Es la base de la jerarquía normativa y de la resolución de conflictos.",
  "Enum", "0..1 obligatorio condicionado", "CAT-125 Rango normativo por país (semilla).", "PE: rango de ley",
  "Derivado por cálculo", "Cálculo", "Rango del tipo documental (MDJ-D04-026).", "Copiar el rango del tipo documental.",
  "Valor del catálogo del país.", "P1", "B", "MDJ-D04-004; MDJ-D04-026", "F03; F04; F09", "E7", "R2",
  cond="Normas y actos generales.", country_status="Pendiente validación nacional", pending="DEC-08; DEC-04")

F("MDJ-D04-008", "nivel_normativo_pivote", "Nivel normativo pivote", "D04", "NOR; ADM", "Obra",
  "Nivel común (constitucional, supranacional, legal, infralegal reglamentario, infralegal administrativo, subnacional) para comparar normas entre países.",
  "Permite comparar y filtrar por nivel sin un número de rango universal.",
  "Enum", "0..1 obligatorio condicionado", "CAT-115 Nivel normativo pivote.", "legal", "Derivado por cálculo", "Cálculo",
  "Nivel del tipo documental (MDJ-D04-027).", "Copiar del tipo documental.", "Valor de CAT-115.", "P1", "B", "MDJ-D04-027", "F09; F03", "E7", "R2",
  cond="Normas y actos generales.", country_status="Pendiente validación nacional", pending="DEC-08")

F("MDJ-D04-009", "alcance_acto", "Alcance general o particular", "D04", "ADM; NOR", "Obra",
  "Indica si el acto tiene destinatarios generales e indeterminados, particulares y determinados, o ambos.",
  "Separa actos normativos de decisiones individuales y decide el perfil (normativo o contencioso) aplicable.",
  "Enum", "1 obligatorio", "CAT-117 Alcance del acto.", "particular", "Inferido por modelo", "Clasificación",
  "Tramo de la parte resolutiva o del objeto que identifica a los destinatarios.",
  "Clasificar según los destinatarios de la parte resolutiva: un administrado identificado = particular; categoría abierta de sujetos = general.",
  "Valor de CAT-117; coherente con la naturaleza jurídica.", "P1", "A", "MDJ-D04-002", "F01; F03; F13", "E3", "R2",
  cond="Actos administrativos y normas emitidas por la Administración.")

F("MDJ-D04-010", "funcion_acto_administrativo", "Función del acto administrativo", "D04", "ADM", "Obra",
  "Función principal del acto: decisoria, sancionadora, interpretativa, normativa, organizativa o instrucción interna, habilitante o registral, resolutoria de recurso.",
  "Elige el perfil de extracción y diferencia los pronunciamientos que interpretan de los que aplican la normativa.",
  "Enum", "1 obligatorio", "CAT-118 Función del acto administrativo.", "interpretativa", "Inferido por modelo", "Clasificación",
  "Tramo de la parte resolutiva o del objeto.", "Clasificar por lo que dispone la parte resolutiva; si interpreta una norma en respuesta a consulta, 'interpretativa'.",
  "Valor de CAT-118.", "P1", "A", "MDJ-D04-002", "F01; F03; F10", "E3", "R2",
  obs="La función jurídica por unidad (faceta F11) se registra en D06; este campo describe el acto completo.")

F("MDJ-D04-011", "es_documento_compuesto", "Documento compuesto o híbrido", "D04", "UNI", "Obra",
  "Indica que la obra combina contenidos de distinta naturaleza (p. ej. revista jurisprudencial que reproduce sentencias, resolución que transcribe íntegramente otra).",
  "Controla el riesgo de forzar una sola naturaleza y de atribuir contenido reproducido a la obra.",
  "Boolean", "1 obligatorio", "No aplica: verdadero o falso.", "true", "Inferido por modelo", "Clasificación",
  "Tramos de los contenidos reproducidos.", "Marcar verdadero cuando más de una obra identificable esté reproducida dentro de la obra o cuando su soporte y contenido tengan naturalezas distintas.",
  "Si es verdadero, debe existir al menos una referencia o relación 'reproduce' (D07).", "P1", "A", "Referencias (D07)", "F04; F16", "E3", "R2", review="Condicionado")

F("MDJ-D04-012", "tipo_publicacion_doctrinal", "Tipo de publicación doctrinal", "D04", "DOC", "Obra",
  "Clase de obra doctrinal (artículo de revista, libro, capítulo, tesis de pregrado, maestría o doctorado, ponencia, comentario jurisprudencial, informe, manual, reseña).",
  "Activa perfiles doctrinales y es señal de autoridad junto con el nivel académico.",
  "Enum", "1 obligatorio", "CAT-119 Tipo de publicación doctrinal.", "articulo_revista", "Normalizado por regla", "Clasificación",
  "Portada, cabecera o tipo de fuente.", "Clasificar usando portada (\"Tesis para optar…\"), cabecera de revista o metadatos de la fuente.",
  "Valor de CAT-119.", "P1", "A", "MDJ-D02-042", "F03; F04", "E3", "R2")

F("MDJ-D04-013", "nivel_academico", "Nivel académico", "D04", "DOC", "Obra",
  "Nivel de la obra doctrinal: pregrado, maestría, doctorado, investigación arbitrada, divulgación o estudiantil.",
  "Criterio usado en los mapas de fuentes de doctrina (columna 'Nivel') y señal objetiva de autoridad.",
  "Enum", "1 obligatorio", "CAT-120 Nivel académico.", "maestria", "Inferido por modelo", "Clasificación",
  "Portada o tipo de revista.", "Clasificar a partir del grado declarado en tesis o del tipo de revista.", "Valor de CAT-120.",
  "P1", "A", "MDJ-D04-012", "F03; F04", "E3", "R3")

F("MDJ-D04-014", "tipo_pronunciamiento_judicial", "Tipo de pronunciamiento judicial (pivote)", "D04", "JUR", "Obra",
  "Clase pivote del pronunciamiento judicial (sentencia definitiva, sentencia de casación, sentencia de control constitucional, auto, decreto o providencia, sentencia de reemplazo, criterio extractado).",
  "Distingue pronunciamientos con distinto valor y estructura entre países sin igualar sus denominaciones nacionales.",
  "Enum", "1 obligatorio", "CAT-121 Tipo de pronunciamiento judicial.", "sentencia_casacion", "Derivado por cálculo", "Cálculo + Inferencia",
  "Tipo y subtipo documental; tramo del encabezado si se infiere.", "Derivar del subtipo documental; si no está catalogado, inferir del encabezado y la parte resolutiva.",
  "Valor de CAT-121.", "P1", "B", "MDJ-D04-004; MDJ-D04-005", "F07; F08; F09", "E7", "R2",
  country_status="Pendiente validación nacional", pending="DEC-08; DEC-25")

F("MDJ-D04-015", "es_compilacion_oficial", "Compilación oficial (texto ordenado o refundido)", "D04", "NOR", "Obra",
  "Indica que la obra es un acto que compila y reordena el texto de otra norma (Texto Único Ordenado, texto ordenado, texto refundido).",
  "La arquitectura trata estas obras como propias, con relación 'ordena o refunde' y correspondencias de unidades.",
  "Boolean", "1 obligatorio", "No aplica: verdadero o falso.", "true", "Derivado por cálculo", "Cálculo + Inferencia",
  "Tipo documental o tramo del título ('Texto Único Ordenado de…').", "Derivar del tipo documental; si no basta, detectar en el título la fórmula de compilación.",
  "Si es verdadero, debe existir relación 'ordena o refunde' hacia la obra compilada (D07).", "P1", "B", "MDJ-D04-004; MDJ-D01-010", "F06; F11", "E7", "R2",
  countries="PE; AR; CL", country_status="Pendiente validación nacional", pending="DEC-04",
  obs="Identificado en PE, AR y CL; existencia de figuras similares en CO, EC, BO y MX pendiente de validación.")

F("MDJ-D04-016", "tipo_documental_legado", "Tipo documental en la base actual", "D04", "UNI", "Obra",
  "Tipo documental con que la base actual de Juztina registra el documento.",
  "Permite contrastar la normalización nueva con los criterios con que se construyeron los especialistas.",
  "String", "0..1 opcional", NA_VAL, "Resolución Directoral", "Fuente externa", "Enriquecimiento externo", "Registro de la base actual.",
  "Copiar el valor del registro de la base actual.", "No aplica validación de contenido; se conserva tal cual.", "P0", "D", "MDJ-D01-020", "F01; F16", "E0", "R3",
  obs="Esquema real de la base actual desconocido.")

# --- Entidad: tipo documental ---
F("MDJ-D04-017", "pais_tipo_documental", "País del tipo documental", "D04", "UNI", "Entidad: tipo documental",
  "País o pseudo jurisdicción al que pertenece la entrada del catálogo de tipos.", "Un tipo solo se interpreta junto con su país.",
  "Código ISO", "1 obligatorio", "CAT-001 País y jurisdicción.", "PE", "Curado por persona", "Revisión humana", "No aplica: dato de catálogo.",
  "Cargar por curaduría.", "Valor de CAT-001.", "P0", "D", "No aplica: entrada maestra", "F18", "Curaduría", "R2", country_status="Catálogo por país")

F("MDJ-D04-018", "denominacion_original_tipo", "Denominación original del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Nombre del tipo documental en el ordenamiento del país.", "Conserva la denominación original como exige la arquitectura.",
  "String", "1 obligatorio", NA_VAL, "Decreto de Necesidad y Urgencia", "Curado por persona", "Revisión humana", "Norma que regula el tipo.",
  "Cargar por curaduría.", "Única dentro del país y periodo.", "P0", "D", "MDJ-D04-017", "F03; F18", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D04-019", "variantes_denominacion_tipo", "Variantes de denominación del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Formas alternativas y abreviaturas con que el tipo aparece en los documentos (equivalencia terminológica dentro del país).",
  "Son la base del mapeo del tipo original al tipo normalizado.",
  "Array", "0..n", NA_VAL, "['DNU', 'Decreto de necesidad y urgencia']", "Curado por persona", "Revisión humana", "Documentos de muestra.",
  "Cargar por curaduría y por propuestas desde E1.", "Una variante no puede mapear a dos tipos del mismo país sin regla de desambiguación.",
  "P0", "D", "MDJ-D04-018", "F03; F18", "Curaduría", "R2", country_status="Catálogo por país")

F("MDJ-D04-020", "periodo_existencia_tipo", "Periodo de existencia del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Intervalo durante el cual el tipo existió en el ordenamiento.", "Evita mapear documentos a tipos que no existían a su fecha.",
  "Intervalo de fechas", "0..1 opcional", "No aplica: intervalo ISO.", "1994-08-24/..", "Curado por persona", "Revisión humana", "Norma que crea o suprime el tipo.",
  "Cargar por curaduría.", "Inicio anterior al fin.", "P1", "D", "MDJ-D04-018", "F06; F18", "Curaduría", "R2",
  country_status="Pendiente validación nacional", pending="DEC-08")

F("MDJ-D04-021", "categoria_coleccion_por_defecto", "Categoría de colección por defecto del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Colección en la que Juztina guarda por defecto los documentos de este tipo.", "Regla de carga para documentos nuevos.",
  "Enum", "1 obligatorio", "CAT-002 Categoría de colección.", "actos_administrativos", "Curado por persona", "Revisión humana", "Decisión de producto.",
  "Asignar por decisión de producto.", "Valor de CAT-002.", "P0", "D", "MDJ-D04-018", "F01; F18", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-07")

F("MDJ-D04-022", "naturaleza_juridica_por_defecto", "Naturaleza jurídica por defecto del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Naturaleza jurídica que corresponde a los documentos de este tipo salvo indicación en contrario.", "Permite calcular la naturaleza de la obra sin inferencia.",
  "Enum", "1 obligatorio", "CAT-003 Naturaleza jurídica.", "norma_rango_ley", "Curado por persona", "Revisión humana", "Norma que regula el tipo y validación del responsable del país.",
  "Asignar por el responsable jurídico del país.", "Valor de CAT-003.", "P0", "D", "MDJ-D04-018", "F01; F02; F18", "Curaduría", "R1",
  review="Sí", country_status="Pendiente validación nacional", pending="DEC-08")

F("MDJ-D04-023", "tipo_pivote_asignado", "Tipo pivote asignado al tipo", "D04", "UNI", "Entidad: tipo documental",
  "Clase pivote común a la que se vincula el tipo del país.", "Habilita la comparación entre países.",
  "Enum", "1 obligatorio", "CAT-114 Tipo documental pivote.", "norma_rango_ley_ejecutivo", "Curado por persona", "Revisión humana",
  "Justificación del mapeo.", "Asignar por el comité taxonómico con validación del responsable del país.", "Valor de CAT-114.",
  "P0", "D", "MDJ-D04-018", "F09; F18", "Curaduría", "R2", review="Sí", country_status="Pendiente validación nacional", pending="DEC-14")

F("MDJ-D04-024", "tipo_equivalencia_pivote", "Tipo de equivalencia con el pivote", "D04", "UNI", "Entidad: tipo documental",
  "Grado de equivalencia entre el tipo nacional y su pivote (terminológica, semejanza funcional, equivalencia jurídica, sin equivalente, falso amigo).",
  "Impide que el asistente presente como equivalentes tipos que solo son comparables.",
  "Enum", "1 obligatorio", "CAT-012 Tipo de equivalencia entre países.", "semejanza_funcional", "Curado por persona", "Revisión humana",
  "Nota de diferencias (MDJ-D04-025).", "Asignar con el mapeo; 'equivalencia jurídica' solo con validación de todos los países involucrados.",
  "Valor de CAT-012; 'equivalencia_juridica' exige validación registrada.", "P0", "D", "MDJ-D04-023", "F09; F18", "Curaduría", "R1",
  review="Sí", country_status="Pendiente validación nacional", pending="DEC-14")

F("MDJ-D04-025", "nota_diferencias_regimen", "Nota de diferencias de régimen", "D04", "UNI", "Entidad: tipo documental",
  "Explicación de las diferencias jurídicas entre el tipo nacional y el pivote o los tipos comparables de otros países.",
  "Hace explícito por qué una semejanza no es equivalencia.",
  "Texto largo", "0..1 obligatorio condicionado", NA_VAL, "El DNU argentino y el decreto de urgencia peruano difieren en materias habilitadas y control posterior.",
  "Curado por persona", "Revisión humana", "Fuentes normativas citadas.", "Redactar por el responsable del país.",
  "Obligatoria si la equivalencia no es terminológica ni jurídica.", "P1", "D", "MDJ-D04-024", "F09", "Curaduría", "R2",
  review="Sí", country_status="Pendiente validación nacional", pending="DEC-14")

F("MDJ-D04-026", "rango_normativo_tipo", "Rango normativo del tipo", "D04", "NOR; ADM", "Entidad: tipo documental",
  "Rango que el ordenamiento asigna al tipo documental.", "Insumo del rango de cada obra.",
  "Enum", "0..1 obligatorio condicionado", "CAT-125 Rango normativo por país (semilla).", "PE: rango de ley", "Curado por persona", "Revisión humana",
  "Norma constitucional o legal que fija el rango.", "Asignar por el responsable del país.", "Valor del catálogo del país.",
  "P0", "D", "MDJ-D04-018", "F03; F18", "Curaduría", "R1", review="Sí", country_status="Pendiente validación nacional", pending="DEC-08; DEC-04")

F("MDJ-D04-027", "nivel_normativo_pivote_tipo", "Nivel normativo pivote del tipo", "D04", "NOR; ADM", "Entidad: tipo documental",
  "Nivel común del tipo para comparación.", "Insumo del nivel pivote de cada obra.",
  "Enum", "0..1 obligatorio condicionado", "CAT-115 Nivel normativo pivote.", "infralegal_reglamentario", "Curado por persona", "Revisión humana",
  "Justificación del mapeo.", "Asignar por el comité con validación del país.", "Valor de CAT-115.", "P0", "D", "MDJ-D04-018", "F09; F18", "Curaduría", "R2",
  review="Sí", country_status="Pendiente validación nacional", pending="DEC-08")

F("MDJ-D04-028", "criterio_ordenacion_tipo", "Criterio de ordenación del tipo", "D04", "NOR; ADM", "Entidad: tipo documental",
  "Indica si la relación del tipo con otros se ordena por jerarquía, por competencia o de forma mixta.",
  "En ordenamientos con autonomías la prevalencia depende de la competencia, no de un rango lineal.",
  "Enum", "0..1 opcional", "CAT-116 Criterio de ordenación.", "competencia", "Curado por persona", "Revisión humana", "Norma constitucional.",
  "Asignar por el responsable del país.", "Valor de CAT-116.", "P2", "D", "MDJ-D04-018", "F04; F09", "Curaduría", "R2",
  review="Sí", country_status="Pendiente validación nacional", pending="DEC-08")

F("MDJ-D04-029", "organos_emisores_habituales", "Órganos emisores habituales del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Organismos que pueden emitir documentos de este tipo.", "Valida la coherencia emisor-tipo en la extracción.",
  "Array de referencias", "0..n", "Referencias a Entidad: organismo u órgano o a tipos funcionales (CAT-107).", "[ORG-PE-PRESIDENCIA]",
  "Curado por persona", "Revisión humana", "Norma que regula el tipo.", "Cargar por curaduría.", "Organismos existentes.", "P2", "D", "MDJ-D04-018", "F16; F18", "Curaduría", "R3",
  country_status="Catálogo por país")

F("MDJ-D04-030", "tipo_padre", "Tipo documental padre", "D04", "UNI", "Entidad: tipo documental",
  "Tipo del que este es subtipo.", "Construye la jerarquía tipo-subtipo usada por MDJ-D04-005.",
  "Referencia", "0..1 opcional", "Referencia a Entidad: tipo documental.", "TD-PE-SENTENCIA", "Curado por persona", "Revisión humana", "No aplica: estructura del catálogo.",
  "Cargar por curaduría.", "Sin ciclos; mismo país.", "P1", "D", "MDJ-D04-018", "F18", "Curaduría", "R3", country_status="Catálogo por país")

F("MDJ-D04-031", "patron_numeracion_tipo", "Patrón de numeración del tipo", "D04", "UNI", "Entidad: tipo documental",
  "Plantilla o expresión regular que describe cómo se numeran los documentos del tipo en el país y periodo.",
  "Permite detectar, validar y normalizar números oficiales y resolver citas.",
  "String", "0..n", "No aplica: expresión regular o plantilla documentada.", "^\\d{3}-\\d{4}-[A-Z]{2,6}$", "Curado por persona", "Revisión humana",
  "Muestras de documentos reales.", "Definir por curaduría a partir de muestras del corpus en el piloto.",
  "Probado contra muestras; sin falsos positivos conocidos.", "P0", "D", "MDJ-D04-018", "F03; F11; F16", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-08")

F("MDJ-D04-032", "base_normativa_tipo", "Base normativa del tipo", "D04", "NOR; JUR; ADM", "Entidad: tipo documental",
  "Norma o normas que crean o regulan el tipo documental y sus efectos.", "Sustenta rango, naturaleza y fuerza asignados al tipo.",
  "Array de referencias", "0..n", "Referencias a obras o unidades estructurales.", "[Constitución Política del Perú, art. 118 inc. 19]",
  "Curado por persona", "Revisión humana", "La propia norma referida.", "Registrar por el responsable del país.", "Referencias resueltas.",
  "P2", "D", "MDJ-D04-018", "F04; F18", "Curaduría", "R2", review="Sí", country_status="Pendiente validación nacional", pending="DEC-08")

F("MDJ-D04-033", "estado_validacion_tipo", "Estado de validación de la entrada", "D04", "UNI", "Entidad: tipo documental",
  "Situación de la entrada del catálogo: semilla, en revisión, validada por el responsable del país, deprecada.",
  "Evita usar como validadas entradas que todavía no revisó un especialista nacional.",
  "Enum", "1 obligatorio", "CAT-124 Estado de validación de entrada de catálogo.", "semilla", "Curado por persona", "Revisión humana",
  "Registro de la validación (responsable y fecha).", "Actualizar en cada revisión.", "Valor de CAT-124.", "P0", "D", "MDJ-D04-018", "F18", "Curaduría", "R2",
  country_status="Catálogo por país", pending="DEC-13")

# =====================================================================================
# D15 LENGUA Y FORMA
# =====================================================================================
F("MDJ-D15-001", "idioma_principal", "Idioma principal", "D15", "UNI", "Manifestación",
  "Idioma predominante del texto de la manifestación.", "Necesario para el procesamiento lingüístico y para laudos y doctrina en otros idiomas.",
  "Código ISO", "1 obligatorio", "CAT-009 Idioma.", "es", "Inferido por modelo", "Clasificación", "Muestra del texto.",
  "Detectar automáticamente sobre el texto normalizado.", "Valor de CAT-009.", "P0", "A", "Texto normalizado (E0)", "F02; F03; F16", "E0", "R3")

F("MDJ-D15-002", "idiomas_adicionales", "Idiomas adicionales", "D15", "UNI", "Manifestación",
  "Otros idiomas presentes en partes relevantes del texto (incluidas lenguas indígenas).", "Detecta textos bilingües y versiones en lenguas originarias.",
  "Array", "0..n", "CAT-009 Idioma.", "['qu']", "Inferido por modelo", "Clasificación", "Tramos en otro idioma.",
  "Detectar segmentos extensos en otro idioma.", "Valores de CAT-009 distintos del principal.", "P2", "A", "MDJ-D15-001", "F03; F09", "E0", "R3")

F("MDJ-D15-003", "es_traduccion", "Es traducción", "D15", "UNI", "Manifestación",
  "Indica que la manifestación es traducción de un texto en otro idioma.", "Una traducción no es el texto auténtico; condiciona su uso como evidencia.",
  "Boolean", "1 obligatorio", "No aplica: verdadero o falso.", "false", "Explícito en documento", "Extracción directa + Inferencia",
  "Tramo que declara la traducción o fuente.", "Marcar verdadero si el texto o la fuente lo declaran como traducción.", "Si es verdadero, MDJ-D15-004 es obligatorio.",
  "P1", "A", "MDJ-D02-013", "F15; F16", "E0", "R2")

F("MDJ-D15-004", "caracter_traduccion", "Carácter de la traducción", "D15", "UNI", "Manifestación",
  "Indica si la traducción es oficial, no oficial o de carácter desconocido.", "Solo una traducción oficial puede usarse como texto auténtico.",
  "Enum", "0..1 obligatorio condicionado", "CAT-123 Carácter oficial de la traducción.", "no_oficial", "Explícito en documento", "Extracción directa + Normalización",
  "Declaración de la fuente.", "Tomar de la declaración del documento o de la fuente.", "Obligatorio si MDJ-D15-003 es verdadero.", "P1", "A", "MDJ-D15-003", "F15", "E0", "R2")

F("MDJ-D15-005", "manifestacion_traducida_de", "Manifestación original traducida", "D15", "UNI", "Manifestación",
  "Manifestación que contiene el texto original del que esta es traducción.", "Vincula traducción y original para mostrar el auténtico.",
  "Referencia", "0..1 opcional", "Referencia a MDJ-D01-003.", "MAN-000200001", "Derivado por cálculo", "Cálculo", "Coincidencia de identidad de obra.",
  "Vincular manifestaciones de la misma obra con distinto idioma.", "Misma obra; distinto idioma.", "P3", "B", "MDJ-D15-003; MDJ-D01-001", "F15", "E7", "R3")

F("MDJ-D15-006", "formato_archivo", "Formato del archivo de origen", "D15", "UNI", "Manifestación",
  "Formato del archivo ingerido (PDF nativo, PDF escaneado, HTML, DOCX, TXT, XML, imagen).", "Determina la necesidad de OCR y la calidad esperada de la segmentación.",
  "Enum", "1 obligatorio", "CAT-122 Formato de archivo.", "pdf_escaneado", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Detectar por tipo MIME y presencia de capa de texto.", "Valor de CAT-122.", "P0", "A", "MDJ-D15-007", "F16", "E0", "R3")

F("MDJ-D15-007", "tipo_mime", "Tipo MIME", "D15", "UNI", "Manifestación",
  "Tipo de medio del archivo según su contenido binario.", "Insumo técnico del formato y del procesamiento.",
  "String", "1 obligatorio", "No aplica: tipo MIME IANA.", "application/pdf", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Detectar por firma binaria.", "Tipo MIME registrado.", "P0", "A", "No aplica: dato de ingesta", "F16", "E0", "R3")

F("MDJ-D15-008", "numero_paginas", "Número de páginas", "D15", "UNI", "Manifestación",
  "Cantidad de páginas del archivo, cuando el formato es paginado.", "Base para citar páginas, estimar costo y controlar completitud.",
  "Integer", "0..1 obligatorio condicionado", "No aplica: entero positivo.", "48", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Contar páginas del archivo.", "Mayor que cero si el formato es paginado.", "P0", "A", "MDJ-D15-006", "F16", "E0", "R3")

F("MDJ-D15-009", "tamano_archivo_bytes", "Tamaño del archivo", "D15", "UNI", "Manifestación",
  "Tamaño del archivo en bytes.", "Control técnico y estimación de costo de procesamiento.",
  "Integer", "1 obligatorio", "No aplica: entero positivo.", "1048576", "Generado por sistema", "Generado por sistema", NA_EVID_SYS,
  "Medir al ingerir.", "Mayor que cero.", "P0", "A", "No aplica: dato de ingesta", "F16", "E0", "R3")


# =====================================================================================
# CATÁLOGOS CAT-100..CAT-199
# =====================================================================================
def V(code, label, definition, parent="", synonyms="", country="", status="", notes=""):
    d = dict(code=code, label=label, definition=definition)
    for k, v in (("parent", parent), ("synonyms", synonyms), ("country", country), ("status", status), ("notes", notes)):
        if v:
            d[k] = v
    return d


SEM = "Semilla — pendiente de validación nacional"

CATALOGS = [
    dict(cat_id="CAT-101", cat_name="Tipo de identificador oficial",
         cat_def="Clases de identificadores oficiales adicionales que una obra puede tener, además de su número principal.",
         values=[
             V("numero_resolucion", "Número de resolución", "Número propio de una resolución judicial o administrativa distinto del número principal."),
             V("codigo_sentencia_tipificado", "Código tipificado de sentencia", "Código que combina tipo de proceso y número (p. ej. C-, T-, SU- en CO).", country="CO", status=SEM),
             V("rol", "Rol", "Número de rol de una causa usado como identificador de la resolución.", country="CL", status=SEM),
             V("registro_digital_sjf", "Registro digital del Semanario Judicial", "Número de registro digital de tesis y ejecutorias.", country="MX", status=SEM),
             V("referencia_fallos", "Referencia en colección oficial de fallos", "Tomo y página en una colección oficial de fallos (p. ej. Fallos: tomo:página en AR).", country="AR", status=SEM),
             V("numero_caso_internacional", "Número de caso internacional", "Identificador de caso en un órgano internacional o arbitral (p. ej. ARB/xx/x)."),
             V("doi", "DOI", "Identificador de objeto digital."),
             V("isbn", "ISBN", "Número internacional normalizado del libro."),
             V("otro", "Otro", "Identificador oficial no catalogado; requiere nota."),
         ]),
    dict(cat_id="CAT-102", cat_name="Estado de deduplicación",
         cat_def="Resultado de comparar una obra con las ya registradas.",
         values=[
             V("unica", "Única", "No coincide con ninguna obra registrada."),
             V("candidato_duplicado", "Candidata a duplicado", "Coincidencia parcial; requiere revisión."),
             V("duplicado_confirmado", "Duplicado confirmado", "Coincidencia confirmada; se fusiona con la obra que prevalece."),
             V("fusionada", "Fusionada", "Identificador redirigido a la obra que prevalece."),
         ]),
    dict(cat_id="CAT-103", cat_name="Rol de firma",
         cat_def="Función con que una autoridad suscribe un acto.",
         values=[
             V("promulga", "Promulga", "Ordena la publicación y cumplimiento de una norma aprobada por otro órgano."),
             V("refrenda", "Refrenda", "Suscribe como ministro o autoridad que asume responsabilidad del acto del Ejecutivo."),
             V("suscribe", "Suscribe", "Firma como autor del acto."),
             V("integra", "Integra el órgano", "Firma como integrante de un órgano colegiado."),
             V("certifica", "Certifica", "Da fe del acto (secretario, relator)."),
         ]),
    dict(cat_id="CAT-104", cat_name="Tipo de texto de la manifestación",
         cat_def="Relación entre el texto del archivo y el texto oficial de la obra.",
         values=[
             V("original_publicado", "Original publicado", "Texto tal como se publicó oficialmente por primera vez."),
             V("consolidado_oficial", "Consolidado oficial", "Texto actualizado con sus modificaciones por una fuente oficial."),
             V("consolidado_editorial", "Consolidado editorial", "Texto actualizado por una fuente no oficial o editorial."),
             V("compilacion_oficial", "Compilación oficial", "Texto de un acto que compila y reordena otra norma."),
             V("extracto", "Extracto o sumilla", "Fragmento o resumen del documento, no el texto completo."),
             V("traduccion", "Traducción", "Traducción a otro idioma."),
             V("desconocido", "Desconocido", "No determinable con la información disponible."),
         ]),
    dict(cat_id="CAT-105", cat_name="Método de captura",
         cat_def="Forma en que se obtuvo el archivo.",
         values=[
             V("descarga_directa", "Descarga directa", "Descarga individual desde una URL."),
             V("api", "API", "Obtención mediante una interfaz programática de la fuente."),
             V("rastreo_web", "Rastreo web", "Obtención automatizada por rastreo de páginas."),
             V("carga_manual", "Carga manual", "Archivo cargado por una persona."),
             V("migracion_legada", "Migración legada", "Archivo proveniente de la base actual de Juztina."),
             V("digitalizacion", "Digitalización", "Escaneo de un documento físico."),
         ]),
    dict(cat_id="CAT-106", cat_name="Estado del enlace",
         cat_def="Resultado de verificar una URL de fuente.",
         values=[
             V("verificado_abre", "Verificado (abre)", "La URL responde con el documento."),
             V("redirige", "Redirige", "La URL redirige a otra dirección."),
             V("no_responde", "No responde", "Error o tiempo de espera."),
             V("contenido_distinto", "Contenido distinto", "Responde con contenido que no corresponde."),
             V("retirado", "Retirado", "La fuente declara el documento retirado."),
         ]),
    dict(cat_id="CAT-107", cat_name="Tipo funcional de organismo",
         cat_def="Categoría pivote de función del organismo, sin afirmar equivalencia jurídica entre países.",
         values=[
             V("organo_legislativo", "Órgano legislativo", "Congreso, asamblea o parlamento."),
             V("jefatura_ejecutivo", "Jefatura del Ejecutivo", "Presidencia o jefatura de gobierno."),
             V("ministerio", "Ministerio o secretaría", "Órgano del Ejecutivo central sectorial."),
             V("organismo_autonomo_constitucional", "Organismo autónomo constitucional", "Entidad con autonomía reconocida constitucionalmente."),
             V("regulador_sectorial", "Regulador sectorial", "Entidad que regula un sector económico."),
             V("superintendencia_fiscalizador", "Superintendencia o fiscalizador", "Entidad de supervisión y fiscalización."),
             V("administracion_tributaria", "Administración tributaria o aduanera", "Entidad que administra tributos."),
             V("organo_jurisdiccional", "Órgano jurisdiccional", "Tribunal o juzgado del Poder Judicial."),
             V("tribunal_constitucional", "Tribunal o corte constitucional", "Órgano de control constitucional concentrado."),
             V("tribunal_administrativo", "Tribunal administrativo", "Órgano administrativo que resuelve controversias en última instancia administrativa."),
             V("organo_control", "Órgano de control", "Contraloría o similar."),
             V("gobierno_subnacional", "Gobierno subnacional", "Provincia, estado, región, departamento, municipio."),
             V("organismo_internacional", "Organismo o tribunal internacional", "Órgano supranacional o internacional."),
             V("centro_arbitraje", "Centro de arbitraje o conciliación", "Institución que administra arbitrajes o conciliaciones."),
             V("universidad_centro", "Universidad o centro académico", "Institución académica."),
             V("editorial", "Editorial", "Casa editora."),
             V("otro", "Otro", "Tipo no catalogado; requiere nota."),
         ]),
    dict(cat_id="CAT-108", cat_name="Poder público",
         cat_def="Poder o esfera a la que pertenece un organismo.",
         values=[
             V("legislativo", "Legislativo", "Poder legislativo."),
             V("ejecutivo", "Ejecutivo", "Poder ejecutivo y administración pública."),
             V("judicial", "Judicial", "Poder judicial."),
             V("autonomo", "Autónomo", "Órganos constitucionalmente autónomos."),
             V("control", "Control", "Órganos de control."),
             V("electoral", "Electoral", "Órganos electorales."),
             V("no_estatal", "No estatal", "Instituciones privadas, académicas, arbitrales o comunitarias."),
             V("supranacional", "Supranacional", "Órganos de integración o internacionales."),
         ]),
    dict(cat_id="CAT-109", cat_name="Tipo de sucesión institucional",
         cat_def="Forma en que un organismo sucede a otro.",
         values=[
             V("cambio_nombre", "Cambio de nombre", "Mismo organismo con nueva denominación."),
             V("fusion", "Fusión", "Dos o más organismos se integran en uno nuevo."),
             V("absorcion", "Absorción", "Un organismo existente asume a otro que se extingue."),
             V("escision", "Escisión", "Un organismo se divide en varios."),
             V("extincion_sin_sucesor", "Extinción sin sucesor", "El organismo se extingue sin sucesor."),
         ]),
    dict(cat_id="CAT-110", cat_name="Grado jurisdiccional del órgano",
         cat_def="Posición del órgano en la estructura de instancias, sin igualar denominaciones nacionales.",
         values=[
             V("primera_instancia", "Primera instancia", "Órgano que conoce en primer grado."),
             V("apelacion", "Segunda instancia o apelación", "Órgano que revisa decisiones de primera instancia."),
             V("casacion_suprema", "Casación o corte suprema", "Máximo órgano de la justicia ordinaria o de casación."),
             V("constitucional", "Constitucional", "Órgano de control constitucional."),
             V("especial", "Jurisdicción especial", "Jurisdicciones especiales (electoral, indígena, de paz, militar, transicional)."),
             V("administrativa_ultima", "Última instancia administrativa", "Órgano administrativo que agota la vía."),
             V("administrativa_otra", "Otra instancia administrativa", "Órgano administrativo de primera o segunda instancia."),
             V("arbitral", "Arbitral", "Tribunal arbitral."),
             V("internacional", "Internacional", "Tribunal internacional o supranacional."),
         ]),
    dict(cat_id="CAT-111", cat_name="Tipo de publicación o fuente",
         cat_def="Clase de publicación o fuente de documentos.",
         values=[
             V("diario_oficial", "Diario oficial nacional", "Publicación oficial del Estado."),
             V("boletin_subnacional", "Boletín o gaceta subnacional", "Publicación oficial de una entidad subnacional."),
             V("repositorio_oficial_normas", "Repositorio oficial de normas", "Sistema estatal de información normativa."),
             V("repositorio_judicial", "Repositorio judicial oficial", "Portal de jurisprudencia de un órgano jurisdiccional."),
             V("portal_institucional", "Portal institucional", "Sitio de una entidad pública."),
             V("revista_juridica", "Revista jurídica", "Publicación periódica de doctrina."),
             V("repositorio_academico", "Repositorio académico", "Repositorio institucional de tesis o publicaciones."),
             V("base_comercial", "Base de datos o editorial comercial", "Fuente privada de pago."),
             V("indice_bibliografico", "Índice o hemeroteca", "Índice o agregador bibliográfico."),
             V("repositorio_internacional", "Repositorio internacional", "Base de datos de un organismo internacional o centro arbitral."),
             V("otro", "Otro", "No catalogado."),
         ]),
    dict(cat_id="CAT-112", cat_name="Carácter oficial de la fuente",
         cat_def="Valor jurídico de los textos que publica la fuente.",
         values=[
             V("oficial_con_valor_legal", "Oficial con valor legal", "La publicación tiene efectos jurídicos (p. ej. diario oficial)."),
             V("oficial_informativo", "Oficial informativo", "Fuente estatal cuyos textos no reemplazan la publicación oficial."),
             V("no_oficial", "No oficial", "Fuente privada, académica o editorial."),
             V("no_determinado", "No determinado", "Carácter pendiente de verificación."),
         ]),
    dict(cat_id="CAT-113", cat_name="Periodicidad",
         cat_def="Frecuencia de aparición de una publicación.",
         values=[V(c, l, d) for c, l, d in [
             ("diaria", "Diaria", "Aparece cada día hábil."), ("semanal", "Semanal", "Una vez por semana."),
             ("mensual", "Mensual", "Una vez por mes."), ("trimestral", "Trimestral", "Cuatro veces por año."),
             ("semestral", "Semestral", "Dos veces por año."), ("anual", "Anual", "Una vez por año."),
             ("irregular", "Irregular", "Sin periodicidad fija."), ("continua", "Publicación continua", "Publica artículos a medida que se aprueban.")]]),
    dict(cat_id="CAT-114", cat_name="Tipo documental pivote",
         cat_def="Clases conceptuales comunes de tipos documentales. Sirven para encontrar instrumentos comparables; no afirman equivalencia jurídica.",
         values=[
             V("constitucion", "Constitución", "Norma constitucional."),
             V("reforma_constitucional", "Reforma constitucional", "Acto que modifica la constitución."),
             V("ley_parlamentaria", "Ley parlamentaria", "Norma con rango de ley aprobada por el legislativo."),
             V("norma_rango_ley_ejecutivo", "Norma con rango de ley del Ejecutivo", "Norma con fuerza de ley dictada por el Ejecutivo, con o sin delegación."),
             V("reglamento_ejecutivo", "Reglamento del Ejecutivo", "Norma reglamentaria del Ejecutivo central."),
             V("norma_entidad_publica", "Norma de entidad pública", "Disposición general de un ministerio, regulador u organismo."),
             V("norma_subnacional", "Norma subnacional", "Ley, ordenanza o disposición de entidad subnacional."),
             V("norma_comunitaria", "Norma comunitaria", "Norma de un órgano de integración."),
             V("tratado", "Tratado", "Acuerdo internacional."),
             V("sentencia", "Sentencia", "Decisión jurisdiccional de fondo."),
             V("auto_judicial", "Auto u otra resolución judicial", "Resolución judicial no definitiva o de trámite."),
             V("criterio_extractado", "Criterio jurisprudencial extractado", "Tesis, sumilla oficial o extracto con identidad propia."),
             V("resolucion_administrativa", "Resolución administrativa", "Decisión administrativa particular."),
             V("pronunciamiento_interpretativo", "Pronunciamiento interpretativo", "Respuesta administrativa que interpreta normativa."),
             V("instruccion_interna", "Instrucción interna", "Circular, directiva o instrucción a la propia administración."),
             V("laudo", "Laudo arbitral", "Decisión de un tribunal arbitral."),
             V("acta_conciliacion", "Acta de conciliación", "Acuerdo conciliatorio."),
             V("obra_doctrinal", "Obra doctrinal", "Artículo, libro, tesis u otra obra de doctrina."),
             V("documento_prenormativo", "Documento prenormativo", "Proyecto, exposición de motivos o dictamen parlamentario."),
         ]),
    dict(cat_id="CAT-115", cat_name="Nivel normativo pivote",
         cat_def="Nivel común para comparar normas entre países sin un rango numérico universal.",
         values=[
             V("constitucional", "Constitucional", "Normas de rango constitucional."),
             V("supranacional", "Supranacional o convencional", "Tratados y normas comunitarias, cuyo rango interno depende de cada país."),
             V("legal", "Legal", "Normas con rango de ley."),
             V("infralegal_reglamentario", "Infralegal reglamentario", "Reglamentos del Ejecutivo central."),
             V("infralegal_administrativo", "Infralegal administrativo", "Disposiciones generales de entidades."),
             V("subnacional", "Subnacional", "Normas de entidades territoriales; su relación con las nacionales puede ser por competencia."),
             V("no_normativo", "No normativo", "Documentos sin carácter normativo."),
         ]),
    dict(cat_id="CAT-116", cat_name="Criterio de ordenación",
         cat_def="Criterio por el que el ordenamiento resuelve la relación entre tipos normativos.",
         values=[
             V("jerarquia", "Jerarquía", "Prevalece el de mayor rango."),
             V("competencia", "Competencia", "Prevalece el del órgano competente en la materia."),
             V("mixto", "Mixto", "Combina jerarquía y competencia."),
         ]),
    dict(cat_id="CAT-117", cat_name="Alcance del acto",
         cat_def="Determinación de los destinatarios de un acto.",
         values=[
             V("general", "General", "Destinatarios indeterminados o categoría abierta."),
             V("particular", "Particular", "Destinatarios determinados."),
             V("mixto", "Mixto", "Contiene disposiciones generales y decisiones particulares."),
             V("indeterminado", "Indeterminado", "No determinable."),
         ]),
    dict(cat_id="CAT-118", cat_name="Función del acto administrativo",
         cat_def="Función principal de un acto administrativo.",
         values=[
             V("decisoria", "Decisoria", "Resuelve una solicitud o procedimiento."),
             V("sancionadora", "Sancionadora", "Impone sanciones."),
             V("interpretativa", "Interpretativa", "Interpreta normativa, usualmente en respuesta a consulta."),
             V("normativa", "Normativa", "Establece reglas generales."),
             V("instruccion_interna", "Instrucción interna u organizativa", "Organiza la propia administración."),
             V("habilitante", "Habilitante o registral", "Otorga licencias, permisos, registros o concesiones."),
             V("resolutoria_recurso", "Resolutoria de recurso", "Resuelve un recurso administrativo."),
             V("fiscalizadora", "Fiscalizadora", "Documenta actuaciones de inspección o supervisión."),
         ]),
    dict(cat_id="CAT-119", cat_name="Tipo de publicación doctrinal",
         cat_def="Clases de obras doctrinales.",
         values=[V(c, l, d) for c, l, d in [
             ("articulo_revista", "Artículo de revista", "Artículo publicado en una revista."),
             ("libro", "Libro", "Monografía o tratado."),
             ("capitulo_libro", "Capítulo de libro", "Contribución en un libro."),
             ("tesis_pregrado", "Tesis de pregrado", "Trabajo para optar un título profesional o licenciatura."),
             ("tesis_maestria", "Tesis de maestría", "Trabajo para optar el grado de maestro."),
             ("tesis_doctorado", "Tesis doctoral", "Trabajo para optar el grado de doctor."),
             ("ponencia", "Ponencia", "Texto presentado en un evento académico."),
             ("comentario_jurisprudencial", "Comentario jurisprudencial", "Análisis de una o más resoluciones."),
             ("sistematizacion_jurisprudencia", "Sistematización de jurisprudencia", "Compilación comentada de jurisprudencia."),
             ("informe", "Informe o documento de trabajo", "Informe técnico o documento de trabajo."),
             ("manual", "Manual o guía", "Obra didáctica."),
             ("resena", "Reseña", "Reseña bibliográfica."),
             ("otro", "Otro", "No catalogado.")]]),
    dict(cat_id="CAT-120", cat_name="Nivel académico",
         cat_def="Nivel académico de una obra doctrinal.",
         values=[V(c, l, d) for c, l, d in [
             ("pregrado", "Pregrado", "Trabajos de grado o licenciatura."),
             ("maestria", "Maestría", "Trabajos de maestría."),
             ("doctorado", "Doctorado", "Trabajos doctorales."),
             ("investigacion_arbitrada", "Investigación arbitrada", "Publicaciones con revisión por pares."),
             ("divulgacion", "Divulgación", "Publicaciones sin arbitraje para público general o profesional."),
             ("estudiantil", "Estudiantil", "Publicaciones gestionadas por estudiantes."),
             ("no_determinado", "No determinado", "No determinable.")]]),
    dict(cat_id="CAT-121", cat_name="Tipo de pronunciamiento judicial (pivote)",
         cat_def="Clases pivote de pronunciamientos judiciales; las denominaciones nacionales se conservan en el tipo documental.",
         values=[
             V("sentencia_definitiva", "Sentencia definitiva", "Decide el fondo en una instancia."),
             V("sentencia_casacion", "Sentencia de casación", "Decide un recurso de casación."),
             V("sentencia_control_constitucional", "Sentencia de control constitucional", "Decide sobre la constitucionalidad de normas."),
             V("sentencia_garantia_derechos", "Sentencia de garantía de derechos", "Decide acciones de amparo, tutela, protección o similares."),
             V("sentencia_reemplazo", "Sentencia de reemplazo", "Dictada tras anular otra en casación."),
             V("auto", "Auto", "Resolución que decide incidentes o cuestiones procesales."),
             V("decreto_providencia", "Decreto o providencia de trámite", "Resolución de mero trámite."),
             V("resolucion_admisibilidad", "Resolución de admisibilidad", "Decide la admisión o procedencia de un recurso o acción."),
             V("criterio_extractado", "Criterio extractado", "Tesis, sumilla oficial o extracto con identidad propia."),
             V("laudo", "Laudo", "Decisión arbitral (si se incorpora a esta colección)."),
         ]),
    dict(cat_id="CAT-122", cat_name="Formato de archivo",
         cat_def="Formato del archivo ingerido.",
         values=[V(c, l, d) for c, l, d in [
             ("pdf_nativo", "PDF nativo", "PDF con capa de texto original."),
             ("pdf_escaneado", "PDF escaneado", "PDF de imágenes; requiere OCR."),
             ("pdf_mixto", "PDF mixto", "PDF con páginas nativas y escaneadas."),
             ("html", "HTML", "Página web."), ("docx", "DOCX o DOC", "Documento de procesador de texto."),
             ("txt", "Texto plano", "Archivo de texto."), ("xml", "XML", "Documento estructurado."),
             ("imagen", "Imagen", "Archivo de imagen."), ("otro", "Otro", "Formato no catalogado.")]]),
    dict(cat_id="CAT-123", cat_name="Carácter oficial de la traducción",
         cat_def="Valor jurídico de una traducción.",
         values=[
             V("oficial", "Oficial", "Traducción con valor auténtico u oficial."),
             V("no_oficial", "No oficial", "Traducción de cortesía o editorial."),
             V("desconocido", "Desconocido", "No determinable."),
         ]),
    dict(cat_id="CAT-124", cat_name="Estado de validación de entrada de catálogo",
         cat_def="Situación de una entrada de catálogo respecto de su validación jurídica.",
         values=[
             V("semilla", "Semilla", "Propuesta inicial no validada."),
             V("en_revision", "En revisión", "Asignada a un responsable para validar."),
             V("validada", "Validada", "Validada por el responsable correspondiente."),
             V("deprecada", "Deprecada", "Sustituida o retirada; se conserva con su sucesor."),
         ]),
    dict(cat_id="CAT-125", cat_name="Rango normativo por país (semilla)",
         cat_def="Rangos normativos nacionales. Semilla ilustrativa que debe completar y validar el responsable jurídico de cada país.",
         values=[
             V("pe_constitucional", "Rango constitucional", "Constitución y normas de su mismo rango.", country="PE", status=SEM),
             V("pe_ley", "Rango de ley", "Leyes y normas con rango de ley.", country="PE", status=SEM),
             V("pe_reglamentario", "Rango reglamentario", "Decretos supremos y reglamentos.", country="PE", status=SEM),
             V("co_constitucional", "Rango constitucional", "Constitución y bloque de constitucionalidad.", country="CO", status=SEM),
             V("co_ley", "Rango de ley", "Leyes y decretos con fuerza de ley.", country="CO", status=SEM),
             V("co_reglamentario", "Rango reglamentario", "Decretos reglamentarios.", country="CO", status=SEM),
             V("ar_constitucional", "Rango constitucional", "Constitución y tratados con jerarquía constitucional.", country="AR", status=SEM),
             V("ar_ley", "Rango de ley", "Leyes y decretos de necesidad y urgencia.", country="AR", status=SEM),
             V("ar_reglamentario", "Rango reglamentario", "Decretos reglamentarios.", country="AR", status=SEM),
             V("cl_constitucional", "Rango constitucional", "Constitución.", country="CL", status=SEM),
             V("cl_ley", "Rango de ley", "Leyes, DFL y DL.", country="CL", status=SEM),
             V("cl_reglamentario", "Rango reglamentario", "Decretos supremos reglamentarios.", country="CL", status=SEM),
             V("ec_constitucional", "Rango constitucional", "Constitución.", country="EC", status=SEM),
             V("ec_ley_organica", "Ley orgánica", "Leyes orgánicas.", country="EC", status=SEM),
             V("ec_ley_ordinaria", "Ley ordinaria", "Leyes ordinarias.", country="EC", status=SEM),
             V("ec_reglamentario", "Rango reglamentario", "Decretos y reglamentos.", country="EC", status=SEM),
             V("bo_constitucional", "Rango constitucional", "Constitución.", country="BO", status=SEM),
             V("bo_ley", "Rango de ley", "Leyes nacionales y legislación autonómica según competencia.", country="BO", status=SEM),
             V("bo_reglamentario", "Rango reglamentario", "Decretos supremos.", country="BO", status=SEM),
             V("mx_constitucional", "Rango constitucional", "Constitución y tratados de derechos humanos según criterios nacionales.", country="MX", status=SEM),
             V("mx_ley", "Rango de ley", "Leyes generales, federales y locales.", country="MX", status=SEM),
             V("mx_reglamentario", "Rango reglamentario", "Reglamentos y normas oficiales.", country="MX", status=SEM),
         ]),
    dict(cat_id="CAT-126", cat_name="Tipos documentales por país (semilla)",
         cat_def="Entradas iniciales del catálogo de tipos documentales por país. Semilla ilustrativa: cada entrada debe completarse y validarse por el responsable jurídico del país antes de usarse para calcular naturaleza, rango o fuerza.",
         values=[
             V("TD-PE-LEY", "Ley", "Norma aprobada por el Congreso.", country="PE", status=SEM),
             V("TD-PE-DECRETO-LEGISLATIVO", "Decreto Legislativo", "Norma del Ejecutivo por delegación.", country="PE", status=SEM),
             V("TD-PE-DECRETO-URGENCIA", "Decreto de Urgencia", "Norma extraordinaria del Ejecutivo.", country="PE", status=SEM),
             V("TD-PE-DECRETO-SUPREMO", "Decreto Supremo", "Norma del Ejecutivo.", country="PE", status=SEM),
             V("TD-PE-TUO", "Texto Único Ordenado", "Compilación oficial aprobada por decreto supremo.", parent="TD-PE-DECRETO-SUPREMO", country="PE", status=SEM),
             V("TD-PE-CASACION", "Casación", "Resolución de la Corte Suprema en casación.", country="PE", status=SEM),
             V("TD-CO-LEY", "Ley", "Norma del Congreso.", country="CO", status=SEM),
             V("TD-CO-DECRETO", "Decreto", "Norma del Ejecutivo.", country="CO", status=SEM),
             V("TD-CO-SENTENCIA-CC", "Sentencia de la Corte Constitucional", "Sentencias C-, T- y SU-.", country="CO", status=SEM),
             V("TD-CO-CONCEPTO", "Concepto", "Pronunciamiento de una entidad en respuesta a consulta.", country="CO", status=SEM),
             V("TD-AR-LEY", "Ley", "Norma del Congreso de la Nación.", country="AR", status=SEM),
             V("TD-AR-DNU", "Decreto de Necesidad y Urgencia", "Norma del Ejecutivo nacional.", country="AR", status=SEM),
             V("TD-AR-DECRETO", "Decreto", "Norma del Ejecutivo.", country="AR", status=SEM),
             V("TD-AR-FALLO-CSJN", "Fallo de la Corte Suprema", "Sentencia de la CSJN.", country="AR", status=SEM),
             V("TD-CL-LEY", "Ley", "Norma del Congreso Nacional.", country="CL", status=SEM),
             V("TD-CL-DFL", "Decreto con Fuerza de Ley", "Norma del Ejecutivo por delegación.", country="CL", status=SEM),
             V("TD-CL-DECRETO-SUPREMO", "Decreto Supremo", "Norma del Ejecutivo.", country="CL", status=SEM),
             V("TD-CL-DICTAMEN-CGR", "Dictamen de la Contraloría", "Pronunciamiento de la Contraloría General.", country="CL", status=SEM),
             V("TD-EC-LEY-ORGANICA", "Ley Orgánica", "Ley orgánica.", country="EC", status=SEM),
             V("TD-EC-DECRETO-EJECUTIVO", "Decreto Ejecutivo", "Norma del Presidente de la República.", country="EC", status=SEM),
             V("TD-EC-SENTENCIA-CC", "Sentencia de la Corte Constitucional", "Sentencia constitucional.", country="EC", status=SEM),
             V("TD-BO-LEY", "Ley", "Norma de la Asamblea Legislativa Plurinacional.", country="BO", status=SEM),
             V("TD-BO-DECRETO-SUPREMO", "Decreto Supremo", "Norma del Ejecutivo.", country="BO", status=SEM),
             V("TD-BO-SCP", "Sentencia Constitucional Plurinacional", "Sentencia del TCP.", country="BO", status=SEM),
             V("TD-BO-AUTO-SUPREMO", "Auto Supremo", "Resolución del Tribunal Supremo de Justicia.", country="BO", status=SEM),
             V("TD-MX-LEY-FEDERAL", "Ley Federal", "Ley del Congreso de la Unión.", country="MX", status=SEM),
             V("TD-MX-LEY-GENERAL", "Ley General", "Ley del Congreso de la Unión que distribuye competencias.", country="MX", status=SEM),
             V("TD-MX-REGLAMENTO", "Reglamento", "Norma reglamentaria del Ejecutivo.", country="MX", status=SEM),
             V("TD-MX-NOM", "Norma Oficial Mexicana", "Regulación técnica de observancia obligatoria.", country="MX", status=SEM),
             V("TD-MX-TESIS", "Tesis", "Criterio extractado publicado en el Semanario Judicial.", country="MX", status=SEM),
         ]),
]
