/* Tableau de bord du corpus 2BAC PC — vanilla JS, aucune dépendance.
   Toutes les données viennent de data.json (généré par scripts/build_preview.py). */
(function () {
  "use strict";

  var DATA = null;
  var state = { view: "overview", q: "", mat: "", statut: "", sort: null, dir: 1 };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var TL = {};
  var TYPE_CLASS = { cours: "c", ex: "x", corr: "x", exam: "e", exam_corr: "e", fiche: "", doc: "", autre: "" };
  var STATUS_LABEL = { complet: "Complet", incomplet: "Incomplet", critique: "Critique", vide: "Vide" };
  var STATUS_COLOR = { complet: "var(--ok)", incomplet: "var(--warn)", critique: "var(--bad)", vide: "var(--bad)" };
  var MAT_COLOR = { Mathematiques: "#5aa9ff", Physique_Chimie: "#a78bfa", SVT: "#3ddc97" };

  /* ---------------- helpers ---------------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function ko(n) {
    if (n >= 1048576) return (n / 1048576).toFixed(1) + " Mo";
    if (n >= 1024) return (n / 1024).toFixed(0) + " Ko";
    return n + " o";
  }
  function chapLabel(c) {
    return c.label.replace(/_/g, " ");
  }
  function typesOf(c) {
    return ["cours", "ex", "corr", "exam", "exam_corr", "fiche", "doc", "autre"]
      .filter(function (k) { return c.types[k]; })
      .map(function (k) { return { k: k, n: c.types[k] }; });
  }
  function docPath(c, d) {
    return "../2BAC_PC_Corpus/" + c.matiere + "/" + c.dir + "/" + encodeURIComponent(d.name);
  }
  function filtered() {
    var q = state.q.toLowerCase();
    return DATA.chapters.filter(function (c) {
      if (state.mat && c.matiere !== state.mat) return false;
      if (state.statut && c.status !== state.statut) return false;
      if (!q) return true;
      var hay = (c.matiere_label + " " + chapLabel(c) + " " + typesOf(c).map(function (t) { return TL[t.k]; }).join(" ")).toLowerCase();
      if (hay.indexOf(q) >= 0) return true;
      return c.docs.some(function (d) { return d.name.toLowerCase().indexOf(q) >= 0; });
    });
  }

  /* ---------------- KPI ---------------- */
  function renderKpis() {
    var t = DATA.totals;
    var items = [
      { k: "Documents", v: t.docs, d: "avant <b>" + t.docs_before + "</b> · <span class='up'>+" + (t.docs - t.docs_before) + "</span>" },
      { k: "Liens indexés", v: t.links, d: "avant <b>" + t.links_before + "</b> · <span class='up'>+" + (t.links - t.links_before) + "</span>" },
      { k: "Pages PDF", v: t.pages, d: t.pdf + " PDF · " + t.invalid + " invalide" },
      { k: "Chapitres", v: t.chapters, d: t.complet + " complets · " + (t.chapters - t.complet) + " à compléter" },
      { k: "Sans exercice", v: t.sans_exercice, d: "chapitres concernés", bad: true },
      { k: "Doublons MD5", v: t.dupes, d: "paires identiques", bad: t.dupes > 0 },
      { k: "Volume", v: ko(t.bytes), d: t.txt + " fichiers texte" }
    ];
    $("#kpis").innerHTML = items.map(function (i) {
      return "<div class='kpi'><div class='k'>" + esc(i.k) + "</div>" +
        "<div class='v'" + (i.bad ? " style='color:var(--bad)'" : "") + ">" + esc(i.v) + "</div>" +
        "<div class='d'>" + i.d + "</div></div>";
    }).join("");
    $("#m-date").textContent = "Généré le " + DATA.generated;
    $("#m-base").textContent = DATA.baseline;
    $("#pill-chap").textContent = DATA.chapters;
    $("#pill-dupe").textContent = DATA.dupes;
  }

  /* ---------------- santé ---------------- */
  function renderHealth() {
    var t = DATA.totals;
    var order = ["complet", "incomplet", "critique", "vide"];
    var total = order.reduce(function (a, k) { return a + t[k]; }, 0) || 1;
    $("#stackbar").innerHTML = order.map(function (k) {
      var pct = (t[k] / total) * 100;
      return "<div title='" + STATUS_LABEL[k] + " : " + t[k] + "' style='width:" + pct + "%;background:" + STATUS_COLOR[k] + "'></div>";
    }).join("");
    $("#health-legend").innerHTML = order.map(function (k) {
      return "<span><i style='background:" + STATUS_COLOR[k] + "'></i>" + STATUS_LABEL[k] + " · " + t[k] + "</span>";
    }).join("");
    var cells = [
      { n: t.sans_exercice, l: "chapitres sans exercices corrigés" },
      { n: t.sans_examen, l: "chapitres sans sujets d'examens" },
      { n: t.scans, l: "PDF scannés (non indexables)" },
      { n: t.critique + t.vide, l: "chapitres critiques ou vides" }
    ];
    $("#health-grid").innerHTML = cells.map(function (c) {
      return "<div class='hcell'><div class='n'>" + c.n + "</div><div class='l'>" + esc(c.l) + "</div></div>";
    }).join("");
  }

  /* ---------------- vue : overview ---------------- */
  function renderOverview() {
    var mats = ["Mathematiques", "Physique_Chimie", "SVT"];
    var html = "<div class='grid'>";
    mats.forEach(function (m) {
      var ch = DATA.chapters.filter(function (c) { return c.matiere === m; });
      var docs = ch.reduce(function (a, c) { return a + c.after.docs; }, 0);
      var docsB = ch.reduce(function (a, c) { return a + c.before.docs; }, 0);
      var links = ch.reduce(function (a, c) { return a + c.after.links; }, 0);
      var pages = ch.reduce(function (a, c) {
        return a + c.docs.reduce(function (x, d) { return x + (d.pages || 0); }, 0);
      }, 0);
      var crit = ch.filter(function (c) { return c.status === "critique" || c.status === "vide"; }).length;
      var noEx = ch.filter(function (c) { return c.gaps.indexOf("exercices corrigés") >= 0; }).length;
      var max = Math.max.apply(null, ch.map(function (c) { return c.after.docs; }).concat([1]));
      html += "<div class='card'><div class='mat' style='color:" + MAT_COLOR[m] + "'>" +
        esc(ch[0].matiere_label) + "</div><h3>" + ch.length + " chapitres · " + docs + " documents</h3>" +
        "<div class='num'><div><b>" + docsB + " → " + docs + "</b>documents</div>" +
        "<div><b>" + links + "</b>liens</div><div><b>" + pages + "</b>pages</div></div>" +
        "<div style='display:flex;flex-direction:column;gap:5px;margin-top:2px'>" +
        ch.map(function (c) {
          var w = Math.max(2, (c.after.docs / max) * 100);
          return "<div style='display:flex;gap:8px;align-items:center;font-size:12px'>" +
            "<span style='flex:0 0 130px;color:var(--dim);overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>" + esc(chapLabel(c)) + "</span>" +
            "<span style='flex:1;height:8px;background:var(--bg3);border-radius:5px;overflow:hidden'>" +
            "<span style='display:block;height:100%;width:" + w + "%;background:" + STATUS_COLOR[c.status] + "'></span></span>" +
            "<span style='flex:0 0 22px;text-align:right;color:var(--dim);font-variant-numeric:tabular-nums'>" + c.after.docs + "</span></div>";
        }).join("") + "</div>" +
        (crit ? "<div class='gap crit'>" + crit + " chapitre(s) critique(s)</div>" : "") +
        (noEx ? "<div class='gap'>" + noEx + " chapitre(s) sans exercices corrigés</div>" : "") +
        "</div>";
    });
    html += "</div>";

    var worst = DATA.chapters.filter(function (c) { return c.status === "vide" || c.status === "critique"; });
    if (worst.length) {
      html += "<h2 style='margin:26px 0 12px;font-size:17px'>Chapitres prioritaires (" + worst.length + ")</h2><div class='grid'>";
      worst.forEach(function (c) { html += cardHtml(c, true); });
      html += "</div>";
    }
    return html;
  }

  /* ---------------- carte chapitre ---------------- */
  function cardHtml(c, compact) {
    var delta = c.after.docs - c.before.docs;
    var t = typesOf(c);
    var h = "<div class='card" + (delta > 0 ? " new" : "") + "'>" +
      "<div class='row' style='justify-content:space-between'>" +
      "<div class='mat' style='color:" + MAT_COLOR[c.matiere] + "'>" + esc(c.matiere_label) + "</div>" +
      "<span class='badge b-" + c.status + "'>" + STATUS_LABEL[c.status] + "</span></div>" +
      "<h3>" + esc(chapLabel(c)) + "</h3>" +
      "<div class='row'>" + t.map(function (x) {
        return "<span class='chip'>" + esc(TL[x.k]) + " <b>" + x.n + "</b></span>";
      }).join("") + "</div>" +
      "<div class='num'><div><b>" + c.before.docs + " → " + c.after.docs + "</b>documents" +
      (delta > 0 ? " <span class='up'>+" + delta + "</span>" : "") + "</div>" +
      "<div><b>" + c.before.links + " → " + c.after.links + "</b>liens</div></div>";
    if (c.gaps.length) {
      h += "<div class='gap" + (c.status === "critique" || c.status === "vide" ? " crit" : "") +
        "'>Manque : " + esc(c.gaps.join(" · ")) + "</div>";
    }
    if (!compact) {
      h += "<details class='doc'><summary>" + c.docs.length + " document(s) · " + c.links.length + " lien(s)</summary>";
      if (c.docs.length) {
        h += "<ul class='files'>" + c.docs.map(function (d) {
          var tags = "<span class='tag " + (TYPE_CLASS[d.type] || "") + "'>" + esc(TL[d.type]) + "</span>";
          if (d.dupe) tags += " <span class='tag dupe'>doublon</span>";
          if (d.scanned) tags += " <span class='tag scan'>scan</span>";
          return "<li><span class='nm'><a href='" + esc(docPath(c, d)) + "' target='_blank' rel='noopener'>" +
            esc(d.name) + "</a></span>" + tags +
            "<span class='sz'>" + (d.pages ? d.pages + " p · " : "") + ko(d.size) + "</span></li>";
        }).join("") + "</ul>";
      } else {
        h += "<div class='gap crit'>Aucun document dans ce chapitre.</div>";
      }
      h += "</details>";
    }
    return h + "</div>";
  }

  /* ---------------- vue : chapitres ---------------- */
  function renderChapters() {
    var ch = filtered();
    if (!ch.length) return "<div class='empty'>Aucun chapitre ne correspond à ces filtres.</div>";
    return "<div class='grid'>" + ch.map(function (c) { return cardHtml(c, false); }).join("") + "</div>";
  }

  /* ---------------- vue : tableau ---------------- */
  var COLS = [
    { id: "mat", t: "Matière", get: function (c) { return c.matiere_label; } },
    { id: "chap", t: "Chapitre", get: function (c) { return chapLabel(c); } },
    { id: "stat", t: "Statut", get: function (c) { return STATUS_LABEL[c.status]; } },
    { id: "before", t: "Docs avant", n: 1, get: function (c) { return c.before.docs; } },
    { id: "after", t: "Docs après", n: 1, get: function (c) { return c.after.docs; } },
    { id: "lb", t: "Liens avant", n: 1, get: function (c) { return c.before.links; } },
    { id: "la", t: "Liens après", n: 1, get: function (c) { return c.after.links; } },
    { id: "gaps", t: "Manque", get: function (c) { return c.gaps.join(", "); } },
    { id: "types", t: "Types couverts", get: function (c) {
      return typesOf(c).map(function (x) { return TL[x.k] + "×" + x.n; }).join(" + ");
    } }
  ];

  function renderTable() {
    var ch = filtered();
    if (state.sort) {
      var col = COLS.filter(function (c) { return c.id === state.sort; })[0];
      if (col) {
        ch = ch.slice().sort(function (a, b) {
          var x = col.get(a), y = col.get(b);
          if (typeof x === "number" && typeof y === "number") return (x - y) * state.dir;
          return String(x).localeCompare(String(y), "fr") * state.dir;
        });
      }
    }
    var T = DATA.totals;
    var head = "<tr>" + COLS.map(function (c) {
      var arrow = state.sort === c.id ? (state.dir > 0 ? " ▲" : " ▼") : "";
      return "<th data-sort='" + c.id + "'>" + esc(c.t) + arrow + "</th>";
    }).join("") + "</tr>";
    var body = ch.map(function (c) {
      return "<tr>" + COLS.map(function (col) {
        var v = col.get(c);
        if (col.id === "stat") return "<td><span class='badge b-" + c.status + "'>" + esc(v) + "</span></td>";
        if (col.id === "chap") return "<td><a href='#' data-open='" + esc(c.matiere + "/" + c.dir) + "'>" + esc(v) + "</a></td>";
        if (col.id === "gaps") return "<td>" + (v ? "<span style='color:var(--warn)'>" + esc(v) + "</span>" : "<span style='color:var(--ok)'>—</span>") + "</td>";
        return "<td" + (col.n ? " class='n'" : "") + ">" + esc(v) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    var tot = "<tr class='total'><td colspan='3'>TOTAL (" + ch.length + " lignes affichées)</td>" +
      "<td class='n'>" + ch.reduce(function (a, c) { return a + c.before.docs; }, 0) + "</td>" +
      "<td class='n'>" + ch.reduce(function (a, c) { return a + c.after.docs; }, 0) + "</td>" +
      "<td class='n'>" + ch.reduce(function (a, c) { return a + c.before.links; }, 0) + "</td>" +
      "<td class='n'>" + ch.reduce(function (a, c) { return a + c.after.links; }, 0) + "</td><td></td><td></td></tr>";
    return "<div class='tbl-wrap'><table><thead>" + head + "</thead><tbody>" + body + tot + "</tbody></table></div>" +
      "<p style='color:var(--dim);font-size:12.5px;margin-top:10px'>Corpus entier (non filtré) : " +
      T.docs_before + " → <b>" + T.docs + "</b> documents · " + T.links_before + " → <b>" + T.links + "</b> liens.</p>";
  }

  /* ---------------- vue : doublons ---------------- */
  function renderDupes() {
    if (!DATA.dupes.length) return "<div class='empty'>Aucun doublon MD5 détecté.</div>";
    return "<p style='color:var(--dim);margin-bottom:14px'>" + DATA.dupes.length +
      " paires de fichiers strictement identiques (même empreinte MD5). À purger ou à remplacer par un document distinct.</p>" +
      DATA.dupes.map(function (g, i) {
        return "<div class='dupe'><b>Doublon " + (i + 1) + "</b> — " + g.length + " fichiers identiques" +
          g.map(function (p) { return "<code>" + esc(p) + "</code>"; }).join("") + "</div>";
      }).join("");
  }

  /* ---------------- markdown minimal ---------------- */
  function inline(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<i>$2</i>");
  }
  function md(src) {
    var lines = String(src || "").split("\n"), out = [], i = 0;
    while (i < lines.length) {
      var l = lines[i];
      if (/^\s*$/.test(l)) { i++; continue; }
      if (/^---+\s*$/.test(l)) { out.push("<hr>"); i++; continue; }
      var h = l.match(/^(#{1,4})\s+(.*)$/);
      if (h) { out.push("<h" + h[1].length + ">" + inline(h[2]) + "</h" + h[1].length + ">"); i++; continue; }
      if (/^\s*>/.test(l)) {
        var buf = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) { buf.push(lines[i].replace(/^\s*>\s?/, "")); i++; }
        out.push("<blockquote>" + inline(buf.join(" ")) + "</blockquote>"); continue;
      }
      if (/^\s*\|.*\|\s*$/.test(l)) {
        var rows = [];
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) { rows.push(lines[i].trim()); i++; }
        var cells = function (r) { return r.replace(/^\||\|$/g, "").split("|").map(function (c) { return c.trim(); }); };
        var head = cells(rows[0]);
        var bodyR = rows.slice(2).map(cells);
        out.push("<div class='tbl-wrap'><table><thead><tr>" +
          head.map(function (c) { return "<th>" + inline(c) + "</th>"; }).join("") +
          "</tr></thead><tbody>" +
          bodyR.map(function (r) {
            return "<tr>" + r.map(function (c) { return "<td>" + inline(c) + "</td>"; }).join("") + "</tr>";
          }).join("") + "</tbody></table></div>");
        continue;
      }
      if (/^\s*[-*]\s+/.test(l)) {
        var items = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) { items.push(lines[i].replace(/^\s*[-*]\s+/, "")); i++; }
        out.push("<ul>" + items.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</ul>"); continue;
      }
      var para = [];
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,4}\s|>|\s*\||\s*[-*]\s|---)/.test(lines[i])) {
        para.push(lines[i]); i++;
      }
      out.push("<p>" + inline(para.join(" ")) + "</p>");
    }
    return out.join("\n");
  }
  function renderReport() {
    return "<div class='report'>" + md(DATA.report_md) + "</div>";
  }

  /* ---------------- rendu ---------------- */
  function render() {
    var v = $("#view");
    var showToolbar = state.view === "chapters" || state.view === "table";
    $("#toolbar").style.display = showToolbar ? "flex" : "none";
    if (state.view === "overview") v.innerHTML = renderOverview();
    else if (state.view === "chapters") v.innerHTML = renderChapters();
    else if (state.view === "table") v.innerHTML = renderTable();
    else if (state.view === "dupes") v.innerHTML = renderDupes();
    else v.innerHTML = renderReport();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* ---------------- événements ---------------- */
  function bind() {
    $("#tabs").addEventListener("click", function (e) {
      var b = e.target.closest(".tab");
      if (!b) return;
      $$(".tab").forEach(function (x) { x.classList.remove("active"); });
      b.classList.add("active");
      state.view = b.dataset.view;
      render();
    });
    $("#q").addEventListener("input", function (e) { state.q = e.target.value; render(); });
    $("#f-matiere").addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("#f-matiere button").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on"); state.mat = b.dataset.m; render();
    });
    $("#f-statut").addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("#f-statut button").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on"); state.statut = b.dataset.s; render();
    });
    $("#view").addEventListener("click", function (e) {
      var th = e.target.closest("th[data-sort]");
      if (th) {
        var id = th.dataset.sort;
        state.dir = state.sort === id ? -state.dir : 1;
        state.sort = id; render(); return;
      }
      var a = e.target.closest("a[data-open]");
      if (a) {
        e.preventDefault();
        var key = a.dataset.open.split("/");
        state.mat = key[0]; state.statut = ""; state.q = key[1].replace(/_/g, " ");
        $("#q").value = state.q;
        $$("#f-matiere button").forEach(function (x) { x.classList.toggle("on", x.dataset.m === state.mat); });
        $$(".tab").forEach(function (x) { x.classList.toggle("active", x.dataset.view === "chapters"); });
        state.view = "chapters"; render();
      }
    });
  }

  fetch("data.json").then(function (r) {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  }).then(function (d) {
    DATA = d; TL = d.type_labels;
    renderKpis(); renderHealth(); bind(); render();
  }).catch(function (err) {
    $("#view").innerHTML = "<div class='empty'>Impossible de charger <code>data.json</code> (" +
      esc(err.message) + ").<br>Lancez d'abord : <code>python3 scripts/build_preview.py</code></div>";
  });
})();
