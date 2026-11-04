# Centro de Inteligencia Metalúrgica — Prototipo

Motor de cálculo metalúrgico (grado de liberación, asociaciones, intercrecimientos,
tamaños) en Python, con base de datos e interfaz web. Reemplaza el motor VBA del
Excel `Analizar.xlsm`, **dando exactamente los mismos números** (validado 67/67
celda por celda contra tu libro real).

## Qué incluye
| Archivo | Función |
|---|---|
| `importer.py` | Lee una hoja de registro (CAB+140, etc.) tal como la interpreta el VBA |
| `engine.py`   | Motor de cálculo (réplica fiel de los resúmenes) |
| `db.py`       | Base de datos SQLite (muestras, libres, partículas) |
| `report.py`   | Arma las tablas de resultados |
| `app.py`      | Interfaz web (Streamlit) |
| `validate.py` | Compara el motor contra el Excel y reporta diferencias |

## Instalar y ejecutar
```bash
pip install -r requirements.txt
streamlit run app.py
```
Se abre en el navegador. Importa tu `.xlsm`, elige la hoja y calcula; o abre una
muestra ya guardada en la base de datos.

## Validar contra tu Excel (opcional)
```bash
python validate.py "ruta/Analizar.xlsm" "CAB+140"
```

## Roadmap (hacia el Centro de Inteligencia)
- **Fase 1 (esto):** motor validado + BD + visor web. Importa desde Excel.
- **Fase 2:** formulario de captura en la web (reemplaza el UserForm1) → dejar de depender de Excel.
- **Fase 3:** histórico y comparación entre muestras, reportes PDF automáticos.
- **Fase 4:** multiusuario (PostgreSQL + hosting) para el equipo.
- **Fase 5:** capa de inteligencia: tendencias, alertas y optimización.

## Notas
- `engine.py` replica el VBA incluil los criterios de rango (tamaños ≤20/≤75/≤106/>106,
  perímetros 0-20/21-49/50-80/81-100) y la ponderación por Área×Conteo.
- La base de datos vive en `metalurgia.db` (se crea sola).
