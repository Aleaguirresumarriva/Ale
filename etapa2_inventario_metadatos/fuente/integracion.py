"""
Capa de integración entre los módulos de campos (Etapa 2).

Los módulos campos_g1..g5 se redactaron por bloques de dimensiones. Al unirlos se detectaron
duplicidades y solapamientos. Este archivo registra cada decisión de integración de forma auditable:
  - RETIRADOS: campos eliminados antes de la publicación v1.0 por duplicar otro campo. Sus IDs quedan
    RESERVADOS y no se reutilizan. Las referencias a ellos se redirigen al campo que se conserva.
  - CAT_RETIRADOS: catálogos absorbidos por otro catálogo.
  - CAT_RENOMBRES / CAT_NOTAS: precisiones de nombre o definición para distinguir catálogos parecidos.
  - AJUSTES: modificaciones puntuales de atributos de un campo (clave -> nuevo valor).
"""

RETIRADOS = {
    "MDJ-D03-047": ("MDJ-D01-002", "Duplicaba el identificador de la versión (id_version)."),
    "MDJ-D03-055": ("MDJ-D02-019", "Duplicaba la fecha de captura de la manifestación."),
    "MDJ-D11-023": ("MDJ-D02-024", "Duplicaba el estado del enlace de la fuente; se conserva el campo con catálogo controlado (CAT-106)."),
    "MDJ-D17-016": ("MDJ-D04-013", "Duplicaba el nivel académico de la obra doctrinal; D17 lo usa como señal de autoridad por dependencia."),
    "MDJ-PRO-029": ("MDJ-D05-019", "Duplicaba la marca de contenido ajeno; se conserva el campo de anclas de tramos transcritos."),
    "MDJ-D07-033": ("MDJ-D05-019", "Duplicaba la marca de contenido ajeno del fragmento; D05-019 pasa a calcularse desde los límites de las citas textuales."),
    "MDJ-D16-018": ("MDJ-D13-012", "Duplicaba el nombre de persona natural de una parte (ambos fuera de alcance, clase X)."),
    "MDJ-D02-005": ("MDJ-D13-015", "Firmantes: se representan como registros de actor institucional (D13) con rol, nombre, cargo y órgano."),
    "MDJ-D02-006": ("MDJ-D13-015", "Ponente: se representa como actor institucional con rol 'magistrado ponente' (D13)."),
    "MDJ-D02-007": ("MDJ-D13-019", "Composición del órgano: se representa con registros de actor institucional y su sentido de voto (D13)."),
    "MDJ-D11-007": ("MDJ-D15-008", "Duplicaba el número de páginas de la manifestación."),
    "MDJ-D14-022": ("MDJ-D17-004", "Duplicaba el resultado de la votación; D17-004 incorpora la modalidad (unanimidad o mayoría)."),
}

CAT_RETIRADOS = {
    "CAT-103": ("CAT-412", "El rol de firma se integra en el rol del actor institucional; se agregan los valores que faltaban."),
    "CAT-120": ("CAT-317", "Dos catálogos de nivel académico; se conserva el más completo (incluye tesis doctoral, de maestría, material docente y comentario profesional)."),
}

CAT_RENOMBRES = {
    "CAT-113": "Periodicidad de publicación",
    "CAT-531": "Periodicidad de pago u obligación",
    "CAT-317": "Nivel académico o de publicación doctrinal",
}

CAT_NOTAS = {
    "CAT-504": " Integración: cada valor debe corresponderse con un concepto de la faceta F8 (sujetos) de la taxonomía; "
               "la faceta F8 se siembra con estos valores para no mantener dos vocabularios divergentes de sujetos (DEC-13).",
    "CAT-512": " Integración: se calcula a partir del carácter oficial de la fuente (CAT-112, MDJ-D02-043) y del tipo de texto de la manifestación; "
               "no son catálogos duplicados: CAT-112 describe la fuente, CAT-512 la confiabilidad de una manifestación concreta.",
}

CAT_VALORES_AGREGADOS = {
    "CAT-412": [
        dict(code="promulgante", label="Promulgante", definition="Autoridad que promulga la norma (integrado desde CAT-103)."),
        dict(code="suscriptor", label="Suscriptor", definition="Autoridad que suscribe el acto sin ser su emisor principal (integrado desde CAT-103)."),
        dict(code="certificador", label="Certificador", definition="Funcionario que certifica o da fe del documento (integrado desde CAT-103)."),
    ],
}

AJUSTES = {
    "MDJ-D04-013": {"values": "CAT-317 Nivel académico o de publicación doctrinal."},
    "MDJ-D05-019": {
        "origin": "Derivado por cálculo", "method": "Cálculo", "mode": "B", "stage": "E7",
        "extraction": "Se calcula uniendo los límites de las citas textuales (MDJ-D07-031) cuyo tramo cae dentro del fragmento y su atribución (MDJ-D07-032). No requiere nueva lectura del documento.",
        "evidence": "La de las citas textuales que lo originan (límites anclados en la manifestación).",
        "deps": "MDJ-D07-031; MDJ-D07-032; segmentación del fragmento (D05).",
        "obs": "Integración: absorbe las marcas de contenido ajeno definidas en D07 y en la capa de procedencia. Las etapas de clasificación, efectos y montos excluyen estos tramos del contenido propio (RG-16).",
    },
    "MDJ-D17-004": {
        "values": "Objeto {modalidad: unanimidad | mayoría | no_indicada, a_favor: entero, en_contra: entero, abstenciones: entero, otros: texto}.",
        "extraction": "Extraer la modalidad expresa ('por unanimidad', 'por mayoría') y el conteo solo si el texto lo consigna. No deducir conteos de las firmas ni del número de votos singulares.",
        "defn": "Modalidad de adopción de la decisión colegiada (unanimidad o mayoría) y, cuando consta, el número de votos a favor, en contra, abstenciones y otras posiciones.",
    },
    "MDJ-D13-015": {"values": "CAT-412 Rol del actor institucional (incluye los roles de firma integrados desde CAT-103)."},
}


# Regla transversal derivada de RG-10 (arquitectura v3, G, regla 10)
R1_ORIGENES_REVISABLES = ("Explícito en documento", "Normalizado por regla", "Inferido por modelo", "Fuente externa")
R1_NOTA = (" Integración (RG-10): afirmación de riesgo R1. La revisión humana es obligatoria antes de que el valor alimente "
           "cálculos de vigencia, precedente o montos finales; solo puede ser muestral si el piloto demuestra una precisión "
           "igual o superior a la meta R1 (DEC-20).")

def aplicar_regla_r1(f):
    """Devuelve True si ajustó el campo."""
    if f["risk"] == "R1" and f["review"] == "No" and f["origin"] in R1_ORIGENES_REVISABLES:
        f["review"] = "Condicionado"
        f["obs"] = (f["obs"] + R1_NOTA) if not f["obs"].startswith("No aplica") else R1_NOTA.strip()
        if "DEC-20" not in f["pending"]:
            f["pending"] = "DEC-20" if f["pending"] == "No" else f["pending"] + "; DEC-20"
        return True
    return False
