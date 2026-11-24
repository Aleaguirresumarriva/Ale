"""
Campos del grupo 3: D06 Clasificación jurídica, D10 Información sectorial, D17 Autoridad y fuerza jurídica.
Fuente: arquitectura de metadatos jurídicos de Juztina, versión 3 (secciones A.4, C, D.4 y validación transversal).
Catálogos propios: CAT-300..CAT-399.
"""

_DEF = dict(
    profiles="UNI",
    countries="ALL",
    country_status="Común",
    pending="No",
    privacy="Ninguna",
    review="No",
    obs="Sin observaciones adicionales.",
)

FIELDS = []


def F(**kw):
    d = dict(_DEF)
    d.update(kw)
    if "applicability" not in d:
        d["applicability"] = "Todos los perfiles documentales y los siete países."
    FIELDS.append(d)


# Valores reutilizados
ASIG = "Afirmación compuesta: asignación de clasificación"
CONC = "Entidad: concepto de taxonomía"
EV_CLASIF = ("Una o más anclas de evidencia en la unidad clasificada; en JUR y ADM contenciosos, al menos una "
             "en fundamentos del problema resuelto o en la parte resolutiva.")
NA_SIS = "No aplica: valor generado por el sistema, sin evidencia textual."
NA_CALC = "No aplica: valor calculado; hereda la evidencia de sus insumos."

# ---------------------------------------------------------------------------
# D06 · Asignación de clasificación (registro compuesto)
# ---------------------------------------------------------------------------
F(id="MDJ-D06-001", tech="id_asignacion_clasificacion", func="Identificador de la asignación de clasificación",
  dim="D06", unit=ASIG,
  defn="Identificador persistente y opaco de cada asignación de un concepto de la taxonomía a una unidad de registro.",
  just="Permite auditar, revisar, remapear o revocar cada clasificación de forma individual.",
  dtype="Identificador", card="1 obligatorio", values="No aplica: identificador opaco generado por el sistema.",
  example="ASG-7f3c2a91", origin="Generado por sistema", method="Generado por sistema", evidence=NA_SIS,
  extraction="Se genera al registrar la asignación en la etapa E5 o al calcularla en E7.",
  validation="Único en todo el repositorio; nunca se reutiliza aunque la asignación se revoque.",
  prio="P1", mode="A", stage="Sistema", risk="R3", deps="No aplica: no depende de otros campos.",
  funcs="F16; F18")

F(id="MDJ-D06-002", tech="asignacion_unidad_sujeto", func="Unidad clasificada",
  dim="D06", unit=ASIG,
  defn="Unidad de registro a la que se asigna el concepto: unidad estructural por defecto u obra cuando la asignación es agregada.",
  just="La arquitectura clasifica en la unidad mínima donde la materia puede diferir; sin este vínculo la clasificación vuelve al documento completo.",
  dtype="Referencia", card="1 obligatorio", values="Referencia a una unidad estructural u obra existente.",
  example="UE-LEY29783-000231 (art. 22)", origin="Generado por sistema", method="Generado por sistema",
  evidence=NA_SIS,
  extraction="Se fija con la unidad que el perfil de clasificación procesa (E5) o con la obra en la agregación (E7).",
  validation="La unidad referida existe y su nivel estructural es clasificable según los criterios de granularidad (E.3).",
  prio="P1", mode="A", stage="E5", risk="R3", deps="Identificación de unidades estructurales (D5); id_asignacion_clasificacion.",
  funcs="F01; F03; F04")

F(id="MDJ-D06-003", tech="asignacion_faceta", func="Faceta de la asignación",
  dim="D06", unit=ASIG,
  defn="Faceta taxonómica (F1 a F11) a la que pertenece el concepto asignado.",
  just="Las facetas son independientes; mezclar rama, sector, sujeto o vía procesal en una sola lista genera sobreclasificación.",
  dtype="Enum", card="1 obligatorio", values="CAT-301 Facetas de la taxonomía jurídica.",
  example="F2", origin="Normalizado por regla", method="Normalización",
  evidence="No aplica: se deriva del concepto asignado (concepto_faceta).",
  extraction="Se copia de la faceta del concepto asignado; no la propone el modelo.",
  validation="Coincide con concepto_faceta del concepto referido en la versión de taxonomía indicada.",
  prio="P1", mode="A", stage="E5", risk="R3", deps="asignacion_concepto_id; concepto_faceta.",
  funcs="F01; F03; F18")

F(id="MDJ-D06-004", tech="asignacion_concepto_id", func="Concepto asignado",
  dim="D06", unit=ASIG,
  defn="Identificador persistente del concepto de la taxonomía asignado a la unidad.",
  just="Es el valor de la clasificación; usar identificadores y no etiquetas permite renombrar conceptos sin perder asignaciones.",
  dtype="Referencia", card="1 obligatorio", values="Referencia a un concepto activo de la taxonomía (Entidad: concepto de taxonomía).",
  example="CON-LAB-000148 (Despido nulo o discriminatorio)", origin="Inferido por modelo", method="Clasificación",
  evidence=EV_CLASIF,
  extraction=("El perfil de clasificación lee la unidad y propone conceptos del nivel más específico aplicable, "
              "solo si superan las pruebas de objeto, supresión o consulta; no asigna a la vez un concepto y su ancestro."),
  validation="Concepto en estado activo en la versión indicada; no coexiste con un ancestro en la misma unidad; tiene evidencia verificada.",
  prio="P1", mode="A", review="Condicionado", stage="E5", risk="R2",
  deps="asignacion_unidad_sujeto; asignacion_version_taxonomia; segmentación (D5).",
  funcs="F01; F02; F03; F04; F09; F10",
  obs="Revisión humana cuando la precisión del nodo en el piloto no alcanza la meta R2 (DEC-20).",
  pending="DEC-20")

F(id="MDJ-D06-005", tech="asignacion_version_taxonomia", func="Versión de taxonomía de la asignación",
  dim="D06", unit=ASIG,
  defn="Versión publicada de la taxonomía vigente cuando se hizo la asignación.",
  just="Permite remapear asignaciones tras fusiones o divisiones de conceptos y reconstruir qué se clasificó con qué reglas.",
  dtype="String", card="1 obligatorio", values="Identificador de versión de taxonomía publicado (formato AAAA.MM.n).",
  example="2027.01.0", origin="Generado por sistema", method="Generado por sistema", evidence=NA_SIS,
  extraction="Se toma de la configuración de la ejecución que produce la asignación.",
  validation="Corresponde a una versión publicada; coincide con la versión registrada en la ejecución.",
  prio="P1", mode="A", stage="Sistema", risk="R3", deps="Ejecución de extracción (capa de procedencia).",
  funcs="F16; F18")

F(id="MDJ-D06-006", tech="asignacion_nivel_relevancia", func="Nivel de relevancia temática",
  dim="D06", unit=ASIG,
  defn="Grado en que el concepto es objeto de la unidad: principal, secundaria o contexto. La mera mención no es asignación: se registra como referencia (D7).",
  just="Los especialistas consumen principal y secundaria; el contexto sirve a búsqueda y análisis sectorial sin contaminar los especialistas.",
  dtype="Enum", card="1 obligatorio", values="CAT-302 Nivel de relevancia temática.",
  example="principal", origin="Inferido por modelo", method="Clasificación",
  evidence=EV_CLASIF,
  extraction=("Principal: el concepto es objeto directo de la función de la unidad y supera objeto, supresión y consulta. "
              "Secundaria: es regulado o resuelto de modo instrumental (supera objeto, no supresión). "
              "Contexto: describe hechos, sujetos o actividad sin que ninguna regla o decisión dependa de él. "
              "No hay límite numérico de principales."),
  validation=("Principal y secundaria exigen asignacion_pruebas_superadas coherente y evidencia en sección decisiva cuando el perfil la exige; "
              "dos principales no pueden apoyarse en la misma oración salvo que esta regule ambos objetos."),
  prio="P1", mode="A", review="Condicionado", stage="E5", risk="R2",
  deps="asignacion_concepto_id; asignacion_pruebas_superadas; asignacion_seccion_evidencia.",
  funcs="F01; F02; F03; F04",
  obs="Sustituye el límite de dos principales de la revisión 2. Unidades con exceso de principales van a muestra por alerta estadística (MDJ-D06-019).")

F(id="MDJ-D06-007", tech="asignacion_funcion_juridica", func="Función jurídica respecto del concepto",
  dim="D06", unit=ASIG,
  defn="Qué hace la unidad con el concepto asignado: lo regula, define, sanciona, decide, interpreta, analiza o lo trata procesalmente.",
  just="Registra el fundamento funcional de la clasificación y distingue pertinencia real de mera aparición del término.",
  dtype="Enum", card="1 obligatorio", values="CAT-303 Función jurídica de la asignación.",
  example="decide", origin="Inferido por modelo", method="Clasificación",
  evidence=EV_CLASIF,
  extraction="Se elige la función que la evidencia muestra; si solo aparece citado o transcrito, no se registra asignación.",
  validation="Compatible con el perfil: 'decide' solo en JUR y ADM; 'regula' y 'define' en NOR y ADM general; 'analiza' en DOC.",
  prio="P1", mode="A", stage="E5", risk="R2", deps="asignacion_concepto_id; naturaleza jurídica (D4).",
  funcs="F01; F04; F07")

F(id="MDJ-D06-008", tech="asignacion_evidencias", func="Evidencias de la asignación",
  dim="D06", unit=ASIG,
  defn="Anclas a los tramos de texto que sustentan la asignación.",
  just="Ninguna clasificación sin evidencia: permite verificarla, mostrarla al usuario y auditarla.",
  dtype="Array de referencias", card="1..n", values="Referencias a registros de evidencia (capa de procedencia).",
  example="[EVD-01a2 (fundamento 7, car. 1204–1311)]", origin="Explícito en documento", method="Extracción directa",
  evidence="El propio tramo citado, con verificación literal contra el texto normalizado de la manifestación.",
  extraction="El perfil de clasificación devuelve los tramos literales que motivan la asignación; el sistema los convierte en anclas.",
  validation="Cada tramo coincide literalmente con el texto de la manifestación; ningún tramo está marcado como contenido ajeno (transcripción).",
  prio="P1", mode="A", stage="E5", risk="R2", deps="Segmentación y anclas (D5); marca de contenido ajeno (D7).",
  funcs="F15; F16")

F(id="MDJ-D06-009", tech="asignacion_seccion_evidencia", func="Sección funcional de la evidencia",
  dim="D06", unit=ASIG,
  defn="Sección funcional donde se ubica cada evidencia (vistos, antecedentes, alegaciones, fundamentos, parte resolutiva, voto, cuerpo de artículo, nota).",
  just="Aplica el control de 'evidencia en sección decisiva' que separa la pertinencia temática de la mención contextual.",
  dtype="Enum múltiple", card="1..n", values="Catálogo de secciones funcionales de la dimensión D5.",
  example="[fundamentos_problema, parte_resolutiva]", origin="Derivado por cálculo", method="Cálculo",
  evidence=NA_CALC,
  extraction="Se calcula proyectando cada ancla sobre la segmentación funcional de la unidad.",
  validation="Una entrada por evidencia; valores del catálogo de secciones funcionales.",
  prio="P1", mode="A", stage="E5", risk="R3", deps="asignacion_evidencias; secciones funcionales (D5).",
  funcs="F16")

F(id="MDJ-D06-010", tech="asignacion_evidencia_seccion_decisiva", func="Evidencia en sección decisiva",
  dim="D06", profiles="JUR; ADM", unit=ASIG,
  defn="Indica si al menos una evidencia de la asignación está en los fundamentos del problema resuelto o en la parte resolutiva.",
  just="Control obligatorio de la arquitectura: sin evidencia decisiva, una asignación principal o secundaria en jurisprudencia o actos contenciosos se rechaza.",
  dtype="Boolean", card="0..1 obligatorio condicionado", values="true / false.",
  example="true", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Verdadero si asignacion_seccion_evidencia contiene una sección decisiva.",
  validation="Obligatorio para asignaciones principal o secundaria en JUR y ADM contenciosos; si es false, la asignación se degrada a contexto o se descarta.",
  applicability="Jurisprudencia y actos administrativos contenciosos o sancionadores.",
  prio="P1", mode="B", stage="E7", risk="R2", deps="asignacion_seccion_evidencia; asignacion_nivel_relevancia.",
  funcs="F01; F07; F16")

F(id="MDJ-D06-011", tech="asignacion_pruebas_superadas", func="Pruebas de relevancia superadas",
  dim="D06", unit=ASIG,
  defn="Pruebas de relevancia que la asignación supera según el modelo: objeto, supresión y consulta.",
  just="Hace explícito el criterio que justifica el nivel de relevancia en lugar de un límite numérico arbitrario.",
  dtype="Enum múltiple", card="0..n", values="CAT-304 Pruebas de relevancia temática.",
  example="[objeto, supresion, consulta]", origin="Inferido por modelo", method="Clasificación",
  evidence="La misma evidencia de la asignación.",
  extraction="El perfil responde por separado cada prueba para el concepto propuesto: ¿la regla, decisión o análisis recae sobre el concepto?, ¿sin él la unidad pierde su efecto principal?, ¿un especialista la necesitaría como fuente directa?",
  validation="Principal exige las tres; secundaria exige al menos 'objeto'; contexto no exige ninguna.",
  prio="P1", mode="A", stage="E5", risk="R2", deps="asignacion_nivel_relevancia.",
  funcs="F16; F18")

F(id="MDJ-D06-012", tech="asignacion_justificacion", func="Justificación de la asignación",
  dim="D06", unit=ASIG,
  defn="Frase breve con plantilla fija que explica la asignación: 'La unidad [función] [objeto] porque [razón]'.",
  just="Permite revisar y explicar la clasificación sin releer el documento; exigencia de la arquitectura (C.6).",
  dtype="Texto largo", card="0..1 obligatorio condicionado", values="Texto libre con plantilla fija; máximo 300 caracteres.",
  example="La unidad decide el despido nulo porque declara fundada la reposición por discriminación por embarazo (fundamento 9).",
  origin="Inferido por modelo", method="Inferencia", evidence="La misma evidencia de la asignación.",
  extraction="El perfil de clasificación redacta la frase usando solo información de las evidencias citadas.",
  validation="Respeta la plantilla; menciona la función registrada; no introduce hechos ausentes de la evidencia.",
  applicability="Obligatoria para asignaciones principal y secundaria; opcional para contexto.",
  prio="P1", mode="A", stage="E5", risk="R3", deps="asignacion_funcion_juridica; asignacion_evidencias.",
  funcs="F02; F15; F16")

F(id="MDJ-D10-007", tech="asignacion_rol_sector", func="Rol del sector en la unidad",
  dim="D10", unit=ASIG,
  defn="Para asignaciones de la faceta F9: si la actividad es sector regulado (la unidad establece reglas para ella) o sector del caso (actividad del sujeto sin que la decisión dependa de ella).",
  just="Evita que una sentencia laboral contra una empresa textil se trate como regulación textil y alimente especialidades de práctica indebidas.",
  dtype="Enum", card="0..1 obligatorio condicionado", values="CAT-308 Rol del sector.",
  example="sector_del_caso", origin="Inferido por modelo", method="Clasificación",
  evidence="Tramo que regula la actividad (regulado) o que describe la actividad del sujeto (caso).",
  extraction="Regulado si la unidad impone obligaciones, condiciones o sanciones propias de la actividad; del caso si la actividad solo describe al sujeto o los hechos.",
  validation="Obligatorio si asignacion_faceta = F9; prohibido en otras facetas.",
  applicability="Solo asignaciones de la faceta F9.",
  prio="P1", mode="A", stage="E5", risk="R2", deps="asignacion_faceta.", funcs="F10; F01")

F(id="MDJ-D06-014", tech="asignacion_estado_taxonomico", func="Estado de la asignación frente a cambios de taxonomía",
  dim="D06", unit=ASIG,
  defn="Situación de la asignación cuando el concepto asignado se fusiona, divide o desactiva.",
  just="Garantiza que los especialistas consulten la taxonomía vigente sin perder el historial de clasificación.",
  dtype="Enum", card="1 obligatorio", values="CAT-305 Estado de la asignación frente a cambios de taxonomía.",
  example="remapeada_por_fusion", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Se recalcula al publicar una versión de taxonomía según la operación aplicada al concepto.",
  validation="'pendiente_reclasificacion' solo si el concepto fue dividido; 'historica' solo si fue desactivado sin sucesor.",
  prio="P1", mode="B", stage="E7", risk="R3", deps="concepto_estado_ciclo_vida; concepto_sucesores.",
  funcs="F16; F18")

# ---------------------------------------------------------------------------
# D06 · Campos calculados sobre la unidad y la obra
# ---------------------------------------------------------------------------
F(id="MDJ-D06-015", tech="obra_clasificacion_principal_agregada", func="Materias principales de la obra",
  dim="D06", unit="Obra",
  defn="Conceptos que son principales en las unidades que contienen el objeto declarado de la obra o en una proporción relevante de sus unidades.",
  just="Da una clasificación global sin convertir una ley de presupuesto en laboral por un artículo.",
  dtype="Array de referencias", card="0..n", values="Referencias a conceptos de la taxonomía (facetas F1, F2, F4, F5).",
  example="[Tributario y Financiero Público › Derecho Presupuestario]", origin="Derivado por cálculo", method="Cálculo",
  evidence=NA_CALC,
  extraction="Regla de agregación (C.5): principal en unidades de objeto declarado, o en una proporción de unidades calibrada por tipo documental.",
  validation="Cada concepto es principal en al menos una unidad de la obra; la proporción usada consta en la versión de la regla.",
  prio="P1", mode="B", stage="E7", risk="R2", deps="obra_unidades_objeto_declarado; asignaciones por unidad.",
  funcs="F01; F02; F03; F04",
  obs="La proporción mínima se calibra en el piloto por tipo documental.", pending="DEC-11")

F(id="MDJ-D06-016", tech="obra_principal_en_fragmento", func="Materias principales en fragmentos",
  dim="D06", unit="Obra",
  defn="Conceptos principales en alguna unidad que no alcanzan la agregación a la obra, con la lista de unidades que los contienen.",
  just="Permite al especialista Laboral encontrar el artículo laboral de una ley de presupuesto sin clasificar la ley entera.",
  dtype="Array", card="0..n", values="Objetos {concepto: referencia, unidades: array de referencias a unidades estructurales}.",
  example="[{concepto: Laboral › Empleo público, unidades: [art. 15]}]", origin="Derivado por cálculo", method="Cálculo",
  evidence=NA_CALC, extraction="Diferencia entre las principales por unidad y obra_clasificacion_principal_agregada.",
  validation="Ningún concepto aparece a la vez aquí y en la clasificación principal agregada.",
  prio="P1", mode="B", stage="E7", risk="R3", deps="obra_clasificacion_principal_agregada; asignaciones por unidad.",
  funcs="F01; F03; F04")

F(id="MDJ-D06-017", tech="obra_unidades_objeto_declarado", func="Unidades de objeto declarado",
  dim="D06", unit="Obra",
  defn="Unidades que expresan el objeto o finalidad de la obra: artículo de objeto, título preliminar, parte resolutiva, resumen o introducción de la doctrina.",
  just="Son el insumo de la regla de agregación de la clasificación a la obra.",
  dtype="Array de referencias", card="0..n", values="Referencias a unidades estructurales de la obra.",
  example="[art. 1 'Objeto de la ley']", origin="Inferido por modelo", method="Inferencia",
  evidence="Rótulo o epígrafe de la unidad ('Objeto', 'Finalidad') o tramo que declara el objeto.",
  extraction="Identificar por epígrafe o contenido las unidades que declaran objeto, finalidad o ámbito; en JUR y ADM, la parte resolutiva; en DOC, el resumen.",
  validation="Las unidades pertenecen a la obra; en NOR, si existe epígrafe 'Objeto' debe estar incluida.",
  prio="P1", mode="A", stage="E5", risk="R3", deps="Estructura de la obra (D5).", funcs="F02; F04")

F(id="MDJ-D06-018", tech="unidad_numero_asignaciones_principales", func="Número de asignaciones principales de la unidad",
  dim="D06", unit="Unidad estructural",
  defn="Cantidad de asignaciones principales vigentes de la unidad, por faceta.",
  just="Insumo de la alerta estadística de sobreclasificación; no es un límite.",
  dtype="Objeto", card="1 obligatorio", values="Objeto {faceta: entero ≥ 0} por cada faceta CAT-301.",
  example="{F2: 2, F5: 3}", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Conteo de asignaciones con nivel principal y estado vigente.",
  validation="Coincide con el conteo real de asignaciones.",
  prio="P1", mode="B", stage="E7", risk="R3", deps="asignacion_nivel_relevancia; asignacion_estado_taxonomico.",
  funcs="F16; F18")

F(id="MDJ-D06-019", tech="unidad_alerta_sobreclasificacion", func="Alerta de sobreclasificación",
  dim="D06", unit="Unidad estructural",
  defn="Marca que indica que la unidad tiene más asignaciones principales que lo esperado para su tipo, según la distribución medida en el piloto.",
  just="Envía la unidad a una muestra de revisión sin recortar etiquetas de forma automática; también detecta unidades mal segmentadas.",
  dtype="Boolean", card="1 obligatorio", values="true / false.",
  example="false", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Verdadero si unidad_numero_asignaciones_principales supera el umbral de alerta calibrado para el tipo de unidad y perfil.",
  validation="El umbral aplicado consta en la configuración versionada; nunca elimina asignaciones.",
  prio="P1", mode="B", review="Condicionado", stage="E8", risk="R3",
  deps="unidad_numero_asignaciones_principales; umbrales por tipo (DEC-11).", funcs="F16; F18",
  obs="Revisión humana sobre muestra de unidades con alerta. Umbrales por tipo, no universales.", pending="DEC-11")

# ---------------------------------------------------------------------------
# D06 · Facetas sobre la unidad (vistas por faceta de las asignaciones)
# ---------------------------------------------------------------------------
_FAC_OBS = ("Vista por faceta de las asignaciones (MDJ-D06-001 a 014): no se almacena una segunda vez; "
            "su perfil de extracción es específico de la faceta.")


def FAC(id, tech, func, faceta, defn, just, example, extraction, prio="P1", mode="A", origin="Inferido por modelo",
        method="Clasificación", risk="R2", funcs="F01; F03; F04", stage="E5", review="Condicionado", pending="No",
        obs=_FAC_OBS, values=None, country_status="Común", applicability=None, profiles="UNI"):
    F(id=id, tech=tech, func=func, dim="D06", unit="Unidad estructural", profiles=profiles,
      defn=defn, just=just, dtype="Array de referencias", card="0..n",
      values=values or f"Conceptos de la faceta {faceta} (CAT-301) en la taxonomía vigente.",
      example=example, origin=origin, method=method, evidence=EV_CLASIF if origin != "Conclusión jurídica por reglas" else NA_CALC,
      extraction=extraction,
      validation=f"Solo conceptos de la faceta {faceta}; cada valor respaldado por una asignación con evidencia y nivel de relevancia.",
      prio=prio, mode=mode, review=review, stage=stage, risk=risk,
      deps="Asignaciones de clasificación de la unidad; taxonomía vigente.", funcs=funcs, obs=obs, pending=pending,
      country_status=country_status,
      applicability=applicability or "Todas las unidades clasificables según los criterios de granularidad (E.3).")


FAC("MDJ-D06-020", "clasif_area_matriz", "Área matriz del Derecho", "F1",
    "Gran sector del ordenamiento al que pertenece la materia de la unidad (p. ej., Laboral y Seguridad Social).",
    "Navegación de primer nivel y agrupación estable para todos los países.",
    "[Laboral y Seguridad Social]",
    "Se infiere del padre preferente de los conceptos F2 asignados; el modelo solo la asigna directamente si no hay F2 aplicable.",
    origin="Derivado por cálculo", method="Cálculo", mode="B", stage="E7", risk="R3", review="No",
    values="CAT-318 Áreas matrices (semilla de la faceta F1).")
FAC("MDJ-D06-021", "clasif_rama_especialidad", "Rama y especialidad dogmática", "F2",
    "Disciplina jurídica que estudia la materia de la unidad (p. ej., Derecho Aduanero, Contratación Pública). Polijerárquica con padre preferente.",
    "Base de los especialistas de Juztina y de la búsqueda por materia.",
    "[Derecho Individual del Trabajo]",
    "Perfil de clasificación F2 sobre la unidad, con pruebas de relevancia; nivel más específico aplicable, sin ancestros.")
FAC("MDJ-D06-022", "clasif_especialidad_practica", "Especialidad de práctica (calculada)", "F3",
    "Campo profesional (p. ej., Derecho Minero, Derecho de la Moda) que resulta de aplicar reglas sobre otras facetas y el rol del sector.",
    "Permite crear especialistas sin reclasificar el corpus; la regla es explícita y discutible por los especialistas.",
    "[Derecho Minero]",
    "No la asigna el modelo. Se calcula con reglas versionadas, p. ej., Minero = sector regulado minería ∧ rama ∈ {Ambiental, Administrativo, Tributario, Laboral}.",
    origin="Conclusión jurídica por reglas", method="Cálculo", mode="B", stage="E7", risk="R2", review="No",
    pending="DEC-12",
    obs="Reglas concretas pendientes de los especialistas (DEC-12). " + _FAC_OBS)
FAC("MDJ-D06-023", "clasif_subespecialidad", "Subespecialidad", "F4",
    "Parte de una especialidad dogmática a la que pertenece la materia (p. ej., Extinción del vínculo laboral).",
    "Granularidad intermedia para especialistas y filtros avanzados.",
    "[Extinción del vínculo]",
    "Perfil de clasificación F4 con las mismas pruebas; se asigna en lugar de F2 cuando es aplicable (F2 se infiere como ancestro).")
FAC("MDJ-D06-024", "clasif_institucion_juridica", "Institución jurídica", "F5",
    "Figura con régimen jurídico propio regulada, decidida o analizada en la unidad (p. ej., despido arbitrario, prescripción tributaria). Puede ser concepto nacional o pivote.",
    "Es la faceta más útil para investigación y comparación; las instituciones nacionales se vinculan por semejanza funcional, no por identidad.",
    "[Despido nulo o discriminatorio (PE)]",
    "Perfil F5: identificar instituciones sobre las que recae la regla o decisión; preferir el concepto nacional del país de la obra y no el pivote.",
    country_status="Catálogo por país", pending="DEC-14",
    obs="Los conceptos nacionales y sus correspondencias requieren validación del responsable de cada país. " + _FAC_OBS)
FAC("MDJ-D06-025", "clasif_concepto_juridico", "Concepto jurídico", "F6",
    "Noción jurídica atómica utilizada de forma relevante en la unidad (p. ej., buena fe, plazo razonable, carga de la prueba).",
    "Búsqueda conceptual fina y relaciones asociativas en el grafo.",
    "[Carga de la prueba]",
    "Perfil F6 solo si la noción es objeto de definición, regla o razonamiento decisivo; nunca por aparición del término.",
    prio="P3", mode="C", stage="Posterior (C)", risk="R3", review="No", funcs="F03; F04; F12")
FAC("MDJ-D06-026", "clasif_tema", "Tema", "F7",
    "Asunto concreto o emergente que trata la unidad (p. ej., teletrabajo, criptoactivos), de la faceta más dinámica.",
    "Captura asuntos nuevos antes de que justifiquen una institución o rama propia.",
    "[Teletrabajo]",
    "Perfil F7 con lista abierta gobernada; si el tema no existe se propone como concepto en estado 'propuesto', no se crea libre.",
    prio="P3", mode="C", stage="Posterior (C)", risk="R3", review="No", funcs="F03; F04; F05")
FAC("MDJ-D06-027", "clasif_subtema", "Subtema", "F7",
    "Subdivisión de un tema de la faceta F7 (p. ej., teletrabajo › derecho a la desconexión digital).",
    "Afinar búsqueda y alertas por asuntos emergentes.",
    "[Derecho a la desconexión digital]",
    "Se asigna en lugar del tema cuando aplica; el tema se infiere como ancestro.",
    prio="P3", mode="C", stage="Posterior (C)", risk="R3", review="No", funcs="F03; F05")
FAC("MDJ-D06-028", "clasif_materia_juztina_actual", "Materia según la clasificación actual de Juztina", "F2",
    "Materia asignada al documento por los criterios vigentes de selección de especialistas de Juztina (emisor, tipo documental y materia), conservada y mapeada a la taxonomía facetada.",
    "Garantiza continuidad con los especialistas actuales y permite medir la cobertura de la nueva clasificación frente a la anterior.",
    "[Laboral] (sistema actual) → CON-LAB-000001",
    "Se importa del sistema actual sin reinterpretarla; el mapeo a conceptos de la taxonomía lo curan los especialistas.",
    origin="Fuente externa", method="Enriquecimiento externo", mode="D", stage="Curaduría", risk="R3", review="Sí",
    prio="P0", values="Valores del sistema actual de Juztina mapeados a conceptos de CAT-301 F2.",
    pending="DEC-12",
    obs="Depende de los criterios actuales de los especialistas, aún no documentados. Se marca P0 porque su pérdida impediría comparar con la línea base.",
    applicability="Obras ya clasificadas por el sistema actual de Juztina; el valor se registra a nivel de obra y se replica en sus unidades.")
FAC("MDJ-D06-029", "clasif_sujetos_afectados", "Sujetos o grupos afectados", "F8",
    "Categorías de sujetos a quienes la unidad afecta (trabajador, consumidor, MYPE, contribuyente, pueblos indígenas, niñas, niños y adolescentes, entidad pública…).",
    "Filtros por destinatario y análisis de impacto; base de enfoques de protección.",
    "[Trabajadora gestante; Empleador privado]",
    "Perfil F8: sujetos a quienes la regla o decisión impone, reconoce o niega algo; no los mencionados de paso.",
    funcs="F01; F03; F04; F13")
FAC("MDJ-D06-030", "clasif_enfoque_transversal", "Enfoques transversales", "F10",
    "Perspectiva expresa desde la que se regula o decide (derechos humanos, género, interculturalidad, anticorrupción, sostenibilidad, interés superior del niño).",
    "Permite investigación transversal y verificación de estándares interamericanos.",
    "[Enfoque de género]",
    "Solo si la unidad invoca o aplica expresamente el enfoque; no se infiere por el tema.",
    values="CAT-320 Enfoques transversales (semilla).", funcs="F03; F04; F09")
FAC("MDJ-D06-031", "clasif_funcion_juridica_unidad", "Función jurídica de la unidad", "F11",
    "Qué hace la unidad en el ordenamiento: sancionadora, tributaria, habilitante, organizativa, procedimental, protectora de derechos, definitoria o interpretativa.",
    "Filtro por tipo de regla y base para mapas de obligaciones y compliance.",
    "[sancionadora]",
    "Perfil F11 sobre la unidad completa (no sobre un concepto); puede tener varias funciones.",
    values="CAT-321 Función jurídica de la unidad (faceta F11).", funcs="F03; F13; F04", risk="R3")

# ---------------------------------------------------------------------------
# D06 · Entidad: concepto de taxonomía
# ---------------------------------------------------------------------------
_CON_APP = "Todos los conceptos de la taxonomía facetada (Entidad: concepto de taxonomía)."
_CUR = dict(origin="Curado por persona", method="Revisión humana", mode="D", stage="Curaduría", review="Sí",
            applicability=_CON_APP, risk="R2")

F(id="MDJ-D06-032", tech="concepto_id", func="Identificador persistente del concepto",
  dim="D06", unit=CONC,
  defn="Identificador opaco y persistente del concepto de la taxonomía; nunca se reutiliza ni cambia al renombrar.",
  just="Las asignaciones apuntan al identificador; renombrar o mover un concepto no rompe la clasificación.",
  dtype="Identificador", card="1 obligatorio", values="Formato CON-<siglas faceta>-<número>; opaco.",
  example="CON-LAB-000148", origin="Generado por sistema", method="Generado por sistema", evidence=NA_SIS,
  extraction="Se genera al aprobar la creación del concepto.",
  validation="Único; nunca reasignado a otro concepto, aun desactivado.",
  prio="P0", mode="D", stage="Curaduría", risk="R3", applicability=_CON_APP, deps="No aplica: no depende de otros campos.",
  funcs="F18")

F(id="MDJ-D06-033", tech="concepto_faceta", func="Faceta del concepto",
  dim="D06", unit=CONC,
  defn="Faceta (F1 a F11) a la que pertenece el concepto.",
  just="Impide mezclar facetas y fija qué perfil de clasificación lo puede asignar.",
  dtype="Enum", card="1 obligatorio", values="CAT-301 Facetas de la taxonomía jurídica.",
  example="F5", evidence="Acta o registro de aprobación del concepto.",
  extraction="La fija el comité taxonómico al crear el concepto.",
  validation="Un solo valor; coincide con la faceta de sus padres.",
  prio="P0", deps="concepto_id.", funcs="F18", **_CUR)

F(id="MDJ-D06-034", tech="concepto_etiqueta_preferente", func="Etiqueta preferente",
  dim="D06", unit=CONC,
  defn="Denominación principal del concepto en español neutro (pivote) o en la terminología del país (concepto nacional).",
  just="Nombre mostrado al usuario y usado en instrucciones de clasificación.",
  dtype="String", card="1 obligatorio", values="Texto único dentro de la faceta y el ámbito.",
  example="Despido nulo o discriminatorio", evidence="Fuente normativa o doctrinal que justifica la denominación.",
  extraction="La define el responsable de la materia; los conceptos nacionales usan la denominación legal del país.",
  validation="Única por faceta y ámbito; sin siglas sin desarrollar.",
  prio="P0", deps="concepto_id; concepto_ambito.", funcs="F18; F03", **_CUR)

F(id="MDJ-D06-035", tech="concepto_etiquetas_alternativas", func="Etiquetas alternativas",
  dim="D06", unit=CONC,
  defn="Sinónimos, siglas, variantes y términos históricos del mismo concepto, con país e idioma. Solo para equivalencia terminológica (mismo concepto).",
  just="Mejora búsqueda y detección sin crear conceptos duplicados ni forzar equivalencias entre instituciones distintas.",
  dtype="Array", card="0..n",
  values="Objetos {etiqueta, pais: CAT-001, idioma: CAT-009, tipo: CAT-319}.",
  example="[{etiqueta: 'LPAG', pais: PE, idioma: es, tipo: sigla}]",
  evidence="Uso documentado en normas, jurisprudencia o doctrina del país.",
  extraction="Las proponen los responsables de país; también se sugieren desde referencias no resueltas (D7) para curaduría.",
  validation="No se usa para instituciones de otro país con régimen distinto; esas van a concepto_correspondencias.",
  prio="P1", deps="concepto_id.", funcs="F03; F18", country_status="Catálogo por país", **_CUR)

F(id="MDJ-D06-036", tech="concepto_nota_alcance_incluye", func="Nota de alcance: incluye",
  dim="D06", unit=CONC,
  defn="Descripción de lo que el concepto comprende.",
  just="Sin nota de alcance ni el modelo ni los anotadores clasifican de forma consistente.",
  dtype="Texto largo", card="1 obligatorio", values="Texto libre; máximo 800 caracteres.",
  example="Despidos fundados en motivos discriminatorios o vulneratorios de derechos fundamentales y su remedio de reposición.",
  evidence="Fuentes normativas o doctrinales citadas en concepto_garantia_literaria.",
  extraction="La redacta el especialista de la materia y la valida el responsable del país si es nacional.",
  validation="Obligatoria para conceptos activos; se incluye en las instrucciones del perfil de clasificación.",
  prio="P0", deps="concepto_id.", funcs="F18; F01", **_CUR)

F(id="MDJ-D06-037", tech="concepto_nota_alcance_excluye", func="Nota de alcance: excluye",
  dim="D06", unit=CONC,
  defn="Descripción de lo que el concepto no comprende y a qué concepto remitir esos casos.",
  just="Reduce confusiones entre conceptos vecinos y la sobreclasificación.",
  dtype="Texto largo", card="0..1 opcional", values="Texto libre con referencias a conceptos.",
  example="Excluye el despido sin causa sin motivo discriminatorio (ver CON-LAB-000147).",
  evidence="No aplica: definición curada por el responsable.",
  extraction="La redacta el especialista; recomendable cuando existen conceptos hermanos cercanos.",
  validation="Las remisiones apuntan a conceptos existentes.",
  prio="P1", deps="concepto_id.", funcs="F18", **_CUR)

F(id="MDJ-D06-038", tech="concepto_padres", func="Conceptos padre",
  dim="D06", unit=CONC,
  defn="Conceptos más generales de la misma faceta de los que depende el concepto (polijerarquía controlada).",
  just="Permite que una especialidad se relacione con varias áreas matrices sin duplicar el nodo.",
  dtype="Array de referencias", card="0..n", values="Referencias a conceptos de la misma faceta.",
  example="[Tributario y Financiero Público, Internacional]",
  evidence="No aplica: estructura curada.", extraction="La fija el comité taxonómico.",
  validation="Sin ciclos; misma faceta; profundidad máxima de tres niveles en F2 y F4.",
  prio="P0", deps="concepto_id; concepto_faceta.", funcs="F18; F03", **_CUR)

F(id="MDJ-D06-039", tech="concepto_padre_preferente", func="Padre preferente",
  dim="D06", unit=CONC,
  defn="Padre usado para la navegación por defecto y para inferir la faceta F1.",
  just="Ofrece una ruta única de navegación sin perder la polijerarquía.",
  dtype="Referencia", card="0..1 obligatorio condicionado", values="Uno de los valores de concepto_padres.",
  example="Tributario y Financiero Público",
  evidence="No aplica: estructura curada.", extraction="La fija el comité taxonómico.",
  validation="Obligatorio si concepto_padres tiene al menos un valor; debe pertenecer a esa lista.",
  prio="P0", deps="concepto_padres.", funcs="F18", **_CUR)

F(id="MDJ-D06-040", tech="concepto_relaciones_asociativas", func="Relaciones asociativas",
  dim="D06", unit=CONC,
  defn="Conceptos afines no jerárquicos, de la misma u otra faceta (p. ej., despido nulo ↔ protección de la maternidad).",
  just="Sugerencias de búsqueda y aristas del grafo de conocimiento.",
  dtype="Array de referencias", card="0..n", values="Referencias a conceptos activos.",
  example="[Protección de la maternidad; Igualdad y no discriminación]",
  evidence="No aplica: estructura curada.", extraction="Las proponen especialistas; se pueden sugerir por coocurrencia, con aprobación humana.",
  validation="Simétricas; no duplican una relación jerárquica.",
  prio="P2", deps="concepto_id.", funcs="F12; F03; F18", **_CUR)

F(id="MDJ-D06-041", tech="concepto_ambito", func="Ámbito del concepto",
  dim="D06", unit=CONC,
  defn="Si el concepto es pivote de Juztina, multinacional (fuente común, p. ej., norma comunitaria andina) o propio de un ordenamiento.",
  just="Evita presentar instituciones nacionales como universales y habilita la comparación por pivotes.",
  dtype="Enum", card="1 obligatorio", values="CAT-306 Ámbito del concepto.",
  example="nacional", evidence="Fuente que acredita el régimen del concepto.",
  extraction="Lo fija el comité taxonómico; los nacionales los valida el responsable del país.",
  validation="'nacional' y 'multinacional' exigen concepto_paises_ambito.",
  prio="P0", deps="concepto_id.", funcs="F09; F18", country_status="Catálogo por país", **_CUR)

F(id="MDJ-D06-042", tech="concepto_paises_ambito", func="Países del ámbito del concepto",
  dim="D06", unit=CONC,
  defn="Países u ordenamientos en los que rige el concepto cuando no es pivote.",
  just="Restringe la asignación de conceptos nacionales a documentos del país correspondiente.",
  dtype="Enum múltiple", card="0..1 obligatorio condicionado", values="CAT-001 País y jurisdicción.",
  example="[CO]", evidence="Fuente que acredita el régimen.",
  extraction="Lo fija el responsable del país al validar el concepto.",
  validation="Obligatorio si concepto_ambito ≠ pivote; vacío si es pivote.",
  prio="P0", deps="concepto_ambito.", funcs="F09; F18", country_status="Catálogo por país", **_CUR)

F(id="MDJ-D06-043", tech="concepto_estado_ciclo_vida", func="Estado del concepto",
  dim="D06", unit=CONC,
  defn="Estado del concepto en su ciclo de vida: propuesto, activo, fusionado, dividido o desactivado.",
  just="Ningún concepto se borra; el estado determina si puede asignarse y cómo se remapean las asignaciones.",
  dtype="Enum", card="1 obligatorio", values="CAT-307 Estado del ciclo de vida del concepto.",
  example="activo", evidence="Registro de cambio en la versión de taxonomía.",
  extraction="Lo cambia el comité taxonómico con análisis de impacto previo.",
  validation="Solo 'activo' admite nuevas asignaciones; 'fusionado' y 'dividido' exigen sucesores.",
  prio="P0", deps="concepto_id.", funcs="F18; F16", **_CUR)

F(id="MDJ-D06-044", tech="concepto_sucesores", func="Conceptos sucesores",
  dim="D06", unit=CONC,
  defn="Concepto o conceptos que reemplazan a uno fusionado, dividido o desactivado.",
  just="Permite redirigir asignaciones y búsquedas a la taxonomía vigente.",
  dtype="Array de referencias", card="0..1 obligatorio condicionado", values="Referencias a conceptos activos.",
  example="[CON-LAB-000201]", evidence="Registro de cambio en la versión de taxonomía.",
  extraction="Se fija al aprobar la fusión, división o desactivación.",
  validation="Obligatorio si estado = fusionado o dividido; uno para fusión, dos o más para división.",
  prio="P0", deps="concepto_estado_ciclo_vida.", funcs="F18", **_CUR)

F(id="MDJ-D06-045", tech="concepto_version_alta", func="Versión de alta del concepto",
  dim="D06", unit=CONC,
  defn="Versión de la taxonomía en la que el concepto pasó a activo.",
  just="Trazabilidad de la evolución de la taxonomía.",
  dtype="String", card="1 obligatorio", values="Identificador de versión de taxonomía.",
  example="2027.01.0", origin="Generado por sistema", method="Generado por sistema", evidence=NA_SIS,
  extraction="Se registra al publicar la versión que activa el concepto.",
  validation="Versión publicada; anterior o igual a concepto_version_ultimo_cambio.",
  prio="P0", mode="D", stage="Sistema", review="No", risk="R3", applicability=_CON_APP,
  deps="concepto_estado_ciclo_vida.", funcs="F18")

F(id="MDJ-D06-046", tech="concepto_version_ultimo_cambio", func="Versión del último cambio del concepto",
  dim="D06", unit=CONC,
  defn="Versión de la taxonomía en la que cambió por última vez la etiqueta, la nota, los padres o el estado del concepto.",
  just="Permite decidir qué asignaciones revisar tras un cambio de alcance.",
  dtype="String", card="1 obligatorio", values="Identificador de versión de taxonomía.",
  example="2027.04.1", origin="Generado por sistema", method="Generado por sistema", evidence=NA_SIS,
  extraction="Se actualiza al publicar una versión que modifica el concepto.",
  validation="Igual o posterior a concepto_version_alta.",
  prio="P1", mode="D", stage="Sistema", review="No", risk="R3", applicability=_CON_APP,
  deps="concepto_version_alta.", funcs="F18; F16")

F(id="MDJ-D06-047", tech="concepto_responsable_validacion", func="Responsable de validación del concepto",
  dim="D06", unit=CONC,
  defn="Rol que valida el concepto: comité taxonómico, especialista de la materia o responsable jurídico del país.",
  just="Asigna la responsabilidad jurídica de cada nodo, exigencia de la gobernanza (C.8).",
  dtype="Enum múltiple", card="1..n", values="Roles: comite_taxonomico, especialista_materia, responsable_pais_<ISO>.",
  example="[especialista_materia, responsable_pais_PE]", evidence="Registro de aprobación.",
  extraction="Lo registra el sistema de gobierno de la taxonomía al aprobar el concepto.",
  validation="Los conceptos nacionales incluyen el responsable del país correspondiente.",
  prio="P1", deps="concepto_ambito.", funcs="F18", pending="DEC-13",
  obs="La designación de personas para cada rol está pendiente (DEC-13).", **_CUR)

F(id="MDJ-D06-048", tech="concepto_garantia_literaria", func="Garantía literaria del concepto",
  dim="D06", unit=CONC,
  defn="Documentos y fuentes que justifican la existencia del concepto: normas que lo regulan y unidades reales que lo requieren.",
  just="Regla de creación: sin documentos reales que lo necesiten no se crea un nodo, se usa la faceta de temas.",
  dtype="Array de referencias", card="1..n", values="Referencias a obras o unidades estructurales del corpus o a fuentes externas citadas.",
  example="[Ley X art. 29; 34 unidades del piloto]", evidence="Las propias referencias citadas.",
  extraction="Se adjuntan en la propuesta de creación del concepto.",
  validation="Al menos una fuente normativa o un volumen mínimo de unidades definido por el comité.",
  prio="P1", deps="concepto_id.", funcs="F18", **_CUR)

F(id="MDJ-D06-049", tech="concepto_correspondencias", func="Correspondencias con conceptos de otros países",
  dim="D06", unit=CONC,
  defn="Vínculos del concepto con conceptos de otros ordenamientos o con su pivote, con tipo de equivalencia, diferencias documentadas y estado de validación.",
  just="Habilita la comparación entre países sin forzar equivalencias inexistentes; solo la equivalencia jurídica validada permite decir 'el equivalente es'.",
  dtype="Array", card="0..n",
  values="Objetos {concepto_destino: referencia, tipo: CAT-012, nota_diferencias: texto, validado_por: roles, estado: propuesta|validada|rechazada}.",
  example="[{concepto_destino: Pivote 'garantía jurisdiccional de derechos fundamentales', tipo: semejanza_funcional, nota_diferencias: 'plazos y legitimación distintos', estado: propuesta}]",
  evidence="Fuentes normativas de ambos ordenamientos citadas en la nota de diferencias.",
  extraction="Las proponen especialistas; nunca se infieren automáticamente por similitud de nombre.",
  validation="'equivalencia_juridica' exige validación de los responsables de todos los países involucrados; 'semejanza_funcional' exige nota de diferencias.",
  prio="P2", deps="concepto_ambito; concepto_paises_ambito.", funcs="F09; F12; F18",
  country_status="Pendiente validación nacional", pending="DEC-14",
  obs="Ninguna correspondencia se considera validada hasta la revisión nacional (DEC-14).", **_CUR)

F(id="MDJ-D06-050", tech="concepto_regla_especialidad_practica", func="Regla de la especialidad de práctica",
  dim="D06", unit=CONC,
  defn="Expresión lógica versionada que define un concepto F3 combinando facetas, rol del sector y otras condiciones.",
  just="Las especialidades de práctica se calculan; crear un especialista nuevo es definir una regla, no reclasificar.",
  dtype="Objeto", card="0..1 obligatorio condicionado",
  values="Objeto {expresion: lógica sobre IDs de conceptos y roles, version, aprobada_por}.",
  example="{expresion: 'F9 regulado ∈ {minería} ∧ F2 ∈ {Ambiental, Administrativo, Tributario, Laboral}', version: 1}",
  evidence="Acta de aprobación de los especialistas.",
  extraction="La redactan los especialistas de la materia con el comité taxonómico.",
  validation="Obligatoria si concepto_faceta = F3; solo referencia conceptos activos; se prueba sobre el piloto antes de publicarse.",
  prio="P1", deps="concepto_faceta.", funcs="F01; F18", pending="DEC-12",
  applicability="Conceptos de la faceta F3.", origin="Curado por persona", method="Revisión humana", mode="D",
  stage="Curaduría", review="Sí", risk="R2")

F(id="MDJ-D06-051", tech="concepto_precision_piloto", func="Precisión del concepto en el piloto",
  dim="D06", unit=CONC,
  defn="Precisión medida de las asignaciones automáticas del concepto contra el conjunto de referencia anotado.",
  just="Un nodo con baja precisión se excluye del uso automático hasta revisar su nota de alcance (C.4).",
  dtype="Porcentaje", card="0..1 opcional", values="0 % a 100 %, con fecha y tamaño de muestra.",
  example="92,5 % (n = 120)", origin="Derivado por cálculo", method="Cálculo",
  evidence="Conjunto de referencia anotado y versión de la ejecución medida.",
  extraction="Se calcula al comparar asignaciones del piloto con la anotación de abogados.",
  validation="Se informa con tamaño de muestra; si n < mínimo definido, el valor se marca como no concluyente.",
  prio="P1", mode="B", stage="E8", review="No", risk="R3", applicability=_CON_APP,
  deps="Conjunto de referencia del piloto; asignaciones del concepto.", funcs="F16; F18", pending="DEC-20")

F(id="MDJ-D06-052", tech="concepto_habilitado_uso_automatico", func="Habilitado para uso automático",
  dim="D06", unit=CONC,
  defn="Indica si las asignaciones automáticas del concepto pueden alimentar especialistas y filtros sin revisión.",
  just="Aplica el control de precisión por nodo sin bloquear el resto de la taxonomía.",
  dtype="Boolean", card="1 obligatorio", values="true / false.",
  example="true", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Verdadero si concepto_precision_piloto alcanza la meta de su clase de riesgo y el concepto está activo.",
  validation="Falso para conceptos no activos o sin medición concluyente.",
  prio="P1", mode="B", stage="E8", review="No", risk="R3", applicability=_CON_APP,
  deps="concepto_precision_piloto; concepto_estado_ciclo_vida.", funcs="F01; F16; F18", pending="DEC-20")

F(id="MDJ-D10-008", tech="concepto_codigo_ciiu", func="Código CIIU Rev. 4 del concepto sectorial",
  dim="D10", unit=CONC,
  defn="Código de la Clasificación Industrial Internacional Uniforme (CIIU Rev. 4, Naciones Unidas) que corresponde a un concepto de la faceta F9.",
  just="Pivote internacional para comparar sectores entre países y para due diligence sectorial.",
  dtype="Array", card="0..1 obligatorio condicionado", values="Códigos CIIU Rev. 4 (sección, división, grupo o clase).",
  example="[07 Extracción de minerales metalíferos]", origin="Fuente externa", method="Enriquecimiento externo",
  evidence="Tabla oficial CIIU Rev. 4 (fuente externa).",
  extraction="Se asigna desde la tabla oficial al crear el concepto sectorial.",
  validation="Código existente en CIIU Rev. 4; obligatorio para conceptos F9 que representan actividades.",
  applicability="Conceptos de la faceta F9.", prio="P1", mode="D", stage="Curaduría", review="Sí", risk="R3",
  deps="concepto_faceta.", funcs="F10; F09")

F(id="MDJ-D10-009", tech="concepto_codigos_actividad_nacionales", func="Códigos de actividad nacionales",
  dim="D10", unit=CONC,
  defn="Códigos del sistema nacional de clasificación de actividades de cada país (adaptaciones de la CIIU o sistemas propios como el SCIAN en México).",
  just="Conservar la denominación original del país y vincularla con el pivote sin forzar equivalencias.",
  dtype="Array", card="0..n",
  values="Objetos {pais: CAT-001, sistema: CAT-323, codigo, tipo_equivalencia_ciiu: CAT-012}.",
  example="[{pais: MX, sistema: SCIAN, codigo: '2122', tipo_equivalencia_ciiu: semejanza_funcional}]",
  origin="Fuente externa", method="Enriquecimiento externo", evidence="Tabla de correspondencias oficial del país.",
  extraction="Se cargan desde tablas oficiales de correspondencia de cada país.",
  validation="Código existente en el sistema nacional vigente; la vigencia del sistema se verifica por país.",
  applicability="Conceptos de la faceta F9.", prio="P2", mode="D", stage="Curaduría", review="Sí", risk="R3",
  deps="concepto_codigo_ciiu.", funcs="F10; F09", country_status="Catálogo por país", pending="DEC-28",
  obs="Los sistemas nacionales vigentes y sus tablas de correspondencia deben confirmarse por país.")

# ---------------------------------------------------------------------------
# D10 · Información sectorial sobre unidades y obras
# ---------------------------------------------------------------------------
F(id="MDJ-D10-001", tech="sector_actividad", func="Sector y actividad económica",
  dim="D10", unit="Unidad estructural",
  defn="Actividades económicas reguladas por la unidad o que caracterizan al sujeto del caso, como conceptos de la faceta F9 con su rol.",
  just="Investigación sectorial, due diligence regulatorio y especialidades de práctica.",
  dtype="Array de referencias", card="0..n", values="Asignaciones de clasificación con faceta F9 y asignacion_rol_sector.",
  example="[{CIIU 07 Minería metalífera, rol: sector_regulado}]", origin="Inferido por modelo", method="Clasificación",
  evidence=EV_CLASIF,
  extraction="Perfil F9: identificar la actividad a la que la regla se dirige o que realiza el sujeto; elegir el código más específico aplicable y su rol.",
  validation="Cada valor tiene rol de sector y evidencia; no se asigna sector por la mera mención de una empresa.",
  prio="P1", mode="A", review="Condicionado", stage="E5", risk="R2",
  deps="Asignaciones de clasificación; concepto_codigo_ciiu.", funcs="F10; F01; F03; F13",
  obs="Vista por faceta F9 de las asignaciones; no se almacena dos veces.")

F(id="MDJ-D10-002", tech="actividad_economica_literal", func="Descripción literal de la actividad",
  dim="D10", unit="Unidad estructural",
  defn="Texto con el que el documento describe la actividad regulada o la actividad del sujeto.",
  just="Conserva la denominación original y permite reclasificar el sector sin releer el documento.",
  dtype="Array", card="0..n", values="Cadenas literales con ancla de evidencia.",
  example="['actividades de explotación y beneficio de minerales metálicos']", origin="Explícito en documento",
  method="Extracción directa", evidence="Tramo literal con ancla.",
  extraction="Copiar literalmente la expresión que nombra la actividad; no parafrasear.",
  validation="Coincidencia literal verificada con el texto normalizado.",
  prio="P1", mode="A", stage="E5", risk="R3", deps="Segmentación y anclas (D5).", funcs="F10; F03")

F(id="MDJ-D10-003", tech="sector_regulado_juztina", func="Sector regulado (catálogo Juztina)",
  dim="D10", unit="Unidad estructural",
  defn="Régimen regulatorio sectorial al que pertenece la unidad (telecomunicaciones, energía, sistema financiero, salud…), distinto de la actividad CIIU.",
  just="La CIIU describe actividades, no regímenes regulatorios; los especialistas y reguladores trabajan por régimen.",
  dtype="Enum múltiple", card="0..n", values="CAT-309 Sectores regulados (semilla).",
  example="[telecomunicaciones]", origin="Inferido por modelo", method="Clasificación",
  evidence=EV_CLASIF,
  extraction="Asignar solo si la unidad pertenece a un régimen sectorial específico (regla, supervisión o sanción sectorial); calcular directamente desde el emisor cuando este es un regulador sectorial.",
  validation="Coherente con sector_actividad de rol regulado o con el regulador emisor.",
  prio="P1", mode="A", stage="E5", risk="R2", deps="sector_actividad; emisor (D2).",
  funcs="F10; F01; F05; F13")

F(id="MDJ-D10-004", tech="sujetos_regulados", func="Sujetos regulados",
  dim="D10", unit="Unidad estructural",
  defn="Tipos de agentes económicos sometidos a la regulación sectorial de la unidad (concesionario, entidad supervisada, operador, titular de actividad).",
  just="Base para mapas de obligaciones por tipo de agente y due diligence.",
  dtype="Array", card="0..n", values="Objetos {categoria: concepto F8, literal: texto con ancla}.",
  example="[{categoria: Concesionario de servicios públicos, literal: 'las empresas operadoras'}]",
  origin="Inferido por modelo", method="Clasificación + Extracción directa", evidence="Tramo literal que nombra al sujeto.",
  extraction="Identificar a quién se dirige la obligación sectorial; conservar el literal y normalizar a un concepto F8.",
  validation="Literal verificado; categoría de la faceta F8.",
  applicability="Unidades con sector regulado; prioritario en normativa y actos sectoriales.",
  profiles="NOR; ADM; JUR", prio="P2", mode="C", stage="Posterior (C)", risk="R2",
  deps="sector_regulado_juztina; clasif_sujetos_afectados.", funcs="F13; F10")

F(id="MDJ-D10-005", tech="regulador_competente", func="Regulador o supervisor competente",
  dim="D10", unit="Unidad estructural",
  defn="Organismo con competencia de regulación, supervisión o fiscalización sobre la actividad regulada por la unidad, cuando el texto lo identifica.",
  just="Permite agrupar normas y actos por regulador y alimentar alertas sectoriales.",
  dtype="Array de referencias", card="0..n", values="Referencias a Entidad: organismo u órgano.",
  example="[Organismo supervisor de telecomunicaciones del país]", origin="Explícito en documento",
  method="Extracción directa + Normalización", evidence="Tramo que nombra al organismo competente.",
  extraction="Extraer solo organismos que el texto designa como competentes; normalizar al registro de organismos.",
  validation="El organismo existe en el registro con competencia vigente en la fecha del documento.",
  profiles="NOR; ADM", prio="P2", mode="C", stage="Posterior (C)", risk="R2",
  deps="Registro de organismos (D2).", funcs="F10; F05", country_status="Catálogo por país",
  applicability="Normativa y actos administrativos sectoriales.")

F(id="MDJ-D10-006", tech="obra_sectores_agregados", func="Sectores de la obra",
  dim="D10", unit="Obra",
  defn="Unión de sectores regulados y actividades con rol regulado en las unidades de la obra, con la proporción de unidades en que aparecen.",
  just="Filtro sectorial a nivel de documento sin perder el detalle por unidad.",
  dtype="Array", card="0..n", values="Objetos {concepto F9 o CAT-309, proporcion_unidades}.",
  example="[{telecomunicaciones, 0,82}]", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Agregación de sector_actividad (rol regulado) y sector_regulado_juztina de las unidades.",
  validation="Solo incluye sectores presentes en alguna unidad.",
  prio="P1", mode="B", stage="E7", risk="R3", deps="sector_actividad; sector_regulado_juztina.",
  funcs="F10; F03")

# ---------------------------------------------------------------------------
# D17 · Autoridad y fuerza jurídica
# ---------------------------------------------------------------------------
F(id="MDJ-D17-001", tech="autodeclaracion_fuerza_vinculante", func="Autodeclaración de fuerza vinculante",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Hecho primario: el propio pronunciamiento declara expresamente que establece un precedente, doctrina o criterio de observancia obligatoria.",
  just="Es el insumo más confiable del cálculo de fuerza; separa lo que dice el documento de la conclusión de Juztina.",
  dtype="Boolean", card="1 obligatorio", values="true / false / indeterminado (vía estado de campo).",
  example="true", origin="Explícito en documento", method="Extracción directa",
  evidence="Tramo literal de la declaración (p. ej., 'constituye precedente vinculante', 'de observancia obligatoria').",
  extraction="Buscar en la parte resolutiva y en los fundamentos la declaración expresa; no inferir por el prestigio del órgano.",
  validation="Si es true, exige evidencia literal verificada; si no hay declaración en texto completo y legible, estado 'no encontrado'.",
  prio="P0", mode="A", review="Condicionado", stage="E3", risk="R1",
  deps="Parte resolutiva delimitada (D5); calidad y completitud (D11).", funcs="F08; F07; F01",
  obs="R1: revisión humana antes de alimentar fuerza_juridica_pivote si el texto es ambiguo.")

F(id="MDJ-D17-002", tech="fundamentos_declarados_vinculantes", func="Fundamentos declarados vinculantes",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Unidades (fundamentos, considerandos) que el pronunciamiento señala expresamente como vinculantes o como regla de precedente.",
  just="En varios sistemas la vinculación se predica de fundamentos concretos y no de toda la sentencia.",
  dtype="Array de referencias", card="0..1 obligatorio condicionado", values="Referencias a unidades estructurales de la obra.",
  example="[fundamento 37, fundamento 38]", origin="Explícito en documento", method="Extracción directa",
  evidence="Tramo literal que enumera los fundamentos vinculantes.",
  extraction="Resolver los números de fundamento citados en la declaración a unidades estructurales de la misma obra.",
  validation="Solo si autodeclaracion_fuerza_vinculante = true; las unidades existen en la obra.",
  prio="P0", mode="A", review="Condicionado", stage="E3", risk="R1",
  deps="autodeclaracion_fuerza_vinculante; estructura (D5).", funcs="F08; F07")

F(id="MDJ-D17-003", tech="formacion_organo_decisor", func="Formación del órgano que decide",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Composición con la que se dictó la resolución: pleno, sala plena, sala o sección, sala especial, juez unipersonal, tribunal administrativo en sala plena o en sala.",
  just="La fuerza del precedente depende a menudo de la formación que decide; es un hecho primario del encabezado.",
  dtype="Enum", card="1 obligatorio", values="CAT-310 Formación del órgano decisor.",
  example="sala_plena", origin="Explícito en documento", method="Extracción directa + Normalización",
  evidence="Encabezado o firma que identifica la formación.",
  extraction="Leer el encabezado y las firmas; normalizar al catálogo sin inferir por el número de firmantes salvo regla explícita.",
  validation="Coherente con el órgano emisor (D2).",
  prio="P0", mode="A", stage="E3", risk="R2", deps="Órgano emisor (D2).", funcs="F08; F07",
  country_status="Catálogo por país")

F(id="MDJ-D17-004", tech="votacion_resultado", func="Resultado de la votación",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Número de votos a favor, en contra y otras posiciones con que se adoptó la decisión, cuando consta.",
  just="Algunas categorías de precedente exigen mayorías calificadas; también sirve al análisis jurisprudencial.",
  dtype="Objeto", card="0..1 opcional", values="Objeto {a_favor: entero, en_contra: entero, abstenciones: entero, otros: texto}.",
  example="{a_favor: 8, en_contra: 3}", origin="Explícito en documento", method="Extracción directa",
  evidence="Tramo literal que consigna la votación o firmas con indicación de voto.",
  extraction="Extraer solo si el texto consigna la votación; no deducirla del número de votos singulares.",
  validation="Enteros ≥ 0; la suma no supera la composición del órgano cuando esta es conocida.",
  prio="P1", mode="A", stage="E3", risk="R2", deps="formacion_organo_decisor.", funcs="F08; F07",
  privacy="Dato de funcionario público")

F(id="MDJ-D17-005", tech="decision_unanime", func="Decisión unánime",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Indica si la decisión se adoptó sin votos en contra.",
  just="Señal de solidez del criterio usada en análisis jurisprudencial.",
  dtype="Boolean", card="0..1 opcional", values="true / false.",
  example="false", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Se calcula desde votacion_resultado o desde la existencia de votos en discordia (D5).",
  validation="Indeterminado si no hay votación ni información de votos.",
  prio="P1", mode="B", stage="E7", risk="R3", deps="votacion_resultado; votos singulares (D5).", funcs="F07; F08")

F(id="MDJ-D17-006", tech="categoria_precedente_original", func="Categoría de precedente según el ordenamiento",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Denominación original de la categoría jurisprudencial o de precedente que el documento o el registro oficial le atribuye (p. ej., sentencia de unificación, tesis aislada, jurisprudencia por reiteración, precedente de observancia obligatoria).",
  just="Conserva la categoría nacional sin equipararla; es insumo del cálculo de fuerza pivote.",
  dtype="Enum", card="0..1 opcional", values="CAT-311 Categoría de precedente original por país (semilla pendiente de validación).",
  example="tesis_aislada (MX)", origin="Explícito en documento", method="Extracción directa + Normalización",
  evidence="Rótulo, encabezado o registro oficial que atribuye la categoría.",
  extraction="Extraer solo la categoría expresamente atribuida por el documento o su publicación oficial; no deducirla.",
  validation="Valor del catálogo del país de la obra; vacío con estado 'no encontrado' si no consta.",
  prio="P0", mode="A", review="Condicionado", stage="E3", risk="R1",
  deps="País (D1); tipo documental (D4).", funcs="F08; F09; F07",
  country_status="Pendiente validación nacional", pending="DEC-25",
  obs="El catálogo por país es una semilla ilustrativa; ningún valor está validado (DEC-25).")

F(id="MDJ-D17-007", tech="inclusion_registro_oficial_precedentes", func="Inclusión en registro oficial de precedentes",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Indica si el pronunciamiento figura en un registro, gaceta o sistematización oficial de precedentes o criterios del país, con su identificador.",
  just="La publicación oficial como precedente es, en algunos países, condición de su fuerza.",
  dtype="Objeto", card="0..1 opcional", values="Objeto {incluido: boolean, registro: texto, identificador: texto, fecha}.",
  example="{incluido: true, registro: 'Semanario Judicial de la Federación', identificador: '2024512'}",
  origin="Fuente externa", method="Enriquecimiento externo", evidence="Fuente oficial consultada y fecha de consulta.",
  extraction="Cruce con registros oficiales de precedentes del país cuando existan y estén autorizados.",
  validation="Fuente identificada y fecha de consulta registrada.",
  prio="P2", mode="D", stage="Curaduría", risk="R2", review="No", deps="Identificación oficial (D1).",
  funcs="F08; F07", country_status="Pendiente validación nacional", pending="DEC-25; DEC-17")

F(id="MDJ-D17-008", tech="fuerza_juridica_pivote", func="Fuerza jurídica (categoría común)",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Conclusión jurídica sobre la fuerza del pronunciamiento en categorías comunes (vinculante general, para órganos inferiores, para la administración, inter partes, persuasiva, indeterminada), calculada con reglas por país y período.",
  just="Responde '¿esto me obliga?' sin que el modelo afirme fuerza vinculante; base de la identificación de precedentes.",
  dtype="Enum", card="1 obligatorio", values="CAT-312 Fuerza jurídica pivote.",
  example="vinculante_organos_inferiores", origin="Conclusión jurídica por reglas", method="Cálculo",
  evidence="Regla de país aplicada (ID y versión) + insumos (autodeclaración, formación, votación, categoría, registro).",
  extraction="No la extrae el modelo. Reglas deterministas versionadas por país y período; si la regla del país no está validada, el valor es 'indeterminada'.",
  validation="Toda salida distinta de 'indeterminada' cita la regla validada y sus insumos; 'vinculante_*' exige que los insumos R1 estén revisados.",
  prio="P1", mode="B", review="Condicionado", stage="E7", risk="R1",
  deps="autodeclaracion_fuerza_vinculante; formacion_organo_decisor; votacion_resultado; categoria_precedente_original; base_normativa_fuerza.",
  funcs="F08; F07; F01; F02", country_status="Pendiente validación nacional", pending="DEC-25",
  obs="Reglas de fuerza vinculante y sus cambios en el tiempo pendientes de cada país (DEC-25).")

F(id="MDJ-D17-009", tech="base_normativa_fuerza", func="Base normativa de la fuerza",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Disposiciones que fundamentan la fuerza atribuida (p. ej., el artículo del código procesal constitucional que regula el precedente).",
  just="Toda fuerza vinculante debe poder justificarse con su fuente; exigencia de D17.",
  dtype="Array de referencias", card="0..1 obligatorio condicionado", values="Referencias a unidades estructurales normativas.",
  example="[Código Procesal Constitucional, art. VI]", origin="Curado por persona", method="Revisión humana",
  evidence="Fuente normativa incorporada a la regla de país.",
  extraction="Se toma de la regla de país validada que produjo fuerza_juridica_pivote.",
  validation="Obligatoria si fuerza_juridica_pivote ≠ indeterminada; las disposiciones están vigentes a la fecha del pronunciamiento.",
  prio="P1", mode="D", stage="Curaduría", review="Sí", risk="R1",
  deps="fuerza_juridica_pivote; vigencia (D3).", funcs="F08; F15",
  country_status="Pendiente validación nacional", pending="DEC-25")

F(id="MDJ-D17-010", tech="destinatarios_vinculacion", func="Destinatarios de la vinculación",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="A quiénes vincula el pronunciamiento según la regla aplicada: todos los jueces, órganos inferiores de la jurisdicción, la administración, los administrados o solo las partes.",
  just="La fuerza depende del destinatario; evita afirmar vinculación general de lo que solo obliga a la administración emisora.",
  dtype="Enum múltiple", card="0..n", values="CAT-322 Destinatarios de la vinculación.",
  example="[organos_inferiores_jurisdiccion]", origin="Conclusión jurídica por reglas", method="Cálculo",
  evidence="Regla de país aplicada e insumos.",
  extraction="Se obtiene junto con fuerza_juridica_pivote por la misma regla.",
  validation="Coherente con fuerza_juridica_pivote.",
  prio="P1", mode="B", review="Condicionado", stage="E7", risk="R1",
  deps="fuerza_juridica_pivote.", funcs="F08; F07; F02", country_status="Pendiente validación nacional", pending="DEC-25")

F(id="MDJ-D17-011", tech="estado_precedente", func="Estado del precedente o criterio",
  dim="D17", profiles="JUR; ADM", unit="Obra",
  defn="Situación actual del criterio: vigente, reiterado, modificado, superado, interrumpido o indeterminado, calculada desde relaciones posteriores.",
  just="Evita citar como precedente vigente un criterio superado.",
  dtype="Enum", card="1 obligatorio", values="CAT-313 Estado del precedente o criterio.",
  example="superado", origin="Conclusión jurídica por reglas", method="Cálculo",
  evidence="Relaciones posteriores (se aparta, supera, unifica, interrumpe) con su evidencia (D7).",
  extraction="Regla determinista sobre relaciones entrantes; 'superado' o 'interrumpido' solo con relaciones revisadas por humanos.",
  validation="Cualquier valor distinto de vigente o indeterminado cita la relación que lo produce y su estado de revisión.",
  prio="P2", mode="B", review="Sí", stage="E7", risk="R1",
  deps="Relaciones de uso de precedentes (D7); fuerza_juridica_pivote.", funcs="F08; F07; F05",
  country_status="Pendiente validación nacional", pending="DEC-25")

F(id="MDJ-D17-012", tech="observancia_obligatoria_declarada", func="Observancia obligatoria declarada (administración)",
  dim="D17", profiles="ADM", unit="Obra",
  defn="Hecho primario: la resolución de un tribunal administrativo o entidad declara expresamente que su criterio es de observancia obligatoria o constituye precedente administrativo.",
  just="Los precedentes administrativos tienen fuerza propia en varios países; deben distinguirse de la jurisprudencia.",
  dtype="Boolean", card="1 obligatorio", values="true / false.",
  example="true", origin="Explícito en documento", method="Extracción directa",
  evidence="Tramo literal de la declaración en la parte resolutiva o considerativa.",
  extraction="Buscar la declaración expresa; no inferirla del órgano.",
  validation="Si es true, evidencia literal verificada.",
  applicability="Actos administrativos de tribunales administrativos y entidades con potestad de fijar precedentes.",
  prio="P0", mode="A", review="Condicionado", stage="E3", risk="R1",
  deps="Parte resolutiva (D5).", funcs="F08; F01")

F(id="MDJ-D17-013", tech="fuerza_pronunciamiento_interpretativo", func="Fuerza del pronunciamiento interpretativo administrativo",
  dim="D17", profiles="ADM", unit="Obra",
  defn="Conclusión jurídica sobre a quién vincula un pronunciamiento interpretativo (concepto, informe, oficio, circular, criterio normativo, dictamen): a la administración emisora, a otras entidades, a los administrados u orientativo.",
  just="Los pronunciamientos interpretativos tienen efectos muy distintos por país y tipo; no deben presentarse como norma ni como jurisprudencia.",
  dtype="Enum", card="1 obligatorio", values="CAT-314 Fuerza del pronunciamiento interpretativo administrativo.",
  example="vinculante_administracion_emisora", origin="Conclusión jurídica por reglas", method="Cálculo",
  evidence="Regla de país aplicada (ID, versión) y tipo documental original.",
  extraction="Regla por país y tipo documental; 'indeterminada' mientras la regla no esté validada.",
  validation="Solo para naturaleza jurídica 'pronunciamiento interpretativo administrativo'; cita la regla aplicada.",
  applicability="Actos administrativos con naturaleza de pronunciamiento interpretativo.",
  prio="P1", mode="B", review="Condicionado", stage="E7", risk="R1",
  deps="Naturaleza jurídica (D4); tipo documental original (D4).", funcs="F01; F02; F04",
  country_status="Pendiente validación nacional", pending="DEC-26")

F(id="MDJ-D17-014", tech="autoridad_doctrinal_indexacion", func="Indexación del medio doctrinal",
  dim="D17", profiles="DOC", unit="Entidad: publicación o fuente",
  defn="Índices y bases en los que está indexada la revista o colección donde se publicó la obra doctrinal (Scopus, Web of Science, SciELO, Latindex, Dialnet, DOAJ…), con fecha de verificación.",
  just="Señal objetiva de autoridad doctrinal, ya usada en el mapeo de fuentes de Bolivia; evita juicios del modelo sobre la calidad del autor.",
  dtype="Array", card="0..n", values="Objetos {indice: CAT-315, nivel: texto (p. ej., 'catálogo'), fecha_verificacion}.",
  example="[{indice: latindex, nivel: 'directorio'}, {indice: dialnet}]",
  origin="Fuente externa", method="Enriquecimiento externo", evidence="Ficha del índice consultada y fecha.",
  extraction="Se verifica en los índices por ISSN; también se acepta lo declarado por la revista, marcado como 'declarado'.",
  validation="ISSN coincide con la ficha del índice; fecha de verificación no mayor a la política de actualización.",
  applicability="Doctrina publicada en revistas o colecciones identificables.",
  prio="P2", mode="D", stage="Curaduría", review="No", risk="R3",
  deps="ISSN de la publicación (D1).", funcs="F03; F04; F01",
  obs="Los archivos de Bolivia del repositorio ya registran 'Indexación / ISSN' por fuente: pueden sembrar este campo.")

F(id="MDJ-D17-015", tech="autoridad_doctrinal_revision_pares", func="Revisión por pares",
  dim="D17", profiles="DOC", unit="Obra",
  defn="Tipo de revisión editorial a la que se sometió la obra doctrinal: doble ciego, simple ciego, abierta, editorial, sin revisión o no consta.",
  just="Señal objetiva de rigor para ponderar la doctrina en búsqueda y respuestas.",
  dtype="Enum", card="1 obligatorio", values="CAT-316 Tipo de revisión por pares.",
  example="doble_ciego", origin="Explícito en documento", method="Extracción directa + Normalización",
  evidence="Mención en la obra o en la política editorial de la publicación (fuente externa).",
  extraction="Leer la indicación en la obra; si no consta, heredar de la política editorial de la publicación como 'declarado por la publicación'.",
  validation="Valor del catálogo; 'no_consta' si no hay evidencia.",
  applicability="Doctrina.", prio="P1", mode="A", stage="E3", risk="R3",
  deps="Publicación (D1, D2).", funcs="F03; F04")

F(id="MDJ-D17-016", tech="autoridad_doctrinal_nivel_academico", func="Nivel académico de la obra",
  dim="D17", profiles="DOC", unit="Obra",
  defn="Nivel de la obra: investigación arbitrada, tesis doctoral, tesis de maestría, trabajo de pregrado, divulgación, material docente o comentario profesional.",
  just="Distingue autoridad doctrinal sin juzgar al autor; dato ya presente como 'Nivel' en los mapas de Bolivia.",
  dtype="Enum", card="1 obligatorio", values="CAT-317 Nivel académico o de publicación.",
  example="tesis_maestria", origin="Explícito en documento", method="Extracción directa + Normalización",
  evidence="Portada, colofón o metadatos del repositorio.",
  extraction="Leer la portada o la ficha del repositorio; normalizar al catálogo.",
  validation="Valor del catálogo; coherente con el tipo de publicación doctrinal (D4).",
  applicability="Doctrina.", prio="P1", mode="A", stage="E3", risk="R3",
  deps="Tipo de obra doctrinal (D4).", funcs="F03; F04; F01")

F(id="MDJ-D17-017", tech="autoridad_doctrinal_citas_recibidas", func="Citas recibidas por la obra doctrinal",
  dim="D17", profiles="DOC", unit="Obra",
  defn="Número de unidades del corpus (sentencias, actos, otra doctrina) que citan la obra, separado por categoría de colección.",
  just="Mide la influencia real de la doctrina en la jurisprudencia sin juicios subjetivos.",
  dtype="Objeto", card="1 obligatorio", values="Objeto {jurisprudencia: entero, actos: entero, doctrina: entero}.",
  example="{jurisprudencia: 14, actos: 2, doctrina: 31}", origin="Derivado por cálculo", method="Cálculo",
  evidence=NA_CALC, extraction="Conteo de referencias doctrinales resueltas a la obra (D7).",
  validation="Solo cuenta referencias en estado 'resuelta a obra' o 'resuelta a unidad'.",
  applicability="Doctrina incorporada al corpus.", prio="P3", mode="B", stage="E7", risk="R3",
  deps="Referencias doctrinales resueltas (D7).", funcs="F04; F12; F03")

F(id="MDJ-D17-018", tech="unidad_es_ratio_vinculante", func="Unidad con regla vinculante",
  dim="D17", profiles="JUR; ADM", unit="Unidad estructural",
  defn="Marca las unidades de un pronunciamiento cuya regla tiene la fuerza calculada para la obra (fundamentos declarados o, si no hay declaración, la ratio identificada).",
  just="La fuerza se predica de la regla de decisión, no del obiter ni de los votos singulares.",
  dtype="Boolean", card="1 obligatorio", values="true / false.",
  example="true", origin="Derivado por cálculo", method="Cálculo", evidence=NA_CALC,
  extraction="Verdadero si la unidad está en fundamentos_declarados_vinculantes o, sin declaración, si es ratio identificada (P2, D5) y la regla del país atribuye fuerza a la ratio.",
  validation="Nunca verdadero para votos singulares ni secciones de antecedentes.",
  prio="P2", mode="B", review="Condicionado", stage="E7", risk="R1",
  deps="fundamentos_declarados_vinculantes; ratio decidendi (D5, P2); fuerza_juridica_pivote.",
  funcs="F08; F15", country_status="Pendiente validación nacional", pending="DEC-25")


# ---------------------------------------------------------------------------
# CATÁLOGOS (CAT-300..CAT-399)
# ---------------------------------------------------------------------------
def V(code, label, definition, **kw):
    d = dict(code=code, label=label, definition=definition)
    d.update(kw)
    return d


SEM = "Semilla – pendiente validación"

CATALOGS = [
    dict(cat_id="CAT-301", cat_name="Facetas de la taxonomía jurídica",
         cat_def="Ejes independientes de la clasificación jurídica (arquitectura v3, C.1).",
         values=[
             V("F1", "Área matriz", "Gran sector del ordenamiento; lista corta y estable."),
             V("F2", "Rama y especialidad dogmática", "Disciplina jurídica; polijerárquica con padre preferente."),
             V("F3", "Especialidad de práctica", "Campo profesional calculado por reglas sobre otras facetas; no lo asigna el modelo."),
             V("F4", "Subespecialidad", "Parte de una especialidad dogmática; hija de F2."),
             V("F5", "Institución jurídica", "Figura con régimen propio; puede ser nacional o pivote."),
             V("F6", "Concepto jurídico", "Noción atómica; vocabulario plano con relaciones asociativas."),
             V("F7", "Tema y subtema", "Asunto concreto o emergente; la faceta más dinámica."),
             V("F8", "Sujetos", "Categorías de sujetos afectados."),
             V("F9", "Sector y actividad económica", "Actividad con código nacional y pivote CIIU Rev. 4; con rol regulado o del caso."),
             V("F10", "Enfoque transversal", "Perspectiva expresa (derechos humanos, género, interculturalidad…)."),
             V("F11", "Función jurídica de la unidad", "Qué hace la unidad en el ordenamiento."),
         ]),
    dict(cat_id="CAT-302", cat_name="Nivel de relevancia temática",
         cat_def="Grado en que un concepto es objeto de la unidad. La mención no es un nivel: se registra como referencia (D7).",
         values=[
             V("principal", "Principal", "Objeto directo de la función jurídica de la unidad; supera las pruebas de objeto, supresión y consulta."),
             V("secundaria", "Secundaria", "Regulado o resuelto de modo instrumental o accesorio; supera la prueba de objeto, no la de supresión."),
             V("contexto", "Contexto", "Describe hechos, sujetos o actividad; ninguna regla o decisión depende de él."),
         ]),
    dict(cat_id="CAT-303", cat_name="Función jurídica de la asignación",
         cat_def="Qué hace la unidad con el concepto asignado.",
         values=[
             V("regula", "Regula", "Establece reglas sobre el concepto."),
             V("define", "Define", "Fija el significado del concepto."),
             V("sanciona", "Sanciona", "Tipifica o impone consecuencias por infracción relacionada con el concepto."),
             V("decide", "Decide", "Resuelve una controversia cuya solución depende del concepto (JUR, ADM)."),
             V("interpreta", "Interpreta", "Fija el sentido o alcance de una disposición sobre el concepto."),
             V("analiza", "Analiza", "Lo estudia como objeto (DOC)."),
             V("procedimental", "Trata procesalmente", "Lo resuelve como cuestión de procedimiento o vía."),
         ]),
    dict(cat_id="CAT-304", cat_name="Pruebas de relevancia temática",
         cat_def="Pruebas que justifican el nivel de relevancia (arquitectura v3, C.2).",
         values=[
             V("objeto", "Prueba de objeto", "¿La regla, decisión o análisis recae sobre el concepto?"),
             V("supresion", "Prueba de supresión", "Sin el concepto, ¿pierde la unidad su efecto principal?"),
             V("consulta", "Prueba de consulta", "¿Un especialista en el concepto necesitaría la unidad como fuente directa?"),
         ]),
    dict(cat_id="CAT-305", cat_name="Estado de la asignación frente a cambios de taxonomía",
         cat_def="Efecto de las operaciones del ciclo de vida del concepto sobre la asignación.",
         values=[
             V("vigente", "Vigente", "El concepto asignado está activo."),
             V("remapeada_por_fusion", "Remapeada por fusión", "El concepto se fusionó; la asignación apunta al sucesor de forma automática."),
             V("pendiente_reclasificacion", "Pendiente de reclasificación", "El concepto se dividió; requiere reclasificación por fragmento (clase C)."),
             V("historica", "Histórica", "El concepto fue desactivado sin sucesor; se conserva para trazabilidad."),
             V("revocada", "Revocada", "Rechazada en revisión humana o invalidada por su ejecución."),
         ]),
    dict(cat_id="CAT-306", cat_name="Ámbito del concepto",
         cat_def="Alcance jurídico-territorial del concepto de la taxonomía.",
         values=[
             V("pivote", "Pivote", "Clase conceptual abstracta definida por Juztina por su función; no es una institución de ningún país."),
             V("multinacional", "Multinacional", "Concepto con fuente común aplicable en varios países (p. ej., norma comunitaria andina)."),
             V("nacional", "Nacional", "Concepto propio de un ordenamiento."),
         ]),
    dict(cat_id="CAT-307", cat_name="Estado del ciclo de vida del concepto",
         cat_def="Estados de un concepto de la taxonomía; ningún concepto se borra (C.8).",
         values=[
             V("propuesto", "Propuesto", "En evaluación; no admite asignaciones automáticas."),
             V("activo", "Activo", "Aprobado; admite asignaciones."),
             V("fusionado", "Fusionado", "Absorbido por otro concepto; redirige a su sucesor."),
             V("dividido", "Dividido", "Reemplazado por dos o más conceptos; asignaciones pendientes de reclasificación."),
             V("desactivado", "Desactivado", "Retirado del uso; se conserva con sucesor si existe."),
         ]),
    dict(cat_id="CAT-308", cat_name="Rol del sector",
         cat_def="Relación de la actividad económica con la unidad (faceta F9).",
         values=[
             V("sector_regulado", "Sector regulado", "La unidad establece reglas, condiciones o sanciones para la actividad."),
             V("sector_del_caso", "Sector del caso", "La actividad describe al sujeto o los hechos; la decisión no depende de ella."),
         ]),
    dict(cat_id="CAT-309", cat_name="Sectores regulados (semilla)",
         cat_def="Regímenes regulatorios sectoriales propios de Juztina, vinculados a CIIU y a reguladores de cada país. Semilla para validación.",
         values=[V(c, l, d, status=SEM) for c, l, d in [
             ("telecomunicaciones", "Telecomunicaciones", "Servicios de telecomunicaciones y espectro."),
             ("energia_electrica", "Energía eléctrica", "Generación, transmisión, distribución y comercialización eléctrica."),
             ("hidrocarburos", "Hidrocarburos", "Exploración, explotación, transporte y comercialización de hidrocarburos."),
             ("mineria", "Minería", "Concesiones, explotación y cierre de minas."),
             ("agua_saneamiento", "Agua y saneamiento", "Servicios de agua potable y alcantarillado."),
             ("sistema_financiero", "Sistema financiero", "Banca y entidades de crédito supervisadas."),
             ("seguros", "Seguros", "Actividad aseguradora y reaseguradora."),
             ("pensiones", "Pensiones", "Sistemas privados y públicos de pensiones."),
             ("mercado_valores", "Mercado de valores", "Emisores, intermediarios y oferta pública de valores."),
             ("salud", "Salud", "Prestadores y aseguradores de salud."),
             ("farmaceutico", "Productos farmacéuticos y sanitarios", "Registro, comercialización y vigilancia sanitaria."),
             ("transporte", "Transporte", "Transporte terrestre, aéreo, marítimo e infraestructura."),
             ("educacion", "Educación", "Prestación de servicios educativos regulados."),
             ("datos_digital", "Datos y servicios digitales", "Plataformas, comercio electrónico y protección de datos sectorial."),
         ]]),
    dict(cat_id="CAT-310", cat_name="Formación del órgano decisor",
         cat_def="Composición con la que se adopta la resolución.",
         values=[
             V("pleno", "Pleno", "Totalidad de los miembros del tribunal."),
             V("sala_plena", "Sala plena", "Reunión de las salas o secciones como un solo cuerpo, según denominación nacional."),
             V("sala_seccion", "Sala o sección", "Una sala o sección del tribunal."),
             V("sala_especial", "Sala especial o de unificación", "Formación especial prevista para unificar o resolver contradicciones."),
             V("unipersonal", "Juez o autoridad unipersonal", "Decisión de un solo juez o funcionario."),
             V("tribunal_administrativo_sala_plena", "Tribunal administrativo en sala plena", "Formación plenaria de un tribunal administrativo."),
             V("tribunal_administrativo_sala", "Tribunal administrativo en sala", "Una sala de un tribunal administrativo."),
             V("no_consta", "No consta", "El documento no permite determinar la formación."),
         ]),
    dict(cat_id="CAT-311", cat_name="Categoría de precedente original por país (semilla)",
         cat_def="Denominaciones nacionales de categorías jurisprudenciales o de precedente. Ilustrativas: ninguna validada (DEC-25).",
         values=[
             V("pe_precedente_constitucional_vinculante", "Precedente constitucional vinculante", "Categoría del Tribunal Constitucional peruano.", country="PE", status=SEM),
             V("pe_precedente_judicial_casatorio", "Precedente o doctrina jurisprudencial en casación", "Categorías de la Corte Suprema peruana; denominación a validar.", country="PE", status=SEM),
             V("co_sentencia_unificacion", "Sentencia de unificación", "Sentencias SU de la Corte Constitucional y de unificación de otras altas cortes.", country="CO", status=SEM),
             V("mx_jurisprudencia_reiteracion", "Jurisprudencia por reiteración", "Categoría del sistema mexicano.", country="MX", status=SEM),
             V("mx_jurisprudencia_contradiccion", "Jurisprudencia por contradicción de criterios", "Categoría del sistema mexicano.", country="MX", status=SEM),
             V("mx_precedente_obligatorio", "Precedente obligatorio", "Introducido por la reforma de 2021; efectos posteriores a la reforma de 2024 a validar.", country="MX", status=SEM),
             V("mx_tesis_aislada", "Tesis aislada", "Criterio sin fuerza obligatoria por sí mismo.", country="MX", status=SEM),
             V("ec_precedente_cc", "Precedente de la Corte Constitucional", "Precedentes obligatorios de la Corte Constitucional ecuatoriana.", country="EC", status=SEM),
             V("ec_jurisprudencia_vinculante_cnj", "Jurisprudencia vinculante de la Corte Nacional", "Por reiteración de fallos; requisitos a validar.", country="EC", status=SEM),
             V("bo_sentencia_constitucional_vinculante", "Sentencia constitucional plurinacional", "Carácter vinculante de las sentencias del TCP.", country="BO", status=SEM),
             V("ar_fallo_plenario", "Fallo plenario", "Vigencia y alcance a validar.", country="AR", status=SEM),
             V("ar_doctrina_csjn", "Doctrina de la Corte Suprema", "Seguimiento esperado de la doctrina de la CSJN; fuerza a validar.", country="AR", status=SEM),
             V("cl_sin_categoria_formal", "Sin categoría formal de precedente obligatorio", "Chile no tiene sistema formal de precedente obligatorio; a validar.", country="CL", status=SEM),
             V("adm_precedente_observancia_obligatoria", "Precedente administrativo de observancia obligatoria", "Criterios de tribunales administrativos declarados obligatorios; existencia por país a validar.", country="Varios", status=SEM),
         ]),
    dict(cat_id="CAT-312", cat_name="Fuerza jurídica pivote",
         cat_def="Categorías comunes de fuerza jurídica de pronunciamientos; resultado de reglas por país (D17).",
         values=[
             V("vinculante_general", "Vinculante general", "Obliga a todos los órganos y personas (efecto erga omnes)."),
             V("vinculante_organos_inferiores", "Vinculante para órganos inferiores", "Obliga a los órganos jurisdiccionales de la misma jurisdicción o inferiores."),
             V("vinculante_administracion", "Vinculante para la administración", "Obliga a entidades administrativas."),
             V("inter_partes", "Inter partes", "Efectos solo entre las partes del proceso."),
             V("persuasiva", "Persuasiva", "Sin obligatoriedad formal; valor argumentativo."),
             V("no_vinculante", "No vinculante", "Declaradamente sin fuerza obligatoria (p. ej., obiter, voto singular)."),
             V("indeterminada", "Indeterminada", "No hay regla validada o insumos suficientes para concluir."),
         ]),
    dict(cat_id="CAT-313", cat_name="Estado del precedente o criterio",
         cat_def="Situación del criterio según relaciones posteriores.",
         values=[
             V("vigente", "Vigente", "No hay relación posterior que lo modifique."),
             V("reiterado", "Reiterado", "Seguido o reiterado por pronunciamientos posteriores."),
             V("modificado", "Modificado", "Ajustado o precisado por un pronunciamiento posterior."),
             V("superado", "Superado", "Abandonado expresamente por un pronunciamiento con fuerza suficiente."),
             V("interrumpido", "Interrumpido", "Interrupción formal según el ordenamiento (p. ej., MX); a validar."),
             V("indeterminado", "Indeterminado", "Sin información o reglas suficientes."),
         ]),
    dict(cat_id="CAT-314", cat_name="Fuerza del pronunciamiento interpretativo administrativo",
         cat_def="Efectos de conceptos, informes, oficios, circulares, criterios normativos y dictámenes; por país y tipo (DEC-26).",
         values=[
             V("vinculante_administracion_emisora", "Vinculante para la administración emisora", "Obliga a la entidad que lo emite."),
             V("vinculante_administracion_general", "Vinculante para la administración en general", "Obliga a otras entidades públicas."),
             V("vinculante_administrados", "Vinculante para los administrados", "Oponible a los particulares."),
             V("orientativo", "Orientativo", "Criterio de orientación sin obligatoriedad."),
             V("indeterminada", "Indeterminada", "Regla de país no validada o insumos insuficientes."),
         ]),
    dict(cat_id="CAT-315", cat_name="Índices y bases de indexación doctrinal",
         cat_def="Índices bibliográficos usados como señal objetiva de autoridad doctrinal.",
         values=[
             V("scopus", "Scopus", "Base bibliográfica de Elsevier."),
             V("wos", "Web of Science", "Colecciones de Clarivate (incluye ESCI)."),
             V("scielo", "SciELO", "Biblioteca científica electrónica en línea, colecciones nacionales."),
             V("latindex", "Latindex", "Sistema regional de información para revistas; distinguir directorio y catálogo."),
             V("dialnet", "Dialnet", "Portal bibliográfico de la Universidad de La Rioja."),
             V("doaj", "DOAJ", "Directory of Open Access Journals."),
             V("redalyc", "Redalyc", "Red de revistas científicas de América Latina."),
             V("miar", "MIAR", "Matriz de información para el análisis de revistas."),
             V("ninguno", "Sin indexación conocida", "No se encontró indexación."),
         ]),
    dict(cat_id="CAT-316", cat_name="Tipo de revisión por pares",
         cat_def="Modalidad de evaluación editorial de una obra doctrinal.",
         values=[
             V("doble_ciego", "Doble ciego", "Autor y evaluadores anónimos entre sí."),
             V("simple_ciego", "Simple ciego", "Evaluadores anónimos para el autor."),
             V("abierta", "Abierta", "Identidades conocidas."),
             V("editorial", "Editorial", "Revisión solo por el comité o editor."),
             V("sin_revision", "Sin revisión", "Publicación sin evaluación."),
             V("no_consta", "No consta", "No hay información."),
         ]),
    dict(cat_id="CAT-317", cat_name="Nivel académico o de publicación",
         cat_def="Nivel de la obra doctrinal (señal objetiva de autoridad).",
         values=[
             V("investigacion_arbitrada", "Investigación arbitrada", "Artículo o libro sometido a revisión académica."),
             V("tesis_doctoral", "Tesis doctoral", "Trabajo de doctorado."),
             V("tesis_maestria", "Tesis de maestría", "Trabajo de maestría o posgrado."),
             V("trabajo_pregrado", "Trabajo de pregrado", "Tesis o monografía de grado."),
             V("comentario_profesional", "Comentario profesional", "Análisis de práctica profesional o de jurisprudencia."),
             V("divulgacion", "Divulgación", "Publicación para público general."),
             V("material_docente", "Material docente", "Manuales y materiales de enseñanza."),
             V("no_consta", "No consta", "No hay información."),
         ]),
    dict(cat_id="CAT-318", cat_name="Áreas matrices (semilla de la faceta F1)",
         cat_def="Lista corta y estable de áreas matrices propuesta en la arquitectura; sujeta a validación del comité taxonómico.",
         values=[V(c, l, d, status=SEM) for c, l, d in [
             ("constitucional", "Constitucional", "Organización del Estado, derechos fundamentales y garantías."),
             ("administrativo_publico_economico", "Administrativo y Público Económico", "Administración pública, regulación, contratación pública, competencia."),
             ("civil_patrimonial", "Civil y Patrimonial", "Personas, familia, obligaciones, contratos, bienes, sucesiones."),
             ("mercantil_empresarial", "Mercantil y Empresarial", "Sociedades, comercio, consumidor, propiedad industrial."),
             ("laboral_seguridad_social", "Laboral y Seguridad Social", "Trabajo individual y colectivo, seguridad social."),
             ("tributario_financiero_publico", "Tributario y Financiero Público", "Tributos, aduanas, presupuesto y finanzas públicas."),
             ("penal", "Penal", "Delitos, penas y ejecución penal."),
             ("procesal", "Procesal", "Procesos judiciales y sus garantías."),
             ("internacional", "Internacional", "Derecho internacional público y privado, inversiones, comercio exterior."),
             ("ambiental_recursos_naturales", "Ambiental y Recursos Naturales", "Ambiente, recursos naturales y su aprovechamiento."),
         ]]),
    dict(cat_id="CAT-319", cat_name="Tipo de etiqueta alternativa",
         cat_def="Clase de denominación alternativa de un mismo concepto (equivalencia terminológica).",
         values=[
             V("sinonimo", "Sinónimo", "Otra denominación del mismo concepto."),
             V("sigla", "Sigla o acrónimo", "Forma abreviada."),
             V("variante_nacional", "Variante nacional", "Denominación usada en un país para el mismo concepto del mismo régimen."),
             V("termino_historico", "Término histórico", "Denominación anterior en desuso."),
         ]),
    dict(cat_id="CAT-320", cat_name="Enfoques transversales (semilla)",
         cat_def="Valores iniciales de la faceta F10; requieren invocación expresa en la unidad.",
         values=[V(c, l, d, status=SEM) for c, l, d in [
             ("derechos_humanos", "Derechos humanos", "Aplicación expresa de estándares de derechos humanos o control de convencionalidad."),
             ("genero", "Género", "Enfoque de género invocado o aplicado."),
             ("interculturalidad", "Interculturalidad", "Enfoque intercultural o de pueblos indígenas."),
             ("interes_superior_nino", "Interés superior del niño", "Aplicación expresa del principio."),
             ("anticorrupcion", "Anticorrupción", "Integridad pública y lucha contra la corrupción."),
             ("sostenibilidad", "Sostenibilidad y ESG", "Criterios ambientales, sociales y de gobernanza."),
             ("discapacidad", "Discapacidad", "Enfoque de derechos de personas con discapacidad."),
         ]]),
    dict(cat_id="CAT-321", cat_name="Función jurídica de la unidad (faceta F11)",
         cat_def="Qué hace la unidad en el ordenamiento, con independencia del concepto (distinto de CAT-303).",
         values=[
             V("sancionadora", "Sancionadora", "Tipifica infracciones o impone sanciones."),
             V("tributaria", "Tributaria", "Crea, modifica o regula tributos."),
             V("habilitante", "Habilitante", "Otorga licencias, permisos, autorizaciones o concesiones."),
             V("organizativa", "Organizativa", "Crea o estructura órganos y competencias."),
             V("procedimental", "Procedimental", "Regula trámites y procedimientos."),
             V("protectora_derechos", "Protectora de derechos", "Reconoce o tutela derechos."),
             V("definitoria", "Definitoria", "Establece definiciones."),
             V("interpretativa", "Interpretativa", "Fija el sentido de otras disposiciones."),
             V("prestacional", "Prestacional", "Establece prestaciones, beneficios o subsidios."),
         ]),
    dict(cat_id="CAT-322", cat_name="Destinatarios de la vinculación",
         cat_def="Sujetos obligados por un pronunciamiento con fuerza jurídica.",
         values=[
             V("todos", "Todos", "Todos los poderes públicos y particulares."),
             V("todos_jueces", "Todos los jueces", "Toda la judicatura."),
             V("organos_inferiores_jurisdiccion", "Órganos inferiores de la jurisdicción", "Órganos de la misma jurisdicción de menor jerarquía."),
             V("propio_tribunal", "El propio tribunal", "Autovinculación del órgano emisor."),
             V("administracion", "Administración pública", "Entidades administrativas."),
             V("administrados", "Administrados", "Particulares ante la administración."),
             V("partes", "Partes del proceso", "Solo las partes."),
         ]),
    dict(cat_id="CAT-323", cat_name="Sistemas de clasificación de actividades económicas",
         cat_def="Pivote internacional y sistemas nacionales; vigencia y versión por país a validar (DEC-28).",
         values=[
             V("ciiu_rev4", "CIIU Rev. 4", "Clasificación Industrial Internacional Uniforme, Rev. 4 (Naciones Unidas). Pivote.", status="Referencia internacional"),
             V("pe_ciiu", "Adaptación nacional CIIU – Perú", "Sistema nacional vigente a confirmar.", country="PE", status=SEM),
             V("co_ciiu_ac", "CIIU Rev. 4 adaptada para Colombia", "Sistema nacional vigente a confirmar.", country="CO", status=SEM),
             V("ar_clanae", "ClaNAE (Argentina)", "Clasificador nacional de actividades económicas; versión a confirmar.", country="AR", status=SEM),
             V("cl_ciiu_cl", "CIIU4.CL (Chile)", "Adaptación chilena; versión a confirmar.", country="CL", status=SEM),
             V("ec_ciiu", "CIIU – Ecuador", "Sistema nacional vigente a confirmar.", country="EC", status=SEM),
             V("bo_caeb", "CAEB (Bolivia)", "Clasificador de actividades económicas de Bolivia; versión a confirmar.", country="BO", status=SEM),
             V("mx_scian", "SCIAN (México)", "Sistema de Clasificación Industrial de América del Norte; requiere tablas de correspondencia con CIIU.", country="MX", status=SEM),
         ]),
]
