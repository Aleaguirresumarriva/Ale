"""
Campos del grupo 5: D08 Alcance y efectos, D09 Información económica, D11 Calidad documental,
D16 Derechos, acceso y datos personales, capa de procedencia (PRO) y capa operativa (OPE).
Catálogos propios: CAT-500..CAT-599.
"""

FIELDS = []

PAISES_TODOS = "ALL"


def F(**kw):
    """Crea un campo aplicando valores por defecto del grupo y componiendo la aplicabilidad."""
    base = dict(
        countries=PAISES_TODOS,
        country_status="Común",
        pending="No",
        review="No",
        privacy="Ninguna",
    )
    base.update(kw)
    cond = base.pop("cond", "Siempre que el perfil documental aplique")
    if "applicability" not in base:
        paises = "los siete países" if base["countries"] == "ALL" else base["countries"]
        base["applicability"] = f"Perfiles {base['profiles']}; {paises}. {cond}."
    FIELDS.append(base)


# ---------------------------------------------------------------------------------------------
# D08 ALCANCE Y EFECTOS
# ---------------------------------------------------------------------------------------------
EF = dict(dim="D08", profiles="NOR; ADM; JUR", unit="Afirmación compuesta: efecto jurídico",
          prio="P2", mode="C", stage="Posterior (C)", risk="R2", review="Condicionado",
          funcs="F13; F01; F04; F02", origin="Inferido por modelo", method="Inferencia",
          evidence="Tramo literal de la unidad estructural propia (no transcrita) que enuncia el efecto, con sección",
          cond="Solo unidades con efecto jurídico autónomo (E.3): artículo o numeral con consecuencia propia en normativa; punto resolutivo en jurisprudencia y actos")

F(id="MDJ-D08-001", tech="ambito_territorial_aplicacion", func="Ámbito territorial de aplicación",
  dim="D08", profiles="NOR; ADM", unit="Obra",
  defn="Territorios en los que la obra o el acto produce efectos, como referencias a entidades de territorio.",
  just="Permite filtrar normas por departamento, provincia, estado o municipio y distinguir normas nacionales de subnacionales.",
  dtype="Array de referencias", card="1..n",
  values="Entidad: territorio o jurisdicción (catálogo territorial por país, DEC-28)",
  example="[PE-ubigeo 15 (Lima)]", origin="Normalizado por regla", method="Extracción directa + Normalización",
  evidence="Tramo que declara el ámbito o, en su defecto, regla por emisor (competencia territorial del órgano)",
  extraction="Leer el ámbito declarado (artículo de ámbito de aplicación, encabezado del emisor). Si no se declara, asignar el territorio de competencia del emisor y marcar modo normalizado por regla.",
  validation="Cada territorio debe existir en el catálogo y estar subordinado o igual al ámbito de competencia del emisor.",
  prio="P1", mode="A", stage="E3", risk="R2", country_status="Catálogo por país", pending="DEC-28; DEC-31",
  deps="MDJ-D02 emisor de la obra; catálogo territorial", funcs="F03; F05; F09; F10; F13",
  obs="Las pseudo jurisdicciones (CAN, SIDH) se tratan como territorio supranacional con relación 'aplica en'.")

F(id="MDJ-D08-002", tech="nivel_gobierno_ambito", func="Nivel de gobierno del ámbito",
  dim="D08", profiles="NOR; ADM", unit="Obra",
  defn="Nivel de gobierno al que corresponde el ámbito territorial: supranacional, nacional o federal, intermedio, local, autónomo indígena.",
  just="Facilita separar normativa nacional y subnacional en búsquedas y alertas.",
  dtype="Enum", card="1 obligatorio", values="CAT-004 Nivel de gobierno", example="Nacional",
  origin="Derivado por cálculo", method="Cálculo", evidence="Regla aplicada sobre MDJ-D08-001",
  extraction="No se extrae: se calcula del territorio de mayor nivel en MDJ-D08-001.",
  validation="Coherente con el nivel del emisor; si discrepan, marcar conflicto.",
  prio="P1", mode="B", stage="E7", risk="R3", country_status="Catálogo por país", pending="DEC-31",
  deps="MDJ-D08-001", funcs="F03; F05; F09", obs="No aplica a doctrina.")

F(id="MDJ-D08-003", tech="destinatarios_tipo", func="Tipo de destinatarios",
  dim="D08", profiles="NOR; ADM", unit="Unidad estructural",
  defn="Categorías pivote de sujetos a quienes se dirige la unidad (empleadores, contribuyentes, entidades públicas, consumidores, concesionarios…).",
  just="Base de los mapas de obligaciones y de los filtros por sujeto obligado.",
  dtype="Enum múltiple", card="0..n", values="CAT-504 Tipo de destinatario (pivote)", example="[Empleador privado; Trabajador]",
  origin="Inferido por modelo", method="Clasificación", evidence="Tramo que nombra o describe al destinatario",
  extraction="Identificar quién debe cumplir o a quién se dirige la disposición. Usar solo el texto propio de la unidad; si el destinatario es tácito, inferirlo del sujeto de la oración y marcar 'interpretado'.",
  validation="Al menos una evidencia en la unidad; valores del catálogo; no asignar destinatarios mencionados solo en transcripciones.",
  prio="P1", mode="A", stage="E3", risk="R2", review="Condicionado",
  deps="Segmentación (MDJ-D05); marca de contenido ajeno (MDJ-PRO-029)", funcs="F13; F01; F03; F10",
  obs="Relaciona con F8 Sujetos de la taxonomía (D06); aquí se registra a quién se dirige la regla, no de qué trata.")

F(id="MDJ-D08-004", tech="destinatarios_texto_literal", func="Destinatarios (texto literal)",
  dim="D08", profiles="NOR; ADM", unit="Unidad estructural",
  defn="Expresión literal con la que la unidad designa a sus destinatarios.",
  just="Conserva la denominación nacional original sin forzar el pivote.",
  dtype="Array", card="0..n", values="No aplica: texto libre literal", example="['los empleadores del régimen laboral de la actividad privada']",
  origin="Explícito en documento", method="Extracción directa", evidence="Tramo literal verificado",
  extraction="Copiar literalmente el sintagma que designa a los destinatarios.",
  validation="Coincidencia literal con la evidencia (verificación MDJ-PRO-024).",
  prio="P1", mode="A", stage="E3", risk="R3", deps="MDJ-D08-003", funcs="F03; F13; F09",
  obs="Fuente para validar el mapeo al pivote CAT-504.")

F(id="MDJ-D08-005", tech="ambito_material_descripcion", func="Ámbito material de aplicación",
  dim="D08", profiles="NOR; ADM", unit="Obra",
  defn="Descripción breve de las materias, actividades o situaciones que la obra regula según su artículo de objeto o ámbito.",
  just="Ayuda a decidir la pertinencia de una norma sin leerla completa.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto con evidencia", example="Relaciones laborales del sector privado y sus excepciones",
  origin="Explícito en documento", method="Extracción directa", evidence="Artículo de objeto, finalidad o ámbito de aplicación",
  extraction="Transcribir el artículo de objeto o ámbito; si no existe, dejar estado 'no encontrado'. No resumir el resto de la obra.",
  validation="Evidencia en una unidad de tipo 'objeto' o 'ámbito'.",
  prio="P2", mode="C", stage="Posterior (C)", risk="R3", deps="Segmentación con epígrafes", funcs="F03; F04; F02")

F(id="MDJ-D08-006", tech="ambito_personal_exclusiones", func="Exclusiones expresas del ámbito",
  dim="D08", profiles="NOR; ADM", unit="Unidad estructural",
  defn="Sujetos, actividades o situaciones expresamente excluidos de la aplicación de la unidad u obra.",
  just="Evita falsos positivos en compliance y en respuestas del asistente.",
  dtype="Array", card="0..n", values="No aplica: texto literal; mapeo opcional a CAT-504", example="['trabajadores del hogar']",
  origin="Explícito en documento", method="Extracción directa", evidence="Tramo con la fórmula de exclusión ('no se aplica a', 'se exceptúa')",
  extraction="Detectar fórmulas de exclusión o excepción de ámbito y copiar su objeto.",
  validation="Debe existir verbo o fórmula de exclusión en la evidencia.",
  prio="P2", mode="C", stage="Posterior (C)", risk="R2", deps="MDJ-D08-003", funcs="F13; F01; F04")

F(id="MDJ-D08-007", tech="aplicacion_temporal_tipo", func="Tipo de aplicación temporal declarada",
  dim="D08", profiles="NOR; ADM; JUR", unit="Unidad estructural",
  defn="Modalidad temporal de aplicación declarada por la unidad: inmediata, diferida, retroactiva, ultraactiva o condicionada.",
  just="Determina a qué hechos se aplica la regla; insumo para vigencia y análisis de casos.",
  dtype="Enum", card="0..1 opcional", values="CAT-503 Ámbito temporal de aplicación", example="Retroactiva",
  origin="Explícito en documento", method="Extracción directa + Normalización", evidence="Fórmula expresa de aplicación temporal",
  extraction="Solo cuando el texto lo declara ('con efecto retroactivo', 'se aplica a los procedimientos en trámite'). No inferir de la naturaleza de la norma.",
  validation="Requiere fórmula expresa; si no hay, estado 'no encontrado'.",
  prio="P1", mode="A", stage="E3", risk="R1", review="Condicionado",
  deps="Eventos temporales (MDJ-D03)", funcs="F06; F05; F04; F02",
  obs="La retroactividad real puede depender de reglas constitucionales del país: esa conclusión es D03/D17, no este campo.")

F(id="MDJ-D08-008", tech="alcance_efectos_declarado", func="Alcance de efectos declarado",
  dim="D08", profiles="JUR; ADM", unit="Obra",
  defn="Alcance subjetivo de los efectos de la decisión cuando la propia decisión lo declara (inter partes, erga omnes, inter pares, inter comunis, general).",
  just="Distingue decisiones con efecto solo entre partes de las de efecto general.",
  dtype="Enum", card="0..1 opcional", values="CAT-502 Alcance subjetivo de efectos", example="Inter comunis",
  origin="Explícito en documento", method="Extracción directa + Normalización", evidence="Punto resolutivo o fundamento que declara el alcance",
  extraction="Registrar solo si la decisión declara expresamente el alcance.",
  validation="Evidencia en parte resolutiva o en fundamento de efectos.",
  prio="P1", mode="A", stage="E3", risk="R1", review="Condicionado", country_status="Pendiente validación nacional",
  pending="DEC-25", deps="Parte resolutiva delimitada (MDJ-D05)", funcs="F07; F08; F04")

F(id="MDJ-D08-009", tech="alcance_efectos_calculado", func="Alcance de efectos (conclusión)",
  dim="D08", profiles="JUR; ADM", unit="Obra",
  defn="Alcance subjetivo de efectos determinado por reglas de cada país según órgano, tipo de proceso y declaración expresa.",
  just="Permite al asistente advertir si una decisión vincula más allá de las partes.",
  dtype="Enum", card="0..1 obligatorio condicionado", values="CAT-502 Alcance subjetivo de efectos", example="Erga omnes",
  origin="Conclusión jurídica por reglas", method="Cálculo", evidence="Regla aplicada (ID y versión) e insumos",
  extraction="No se extrae: se calcula con reglas nacionales validadas a partir de MDJ-D08-008, tipo de proceso (D14) y órgano (D02).",
  validation="Solo con regla validada para el país; sin regla, estado 'indeterminado'.",
  prio="P1", mode="B", stage="E7", risk="R1", review="Condicionado", country_status="Pendiente validación nacional",
  pending="DEC-25", deps="MDJ-D08-008; vía procesal (D14); órgano (D02)", funcs="F07; F08; F02")

F(id="MDJ-D08-010", tech="efecto_id", func="Identificador del efecto jurídico",
  unit="Afirmación compuesta: efecto jurídico", dim="D08", profiles="NOR; ADM; JUR",
  defn="Identificador persistente de cada efecto jurídico (obligación, prohibición, sanción…) extraído de una unidad.",
  just="Permite referenciar efectos individuales en mapas de obligaciones y relaciones.",
  dtype="Identificador", card="1 obligatorio", values="No aplica: generado por el sistema", example="EFE-000184233",
  origin="Generado por sistema", method="Generado por sistema", evidence="No aplica: dato de sistema",
  extraction="Asignar al crear el registro de efecto.", validation="Único y nunca reutilizado.",
  prio="P2", mode="C", stage="Sistema", risk="R3", review="No", deps="No aplica: primer dato del registro",
  funcs="F13; F12", obs="Registro dependiente de la unidad estructural de origen.")

F(id="MDJ-D08-011", tech="efecto_unidad_origen", func="Unidad que establece el efecto",
  defn="Unidad estructural (artículo, numeral, punto resolutivo) que enuncia el efecto.",
  just="Ancla el efecto a la disposición y permite seguir su vigencia.",
  dtype="Referencia", card="1 obligatorio", values="Unidad estructural", example="U-PE-LEY29783-ART022",
  origin="Generado por sistema", method="Generado por sistema", evidence="No aplica: es el sujeto del registro",
  extraction="Tomar la unidad sobre la que corre el perfil de extracción.", validation="Debe existir y pertenecer al nivel de efectos definido en E.3.",
  review="No", risk="R3", stage="Sistema", deps="MDJ-D05 unidades estructurales",
  funcs="F13; F06; F12", **{k: v for k, v in EF.items() if k not in ("origin", "method", "review", "risk", "stage", "funcs", "evidence")})

F(id="MDJ-D08-012", tech="efecto_tipo", func="Tipo de efecto jurídico",
  defn="Clase de efecto que establece la unidad: obligación, prohibición, permiso, derecho, sanción, definición, habilitación, atribución de competencia, orden, medida correctiva.",
  just="Clave para mapas de obligaciones, compliance y análisis de sanciones.",
  dtype="Enum", card="1 obligatorio", values="CAT-501 Tipo de efecto jurídico", example="Obligación",
  extraction="Clasificar el efecto por el operador deóntico del texto propio (debe, está prohibido, puede, tiene derecho, será sancionado, se entiende por). Un efecto por operador.",
  validation="Valor del catálogo; evidencia contiene el operador; no usar transcripciones ajenas.",
  deps="MDJ-D08-011", **{k: v for k, v in EF.items()})

F(id="MDJ-D08-013", tech="efecto_sujeto_obligado_tipo", func="Sujeto obligado (tipo)",
  defn="Categoría pivote del sujeto que debe cumplir el efecto o que resulta sancionado.",
  just="Permite filtrar obligaciones por tipo de sujeto.",
  dtype="Enum", card="0..1 obligatorio condicionado", values="CAT-504 Tipo de destinatario (pivote)", example="Empleador privado",
  extraction="Identificar el sujeto gramatical o lógico del operador deóntico. Obligatorio para obligación, prohibición y sanción.",
  validation="Requerido si efecto_tipo ∈ {Obligación, Prohibición, Sanción}.",
  deps="MDJ-D08-012", **EF)

F(id="MDJ-D08-014", tech="efecto_sujeto_obligado_literal", func="Sujeto obligado (texto literal)",
  defn="Denominación literal del sujeto obligado tal como aparece en la unidad.",
  just="Conserva la terminología nacional.",
  dtype="String", card="0..1 obligatorio condicionado", values="No aplica: texto literal", example="el titular de la actividad minera",
  extraction="Copiar el sintagma literal del sujeto del operador deóntico.", validation="Verificación literal.",
  deps="MDJ-D08-013", **{**EF, "origin": "Explícito en documento", "method": "Extracción directa", "risk": "R3"})

F(id="MDJ-D08-015", tech="efecto_beneficiario_tipo", func="Beneficiario o titular del derecho (tipo)",
  defn="Categoría pivote del sujeto a cuyo favor se establece el efecto (titular del derecho, acreedor de la obligación).",
  just="Permite responder qué derechos tiene un sujeto y quién puede exigirlos.",
  dtype="Enum", card="0..1 opcional", values="CAT-504 Tipo de destinatario (pivote)", example="Trabajador",
  extraction="Identificar a quién beneficia la obligación o quién es titular del derecho; solo si el texto lo permite.",
  validation="Valor del catálogo con evidencia.", deps="MDJ-D08-012", **EF)

F(id="MDJ-D08-016", tech="efecto_autoridad_competente", func="Autoridad competente para el efecto",
  defn="Organismo u órgano que la unidad designa para fiscalizar, sancionar, otorgar o exigir el efecto.",
  just="Responde ante quién se cumple o reclama; útil para compliance y rutas procedimentales.",
  dtype="Referencia", card="0..1 opcional", values="Entidad: organismo u órgano", example="Superintendencia Nacional de Fiscalización Laboral",
  extraction="Extraer la autoridad nombrada en la unidad y normalizarla al catálogo de organismos; si no se nombra, no inferir.",
  validation="Debe resolverse a un organismo del catálogo o quedar como literal no resuelto.",
  country_status="Catálogo por país", deps="Catálogo de organismos (MDJ-D02)", **EF)

F(id="MDJ-D08-017", tech="efecto_conducta", func="Conducta regulada",
  defn="Acción u omisión objeto del efecto, expresada como verbo + objeto en forma normalizada breve.",
  just="Núcleo del mapa de obligaciones; permite buscar 'qué hay que hacer'.",
  dtype="String", card="1 obligatorio", values="No aplica: texto normalizado breve con evidencia", example="registrar la asistencia diaria del personal",
  extraction="Redactar verbo en infinitivo + objeto, sin añadir elementos no presentes en la evidencia.",
  validation="Todas las palabras de contenido deben poder rastrearse a la evidencia (control de no adición).",
  deps="MDJ-D08-012", **EF)

F(id="MDJ-D08-018", tech="efecto_condicion_aplicacion", func="Condición de aplicación del efecto",
  defn="Supuesto de hecho o condición que debe cumplirse para que el efecto opere.",
  just="Evita presentar como absolutas obligaciones condicionadas.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto con evidencia", example="cuando la empresa tenga más de 20 trabajadores",
  extraction="Extraer las cláusulas condicionales ('cuando', 'siempre que', 'en caso de') que gobiernan el operador.",
  validation="La condición debe estar en la misma unidad o en una referencia interna resuelta.", deps="MDJ-D08-012", **EF)

F(id="MDJ-D08-019", tech="efecto_plazo_cantidad", func="Plazo del efecto (cantidad)",
  defn="Cantidad numérica del plazo para cumplir el efecto.",
  just="Permite alertas y cálculo de vencimientos.",
  dtype="Integer", card="0..1 opcional", values="Entero positivo", example="10",
  extraction="Extraer el número del plazo expresado en cifras o letras.", validation="Entero > 0; cotejo cifras/letras si ambos existen.",
  deps="MDJ-D08-012", **{**EF, "origin": "Explícito en documento", "method": "Extracción directa + Normalización", "risk": "R2"})

F(id="MDJ-D08-020", tech="efecto_plazo_unidad", func="Plazo del efecto (unidad)",
  defn="Unidad del plazo: días hábiles, días calendario, meses, años u otra.",
  just="Sin unidad el plazo no es computable; la distinción hábil/calendario es jurídicamente decisiva.",
  dtype="Enum", card="0..1 obligatorio condicionado", values="CAT-530 Unidad de plazo", example="Días hábiles",
  extraction="Normalizar la unidad expresada; si dice 'días' sin calificar, registrar 'Días (sin calificar)' y no presumir.",
  validation="Obligatorio si existe MDJ-D08-019.", deps="MDJ-D08-019",
  **{**EF, "origin": "Explícito en documento", "method": "Extracción directa + Normalización"})

F(id="MDJ-D08-021", tech="efecto_plazo_hito_inicio", func="Hito de inicio del plazo",
  defn="Evento desde el cual se computa el plazo (notificación, publicación, ocurrencia del hecho…).",
  just="Necesario para calcular vencimientos.",
  dtype="String", card="0..1 opcional", values="No aplica: texto literal", example="desde el día siguiente de la notificación",
  extraction="Copiar la expresión que fija el inicio del cómputo.", validation="Verificación literal.",
  deps="MDJ-D08-019", **{**EF, "origin": "Explícito en documento", "method": "Extracción directa"})

F(id="MDJ-D08-022", tech="efecto_consecuencia_incumplimiento", func="Consecuencia del incumplimiento",
  defn="Consecuencia que la propia unidad prevé si el efecto no se cumple.",
  just="Conecta obligaciones con sanciones para estimar riesgo.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto con evidencia", example="multa de 1 a 10 UIT",
  extraction="Extraer solo si la consecuencia está en la misma unidad; si está en otra, usar MDJ-D08-023.",
  validation="Evidencia en la unidad; montos se registran además como registros D09.", deps="MDJ-D08-012; D09", **EF)

F(id="MDJ-D08-023", tech="efecto_unidad_sancionadora", func="Unidad que tipifica la sanción",
  defn="Referencia a la unidad estructural (de la misma u otra obra) que establece la sanción aplicable al incumplimiento.",
  just="Enlaza la obligación con su régimen sancionador para compliance.",
  dtype="Referencia", card="0..1 opcional", values="Unidad estructural", example="Reglamento de infracciones, art. 25, numeral 25.1",
  extraction="Usar la referencia normativa presente en la unidad o, en catálogos de infracciones, la unidad que remite a la obligación; no inferir por similitud.",
  validation="La referencia debe estar resuelta (MDJ-D07) a unidad.", deps="Referencias resueltas (MDJ-D07)", **EF)

F(id="MDJ-D08-024", tech="efecto_excepciones", func="Excepciones al efecto",
  defn="Supuestos en que el efecto no se aplica según la propia unidad.",
  just="Evita respuestas incompletas sobre obligaciones.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto con evidencia", example="salvo pacto en contrario",
  extraction="Extraer cláusulas 'salvo', 'excepto', 'no será exigible cuando' vinculadas al operador.",
  validation="Evidencia en la unidad.", deps="MDJ-D08-012", **EF)

F(id="MDJ-D08-025", tech="efecto_fecha_exigibilidad", func="Fecha de exigibilidad del efecto",
  defn="Fecha expresa desde la cual el efecto es exigible, cuando difiere de la entrada en vigor de la unidad.",
  just="Algunas obligaciones rigen con calendario propio; evita alertas erróneas.",
  dtype="Fecha", card="0..1 opcional", values="Fecha ISO 8601", example="2025-01-01",
  extraction="Extraer fechas o plazos de adecuación expresos ligados al efecto ('a partir del…', 'en un plazo de 180 días').",
  validation="Fecha válida; si es relativa, registrar el plazo y calcular en B.",
  deps="MDJ-D03 eventos; MDJ-D08-012", **{**EF, "origin": "Explícito en documento", "method": "Extracción directa + Normalización", "risk": "R1"})

# ---------------------------------------------------------------------------------------------
# D09 INFORMACIÓN ECONÓMICA Y CUANTITATIVA
# ---------------------------------------------------------------------------------------------
MO = dict(dim="D09", profiles="NOR; JUR; ADM", unit="Afirmación compuesta: monto",
          prio="P1", mode="A", stage="E3", risk="R1", review="Condicionado",
          funcs="F14; F07; F13; F03", origin="Explícito en documento", method="Extracción directa",
          evidence="Tramo literal con la cifra y su contexto inmediato (concepto, sujeto, rol)",
          cond="Toda cifra con significado jurídico-económico en unidades propias; en jurisprudencia y actos, prioritariamente en la parte resolutiva")

F(id="MDJ-D09-001", tech="monto_id", func="Identificador del monto",
  defn="Identificador persistente de cada registro de monto.",
  just="Permite seguir un mismo monto a lo largo de la cadena procesal.",
  dtype="Identificador", card="1 obligatorio", values="No aplica: generado por el sistema", example="MON-000552190",
  extraction="Asignar al crear el registro.", validation="Único, nunca reutilizado.",
  deps="No aplica: primer dato del registro",
  **{**MO, "origin": "Generado por sistema", "method": "Generado por sistema", "stage": "Sistema", "risk": "R3", "review": "No", "evidence": "No aplica: dato de sistema"})

F(id="MDJ-D09-002", tech="monto_unidad_origen", func="Unidad donde aparece el monto",
  defn="Fragmento o unidad estructural en la que aparece el monto.",
  just="Ancla el monto y permite distinguir parte resolutiva de antecedentes.",
  dtype="Referencia", card="1 obligatorio", values="Unidad estructural o Fragmento textual", example="Punto resolutivo 2",
  extraction="Tomar la unidad sobre la que corre el perfil.", validation="La unidad debe existir; si es contenido ajeno, el monto se descarta.",
  deps="MDJ-D05 segmentación; MDJ-PRO-029",
  **{**MO, "origin": "Generado por sistema", "method": "Generado por sistema", "stage": "Sistema", "risk": "R3", "review": "No", "evidence": "No aplica: es el sujeto del registro"})

F(id="MDJ-D09-003", tech="monto_texto_cifras", func="Monto en cifras (literal)",
  defn="Expresión numérica literal tal como aparece en el texto, con su formato original.",
  just="Conserva la fuente exacta para auditar la normalización (separadores decimales distintos por país).",
  dtype="String", card="0..1 obligatorio condicionado", values="No aplica: literal", example="S/ 12.450,00",
  extraction="Copiar la cifra con símbolo y separadores tal cual.", validation="Verificación literal; obligatorio si no existe monto en letras.",
  deps="MDJ-D09-002", **MO)

F(id="MDJ-D09-004", tech="monto_texto_letras", func="Monto en letras (literal)",
  defn="Expresión del monto en palabras, cuando el documento la incluye.",
  just="Permite el cotejo cifras-letras, control clave contra errores de OCR y de extracción.",
  dtype="String", card="0..1 opcional", values="No aplica: literal", example="doce mil cuatrocientos cincuenta y 00/100 soles",
  extraction="Copiar la expresión en letras asociada a la cifra.", validation="Verificación literal.",
  deps="MDJ-D09-002", **MO)

F(id="MDJ-D09-005", tech="monto_cotejo_cifras_letras", func="Cotejo cifras-letras",
  defn="Resultado de comparar el monto en cifras con el monto en letras.",
  just="Detecta errores de OCR, de extracción o del propio documento.",
  dtype="Enum", card="1 obligatorio", values="Coincide; Discrepa; Solo cifras; Solo letras", example="Coincide",
  extraction="No se extrae: se calcula convirtiendo ambas expresiones a número.",
  validation="'Discrepa' envía el registro a revisión y bloquea su uso en cálculos.",
  deps="MDJ-D09-003; MDJ-D09-004",
  **{**MO, "origin": "Derivado por cálculo", "method": "Cálculo", "mode": "B", "stage": "E8", "risk": "R2", "evidence": "Regla de conversión aplicada"})

F(id="MDJ-D09-006", tech="monto_cantidad", func="Cantidad normalizada",
  defn="Valor numérico del monto en la unidad en que está expresado (moneda, unidad de valor, porcentaje o unidad física).",
  just="Base de todos los cálculos y filtros por cuantía.",
  dtype="Decimal", card="0..1 obligatorio condicionado", values="Decimal ≥ 0", example="12450.00",
  extraction="Normalizar la cifra según el separador decimal del país del documento.",
  validation="Coherente con MDJ-D09-003/004; sin valor si la naturaleza es 'Por liquidar'.",
  deps="MDJ-D09-003; MDJ-D09-004; país (D01)",
  **{**MO, "origin": "Normalizado por regla", "method": "Normalización"})

F(id="MDJ-D09-007", tech="monto_tipo_unidad", func="Tipo de unidad del monto",
  defn="Indica si el monto está expresado en moneda, unidad de valor, porcentaje o unidad de medida física.",
  just="Evita sumar soles con UIT o porcentajes.",
  dtype="Enum", card="1 obligatorio", values="Moneda; Unidad de valor; Porcentaje; Unidad de medida física; Otra", example="Unidad de valor",
  extraction="Determinar por el símbolo o la denominación que acompaña la cifra.", validation="Exactamente uno de MDJ-D09-008/009/010 según el valor.",
  deps="MDJ-D09-003", **{**MO, "origin": "Normalizado por regla", "method": "Normalización", "risk": "R2"})

F(id="MDJ-D09-008", tech="monto_moneda", func="Moneda",
  defn="Moneda en que se expresa el monto, en código ISO 4217.",
  just="Imprescindible para comparar y convertir montos.",
  dtype="Código ISO", card="0..1 obligatorio condicionado", values="CAT-010 Moneda (ISO 4217); incluye monedas históricas", example="PEN",
  extraction="Normalizar símbolos y nombres ('S/', 'soles', '$', 'pesos', 'Bs.') según país y época; '$' es ambiguo entre países y con el dólar: resolver por contexto y país.",
  validation="Obligatorio si tipo de unidad = Moneda; código vigente en la fecha de referencia.",
  deps="MDJ-D09-007; país (D01); fecha (D03)", **{**MO, "origin": "Normalizado por regla", "method": "Normalización"})

F(id="MDJ-D09-009", tech="monto_unidad_valor", func="Unidad de valor de referencia",
  defn="Unidad de valor legal en que se expresa el monto (UIT, UVT, UF, UTM, UMA, salario mínimo u otra).",
  just="Muchas multas y topes se expresan en estas unidades; sin ellas el monto no es convertible.",
  dtype="Referencia", card="0..1 obligatorio condicionado", values="Entidad: unidad de valor (CAT-508, semilla pendiente)", example="UIT (PE)",
  extraction="Detectar la sigla o denominación de la unidad y vincularla al catálogo del país.",
  validation="Obligatorio si tipo de unidad = Unidad de valor; la unidad debe pertenecer al país del documento.",
  country_status="Catálogo por país", pending="DEC-29", deps="MDJ-D09-007; catálogo de unidades de valor",
  **{**MO, "origin": "Normalizado por regla", "method": "Normalización"})

F(id="MDJ-D09-010", tech="monto_unidad_medida", func="Unidad de medida física",
  defn="Unidad física de un valor cuantitativo no monetario (hectáreas, toneladas, metros cúbicos, kilogramos…).",
  just="Permite usar límites y umbrales regulatorios cuantitativos (ambientales, mineros, aduaneros).",
  dtype="Enum", card="0..1 obligatorio condicionado", values="CAT-509 Unidad de medida física", example="Toneladas métricas",
  extraction="Normalizar la unidad expresada junto a la cifra.", validation="Obligatorio si tipo de unidad = Unidad de medida física.",
  deps="MDJ-D09-007", **{**MO, "origin": "Normalizado por regla", "method": "Normalización", "risk": "R2", "prio": "P2", "mode": "C", "stage": "Posterior (C)"})

F(id="MDJ-D09-011", tech="monto_fecha_referencia", func="Fecha de referencia del monto",
  defn="Fecha o año al que corresponde el valor nominal del monto (año de la UIT aplicable, fecha del daño, fecha de la infracción).",
  just="Sin fecha de referencia no puede convertirse ni compararse un monto histórico.",
  dtype="Fecha parcial", card="1 obligatorio", values="ISO 8601 (AAAA, AAAA-MM o AAAA-MM-DD)", example="2023",
  extraction="Usar la fecha expresa asociada al monto; si no existe, aplicar MDJ-D09-012 y registrar la regla.",
  validation="No puede quedar vacía: si no es determinable, estado 'indeterminado' y el monto no se convierte.",
  deps="MDJ-D09-012; fechas del documento (D03)", **{**MO, "origin": "Normalizado por regla", "method": "Extracción directa + Normalización"})

F(id="MDJ-D09-012", tech="monto_regla_fecha_referencia", func="Criterio de la fecha de referencia",
  defn="Criterio usado para fijar la fecha de referencia: expresa en el texto, fecha de la infracción, fecha de emisión u otra regla nacional.",
  just="Hace auditable una decisión que cambia el valor convertido.",
  dtype="Enum", card="1 obligatorio", values="Expresa en el texto; Fecha de los hechos o infracción; Fecha de emisión; Regla nacional (ID); No determinable", example="Fecha de los hechos o infracción",
  extraction="Registrar 'Expresa' si el texto la indica; en otro caso, el criterio aplicado.",
  validation="Si es 'Regla nacional', la regla debe estar validada (DEC-29).", country_status="Pendiente validación nacional",
  pending="DEC-29", deps="MDJ-D09-011", **{**MO, "origin": "Normalizado por regla", "method": "Normalización", "risk": "R2"})

F(id="MDJ-D09-013", tech="monto_concepto_economico", func="Concepto económico",
  defn="Concepto al que responde el monto: multa, indemnización, remuneración, tributo, tasa, costas, intereses, garantía, tope, umbral, etc.",
  just="Distingue sanciones de reparaciones y de límites regulatorios.",
  dtype="Enum", card="1 obligatorio", values="CAT-505 Concepto económico", example="Multa administrativa",
  extraction="Clasificar por el sustantivo que califica la cifra en su contexto inmediato.",
  validation="Valor del catálogo con evidencia del sustantivo calificador.",
  deps="MDJ-D09-002", **{**MO, "origin": "Inferido por modelo", "method": "Clasificación", "risk": "R2"})

F(id="MDJ-D09-014", tech="monto_naturaleza_importe", func="Naturaleza del importe",
  defn="Si el importe es fijo, máximo, mínimo, rango, porcentaje sobre una base, estimado o por liquidar.",
  just="Evita presentar topes o rangos como importes determinados.",
  dtype="Enum", card="1 obligatorio", values="CAT-506 Naturaleza del importe", example="Rango",
  extraction="Detectar fórmulas 'hasta', 'no menor de', 'de… a…', 'equivalente al…%', 'por liquidar'.",
  validation="Si es Rango, deben existir MDJ-D09-019 y MDJ-D09-020.",
  deps="MDJ-D09-003", **{**MO, "origin": "Inferido por modelo", "method": "Clasificación", "risk": "R2"})

F(id="MDJ-D09-015", tech="monto_rol", func="Rol del monto en la decisión",
  defn="Papel del monto: pretendido por una parte, ordenado, confirmado, reducido, incrementado, revocado, propuesto por la autoridad instructora, tope normativo, etc.",
  just="Error frecuente y grave: confundir lo pedido con lo ordenado.",
  dtype="Enum", card="1 obligatorio", values="CAT-507 Rol del monto", example="Ordenado",
  extraction="Determinar el rol por la sección (pretensión, parte resolutiva) y por el verbo (solicita, ordena, confirma, reduce).",
  validation="'Ordenado', 'Confirmado' o 'Reducido' exigen evidencia en la parte resolutiva.",
  deps="MDJ-D09-002; secciones funcionales (D05)",
  **{**MO, "profiles": "JUR; ADM", "origin": "Inferido por modelo", "method": "Clasificación"})

F(id="MDJ-D09-016", tech="monto_sujeto_obligado", func="Obligado al pago",
  defn="Parte o actor que debe pagar o soportar el monto.",
  just="Permite análisis de contingencias por tipo de sujeto.",
  dtype="Referencia", card="0..1 opcional", values="Afirmación compuesta: parte o actor (D13) o tipo pivote CAT-504", example="Parte demandada (persona jurídica)",
  extraction="Vincular al registro de parte del proceso; en normativa, al tipo de destinatario.",
  validation="Respetar la política de datos personales: no registrar nombres de personas naturales (DEC-18).",
  privacy="Puede contener datos personales", pending="DEC-18", deps="Partes y roles (D13)",
  **{**MO, "origin": "Inferido por modelo", "method": "Inferencia", "risk": "R2"})

F(id="MDJ-D09-017", tech="monto_beneficiario", func="Beneficiario del monto",
  defn="Parte, actor o entidad a cuyo favor se establece el monto.",
  just="Completa la relación económica obligado-beneficiario.",
  dtype="Referencia", card="0..1 opcional", values="Afirmación compuesta: parte o actor (D13), organismo o tipo pivote", example="Tesoro público",
  extraction="Vincular al registro de parte o al organismo destinatario.",
  validation="Igual que MDJ-D09-016.", privacy="Puede contener datos personales", pending="DEC-18",
  deps="Partes y roles (D13)", **{**MO, "origin": "Inferido por modelo", "method": "Inferencia", "risk": "R2"})

F(id="MDJ-D09-018", tech="monto_condicion", func="Condición del monto",
  defn="Condición a la que está sujeto el monto (por cada día de retraso, si reincide, en caso de incumplimiento).",
  just="Evita tratar como cierto un monto condicional.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto con evidencia", example="por cada día de retraso en el cumplimiento",
  extraction="Extraer la cláusula condicional ligada a la cifra.", validation="Evidencia en el mismo segmento.",
  deps="MDJ-D09-003", **{**MO, "risk": "R2", "prio": "P2", "mode": "C", "stage": "Posterior (C)"})

F(id="MDJ-D09-019", tech="monto_limite_inferior", func="Límite inferior del rango",
  defn="Valor mínimo cuando el monto se expresa como rango o mínimo.",
  just="Necesario para escalas de sanciones.",
  dtype="Decimal", card="0..1 obligatorio condicionado", values="Decimal ≥ 0, en la misma unidad que el monto", example="1",
  extraction="Extraer el extremo inferior de 'de X a Y' o 'no menor de X'.", validation="≤ límite superior.",
  deps="MDJ-D09-014", **{**MO, "origin": "Normalizado por regla", "method": "Extracción directa + Normalización"})

F(id="MDJ-D09-020", tech="monto_limite_superior", func="Límite superior del rango",
  defn="Valor máximo cuando el monto se expresa como rango o tope.",
  just="Necesario para escalas de sanciones y topes regulatorios.",
  dtype="Decimal", card="0..1 obligatorio condicionado", values="Decimal ≥ 0, en la misma unidad que el monto", example="50",
  extraction="Extraer el extremo superior de 'de X a Y' o 'hasta Y'.", validation="≥ límite inferior.",
  deps="MDJ-D09-014", **{**MO, "origin": "Normalizado por regla", "method": "Extracción directa + Normalización"})

F(id="MDJ-D09-021", tech="monto_base_calculo", func="Base de cálculo del porcentaje",
  defn="Magnitud sobre la cual se aplica un porcentaje o tasa (remuneración, ventas anuales, valor en aduana, deuda tributaria).",
  just="Un porcentaje sin base no es interpretable.",
  dtype="String", card="0..1 obligatorio condicionado", values="No aplica: texto literal normalizado", example="ingresos netos del ejercicio anterior",
  extraction="Extraer el término que sigue a 'sobre', 'del', 'calculado sobre'.", validation="Obligatorio si tipo de unidad = Porcentaje.",
  deps="MDJ-D09-007", **{**MO, "risk": "R2"})

F(id="MDJ-D09-022", tech="monto_periodicidad", func="Periodicidad del monto",
  defn="Si el monto es único o periódico (diario, mensual, anual, por evento).",
  just="Permite estimar el impacto económico total.",
  dtype="Enum", card="1 obligatorio", values="CAT-531 Periodicidad", example="Único",
  extraction="Detectar expresiones de periodicidad; por defecto 'Único' solo si el texto no indica otra.",
  validation="Valor del catálogo.", deps="MDJ-D09-003", **{**MO, "origin": "Normalizado por regla", "method": "Normalización", "risk": "R2"})

F(id="MDJ-D09-023", tech="monto_por_liquidar", func="Monto por liquidar",
  defn="Indica que el texto ordena un concepto económico cuyo importe se determinará después (intereses, costas por liquidar).",
  just="Impide registrar como cero un importe indeterminado.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Verdadero",
  extraction="Detectar fórmulas 'a liquidarse', 'en ejecución de sentencia', 'más intereses legales'.",
  validation="Si es Verdadero, monto_cantidad debe estar vacío con estado 'no aplicable'.",
  deps="MDJ-D09-014", **{**MO, "profiles": "JUR; ADM"})

F(id="MDJ-D09-024", tech="monto_valor_convertido", func="Valor convertido a moneda (histórico)",
  defn="Equivalente en moneda del monto expresado en unidad de valor, calculado con el valor de la unidad en la fecha de referencia.",
  just="Permite comparar montos en UIT, UF o UMA sin perder su valor histórico.",
  dtype="Decimal", card="0..1 obligatorio condicionado", values="Decimal ≥ 0", example="61800.00",
  extraction="No se extrae: cantidad × valor de la unidad en la fecha de referencia (catálogo de unidades de valor).",
  validation="Solo si fecha de referencia y valor de la unidad existen; nunca usar el valor actual de la unidad.",
  pending="DEC-29", country_status="Catálogo por país",
  deps="MDJ-D09-006; MDJ-D09-009; MDJ-D09-011; MDJ-D09-034..038",
  **{**MO, "origin": "Derivado por cálculo", "method": "Cálculo", "mode": "B", "stage": "E7", "risk": "R2", "review": "No", "evidence": "Regla de conversión (ID y versión) y valor de la unidad usado"})

F(id="MDJ-D09-025", tech="monto_moneda_conversion", func="Moneda del valor convertido",
  defn="Moneda en la que se expresa el valor convertido.",
  just="Completa el valor convertido.",
  dtype="Código ISO", card="0..1 obligatorio condicionado", values="CAT-010 Moneda (ISO 4217)", example="PEN",
  extraction="No se extrae: moneda de la unidad de valor.", validation="Obligatoria si existe MDJ-D09-024.",
  deps="MDJ-D09-024", **{**MO, "origin": "Derivado por cálculo", "method": "Cálculo", "mode": "B", "stage": "E7", "risk": "R3", "review": "No", "evidence": "Regla de conversión aplicada"})

F(id="MDJ-D09-026", tech="monto_regla_conversion", func="Regla de conversión aplicada",
  defn="Identificador y versión de la regla y del valor de serie usados para convertir el monto.",
  just="Hace reproducible y corregible la conversión.",
  dtype="String", card="0..1 obligatorio condicionado", values="ID de regla + versión + ID del valor de la unidad", example="CONV-UV-PE-v1 / UIT-2023",
  extraction="Registrar automáticamente al calcular.", validation="Obligatoria si existe MDJ-D09-024.",
  deps="MDJ-D09-024", **{**MO, "origin": "Generado por sistema", "method": "Generado por sistema", "mode": "B", "stage": "E7", "risk": "R3", "review": "No", "evidence": "No aplica: dato de sistema"})

F(id="MDJ-D09-027", tech="monto_valor_actualizado", func="Valor actualizado",
  defn="Valor del monto actualizado a una fecha posterior mediante un índice (inflación, reajuste legal).",
  just="Útil para estimar contingencias actuales sin perder el valor histórico.",
  dtype="Decimal", card="0..1 opcional", values="Decimal ≥ 0", example="70210.55",
  extraction="No se extrae: se calcula a pedido con la regla y la fecha de actualización indicadas.",
  validation="Siempre acompañado de MDJ-D09-028 y MDJ-D09-029; nunca sustituye al valor histórico.",
  pending="DEC-29", deps="MDJ-D09-024 o MDJ-D09-006; serie de índices (fuente externa)",
  **{**MO, "origin": "Derivado por cálculo", "method": "Cálculo", "prio": "P3", "mode": "B", "stage": "E7", "risk": "R2", "review": "No", "funcs": "F14", "evidence": "Regla e índice usados"})

F(id="MDJ-D09-028", tech="monto_fecha_actualizacion", func="Fecha de actualización",
  defn="Fecha a la que se actualizó el monto.",
  just="Un valor actualizado sin fecha es engañoso.",
  dtype="Fecha", card="0..1 obligatorio condicionado", values="Fecha ISO 8601", example="2026-10-31",
  extraction="Registrar al calcular.", validation="Obligatoria si existe MDJ-D09-027.",
  deps="MDJ-D09-027", **{**MO, "origin": "Generado por sistema", "method": "Generado por sistema", "prio": "P3", "mode": "B", "stage": "E7", "risk": "R3", "review": "No", "funcs": "F14", "evidence": "No aplica: dato de sistema"})

F(id="MDJ-D09-029", tech="monto_regla_actualizacion", func="Regla de actualización",
  defn="Índice o regla de reajuste usada (IPC, interés legal, reajuste por unidad de valor) con su versión.",
  just="Permite auditar y cambiar la regla sin perder el histórico.",
  dtype="String", card="0..1 obligatorio condicionado", values="ID de regla + versión", example="ACT-IPC-PE-v1",
  extraction="Registrar al calcular.", validation="Obligatoria si existe MDJ-D09-027.",
  deps="MDJ-D09-027", **{**MO, "origin": "Generado por sistema", "method": "Generado por sistema", "prio": "P3", "mode": "B", "stage": "E7", "risk": "R3", "review": "No", "funcs": "F14", "evidence": "No aplica: dato de sistema"})

F(id="MDJ-D09-030", tech="monto_final_proceso", func="Monto final del proceso",
  defn="Monto que resulta firme al final de la cadena procesal, calculado a partir de los montos ordenados, confirmados, reducidos o revocados en cada instancia.",
  just="Responde cuánto se pagó o debe pagarse realmente, no lo que dijo una instancia.",
  dtype="Decimal", card="0..1 opcional", values="Decimal ≥ 0", example="20000.00",
  extraction="No se extrae: se calcula recorriendo la cadena procesal (relaciones confirma/revoca/reduce) del proceso.",
  validation="Solo si la cadena está completa y la última resolución consta como firme; en otro caso, estado 'indeterminado'.",
  unit="Proceso", profiles="JUR; ADM",
  deps="Cadena procesal (D07, D14); MDJ-D09-015; firmeza (D14)",
  **{k: v for k, v in MO.items() if k not in ("unit", "profiles")} | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "evidence": "Regla aplicada e IDs de los montos usados"})

F(id="MDJ-D09-031", tech="monto_final_proceso_estado", func="Estado del monto final",
  defn="Certeza del monto final: firme, no firme o indeterminado por cadena incompleta.",
  just="Evita presentar como definitivo un monto aún impugnable.",
  dtype="Enum", card="0..1 obligatorio condicionado", values="Firme; No firme; Indeterminado (cadena incompleta)", example="Firme",
  extraction="No se extrae: resultado del cálculo de MDJ-D09-030.", validation="Obligatorio si existe MDJ-D09-030.",
  unit="Proceso", profiles="JUR; ADM", deps="MDJ-D09-030",
  **{k: v for k, v in MO.items() if k not in ("unit", "profiles")} | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "evidence": "Regla aplicada"})

F(id="MDJ-D09-032", tech="contiene_montos", func="Contiene montos",
  defn="Indica si la obra tiene al menos un registro de monto.",
  just="Filtro rápido para análisis económicos.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Verdadero",
  extraction="No se extrae: se calcula de la existencia de registros de monto.",
  validation="Falso solo si el perfil de montos se ejecutó (estado distinto de 'no procesado').",
  unit="Obra", profiles="NOR; JUR; ADM", deps="MDJ-D09-001; estado de campo (MDJ-OPE)",
  **{k: v for k, v in MO.items() if k not in ("unit", "profiles")} | {"origin": "Derivado por cálculo", "method": "Cálculo", "mode": "B", "stage": "E7", "risk": "R3", "review": "No", "funcs": "F03; F14", "evidence": "Regla aplicada"})

UV = dict(dim="D09", profiles="NOR; JUR; ADM", unit="Entidad: unidad de valor", prio="P1", mode="D",
          stage="Curaduría", risk="R1", review="Sí", origin="Fuente externa", method="Enriquecimiento externo",
          country_status="Catálogo por país", pending="DEC-29", funcs="F14; F13; F09",
          evidence="Norma o fuente oficial que fija el valor", cond="Catálogo maestro por país; se usa para convertir montos")

F(id="MDJ-D09-033", tech="unidad_valor_codigo", func="Código de la unidad de valor",
  defn="Sigla normalizada de la unidad de valor legal.",
  just="Clave del catálogo que usan los registros de monto.",
  dtype="String", card="1 obligatorio", values="CAT-508 Unidad de valor por país (semilla)", example="UIT",
  extraction="Curaduría del catálogo, no del documento.", validation="Único por país y periodo.",
  deps="No aplica: entidad maestra", **UV)

F(id="MDJ-D09-034", tech="unidad_valor_pais", func="País de la unidad de valor",
  defn="País cuyo ordenamiento define la unidad.",
  just="Evita aplicar una unidad a documentos de otro país.",
  dtype="Código ISO", card="1 obligatorio", values="CAT-001 País y jurisdicción", example="PE",
  extraction="Curaduría.", validation="Código ISO válido.", deps="MDJ-D09-033", **UV)

F(id="MDJ-D09-035", tech="unidad_valor_periodo", func="Periodo de vigencia del valor",
  defn="Intervalo durante el que rige un valor de la unidad (año, mes o día, según la unidad).",
  just="La UIT es anual, la UF diaria: el periodo es parte de la identidad del valor.",
  dtype="Intervalo de fechas", card="1 obligatorio", values="Intervalo ISO 8601", example="2023-01-01/2023-12-31",
  extraction="Curaduría a partir de la norma o serie oficial.", validation="Sin solapamientos para la misma unidad.",
  deps="MDJ-D09-033", **UV)

F(id="MDJ-D09-036", tech="unidad_valor_monto", func="Valor en moneda",
  defn="Valor monetario de la unidad durante el periodo.",
  just="Base de la conversión de montos.",
  dtype="Decimal", card="1 obligatorio", values="Decimal > 0", example="4950.00",
  extraction="Curaduría a partir de la norma o serie oficial.", validation="Cotejado con la fuente oficial citada.",
  deps="MDJ-D09-035", **UV)

F(id="MDJ-D09-037", tech="unidad_valor_moneda", func="Moneda del valor",
  defn="Moneda en que se expresa el valor de la unidad.",
  just="Completa el valor.", dtype="Código ISO", card="1 obligatorio", values="CAT-010 Moneda (ISO 4217)", example="PEN",
  extraction="Curaduría.", validation="Moneda de curso legal del país en el periodo.", deps="MDJ-D09-036", **UV)

F(id="MDJ-D09-038", tech="unidad_valor_fuente", func="Fuente oficial del valor",
  defn="Norma (referencia a obra) o serie oficial (URL) que fija el valor del periodo.",
  just="Trazabilidad de un dato que cambia montos convertidos.",
  dtype="Objeto", card="1 obligatorio", values="{obra: Referencia | url: URL, fecha_consulta: Fecha}", example="{obra: 'DS 309-2022-EF', fecha_consulta: '2026-11-20'}",
  extraction="Curaduría.", validation="Debe existir al menos una de obra o URL.", deps="MDJ-D09-036", **UV)

# ---------------------------------------------------------------------------------------------
# D11 CALIDAD Y CONFIABILIDAD DOCUMENTAL
# ---------------------------------------------------------------------------------------------
QA = dict(dim="D11", profiles="UNI", unit="Manifestación", prio="P0", mode="A", stage="E0", risk="R2",
          review="No", funcs="F16; F02; F15", origin="Derivado por cálculo", method="Cálculo",
          evidence="Resultado de la regla o del análisis técnico aplicado, con su versión",
          cond="Toda manifestación ingerida. Describe la calidad del documento, no el estado del procesamiento (este va en MDJ-OPE)")

F(id="MDJ-D11-001", tech="texto_nativo_disponible", func="Texto nativo disponible",
  defn="Indica si la manifestación trae una capa de texto digital utilizable (no solo imagen).",
  just="Determina si se requiere OCR y fija la confianza máxima alcanzable.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Falso",
  extraction="Detectar capa de texto y su proporción de caracteres válidos por página.",
  validation="Falso si menos del umbral de páginas con texto (umbral configurable en el piloto).",
  deps="Archivo ingerido", **QA)

F(id="MDJ-D11-002", tech="ocr_aplicado", func="OCR aplicado",
  defn="Indica si el texto se obtuvo mediante reconocimiento óptico de caracteres.",
  just="Señal de riesgo de errores en cifras, fechas y nombres.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Verdadero",
  extraction="Registrar automáticamente en E0.", validation="Verdadero implica MDJ-D11-003 y MDJ-D11-004.",
  deps="MDJ-D11-001", **{**QA, "origin": "Generado por sistema", "method": "Generado por sistema", "risk": "R3"})

F(id="MDJ-D11-003", tech="ocr_motor_version", func="Motor y versión de OCR",
  defn="Herramienta y versión de OCR usadas.",
  just="Permite reprocesar selectivamente si se mejora el OCR.",
  dtype="String", card="0..1 obligatorio condicionado", values="No aplica: texto de sistema", example="motorOCR 5.3 (es)",
  extraction="Registrar automáticamente.", validation="Obligatorio si OCR aplicado.",
  deps="MDJ-D11-002", **{**QA, "origin": "Generado por sistema", "method": "Generado por sistema", "risk": "R3"})

F(id="MDJ-D11-004", tech="ocr_confianza_media", func="Confianza media del OCR",
  defn="Confianza media de reconocimiento reportada por el OCR, de 0 a 1.",
  just="Insumo del techo de confianza de las afirmaciones.",
  dtype="Decimal", card="0..1 obligatorio condicionado", values="0.00–1.00", example="0.87",
  extraction="Promediar la confianza por palabra del motor.", validation="Rango 0–1.",
  deps="MDJ-D11-002", **QA)

F(id="MDJ-D11-005", tech="legibilidad_nivel", func="Nivel de legibilidad",
  defn="Calidad del texto disponible para lectura automática: alta, media, baja o inutilizable.",
  just="Condiciona qué perfiles se ejecutan y qué estados son posibles ('no encontrado' exige legibilidad suficiente).",
  dtype="Enum", card="1 obligatorio", values="CAT-510 Nivel de calidad", example="Media",
  extraction="Calcular con proporción de palabras de diccionario, caracteres extraños y confianza OCR.",
  validation="Umbrales calibrados en el piloto.", deps="MDJ-D11-001; MDJ-D11-004", **QA)

F(id="MDJ-D11-006", tech="integridad_archivo", func="Integridad del archivo",
  defn="Estado técnico del archivo: íntegro, dañado, truncado o protegido.",
  just="Detecta archivos que no deben procesarse.",
  dtype="Enum", card="1 obligatorio", values="Íntegro; Dañado; Truncado; Protegido o cifrado", example="Íntegro",
  extraction="Validar estructura del archivo y hash.", validation="Dañado o Protegido bloquea etapas E1 en adelante.",
  deps="Archivo ingerido", **{**QA, "risk": "R3"})

F(id="MDJ-D11-007", tech="paginas_total", func="Número de páginas",
  defn="Número de páginas de la manifestación.",
  just="Control de completitud y de costo de procesamiento.",
  dtype="Integer", card="0..1 obligatorio condicionado", values="Entero ≥ 1", example="34",
  extraction="Leer del archivo.", validation="Obligatorio en formatos paginados.",
  deps="Archivo ingerido", **{**QA, "origin": "Generado por sistema", "method": "Generado por sistema", "risk": "R3"})

F(id="MDJ-D11-008", tech="paginacion_completa", func="Paginación completa",
  defn="Resultado de verificar saltos o ausencias de páginas según la numeración impresa.",
  just="Detecta documentos incompletos antes de extraer conclusiones.",
  dtype="Enum", card="1 obligatorio", values="Completa; Con saltos; Sin numeración verificable", example="Con saltos",
  extraction="Comparar la numeración impresa con el orden de páginas.", validation="'Con saltos' activa la marca de incompletitud.",
  deps="MDJ-D11-007", **QA)

F(id="MDJ-D11-009", tech="secciones_obligatorias_presentes", func="Secciones obligatorias presentes",
  defn="Secciones exigidas para el tipo documental que se encontraron (encabezado, parte considerativa, parte resolutiva, firmas, fórmula de promulgación…).",
  just="Control de completitud por tipo; base del estado 'no encontrado' frente a 'indeterminado'.",
  dtype="Enum múltiple", card="0..n", values="CAT-529 Sección obligatoria por tipo documental", example="[Encabezado; Considerandos; Parte resolutiva; Firma]",
  extraction="Comparar las secciones funcionales detectadas (D05) con la lista exigida para el tipo y naturaleza.",
  validation="Lista exigida definida por naturaleza jurídica y validada por país.",
  country_status="Pendiente validación nacional", pending="DEC-08",
  deps="Secciones funcionales (D05); naturaleza jurídica (D04)", **{**QA, "stage": "E2", "unit": "Versión"})

F(id="MDJ-D11-010", tech="secciones_obligatorias_ausentes", func="Secciones obligatorias ausentes",
  defn="Secciones exigidas para el tipo documental que no se encontraron.",
  just="Señala documentos incompletos (p. ej., sentencia sin parte resolutiva).",
  dtype="Enum múltiple", card="0..n", values="CAT-529 Sección obligatoria por tipo documental", example="[Parte resolutiva]",
  extraction="Diferencia entre lo exigido y MDJ-D11-009.", validation="Si contiene 'Parte resolutiva', se suprimen campos de decisión.",
  country_status="Pendiente validación nacional", pending="DEC-08",
  deps="MDJ-D11-009", **{**QA, "stage": "E2", "unit": "Versión"})

F(id="MDJ-D11-011", tech="completitud_documental", func="Completitud documental",
  defn="Juicio técnico sobre si el texto disponible es completo, incompleto, un extracto o resumen, o indeterminado.",
  just="Ninguna conclusión de ausencia ('no fija plazo') puede sostenerse sobre un texto incompleto.",
  dtype="Enum", card="1 obligatorio", values="Completo; Incompleto; Extracto o resumen; Indeterminado", example="Extracto o resumen",
  extraction="Calcular con MDJ-D11-008 y MDJ-D11-010 y señales como 'resumen ejecutivo'.",
  validation="'Completo' exige paginación completa y ninguna sección obligatoria ausente.",
  deps="MDJ-D11-008; MDJ-D11-010", **{**QA, "stage": "E2", "unit": "Versión", "risk": "R1"})

F(id="MDJ-D11-012", tech="cobertura_textual_disponible", func="Cobertura textual disponible",
  defn="Qué parte del documento posee Juztina: texto completo, texto parcial, solo resumen o solo metadatos.",
  just="Distingue lo que Juztina tiene de lo que la fuente publica (MDJ-D16-007).",
  dtype="Enum", card="1 obligatorio", values="Texto completo; Texto parcial; Solo resumen; Solo metadatos", example="Solo resumen",
  extraction="Determinar en la ingesta según el contenido de la manifestación.", validation="Coherente con MDJ-D11-011.",
  deps="MDJ-D11-011", **{**QA, "risk": "R2"})

F(id="MDJ-D11-013", tech="numeracion_estructural_continua", func="Numeración estructural continua",
  defn="Indica si la numeración de las unidades rotuladas (artículos, considerandos, fundamentos) es continua o presenta saltos no explicados.",
  just="Detecta errores de segmentación o texto faltante.",
  dtype="Boolean", card="0..1 obligatorio condicionado", values="Verdadero; Falso", example="Falso",
  extraction="Recorrer los rótulos detectados y verificar la secuencia, admitiendo 'bis', '-A', derogados.",
  validation="Falso envía la versión a revisión de segmentación.",
  deps="Unidades estructurales (D05)", **{**QA, "stage": "E2", "unit": "Versión"})

F(id="MDJ-D11-014", tech="calidad_segmentacion", func="Calidad de la segmentación",
  defn="Evaluación de la segmentación estructural: alta, media, baja o inutilizable.",
  just="Una segmentación mala contamina vigencia, relaciones y clasificación.",
  dtype="Enum", card="1 obligatorio", values="CAT-510 Nivel de calidad", example="Alta",
  extraction="Calcular con continuidad de numeración, cobertura del texto por unidades y validaciones estructurales.",
  validation="Calidad baja o inutilizable bloquea E5 y E6.", deps="MDJ-D11-013", **{**QA, "stage": "E2", "unit": "Versión"})

F(id="MDJ-D11-015", tech="calidad_tablas_anexos", func="Calidad de tablas y anexos",
  defn="Estado de las tablas y anexos tras la extracción: preservados, degradados o no detectados.",
  just="Muchas normas regulatorias y escalas de multas viven en tablas y anexos.",
  dtype="Enum", card="1 obligatorio", values="Preservados; Degradados; No detectados; No contiene", example="Degradados",
  extraction="Detectar estructuras tabulares y comparar con el texto lineal extraído.", validation="Valor del catálogo.",
  deps="MDJ-D11-001", **{**QA, "prio": "P1"})

F(id="MDJ-D11-016", tech="documento_compuesto", func="Documento compuesto",
  defn="Indica si la manifestación contiene más de una obra (p. ej., una edición del diario oficial con varias normas).",
  just="Evita fusionar obras distintas en una sola.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Verdadero",
  extraction="Resultado de la separación de obras en E1.", validation="Verdadero exige MDJ-D11-017 > 1.",
  deps="Etapa E1", **{**QA, "stage": "E1", "origin": "Inferido por modelo", "method": "Inferencia", "risk": "R1", "review": "Condicionado"})

F(id="MDJ-D11-017", tech="numero_obras_contenidas", func="Número de obras contenidas",
  defn="Cantidad de obras identificadas en la manifestación.",
  just="Control de la separación de obras.",
  dtype="Integer", card="1 obligatorio", values="Entero ≥ 1", example="12",
  extraction="Contar las obras separadas en E1.", validation="Coincide con las obras vinculadas a la manifestación.",
  deps="MDJ-D11-016", **{**QA, "stage": "E1", "risk": "R2"})

F(id="MDJ-D11-018", tech="confiabilidad_fuente", func="Confiabilidad de la fuente",
  defn="Grado de autoridad de la fuente de la manifestación: oficial auténtica, oficial informativa, institucional secundaria, editorial comercial, desconocida.",
  just="Distingue el texto oficial de copias de terceros; condiciona la presentación de la vigencia.",
  dtype="Enum", card="1 obligatorio", values="CAT-512 Confiabilidad de la fuente", example="Institucional secundaria",
  extraction="Asignar según el catálogo de fuentes (entidad publicación o fuente) y el dominio de origen.",
  validation="La fuente debe existir en el catálogo de publicaciones y fuentes.",
  country_status="Catálogo por país", pending="DEC-17",
  deps="Fuente de publicación (D02)", **{**QA, "origin": "Normalizado por regla", "method": "Normalización", "risk": "R2"})

F(id="MDJ-D11-019", tech="techo_confianza", func="Techo de confianza",
  defn="Confianza máxima que puede alcanzar cualquier afirmación extraída de esta manifestación, según su calidad.",
  just="Aplica la regla de control 9: la calidad del texto limita la confianza.",
  dtype="Decimal", card="1 obligatorio", values="0.00–1.00", example="0.70",
  extraction="Calcular con legibilidad, OCR, completitud y calidad de segmentación según tabla configurable.",
  validation="Toda afirmación de la manifestación ≤ techo.", deps="MDJ-D11-005; MDJ-D11-011; MDJ-D11-014",
  **{**QA, "stage": "E8", "mode": "B", "risk": "R2"})

F(id="MDJ-D11-020", tech="incidencias_calidad", func="Incidencias de calidad",
  defn="Lista de problemas detectados: columnas mezcladas, sellos sobre texto, páginas rotadas, marcas de agua, texto cortado, idioma mixto…",
  just="Guía el reprocesamiento y explica estados 'indeterminado'.",
  dtype="Enum múltiple", card="0..n", values="CAT-511 Tipo de incidencia de calidad", example="[Columnas mezcladas; Sellos sobre texto]",
  extraction="Registrar durante E0–E2 cada incidencia detectada.", validation="Valores del catálogo.",
  deps="Etapas E0–E2", **{**QA, "origin": "Inferido por modelo", "method": "Inferencia", "risk": "R3"})

F(id="MDJ-D11-021", tech="duplicado_candidato_de", func="Posible duplicado de",
  defn="Otras manifestaciones que podrían contener la misma obra o versión.",
  just="Base de la deduplicación entre fuentes.",
  dtype="Array de referencias", card="0..n", values="Manifestación", example="[MAN-PE-000331, MAN-PE-009812]",
  extraction="Comparar hash, identificadores oficiales y similitud de texto.", validation="No fusionar automáticamente; requiere MDJ-D11-022.",
  deps="Identificación oficial (D01); hash", **{**QA, "stage": "E1", "prio": "P0", "mode": "B"})

F(id="MDJ-D11-022", tech="tipo_duplicidad", func="Tipo de duplicidad",
  defn="Naturaleza de la coincidencia con el candidato: archivo idéntico, misma versión en otra fuente, versión distinta de la misma obra, falsa coincidencia.",
  just="Una versión distinta no es un duplicado: es historia de la obra.",
  dtype="Enum", card="0..1 obligatorio condicionado", values="Idéntico (hash); Misma versión, otra fuente; Otra versión de la obra; Falsa coincidencia", example="Otra versión de la obra",
  extraction="Comparar texto y fechas entre candidatos.", validation="'Otra versión' crea o vincula una versión (D03), no elimina la manifestación.",
  deps="MDJ-D11-021", **{**QA, "stage": "E1", "mode": "B", "risk": "R2", "review": "Condicionado"})

F(id="MDJ-D11-023", tech="estado_enlace_fuente", func="Estado del enlace a la fuente",
  defn="Resultado de la última verificación del enlace de origen: verificado, no responde, redirige, cambió de contenido.",
  just="Mantiene la trazabilidad hacia la fuente oficial; los mapas de fuentes de Bolivia ya usan este dato.",
  dtype="Enum", card="1 obligatorio", values="Verificado; No responde; Redirige; Contenido cambiado; No verificado", example="Verificado",
  extraction="Verificación periódica automática del URL de origen.", validation="Acompañado de MDJ-D16-016 (fecha de verificación).",
  deps="URL de origen (D01)", **{**QA, "origin": "Generado por sistema", "method": "Generado por sistema", "prio": "P1", "stage": "Sistema", "risk": "R3"})

F(id="MDJ-D11-024", tech="calidad_global", func="Calidad global de la manifestación",
  defn="Síntesis de la calidad de la manifestación para priorizar uso y reprocesamiento.",
  just="Indicador único para paneles de calidad y para el asistente.",
  dtype="Enum", card="1 obligatorio", values="CAT-510 Nivel de calidad", example="Media",
  extraction="Calcular con la regla de síntesis versionada sobre los campos D11.", validation="Regla versionada.",
  deps="MDJ-D11-005; MDJ-D11-011; MDJ-D11-014", **{**QA, "stage": "E8", "mode": "B", "risk": "R3"})

# ---------------------------------------------------------------------------------------------
# D16 DERECHOS, ACCESO Y DATOS PERSONALES
# ---------------------------------------------------------------------------------------------
DP = dict(dim="D16", profiles="UNI", unit="Obra", prio="P0", mode="A", stage="E3", risk="R1",
          review="Condicionado", funcs="F17; F02; F03", origin="Inferido por modelo", method="Clasificación",
          privacy="Ninguna", evidence="Tramo que contiene el dato o la marca (sin copiar datos personales a otros campos)",
          cond="Toda obra; se aplica antes de cualquier campo que pueda estructurar datos personales")

F(id="MDJ-D16-001", tech="acceso_fuente", func="Régimen de acceso en la fuente",
  defn="Condición de acceso al documento en su fuente: abierto, con registro, de pago, restringido o confidencial.",
  just="Determina qué puede mostrarse y si el documento puede incorporarse; los mapas de fuentes de Bolivia ya lo registran.",
  dtype="Enum", card="1 obligatorio", values="CAT-513 Acceso", example="Restringido (pago)",
  extraction="Asignar desde el catálogo de fuentes; confirmar con avisos en la manifestación.",
  validation="Valor del catálogo; coherente con la fuente (D02).", unit="Manifestación",
  deps="Fuente de publicación (D02)", **{k: v for k, v in DP.items() if k != "unit"} | {"origin": "Normalizado por regla", "method": "Normalización", "stage": "E0", "risk": "R2", "review": "No", "privacy": "Restricción de acceso o derechos"})

F(id="MDJ-D16-002", tech="licencia_reutilizacion", func="Licencia o régimen de reutilización",
  defn="Licencia o régimen jurídico que rige la reutilización del texto (dominio público oficial, Creative Commons, todos los derechos reservados, desconocida).",
  just="Indispensable para decidir uso, resumen y reproducción, sobre todo en doctrina.",
  dtype="Enum", card="1 obligatorio", values="CAT-514 Licencia o régimen de reutilización", example="CC BY-NC 4.0",
  extraction="Leer avisos de licencia en la manifestación o en la fuente; en textos oficiales, aplicar el régimen del país validado.",
  validation="'Desconocida' si no hay evidencia; nunca presumir libre uso.",
  country_status="Pendiente validación nacional", pending="DEC-27", unit="Manifestación",
  deps="MDJ-D16-001", **{k: v for k, v in DP.items() if k != "unit"} | {"origin": "Explícito en documento", "method": "Extracción directa + Normalización", "stage": "E0", "risk": "R1", "privacy": "Restricción de acceso o derechos"})

F(id="MDJ-D16-003", tech="titular_derechos", func="Titular de los derechos de autor",
  defn="Persona o entidad titular de los derechos patrimoniales declarada en la obra (editorial, revista, autor).",
  just="Necesario para gestionar permisos de doctrina.",
  dtype="String", card="0..1 opcional", values="No aplica: texto literal", example="Fondo Editorial de la Universidad X",
  extraction="Leer la nota de copyright o créditos editoriales.", validation="Verificación literal.",
  profiles="DOC", deps="MDJ-D16-002",
  **{k: v for k, v in DP.items() if k != "profiles"} | {"origin": "Explícito en documento", "method": "Extracción directa", "prio": "P1", "stage": "E3", "risk": "R2", "privacy": "Restricción de acceso o derechos", "review": "No"})

F(id="MDJ-D16-004", tech="condiciones_uso_declaradas", func="Condiciones de uso declaradas",
  defn="Texto de las condiciones o restricciones de uso que acompañan la obra o su fuente.",
  just="Soporte literal para la decisión de uso permitido.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto literal", example="Prohibida la reproducción total o parcial sin autorización",
  extraction="Copiar avisos de reserva de derechos o términos de la plataforma.", validation="Verificación literal.",
  profiles="DOC; JUR; ADM; NOR", pending="DEC-27", deps="MDJ-D16-002",
  **{k: v for k, v in DP.items() if k != "profiles"} | {"origin": "Explícito en documento", "method": "Extracción directa", "prio": "P1", "stage": "E0", "risk": "R2", "privacy": "Restricción de acceso o derechos", "review": "No"})

F(id="MDJ-D16-005", tech="uso_permitido_resumen", func="Uso permitido: resumen",
  defn="Si Juztina puede generar y mostrar resúmenes de la obra, según licencia, condiciones y política interna.",
  just="Aplica la política de uso de doctrina protegida sin decidir caso por caso.",
  dtype="Enum", card="1 obligatorio", values="Permitido; Limitado; No permitido; Pendiente de política", example="Limitado",
  extraction="No se extrae: se calcula con la política de uso (DEC-27) sobre licencia y condiciones.",
  validation="'Pendiente de política' mientras DEC-27 no se resuelva.", pending="DEC-27",
  deps="MDJ-D16-002; MDJ-D16-004",
  **DP | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "prio": "P1", "privacy": "Restricción de acceso o derechos", "evidence": "Regla de política aplicada"})

F(id="MDJ-D16-006", tech="uso_permitido_reproduccion", func="Uso permitido: reproducción de texto",
  defn="Si Juztina puede mostrar el texto (completo o en citas extensas) al usuario.",
  just="Evita infracciones de derechos de autor y de términos de plataformas.",
  dtype="Enum", card="1 obligatorio", values="Texto completo; Citas breves; Solo referencia; Pendiente de política", example="Citas breves",
  extraction="No se extrae: se calcula con la política de uso.", validation="Igual que MDJ-D16-005.", pending="DEC-27",
  deps="MDJ-D16-002; MDJ-D16-004",
  **DP | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "prio": "P1", "privacy": "Restricción de acceso o derechos", "evidence": "Regla de política aplicada"})

F(id="MDJ-D16-007", tech="fuente_publica_texto_completo", func="La fuente publica el texto completo",
  defn="Si la fuente custodia publica el texto completo, solo un resumen o comunicado, o no publica el documento.",
  just="Explica ausencias (laudos confidenciales, resúmenes ejecutivos) y orienta la adquisición; distinto de lo que Juztina posee (MDJ-D11-012).",
  dtype="Enum", card="1 obligatorio", values="Sí, texto completo; Parcial o resumen; No publica; Desconocido", example="Parcial o resumen",
  extraction="Asignar desde el catálogo de fuentes y avisos de la manifestación.", validation="Valor del catálogo.",
  unit="Manifestación", deps="Fuente (D02)",
  **{k: v for k, v in DP.items() if k != "unit"} | {"origin": "Normalizado por regla", "method": "Normalización", "prio": "P1", "stage": "E0", "risk": "R3", "review": "No"})

F(id="MDJ-D16-008", tech="reserva_confidencialidad_declarada", func="Reserva o confidencialidad declarada",
  defn="Si el documento o parte de él se declara reservado, confidencial o secreto.",
  just="Impide exponer información protegida por ley o por pacto (arbitraje, conciliación).",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Falso",
  extraction="Detectar sellos o fórmulas de reserva ('reservado', 'confidencial', 'versión pública').",
  validation="Verdadero exige revisión antes de cualquier exposición.",
  deps="Texto de la manifestación", **DP | {"origin": "Explícito en documento", "method": "Extracción directa", "privacy": "Restricción de acceso o derechos", "review": "Sí"})

F(id="MDJ-D16-009", tech="base_reserva", func="Base de la reserva",
  defn="Fundamento invocado para la reserva (norma, pacto de confidencialidad, reglamento arbitral).",
  just="Permite decidir si la reserva sigue vigente.",
  dtype="Texto largo", card="0..1 obligatorio condicionado", values="No aplica: texto literal con referencia (D07) si existe", example="Art. 91 del Reglamento de Arbitraje del Centro",
  extraction="Copiar la base invocada.", validation="Obligatorio si MDJ-D16-008 es Verdadero.",
  deps="MDJ-D16-008", **DP | {"origin": "Explícito en documento", "method": "Extracción directa", "prio": "P1", "risk": "R2", "privacy": "Restricción de acceso o derechos"})

F(id="MDJ-D16-010", tech="contiene_nombres_personas_naturales", func="Contiene nombres de personas naturales",
  defn="Indica si el texto contiene nombres de personas naturales que no actúan como autoridad pública.",
  just="Indicador mínimo para aplicar la política de datos personales sin estructurar los nombres.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Verdadero",
  extraction="Detectar nombres propios de personas en roles de parte, testigo, tercero o víctima; no guardar los nombres en este campo.",
  validation="Solo booleano; prohibido almacenar los nombres detectados (minimización).",
  pending="DEC-18", deps="Texto de la manifestación; roles (D13)",
  **DP | {"privacy": "Puede contener datos personales", "review": "No"})

F(id="MDJ-D16-011", tech="tipos_dato_sensible", func="Tipos de datos sensibles presentes",
  defn="Categorías de datos sensibles que aparecen en el texto (salud, menores, violencia, antecedentes penales, origen étnico, orientación sexual, datos biométricos, situación migratoria, identificadores personales…).",
  just="Permite anonimizar, restringir exposición y cumplir reglas judiciales de reserva.",
  dtype="Enum múltiple", card="0..n", values="CAT-515 Tipo de dato sensible", example="[Menores de edad; Salud]",
  extraction="Clasificar el texto por categorías de dato sensible presentes; registrar solo la categoría, nunca el dato.",
  validation="Valores del catálogo; evidencia con la posición, sin copiar el dato.",
  pending="DEC-18", country_status="Pendiente validación nacional",
  deps="Texto de la manifestación", **DP | {"privacy": "Dato personal sensible"})

F(id="MDJ-D16-012", tech="anonimizacion_en_origen", func="Anonimización en origen",
  defn="Si el documento ya llega anonimizado por la fuente, y en qué grado.",
  just="Evita doble tratamiento o, al contrario, exposición de documentos no anonimizados.",
  dtype="Enum", card="1 obligatorio", values="CAT-516 Estado de anonimización", example="Parcialmente anonimizado",
  extraction="Detectar iniciales, supresiones ('XXX', '[…]'), seudónimos.", validation="Valor del catálogo.",
  pending="DEC-18", deps="MDJ-D16-010", **DP | {"privacy": "Puede contener datos personales", "risk": "R2"})

F(id="MDJ-D16-013", tech="tecnica_anonimizacion_origen", func="Técnica de anonimización en origen",
  defn="Técnica usada por la fuente: iniciales, supresión, seudónimo, generalización.",
  just="Evita confundir iniciales con nombres reales en la extracción de partes.",
  dtype="Enum múltiple", card="0..n", values="Iniciales; Supresión; Seudónimo; Generalización; Otra", example="[Iniciales]",
  extraction="Clasificar los patrones de anonimización detectados.", validation="Obligatorio si MDJ-D16-012 indica anonimización.",
  pending="DEC-18", deps="MDJ-D16-012", **DP | {"prio": "P1", "risk": "R3", "privacy": "Puede contener datos personales", "review": "No"})

F(id="MDJ-D16-014", tech="materia_sensible_por_regla", func="Materia sensible por regla",
  defn="Si la obra pertenece a materias que, por regla judicial o legal del país, exigen reserva o anonimización (familia, menores, violencia, delitos sexuales…).",
  just="Algunas reservas dependen de la materia y no de los datos visibles.",
  dtype="Boolean", card="1 obligatorio", values="Verdadero; Falso", example="Verdadero",
  extraction="No se extrae: se calcula con la clasificación (D06), la vía procesal (D14) y reglas por país.",
  validation="Solo con reglas nacionales validadas.", pending="DEC-18", country_status="Pendiente validación nacional",
  deps="Clasificación (D06); vía procesal (D14)",
  **DP | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "prio": "P1", "privacy": "Dato personal sensible", "evidence": "Regla aplicada e insumos"})

F(id="MDJ-D16-015", tech="anonimizacion_requerida", func="Anonimización requerida",
  defn="Si, según la política de Juztina y las reglas del país, el documento debe anonimizarse antes de mostrarse.",
  just="Decisión operativa de privacidad trazable.",
  dtype="Enum", card="1 obligatorio", values="No requerida; Requerida parcial; Requerida total; Pendiente de política", example="Requerida parcial",
  extraction="No se extrae: se calcula con MDJ-D16-010 a 014 y la política (DEC-18).",
  validation="'Pendiente de política' mientras DEC-18 no se resuelva.", pending="DEC-18", country_status="Pendiente validación nacional",
  deps="MDJ-D16-010; MDJ-D16-011; MDJ-D16-012; MDJ-D16-014",
  **DP | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "prio": "P1", "privacy": "Dato personal sensible", "evidence": "Regla de política aplicada"})

F(id="MDJ-D16-016", tech="fecha_verificacion_acceso", func="Fecha de verificación de acceso",
  defn="Fecha de la última verificación del acceso y del enlace a la fuente.",
  just="El acceso y las licencias cambian; los mapas de fuentes de Bolivia ya fechan esta verificación.",
  dtype="Fecha", card="1 obligatorio", values="Fecha ISO 8601", example="2026-09-29",
  extraction="Registrar automáticamente al verificar.", validation="No posterior a la fecha actual.",
  unit="Manifestación", deps="MDJ-D16-001; MDJ-D11-023",
  **{k: v for k, v in DP.items() if k != "unit"} | {"origin": "Generado por sistema", "method": "Generado por sistema", "stage": "Sistema", "prio": "P1", "risk": "R3", "review": "No", "evidence": "No aplica: dato de sistema"})

F(id="MDJ-D16-017", tech="nivel_exposicion_permitido", func="Nivel de exposición permitido",
  defn="Qué puede mostrarse del documento a los usuarios: texto íntegro, texto anonimizado, solo metadatos, ninguno.",
  just="Síntesis aplicable por el producto de derechos y privacidad.",
  dtype="Enum", card="1 obligatorio", values="CAT-517 Nivel de exposición permitido", example="Texto anonimizado",
  extraction="No se extrae: se calcula con MDJ-D16-005, 006, 008 y 015.",
  validation="Debe ser el más restrictivo de los criterios aplicables.", pending="DEC-18; DEC-27",
  deps="MDJ-D16-005; MDJ-D16-006; MDJ-D16-008; MDJ-D16-015",
  **DP | {"origin": "Conclusión jurídica por reglas", "method": "Cálculo", "mode": "B", "stage": "E7", "prio": "P1", "privacy": "Restricción de acceso o derechos", "evidence": "Regla de política aplicada"})

F(id="MDJ-D16-018", tech="nombre_persona_natural_parte", func="Nombre de persona natural (parte, testigo o tercero)",
  defn="Nombre de una persona natural que interviene en el documento sin actuar como autoridad pública.",
  just="Se registra para documentar su exclusión expresa del alcance inicial por minimización.",
  dtype="String", card="0..n", values="No aplica: excluido del alcance inicial", example="No aplica: no se almacena",
  extraction="No extraer en la pasada masiva.", validation="Cualquier valor almacenado es un error de proceso.",
  profiles="JUR; ADM", unit="Afirmación compuesta: parte o actor", pending="DEC-18",
  deps="Política de datos personales (DEC-18)", funcs="No aplica: campo excluido del alcance inicial",
  obs="Excluido (clase X) salvo decisión legal distinta por país; el rol y el tipo de parte sí se extraen (D13).",
  **{k: v for k, v in DP.items() if k not in ("profiles", "unit", "funcs")} | {"origin": "Explícito en documento", "method": "Extracción directa", "prio": "Fuera de alcance", "mode": "X", "stage": "Posterior (C)", "privacy": "Dato personal", "review": "Sí"})

F(id="MDJ-D16-019", tech="restriccion_contractual_fuente", func="Restricción contractual de la fuente",
  defn="Restricciones derivadas de los términos de uso o del contrato con la plataforma de origen (p. ej., bases comerciales).",
  just="Evita incorporar o exponer contenido de terceros sin derecho.",
  dtype="Texto largo", card="0..1 opcional", values="No aplica: texto curado", example="Uso solo para consulta interna; prohibida la redistribución",
  extraction="Curaduría a partir de los términos de la fuente.", validation="Revisión legal de Juztina.",
  unit="Entidad: publicación o fuente", pending="DEC-27", deps="Catálogo de fuentes (D02)",
  **{k: v for k, v in DP.items() if k != "unit"} | {"origin": "Curado por persona", "method": "Revisión humana", "mode": "D", "stage": "Curaduría", "prio": "P1", "risk": "R1", "review": "Sí", "privacy": "Restricción de acceso o derechos"})

# ---------------------------------------------------------------------------------------------
# PRO CAPA DE PROCEDENCIA
# ---------------------------------------------------------------------------------------------
AF = dict(dim="PRO", profiles="UNI", unit="Afirmación", prio="P0", mode="A", stage="Sistema", risk="R3",
          review="No", funcs="F16; F15; F02", origin="Generado por sistema", method="Generado por sistema",
          evidence="No aplica: dato de sistema", cond="Toda afirmación producida por cualquier etapa, perfil o curaduría")

F(id="MDJ-PRO-001", tech="afirmacion_id", func="Identificador de la afirmación",
  defn="Identificador persistente de cada afirmación (valor de un campo sobre una unidad).",
  just="Unidad mínima de trazabilidad y de revocación.", dtype="Identificador", card="1 obligatorio",
  values="No aplica: generado por el sistema", example="AFI-0000000918273", extraction="Asignar al registrar la afirmación.",
  validation="Único; nunca reutilizado.", deps="No aplica: primer dato del registro", **AF)

F(id="MDJ-PRO-002", tech="afirmacion_sujeto", func="Unidad sujeto de la afirmación",
  defn="Unidad de registro (o registro dependiente) de la que se predica el valor.",
  just="Sin sujeto la afirmación no es interpretable.", dtype="Referencia", card="1 obligatorio",
  values="Cualquier unidad de registro o afirmación compuesta", example="U-CO-L1581-ART010",
  extraction="Tomar la unidad procesada por el perfil.", validation="El sujeto debe ser del tipo de unidad declarado para el campo.",
  deps="MDJ-PRO-003", **AF)

F(id="MDJ-PRO-003", tech="afirmacion_campo", func="Campo del diccionario",
  defn="ID del campo del diccionario maestro al que corresponde el valor.",
  just="Vincula cada dato con su definición, reglas y prioridad.", dtype="Referencia", card="1 obligatorio",
  values="ID de campo del diccionario maestro (MDJ-…)", example="MDJ-D03-012",
  extraction="Registrar el ID del campo del perfil.", validation="El ID debe existir y estar activo en la versión de esquema de la ejecución.",
  deps="Diccionario maestro", **AF)

F(id="MDJ-PRO-004", tech="afirmacion_valor", func="Valor de la afirmación",
  defn="Valor asignado al campo, con el tipo de dato del campo.",
  just="Es el dato en sí.", dtype="Objeto", card="1 obligatorio",
  values="Según el tipo de dato del campo", example="{'fecha': '2011-08-20'}",
  extraction="Lo produce el perfil de extracción o la regla de cálculo.", validation="Cumple tipo, cardinalidad y vocabulario del campo.",
  deps="MDJ-PRO-003", **AF | {"origin": "Inferido por modelo", "method": "Extracción directa + Inferencia + Cálculo", "evidence": "Según el campo"})

F(id="MDJ-PRO-005", tech="afirmacion_modo_origen", func="Modo de origen",
  defn="Modo en que se obtuvo el valor: transcrito, normalizado, interpretado, calculado, importado o curado.",
  just="Separa hechos, inferencias y conclusiones (regla de control 1).", dtype="Enum", card="1 obligatorio",
  values="CAT-005 Modo de origen de la afirmación", example="Transcrito",
  extraction="Registrar el modo efectivo; si la verificación literal falla, degradar de transcrito a interpretado.",
  validation="Debe ser compatible con el origen previsto del campo.", deps="MDJ-PRO-024", **AF)

F(id="MDJ-PRO-006", tech="afirmacion_confianza", func="Confianza calculada",
  defn="Confianza de 0 a 1 calculada con señales verificables, no autodeclarada por el modelo.",
  just="Permite aplicar umbrales por clase de riesgo.", dtype="Decimal", card="1 obligatorio",
  values="0.00–1.00 (≤ techo de confianza de la manifestación)", example="0.93",
  extraction="Combinar las señales de MDJ-PRO-007 con la fórmula versionada.", validation="≤ MDJ-D11-019.",
  pending="DEC-20", deps="MDJ-PRO-007; MDJ-D11-019", **AF | {"origin": "Derivado por cálculo", "method": "Cálculo", "stage": "E8", "evidence": "Fórmula de confianza versionada"})

F(id="MDJ-PRO-007", tech="afirmacion_senales_confianza", func="Señales de confianza",
  defn="Señales que alimentaron la confianza: verificación literal, validación por catálogo o formato, acuerdo entre extracciones, calidad del texto, regla determinista.",
  just="Hace auditable la confianza.", dtype="Enum múltiple", card="1..n",
  values="CAT-520 Señal de confianza", example="[Verificación literal; Acuerdo entre extracciones]",
  extraction="Registrar cada control superado o fallido.", validation="Valores del catálogo.", deps="Etapa E8", **AF | {"stage": "E8"})

F(id="MDJ-PRO-008", tech="afirmacion_ejecucion", func="Ejecución que produjo la afirmación",
  defn="Referencia a la ejecución de extracción, cálculo o curaduría.",
  just="Permite invalidar en bloque y reproducir.", dtype="Referencia", card="1 obligatorio",
  values="Ejecución", example="EJE-2027-0042", extraction="Registrar automáticamente.", validation="La ejecución debe existir.",
  deps="MDJ-PRO-030", **AF)

F(id="MDJ-PRO-009", tech="afirmacion_estado_revision", func="Estado de revisión",
  defn="Situación de revisión humana de la afirmación.",
  just="Distingue datos verificados de pendientes.", dtype="Enum", card="1 obligatorio",
  values="CAT-011 Estado de revisión humana", example="Pendiente",
  extraction="Asignar según la clase de riesgo y el umbral; actualizar con cada revisión.",
  validation="Afirmaciones R1 no pueden alimentar cálculos en estado distinto de confirmado o corregido.",
  deps="MDJ-PRO-006; clase de riesgo del campo", **AF)

F(id="MDJ-PRO-010", tech="afirmacion_en_conflicto", func="Afirmación en conflicto",
  defn="Indica que existe otra afirmación incompatible sobre el mismo sujeto y campo.",
  just="Regla de control 8: no elegir en silencio entre fuentes discrepantes.", dtype="Boolean", card="1 obligatorio",
  values="Verdadero; Falso", example="Verdadero", extraction="Detectar al registrar afirmaciones del mismo sujeto y campo.",
  validation="Verdadero exige MDJ-PRO-011 y MDJ-PRO-012.", deps="MDJ-PRO-002; MDJ-PRO-003", **AF | {"stage": "E8", "origin": "Derivado por cálculo", "method": "Cálculo", "evidence": "Regla de detección de conflictos"})

F(id="MDJ-PRO-011", tech="afirmacion_tipo_conflicto", func="Tipo de conflicto",
  defn="Naturaleza del conflicto: oficial frente a calculado, dos extracciones distintas, extracción frente a curaduría, fuentes distintas.",
  just="Orienta la resolución.", dtype="Enum", card="0..1 obligatorio condicionado",
  values="CAT-522 Tipo de conflicto entre afirmaciones", example="Oficial frente a calculado",
  extraction="Clasificar según los modos de origen en conflicto.", validation="Obligatorio si MDJ-PRO-010.",
  deps="MDJ-PRO-010", **AF | {"stage": "E8", "origin": "Derivado por cálculo", "method": "Cálculo", "evidence": "Regla aplicada"})

F(id="MDJ-PRO-012", tech="afirmaciones_en_conflicto", func="Afirmaciones con las que discrepa",
  defn="Referencias a las afirmaciones incompatibles.", just="Permite mostrar ambas versiones.",
  dtype="Array de referencias", card="0..n", values="Afirmación", example="[AFI-0000000918274]",
  extraction="Registrar al detectar el conflicto.", validation="Referencias existentes del mismo sujeto y campo.",
  deps="MDJ-PRO-010", **AF | {"stage": "E8"})

F(id="MDJ-PRO-013", tech="afirmacion_registrada_desde", func="Registrada en el sistema desde",
  defn="Momento desde el cual la afirmación forma parte del estado conocido por Juztina (tiempo de registro).",
  just="Modelo bitemporal: permite responder qué mostraba Juztina en una fecha.", dtype="Datetime", card="1 obligatorio",
  values="Datetime ISO 8601 UTC", example="2027-03-02T14:05:11Z", extraction="Registrar automáticamente.",
  validation="No posterior al momento actual.", deps="MDJ-PRO-001", **AF)

F(id="MDJ-PRO-014", tech="afirmacion_registrada_hasta", func="Registrada en el sistema hasta",
  defn="Momento en que la afirmación fue reemplazada, revocada o invalidada.",
  just="Conserva la historia sin borrar.", dtype="Datetime", card="0..1 opcional",
  values="Datetime ISO 8601 UTC", example="2027-06-10T09:00:00Z", extraction="Registrar al reemplazar o invalidar.",
  validation="Posterior a MDJ-PRO-013.", deps="MDJ-PRO-013", **AF)

F(id="MDJ-PRO-015", tech="afirmacion_insumos", func="Afirmaciones de las que depende",
  defn="Afirmaciones usadas como insumo de un valor calculado o de una conclusión jurídica.",
  just="Permite recalcular cuando cambia un insumo.", dtype="Array de referencias", card="0..n",
  values="Afirmación", example="[AFI-…-501, AFI-…-502]", extraction="Registrar al calcular.",
  validation="Obligatorio para modos calculado y conclusión.", deps="MDJ-PRO-005", **AF | {"stage": "E7"})

F(id="MDJ-PRO-016", tech="afirmacion_regla_aplicada", func="Regla aplicada",
  defn="ID y versión de la regla determinista que produjo un valor calculado o una conclusión jurídica.",
  just="Las conclusiones jurídicas dependen de reglas validadas por país.", dtype="String", card="0..1 obligatorio condicionado",
  values="ID de regla + versión", example="VIG-PE-v1.2", extraction="Registrar al calcular.",
  validation="La regla debe estar en estado validado para el país; si no, no se ejecuta.", pending="DEC-17; DEC-25",
  deps="MDJ-PRO-005", **AF | {"stage": "E7"})

EV = dict(dim="PRO", profiles="UNI", unit="Evidencia", prio="P0", mode="A", stage="E8", risk="R2", review="No",
          funcs="F15; F16; F02", origin="Generado por sistema", method="Generado por sistema",
          evidence="No aplica: la evidencia es el propio registro", cond="Obligatoria para afirmaciones transcritas, normalizadas e interpretadas")

F(id="MDJ-PRO-017", tech="evidencia_id", func="Identificador de la evidencia",
  defn="Identificador de cada ancla de evidencia.", just="Una afirmación puede tener varias evidencias.",
  dtype="Identificador", card="1 obligatorio", values="No aplica: generado por el sistema", example="EVI-00000077123",
  extraction="Asignar al registrar.", validation="Único.", deps="No aplica: primer dato del registro", **EV | {"stage": "Sistema"})

F(id="MDJ-PRO-018", tech="evidencia_afirmacion", func="Afirmación sustentada",
  defn="Afirmación a la que pertenece la evidencia (entidad dependiente).", just="Vincula el dato con su respaldo.",
  dtype="Referencia", card="1 obligatorio", values="Afirmación", example="AFI-0000000918273",
  extraction="Registrar al crear.", validation="La afirmación debe existir.", deps="MDJ-PRO-001", **EV | {"stage": "Sistema"})

F(id="MDJ-PRO-019", tech="evidencia_manifestacion", func="Manifestación de la evidencia",
  defn="Manifestación (archivo concreto) sobre cuyo texto normalizado se anclan las posiciones.",
  just="Las posiciones solo son estables en un archivo concreto.", dtype="Referencia", card="1 obligatorio",
  values="Manifestación", example="MAN-CO-000771", extraction="Registrar al crear.", validation="La manifestación debe existir.",
  deps="MDJ-PRO-028", **EV | {"stage": "Sistema"})

F(id="MDJ-PRO-020", tech="evidencia_posicion_inicio", func="Posición inicial",
  defn="Desplazamiento en caracteres del inicio del tramo sobre el texto normalizado de la manifestación.",
  just="Ancla exacta para verificar y mostrar el tramo.", dtype="Integer", card="1 obligatorio",
  values="Entero ≥ 0", example="12044", extraction="Lo devuelve el perfil o el localizador del tramo.",
  validation="< posición final y dentro del texto.", deps="MDJ-PRO-019; MDJ-PRO-028", **EV | {"stage": "E3", "origin": "Explícito en documento", "method": "Extracción directa"})

F(id="MDJ-PRO-021", tech="evidencia_posicion_fin", func="Posición final",
  defn="Desplazamiento en caracteres del final del tramo.", just="Completa el ancla.",
  dtype="Integer", card="1 obligatorio", values="Entero > posición inicial", example="12131",
  extraction="Igual que MDJ-PRO-020.", validation="> posición inicial.", deps="MDJ-PRO-020",
  **EV | {"stage": "E3", "origin": "Explícito en documento", "method": "Extracción directa"})

F(id="MDJ-PRO-022", tech="evidencia_texto", func="Texto de la evidencia",
  defn="Copia del tramo de texto que sustenta la afirmación.", just="Lectura humana y verificación sin abrir el archivo.",
  dtype="Texto largo", card="1 obligatorio", values="No aplica: literal", example="Modifícase el artículo 22 de la Ley…",
  extraction="Copiar el tramo entre las posiciones.", validation="Igual al substring del texto normalizado.",
  privacy="Puede contener datos personales", deps="MDJ-PRO-020; MDJ-PRO-021",
  **EV | {"stage": "E3", "origin": "Explícito en documento", "method": "Extracción directa"})

F(id="MDJ-PRO-023", tech="evidencia_pagina", func="Página de la evidencia",
  defn="Página o páginas del archivo en que se encuentra el tramo.", just="Facilita la consulta humana del original.",
  dtype="Array", card="0..n", values="Enteros ≥ 1", example="[3]", extraction="Calcular desde las posiciones.",
  validation="Dentro de MDJ-D11-007.", deps="MDJ-PRO-020", **EV | {"mode": "B", "prio": "P1", "risk": "R3", "origin": "Derivado por cálculo", "method": "Cálculo"})

F(id="MDJ-PRO-024", tech="evidencia_verificacion_literal", func="Verificación literal",
  defn="Resultado de comprobar que el texto devuelto por el modelo coincide con el texto del archivo.",
  just="Regla de control 2: sin verificación, un valor transcrito se descarta o degrada.", dtype="Enum", card="1 obligatorio",
  values="CAT-521 Resultado de verificación literal", example="Coincidencia exacta",
  extraction="Comparar el texto de la evidencia con el texto normalizado.", validation="Valor del catálogo.",
  deps="MDJ-PRO-022", **EV | {"risk": "R1", "origin": "Derivado por cálculo", "method": "Cálculo", "evidence": "Regla de comparación versionada"})

F(id="MDJ-PRO-025", tech="evidencia_seccion", func="Sección de la evidencia",
  defn="Unidad estructural o sección funcional en que se ubica el tramo (vistos, antecedentes, fundamentos, parte resolutiva, artículo…).",
  just="Necesaria para las reglas de sección decisiva y de función de referencias.", dtype="Referencia", card="1 obligatorio",
  values="Unidad estructural", example="Fundamentos del problema jurídico 2",
  extraction="Calcular desde la segmentación.", validation="La unidad debe contener las posiciones.",
  deps="Segmentación (D05); MDJ-PRO-020", **EV | {"mode": "B", "origin": "Derivado por cálculo", "method": "Cálculo"})

F(id="MDJ-PRO-026", tech="evidencia_fragmento_proyectado", func="Fragmento textual proyectado",
  defn="Fragmento textual (unidad en una versión) sobre el que se proyecta la evidencia para mostrarla al usuario.",
  just="Permite citar el fragmento vigente o histórico correcto.", dtype="Referencia", card="1 obligatorio",
  values="Fragmento textual", example="F-PE-LEY29783-ART022-v2016",
  extraction="Calcular desde la manifestación y la versión.", validation="El fragmento debe pertenecer a la versión de la manifestación.",
  deps="MDJ-PRO-025; versiones (D03)", **EV | {"mode": "B", "origin": "Derivado por cálculo", "method": "Cálculo"})

F(id="MDJ-PRO-027", tech="evidencia_contenido_ajeno", func="Evidencia en contenido ajeno",
  defn="Indica si el tramo está dentro de una cita textual o transcripción de otro documento.",
  just="Impide que el contenido transcrito se atribuya a la unidad de origen.", dtype="Boolean", card="1 obligatorio",
  values="Verdadero; Falso", example="Falso", extraction="Cruzar posiciones con los límites de citas textuales (D07).",
  validation="Si Verdadero, la afirmación no puede ser de clasificación, efecto ni monto propio.",
  deps="Citas textuales (D07)", **EV | {"mode": "B", "risk": "R1", "origin": "Derivado por cálculo", "method": "Cálculo"})

F(id="MDJ-PRO-028", tech="texto_normalizado_hash", func="Hash del texto normalizado",
  defn="Huella del texto normalizado de la manifestación sobre el que se calculan las posiciones.",
  just="Garantiza que las anclas siguen siendo válidas.", dtype="Hash", card="1 obligatorio",
  values="SHA-256", example="9f2c…e01", extraction="Calcular al normalizar el texto en E0.",
  validation="Si cambia el texto normalizado, las evidencias deben recalcularse.", unit="Manifestación",
  deps="Etapa E0", pending="DEC-24", **{k: v for k, v in EV.items() if k != "unit"} | {"stage": "E0", "risk": "R2"})

F(id="MDJ-PRO-029", tech="tramo_contenido_ajeno", func="Tramo marcado como contenido ajeno",
  defn="Marca sobre un segmento que lo identifica como transcripción o cita textual de otro documento.",
  just="Regla D.1: lo transcrito no se clasifica ni genera efectos de la unidad de origen.", dtype="Boolean", card="1 obligatorio",
  values="Verdadero; Falso", example="Verdadero", unit="Fragmento textual",
  extraction="Se fija a partir de los límites de citas textuales detectados en E4.",
  validation="Debe existir una referencia de tipo cita textual que cubra el tramo.",
  deps="Referencias tipo 5 (D07)", **{k: v for k, v in EV.items() if k != "unit"} | {"stage": "E4", "prio": "P1", "mode": "A", "risk": "R2", "origin": "Inferido por modelo", "method": "Inferencia", "evidence": "Límites de la cita textual"})

EJ = dict(dim="PRO", profiles="UNI", unit="Ejecución", prio="P0", mode="A", stage="Sistema", risk="R3", review="No",
          funcs="F16", origin="Generado por sistema", method="Generado por sistema",
          evidence="No aplica: dato de sistema", cond="Toda ejecución de extracción, cálculo o curaduría masiva")

F(id="MDJ-PRO-030", tech="ejecucion_id", func="Identificador de la ejecución",
  defn="Identificador de cada ejecución de un perfil sobre un lote.", just="Base de auditoría, reproducción e invalidación en bloque.",
  dtype="Identificador", card="1 obligatorio", values="No aplica: generado por el sistema", example="EJE-2027-0042",
  extraction="Asignar al iniciar.", validation="Único.", deps="No aplica: primer dato del registro", **EJ)

F(id="MDJ-PRO-031", tech="ejecucion_etapa", func="Etapa", defn="Etapa del proceso (E0 a E8).",
  just="Ubica la ejecución en el flujo.", dtype="Enum", card="1 obligatorio", values="CAT-008 Etapa de procesamiento", example="E5",
  extraction="Registrar al iniciar.", validation="Valor del catálogo.", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-032", tech="ejecucion_perfil_extraccion", func="Perfil de extracción",
  defn="Perfil de extracción ejecutado (conjunto de campos para un tipo de unidad).", just="Permite saber qué campos se intentaron.",
  dtype="String", card="1 obligatorio", values="ID de perfil de extracción", example="PERF-JUR-PARTE-RESOLUTIVA-v1",
  extraction="Registrar al iniciar.", validation="El perfil debe existir en la versión de esquema.", deps="MDJ-PRO-033", **EJ)

F(id="MDJ-PRO-033", tech="ejecucion_version_esquema", func="Versión del esquema",
  defn="Versión del diccionario maestro usada.", just="Reproducibilidad.", dtype="String", card="1 obligatorio",
  values="Versión semántica", example="1.0.0", extraction="Registrar al iniciar.", validation="Versión publicada.", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-034", tech="ejecucion_version_taxonomia", func="Versión de la taxonomía",
  defn="Versión de la taxonomía jurídica usada.", just="Las asignaciones dependen de la versión.", dtype="String",
  card="0..1 obligatorio condicionado", values="Versión semántica", example="2027.1",
  extraction="Registrar al iniciar.", validation="Obligatoria en etapas que clasifican (E5).", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-035", tech="ejecucion_version_instrucciones", func="Versión de las instrucciones",
  defn="Versión de las instrucciones (prompts y reglas) del perfil.", just="Permite invalidar lo producido por instrucciones defectuosas.",
  dtype="String", card="1 obligatorio", values="ID + versión", example="INS-JUR-RES-v3",
  extraction="Registrar al iniciar.", validation="Congelada durante la ejecución.", deps="MDJ-PRO-032", **EJ)

F(id="MDJ-PRO-036", tech="ejecucion_modelo", func="Modelo usado",
  defn="Identificador y versión del modelo de lenguaje o del motor usado, o 'regla determinista'.",
  just="Reproducibilidad e independencia de proveedor.", dtype="String", card="1 obligatorio",
  values="Identificador de modelo o 'regla determinista'", example="modelo-X-2027-01", extraction="Registrar al iniciar.",
  validation="Congelado durante la ejecución.", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-037", tech="ejecucion_lote", func="Lote", defn="Identificador del lote de documentos procesado.",
  just="Muestreo de control y detención por lote.", dtype="String", card="1 obligatorio", values="ID de lote", example="LOTE-PE-NOR-0007",
  extraction="Registrar al iniciar.", validation="Lote existente.", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-038", tech="ejecucion_inicio", func="Inicio de la ejecución", defn="Fecha y hora de inicio.",
  just="Auditoría y costos.", dtype="Datetime", card="1 obligatorio", values="Datetime ISO 8601 UTC", example="2027-03-02T13:00:00Z",
  extraction="Registrar automáticamente.", validation="Anterior al fin.", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-039", tech="ejecucion_fin", func="Fin de la ejecución", defn="Fecha y hora de término.",
  just="Auditoría y costos.", dtype="Datetime", card="0..1 obligatorio condicionado", values="Datetime ISO 8601 UTC", example="2027-03-02T15:41:00Z",
  extraction="Registrar automáticamente.", validation="Posterior al inicio; obligatorio si la ejecución terminó.", deps="MDJ-PRO-038", **EJ)

F(id="MDJ-PRO-040", tech="ejecucion_estado", func="Estado de la ejecución",
  defn="Situación de la ejecución: en curso, completada, parcial, fallida, detenida por control de calidad, invalidada.",
  just="Distingue ejecuciones válidas de las que deben descartarse.", dtype="Enum", card="1 obligatorio",
  values="En curso; Completada; Parcial; Fallida; Detenida por control; Invalidada", example="Detenida por control",
  extraction="Actualizar automáticamente.", validation="'Invalidada' propaga 'registrada hasta' a sus afirmaciones.", deps="MDJ-PRO-030", **EJ)

F(id="MDJ-PRO-041", tech="ejecucion_motivo_invalidacion", func="Motivo de invalidación o detención",
  defn="Causa por la que una ejecución se detuvo o se invalidó.", just="Trazabilidad de decisiones de calidad.",
  dtype="Texto largo", card="0..1 obligatorio condicionado", values="No aplica: texto libre", example="Precisión de lote 0,82 < meta R2",
  extraction="Registrar al detener o invalidar.", validation="Obligatorio si estado es Detenida o Invalidada.",
  deps="MDJ-PRO-040", **EJ | {"origin": "Curado por persona", "method": "Revisión humana", "review": "Sí", "stage": "E8"})

F(id="MDJ-PRO-042", tech="ejecucion_precision_muestra", func="Precisión de la muestra de control",
  defn="Precisión medida sobre la muestra revisada del lote, por clase de riesgo.", just="Criterio de detención por lote (regla 13).",
  dtype="Objeto", card="0..1 opcional", values="{R1: decimal, R2: decimal, R3: decimal, n: entero}", example="{R1: 0.99, R2: 0.91, R3: 0.84, n: 120}",
  extraction="Calcular con las revisiones de la muestra.", validation="Comparar con metas DEC-20.", pending="DEC-20",
  deps="Revisiones humanas (MDJ-PRO-043…)", **EJ | {"origin": "Derivado por cálculo", "method": "Cálculo", "stage": "E8"})

RV = dict(dim="PRO", profiles="UNI", unit="Afirmación compuesta: revisión humana", prio="P0", mode="A", stage="E8",
          risk="R2", review="Sí", funcs="F16; F08; F06", origin="Curado por persona", method="Revisión humana",
          evidence="No aplica: decisión del revisor registrada", cond="Toda revisión humana de una afirmación (R1 obligatoria; R2 y R3 por muestreo)")

F(id="MDJ-PRO-043", tech="revision_afirmacion", func="Afirmación revisada", defn="Afirmación objeto de la revisión.",
  just="Vincula la decisión humana con el dato.", dtype="Referencia", card="1 obligatorio", values="Afirmación", example="AFI-0000000918273",
  extraction="Registrar al abrir la revisión.", validation="La afirmación debe existir.", deps="MDJ-PRO-001", **RV)

F(id="MDJ-PRO-044", tech="revision_rol_revisor", func="Rol del revisor",
  defn="Rol de quien revisa: especialista jurídico del país, especialista de materia, curador de catálogos, control de calidad.",
  just="Algunas decisiones exigen un rol concreto (p. ej., reglas de país).", dtype="Enum", card="1 obligatorio",
  values="Especialista jurídico de país; Especialista de materia; Curador de catálogos; Control de calidad", example="Especialista jurídico de país",
  extraction="Registrar desde el sistema de revisión.", validation="Rol habilitado para la clase de riesgo del campo.", deps="MDJ-PRO-043", **RV)

F(id="MDJ-PRO-045", tech="revision_revisor", func="Revisor",
  defn="Identificador interno del revisor (seudónimo de usuario interno).", just="Responsabilidad y auditoría.",
  dtype="Identificador", card="1 obligatorio", values="ID interno de usuario", example="REV-0031",
  extraction="Registrar desde el sistema de revisión.", validation="Usuario activo.", privacy="Dato personal",
  deps="MDJ-PRO-043", **{k: v for k, v in RV.items() if k != "privacy"} | {"origin": "Generado por sistema", "method": "Generado por sistema"},
  obs="Dato personal interno de Juztina: se almacena como ID seudónimo, no como nombre.")

F(id="MDJ-PRO-046", tech="revision_fecha", func="Fecha de la revisión", defn="Fecha y hora de la decisión del revisor.",
  just="Auditoría y bitemporalidad.", dtype="Datetime", card="1 obligatorio", values="Datetime ISO 8601 UTC", example="2027-03-05T10:12:00Z",
  extraction="Registrar automáticamente.", validation="Posterior al registro de la afirmación.", deps="MDJ-PRO-043",
  **RV | {"origin": "Generado por sistema", "method": "Generado por sistema"})

F(id="MDJ-PRO-047", tech="revision_decision", func="Decisión de la revisión",
  defn="Resultado: confirmada, corregida, rechazada o escalada.", just="Actualiza el estado de la afirmación.",
  dtype="Enum", card="1 obligatorio", values="CAT-523 Decisión de revisión humana", example="Corregida",
  extraction="Registrar la decisión del revisor.", validation="'Corregida' exige MDJ-PRO-048.", deps="MDJ-PRO-043", **RV)

F(id="MDJ-PRO-048", tech="revision_valor_corregido", func="Valor corregido",
  defn="Valor que el revisor asigna cuando corrige la afirmación; genera una afirmación nueva de modo curado.",
  just="Conserva el valor original y el corregido.", dtype="Objeto", card="0..1 obligatorio condicionado",
  values="Según el tipo de dato del campo", example="{'fecha': '2011-08-21'}",
  extraction="Registrar la corrección.", validation="Cumple el tipo y vocabulario del campo.", deps="MDJ-PRO-047", **RV)

F(id="MDJ-PRO-049", tech="revision_motivo", func="Motivo de la decisión",
  defn="Justificación breve de la decisión del revisor.", just="Retroalimenta instrucciones y reglas.",
  dtype="Texto largo", card="0..1 obligatorio condicionado", values="No aplica: texto libre", example="La cifra corresponde a lo pretendido, no a lo ordenado",
  extraction="Registrar del revisor.", validation="Obligatorio si la decisión es corregida o rechazada.", deps="MDJ-PRO-047", **RV)

# ---------------------------------------------------------------------------------------------
# OPE CAPA OPERATIVA
# ---------------------------------------------------------------------------------------------
EC = dict(dim="OPE", profiles="UNI", unit="Afirmación compuesta: estado de campo", prio="P0", mode="A", stage="Sistema",
          risk="R2", review="No", funcs="F16; F02", origin="Generado por sistema", method="Generado por sistema",
          evidence="No aplica: dato de sistema", cond="Toda combinación unidad × campo aplicable × ejecución")

F(id="MDJ-OPE-001", tech="estado_campo_unidad", func="Unidad del estado de campo", defn="Unidad de registro a la que se refiere el estado.",
  just="El estado se registra por unidad, campo y ejecución.", dtype="Referencia", card="1 obligatorio", values="Cualquier unidad de registro",
  example="O-PE-LEY29783", extraction="Registrar al ejecutar el perfil.", validation="La unidad debe existir.", deps="No aplica: dato del registro", **EC)

F(id="MDJ-OPE-002", tech="estado_campo_campo", func="Campo del estado", defn="ID del campo del diccionario al que se refiere el estado.",
  just="Permite saber qué falta procesar por campo.", dtype="Referencia", card="1 obligatorio", values="ID de campo (MDJ-…)", example="MDJ-D03-015",
  extraction="Registrar al ejecutar el perfil.", validation="Campo existente y aplicable al perfil de la unidad.", deps="Diccionario maestro", **EC)

F(id="MDJ-OPE-003", tech="estado_campo_ejecucion", func="Ejecución del estado", defn="Ejecución que produjo el estado (vacía si 'no procesado').",
  just="Trazabilidad.", dtype="Referencia", card="0..1 obligatorio condicionado", values="Ejecución", example="EJE-2027-0042",
  extraction="Registrar al ejecutar.", validation="Obligatoria salvo en 'no procesado'.", deps="MDJ-PRO-030", **EC)

F(id="MDJ-OPE-004", tech="estado_campo", func="Estado del campo",
  defn="Situación del campo para la unidad: no procesado, no aplicable, procesado con valor, no encontrado, indeterminado, pendiente de revisión, revisado, error de proceso.",
  just="La ausencia de valor nunca significa 'no': hay que leer el estado.", dtype="Enum", card="1 obligatorio",
  values="CAT-006 Estado de campo", example="No encontrado",
  extraction="Asignar al terminar el perfil según el resultado y las condiciones de E.6.",
  validation="'No encontrado' exige completitud 'Completo' y legibilidad ≥ media en la manifestación; si no, 'Indeterminado'.",
  deps="MDJ-D11-005; MDJ-D11-011", **EC | {"risk": "R1", "origin": "Derivado por cálculo", "method": "Cálculo", "evidence": "Regla de asignación de estado"})

F(id="MDJ-OPE-005", tech="estado_campo_motivo_indeterminacion", func="Motivo de indeterminación",
  defn="Causa por la que el campo quedó indeterminado: ilegibilidad, texto incompleto, ambigüedad, varios candidatos, regla nacional no validada, conflicto sin resolver.",
  just="Orienta el reprocesamiento o la revisión.", dtype="Enum", card="0..1 obligatorio condicionado",
  values="CAT-519 Motivo de indeterminación", example="Regla nacional no validada",
  extraction="Registrar junto con el estado.", validation="Obligatorio si el estado es 'Indeterminado'.", deps="MDJ-OPE-004", **EC)

F(id="MDJ-OPE-006", tech="estado_campo_intentos", func="Intentos de procesamiento", defn="Número de veces que se intentó procesar el campo para la unidad.",
  just="Control de reintentos y costos.", dtype="Integer", card="1 obligatorio", values="Entero ≥ 0", example="2",
  extraction="Incrementar en cada intento.", validation="≥ 0.", deps="MDJ-OPE-004", **EC | {"risk": "R3", "prio": "P1"})

F(id="MDJ-OPE-007", tech="estado_campo_fecha", func="Fecha del estado", defn="Momento en que se asignó el estado.",
  just="Historia del procesamiento.", dtype="Datetime", card="1 obligatorio", values="Datetime ISO 8601 UTC", example="2027-03-02T15:41:00Z",
  extraction="Registrar automáticamente.", validation="No futura.", deps="MDJ-OPE-004", **EC | {"risk": "R3"})

OP = dict(dim="OPE", profiles="UNI", unit="Obra", prio="P1", mode="B", stage="E7", risk="R3", review="No",
          funcs="F16; F01", origin="Derivado por cálculo", method="Cálculo", evidence="Regla aplicada",
          cond="Toda obra incorporada")

F(id="MDJ-OPE-008", tech="estado_editorial", func="Estado editorial",
  defn="Situación de la obra en el flujo de Juztina: ingresada, en procesamiento, publicada, retenida por calidad, retenida por privacidad, retirada.",
  just="Controla qué se expone en el producto.", dtype="Enum", card="1 obligatorio", values="CAT-518 Estado editorial", example="Retenida por privacidad",
  extraction="Calcular con calidad (D11), privacidad (D16) y procesamiento; ajustable por curaduría.",
  validation="'Publicada' exige nivel de exposición distinto de 'Ninguno'.", deps="MDJ-D11-024; MDJ-D16-017",
  **OP | {"prio": "P0", "funcs": "F16; F17; F02"})

F(id="MDJ-OPE-009", tech="especialistas_que_incluyen", func="Especialistas que incluyen la unidad",
  defn="Especialistas de Juztina cuya consulta guardada selecciona la obra o alguna de sus unidades.",
  just="Permite auditar la composición de cada especialista sin curaduría manual.", dtype="Array", card="0..n",
  values="IDs de especialistas configurados", example="[ESP-LABORAL; ESP-TRIBUTARIO]",
  extraction="No se extrae: resultado de ejecutar las reglas de especialistas sobre facetas.",
  validation="Recalcular al cambiar reglas o asignaciones.", pending="DEC-12", deps="Clasificación (D06); reglas de especialistas",
  **OP | {"funcs": "F01; F16"})

F(id="MDJ-OPE-010", tech="version_esquema_registro", func="Versión de esquema del registro",
  defn="Versión del diccionario maestro con la que está completo el registro de la obra.", just="Detecta registros desactualizados tras cambios de esquema.",
  dtype="String", card="1 obligatorio", values="Versión semántica", example="1.0.0",
  extraction="Tomar la versión mínima entre las ejecuciones vigentes de la obra.", validation="Versión publicada.",
  deps="MDJ-PRO-033", **OP | {"prio": "P0", "origin": "Generado por sistema", "method": "Generado por sistema", "stage": "Sistema", "evidence": "No aplica: dato de sistema"})

F(id="MDJ-OPE-011", tech="cobertura_procesamiento", func="Cobertura de procesamiento",
  defn="Proporción de campos aplicables de la obra que tienen un estado distinto de 'no procesado'.",
  just="Mide el avance real del enriquecimiento por obra.", dtype="Porcentaje", card="1 obligatorio", values="0–100 %", example="87 %",
  extraction="Calcular con los estados de campo.", validation="0–100.", deps="MDJ-OPE-004", **OP)

F(id="MDJ-OPE-012", tech="prioridad_reprocesamiento", func="Prioridad de reprocesamiento",
  defn="Prioridad para reprocesar la obra según indeterminaciones, calidad, uso y cambios de esquema o taxonomía.",
  just="Orienta el gasto de procesamiento posterior (clase C).", dtype="Enum", card="1 obligatorio", values="Alta; Media; Baja; Ninguna", example="Alta",
  extraction="Calcular con la regla versionada.", validation="Valor del catálogo.", deps="MDJ-OPE-004; MDJ-OPE-013; MDJ-D11-024", **OP | {"prio": "P2"})

F(id="MDJ-OPE-013", tech="senal_uso_consultas", func="Señal de uso: recuperaciones",
  defn="Número de veces que la obra o sus unidades fueron recuperadas por búsquedas o asistentes en un periodo.",
  just="Prioriza revisión y reprocesamiento donde hay más uso.", dtype="Integer", card="1 obligatorio", values="Entero ≥ 0", example="342",
  extraction="Agregar desde los registros de uso del producto (anonimizados).", validation="≥ 0; periodo declarado.",
  deps="Registros de uso del producto", **OP | {"prio": "P3", "origin": "Generado por sistema", "method": "Generado por sistema", "stage": "Sistema", "evidence": "No aplica: dato de sistema", "funcs": "F16"})

F(id="MDJ-OPE-014", tech="senal_uso_citas_asistente", func="Señal de uso: citas del asistente",
  defn="Número de veces que el asistente citó la obra o sus unidades en respuestas en un periodo.",
  just="Identifica las fuentes críticas para la calidad de las respuestas.", dtype="Integer", card="1 obligatorio", values="Entero ≥ 0", example="57",
  extraction="Agregar desde los registros del asistente (sin datos de usuarios).", validation="≥ 0; periodo declarado.",
  deps="Registros del asistente", **OP | {"prio": "P3", "origin": "Generado por sistema", "method": "Generado por sistema", "stage": "Sistema", "evidence": "No aplica: dato de sistema", "funcs": "F16; F15"})

# Ajuste de observaciones por defecto
for _f in FIELDS:
    _f.setdefault("obs", "Sin observaciones adicionales.")

# ---------------------------------------------------------------------------------------------
# CATÁLOGOS (CAT-500..CAT-599)
# ---------------------------------------------------------------------------------------------

def V(code, label, definition, parent="", synonyms="", country="ALL", notes="", status="Propuesto"):
    return dict(code=code, label=label, definition=definition, parent=parent, synonyms=synonyms,
                country=country, notes=notes, status=status)


CATALOGS = [
    dict(cat_id="CAT-501", cat_name="Tipo de efecto jurídico",
         cat_def="Clase de efecto que una unidad establece, según su operador deóntico o función.",
         values=[V("OBL", "Obligación", "Deber de hacer o dar."),
                 V("PRO", "Prohibición", "Deber de abstenerse."),
                 V("PER", "Permiso o facultad", "Autorización para hacer algo sin obligarlo."),
                 V("DER", "Derecho", "Situación jurídica de ventaja exigible por su titular."),
                 V("SAN", "Sanción", "Consecuencia punitiva por una conducta."),
                 V("DEF", "Definición", "Fija el significado de un término para la obra."),
                 V("HAB", "Habilitación o requisito", "Condición para ejercer una actividad (licencia, permiso, registro)."),
                 V("COM", "Atribución de competencia", "Asigna una función o potestad a un órgano."),
                 V("ORD", "Orden", "Mandato concreto de una decisión judicial o administrativa."),
                 V("MCO", "Medida correctiva o cautelar", "Medida para revertir o prevenir un daño o asegurar el resultado."),
                 V("PRC", "Regla de procedimiento", "Establece trámite, plazo o forma de un procedimiento.")]),
    dict(cat_id="CAT-502", cat_name="Alcance subjetivo de efectos",
         cat_def="A quiénes alcanzan los efectos de una decisión. Valores pivote; su aplicación concreta depende de reglas nacionales (DEC-25).",
         values=[V("IPA", "Inter partes", "Solo vincula a las partes del proceso."),
                 V("EOM", "Erga omnes", "Efecto general frente a todos."),
                 V("IPR", "Inter pares", "Se extiende a casos análogos entre sujetos en igual situación.", notes="Figura documentada en la jurisprudencia constitucional de algunos países; validar por país.", status="Pendiente validación nacional"),
                 V("ICO", "Inter comunis", "Se extiende a una comunidad de afectados no demandantes.", notes="Validar por país.", status="Pendiente validación nacional"),
                 V("GEN", "General normativo", "Efecto propio de un acto de alcance general."),
                 V("IND", "Indeterminado", "No determinable con la información disponible.")]),
    dict(cat_id="CAT-503", cat_name="Ámbito temporal de aplicación",
         cat_def="Modalidad temporal de aplicación declarada en el texto.",
         values=[V("INM", "Inmediata", "Se aplica desde la entrada en vigor a hechos y situaciones en curso."),
                 V("DIF", "Diferida", "Se aplica desde una fecha o condición posterior a la entrada en vigor."),
                 V("RET", "Retroactiva", "Se aplica a hechos anteriores a su vigencia."),
                 V("ULT", "Ultraactiva", "La norma anterior sigue aplicándose a ciertos casos."),
                 V("CON", "Condicionada", "Depende de un acto o hecho futuro (p. ej., reglamentación).")]),
    dict(cat_id="CAT-504", cat_name="Tipo de destinatario (pivote)",
         cat_def="Categorías pivote de sujetos destinatarios, obligados o beneficiarios. Las denominaciones nacionales se conservan en campos literales.",
         values=[V("PNA", "Persona natural", "Cualquier persona natural sin calificación específica."),
                 V("PJU", "Persona jurídica de derecho privado", "Sociedades, asociaciones, fundaciones."),
                 V("EMP", "Empleador", "Sujeto que contrata trabajadores.", parent="PJU"),
                 V("TRA", "Trabajador", "Persona que presta servicios subordinados.", parent="PNA"),
                 V("CON", "Consumidor o usuario", "Destinatario final de bienes o servicios."),
                 V("PRV", "Proveedor", "Quien ofrece bienes o servicios en el mercado."),
                 V("CTB", "Contribuyente o responsable tributario", "Sujeto pasivo de obligaciones tributarias."),
                 V("ENP", "Entidad pública", "Órgano u organismo del Estado."),
                 V("FUN", "Funcionario o servidor público", "Persona al servicio del Estado."),
                 V("CNC", "Concesionario o titular de título habilitante", "Titular de concesión, licencia o autorización."),
                 V("REG", "Empresa regulada", "Sujeto bajo supervisión de un regulador sectorial."),
                 V("NNA", "Niñas, niños y adolescentes", "Personas menores de edad."),
                 V("PIN", "Pueblos indígenas", "Pueblos y comunidades indígenas u originarios."),
                 V("MYP", "Micro y pequeña empresa", "Empresas calificadas como micro o pequeñas por la ley nacional.", notes="Los umbrales varían por país."),
                 V("OTR", "Otro", "Destinatario no comprendido; usar con literal obligatorio.")]),
    dict(cat_id="CAT-505", cat_name="Concepto económico",
         cat_def="Concepto al que responde un monto.",
         values=[V("MUA", "Multa administrativa", "Sanción pecuniaria impuesta por la Administración."),
                 V("MUP", "Multa penal o judicial", "Sanción pecuniaria impuesta por un juez."),
                 V("IND", "Indemnización o reparación", "Compensación por daños."),
                 V("REM", "Remuneración o beneficio laboral", "Pagos derivados de la relación de trabajo."),
                 V("TRI", "Tributo", "Impuesto, contribución o tasa."),
                 V("INT", "Intereses", "Intereses legales, moratorios o compensatorios."),
                 V("COS", "Costas y costos", "Gastos del proceso y honorarios."),
                 V("GAR", "Garantía o fianza", "Monto para asegurar una obligación."),
                 V("DEU", "Deuda o capital", "Monto principal adeudado."),
                 V("PRE", "Precio o contraprestación", "Precio de un contrato o retribución."),
                 V("TOP", "Tope o límite regulatorio", "Valor máximo o mínimo fijado por una norma."),
                 V("UMB", "Umbral de aplicación", "Valor que activa o excluye la aplicación de una regla."),
                 V("TAS", "Tasa o porcentaje", "Proporción aplicable a una base."),
                 V("PRS", "Presupuesto o asignación pública", "Montos presupuestarios."),
                 V("OTR", "Otro", "Concepto no comprendido.")]),
    dict(cat_id="CAT-506", cat_name="Naturaleza del importe",
         cat_def="Grado de determinación del importe.",
         values=[V("FIJ", "Fijo", "Importe determinado."),
                 V("MAX", "Máximo", "Importe tope ('hasta')."),
                 V("MIN", "Mínimo", "Importe mínimo ('no menor de')."),
                 V("RAN", "Rango", "Entre un mínimo y un máximo."),
                 V("POR", "Porcentaje sobre base", "Proporción de una magnitud."),
                 V("EST", "Estimado", "Importe aproximado o referencial."),
                 V("LIQ", "Por liquidar", "Se determinará posteriormente.")]),
    dict(cat_id="CAT-507", cat_name="Rol del monto",
         cat_def="Papel del monto en el documento.",
         values=[V("PRT", "Pretendido", "Solicitado por una parte."),
                 V("PRP", "Propuesto", "Propuesto por un órgano instructor o perito."),
                 V("ORD", "Ordenado o impuesto", "Ordenado por la decisión."),
                 V("CNF", "Confirmado", "Confirmado por una instancia superior."),
                 V("RED", "Reducido", "Disminuido por una instancia superior."),
                 V("INC", "Incrementado", "Aumentado por una instancia superior."),
                 V("REV", "Revocado o dejado sin efecto", "Eliminado por una decisión posterior."),
                 V("NOR", "Normativo", "Fijado por una norma (tope, escala, tributo)."),
                 V("PAG", "Pagado o consignado", "Pago acreditado en el expediente.")]),
    dict(cat_id="CAT-508", cat_name="Unidad de valor por país (semilla)",
         cat_def="Unidades de valor legal usadas para expresar montos. Semilla ilustrativa: requiere validación nacional y carga de series (DEC-29).",
         values=[V("UIT", "Unidad Impositiva Tributaria", "Unidad de referencia tributaria y sancionadora.", country="PE", status="Pendiente validación nacional"),
                 V("UVT", "Unidad de Valor Tributario", "Unidad de referencia tributaria.", country="CO", status="Pendiente validación nacional"),
                 V("SMMLV", "Salario mínimo mensual legal vigente", "Referencia para multas y cuantías.", country="CO", status="Pendiente validación nacional"),
                 V("UF", "Unidad de Fomento", "Unidad reajustable diaria.", country="CL", status="Pendiente validación nacional"),
                 V("UTM", "Unidad Tributaria Mensual", "Unidad de referencia tributaria y sancionadora mensual.", country="CL", status="Pendiente validación nacional"),
                 V("UMA", "Unidad de Medida y Actualización", "Referencia para obligaciones y multas.", country="MX", status="Pendiente validación nacional"),
                 V("SBU", "Salario básico unificado", "Referencia para multas y cuantías.", country="EC", status="Pendiente validación nacional"),
                 V("SMN", "Salario mínimo nacional", "Referencia para cuantías.", country="BO", status="Pendiente validación nacional"),
                 V("SMVM", "Salario mínimo, vital y móvil", "Referencia para cuantías.", country="AR", status="Pendiente validación nacional"),
                 V("UFV", "Unidad de Fomento de Vivienda", "Unidad reajustable.", country="BO", status="Pendiente validación nacional")]),
    dict(cat_id="CAT-509", cat_name="Unidad de medida física",
         cat_def="Unidades físicas para valores cuantitativos no monetarios.",
         values=[V("HA", "Hectáreas", "Superficie."), V("M2", "Metros cuadrados", "Superficie."),
                 V("TM", "Toneladas métricas", "Masa."), V("KG", "Kilogramos", "Masa."),
                 V("M3", "Metros cúbicos", "Volumen."), V("L", "Litros", "Volumen."),
                 V("KWH", "Kilovatios hora", "Energía."), V("MGL", "Miligramos por litro", "Concentración."),
                 V("DBA", "Decibeles A", "Nivel de ruido."), V("UND", "Unidades", "Conteo de elementos."),
                 V("OTR", "Otra", "Unidad no comprendida; registrar literal.")]),
    dict(cat_id="CAT-510", cat_name="Nivel de calidad",
         cat_def="Escala ordinal común para calidad de texto, segmentación y manifestación. Umbrales calibrados en el piloto.",
         values=[V("ALT", "Alta", "Apta para todos los perfiles."),
                 V("MED", "Media", "Apta con techo de confianza reducido."),
                 V("BAJ", "Baja", "Solo perfiles P0; resto indeterminado."),
                 V("INU", "Inutilizable", "Requiere reprocesamiento o nueva captura.")]),
    dict(cat_id="CAT-511", cat_name="Tipo de incidencia de calidad",
         cat_def="Problemas detectados en la manifestación.",
         values=[V("COL", "Columnas mezcladas", "Texto de varias columnas leído en orden erróneo."),
                 V("SEL", "Sellos o firmas sobre texto", "Elementos gráficos que ocultan texto."),
                 V("ROT", "Páginas rotadas", "Orientación incorrecta."),
                 V("AGU", "Marca de agua", "Marca que interfiere con la lectura."),
                 V("COR", "Texto cortado", "Texto truncado en márgenes."),
                 V("MIX", "Idioma mixto", "Varios idiomas sin marcar."),
                 V("TAB", "Tabla degradada", "Estructura tabular perdida."),
                 V("ENC", "Codificación de caracteres", "Caracteres corruptos o mal codificados."),
                 V("MAN", "Manuscrito", "Texto o anotaciones manuscritas."),
                 V("DUP", "Páginas duplicadas", "Páginas repetidas en el archivo.")]),
    dict(cat_id="CAT-512", cat_name="Confiabilidad de la fuente",
         cat_def="Grado de autoridad de la fuente de una manifestación.",
         values=[V("OFA", "Oficial auténtica", "Edición oficial con valor legal declarado (p. ej., diario oficial)."),
                 V("OFI", "Oficial informativa", "Sitio oficial sin valor legal declarado del texto."),
                 V("INS", "Institucional secundaria", "Institución pública o académica que reproduce el texto."),
                 V("EDI", "Editorial o comercial", "Plataforma o editorial privada."),
                 V("DES", "Desconocida", "Origen no determinado.")]),
    dict(cat_id="CAT-513", cat_name="Acceso",
         cat_def="Régimen de acceso al documento en su fuente (alineado con los mapas de fuentes de Bolivia).",
         values=[V("ABI", "Abierto", "Acceso libre sin registro."),
                 V("REG", "Con registro", "Acceso gratuito con registro."),
                 V("PAG", "Restringido (pago)", "Acceso por suscripción o pago."),
                 V("RES", "Restringido", "Acceso limitado a ciertos usuarios."),
                 V("CNF", "Confidencial o no publicado", "No disponible públicamente.")]),
    dict(cat_id="CAT-514", cat_name="Licencia o régimen de reutilización",
         cat_def="Régimen jurídico de reutilización del texto. El régimen de los textos oficiales por país requiere validación (DEC-27).",
         values=[V("OFL", "Texto oficial de libre reproducción", "Régimen legal nacional que excluye o libera los textos oficiales.", status="Pendiente validación nacional"),
                 V("CCBY", "Creative Commons BY", "Uso con atribución."),
                 V("CCBYNC", "Creative Commons BY-NC", "Uso no comercial con atribución."),
                 V("CCBYNCND", "Creative Commons BY-NC-ND", "Uso no comercial sin obras derivadas."),
                 V("CCOTR", "Otra licencia Creative Commons", "Registrar variante en observaciones."),
                 V("TDR", "Todos los derechos reservados", "Sin licencia de reutilización."),
                 V("TER", "Términos de plataforma", "Rige el contrato o los términos de uso de la fuente."),
                 V("DES", "Desconocida", "Sin evidencia de régimen; no presumir libre uso.")]),
    dict(cat_id="CAT-515", cat_name="Tipo de dato sensible",
         cat_def="Categorías de datos sensibles o especialmente protegidos detectables en el texto. Su tratamiento depende de la política por país (DEC-18).",
         values=[V("SAL", "Salud", "Datos de salud física o mental."),
                 V("MEN", "Menores de edad", "Datos que identifican o conciernen a menores."),
                 V("VIO", "Violencia de género o familiar", "Datos de víctimas o hechos de violencia."),
                 V("SEX", "Vida u orientación sexual", "Datos sobre vida u orientación sexual."),
                 V("PEN", "Antecedentes penales o infracciones", "Datos sobre delitos o sanciones de personas naturales."),
                 V("ETN", "Origen étnico o racial", "Datos de pertenencia étnica."),
                 V("REL", "Creencias religiosas o filosóficas", "Datos de convicciones."),
                 V("POL", "Opiniones políticas o afiliación sindical", "Datos de afiliación."),
                 V("BIO", "Datos biométricos o genéticos", "Datos biométricos o genéticos."),
                 V("MIG", "Situación migratoria", "Datos de estatus migratorio."),
                 V("FIN", "Datos financieros personales", "Ingresos, cuentas o deudas de personas naturales."),
                 V("IDP", "Identificadores personales", "Documentos de identidad, direcciones, teléfonos.")]),
    dict(cat_id="CAT-516", cat_name="Estado de anonimización",
         cat_def="Grado de anonimización con que el documento llega de la fuente.",
         values=[V("NOA", "No anonimizado", "Contiene datos identificativos visibles."),
                 V("PAR", "Parcialmente anonimizado", "Algunos datos suprimidos o reemplazados."),
                 V("TOT", "Anonimizado", "Sin datos identificativos de personas naturales."),
                 V("NAP", "No aplica", "No contiene datos de personas naturales."),
                 V("IND", "Indeterminado", "No determinable por calidad del texto.")]),
    dict(cat_id="CAT-517", cat_name="Nivel de exposición permitido",
         cat_def="Qué puede mostrarse del documento en el producto.",
         values=[V("INT", "Texto íntegro", "Puede mostrarse el texto completo."),
                 V("ANO", "Texto anonimizado", "Solo tras anonimización."),
                 V("CIT", "Citas breves", "Solo fragmentos breves con atribución."),
                 V("MET", "Solo metadatos", "Solo ficha descriptiva y referencia."),
                 V("NIN", "Ninguno", "No se expone.")]),
    dict(cat_id="CAT-518", cat_name="Estado editorial",
         cat_def="Situación de una obra en el flujo de Juztina.",
         values=[V("ING", "Ingresada", "Incorporada, sin procesar."),
                 V("PRO", "En procesamiento", "En alguna etapa E0–E8."),
                 V("PUB", "Publicada", "Disponible en el producto."),
                 V("RCA", "Retenida por calidad", "No se expone por calidad insuficiente."),
                 V("RPR", "Retenida por privacidad o derechos", "No se expone hasta resolver privacidad o derechos."),
                 V("RET", "Retirada", "Excluida del producto, conservada en el archivo.")]),
    dict(cat_id="CAT-519", cat_name="Motivo de indeterminación",
         cat_def="Causa por la que un campo quedó en estado indeterminado.",
         values=[V("ILE", "Ilegibilidad", "Calidad de texto insuficiente."),
                 V("INC", "Texto incompleto", "Falta la parte del documento que contendría el dato."),
                 V("AMB", "Ambigüedad del texto", "El texto admite más de una lectura."),
                 V("CAN", "Varios candidatos", "Más de un valor posible sin criterio de elección."),
                 V("RNV", "Regla nacional no validada", "La conclusión requiere una regla de país aún no validada."),
                 V("CNF", "Conflicto sin resolver", "Afirmaciones incompatibles pendientes."),
                 V("DEP", "Dependencia no disponible", "Falta un insumo (catálogo, referencia, serie).")]),
    dict(cat_id="CAT-520", cat_name="Señal de confianza",
         cat_def="Controles que alimentan la confianza calculada de una afirmación.",
         values=[V("VLI", "Verificación literal", "La evidencia coincide con el texto del archivo."),
                 V("VCA", "Validación por catálogo", "El valor existe en el vocabulario controlado."),
                 V("VFO", "Validación de formato", "El valor cumple el formato esperado (fecha, número, identificador)."),
                 V("ACU", "Acuerdo entre extracciones", "Dos extracciones independientes coinciden."),
                 V("CAL", "Calidad del texto", "Ajuste por techo de confianza de la manifestación."),
                 V("RDE", "Regla determinista", "Valor producido por regla validada."),
                 V("COH", "Coherencia con otros campos", "Consistencia con fechas, partes u otros valores.")]),
    dict(cat_id="CAT-521", cat_name="Resultado de verificación literal",
         cat_def="Resultado de comparar la evidencia devuelta con el texto del archivo.",
         values=[V("EXA", "Coincidencia exacta", "Igual carácter a carácter."),
                 V("NOR", "Coincidencia normalizada", "Igual tras normalizar espacios, guiones o mayúsculas."),
                 V("PAR", "Coincidencia parcial", "Coincide en parte; el valor se degrada a interpretado."),
                 V("SIN", "Sin coincidencia", "No se encontró; el valor se descarta.")]),
    dict(cat_id="CAT-522", cat_name="Tipo de conflicto entre afirmaciones",
         cat_def="Naturaleza de la discrepancia entre afirmaciones del mismo sujeto y campo.",
         values=[V("OFC", "Oficial frente a calculado", "Una fuente oficial importada discrepa de un cálculo de Juztina."),
                 V("EXT", "Entre extracciones", "Dos extracciones del modelo discrepan."),
                 V("EXC", "Extracción frente a curaduría", "El valor extraído discrepa del curado."),
                 V("FUE", "Entre fuentes", "Dos manifestaciones de distinta fuente discrepan."),
                 V("VER", "Entre versiones de regla", "Dos versiones de una regla producen valores distintos.")]),
    dict(cat_id="CAT-523", cat_name="Decisión de revisión humana",
         cat_def="Resultado de una revisión humana.",
         values=[V("CNF", "Confirmada", "El valor es correcto."),
                 V("COR", "Corregida", "El valor se reemplaza por uno curado."),
                 V("REC", "Rechazada", "El valor se descarta sin reemplazo."),
                 V("ESC", "Escalada", "Requiere otro rol revisor (p. ej., especialista de país).")]),
    dict(cat_id="CAT-529", cat_name="Sección obligatoria por tipo documental",
         cat_def="Secciones cuya presencia se exige para considerar completo un documento según su naturaleza. La lista exigida por tipo y país requiere validación (DEC-08).",
         values=[V("ENC", "Encabezado o identificación", "Identificación del órgano, número y fecha."),
                 V("VIS", "Vistos o base legal", "Normas y antecedentes invocados."),
                 V("CON", "Considerandos o parte considerativa", "Motivación del acto."),
                 V("ANT", "Antecedentes o hechos", "Relato de hechos del caso."),
                 V("FUN", "Fundamentos jurídicos", "Razonamiento jurídico."),
                 V("RES", "Parte resolutiva o decisión", "Decisión o mandato."),
                 V("ART", "Articulado", "Cuerpo dispositivo numerado de una norma."),
                 V("FPR", "Fórmula de promulgación o publicación", "Fórmula de promulgación, refrendo o publicación."),
                 V("FIR", "Firmas", "Firmas de autoridades o magistrados."),
                 V("BIB", "Bibliografía", "Referencias bibliográficas de doctrina.")]),
    dict(cat_id="CAT-530", cat_name="Unidad de plazo",
         cat_def="Unidades para expresar plazos.",
         values=[V("DH", "Días hábiles", "Días laborables según el régimen aplicable."),
                 V("DC", "Días calendario", "Días naturales."),
                 V("DSC", "Días (sin calificar)", "El texto dice 'días' sin precisar; no se presume el tipo."),
                 V("SEM", "Semanas", "Semanas."), V("MES", "Meses", "Meses."), V("ANO", "Años", "Años."),
                 V("HOR", "Horas", "Horas.")]),
    dict(cat_id="CAT-531", cat_name="Periodicidad",
         cat_def="Periodicidad de un monto.",
         values=[V("UNI", "Único", "Se paga una vez."), V("DIA", "Diario", "Por día."),
                 V("MEN", "Mensual", "Por mes."), V("ANU", "Anual", "Por año."),
                 V("EVE", "Por evento", "Por cada ocurrencia (reincidencia, unidad vendida)."),
                 V("OTR", "Otra", "Otra periodicidad; registrar literal.")]),
]
