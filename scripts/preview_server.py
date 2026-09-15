#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preview_server.py — Sert le tableau de bord (`preview/`) et le corpus lui-même.

  * écoute sur 0.0.0.0 (accessible depuis l'aperçu navigateur)
  * `/` redirige vers `/preview/`
  * `.git` et `scripts/` ne sont jamais servis
  * les PDF/txt du corpus restent ouvrables depuis les fiches chapitre

Usage :  python3 scripts/preview_server.py [--port 8000] [--root .]
Python 3.8+ — bibliothèque standard uniquement.
"""
import argparse
import functools
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BLOCKED = ("/.git", "/scripts/", ".pyc")


class Handler(SimpleHTTPRequestHandler):
    server_version = "CorpusPreview/1.0"

    def translate_path(self, path):
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if any(b in clean for b in BLOCKED):
            return os.path.join(self.directory, "__blocked__")
        return SimpleHTTPRequestHandler.translate_path(self, path)

    def do_GET(self):
        clean = self.path.split("?", 1)[0].split("#", 1)[0]
        if clean in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/preview/")
            self.end_headers()
            return
        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--root", default=".", help="racine du dépôt (servie)")
    a = ap.parse_args()

    root = os.path.abspath(a.root)
    if not os.path.exists(os.path.join(root, "preview", "data.json")):
        print("⚠ preview/data.json absent — lancez : python3 scripts/build_preview.py",
              file=sys.stderr)

    handler = functools.partial(Handler, directory=root)
    httpd = ThreadingHTTPServer((a.host, a.port), handler)
    httpd.daemon_threads = True
    print("Corpus 2BAC PC — tableau de bord")
    print("  racine servie : %s" % root)
    print("  écoute        : http://%s:%d/  →  /preview/" % (a.host, a.port))
    print("  (.git et scripts/ non servis)")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\narrêt.")


if __name__ == "__main__":
    main()
