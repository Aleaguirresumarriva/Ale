"""
Esquema común del Diccionario Maestro de Metadatos Jurídicos de Juztina (Etapa 2).

Cada módulo campos_gN.py define:
  FIELDS   = [dict(...), ...]   # un dict por campo, con TODAS las claves de CAMPO_CLAVES
  CATALOGS = [dict(...), ...]   # catálogos nuevos que el módulo necesita (rango CAT-N00..N99)
Reglas:
  - IDs: "MDJ-<DIM>-<NNN>" (DIM = código de DIMENSIONES; NNN de 3 dígitos). El prefijo indica la
    dimensión de alta y NO se cambia aunque el campo se reasigne. Nunca se reutiliza un ID.
  - Nombre técnico: snake_case en español, sin tildes ni ñ (ñ -> n), único en todo el diccionario.
  - Ninguna celda vacía: si no corresponde, "No aplica: <razón>".
  - Valores controlados: referenciar catálogos por ID ("CAT-012 Estado de vigencia").
"""

CAMPO_CLAVES = [
    ("id", "ID del campo"),
    ("tech", "Nombre técnico"),
    ("func", "Nombre funcional"),
    ("dim", "Dimensión"),
    ("profiles", "Perfil documental"),
    ("unit", "Unidad de registro"),
    ("defn", "Definición"),
    ("just", "Justificación"),
    ("dtype", "Tipo de dato"),
    ("card", "Cardinalidad"),
    ("values", "Valores permitidos"),
    ("example", "Ejemplo"),
    ("origin", "Origen del dato"),
    ("method", "Método de adquisición"),
    ("evidence", "Evidencia requerida"),
    ("extraction", "Regla de extracción"),
    ("validation", "Regla de validación"),
    ("applicability", "Aplicabilidad"),
    ("prio", "Prioridad"),
    ("mode", "Modo de adquisición"),
    ("review", "Requiere revisión humana"),
    ("privacy", "Sensibilidad y privacidad"),
    ("deps", "Dependencias"),
    ("funcs", "Funcionalidades habilitadas"),
    ("obs", "Observaciones"),
    # Atributos adicionales exigidos por la arquitectura v3
    ("stage", "Etapa de procesamiento"),
    ("risk", "Clase de riesgo"),
    ("countries", "Países"),
    ("country_status", "Estado por país"),
    ("pending", "Decisiones o validaciones pendientes"),
]

DIMENSIONES = {
    "D01": "D1 Identificación",
    "D02": "D2 Procedencia institucional y custodia",
    "D03": "D3 Temporalidad y vigencia",
    "D04": "D4 Naturaleza, tipología y fuerza documental",
    "D05": "D5 Contenido y estructura",
    "D06": "D6 Clasificación jurídica",
    "D07": "D7 Referencias y relaciones",
    "D08": "D8 Alcance y efectos",
    "D09": "D9 Información económica y cuantitativa",
    "D10": "D10 Información sectorial",
    "D11": "D11 Calidad y confiabilidad documental",
    "D13": "D13 Actores y partes",
    "D14": "D14 Procedimiento y estado procesal",
    "D15": "D15 Lengua y forma",
    "D16": "D16 Derechos, acceso y datos personales",
    "D17": "D17 Autoridad y fuerza jurídica",
    "PRO": "Capa de procedencia (afirmación, evidencia, ejecución)",
    "OPE": "Capa operativa (estado de campo, gobierno, uso)",
}

PERFILES = ["UNI", "NOR", "JUR", "ADM", "DOC"]   # combinar con "; " p. ej. "JUR; ADM". UNI = universal

UNIDADES = [
    "Obra", "Versión", "Manifestación", "Unidad estructural", "Fragmento textual", "Proceso",
    "Afirmación", "Referencia", "Relación", "Evidencia", "Ejecución",
    # Afirmaciones compuestas (registros dependientes de una unidad de registro)
    "Afirmación compuesta: evento temporal",
    "Afirmación compuesta: operación modificatoria",
    "Afirmación compuesta: asignación de clasificación",
    "Afirmación compuesta: parte o actor",
    "Afirmación compuesta: monto",
    "Afirmación compuesta: efecto jurídico",
    "Afirmación compuesta: estado de campo",
    "Afirmación compuesta: revisión humana",
    # Entidades de referencia (catálogos maestros)
    "Entidad: organismo u órgano", "Entidad: persona", "Entidad: territorio o jurisdicción",
    "Entidad: concepto de taxonomía", "Entidad: tipo documental", "Entidad: unidad de valor",
    "Entidad: publicación o fuente",
]

TIPOS_DATO = ["Identificador", "String", "Texto largo", "Boolean", "Integer", "Decimal", "Fecha",
              "Fecha parcial", "Datetime", "Intervalo de fechas", "Enum", "Enum múltiple", "Array",
              "Objeto", "Referencia", "Array de referencias", "Ancla de evidencia", "URL", "Hash",
              "Código ISO", "Porcentaje"]

CARDINALIDADES = ["1 obligatorio", "0..1 opcional", "0..1 obligatorio condicionado", "0..n", "1..n"]

ORIGENES = ["Explícito en documento", "Normalizado por regla", "Inferido por modelo",
            "Derivado por cálculo", "Conclusión jurídica por reglas", "Fuente externa",
            "Generado por sistema", "Curado por persona"]

METODOS = ["Extracción directa", "Normalización", "Clasificación", "Inferencia", "Cálculo",
           "Enriquecimiento externo", "Revisión humana", "Generado por sistema"]
# Se admite combinación con " + " (p. ej. "Extracción directa + Normalización")

PRIORIDADES = ["P0", "P1", "P2", "P3", "Fuera de alcance"]
MODOS = ["A", "B", "C", "D", "X"]     # X sólo con prioridad "Fuera de alcance"
REVISION = ["Sí", "No", "Condicionado"]
PRIVACIDAD = ["Ninguna", "Dato de funcionario público", "Puede contener datos personales",
              "Dato personal", "Dato personal sensible", "Restricción de acceso o derechos"]
ETAPAS = ["E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "Posterior (C)", "Curaduría", "Sistema"]
RIESGOS = ["R1", "R2", "R3"]
PAISES = ["PE", "CO", "AR", "CL", "EC", "BO", "MX"]   # countries = "ALL" o lista con "; "
ESTADO_PAIS = ["Común", "Catálogo por país", "Específico de país", "Condicionado",
               "Pendiente validación nacional"]

FUNCIONALIDADES = {
    "F01": "Asistentes jurídicos especializados",
    "F02": "Asistente general",
    "F03": "Búsqueda jurídica avanzada",
    "F04": "Investigación jurídica",
    "F05": "Seguimiento normativo y alertas",
    "F06": "Línea de tiempo, modificaciones y derogaciones",
    "F07": "Análisis de jurisprudencia",
    "F08": "Identificación de precedentes",
    "F09": "Comparación jurídica entre países",
    "F10": "Investigación por sectores económicos",
    "F11": "Relaciones entre documentos",
    "F12": "Grafo de conocimiento jurídico",
    "F13": "Mapas de obligaciones y cumplimiento",
    "F14": "Estimación de contingencias económicas",
    "F15": "Citas verificadas y redacción asistida",
    "F16": "Calidad, auditoría y reprocesamiento (interno)",
    "F17": "Privacidad y control de acceso (interno)",
    "F18": "Gobierno de taxonomía y catálogos (interno)",
}
# funcs = "F01; F03; F04" o "No aplica: <razón>"

DECISIONES = {  # pending = "No" o lista "DEC-07; DEC-18"
    "DEC-03": "Regla de continuidad presunta por país",
    "DEC-04": "Rango y efectos de textos ordenados o refundidos por país",
    "DEC-07": "Colección de los tipos documentales limítrofes",
    "DEC-08": "Mapeo de tipos documentales originales a naturalezas jurídicas por país",
    "DEC-09": "Alineación de unidades estructurales con fragmentos (chunks) del asistente",
    "DEC-11": "Umbrales de alerta de sobreclasificación por tipo de unidad",
    "DEC-12": "Reglas concretas de especialidades de práctica (F3)",
    "DEC-13": "Designación de responsables de la taxonomía",
    "DEC-14": "Validación de correspondencias entre países",
    "DEC-17": "Reglas de efecto (vigencia, inconstitucionalidad, nulidad) y fuentes oficiales por país",
    "DEC-18": "Política de datos personales por país",
    "DEC-19": "Estadísticas sobre jueces y funcionarios",
    "DEC-20": "Metas numéricas de precisión por clase de riesgo",
    "DEC-22": "Corte P1/P2 según presupuesto y volumen",
    "DEC-24": "Conservación de insumos intermedios",
    "DEC-25": "Reglas de fuerza vinculante y precedente por país",
    "DEC-26": "Fuerza de los pronunciamientos interpretativos administrativos por país",
    "DEC-27": "Política de uso de doctrina protegida (resúmenes, citas, reproducción)",
    "DEC-28": "Catálogo territorial y códigos oficiales por país",
    "DEC-29": "Fuente y serie histórica de unidades de valor (UIT, UVT, UF, UTM, UMA…)",
    "DEC-30": "Incorporación de fuentes no estatales (jurisdicción indígena) y supranacionales",
    "DEC-31": "Cobertura de normativa subnacional",
    "DEC-32": "Completitud histórica real de la normativa almacenada",
    "DEC-33": "Claves auxiliares para organismos (RUC, NIT, RUT, CUIT, RFC)",
    "DEC-34": "Fecha de efecto de las fe de erratas por país",
    "DEC-35": "Validación del contenido de la taxonomía de etiquetas (CAT-330) y de los especialistas de Juztina (CAT-331)",
}

# Catálogos núcleo definidos por el constructor (rango CAT-0xx). Los módulos los referencian por ID.
CATALOGOS_NUCLEO = {
    "CAT-001": "País y jurisdicción (ISO 3166-1 alfa-2 + pseudo jurisdicciones CAN, SIDH, MERCOSUR)",
    "CAT-002": "Categoría de colección (normativa, jurisprudencia, actos administrativos, doctrina)",
    "CAT-003": "Naturaleza jurídica",
    "CAT-004": "Nivel de gobierno",
    "CAT-005": "Modo de origen de la afirmación",
    "CAT-006": "Estado de campo",
    "CAT-007": "Clase de riesgo",
    "CAT-008": "Etapa de procesamiento",
    "CAT-009": "Idioma (ISO 639)",
    "CAT-010": "Moneda (ISO 4217)",
    "CAT-011": "Estado de revisión humana",
    "CAT-012": "Tipo de equivalencia entre países",
}
