# Etapa 2: inventario exhaustivo de metadatos jurídicos de Juztina

Carpeta de entregables de la Etapa 2. Se construyó sobre la arquitectura conceptual versión 3 (final). No modifica los documentos de etapas anteriores.

| Archivo | Contenido |
| --- | --- |
| `Juztina_Diccionario_Maestro_Metadatos_v1.0.xlsx` | Diccionario maestro: 624 campos, 148 catálogos, 61 tipos de relación, 20 hojas. Incluye la **taxonomía de etiquetas jurídicas** (hoja `5b`: 245 etiquetas) y los **especialistas de Juztina** definidos como selección de etiquetas (hoja `5c`). Empezar por la hoja `1_README` |
| `01_Decisiones_metodologicas.md` | Cómo se construyó el inventario, decisiones de integración, hallazgos y validaciones requeridas |
| `02_Resumen_ejecutivo.md` | Resultados cuantitativos principales |
| `03_Riesgos_limitaciones_y_pendientes.md` | Riesgos, limitaciones y decisiones pendientes antes de implementar |
| `fuente/taxonomia.py` | Fuente de la taxonomía de etiquetas y de los especialistas |
| `fuente/` | Fuente reproducible del Excel: esquema, validador, módulos de campos por bloque, capa de integración y generador |

Para regenerar el Excel:

```bash
cd etapa2_inventario_metadatos/fuente && python3 construir_excel.py
```

Las fórmulas se calculan al abrir el libro en Excel. Para recalcularlas sin Excel, usar LibreOffice.
