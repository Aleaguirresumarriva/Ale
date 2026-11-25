# Resumen ejecutivo: inventario de metadatos jurídicos de Juztina

**El diccionario maestro define 624 campos de metadatos.** Cada campo indica:

- su unidad documental, dimensión y perfil;
- su origen, método de adquisición, regla de extracción, regla de validación y evidencia exigida;
- su prioridad, modo de adquisición, clase de riesgo y necesidad de revisión;
- su sensibilidad, aplicabilidad por país, funcionalidades y validaciones pendientes.

**Estado:** listo para revisión por los equipos jurídico, técnico y de producto. **No** está listo para implementar mientras no se resuelvan las validaciones de la sección 4.

Archivo: `Juztina_Diccionario_Maestro_Metadatos_v1.0.xlsx` (20 hojas). Todas las cifras de este resumen salen de la hoja `12_Cobertura`, que las calcula con fórmulas.

## 1. Etiquetas por áreas del Derecho (taxonomía)

La clasificación por áreas, que habilita los especialistas, está en dos hojas:

- **`5b_Taxonomia_etiquetas`.** 245 etiquetas en tres niveles:
  - 27 áreas principales (Constitucional, Administrativo, Civil, Familia, Contratos, Laboral, Tributario, Consumidor, Procesal, Penal, Financiero…);
  - 131 especialidades;
  - 27 especialidades sectoriales o de práctica (Minero, Bancario, Hidrocarburos, Salud, Telecomunicaciones, Moda…);
  - 60 subespecialidades.

  Cada etiqueta indica qué incluye y qué excluye, trae indicadores para la IA y tiene columnas amarillas para que el equipo jurídico la valide o proponga etiquetas nuevas.
- **`5c_Especialistas_Juztina`.** 3 especialistas en producción (Laboral, Tributario, Consumidor) y 24 potenciales, cada uno definido como un conjunto de etiquetas. Un especialista nuevo se crea definiendo sus etiquetas, sin reprocesar el corpus.

La taxonomía es una **semilla pendiente de validación** (DEC-35).

## 2. Cifras principales

| Indicador | Valor |
| --- | --- |
| Campos definidos | **624** |
| Campos universales (cuatro categorías) | 361 |
| Campos compartidos por dos o tres categorías | 211 |
| Campos específicos de una categoría | 52 |
| Campos aplicables a normativa / jurisprudencia / actos / doctrina | 499 / 517 / 577 / 391 |
| Tipos de relación documental | 61 |
| Catálogos controlados / valores | 148 / 1.293 |
| Valores semilla pendientes de validación nacional | 167 |
| Campos con validaciones o decisiones pendientes | 188 |
| Campos con datos personales o restricciones (cualquier nivel) | 49 |
| Campos que se conservan en la pasada masiva (modo A) | 368 |

## 3. Prioridad y modo de adquisición

| Prioridad | A (pasada) | B (calculado) | C (posterior) | D (externo o curado) | X (fuera de alcance) | Total |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | 213 | 44 | 0 | 38 | 0 | 295 |
| P1 | 134 | 65 | 0 | 30 | 0 | 229 |
| P2 | 19 | 10 | 33 | 15 | 0 | 77 |
| P3 | 2 | 8 | 5 | 4 | 0 | 19 |
| Fuera de alcance | 0 | 0 | 0 | 0 | 4 | 4 |

Los 295 campos P0 cubren los seis bloques que la arquitectura protege:

1. identidad y procedencia;
2. estructura, segmentación y anclas;
3. referencias explícitas relevantes;
4. hechos primarios no reconstruibles;
5. datos para la política de privacidad;
6. calidad.

P0 incluye además los identificadores y registros técnicos generados por el sistema. No incluye clasificación temática ni análisis jurídico.

## 4. Distribución

- **Por dimensión.** Los mayores bloques son referencias y relaciones (64), temporalidad y vigencia (60), estructura (60), clasificación (51) y la capa de procedencia (48).
- **Por unidad.** Obra (140), unidad estructural (68), manifestación (51), referencia (44), monto (29), parte o actor (23) y concepto de taxonomía (23).
- **Por origen del dato.**

| Origen | Campos |
| --- | --- |
| Explícito en documento | 174 |
| Derivado por cálculo | 112 |
| Generado por sistema | 98 |
| Inferido por modelo | 72 |
| Curado por persona | 66 |
| Normalizado por regla | 56 |
| Fuente externa | 24 |
| Conclusión jurídica por reglas | 22 |

- **Por riesgo.** R1: 133 · R2: 286 · R3: 205.
- **Revisión humana.** Obligatoria en 56 campos y condicionada en 140.
- **Por país.** Todos los campos aplican a los siete países, salvo los de figuras que no existen en todos (por ejemplo, los textos ordenados). Hay 478 campos comunes, 85 con catálogo por país y 58 pendientes de validación nacional.

## 5. Antes de implementar

1. **Validación de la taxonomía de etiquetas y de los especialistas** (DEC-35) por los especialistas de cada materia: es la base de la funcionalidad principal.
2. **Validación nacional** de catálogos y reglas por un especialista de cada país: tipos documentales, rangos, precedentes, efectos de vigencia, códigos territoriales y unidades de valor.
3. **Política de datos personales** por país (DEC-18). Define el alcance final de los campos de partes y personas.
4. **Metas de precisión y capacidad de revisión** (DEC-20). Afectan a 41 campos y a la interpretación de la regla RG-10.
5. **Presupuesto y volumen del corpus** para fijar el corte entre P1 y P2 (DEC-22).
6. **Piloto** sobre una muestra estratificada con conjunto de referencia anotado por abogados. Ningún campo entra en la pasada masiva sin alcanzar su meta de precisión.
