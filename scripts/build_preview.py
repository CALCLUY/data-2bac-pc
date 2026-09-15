#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_preview.py — Génère `preview/data.json`, la source du tableau de bord.

Ne contient AUCUNE donnée écrite à la main : tout est relu du dépôt.
  * état « après »  = arbre de travail courant (inventaire réel du disque)
  * état « avant »  = commit de référence BASELINE (lu via git ls-tree / git show)
  * intégrité PDF   = en-tête %PDF, comptage /Type /Pages, MD5 anti-doublon
  * liens           = extraits des fichiers *_Liens.md

Usage :  python3 scripts/build_preview.py [--root .] [--out preview/data.json]
Python 3.8+ — bibliothèque standard uniquement.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date

# Commit précédent l'audit du 14/09/2026 — sert d'état de référence « avant ».
BASELINE = "6f251da"

URL_RE = re.compile(r"https?://[^\s)\]<>\"']+")

MATIERE_LABEL = {
    "Mathematiques": "Mathématiques",
    "Physique_Chimie": "Physique-Chimie",
    "SVT": "SVT",
}
MATIERE_ORDER = ["Mathematiques", "Physique_Chimie", "SVT"]

# Libellés lisibles des chapitres (affichage uniquement).
CHAPTER_LABEL = {
    "Examens_nationaux_et_regionaux": "Examens nationaux & devoirs (tous chapitres)",
}


# ---------------------------------------------------------------------------
# Classification des documents par type
# ---------------------------------------------------------------------------
def doc_type(fname):
    b = fname.lower()
    if re.search(r"(examen|national|watani)", b) and re.search(r"(corrig|indication|reponse)", b):
        return "exam_corr"
    if re.search(r"(examen|national|watani|cadre_de_reference)", b):
        return "exam"
    if re.search(r"(corrig|correction|indication|reponse)", b):
        return "corr"
    if re.search(r"(exercice|devoir|sujets?|annales|quiz)", b):
        return "ex"
    if re.search(r"(fiche|r[eé]sum|formule|revision)", b):
        return "fiche"
    if re.search(r"(document|exploitation|activit)", b):
        return "doc"
    if re.search(r"(cours|lesson|le[cç]on)", b):
        return "cours"
    return "autre"


TYPE_LABEL = {
    "cours": "Cours",
    "ex": "Exercices",
    "corr": "Corrigés",
    "exam": "Examens",
    "exam_corr": "Examens corrigés",
    "fiche": "Fiche / résumé",
    "doc": "Documents d'exploitation",
    "autre": "Autre",
}


def is_index(fname):
    return fname.lower().endswith("_liens.md")


# ---------------------------------------------------------------------------
# Intégrité PDF (sans dépendance externe)
# ---------------------------------------------------------------------------
def pdf_probe(path):
    data = open(path, "rb").read()
    ok = data.lstrip().startswith(b"%PDF")
    pages = None
    m = re.findall(rb"/Type\s*/Pages\b[^>]{0,500}?/Count\s+(\d+)", data, re.S)
    if m:
        pages = max(int(x) for x in m)
    if not pages:
        m = re.findall(rb"/Count\s+(\d+)", data)
        if m:
            pages = max(int(x) for x in m)
    if not pages:
        pages = len(re.findall(rb"/Type\s*/Page\b(?!s)", data))
    return {
        "valid": ok,
        "pages": pages,
        "fonts": len(re.findall(rb"/Font\b", data)),
        "images": len(re.findall(rb"/Subtype\s*/Image\b", data)),
    }


# ---------------------------------------------------------------------------
# Index *_Liens.md : extraction des liens
# ---------------------------------------------------------------------------
def parse_index(text):
    out = []
    current = "Document"
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        for field in ("Type :", "Type:"):
            if s.lower().startswith("type") and field[0].lower() in s.lower() and ":" in s:
                if re.match(r"^[-*]?\s*type\s*:", s, re.I):
                    current = re.split(r"[:|]", s, 1)[1].strip() or "Document"
        if "lien direct" in s.lower() or URL_RE.search(s):
            for u in URL_RE.findall(s):
                out.append({"url": u, "type": current})
    # dédoublonnage en préservant l'ordre
    seen, uniq = set(), []
    for e in out:
        if e["url"] not in seen:
            seen.add(e["url"])
            uniq.append(e)
    return uniq


# ---------------------------------------------------------------------------
# Inventaire de l'arbre de travail
# ---------------------------------------------------------------------------
def scan_worktree(corpus_dir):
    chapters = {}
    for mat in sorted(os.listdir(corpus_dir)):
        mp = os.path.join(corpus_dir, mat)
        if not os.path.isdir(mp) or mat not in MATIERE_LABEL:
            continue
        for chap in sorted(os.listdir(mp)):
            cp = os.path.join(mp, chap)
            if not os.path.isdir(cp):
                continue
            entry = chapters.setdefault((mat, chap), {"docs": [], "links": []})
            for f in sorted(os.listdir(cp)):
                fp = os.path.join(cp, f)
                if not os.path.isfile(fp):
                    continue
                if is_index(f):
                    entry["links"] = parse_index(open(fp, encoding="utf-8").read())
                    continue
                ext = f.rsplit(".", 1)[-1].lower()
                d = {
                    "name": f,
                    "ext": ext,
                    "type": doc_type(f),
                    "size": os.path.getsize(fp),
                    "md5": None,
                    "pages": None,
                    "valid": None,
                    "fonts": None,
                    "images": None,
                }
                if ext == "pdf":
                    d["md5"] = hashlib.md5(open(fp, "rb").read()).hexdigest()
                    d.update(pdf_probe(fp))
                entry["docs"].append(d)
    return chapters


# ---------------------------------------------------------------------------
# Inventaire de l'état de référence (git)
# ---------------------------------------------------------------------------
def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def scan_baseline(corpus_prefix):
    listing = git("ls-tree", "-r", BASELINE, "--name-only")
    if listing is None:
        return None
    counts = defaultdict(lambda: defaultdict(int))
    links = defaultdict(set)
    for path in listing.split("\n"):
        if not path.startswith(corpus_prefix):
            continue
        parts = path.split("/")
        if len(parts) < 4:
            continue
        mat, chap, fname = parts[1], parts[2], parts[3]
        if mat not in MATIERE_LABEL:
            continue
        if is_index(fname):
            blob = git("show", "%s:%s" % (BASELINE, path)) or ""
            for u in URL_RE.findall(blob):
                links[(mat, chap)].add(u)
        else:
            counts[(mat, chap)][doc_type(fname)] += 1
    out = {}
    for key in set(list(counts.keys()) + list(links.keys())):
        c = counts.get(key, {})
        out[key] = {
            "docs": sum(c.values()),
            "types": dict(c),
            "links": len(links.get(key, ())),
        }
    return out


# ---------------------------------------------------------------------------
# Statut d'un chapitre
# ---------------------------------------------------------------------------
def chapter_status(types, ndocs, is_exam_folder=False):
    has_ex = (types.get("ex", 0) + types.get("corr", 0) + types.get("exam_corr", 0)) > 0
    has_exam = (types.get("exam", 0) + types.get("exam_corr", 0)) > 0
    has_cours = types.get("cours", 0) > 0
    gaps = []
    # Un dossier d'examens n'a pas vocation à contenir un cours : on ne le
    # signale pas comme manquant (sinon le statut serait faussement dégradé).
    if not is_exam_folder and not has_cours:
        gaps.append("cours complet")
    if not has_ex:
        gaps.append("exercices corrigés")
    if not has_exam:
        gaps.append("sujets d'examens")
    if ndocs == 0:
        status = "vide"
    elif not gaps and ndocs >= 3:
        status = "complet"
    elif ndocs <= 1 or len(gaps) >= 2:
        status = "critique"
    else:
        status = "incomplet"
    return status, gaps


# ---------------------------------------------------------------------------
def build(root, out_path):
    corpus = os.path.join(root, "2BAC_PC_Corpus")
    wt = scan_worktree(corpus)
    base = scan_baseline("2BAC_PC_Corpus/")

    # doublons MD5
    by_md5 = defaultdict(list)
    for (mat, chap), e in wt.items():
        for d in e["docs"]:
            if d["md5"]:
                by_md5[d["md5"]].append("%s/%s/%s" % (mat, chap, d["name"]))
    dupes = [v for v in by_md5.values() if len(v) > 1]
    dupe_set = {p for grp in dupes for p in grp}

    chapters = []
    for (mat, chap), e in sorted(
        wt.items(), key=lambda kv: (MATIERE_ORDER.index(kv[0][0]), kv[0][1])
    ):
        types = defaultdict(int)
        for d in e["docs"]:
            types[d["type"]] += 1
        b = (base or {}).get((mat, chap), {"docs": 0, "links": 0, "types": {}})
        is_exam = chap == "Examens_nationaux_et_regionaux"
        status, gaps = chapter_status(types, len(e["docs"]), is_exam)
        for d in e["docs"]:
            d["dupe"] = ("%s/%s/%s" % (mat, chap, d["name"])) in dupe_set
            d["scanned"] = bool(d["ext"] == "pdf" and d["fonts"] == 0)
        chapters.append(
            {
                "matiere": mat,
                "matiere_label": MATIERE_LABEL[mat],
                "dir": chap,
                "label": CHAPTER_LABEL.get(chap, chap),
                "is_exam_folder": chap == "Examens_nationaux_et_regionaux",
                "status": status,
                "gaps": gaps,
                "types": {k: v for k, v in types.items()},
                "docs": e["docs"],
                "links": e["links"],
                "before": {"docs": b["docs"], "links": b["links"]},
                "after": {"docs": len(e["docs"]), "links": len(e["links"])},
            }
        )

    totals = {
        "docs": sum(c["after"]["docs"] for c in chapters),
        "docs_before": sum(c["before"]["docs"] for c in chapters),
        "links": sum(c["after"]["links"] for c in chapters),
        "links_before": sum(c["before"]["links"] for c in chapters),
        "pdf": sum(1 for c in chapters for d in c["docs"] if d["ext"] == "pdf"),
        "txt": sum(1 for c in chapters for d in c["docs"] if d["ext"] == "txt"),
        "pages": sum(d["pages"] or 0 for c in chapters for d in c["docs"] if d["ext"] == "pdf"),
        "invalid": sum(1 for c in chapters for d in c["docs"] if d["ext"] == "pdf" and not d["valid"]),
        "scans": sum(1 for c in chapters for d in c["docs"] if d.get("scanned")),
        "dupes": len(dupes),
        "chapters": len([c for c in chapters if not c["is_exam_folder"]]),
        "vide": sum(1 for c in chapters if c["status"] == "vide"),
        "critique": sum(1 for c in chapters if c["status"] == "critique"),
        "incomplet": sum(1 for c in chapters if c["status"] == "incomplet"),
        "complet": sum(1 for c in chapters if c["status"] == "complet"),
        "sans_exercice": sum(1 for c in chapters if "exercices corrigés" in c["gaps"]),
        "sans_examen": sum(
            1 for c in chapters if "sujets d'examens" in c["gaps"] and not c["is_exam_folder"]
        ),
        "bytes": sum(d["size"] for c in chapters for d in c["docs"]),
    }

    report_path = os.path.join(corpus, "AUTOCONTROLE_RAPPORT.md")
    report = open(report_path, encoding="utf-8").read() if os.path.exists(report_path) else ""

    data = {
        "generated": date.today().isoformat(),
        "baseline": BASELINE,
        "totals": totals,
        "chapters": chapters,
        "dupes": dupes,
        "report_md": report,
        "type_labels": TYPE_LABEL,
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--root", default=".", help="racine du dépôt")
    ap.add_argument("--out", default="preview/data.json", help="fichier de sortie")
    a = ap.parse_args()
    d = build(a.root, a.out)
    t = d["totals"]
    print("data.json écrit : %s" % a.out)
    print(
        "  %d chapitres · %d documents (avant %d) · %d liens (avant %d) · %d pages · %d doublons"
        % (
            t["chapters"],
            t["docs"],
            t["docs_before"],
            t["links"],
            t["links_before"],
            t["pages"],
            t["dupes"],
        )
    )
    print(
        "  statuts : %d complet · %d incomplet · %d critique · %d vide"
        % (t["complet"], t["incomplet"], t["critique"], t["vide"])
    )
    if t["invalid"]:
        print("  ⚠ %d PDF invalides" % t["invalid"], file=sys.stderr)


if __name__ == "__main__":
    main()
