# Riesgos, limitaciones y decisiones pendientes antes de la implementación

## 1. Limitaciones del inventario

| Limitación | Consecuencia | Cómo se mitiga |
| --- | --- | --- |
| No se conoce el corpus real: volumen, formatos, OCR, completitud histórica, campos actuales | Prioridades y costos son estimaciones de diseño | Nada en el diccionario presupone esos datos; DEC-22 y DEC-32 quedan abiertas |
| No hay esquema de la base de datos actual | No se pudo mapear cada campo con un campo existente de Juztina | MDJ-D06-028 conserva la clasificación actual como línea base; ingeniería debe hacer el mapeo |
| Reglas y catálogos nacionales sin validar | 58 campos y 167 valores de catálogo dependen de validación nacional | Estado «Semilla — pendiente de validación nacional». Las reglas no validadas no se ejecutan y su resultado queda «Indeterminado» |
| Ejemplos de instituciones nacionales tomados del conocimiento general, sin verificar en fuentes | Puede haber imprecisiones en catálogos semilla | Ninguno se presenta como validado; revisión obligatoria por especialistas |
| Redacción por bloques | Riesgo residual de duplicidades semánticas no detectadas | Se integraron 12 campos y 2 catálogos duplicados; los controles automáticos dan cero. Se recomienda una revisión jurídica por dimensión |
| Diccionario, no esquema físico | Tipos de dato y cardinalidades son lógicos | Ingeniería debe traducirlos a su modelo físico |

## 2. Riesgos para la implementación

| Tipo | Riesgo | Impacto | Control previsto en el diccionario |
| --- | --- | --- | --- |
| Jurídico | Presentar como vigente una norma derogada fuera del corpus | Muy alto | Estado de vigencia calculado, con fuente y fecha de corte; leyenda «sin derogación registrada al [fecha]»; derogación tácita fuera del alcance como proceso masivo |
| Jurídico | Atribuir fuerza vinculante sin base | Alto | Hechos primarios de formación y autodeclaración; carácter de precedente calculado por reglas de país (DEC-25) |
| Jurídico | Equivalencias forzadas entre países | Alto | Tipo de equivalencia (CAT-012) en catálogos y taxonomía; solo la equivalencia jurídica validada permite afirmar «el equivalente es» |
| Jurídico | Tratamiento indebido de datos personales | Alto e irreversible | Nombres y documentos de personas naturales fuera de alcance; indicadores de privacidad en P0; DEC-18 abierta |
| Jurídico | Uso de doctrina protegida | Medio | Campos de acceso, licencia y nivel de exposición (D16); DEC-27 abierta |
| Técnico | Alucinación de números, fechas o montos | Alto | Evidencia literal verificada; cotejo de cifra y letras; prohibición de completar con conocimiento externo |
| Técnico | Segmentación incorrecta | Alto | Campos de clase de unidad, nivel, continuidad y calidad de segmentación; controles de numeración |
| Técnico | Demasiados campos por llamada al modelo | Medio | Etapas E0–E8 y perfiles de extracción por tipo de unidad |
| Operativo | Capacidad de revisión insuficiente | Alto | 56 campos con revisión obligatoria y 140 condicionada; interpretación de RG-10 pendiente (DEC-20) |
| Operativo | Falta de especialistas nacionales | Alto | Las reglas nacionales quedan desactivadas hasta validarse |
| Operativo | Presupuesto de la pasada | Alto | Prioridades P0–P3; las secciones de C y P2 se pueden diferir sin releer documentos, si se conservan los insumos intermedios (DEC-24) |

## 3. Decisiones pendientes, por orden de urgencia

| Orden | Decisión | Por qué es urgente | Campos afectados |
| --- | --- | --- | --- |
| 0 | DEC-35 Validación de la taxonomía de etiquetas y de los especialistas | Es la base de la funcionalidad principal (selección de documentos por especialista) | 4 campos y 245 etiquetas |
| 1 | DEC-18 Política de datos personales | Define campos que se extraen en P0 y no es reversible | 23 |
| 2 | DEC-20 Metas de precisión e interpretación de RG-10 | Decide qué campos entran en la pasada y cuánto hay que revisar | 41 |
| 3 | DEC-22 Corte P1/P2 (presupuesto y volumen) | Fija el alcance final de la pasada | Todos los P1 y P2 |
| 4 | DEC-24 Conservación de insumos intermedios | Sin ellos, la clase C exige releer el corpus | 2 directos; condiciona toda la clase C |
| 5 | DEC-08 Mapeo de tipos documentales a naturalezas por país | Activa los perfiles documentales | 21 |
| 6 | DEC-17 Reglas de vigencia y fuentes oficiales por país | Habilita el cálculo de vigencia | 20 |
| 7 | DEC-25 Reglas de precedente por país | Habilita el carácter de precedente | 15 |
| 8 | DEC-28 Catálogo territorial | Habilita el ámbito territorial normalizado | 14 |
| 9 | DEC-29 Serie de unidades de valor | Habilita conversiones de montos | 10 |
| 10 | DEC-14 Validación de correspondencias | Habilita la comparación entre países | 10 |
| — | DEC-03, 04, 07, 09, 11, 12, 13, 19, 26, 27, 30, 31, 32, 33, 34 | Ver hoja 11 | 1–8 cada una |

## 4. Recomendación para pasar a implementación

1. Revisión jurídica del diccionario por dimensión: especialistas por materia y un responsable por país.
2. Resolver las decisiones 1 a 4 anteriores.
3. Mapear los campos existentes de la base de Juztina contra el diccionario (ingeniería).
4. Piloto estratificado por país, categoría y naturaleza, con conjunto de referencia anotado. Medir la precisión por campo y retirar de la pasada los que no alcancen su meta.
5. Congelar la versión del diccionario, las instrucciones y los modelos para la pasada masiva.
