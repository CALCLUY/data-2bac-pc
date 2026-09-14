# Corpus pédagogique — 2BAC Sciences Physiques (PC), Maroc
**Matières : Mathématiques · Physique-Chimie · SVT**
Date de compilation : 14 septembre 2026 — Filière Sciences Physiques, option française

## ⬇️ Télécharger les PDF (279 documents référencés)

Le corpus est un **index de liens directs vérifiés** (le sandbox de compilation n'avait pas
d'accès réseau vers ces sites). Pour récupérer les PDF dans leurs dossiers, lancez sur
votre machine (Python 3.8+, aucune dépendance) :

```bash
python3 scripts/download_corpus.py            # depuis la racine du dépôt
python3 scripts/download_corpus.py --dry-run  # voir le plan sans télécharger
```

Chaque document est enregistré dans son chapitre :
`2BAC_PC_Corpus/[Matière]/[Chapitre]/[MATIÈRE]_[Chapitre]_[Type].pdf`.
Le script est **idempotent** (re-lance = compléments seulement), gère Google Drive
(y compris le jeton de confirmation), ne conserve que les vrais PDF et écrit un
rapport `2BAC_PC_Corpus/download_report.md` listant les éventuels liens morts.

---

## 1. Programme officiel retenu (filière 2BAC PC, vérifié)

> Source de vérification : « Cadres de référence » de l'examen national (Ministère de l'Éducation Nationale) et
> confrontation avec les **examens nationaux officiels 2025 et 2026 (session normale, filière Sciences Physiques)**
> dont le contenu a été exploité (cf. `*/Examens_nationaux_et_regionaux/`).

### Mathématiques (12 chapitres)
| # | Chapitre | Semestre |
|---|----------|----------|
| 01 | Limites et continuité | 1er |
| 02 | Dérivation et étude des fonctions | 1er |
| 03 | Suites numériques | 1er |
| 04 | Fonctions primitives | 1er |
| 05 | Fonctions logarithmiques | 1er |
| 06 | Nombres complexes (Partie 1) | 1er |
| 07 | Fonctions exponentielles | 2e |
| 08 | Nombres complexes (Partie 2) | 2e |
| 09 | Calcul intégral | 2e |
| 10 | Équations différentielles | 2e |
| 11 | Géométrie dans l'espace (produit scalaire + produit vectoriel) | 2e |
| 12 | Dénombrement et probabilités | 2e |

### Physique-Chimie (29 chapitres)
**1er semestre — Ondes & énergie / Chimie des transformations :**
01 Ondes mécaniques progressives · 02 Ondes mécaniques progressives périodiques · 03 Propagation des ondes lumineuses ·
04 Ondes électromagnétiques et modulation d'amplitude · 05 Décroissance radioactive · 06 Noyaux, masse et énergie ·
07 Dipôle RC · 08 Dipôle RL · 09 Oscillations libres d'un circuit RLC série · 10 Circuit RLC série en régime sinusoïdal forcé (approfondi en SM) ·
11 Transformations lentes et rapides · 12 Suivi temporel d'une transformation chimique – vitesse de réaction ·
13 Transformations chimiques s'effectuant dans les 2 sens · 14 État d'équilibre d'un système chimique ·
15 Transformations liées à des réactions acide-base · 16 Dosage acido-basique

**2e semestre — Mécanique / Chimie (électrochimie & organique) :**
17 Lois de Newton · 18 Chute libre verticale d'un solide (avec et sans frottement) · 19 Mouvements plans (projectile) ·
20 Évolution spontanée d'un système chimique · 21 Transformations spontanées dans les piles · 22 Mouvement des satellites et des planètes ·
23 Mouvement de rotation d'un solide autour d'un axe fixe · 24 Systèmes mécaniques oscillants · 25 Transformations forcées (électrolyse) ·
26 Aspects énergétiques des oscillations mécaniques · 27 Atome et mécanique de Newton ·
28 Réactions d'estérification et d'hydrolyse · 29 Contrôle de l'évolution d'un système chimique

*(Chargée particule en champ électrique = SM uniquement, exclue de la filière PC.)*

### SVT (7 unités — programme révisé en vigueur depuis la rentrée 2024, examens 2025 et 2026)
| # | Unité | Contenu |
|---|-------|---------|
| U1 | Consommation de la matière organique et flux d'énergie | Libération de l'énergie emmagasinée dans la matière organique (respiration, fermentation, glycolyse, cycle de Krebs, chaîne respiratoire) ; Rôle du muscle strié squelettique dans la conversion de l'énergie |
| U2 | Nature et mécanisme de l'expression du matériel génétique – Génie génétique | Nature de l'information génétique ; Expression de l'information génétique ; Génie génétique : principes et techniques |
| U3 | Transfert de l'information génétique au cours de la reproduction sexuée – La génétique humaine | Transfert de l'information génétique (mitose, méiose, fécondation) ; Lois statistiques de la transmission des caractères héréditaires ; La génétique humaine (arbres généalogiques, maladies héréditaires) |
| U4 | La variation et la génétique des populations | Biométrie, variation continue, structure génétique des populations |
| U5 | L'immunologie | Soi/non-soi ; Réponses immunitaires (innée et acquise) ; Dysfonctionnements ; Moyens d'aide au système immunitaire |
| U6 | Les phénomènes géologiques accompagnant la formation des chaînes de montagnes et leur relation avec la tectonique des plaques | Chaînes de montagnes récentes (subduction, collision, obduction) ; Métamorphisme ; Granitisation |
| U7 | Les écosystèmes | Cycles biogéochimiques (ex. cycle du carbone), effet de serre, rôle des écosystèmes et impact des activités humaines *(vérifié : exercice 3 de l'examen national SP 2026 = pergélisol/cycle du carbone ; exercice 3 de 2025 = pollution des eaux/nitrates/STEP)* |

> ⚠️ Le programme SVT a été **réformé pour 2024-2025** : les anciens chapitres de 2BAC (volcanisme, séismologie,
> exploitation des ressources minérales, phylogénétique, écosystèmes au sens ancien) ne sont plus au programme ;
> seuls les 7 unités ci-dessus sont testées aux examens 2025-2026.

---

## 2. Méthodologie et critères de qualité (Étape 3)

1. **Recherche libre du programme** : croisement du programme officiel (cadres de référence MEN) avec les
   examens nationaux officiels 2025 & 2026 (fil. Sciences Physiques) et 2 plateformes de référence.
2. **Sources retenues** (de la plus fiable à la moins) :
   - **KhaymaSVT / AdrarPhysic** : sites de professeurs certifiés ; examens nationaux **officiels** 2021→2026 avec
     **éléments de réponse officiels** (PDF Google Drive, liens directs).
   - **AlloSchool** (Prof. H. Cheddadi) : cours complets en PDF gratuits (grille « element/{id}/pdf »), exercices,
     devoirs et examens corrigés ; contenu conforme au programme officiel.
   - **Fayssal Maths** (fayssalmaths.com) : collections d'**examens nationaux corrigés par thème** 2011→2025 +
     résumés de cours, lien direct par PDF.
   - **YouSVT** (Y. Alandalousi) : fascicules de cours + documents + séries d'exercices avec corrections du nouveau
     programme SVT (PDF directs).
   - **Revisio.ma / Bestcours / Sigmaths / ProfElHamdaoui** : archives d'examens nationaux (liens directs ou PDF).
3. **Filtres** : PDF/texte uniquement (pas de vidéos ni d'images isolées) ; contenus de professeurs ou plateformes
   reconnues ; **dédoublonnage** appliqué (un seul document par version distincte ; les « Correction 1..n » du même
   examen sont regroupées dans le même bloc).
4. **Limite technique** : le bac à sable n'autorise pas le téléchargement binaire direct (sortie réseau bloquée).
   → Chaque document est livré **en lien direct** au format demandé (Étape 4), et les documents les plus importants
   ont en plus été **capturés en texte** (fichiers `*_partiel.txt`, extrais des PDF source, avec lien du PDF complet).

## 3. Structure du corpus

```
2BAC_PC_Corpus/
├── README.md                     ← ce fichier (programme + récapitulatif)
├── Mathematiques/
│   ├── 01_Limites_et_continuite/ … 12_Denombrement_et_probabilites/
│   │     └── <MATIERE>_<Chapitre>_<Type>_Liens.md   (blocs Matière/Chapitre/Type/Lien direct)
│   └── Examens_nationaux_et_regionaux/
├── Physique_Chimie/
│   ├── 01_Ondes_mecaniques_progressives/ … 29_Controle_evolution_systeme_chimique/
│   └── Examens_nationaux_et_regionaux/
└── SVT/
    ├── U1_… … U7_Ecosystemes/
    └── Examens_nationaux_et_regionaux/
```

Format des blocs dans chaque fichier `*Liens.md` :
```
Matière : ...
Chapitre : ...
Type (Cours / Fiche formules / Exercices corrigés / Examen + année) : ...
Lien direct : ...
Source : ...
Notes : ...
```

> Note : depuis la réforme de l'évaluation (2024), l'épreuve de **2BAC est nationale** (50 % de la note finale) ;
> l'examen régional concerne la 1ère BAC. Les « examens régionaux » au sens 2BAC sont donc remplacés ici par
> (a) les examens nationaux 2016→2026, (b) les devoirs/contrôles corrigés et examens blancs classés par chapitre.

## 4. Récapitulatif — **mis à jour par l'audit du 14/09/2026**

> ⚠️ Le tableau ci-dessous remplace l'ancien récapitulatif, qui comptait les documents
> *référencés* et non les documents *réellement présents*. Chiffres obtenus par inventaire
> du disque (contrôle d'en-tête `%PDF`, comptage de pages, MD5 anti-doublon).
> Détail complet, écarts constatés et trous restants : **`AUTOCONTROLE_RAPPORT.md`**.

| Matière | Chapitre | Nb de documents | Liens directs indexés | Types couverts |
|---------|----------|:---:|:---:|----------------|
| Mathématiques | 01 Limites et continuite | 3 | 3 | Cours×3 |
| Mathématiques | 02 Derivation et etude des fonctions | 2 | 6 | Cours×2 |
| Mathématiques | 03 Suites numeriques | 3 | 3 | Cours×1 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | 04 Fonctions primitives | 1 | 1 | Cours×1 |
| Mathématiques | 05 Fonctions logarithmiques | 3 | 3 | Cours×1 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | 06 Nombres complexes partie 1 | 3 | 3 | Cours×1 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | 07 Fonctions exponentielles | 3 | 3 | Cours×1 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | 08 Nombres complexes partie 2 | 2 | 2 | Cours×1 + Examens corrigés×1 |
| Mathématiques | 09 Calcul integral | 4 | 3 | Cours×2 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | 10 Equations differentielles | 2 | 1 | Cours×1 + Exercices×1 |
| Mathématiques | 11 Geometrie dans lespace | 4 | 4 | Cours×2 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | 12 Denombrement et probabilites | 4 | 4 | Cours×2 + Examens corrigés×1 + Fiche×1 |
| Mathématiques | **Examens nationaux & devoirs (tous chapitres)** | 4 | 23 | Examens×2 + Examens corrigés×2 |
| Physique-Chimie | 01 Ondes mecaniques progressives | 2 | 22 | Cours×1 + Fiche×1 |
| Physique-Chimie | 02 Ondes mecaniques progressives periodiques | 1 | 5 | Cours×1 |
| Physique-Chimie | 03 Propagation des ondes lumineuses | 1 | 5 | Cours×1 |
| Physique-Chimie | 04 Ondes electromagnetiques et modulation | 1 | 9 | Cours×1 |
| Physique-Chimie | 05 Decroissance radioactive | 1 | 5 | Cours×1 |
| Physique-Chimie | 06 Noyaux masse et energie | 1 | 5 | Cours×1 |
| Physique-Chimie | 07 Dipole RC | 1 | 5 | Cours×1 |
| Physique-Chimie | 08 Dipole RL | 1 | 5 | Cours×1 |
| Physique-Chimie | 09 Oscillations libres RLC serie | 1 | 11 | Cours×1 |
| Physique-Chimie | 10 RLC serie regime sinusoidal force | 1 | 9 | Cours×1 |
| Physique-Chimie | 11 Transformations lentes et rapides | 1 | 5 | Cours×1 |
| Physique-Chimie | 12 Suivi temporel vitesse de reaction | 1 | 5 | Cours×1 |
| Physique-Chimie | 13 Transformations dans les 2 sens | 1 | 5 | Cours×1 |
| Physique-Chimie | 14 Etat d equilibre | 1 | 5 | Cours×1 |
| Physique-Chimie | 15 Reactions acide base | 1 | 11 | Cours×1 |
| Physique-Chimie | 16 Dosage acido basique | 1 | 11 | Cours×1 |
| Physique-Chimie | 17 Lois de Newton | 1 | 9 | Cours×1 |
| Physique-Chimie | 18 Chute libre verticale | 2 | 14 | Cours×2 |
| Physique-Chimie | 19 Mouvements plans | 2 | 13 | Cours×2 |
| Physique-Chimie | 20 Evolution spontanee | 1 | 9 | Cours×1 |
| Physique-Chimie | 21 Transformations spontanees piles | 1 | 9 | Cours×1 |
| Physique-Chimie | 22 Satellites et planetes | 1 | 9 | Cours×1 |
| Physique-Chimie | 23 Rotation autour axe fixe | 1 | 9 | Cours×1 |
| Physique-Chimie | 24 Systemes mecaniques oscillants | 2 | 13 | Cours×2 |
| Physique-Chimie | 25 Electrolyse | 1 | 9 | Cours×1 |
| Physique-Chimie | 26 Aspects energetiques oscillations | 2 | 12 | Cours×2 |
| Physique-Chimie | 27 Atome et mecanique de Newton | 1 | 3 | Cours×1 |
| Physique-Chimie | 28 Esterification et hydrolyse | 1 | 11 | Cours×1 |
| Physique-Chimie | 29 Controle evolution systeme chimique | 1 | 3 | Cours×1 |
| Physique-Chimie | **Examens nationaux & devoirs (tous chapitres)** | 96 | 124 | Examens×57 + Examens corrigés×39 |
| SVT | **Examens nationaux & devoirs (tous chapitres)** | 59 | 67 | Examens×39 + Examens corrigés×20 |
| SVT | U1 Consommation matiere organique et flux energie | 11 | 17 | Cours×6 + Exercices×4 + Docs×1 |
| SVT | U2 Nature expression information genetique genie genetique | 8 | 20 | Cours×6 + Exercices×2 |
| SVT | U3 Transfert information reproduction sexuee genetique humaine | 11 | 21 | Cours×8 + Exercices×3 |
| SVT | U4 Genetique des populations | 1 | 4 | Cours×1 |
| SVT | U5 Immunologie | 2 | 10 | Cours×2 |
| SVT | U6 Chaines de montagnes et tectonique | 8 | 19 | Cours×5 + Exercices×2 + Autre×1 |
| SVT | U7 Ecosystemes | 12 | 13 | Cours×6 + Exercices×2 + Examens×4 |

**Totaux vérifiés : 280 documents réellement présents · 600 liens directs indexés ·
270 PDF (en-tête valide 270/270) · 2 121 pages · 5 paires de doublons MD5 identifiées.**

### Trous connus non comblés (au 14/09/2026)
- **Physique-Chimie : aucun exercice corrigé dans les 29 chapitres.** Les séries
  d'exercices AlloSchool sont **indexées** (29/29 chapitres) mais non téléchargeables
  depuis ce sandbox (pas d'accès réseau binaire) → lancer
  `python3 scripts/download_corpus.py` sur une machine connectée.
- **SVT U4 et U5 : aucun exercice corrigé** (YouSVT = liens morts ; prof-svt = doublons
  de fichiers Drive ; talamidi = href non exposés).
- **MATH 01, 02, 04 : aucun exercice ni recueil d'examens par thème** (Fayssal Maths ne
  publie pas ces recueils ; bibliothèque libre AlloSchool → HTTP 404).
- **MATH 08** et **SVT U7** contiennent des **doublons MD5** (voir le rapport).
- Examens nationaux de **maths** : 4 documents seulement (2021, 2024 + 2 corrigés).

## 5. Limites connues
- Certains fascicules YouSVT « élève » manquent côté serveur (les versions « professeur » sont données en secours).
- Les fichiers `*_partiel.txt` sont des extrais (limitation de lecture PDF à 30 pages / pages manquantes) :
  le **PDF complet** reste accessible via le lien direct indiqué en tête de chaque fichier.
- Les cours « partiel » d'AlloSchool (Cours 1..6) couvrent le même chapitre que le « Doc » : seul le Doc complet
  est référencé pour éviter les doublons.
- Examens nationaux avant 2016 : disponibles en livres complets (liens dans les dossiers Examens).
