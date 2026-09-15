# Auto-contrôle et complément — Corpus 2BAC PC (Maths · Physique-Chimie · SVT)

**Audit du 14 septembre 2026** — branche `arena/01a0a24d-data-2bac-pc`.
État « avant » = commit `6f251da` (lu via `git ls-tree`/`git show`, pas recopié du README).

> Méthode : inventaire réel du disque (`find` + contrôle de l'en-tête `%PDF` + comptage
> `/Type /Pages` + MD5 anti-doublon). Les index `*_Liens.md` sont comptés à part
> (colonne « liens indexés »), jamais comme documents.

---

## 1. Constat de l'Étape 1 — ce qui était faux ou manquant

### 1.1 Le récapitulatif du README ne correspondait PAS au disque
Le tableau « §4 Récapitulatif » du `README.md` annonçait **≈ 260 documents** avec des
chiffres par chapitre qui ne sont pas ceux réellement présents. Exemples vérifiés :

| Chapitre | README §4 | Réel sur disque | Écart |
|---|:--:|:--:|---|
| Maths — Examens complets | 21 | **4** | −17 |
| PC 01 Ondes mécaniques progressives | 8 | **2** | −6 |
| PC 09 Oscillations libres RLC | 5 | **1** | −4 |
| PC 10 RLC régime sinusoïdal forcé | 1 | **1** | conforme |
| SVT U1 | 14 | **11** | −3 |
| SVT U2 | 16 | **8** | −8 |
| SVT U4 | 2 | **1** | −1 |
| SVT U5 Immunologie | 8 | **0** | −8 |
| SVT U6 | 16 | **8** | −8 |
| SVT U7 | 10 | **12** | +2 |

**Cause identifiée** : le README comptait les documents *référencés* (341 liens),
pas les documents *téléchargés*. Le `download_report.md` déclare lui-même
**341 liens → 270 téléchargés, 71 en échec** (46 × HTTP 429, 23 × HTTP 404,
2 × réponse HTML). Les 71 échecs n'ont jamais été répercutés dans le récapitulatif.

### 1.2 Intégrité des fichiers réellement présents
Contrôles exécutés sur les **270 PDF** présents :
- en-tête `%PDF` valide : **270/270** — aucun fichier corrompu ;
- total de pages détectées : **2 121 pages** ;
- **doublons MD5 exacts : 5 paires** (à traiter) :
  1. `MATH_06_..._Examens_nationaux_corriges_par_theme.pdf` = `MATH_08_..._Examens_nationaux_corriges_par_theme.pdf`
     → le chapitre 08 (Complexes P2) ne possède **pas** de recueil d'examens qui lui soit propre ;
  2. `SVT_Examens_Examen_national_SVT_1.pdf` = `SVT_U7_Ecosystemes_Examen_national_2026_1.pdf`
  3. `SVT_Examens_Examen_national_SVT_2.pdf` = `SVT_U7_Ecosystemes_Examen_national_2026_2.pdf`
  4. `SVT_Examens_Examen_national_SVT_5.pdf` = `SVT_U7_Ecosystemes_Examen_national_2025_1.pdf`
  5. `SVT_Examens_Examen_national_SVT_6.pdf` = `SVT_U7_Ecosystemes_Examen_national_2025_2.pdf`
     → les 4 « examens » du dossier U7 sont des copies du dossier Examens (double comptage) ;
- 14 PDF sont des **scans image** (0 police embarquée) : non indexables en texte plein,
  dont 3 où le comptage de pages échoue (`SVT_U3_..._Cours_complet_3`, `SVT_U3_..._Exercices_2`,
  `SVT_U4_Genetique_des_populations_Cours_complet` — 15 Mo, 74 images).

### 1.3 Trous par type de document (avant complément)
- **47 chapitres sur 48 incomplets** ;
- **27 chapitres avec 0 ou 1 seul document** ;
- **34 chapitres sans aucun exercice ni corrigé** ;
- **39 chapitres sans aucun sujet d'examen** ;
- **SVT U5 Immunologie : 0 document** — le seul chapitre entièrement vide du corpus ;
- **Physique-Chimie : 0 exercice corrigé dans les 29 chapitres.** Les 96 PDF du dossier
  `Examens_nationaux_et_regionaux` sont tous « tous chapitres » ; aucun n'est classé par thème.

---

## 2. Étape 2 — ce qui a été cherché et réellement obtenu

### 2.1 Sources testées dans cet audit
| Source | Verdict du test |
|---|---|
| **AlloSchool** `element/<id>/pdf` | ✅ **Fonctionne** — extraction texte + LaTeX réussie (124444, 124444/pdf) |
| **AlloSchool** index officiel 2BAC **Sciences Physiques BIOF** | ✅ page récoltée → carte complète des 29 chapitres PC (Doc/PDF + exercices + devoirs SPC + examens) |
| **AlloSchool** index officiel 2BAC **Maths BIOF** | ✅ page récoltée (IDs Doc 122859-122865 conformes aux cours déjà présents) |
| **AlloSchool** ancienne bibliothèque libre (éléments 100225/100240/100245…) | ❌ `element/100245/pdf` → **Erreur 404**. Bibliothèque partiellement morte |
| **YouSVT** (Prof. Y. Alandalousi) | ✅ PDF directs **accessibles** (`Cours-Unit5-1.pdf`, `Cours-Unit5-2.pdf`) — les HTTP 429 signalés dans `download_report.md` ne se reproduisent pas |
| **YouSVT** exercices U4/U5 | ❌ liens « # » morts sur la page ; `exercices/5-Ex-Unit5-Sujets.pdf` → « Page non trouvée » |
| **MEN — cadres de référence officiels** | ✅ PDF direct vivant, capturé (filière Sciences Physiques, oct. 2015, 20 p.) |
| **prof-svt (Chbani, Wix)** | ⚠️ cadres de référence OK ; mais les blocs exercices « génétique humaine », « populations », « variation », « immunologie », « géologie » pointent **tous sur les 2 mêmes fichiers Drive** → doublons **rejetés** |
| **talamidi.com** | ❌ les tableaux de téléchargement n'exposent pas leurs `href` → non exploitable |
| **chtoukaphysique.com** | ❌ renvoie vers `/login/` — contenu protégé |
| **NéoSvt** `svt-2bac-pc-examens` | ⚠️ liens réels uniquement pour l'U1 ; U2→U4 = « # » |
| **Scribd / Academia.edu** | non retenus : contenu non vérifiable et hors licence de redistribution |
| Téléchargement binaire depuis le sandbox | ❌ `curl` sans réseau (code 000 sur alloschool/yousvt/example) — seuls les outils de récupération de page ont un accès réseau |

### 2.2 Documents réellement ajoutés (4)
| Fichier | Source | Contenu |
|---|---|---|
| `Mathematiques/10_Equations_differentielles/MATH_10_..._Cours_et_exercices_AlloSchool_124444.txt` | AlloSchool, Prof. Cheddadi | Cours complet (ordre 1 + ordre 2, les 3 cas de Δ) **+ 4 exercices** |
| `SVT/U5_Immunologie/SVT_U5_Immunologie_Cours_complet_1_YouSVT_partiel.txt` | YouSVT, Prof. Alandalousi | Chapitre 1 « Notion de soi et de non soi » |
| `SVT/U5_Immunologie/SVT_U5_Immunologie_Cours_complet_2_YouSVT_partiel.txt` | YouSVT, Prof. Alandalousi | Chapitre 2 « Les moyens de défense de soi » |
| `SVT/Examens_nationaux_et_regionaux/SVT_Examens_Cadre_de_reference_officiel_MEN_filiere_Sciences_Physiques.txt` | **MEN / CNEEO** | Cadre de référence officiel de l'examen national, filière Sciences Physiques |

### 2.3 Index complétés (36 fichiers `*_Liens.md`) + plan de téléchargement
- **29 chapitres de Physique-Chimie** : ajout, pour chacun, du lien direct PDF du cours
  **et des séries d'exercices** AlloSchool (+ documents complémentaires pour 18/19/24/26) ;
- `PC_Examens_nationaux_Liens.md` : examens nationaux 2021 SPC/SM/SVT, **4 devoirs SPC
  corrigés (sujets + 15 corrigés)**, cadres de référence MEN, évaluations diagnostiques ;
- `SVT/U5`, `SVT/U4`, `SVT/Examens`, `MATH/10`, `MATH/02` : compléments + **journal des
  sources testées et rejetées** ;
- **Liens indexés : 368 → 600** (+232).

**Correctif appliqué au parseur.** Au premier passage, `scripts/download_corpus.py`
n'a reconnu **aucun** de ces nouveaux liens (plan inchangé à 341) : le parseur
n'acceptait que les lignes `Matière :` / `Type :` / `Lien direct :` et ignorait les
puces markdown. Vérification préalable faite : `git grep "^- .*Lien direct" HEAD`
→ **aucune occurrence** dans l'état d'origine, donc l'extension est strictement
additive et sans collision. Après correctif :

| | avant correctif | après correctif |
|---|:--:|:--:|
| Documents planifiés par le script | 341 | **437** |
| Chapitres PC avec exercices planifiés | 0/29 | **27/29** |
| Fichiers planifiés pour les 29 chapitres PC | 29 | **126** (dont 66 exercices/corrigés) |

Les 2 chapitres sans exercice planifié — **27 Atome et mécanique de Newton** et
**29 Contrôle de l'évolution d'un système chimique** — correspondent à une absence
réelle : l'index officiel AlloSchool ne liste **aucune** série d'exercices pour eux
(colonne « Exos » vide). Ce n'est pas un oubli de collecte.

**Contrôle exécuté** : `python3 scripts/download_corpus.py --dry-run` → exit 0,
« =437 Documents planifiés dans 2BAC_PC_Corpus ». Le téléchargement effectif des 96
PDF manquants reste impossible ici (`curl` sans réseau binaire, code 000) et doit être
lancé sur une machine connectée.

### 2.4 ⚠ Un point de programme à trancher
Le cadre de référence MEN **octobre 2015** pour la filière **Sciences Physiques**
(capturé dans ce tour) retient 5 domaines et **ne mentionne ni l'immunologie, ni la
génétique des populations, ni les écosystèmes** — qui relèvent du cadre de la filière SVT.
Le dossier `SVT/` du corpus est construit sur le programme SVT en 7 unités (U1→U7).
La version révisée applicable depuis la rentrée 2024 **n'a pas pu être vérifiée ici** :
cette contradiction reste ouverte et doit être tranchée avec le cadre 2024-2025 en vigueur.

---

## 3. Étape 3 — Tableau final mis à jour

| Matière | Chapitre | Nb docs (avant) | Nb docs (après) | Liens indexés (avant→après) | Types couverts (après) |
|---|---|:--:|:--:|:--:|---|
| Mathématiques | 01 Limites et continuite | 3 | **3** | 3 → 3 | Cours×3 |
| Mathématiques | 02 Derivation et etude des fonctions | 2 | **2** | 2 → 6 | Cours×2 |
| Mathématiques | 03 Suites numeriques | 3 | **3** | 3 → 3 | Cours×1 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | 04 Fonctions primitives | 1 | **1** | 1 → 1 | Cours×1 |
| Mathématiques | 05 Fonctions logarithmiques | 3 | **3** | 3 → 3 | Cours×1 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | 06 Nombres complexes partie 1 | 3 | **3** | 3 → 3 | Cours×1 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | 07 Fonctions exponentielles | 3 | **3** | 3 → 3 | Cours×1 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | 08 Nombres complexes partie 2 | 2 | **2** | 2 → 2 | Cours×1 + Examens corrigés×1 |
| Mathématiques | 09 Calcul integral | 4 | **4** | 3 → 3 | Cours×2 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | 10 Equations differentielles | 1 | **2** ⬆ | 1 → 1 | Cours×1 + Exercices×1 |
| Mathématiques | 11 Geometrie dans lespace | 4 | **4** | 4 → 4 | Cours×2 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | 12 Denombrement et probabilites | 4 | **4** | 4 → 4 | Cours×2 + Examens corrigés×1 + Fiche / résumé×1 |
| Mathématiques | **Examens nationaux & devoirs (tous chapitres)** | 4 | **4** | 23 → 23 | Examens×2 + Examens corrigés×2 |
| Physique-Chimie | 01 Ondes mecaniques progressives | 2 | **2** | 8 → 22 | Cours×1 + Fiche / résumé×1 |
| Physique-Chimie | 02 Ondes mecaniques progressives periodiques | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 03 Propagation des ondes lumineuses | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 04 Ondes electromagnetiques et modulation | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 05 Decroissance radioactive | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 06 Noyaux masse et energie | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 07 Dipole RC | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 08 Dipole RL | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 09 Oscillations libres RLC serie | 1 | **1** | 5 → 11 | Cours×1 |
| Physique-Chimie | 10 RLC serie regime sinusoidal force | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 11 Transformations lentes et rapides | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 12 Suivi temporel vitesse de reaction | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 13 Transformations dans les 2 sens | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 14 Etat d equilibre | 1 | **1** | 2 → 5 | Cours×1 |
| Physique-Chimie | 15 Reactions acide base | 1 | **1** | 1 → 11 | Cours×1 |
| Physique-Chimie | 16 Dosage acido basique | 1 | **1** | 1 → 11 | Cours×1 |
| Physique-Chimie | 17 Lois de Newton | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 18 Chute libre verticale | 2 | **2** | 2 → 14 | Cours×2 |
| Physique-Chimie | 19 Mouvements plans | 2 | **2** | 2 → 13 | Cours×2 |
| Physique-Chimie | 20 Evolution spontanee | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 21 Transformations spontanees piles | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 22 Satellites et planetes | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 23 Rotation autour axe fixe | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 24 Systemes mecaniques oscillants | 2 | **2** | 2 → 13 | Cours×2 |
| Physique-Chimie | 25 Electrolyse | 1 | **1** | 1 → 9 | Cours×1 |
| Physique-Chimie | 26 Aspects energetiques oscillations | 2 | **2** | 2 → 12 | Cours×2 |
| Physique-Chimie | 27 Atome et mecanique de Newton | 1 | **1** | 1 → 3 | Cours×1 |
| Physique-Chimie | 28 Esterification et hydrolyse | 1 | **1** | 1 → 11 | Cours×1 |
| Physique-Chimie | 29 Controle evolution systeme chimique | 1 | **1** | 1 → 3 | Cours×1 |
| Physique-Chimie | **Examens nationaux & devoirs (tous chapitres)** | 96 | **96** | 99 → 124 | Examens×57 + Examens corrigés×39 |
| SVT | **Examens nationaux & devoirs (tous chapitres)** | 58 | **59** ⬆ | 57 → 67 | Examens×39 + Examens corrigés×20 |
| SVT | U1 Consommation matiere organique et flux energie | 11 | **11** | 17 → 17 | Cours×6 + Exercices×4 + Documents d'exploitation×1 |
| SVT | U2 Nature expression information genetique genie genetique | 8 | **8** | 20 → 20 | Cours×6 + Exercices×2 |
| SVT | U3 Transfert information reproduction sexuee genetique humaine | 11 | **11** | 21 → 21 | Cours×8 + Exercices×3 |
| SVT | U4 Genetique des populations | 1 | **1** | 3 → 4 | Cours×1 |
| SVT | U5 Immunologie | 0 | **2** ⬆ | 10 → 10 | Cours×2 |
| SVT | U6 Chaines de montagnes et tectonique | 8 | **8** | 19 → 19 | Cours×5 + Exercices×2 + Autre×1 |
| SVT | U7 Ecosystemes | 12 | **12** | 13 → 13 | Cours×6 + Exercices×2 + Examens×4 |
| **TOTAL** | **48 chapitres + 3 dossiers d'examens** | **276** | **280** | **368 → 600** | |

Légende : ⬆ = chapitre effectivement enrichi en documents dans cet audit.

---

## 4. Trous qui restent ouverts (honnêtement)

| Priorité | Trou | Pourquoi il n'est pas comblé |
|---|---|---|
| 🔴 1 | **PC : exercices corrigés présents en PDF** | Les liens sont indexés **et** planifiés (27/29 chapitres, 66 fichiers), mais le sandbox n'a **pas d'accès réseau binaire** (`curl` → 000) : les PDF ne peuvent pas être enregistrés ici. `python3 scripts/download_corpus.py` sur une machine connectée les récupère. Chapitres 27 et 29 : aucun exercice publié par AlloSchool. |
| 🔴 2 | **PC : sujets d'examens classés par chapitre** | Aucun recueil « par thème » trouvé en PC (contrairement aux maths, couverts par Fayssal Maths). |
| 🔴 3 | **SVT U4 & U5 : exercices corrigés** | YouSVT = liens morts ; prof-svt = doublons de fichiers Drive ; talamidi = href non exposés. |
| 🟠 4 | **MATH 01, 02, 04 : exercices + examens par thème** | Fayssal Maths ne publie pas de recueil « Limites », « Dérivation » ni « Primitives » ; la bibliothèque libre AlloSchool renvoie 404 (`element/100245/pdf` testé). |
| 🟠 5 | **MATH 08 Complexes P2** | Son seul « examen » est un **doublon MD5** de celui du chapitre 06. |
| 🟠 6 | **SVT U7** | 4 des 12 documents sont des **doublons MD5** du dossier Examens. |
| 🟡 7 | **MATH : examens nationaux 2016-2020, 2022, 2023, 2025, 2026** | Le README en annonçait 21 ; il n'y en a que **4** sur disque. |
| 🟡 8 | **3 scans PDF non indexables** (SVT U3 ×2, SVT U4) | Nécessitent un OCR. |
