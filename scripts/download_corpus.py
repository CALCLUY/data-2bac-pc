#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_corpus.py — Télécharge les PDF référencés dans l'index 2BAC_PC_Corpus.

Lis tous les fichiers * _Liens.md du corpus, extrait les liens directs
(Lien direct : …, ainsi que les liens documentaires dans les lignes
Source/Notes), et télécharge chaque document dans son dossier de chapitre :

    2BAC_PC_Corpus/[Matière]/[Chapitre]/[MATIÈRE]_[Chapitre]_[Type].pdf

Caractéristiques :
  * Python 3.8+ — bibliothèque standard uniquement (aucun pip install)
  * Idempotent : les PDF déjà téléchargés sont sautés (re-lance = compléments)
  * Google Drive : les liens /file/d/ID/view sont convertis en téléchargement
    direct ; le jeton de confirmation (fichiers > 100 Mo) est géré
  * Validation : seuls les fichiers commençant par %PDF sont conservés
    (les pages HTML / 404 / erreurs sont listées dans le rapport, pas gardés)
  * Poli : délai entre requêtes, 3 tentatives avec backoff, limite 40 Mo/fichier
  * Rapport : 2BAC_PC_Corpus/download_report.md (statuts par URL)

Usage :
    python3 scripts/download_corpus.py                 # télécharge tout
    python3 scripts/download_corpus.py --dry-run       # liste le plan sans télécharger
    python3 scripts/download_corpus.py --root /chemin/vers/2BAC_PC_Corpus
    python3 scripts/download_corpus.py --delay 2       # délai entre requêtes (s)
"""

import argparse
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
URL_RE = re.compile(r"https?://[^\s)\]<>\"']+")
MAX_BYTES = 40 * 1024 * 1024          # 40 Mo / fichier
RETRIES = 3
TIMEOUT = 90

SUBJ_PREFIX = {"Mathematiques": "MATH", "Physique_Chimie": "PC", "SVT": "SVT"}
EXAM_FOLDER = "Examens_nationaux_et_regionaux"


# --------------------------------------------------------------------------
# Outils
# --------------------------------------------------------------------------
def slugify(text, maxlen=40):
    """'Cours complet (résumé)' -> 'Cours_complet'"""
    t = unicodedata.normalize("NFD", text)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.replace("œ", "oe").replace("Œ", "Oe")
    t = re.sub(r"[^A-Za-z0-9]+", "_", t)
    t = re.sub(r"_+", "_", t).strip("_")
    return t[:maxlen].rstrip("_")


def normalize_url(url):
    """Convertis les liens Google Drive /view en téléchargement direct."""
    m = re.match(r"https://drive\.google\.com/file/d/([\w-]+)/view", url)
    if m:
        return ("https://drive.google.com/uc?export=download&id=" + m.group(1))
    return url


def is_downloadable(url):
    """Écarte les liens vers des pages (dossier, catégorie) — on ne télécharge
    que des fichiers (chemin ne finissant pas par '/') et du http(s)."""
    path = urllib.parse.urlsplit(url).path
    return not path.endswith("/")


# --------------------------------------------------------------------------
# Analyse des fichiers _Liens.md
# --------------------------------------------------------------------------
def parse_liens_file(path, subject, folder_name, rel_dir):
    """Renvoie la liste des documents du fichier :
    [ {url, type, name}, ... ]"""
    docs = []
    seen_urls = set()
    chap_slug = ("Examens" if folder_name == EXAM_FOLDER
                 else slugify(folder_name, 60))
    base_prefix = "{}_{}".format(SUBJ_PREFIX.get(subject, subject), chap_slug)

    def add(url, type_label):
        url = normalize_url(url.strip())
        if not is_downloadable(url) or url in seen_urls:
            return
        seen_urls.add(url)
        type_part = type_label.split("—")[0].split("(")[0].strip()
        t_slug = slugify(type_part) or "Document"
        name = "{}_{}".format(base_prefix, t_slug)
        docs.append({"url": url, "type": type_part,
                     "name": name, "rel_dir": rel_dir})

    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    current_type = "Document"
    in_block = False
    for raw in lines:
        line = raw.rstrip("\n")
        s = line.strip()
        if not s:
            continue
        if s.startswith("Matière :"):
            # nouveau bloc — style multi-lignes OU une-ligne (| séparateur)
            in_block = True
            parts = [p.strip() for p in s.split("|")]
            t = "Document"
            for p in parts:
                if p.lower().startswith("type :"):
                    t = p.split(":", 1)[1].strip()
            current_type = t or "Document"
            continue
        if in_block and s.startswith("Type :"):
            current_type = s.split(":", 1)[1].strip() or "Document"
            continue
        if in_block and s.startswith("Lien direct :"):
            for u in URL_RE.findall(s):
                add(u, current_type)
            continue
        if in_block and (s.startswith("Source") or s.startswith("Notes")):
            # liens documentaires intégrés (ex. « rattrapage 2021 : https://… »)
            for u in URL_RE.findall(s):
                add(u, current_type)
            continue
        if s.startswith("#") or s.startswith(">") or s.startswith("➡"):
            in_block = False

    # déduplication des noms (même type → _2, _3 …)
    counters = {}
    for d in docs:
        counters[d["name"]] = counters.get(d["name"], 0) + 1
    counters = dict(counters)
    idx = {}
    for d in docs:
        idx[d["name"]] = idx.get(d["name"], 0) + 1
        if counters[d["name"]] > 1:
            d["name"] = "{}_{}".format(d["name"], idx[d["name"]])
    return docs


def collect(root):
    """Parcourt le corpus et renvoie tous les documents planifiés."""
    all_docs = []
    for subject in sorted(os.listdir(root)):
        subj_dir = os.path.join(root, subject)
        if not os.path.isdir(subj_dir):
            continue
        for folder in sorted(os.listdir(subj_dir)):
            fdir = os.path.join(subj_dir, folder)
            if not os.path.isdir(fdir):
                continue
            for fname in sorted(os.listdir(fdir)):
                if fname.endswith("_Liens.md"):
                    rel_dir = os.path.join(subject, folder)
                    all_docs.extend(parse_liens_file(
                        os.path.join(fdir, fname), subject, folder, rel_dir))
    return all_docs


# --------------------------------------------------------------------------
# Téléchargement
# --------------------------------------------------------------------------
def http_get(url, max_bytes=MAX_BYTES):
    host = urllib.parse.urlsplit(url).netloc
    # Headers aussi complets que ceux d'un navigateur : certains hôtes
    # (yousvt.com / Vercel) refusent les clients "minimaux" (403 anti-bot).
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                   "image/avif,image/webp,*/*;q=0.8"),
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://{}/".format(host),
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = r.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise RuntimeError("fichier > 40 Mo")
        return data


def drive_confirm(data, original_url):
    """Pour les gros fichiers Drive : la première réponse est une page de
    confirmation. On en extrait l'action + le jeton et on relance."""
    action = re.search(rb'action="([^"]+)"', data)
    confirm = re.search(rb'name="confirm"\s+value="([^"]+)"', data)
    uuid = re.search(rb'name="uuid"\s+value="([^"]+)"', data)
    did = re.search(rb'name="id"\s+value="([^"]+)"', data)
    if action and confirm:
        url = action.group(1).decode()
        params = urllib.parse.urlparse(url).query
        params += "&confirm={}".format(confirm.group(1).decode())
        if uuid:
            params += "&uuid={}".format(uuid.group(1).decode())
        if did:
            params += "&id={}".format(did.group(1).decode())
        return url.split("?")[0] + "?" + params
    return None


def download_one(url):
    """Renvoie (octets, note). Lève une exception en cas d'échec."""
    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            data = http_get(url)
            if data[:5] == b"%PDF-" or data[:2] == b"PK":
                return data, None
            # page HTML (Drive confirm, anti-bot, 404 stylisé…)
            nxt = drive_confirm(data, url)
            if nxt:
                data = http_get(nxt)
                if data[:5] == b"%PDF-" or data[:2] == b"PK":
                    return data, None
            ct = b"html"
            if b"<html" in data[:400].lower() or b"<!doctype" in data[:200].lower():
                raise RuntimeError("réponse HTML (page, anti-bot ou 404) — "
                                   "lien probablement mort")
            raise RuntimeError("contenu non PDF ({}…)"
                               .format(data[:24]))
        except urllib.error.HTTPError as e:
            last_err = "HTTP {}".format(e.code)
            if e.code == 404 or e.code == 403:
                raise RuntimeError(last_err) from e
        except RuntimeError:
            raise
        except Exception as e:  # URLError, timeout, TLS…
            last_err = "{}: {}".format(type(e).__name__, e)
        if attempt < RETRIES:
            time.sleep(2 * attempt)
    raise RuntimeError(last_err or "erreur inconnue")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--root", default="2BAC_PC_Corpus",
                    help="dossier du corpus (défaut: ./2BAC_PC_Corpus)")
    ap.add_argument("--dry-run", action="store_true",
                    help="affiche le plan sans télécharger")
    ap.add_argument("--delay", type=float, default=1.0,
                    help="délai entre téléchargements (s, défaut 1.0)")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit("Corpus introuvable : {}".format(root))

    docs = collect(root)
    print("={} Documents planifiés dans {}".format(len(docs), os.path.relpath(root, os.getcwd())))

    if args.dry_run:
        by_dir = {}
        for d in docs:
            by_dir.setdefault(d["rel_dir"], []).append(d)
        for rel in sorted(by_dir):
            print("\n[{}]  {} fichier(s)".format(rel, len(by_dir[rel])))
            for d in by_dir[rel]:
                print("   - {}  <-  {}".format(d["name"] + ".pdf", d["url"]))
        return 0

    results = []   # (rel_dir, name, status, size, url, note)
    for i, d in enumerate(docs, 1):
        target_dir = os.path.join(root, d["rel_dir"])
        target = os.path.join(target_dir, d["name"] + ".pdf")
        os.makedirs(target_dir, exist_ok=True)

        if os.path.isfile(target) and open(target, "rb").read(5) == b"%PDF-":
            results.append((d["rel_dir"], d["name"], "OK (existant)",
                            os.path.getsize(target), d["url"], ""))
            print("[{}/{}] {} — déjà présent".format(i, len(docs),
                                                     d["name"]))
            continue

        print("[{}/{}] {} …".format(i, len(docs), d["name"]), end=" ",
              flush=True)
        try:
            data, note = download_one(d["url"])
            if data[:2] == b"PK":
                target = target[:-4] + ".zip"
                note = "archive ZIP (pas un PDF simple)"
            with open(target, "wb") as fh:
                fh.write(data)
            results.append((d["rel_dir"], d["name"], "OK", len(data),
                            d["url"], note or ""))
            print("OK  {:.1f} Ko".format(len(data) / 1024))
        except Exception as e:
            results.append((d["rel_dir"], d["name"], "ÉCHEC", 0,
                            d["url"], str(e)))
            print("ÉCHEC  ({})".format(e))
        time.sleep(args.delay)

    # ------------------------------------------------------------------
    # Rapport
    # ------------------------------------------------------------------
    ok = sum(1 for r in results if r[2].startswith("OK"))
    fail = [r for r in results if r[2] == "ÉCHEC"]
    report = os.path.join(root, "download_report.md")
    with open(report, "w", encoding="utf-8") as fh:
        fh.write("# Rapport de téléchargement — 2BAC PC Corpus\n\n")
        fh.write("Généré le {} (script `scripts/download_corpus.py`).\n\n"
                 "**Totaux : {} liens — {} téléchargés avec succès, "
                 "{} en échec.**\n\n".format(
                     datetime.now().strftime("%Y-%m-%d %H:%M"),
                     len(results), ok, len(fail)))
        fh.write("## Fichiers téléchargés\n\n"
                 "| Dossier | Fichier | Taille | Lien |\n|---|---|---|---|\n")
        for rel, name, status, size, url, note in results:
            if status.startswith("OK"):
                fh.write("| {} | {}.pdf{} | {:.1f} Ko | {} |\n".format(
                    rel, name, " *" if note else "", size / 1024, url))
        if fail:
            fh.write("\n## Liens en échec (à vérifier / remplacer)\n\n")
            for rel, name, status, size, url, note in fail:
                fh.write("- **{}** ({})\n  - Lien : {}\n  - Cause : {}\n".format(
                    name, rel, url, note))
        fh.write("\n*Re-lancer le script après corrections : seuls les liens "
                 "échoués/manquants seront retentés (idempotent).*\n")

    print("\n=== FIN : {}/{} OK, {} échec(s) ===".format(
        ok, len(results), len(fail)))
    print("Rapport : {}".format(report))
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
