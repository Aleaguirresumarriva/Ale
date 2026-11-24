# Decisiones metodológicas del inventario de metadatos (Etapa 2)

**Proyecto:** Arquitectura global de metadatos jurídicos de Juztina
**Entregable:** `Juztina_Diccionario_Maestro_Metadatos_v1.0.xlsx`
**Fecha:** 2026-11-24 · **Versión del diccionario:** 1.0

## 1. Fuente de referencia

El inventario se construyó sobre la **arquitectura conceptual versión 3 (final)**, pestaña «Versión 3 · final» del documento de arquitectura en Claude Docs. Se usaron sus componentes sin modificarlos:

| Componente de la arquitectura | Cómo se refleja en el Excel |
| --- | --- |
| 6 unidades de registro y 4 clases de entidades | Columna «Unidad de registro» (hoja 14 con definiciones) |
| 4 ejes del campo: perfil, dimensión, unidad y modo de origen | Columnas «Perfil documental», «Dimensión», «Unidad de registro» y «Origen del dato» |
| 16 dimensiones (D1–D17, sin D12) más las capas de procedencia y operativa | 18 códigos de dimensión: `D01`…`D17`, `PRO`, `OPE` |
| Etapas E0–E8 | Columna «Etapa de procesamiento» |
| Prioridades P0–P3 y clases A, B, C, D y X | Columnas «Prioridad» y «Modo de adquisición» |
| Clases de riesgo R1–R3 | Columna «Clase de riesgo» y criterios de aceptación (hoja 13) |
| 8 estados de campo | Catálogo CAT-006 y campos de la capa operativa |
| Decisiones pendientes de la matriz F | Códigos DEC-xx (hoja 11), ampliados con DEC-25 a DEC-34 a partir de la validación transversal |

## 2. Inspección del proyecto

El repositorio contiene dos hojas de cálculo de mapeo de fuentes de Bolivia (doctrina; laudos y conciliación). No hay esquema de base de datos, código ni diccionario de datos de Juztina.

Los atributos que esas hojas ya usan tienen su campo en el diccionario:

| Atributo en las hojas de Bolivia | Campo |
| --- | --- |
| Institución que emite | MDJ-D02-001 `organismo_emisor` |
| Institución que custodia | MDJ-D02-014 `custodio` |
| Link | MDJ-D01-021 `url_oficial` |
| Estado del link y fecha de verificación | MDJ-D02-024 y MDJ-D02-025 |
| Acceso | MDJ-D16-001 `acceso_fuente` |
| ¿Publica texto completo? | MDJ-D16-007 |
| Indexación / ISSN | MDJ-D17-014 y MDJ-D02-044 |
| Nivel | MDJ-D04-013 `nivel_academico` |
| Tipo de fuente | MDJ-D02-042 `tipo_publicacion_fuente` |
| Cobertura / periodicidad | MDJ-D02-049 y MDJ-D02-045 |

Los laudos y las actas de conciliación de esas hojas tienen naturaleza jurídica propia (CAT-003: NJ14 y NJ15). Su colección sigue pendiente (DEC-07), como estableció la arquitectura.

## 3. Cómo se construyó el inventario

1. **Esquema común** (`fuente/esquema.py`). Fija los atributos de cada campo y los vocabularios cerrados de cada atributo: dimensiones, perfiles, unidades, tipos de dato, orígenes, métodos, prioridades, modos, etapas, riesgos, países, funcionalidades y decisiones.
2. **Redacción por bloques de dimensiones** (`fuente/campos_g1.py`…`campos_g6.py`). Cada bloque se validó contra el esquema con `validar_modulo.py`, hasta cero errores.
3. **Integración** (`fuente/integracion.py`). Registro auditable de cada decisión tomada al unir los bloques (sección 4).
4. **Generación** (`fuente/construir_excel.py`). Produce el libro. Las hojas derivadas leen el diccionario maestro por fórmula y la cobertura se calcula con fórmulas. Se recalculó con LibreOffice: 42.856 fórmulas, sin errores.

El libro se regenera ejecutando `python3 construir_excel.py` desde `fuente/`. Para mantener la consistencia, conviene editar los módulos y regenerar, no editar el Excel a mano.

## 4. Decisiones de integración

Los bloques se redactaron por dimensiones. Al unirlos se encontraron solapamientos, resueltos así:

| Situación | Decisión |
| --- | --- |
| 12 campos duplicaban otros con distinto nombre o en otra dimensión | Se retiraron antes de publicar la v1.0. Sus IDs quedan **reservados y no se reutilizan**. Las referencias se redirigieron al campo conservado (hoja 15) |
| Firmantes, ponente y composición del órgano figuraban en D2 y en D13 | El registro canónico es el de **actor institucional en D13**, que es más granular (rol, nombre, cargo, órgano y voto). D2 conserva el emisor y el órgano emisor. El catálogo de rol de firma se fusionó en el de rol del actor |
| Dos catálogos de nivel académico | Se conservó el más completo (CAT-317) |
| Dos catálogos llamados «Periodicidad» | No eran duplicados: se renombraron como «de publicación» y «de pago u obligación» |
| Marca de contenido ajeno en D5, D7 y en la capa de procedencia | Un único campo (MDJ-D05-019), que se **calcula** desde los límites de las citas textuales (D7) |
| Tipo de destinatario (CAT-504) y faceta F8 de sujetos | Se mantienen ambos, con la regla de que la faceta F8 se siembra con los valores de CAT-504 |
| La entidad «territorio o jurisdicción» no tenía atributos | Se agregaron 10 campos (MDJ-D08-026 a 035) y 2 catálogos semilla. Era un vacío de cobertura, no un cambio de arquitectura |

## 5. Criterios aplicados

- **Unidad correcta antes que documento completo.** Cada campo se asignó a la unidad de la que se predica: artículo, problema jurídico, punto resolutivo, manifestación, proceso, etc.
- **Afirmaciones compuestas.** Algunos datos solo tienen sentido con varios subcampos: eventos de vigencia, operaciones modificatorias, asignaciones de clasificación, partes, montos, efectos, estados de campo y revisiones. Se modelan como *afirmaciones compuestas*, es decir, registros dependientes de una unidad de registro. Es una precisión de implementación de la arquitectura, que ya los trataba como afirmaciones con valor estructurado. No es una unidad nueva.
- **Hechos, inferencias y conclusiones separados.** El origen del dato distingue ocho modos. Las conclusiones jurídicas, como el estado de vigencia, el carácter de precedente, la especialidad de práctica o el monto final, son siempre «Conclusión jurídica por reglas» en modo B. Nunca las extrae el modelo.
- **Sin topes de clasificación.** Se aplican los criterios de objeto, supresión y consulta, y los controles de la arquitectura (sección C).
- **Minimización de datos personales.** Los nombres y documentos de identidad de personas naturales y los abogados quedan en la clase X, fuera del alcance inicial. Los indicadores de privacidad están en P0.
- **Países.** Ningún catálogo nacional se presenta como validado. Los valores sembrados por país llevan el estado «Semilla — pendiente de validación nacional» (167 valores).

## 6. Hallazgo que requiere decisión: la regla RG-10

La arquitectura v3 (G, regla 10) dice que **toda** afirmación R1 pasa por revisión humana antes de alimentar cálculos. Aplicada literalmente, obliga a revisar cada evento de vigencia, cada operación modificatoria y cada monto ordenado del corpus.

El inventario no modifica la regla. Los 36 campos R1 extraídos o inferidos que figuraban sin revisión pasaron a «Condicionado», con esta condición:

> Revisión obligatoria antes de alimentar cálculos; solo puede ser muestral si el piloto demuestra una precisión igual o superior a la meta R1.

Esos campos quedaron vinculados a DEC-20. **Producto debe confirmar o rechazar esta interpretación** según su capacidad real de revisión.

## 7. Qué requiere validación

| Validación | Quién | Decisiones |
| --- | --- | --- |
| Reglas y catálogos nacionales: tipos documentales, rangos, precedentes, efectos de vigencia, fuerza de los pronunciamientos administrativos, códigos territoriales, unidades de valor | Responsable jurídico de cada país | DEC-03, 04, 08, 14, 17, 25, 26, 28, 29, 34 |
| Política de datos personales | Área legal y de privacidad | DEC-18, DEC-19 |
| Uso de doctrina protegida | Área legal | DEC-27 |
| Metas de precisión, corte P1/P2, colecciones de tipos limítrofes, cobertura subnacional | Producto | DEC-07, 20, 22, 31 |
| Alineación con los fragmentos del asistente, insumos intermedios, completitud histórica, claves de organismos | Ingeniería | DEC-09, 24, 32, 33 |
| Reglas de especialidades de práctica, responsables de la taxonomía, umbrales de sobreclasificación | Comité taxonómico y especialistas | DEC-11, 12, 13 |
