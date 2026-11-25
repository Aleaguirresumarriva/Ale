"""
Taxonomía de etiquetas jurídicas de Juztina — versión semilla 0.1 (pendiente de validación).

Sirve para etiquetar unidades estructurales y obras (campos MDJ-D06-021, -022, -023) y, a partir de esas
etiquetas, armar el corpus de cada especialista (CAT-331, campo MDJ-OPE-009).

Niveles:
  1 Área principal      (faceta F2, nivel superior)   IDs CON-F2-Axx
  2 Especialidad        (F2 dogmática o F3 sectorial)  IDs CON-F2-Exxx / CON-F3-Exxx
  3 Subespecialidad     (faceta F4)                    IDs CON-F4-Sxxx
Los IDs son persistentes: no cambian si la etiqueta se renombra, se mueve o cambia de tipo.
Un documento puede llevar muchas etiquetas a la vez (sin tope), con relevancia principal o secundaria.
"""

GA = {  # gran área (faceta F1, CAT-318)
    "CONS": "constitucional", "ADM": "administrativo_publico_economico", "CIV": "civil_patrimonial",
    "MER": "mercantil_empresarial", "LAB": "laboral_seguridad_social", "TRI": "tributario_financiero_publico",
    "PEN": "penal", "PRO": "procesal", "INT": "internacional", "AMB": "ambiental_recursos_naturales",
}

ROWS = []

def A(i, nombre, ga, incluye, excluye, indicadores, sinonimos="—", actual="—"):
    ROWS.append(dict(id=f"CON-F2-A{i:02d}", nivel=1, tipo="Área principal", nombre=nombre, padre="—", otros="—",
                     ga=GA[ga], incluye=incluye, excluye=excluye, indicadores=indicadores, sinonimos=sinonimos,
                     sector="—", regla="—", actual=actual))

def E(i, area, nombre, incluye, otros="—", sector="—", regla="—", sectorial=False, excluye="—", indicadores=None, sinonimos="—", actual="—"):
    pref = "CON-F3-E" if sectorial else "CON-F2-E"
    ROWS.append(dict(id=f"{pref}{i:03d}", nivel=2, tipo="Especialidad sectorial o de práctica" if sectorial else "Especialidad",
                     nombre=nombre, padre=f"CON-F2-A{area:02d}", otros=otros, ga=None, incluye=incluye, excluye=excluye,
                     indicadores=indicadores or "La unidad regula, decide o analiza: " + incluye[0].lower() + incluye[1:],
                     sinonimos=sinonimos, sector=sector, regla=regla, actual=actual))

def S(i, padre, nombre, incluye, sinonimos="—", actual="—"):
    ROWS.append(dict(id=f"CON-F4-S{i:03d}", nivel=3, tipo="Subespecialidad", nombre=nombre, padre=padre, otros="—",
                     ga=None, incluye=incluye, excluye="—",
                     indicadores="Hereda los criterios de su especialidad; se asigna cuando la unidad trata específicamente: " + incluye[0].lower() + incluye[1:],
                     sinonimos=sinonimos, sector="—", regla="—", actual=actual))

# =============================================================================== NIVEL 1: ÁREAS PRINCIPALES
A(1, "Constitucional", "CONS", "Organización del Estado, división de poderes, derechos fundamentales en su dimensión constitucional, control de constitucionalidad y procesos constitucionales.",
  "Aplicación de derechos fundamentales resuelta solo con normas legales de una materia (va a esa materia, con Constitucional como secundaria si se invoca la Constitución de forma decisiva).",
  "Interpretación de la Constitución; control abstracto o concreto; demandas de amparo, tutela, hábeas corpus, acción de protección; organización de poderes del Estado.")
A(2, "Derechos Humanos", "CONS", "Estándares internacionales y nacionales de derechos humanos, sistema interamericano, control de convencionalidad, grupos en situación de vulnerabilidad.",
  "Menciones genéricas a 'derechos' sin análisis de estándares de derechos humanos.",
  "Cita o aplicación de tratados de derechos humanos, decisiones de la Corte IDH o de la CIDH, control de convencionalidad, reparaciones.")
A(3, "Administrativo", "ADM", "Organización y actuación de la Administración pública, acto y procedimiento administrativo, potestad sancionadora general, servicio civil, responsabilidad del Estado, bienes públicos.",
  "Procedimientos administrativos de una materia con área propia (tributario, aduanero, laboral inspectivo, consumidor): van a esa área, con Administrativo como secundaria si se discute el procedimiento.",
  "Validez, nulidad o eficacia de actos administrativos; silencio administrativo; recursos administrativos; competencias de entidades; régimen de funcionarios.")
A(4, "Contratación Pública", "ADM", "Contratación del Estado: planificación, procedimientos de selección, ejecución contractual, controversias y sanciones a proveedores; asociaciones público-privadas y concesiones de obra.",
  "Contratos entre privados (Contratos).", "Licitaciones, concursos, adjudicaciones, adicionales de obra, penalidades, impedimentos para contratar, tribunales o salas de contrataciones.",
  sinonimos="Compras públicas; contrataciones del Estado; adquisiciones públicas")
A(5, "Regulatorio y Servicios Públicos", "ADM", "Regulación económica de sectores y servicios públicos: tarifas, títulos habilitantes, calidad del servicio, supervisión y sanción de organismos reguladores.",
  "Recursos naturales extractivos (área 7) y sistema financiero (área 22), que tienen área propia.",
  "Organismos reguladores; tarifas; concesiones de servicios públicos; obligaciones de operadores; reglamentos sectoriales.")
A(6, "Ambiental", "AMB", "Protección del ambiente: evaluación de impacto, fiscalización y sanción ambiental, responsabilidad por daño ambiental, áreas protegidas, biodiversidad, residuos, cambio climático.",
  "Aprovechamiento económico de recursos naturales sin componente de protección ambiental (área 7).",
  "Estudios o certificaciones ambientales, límites máximos permisibles, estándares de calidad ambiental, daño ambiental, fiscalizador ambiental, consulta y participación ambiental.")
A(7, "Recursos Naturales y Energía", "AMB", "Régimen jurídico del aprovechamiento de recursos naturales y de la energía: minería, hidrocarburos, electricidad, agua como recurso, forestal, pesca.",
  "Protección ambiental de esas actividades (Ambiental, como etiqueta adicional).",
  "Concesiones, derechos de aprovechamiento, regalías, contratos de exploración o explotación, títulos mineros o petroleros, generación y transmisión eléctrica.")
A(8, "Civil", "CIV", "Personas, acto jurídico, obligaciones, derechos reales, responsabilidad civil extracontractual, prescripción y caducidad civil, sucesiones.",
  "Familia (área 9) y contratos típicos o atípicos en particular (área 10).",
  "Capacidad, nulidad o anulabilidad del acto jurídico, propiedad, posesión, usucapión, garantías reales, indemnización por daños, herencia, testamentos.")
A(9, "Familia", "CIV", "Matrimonio, uniones de hecho, divorcio, filiación, alimentos, tenencia y régimen de visitas, adopción, violencia familiar en su dimensión de protección, niñez y adolescencia.",
  "Sucesiones (Civil) y delitos de violencia (Penal, con Familia como secundaria si se dictan medidas de protección familiar).",
  "Pensión de alimentos, tenencia o custodia, patria potestad, filiación, divorcio, régimen patrimonial del matrimonio, interés superior del niño.",
  sinonimos="Derecho de Familia y Niñez")
A(10, "Contratos", "CIV", "Formación, interpretación, ejecución, incumplimiento y resolución de contratos entre privados, civiles y comerciales, y contratos típicos o atípicos.",
  "Contratos con el Estado (Contratación Pública) y contratos de trabajo (Laboral), de seguro (Seguros) o bancarios (Financiero), salvo que se analice la teoría general del contrato.",
  "Cláusulas, incumplimiento contractual, resolución, penalidades, compraventa, arrendamiento, mutuo, obra, distribución, franquicia, licencias.")
A(11, "Inmobiliario, Urbanístico y Registral", "CIV", "Operaciones inmobiliarias, propiedad horizontal, habilitaciones urbanas y edificación, zonificación, registros públicos y función notarial.",
  "Derechos reales en abstracto sin componente inmobiliario o registral específico (Civil).",
  "Inscripción registral, partidas, títulos, licencias de edificación, zonificación, condominios, notarios, tasación.")
A(12, "Societario y Corporativo", "MER", "Sociedades y personas jurídicas de fines lucrativos: constitución, órganos, acciones, gobierno corporativo, reorganizaciones, fusiones y adquisiciones.",
  "Insolvencia (Mercantil) y valores de oferta pública (Financiero), salvo que se analice el régimen societario.",
  "Juntas de accionistas, directorio, estatutos, aumento de capital, transferencia de acciones, fusión, escisión, responsabilidad de administradores.")
A(13, "Mercantil y Comercial", "MER", "Actos de comercio, empresario, títulos valores, insolvencia y reestructuración, contratos mercantiles de distribución y transporte de mercancías, comercio electrónico entre empresas.",
  "Sociedades (Societario) y relaciones con consumidores (Consumidor).",
  "Letras, pagarés, cheques, protestos, concurso o quiebra, acreedores, reestructuración patrimonial, registro mercantil.")
A(14, "Consumidor", "MER", "Protección del consumidor: idoneidad, información, publicidad frente al consumidor, cláusulas abusivas, libro de reclamaciones, servicios financieros a consumidores, sanción a proveedores.",
  "Relaciones entre empresas sin consumidor final (Contratos o Mercantil).",
  "Consumidor o usuario final, proveedor, reclamo, deber de idoneidad, garantías, publicidad engañosa, agencia o autoridad de protección al consumidor.",
  actual="Especialista Consumidor (en producción)")
A(15, "Competencia", "MER", "Libre competencia (conductas anticompetitivas y control de concentraciones), competencia desleal, publicidad entre competidores, dumping y subsidios.",
  "Protección del consumidor frente a la publicidad (Consumidor).",
  "Abuso de posición de dominio, prácticas colusorias, carteles, control de fusiones, actos de engaño o confusión entre competidores, autoridad de competencia.",
  sinonimos="Antimonopolio; libre competencia; defensa de la competencia")
A(16, "Propiedad Intelectual", "MER", "Derecho de autor y derechos conexos, marcas y signos distintivos, patentes, diseños, secretos empresariales, obtenciones vegetales, denominaciones de origen.",
  "Tecnología y datos sin componente de exclusividad intelectual (área 17).",
  "Registro u oposición de marcas, infracción de derechos de autor, patentes, licencias de uso de intangibles, sociedades de gestión colectiva.",
  sinonimos="Propiedad industrial y derechos de autor")
A(17, "Tecnología, Datos y Digital", "MER", "Protección de datos personales, comercio y firma electrónicos, ciberseguridad, plataformas digitales, inteligencia artificial, gobierno digital.",
  "Telecomunicaciones como servicio público (Regulatorio).",
  "Tratamiento de datos personales, bancos de datos, consentimiento, firmas digitales, contratos electrónicos, plataformas, algoritmos, delitos informáticos (con Penal).")
A(18, "Laboral", "LAB", "Relaciones de trabajo individuales y colectivas en el sector privado y, cuando corresponda, en el público; inspección y sanción laboral.",
  "Pensiones y prestaciones de seguridad social (área 19); servicio civil sin componente laboral (Administrativo, con Laboral si se discute la relación de trabajo).",
  "Contrato de trabajo, despido, remuneraciones, beneficios sociales, jornada, sindicatos, negociación colectiva, huelga, inspección del trabajo, autoridad laboral.",
  sinonimos="Derecho del Trabajo", actual="Especialista Laboral (en producción)")
A(19, "Seguridad Social y Pensiones", "LAB", "Sistemas públicos y privados de pensiones, salud contributiva, riesgos del trabajo y prestaciones de seguridad social.",
  "Seguros privados no previsionales (Seguros).",
  "Jubilación, pensión de invalidez o sobrevivencia, aportes, administradoras de fondos de pensiones, prestaciones de salud contributivas, accidentes de trabajo y enfermedades profesionales.",
  sinonimos="Previsional")
A(20, "Tributario", "TRI", "Tributos nacionales y subnacionales: obligación tributaria, impuestos, contribuciones, tasas, procedimientos de fiscalización, cobranza y sanción tributaria, tributación internacional.",
  "Tributos aduaneros sobre importación y exportación (Aduanero) y presupuesto público sin componente tributario (Administrativo).",
  "Impuesto a la renta, IVA o IGV, impuestos municipales, determinación, fiscalización, multas tributarias, administración tributaria, tribunal fiscal, convenios de doble imposición.",
  sinonimos="Fiscal; impositivo", actual="Especialista Tributario (en producción)")
A(21, "Aduanero y Comercio Exterior", "TRI", "Régimen aduanero, tributos a la importación y exportación, regímenes aduaneros, infracciones y delitos aduaneros, reglas de origen y acuerdos comerciales.",
  "Inversión extranjera y arbitraje de inversiones (Internacional).",
  "Despacho aduanero, aranceles, valoración, clasificación arancelaria, drawback, contrabando, certificados de origen, tratados de libre comercio.")
A(22, "Financiero, Bancario y Mercado de Valores", "MER", "Sistema financiero, banca, crédito, medios de pago, fintech, mercado de valores, fondos de inversión, prevención del lavado de activos en entidades financieras.",
  "Relación con el consumidor financiero en su dimensión de protección (Consumidor, como etiqueta adicional).",
  "Entidades supervisadas, superintendencia o comisión del mercado, créditos, garantías financieras, emisión de valores, intermediarios, encaje, criptoactivos.")
A(23, "Seguros", "MER", "Contrato de seguro, reaseguro, intermediarios, supervisión de aseguradoras y siniestros.",
  "Seguros previsionales y de salud contributiva (Seguridad Social).",
  "Pólizas, siniestros, cobertura, indemnización por seguro, corredores, supervisión de aseguradoras.")
A(24, "Penal", "PEN", "Delitos y penas: parte general, delitos en particular, ejecución penal, responsabilidad penal de personas jurídicas.",
  "Proceso penal en sus aspectos procedimentales (Procesal, Procesal Penal), salvo que se analice el tipo penal.",
  "Tipicidad, antijuridicidad, culpabilidad, delitos específicos, penas, reparación civil derivada del delito, prescripción de la acción penal.")
A(25, "Procesal", "PRO", "Reglas de los procesos judiciales: competencia, actos procesales, prueba, medios impugnatorios, medidas cautelares, ejecución, en cualquier vía.",
  "Procedimientos administrativos (Administrativo o el área de su materia).",
  "Admisibilidad, competencia, notificación, prueba, apelación, casación, cautelares, ejecución de sentencias, plazos procesales.")
A(26, "Arbitraje y Medios Alternativos", "PRO", "Arbitraje comercial y de inversiones en su aspecto procesal, conciliación, mediación, anulación y ejecución de laudos.",
  "Fondo de la controversia arbitral (área de la materia, como etiqueta adicional).",
  "Convenio arbitral, tribunal arbitral, laudo, anulación de laudo, conciliación extrajudicial, centros de arbitraje, reconocimiento de laudos extranjeros.",
  sinonimos="MASC; métodos alternativos de solución de conflictos")
A(27, "Internacional", "INT", "Derecho internacional público, derecho internacional privado, tratados, inversiones extranjeras, integración regional y migraciones internacionales.",
  "Derechos humanos (área 2) y comercio exterior aduanero (área 21).",
  "Tratados, conflicto de leyes, ley aplicable, reconocimiento de sentencias extranjeras, inversión extranjera, Comunidad Andina, Mercosur, organismos internacionales.")

# =============================================================================== NIVEL 2: ESPECIALIDADES
# Constitucional (1)
E(1, 1, "Procesos constitucionales", "Amparo, tutela, hábeas corpus, hábeas data, cumplimiento, acción de protección y demás garantías jurisdiccionales.", otros="CON-F2-A25")
E(2, 1, "Control de constitucionalidad", "Control abstracto y concreto de normas, efectos de las sentencias constitucionales, control difuso.")
E(3, 1, "Organización del Estado y división de poderes", "Poderes del Estado, órganos constitucionales autónomos, conflictos de competencia.")
E(4, 1, "Electoral y parlamentario", "Organismos y procesos electorales, partidos políticos, procedimiento parlamentario, control político.")
E(5, 1, "Descentralización y autonomías territoriales", "Distribución de competencias entre niveles de gobierno, autonomías regionales, departamentales o indígenas.", otros="CON-F2-A03")
# Derechos humanos (2)
E(6, 2, "Sistema interamericano", "Decisiones y procedimientos ante la Comisión y la Corte Interamericana, control de convencionalidad.")
E(7, 2, "Pueblos indígenas y consulta previa", "Derechos de pueblos indígenas, consulta previa, territorios y justicia indígena.", otros="CON-F2-A01; CON-F2-A07")
E(8, 2, "Igualdad y no discriminación", "Discriminación por género, origen, discapacidad, orientación sexual u otros motivos; acciones afirmativas.")
E(9, 2, "Niñez, adolescencia y grupos vulnerables", "Derechos de niñas, niños, adolescentes, personas mayores y con discapacidad.", otros="CON-F2-A09")
# Administrativo (3)
E(10, 3, "Acto y procedimiento administrativo", "Validez, eficacia, nulidad, notificación y recursos en el procedimiento administrativo general.")
E(11, 3, "Sancionador administrativo", "Principios y procedimiento sancionador general, graduación de sanciones, prescripción de la potestad sancionadora.")
E(12, 3, "Servicio civil y función pública", "Régimen de servidores públicos, carrera administrativa, régimen disciplinario.", otros="CON-F2-A18")
E(13, 3, "Responsabilidad del Estado", "Responsabilidad patrimonial de la Administración y de funcionarios.")
E(14, 3, "Bienes y dominio público", "Bienes estatales, expropiación, dominio público y patrimonio del Estado.")
E(15, 3, "Control gubernamental y anticorrupción", "Contraloría, auditoría, responsabilidad administrativa funcional, integridad pública.")
E(16, 3, "Municipal y gobiernos subnacionales", "Competencias, ordenanzas y actuación de gobiernos regionales y locales.")
E(17, 3, "Migratorio", "Ingreso, permanencia, residencia, expulsión de extranjeros y nacionalidad.", otros="CON-F2-A27")
E(18, 3, "Contencioso administrativo", "Impugnación judicial de actuaciones de la Administración.", otros="CON-F2-A25")
# Contratación pública (4)
E(19, 4, "Procedimientos de selección", "Planificación, licitaciones, concursos, adjudicación, impugnaciones en la selección.")
E(20, 4, "Ejecución contractual pública", "Adicionales, ampliaciones de plazo, penalidades, resolución de contratos estatales.")
E(21, 4, "Asociaciones público-privadas y concesiones", "APP, concesiones de infraestructura, iniciativas privadas, obras por impuestos.", otros="CON-F2-A05")
E(22, 4, "Sanciones a proveedores del Estado", "Infracciones, inhabilitaciones y registro de proveedores.")
# Regulatorio (5)
E(23, 5, "Telecomunicaciones", "Servicios de telecomunicaciones, espectro, interconexión, derechos de usuarios de telecomunicaciones.", sectorial=True, sector="CAT-309 telecomunicaciones", regla="Sector regulado = telecomunicaciones ∧ área ∈ {Regulatorio, Administrativo, Consumidor, Competencia}")
E(24, 5, "Transporte y logística", "Transporte terrestre, aéreo, marítimo, ferroviario, puertos, aeropuertos y logística.", sectorial=True, sector="CAT-309 transporte", regla="Sector regulado = transporte ∧ área ∈ {Regulatorio, Administrativo, Contratación Pública, Consumidor}")
E(25, 5, "Infraestructura y construcción", "Obras de infraestructura, construcción, contratos de obra pública y privada a gran escala.", sectorial=True, otros="CON-F2-A04; CON-F2-A10", sector="CIIU F (construcción)", regla="Actividad = construcción ∧ área ∈ {Contratación Pública, Contratos, Regulatorio}")
E(26, 5, "Salud", "Prestadores y aseguradores de salud, derechos del paciente, autorización y fiscalización sanitaria.", sectorial=True, sector="CAT-309 salud", regla="Sector regulado = salud ∧ área ∈ {Regulatorio, Administrativo, Consumidor, Seguridad Social}")
E(27, 5, "Farmacéutico y dispositivos médicos", "Registro sanitario, comercialización, publicidad y vigilancia de medicamentos y dispositivos.", sectorial=True, sector="CAT-309 farmaceutico", regla="Sector regulado = farmacéutico ∧ área ∈ {Regulatorio, Consumidor, Propiedad Intelectual, Competencia}")
E(28, 5, "Alimentos y bebidas", "Inocuidad, etiquetado, registro y publicidad de alimentos y bebidas.", sectorial=True, sector="CIIU 10–11", regla="Actividad = alimentos o bebidas ∧ área ∈ {Regulatorio, Consumidor}")
E(29, 5, "Educación", "Licenciamiento, supervisión y derechos en servicios educativos públicos y privados.", sectorial=True, sector="CAT-309 educacion", regla="Sector regulado = educación ∧ área ∈ {Regulatorio, Administrativo, Consumidor}")
E(30, 5, "Turismo y hotelería", "Prestadores turísticos, agencias de viaje, hospedaje.", sectorial=True, sector="CIIU 55, 79", regla="Actividad = turismo ∧ área ∈ {Regulatorio, Consumidor}")
E(31, 5, "Juegos y apuestas", "Casinos, máquinas tragamonedas, apuestas deportivas y en línea.", sectorial=True, sector="CIIU 92", regla="Actividad = juegos de azar ∧ área ∈ {Regulatorio, Tributario}")
E(32, 5, "Medios, publicidad y entretenimiento", "Radio, televisión, prensa, publicidad comercial, espectáculos.", sectorial=True, otros="CON-F2-A16", sector="CIIU 59–60, 73, 90", regla="Actividad = medios o entretenimiento ∧ área ∈ {Regulatorio, Propiedad Intelectual, Consumidor}")
E(33, 5, "Deportivo", "Organizaciones deportivas, contratos de deportistas, disciplina y justicia deportiva.", sectorial=True, otros="CON-F2-A18; CON-F2-A10", sector="CIIU 93", regla="Actividad = deporte ∧ área ∈ {Laboral, Contratos, Propiedad Intelectual, Administrativo}")
E(34, 5, "Moda", "Diseño, confección y comercialización de prendas y accesorios: marcas, licencias, importación, consumo y cadena de suministro.", sectorial=True, otros="CON-F2-A16; CON-F2-A14; CON-F2-A21; CON-F2-A10", sector="CIIU 13–15 y comercio de prendas", regla="Sector (regulado o del caso) = confección ∧ área ∈ {Propiedad Intelectual, Consumidor, Aduanero, Contratos}. Laboral excluido salvo decisión de producto")
# Ambiental (6)
E(35, 6, "Evaluación de impacto ambiental", "Instrumentos de gestión ambiental, certificaciones y estudios de impacto.")
E(36, 6, "Fiscalización y sanción ambiental", "Supervisión, infracciones, medidas correctivas y sanciones ambientales.", otros="CON-F2-A03")
E(37, 6, "Responsabilidad por daño ambiental", "Reparación, remediación y responsabilidad civil o administrativa por daño ambiental.")
E(38, 6, "Áreas naturales y biodiversidad", "Áreas protegidas, flora y fauna, recursos genéticos.")
E(39, 6, "Residuos, emisiones y calidad ambiental", "Residuos sólidos, estándares de calidad, límites de emisión, sustancias peligrosas.")
E(40, 6, "Cambio climático y sostenibilidad", "Mitigación, adaptación, mercados de carbono, finanzas sostenibles y ESG.")
# Recursos naturales y energía (7)
E(41, 7, "Minero", "Concesiones mineras, exploración, explotación, beneficio, cierre de minas, regalías y obligaciones de titulares mineros.", sectorial=True, otros="CON-F2-A06", sector="CAT-309 mineria", regla="Sector regulado = minería ∧ área ∈ {Recursos Naturales, Ambiental, Administrativo, Tributario, Laboral}")
E(42, 7, "Hidrocarburos", "Exploración, explotación, transporte, refinación y comercialización de petróleo y gas.", sectorial=True, otros="CON-F2-A06", sector="CAT-309 hidrocarburos", regla="Sector regulado = hidrocarburos ∧ área ∈ {Recursos Naturales, Ambiental, Administrativo, Tributario}")
E(43, 7, "Electricidad", "Generación, transmisión, distribución y comercialización eléctrica; tarifas eléctricas.", sectorial=True, otros="CON-F2-A05", sector="CAT-309 energia_electrica", regla="Sector regulado = electricidad ∧ área ∈ {Recursos Naturales, Regulatorio, Administrativo, Consumidor}")
E(44, 7, "Energías renovables", "Promoción y régimen de energías renovables no convencionales.", sectorial=True, otros="CON-F2-A06", sector="CAT-309 energia_electrica", regla="Sector regulado = electricidad (renovable) ∧ área ∈ {Recursos Naturales, Ambiental}")
E(45, 7, "Aguas y recursos hídricos", "Derechos de uso de agua, gestión de cuencas; agua potable y saneamiento como servicio.", sectorial=True, otros="CON-F2-A05; CON-F2-A06", sector="CAT-309 agua_saneamiento", regla="Sector = agua ∧ área ∈ {Recursos Naturales, Regulatorio, Ambiental}")
E(46, 7, "Forestal y fauna silvestre", "Concesiones y aprovechamiento forestal, tala, comercio de fauna.", sectorial=True, otros="CON-F2-A06", sector="CIIU 02", regla="Actividad = forestal ∧ área ∈ {Recursos Naturales, Ambiental, Penal}")
E(47, 7, "Pesca y acuicultura", "Derechos de pesca, cuotas, acuicultura y fiscalización pesquera.", sectorial=True, otros="CON-F2-A06", sector="CIIU 03", regla="Actividad = pesca ∧ área ∈ {Recursos Naturales, Ambiental, Administrativo}")
E(48, 7, "Agrario", "Propiedad y tenencia de tierras rurales, comunidades campesinas, desarrollo agrario, sanidad agraria.", sectorial=True, otros="CON-F2-A11", sector="CIIU 01", regla="Actividad = agricultura o ganadería ∧ área ∈ {Recursos Naturales, Civil, Inmobiliario, Regulatorio}")
# Civil (8)
E(49, 8, "Personas y capacidad", "Derechos de la personalidad, capacidad, apoyos y salvaguardias, personas jurídicas sin fines de lucro.")
E(50, 8, "Acto jurídico", "Elementos, vicios, nulidad, anulabilidad, representación.")
E(51, 8, "Obligaciones", "Fuentes, modalidades, pago, extinción, inejecución de obligaciones.")
E(52, 8, "Derechos reales", "Propiedad, posesión, copropiedad, servidumbres, usucapión, garantías reales.")
E(53, 8, "Responsabilidad civil", "Responsabilidad extracontractual y contractual, daños e indemnizaciones.")
E(54, 8, "Sucesiones", "Herencia, testamentos, sucesión intestada, partición.", otros="CON-F2-A09")
E(55, 8, "Prescripción y caducidad", "Prescripción extintiva y adquisitiva, caducidad en materia civil.")
# Familia (9)
E(56, 9, "Matrimonio, divorcio y uniones de hecho", "Celebración, nulidad, separación, divorcio y uniones convivenciales.")
E(57, 9, "Filiación", "Reconocimiento, impugnación de paternidad, filiación extramatrimonial, técnicas de reproducción.")
E(58, 9, "Alimentos", "Pensión alimenticia, aumento, reducción, exoneración y ejecución.")
E(59, 9, "Tenencia, custodia y régimen de visitas", "Custodia de hijos, patria potestad, régimen de comunicación.")
E(60, 9, "Adopción y protección de niñez", "Adopción, desprotección familiar, medidas de protección de niñas, niños y adolescentes.", otros="CON-F2-A02")
E(61, 9, "Violencia familiar (protección)", "Medidas de protección y procesos de violencia contra la mujer y el grupo familiar.", otros="CON-F2-A24")
E(62, 9, "Régimen patrimonial familiar", "Sociedad de gananciales, separación de patrimonios, liquidación.")
# Contratos (10)
E(63, 10, "Teoría general del contrato", "Formación, consentimiento, interpretación, resolución, rescisión, excesiva onerosidad.")
E(64, 10, "Compraventa y permuta", "Compraventa civil y mercantil, saneamiento, vicios ocultos.")
E(65, 10, "Arrendamiento", "Arrendamiento de bienes muebles e inmuebles, desalojo derivado del contrato.", otros="CON-F2-A11")
E(66, 10, "Contratos de servicios y obra", "Locación de servicios, contrato de obra, mandato, consultoría.")
E(67, 10, "Contratos de colaboración empresarial", "Distribución, agencia, franquicia, joint venture, consorcios.", otros="CON-F2-A13")
E(68, 10, "Contratos financieros y de garantía privados", "Mutuo, fianza, leasing, factoring entre particulares.", otros="CON-F2-A22")
E(69, 10, "Contratación tecnológica", "Licencias de software, servicios en la nube, desarrollo tecnológico.", otros="CON-F2-A17")
# Inmobiliario (11)
E(70, 11, "Registral", "Inscripción, principios registrales, calificación y tracto sucesivo.")
E(71, 11, "Notarial", "Función notarial, instrumentos públicos, asuntos no contenciosos notariales.")
E(72, 11, "Urbanístico y edificación", "Habilitación urbana, licencias de edificación, zonificación y planeamiento.", otros="CON-F2-A03")
E(73, 11, "Propiedad horizontal y condominios", "Régimen de unidades inmobiliarias de propiedad exclusiva y común.")
E(74, 11, "Negocios inmobiliarios", "Desarrollo y financiamiento inmobiliario, fideicomisos inmobiliarios, habilitación para la venta.", sectorial=True, otros="CON-F2-A10", sector="CIIU 68", regla="Actividad = inmobiliaria ∧ área ∈ {Inmobiliario, Contratos, Financiero}")
# Societario (12)
E(75, 12, "Constitución y gobierno corporativo", "Tipos societarios, estatutos, juntas, directorio, gerencia, deberes de administradores.")
E(76, 12, "Fusiones, adquisiciones y reorganizaciones", "Fusión, escisión, transformación, compraventa de empresas.")
E(77, 12, "Accionistas y valores societarios", "Derechos de socios, transferencia de acciones, pactos de accionistas.")
E(78, 12, "Cooperativas y otras formas asociativas", "Cooperativas, asociaciones y fundaciones con actividad económica.")
E(79, 12, "Compliance corporativo", "Programas de cumplimiento, prevención de delitos y de lavado de activos en empresas.", sectorial=True, otros="CON-F2-A24; CON-F2-A22", regla="Área ∈ {Societario, Penal económico, Financiero (prevención de lavado), Datos} ∧ función = obligaciones de cumplimiento empresarial")
# Mercantil (13)
E(80, 13, "Títulos valores", "Letras, pagarés, cheques, facturas negociables, protesto.")
E(81, 13, "Insolvencia y reestructuración", "Concurso, quiebra, reestructuración patrimonial, prelación de créditos.")
E(82, 13, "Contratos y transporte mercantil", "Transporte de mercancías, almacenaje, contratos mercantiles típicos.")
# Consumidor (14)
E(83, 14, "Idoneidad y garantías", "Deber de idoneidad de productos y servicios, garantías legales y voluntarias.", actual="Especialista Consumidor")
E(84, 14, "Información y publicidad al consumidor", "Deber de información, precios, publicidad engañosa frente a consumidores.", actual="Especialista Consumidor")
E(85, 14, "Cláusulas abusivas y contratos de consumo", "Contratos por adhesión, cláusulas abusivas, métodos comerciales coercitivos.", otros="CON-F2-A10", actual="Especialista Consumidor")
E(86, 14, "Consumidor financiero", "Protección de usuarios de servicios bancarios, de seguros y de pensiones.", otros="CON-F2-A22; CON-F2-A23", actual="Especialista Consumidor")
E(87, 14, "Procedimiento de protección al consumidor", "Reclamos, libro de reclamaciones, procedimientos sancionadores y sumarísimos.", otros="CON-F2-A03", actual="Especialista Consumidor")
E(88, 14, "Seguridad de productos y servicios", "Alertas, retiro de productos, salud y seguridad del consumidor.", actual="Especialista Consumidor")
# Competencia (15)
E(89, 15, "Libre competencia", "Abuso de posición de dominio, prácticas colusorias horizontales y verticales.")
E(90, 15, "Control de concentraciones", "Notificación y evaluación de fusiones y adquisiciones.", otros="CON-F2-A12")
E(91, 15, "Competencia desleal", "Actos de engaño, confusión, denigración, publicidad comparativa ilícita.")
E(92, 15, "Dumping, subsidios y salvaguardias", "Defensa comercial frente a importaciones.", otros="CON-F2-A21")
# Propiedad intelectual (16)
E(93, 16, "Marcas y signos distintivos", "Registro, oposición, nulidad, cancelación e infracción de marcas, nombres comerciales.")
E(94, 16, "Derecho de autor y conexos", "Obras, software, derechos morales y patrimoniales, gestión colectiva.")
E(95, 16, "Patentes y diseños", "Invenciones, modelos de utilidad, diseños industriales.")
E(96, 16, "Secretos empresariales e información confidencial", "Protección de know-how e información no divulgada.")
E(97, 16, "Denominaciones de origen y obtenciones vegetales", "Indicaciones geográficas y variedades vegetales.")
# Tecnología (17)
E(98, 17, "Protección de datos personales", "Tratamiento de datos, derechos de los titulares, autoridad de datos, transferencias internacionales.")
E(99, 17, "Comercio y firma electrónicos", "Contratación electrónica, firma y certificados digitales.")
E(100, 17, "Ciberseguridad y delitos informáticos", "Seguridad de la información, incidentes, delitos informáticos.", otros="CON-F2-A24")
E(101, 17, "Plataformas digitales e inteligencia artificial", "Economía de plataformas, algoritmos, IA, responsabilidad de intermediarios.")
E(102, 17, "Fintech y activos digitales", "Plataformas de financiamiento, pagos digitales, criptoactivos.", sectorial=True, otros="CON-F2-A22", sector="CAT-309 datos_digital; sistema_financiero", regla="Actividad = servicios financieros digitales ∧ área ∈ {Financiero, Tecnología}")
# Laboral (18)
E(103, 18, "Derecho individual del trabajo", "Contrato de trabajo, modalidades, remuneración, jornada, beneficios, extinción.", actual="Especialista Laboral")
E(104, 18, "Derecho colectivo del trabajo", "Sindicatos, negociación colectiva, convenios, huelga.", actual="Especialista Laboral")
E(105, 18, "Seguridad y salud en el trabajo", "Obligaciones de prevención, comités, accidentes, fiscalización en SST.", otros="CON-F2-A19", actual="Especialista Laboral")
E(106, 18, "Inspección y sanción laboral", "Procedimiento inspectivo, infracciones y multas laborales.", otros="CON-F2-A03", actual="Especialista Laboral")
E(107, 18, "Procesal laboral", "Procesos judiciales laborales, competencia, prueba y medios impugnatorios laborales.", otros="CON-F2-A25", actual="Especialista Laboral")
E(108, 18, "Regímenes laborales especiales", "Trabajo doméstico, agrario, minero, construcción civil, MYPE, teletrabajo, regímenes públicos.", actual="Especialista Laboral")
E(109, 18, "Tercerización e intermediación laboral", "Subcontratación, intermediación, responsabilidad solidaria.", actual="Especialista Laboral")
# Seguridad social (19)
E(110, 19, "Pensiones públicas", "Sistemas públicos o de reparto, requisitos y cálculo de pensiones.")
E(111, 19, "Pensiones privadas", "Administradoras de fondos, afiliación, aportes, retiro de fondos.", sectorial=True, otros="CON-F2-A22", sector="CAT-309 pensiones", regla="Sector regulado = pensiones ∧ área ∈ {Seguridad Social, Financiero, Consumidor}")
E(112, 19, "Salud contributiva y prestaciones", "Seguro social de salud, subsidios por incapacidad o maternidad.")
E(113, 19, "Riesgos del trabajo", "Seguro complementario de trabajo de riesgo, enfermedades profesionales y accidentes.", otros="CON-F2-A18")
# Tributario (20)
E(114, 20, "Código tributario y procedimientos", "Obligación tributaria, fiscalización, determinación, cobranza coactiva, reclamación y apelación.", actual="Especialista Tributario")
E(115, 20, "Impuesto a la renta", "Renta empresarial y de personas naturales, retenciones, gastos deducibles.", actual="Especialista Tributario")
E(116, 20, "IVA o IGV e impuestos al consumo", "Impuesto al valor agregado, impuestos selectivos o especiales al consumo.", actual="Especialista Tributario")
E(117, 20, "Tributación municipal y subnacional", "Predial, alcabala, arbitrios, impuestos y tasas locales o provinciales.", otros="CON-F2-E016", actual="Especialista Tributario")
E(118, 20, "Tributación internacional", "Convenios de doble imposición, precios de transferencia, no domiciliados, establecimiento permanente.", otros="CON-F2-A27", actual="Especialista Tributario")
E(119, 20, "Infracciones, sanciones y delitos tributarios", "Multas tributarias, gradualidad, defraudación tributaria.", otros="CON-F2-A24", actual="Especialista Tributario")
E(120, 20, "Beneficios y regímenes tributarios especiales", "Exoneraciones, inafectaciones, regímenes promocionales y sectoriales.", actual="Especialista Tributario")
E(121, 20, "Contribuciones y tasas", "Contribuciones parafiscales, aportes, tasas por servicios públicos.", actual="Especialista Tributario")
# Aduanero (21)
E(122, 21, "Regímenes y procedimientos aduaneros", "Importación, exportación, tránsito, regímenes temporales y de perfeccionamiento.")
E(123, 21, "Valoración y clasificación arancelaria", "Valor en aduana, nomenclatura arancelaria, origen de mercancías.")
E(124, 21, "Infracciones y delitos aduaneros", "Sanciones aduaneras, contrabando, defraudación de rentas de aduana.", otros="CON-F2-A24")
E(125, 21, "Acuerdos comerciales y origen", "Tratados de libre comercio, reglas de origen, preferencias arancelarias.", otros="CON-F2-A27")
# Financiero (22)
E(126, 22, "Bancario", "Entidades bancarias y financieras, operaciones activas y pasivas, supervisión bancaria.", sectorial=True, sector="CAT-309 sistema_financiero", regla="Sector regulado = sistema financiero ∧ área ∈ {Financiero, Contratos, Consumidor, Administrativo}")
E(127, 22, "Mercado de valores", "Oferta pública, emisores, intermediarios, fondos de inversión, abuso de mercado.", sectorial=True, sector="CAT-309 mercado_valores", regla="Sector regulado = mercado de valores ∧ área ∈ {Financiero, Societario, Administrativo}")
E(128, 22, "Medios de pago y dinero electrónico", "Transferencias, tarjetas, billeteras y dinero electrónico.")
E(129, 22, "Prevención de lavado de activos", "Sujetos obligados, debida diligencia, reportes de operaciones sospechosas.", otros="CON-F2-A24")
E(130, 22, "Garantías y financiamiento", "Garantías mobiliarias, fideicomisos, financiamiento estructurado.", otros="CON-F2-A10")
E(131, 22, "Microfinanzas y cooperativas de ahorro", "Entidades microfinancieras y cooperativas de ahorro y crédito.")
# Seguros (23)
E(132, 23, "Contrato de seguro y siniestros", "Pólizas, coberturas, exclusiones, indemnizaciones.", otros="CON-F2-A10")
E(133, 23, "Supervisión de aseguradoras e intermediarios", "Autorización, solvencia y conducta de aseguradoras y corredores.", sectorial=True, sector="CAT-309 seguros", regla="Sector regulado = seguros ∧ área ∈ {Seguros, Administrativo}")
# Penal (24)
E(134, 24, "Parte general penal", "Teoría del delito, autoría y participación, consecuencias jurídicas, prescripción.")
E(135, 24, "Delitos contra la persona", "Homicidio, lesiones, delitos contra la libertad e integridad.")
E(136, 24, "Delitos contra el patrimonio", "Hurto, robo, estafa, apropiación ilícita, usurpación.")
E(137, 24, "Penal económico y empresarial", "Delitos societarios, financieros, contra el orden económico, responsabilidad penal de personas jurídicas.", otros="CON-F2-A12")
E(138, 24, "Delitos contra la administración pública", "Corrupción de funcionarios, peculado, colusión, negociación incompatible.", otros="CON-F2-E015")
E(139, 24, "Lavado de activos y crimen organizado", "Lavado de activos, organización criminal, financiamiento del terrorismo.")
E(140, 24, "Tráfico ilícito de drogas", "Delitos de drogas y precursores.")
E(141, 24, "Violencia de género y sexual", "Feminicidio, violencia contra la mujer, delitos contra la libertad sexual.", otros="CON-F2-E061")
E(142, 24, "Ejecución penal y penitenciario", "Ejecución de penas, beneficios penitenciarios, régimen carcelario.")
E(143, 24, "Penal ambiental", "Delitos ambientales, minería ilegal, tala ilegal.", otros="CON-F2-A06")
# Procesal (25)
E(144, 25, "Procesal civil", "Proceso civil: demanda, prueba, medios impugnatorios, cautelares, ejecución.")
E(145, 25, "Procesal penal", "Investigación, medidas coercitivas, juicio, recursos y ejecución en el proceso penal.", otros="CON-F2-A24")
E(146, 25, "Procesal constitucional", "Reglas procesales de las garantías constitucionales.", otros="CON-F2-A01")
E(147, 25, "Procesal de familia", "Reglas procesales de los procesos de familia.", otros="CON-F2-A09")
E(148, 25, "Medidas cautelares y ejecución", "Embargos, secuestros, ejecución forzada de resoluciones.")
E(149, 25, "Recursos extraordinarios y casación", "Casación, revisión y recursos ante cortes supremas.")
E(150, 25, "Organización judicial y ética", "Organización del poder judicial, carrera judicial, responsabilidad de jueces y abogados.")
# Arbitraje (26)
E(151, 26, "Arbitraje comercial", "Convenio arbitral, procedimiento, laudo y anulación en arbitraje comercial.")
E(152, 26, "Arbitraje de inversiones", "Controversias inversor-Estado bajo tratados de inversión.", otros="CON-F2-A27")
E(153, 26, "Arbitraje en contratación pública", "Controversias de contratos estatales sometidas a arbitraje.", otros="CON-F2-A04")
E(154, 26, "Conciliación y mediación", "Conciliación extrajudicial y judicial, mediación.")
# Internacional (27)
E(155, 27, "Internacional público", "Tratados, responsabilidad internacional del Estado, organismos internacionales, fronteras.")
E(156, 27, "Internacional privado", "Ley aplicable, jurisdicción internacional, reconocimiento de sentencias y laudos extranjeros.")
E(157, 27, "Inversión extranjera", "Régimen de inversiones, convenios de estabilidad, tratados bilaterales de inversión.")
E(158, 27, "Integración regional", "Comunidad Andina, Mercosur y sus normas y tribunales.")

# =============================================================================== NIVEL 3: SUBESPECIALIDADES (selección inicial)
# Laboral – individual (E103)
for i, (n, inc) in enumerate([
    ("Contratación y modalidades laborales", "Contratos a plazo fijo, a tiempo parcial, desnaturalización de contratos."),
    ("Remuneraciones y beneficios sociales", "Remuneración, gratificaciones, compensación por tiempo de servicios, vacaciones, utilidades."),
    ("Jornada y descansos", "Jornada máxima, horas extras, trabajo nocturno, descansos."),
    ("Despido y estabilidad laboral", "Despido arbitrario, nulo, fraudulento, incausado; reposición e indemnización."),
    ("Hostigamiento y acoso laboral", "Hostigamiento sexual, acoso laboral, actos de hostilidad."),
    ("Igualdad y no discriminación en el empleo", "Discriminación salarial, maternidad, igualdad de oportunidades."),
    ("Teletrabajo y trabajo remoto", "Régimen de teletrabajo y trabajo a distancia."),
    ("Poder de dirección y disciplina", "Facultades del empleador, reglamento interno, sanciones disciplinarias."),
], 1):
    S(i, "CON-F2-E103", n, inc, actual="Especialista Laboral")
for i, (n, inc) in enumerate([
    ("Libertad sindical", "Constitución de sindicatos, fuero sindical, actos antisindicales."),
    ("Negociación colectiva", "Pliegos, convenios colectivos, arbitraje laboral."),
    ("Huelga", "Ejercicio, declaratoria y efectos de la huelga."),
], 9):
    S(i, "CON-F2-E104", n, inc, actual="Especialista Laboral")
# Tributario
for i, (padre, n, inc) in enumerate([
    ("CON-F2-E114", "Fiscalización y determinación", "Procedimientos de fiscalización, verificación, determinación sobre base cierta o presunta."),
    ("CON-F2-E114", "Cobranza coactiva", "Ejecución coactiva de deuda tributaria, medidas cautelares previas."),
    ("CON-F2-E114", "Reclamación y apelación tributaria", "Recursos ante la administración y el tribunal fiscal."),
    ("CON-F2-E114", "Prescripción tributaria", "Plazos de prescripción, interrupción y suspensión."),
    ("CON-F2-E115", "Renta empresarial", "Rentas de tercera categoría o empresariales, gastos, depreciación."),
    ("CON-F2-E115", "Renta de personas naturales", "Rentas del trabajo y del capital de personas naturales."),
    ("CON-F2-E115", "Retenciones y pagos a cuenta", "Agentes de retención, pagos anticipados."),
    ("CON-F2-E116", "Crédito fiscal", "Requisitos y uso del crédito fiscal del IVA o IGV."),
    ("CON-F2-E116", "Exportación de servicios e IVA", "Tratamiento de exportaciones, servicios digitales del exterior."),
    ("CON-F2-E118", "Precios de transferencia", "Valor de mercado entre partes vinculadas."),
    ("CON-F2-E118", "Convenios para evitar la doble imposición", "Aplicación de convenios y residencia fiscal."),
    ("CON-F2-E119", "Régimen de infracciones y gradualidad", "Tipificación de infracciones tributarias y rebajas de multas."),
], 12):
    S(i, padre, n, inc, actual="Especialista Tributario")
# Consumidor
for i, (padre, n, inc) in enumerate([
    ("CON-F2-E83", "Servicios de telecomunicaciones al usuario", "Reclamos de usuarios de telefonía, internet y televisión."),
    ("CON-F2-E83", "Transporte de pasajeros", "Pasajes aéreos y terrestres, demoras, cancelaciones, equipaje."),
    ("CON-F2-E83", "Productos inmobiliarios al consumidor", "Venta de inmuebles a consumidores, entrega y vicios."),
    ("CON-F2-E83", "Servicios educativos al consumidor", "Cobros, información y calidad en servicios educativos."),
    ("CON-F2-E86", "Tarjetas de crédito y cobros indebidos", "Consumos no reconocidos, cobros, tasas e intereses."),
    ("CON-F2-E86", "Seguros al consumidor", "Denegatoria de coberturas y reclamos de asegurados consumidores."),
    ("CON-F2-E84", "Publicidad engañosa", "Publicidad que induce a error al consumidor."),
    ("CON-F2-E87", "Libro de reclamaciones", "Obligaciones y procedimientos del libro de reclamaciones."),
    ("CON-F2-E85", "Métodos comerciales agresivos", "Prácticas coercitivas y cobranza abusiva."),
], 24):
    S(i, padre.replace("E83", "E083").replace("E84", "E084").replace("E85", "E085").replace("E86", "E086").replace("E87", "E087"), n, inc, actual="Especialista Consumidor")
# Otras áreas de alta demanda
OTRAS = [
    ("CON-F2-E053", "Responsabilidad médica", "Daños por actos médicos y de establecimientos de salud."),
    ("CON-F2-E053", "Accidentes de tránsito", "Responsabilidad e indemnización por accidentes de tránsito."),
    ("CON-F2-E052", "Prescripción adquisitiva", "Usucapión de bienes muebles e inmuebles."),
    ("CON-F2-E052", "Desalojo y reivindicación", "Recuperación de la posesión y de la propiedad."),
    ("CON-F2-E052", "Garantías hipotecarias", "Constitución, ejecución y cancelación de hipotecas."),
    ("CON-F2-E058", "Alimentos para hijos mayores de edad", "Continuación de alimentos por estudios o discapacidad."),
    ("CON-F2-E056", "Divorcio por causal", "Causales de divorcio y sus efectos."),
    ("CON-F2-E010", "Nulidad de actos administrativos", "Causales y declaración de nulidad de oficio o a pedido de parte."),
    ("CON-F2-E010", "Silencio administrativo", "Silencio positivo y negativo y sus efectos."),
    ("CON-F2-E011", "Graduación de sanciones administrativas", "Criterios de graduación y atenuantes."),
    ("CON-F2-E020", "Penalidades y resolución en contratos estatales", "Aplicación de penalidades y resolución contractual."),
    ("CON-F2-E019", "Impedimentos para contratar con el Estado", "Supuestos y alcance de los impedimentos."),
    ("CON-F2-E134", "Prescripción de la acción penal", "Plazos y cómputo de la prescripción penal."),
    ("CON-F2-E145", "Prisión preventiva y medidas coercitivas", "Requisitos y control de medidas coercitivas personales."),
    ("CON-F2-E138", "Colusión y peculado", "Delitos funcionales de colusión y peculado."),
    ("CON-F2-E144", "Proceso de ejecución", "Ejecución de títulos ejecutivos y de resoluciones."),
    ("CON-F2-E149", "Casación civil", "Causales y procedencia del recurso de casación civil."),
    ("CON-F2-E075", "Responsabilidad de directores y gerentes", "Deberes fiduciarios y responsabilidad de administradores."),
    ("CON-F2-E098", "Videovigilancia y datos de trabajadores", "Tratamiento de datos en el ámbito laboral y videovigilancia."),
    ("CON-F2-E093", "Oposición y nulidad de marcas", "Procedimientos de oposición, nulidad y cancelación de registros."),
    ("CON-F2-E089", "Carteles", "Acuerdos colusorios horizontales entre competidores."),
    ("CON-F3-E041", "Cierre de minas y pasivos ambientales", "Planes de cierre, garantías y pasivos ambientales mineros."),
    ("CON-F3-E041", "Concesiones y derechos mineros", "Otorgamiento, caducidad y extinción de concesiones."),
    ("CON-F3-E041", "Regalías y tributación minera", "Regalías, gravámenes e impuestos especiales a la minería."),
    ("CON-F3-E126", "Créditos y garantías bancarias", "Operaciones de crédito, garantías y recuperación de cartera."),
    ("CON-F3-E126", "Supervisión prudencial", "Requerimientos de capital, provisiones y supervisión bancaria."),
    ("CON-F2-E036", "Medidas administrativas ambientales", "Medidas preventivas, correctivas y cautelares ambientales."),
    ("CON-F2-E105", "Accidentes de trabajo y responsabilidad del empleador", "Indemnización por accidentes y enfermedades laborales."),
]
for i, (padre, n, inc) in enumerate(OTRAS, 33):
    S(i, padre, n, inc, actual="Especialista Laboral" if padre in ("CON-F2-E105",) else "—")

# Normaliza IDs de padres de nivel 3 con número de 3 dígitos
for r in ROWS:
    if r["nivel"] == 3:
        p = r["padre"]
        pre, num = p.rsplit("E", 1)
        r["padre"] = f"{pre}E{int(num):03d}"
        if r["padre"] not in {x["id"] for x in ROWS}:
            # especialidad sectorial (F3)
            alt = r["padre"].replace("CON-F2-", "CON-F3-")
            r["padre"] = alt
# Nivel 2: gran área heredada del área principal
AREA = {r["id"]: r for r in ROWS if r["nivel"] == 1}
for r in ROWS:
    if r["nivel"] == 2:
        r["ga"] = AREA[r["padre"]]["ga"]
IDX = {r["id"]: r for r in ROWS}
for r in ROWS:
    if r["nivel"] == 3:
        r["ga"] = IDX[r["padre"]]["ga"]

# =============================================================================== ESPECIALISTAS DE JUZTINA (CAT-331)
# 'etiquetas': IDs de etiquetas; se incluyen sus descendientes. 'relevancia': mínima exigida.
SPECIALISTS = [
 dict(id="ESP-01", nombre="Laboral", estado="En producción", etiquetas="CON-F2-A18; CON-F2-E113", relevancia="Principal o secundaria",
      excluye="—", nota="Validar contra los criterios actuales del especialista (emisor, tipo documental, materia). Riesgos del trabajo (E113) se incluye por cercanía con SST."),
 dict(id="ESP-02", nombre="Tributario", estado="En producción", etiquetas="CON-F2-A20", relevancia="Principal o secundaria",
      excluye="—", nota="Decidir si Aduanero (A21) se integra o es un producto aparte."),
 dict(id="ESP-03", nombre="Consumidor", estado="En producción", etiquetas="CON-F2-A14", relevancia="Principal o secundaria",
      excluye="—", nota="Incluye consumidor financiero (E086)."),
 dict(id="ESP-04", nombre="Civil y Contratos", estado="Potencial", etiquetas="CON-F2-A08; CON-F2-A10", relevancia="Principal", excluye="—", nota="—"),
 dict(id="ESP-05", nombre="Familia", estado="Potencial", etiquetas="CON-F2-A09; CON-F2-E147", relevancia="Principal o secundaria", excluye="—", nota="Alta sensibilidad de datos personales (D16)."),
 dict(id="ESP-06", nombre="Penal", estado="Potencial", etiquetas="CON-F2-A24; CON-F2-E145", relevancia="Principal", excluye="—", nota="—"),
 dict(id="ESP-07", nombre="Procesal Civil", estado="Potencial", etiquetas="CON-F2-E144; CON-F2-E148; CON-F2-E149", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-08", nombre="Constitucional", estado="Potencial", etiquetas="CON-F2-A01; CON-F2-A02", relevancia="Principal", excluye="—", nota="—"),
 dict(id="ESP-09", nombre="Administrativo", estado="Potencial", etiquetas="CON-F2-A03", relevancia="Principal", excluye="—", nota="—"),
 dict(id="ESP-10", nombre="Contratación Pública", estado="Potencial", etiquetas="CON-F2-A04; CON-F2-E153", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-11", nombre="Ambiental", estado="Potencial", etiquetas="CON-F2-A06; CON-F2-E143", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-12", nombre="Minero", estado="Potencial", etiquetas="CON-F3-E041", relevancia="Principal o secundaria", excluye="—", nota="Etiqueta sectorial calculada por regla (sector minería + áreas)."),
 dict(id="ESP-13", nombre="Energía e Hidrocarburos", estado="Potencial", etiquetas="CON-F3-E042; CON-F3-E043; CON-F3-E044", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-14", nombre="Financiero y Bancario", estado="Potencial", etiquetas="CON-F2-A22", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-15", nombre="Seguros", estado="Potencial", etiquetas="CON-F2-A23", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-16", nombre="Societario y Corporativo", estado="Potencial", etiquetas="CON-F2-A12; CON-F2-E081", relevancia="Principal", excluye="—", nota="—"),
 dict(id="ESP-17", nombre="Competencia", estado="Potencial", etiquetas="CON-F2-A15", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-18", nombre="Propiedad Intelectual", estado="Potencial", etiquetas="CON-F2-A16", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-19", nombre="Protección de Datos y Tecnología", estado="Potencial", etiquetas="CON-F2-A17", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-20", nombre="Aduanero y Comercio Exterior", estado="Potencial", etiquetas="CON-F2-A21; CON-F2-E092", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-21", nombre="Seguridad Social y Pensiones", estado="Potencial", etiquetas="CON-F2-A19", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-22", nombre="Inmobiliario y Registral", estado="Potencial", etiquetas="CON-F2-A11; CON-F2-E052; CON-F2-E065", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-23", nombre="Arbitraje", estado="Potencial", etiquetas="CON-F2-A26", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-24", nombre="Salud y Farmacéutico", estado="Potencial", etiquetas="CON-F3-E026; CON-F3-E027; CON-F4-S033", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-25", nombre="Telecomunicaciones", estado="Potencial", etiquetas="CON-F3-E023; CON-F4-S024", relevancia="Principal o secundaria", excluye="—", nota="—"),
 dict(id="ESP-26", nombre="Compliance Corporativo", estado="Potencial", etiquetas="CON-F3-E079; CON-F2-E137; CON-F2-E129; CON-F2-E098; CON-F2-E089", relevancia="Principal o secundaria", excluye="—", nota="Producto compuesto: combina etiquetas de cinco áreas."),
 dict(id="ESP-27", nombre="Moda", estado="Potencial", etiquetas="CON-F3-E034", relevancia="Principal o secundaria", excluye="—", nota="Ejemplo de especialidad de práctica definida por regla sectorial."),
]
