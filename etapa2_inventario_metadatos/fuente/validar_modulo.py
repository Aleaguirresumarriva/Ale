"""Valida un módulo campos_gN.py contra esquema.py.  Uso: python3 validar_modulo.py campos_g1.py"""
import importlib.util, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import esquema as E

def load(path):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def check(path):
    m = load(path); errs = []
    keys = [k for k, _ in E.CAMPO_CLAVES]
    ids, techs = set(), set()
    for f in m.FIELDS:
        fid = f.get("id", "?")
        miss = [k for k in keys if k not in f]; extra = [k for k in f if k not in keys]
        if miss: errs.append(f"{fid}: faltan {miss}")
        if extra: errs.append(f"{fid}: claves extra {extra}")
        for k in keys:
            v = f.get(k)
            if v is None or (isinstance(v, str) and not v.strip()): errs.append(f"{fid}: '{k}' vacío")
        if not re.fullmatch(r"MDJ-(D\d\d|PRO|OPE)-\d{3}", fid): errs.append(f"{fid}: formato de ID")
        elif fid.split("-")[1] not in E.DIMENSIONES: errs.append(f"{fid}: prefijo de dimensión desconocido")
        if fid in ids: errs.append(f"{fid}: ID duplicado")
        ids.add(fid)
        t = f.get("tech", "")
        if not re.fullmatch(r"[a-z][a-z0-9_]*", t): errs.append(f"{fid}: tech no snake_case ascii: {t}")
        if t in techs: errs.append(f"{fid}: tech duplicado {t}")
        techs.add(t)
        if f.get("dim") not in E.DIMENSIONES: errs.append(f"{fid}: dim {f.get('dim')}")
        for p in str(f.get("profiles", "")).split("; "):
            if p not in E.PERFILES: errs.append(f"{fid}: perfil {p}")
        if f.get("unit") not in E.UNIDADES: errs.append(f"{fid}: unidad {f.get('unit')}")
        if f.get("dtype") not in E.TIPOS_DATO: errs.append(f"{fid}: dtype {f.get('dtype')}")
        if f.get("card") not in E.CARDINALIDADES: errs.append(f"{fid}: card {f.get('card')}")
        if f.get("origin") not in E.ORIGENES: errs.append(f"{fid}: origin {f.get('origin')}")
        for mm in str(f.get("method", "")).split(" + "):
            if mm not in E.METODOS: errs.append(f"{fid}: method {mm}")
        if f.get("prio") not in E.PRIORIDADES: errs.append(f"{fid}: prio")
        if f.get("mode") not in E.MODOS: errs.append(f"{fid}: mode")
        if (f.get("mode") == "X") != (f.get("prio") == "Fuera de alcance"): errs.append(f"{fid}: X <-> Fuera de alcance")
        if f.get("review") not in E.REVISION: errs.append(f"{fid}: review")
        if f.get("privacy") not in E.PRIVACIDAD: errs.append(f"{fid}: privacy")
        if f.get("stage") not in E.ETAPAS: errs.append(f"{fid}: stage")
        if f.get("risk") not in E.RIESGOS: errs.append(f"{fid}: risk")
        c = f.get("countries", "")
        if c != "ALL":
            for p in c.split("; "):
                if p not in E.PAISES: errs.append(f"{fid}: país {p}")
        if f.get("country_status") not in E.ESTADO_PAIS: errs.append(f"{fid}: country_status")
        fu = f.get("funcs", "")
        if not fu.startswith("No aplica"):
            for x in fu.split("; "):
                if x not in E.FUNCIONALIDADES: errs.append(f"{fid}: func {x}")
        pe = f.get("pending", "")
        if pe != "No":
            for x in pe.split("; "):
                if x not in E.DECISIONES: errs.append(f"{fid}: decisión {x}")
    cats = getattr(m, "CATALOGS", [])
    for c in cats:
        for k in ("cat_id", "cat_name", "cat_def", "values"):
            if k not in c: errs.append(f"catálogo {c.get('cat_id')}: falta {k}")
        for v in c.get("values", []):
            for k in ("code", "label", "definition"):
                if not v.get(k): errs.append(f"{c.get('cat_id')}: valor sin {k}")
    return errs, len(m.FIELDS), len(cats)

if __name__ == "__main__":
    errs, n, nc = check(sys.argv[1])
    print(f"campos={n} catalogos={nc} errores={len(errs)}")
    for e in errs[:80]: print(" -", e)
