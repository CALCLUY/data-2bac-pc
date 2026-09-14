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

## 4. Récapitulatif (Étape 5)

| Matière | Chapitre | Nb de documents | Types couverts |
|---------|----------|:---:|----------------|
| Mathématiques | 01 Limites et continuité | 3 | Cours |
| Mathématiques | 02 Dérivation et étude des fonctions | 2 | Cours |
| Mathématiques | 03 Suites numériques | 4 | Cours + Examens par thème |
| Mathématiques | 04 Fonctions primitives | 1 | Cours |
| Mathématiques | 05 Fonctions logarithmiques | 4 | Cours + Fiche + Examens |
| Mathématiques | 06 Nombres complexes (P1) | 4 | Cours + Fiche + Examens |
| Mathématiques | 07 Fonctions exponentielles | 4 | Cours + Fiche + Examens |
| Mathématiques | 08 Nombres complexes (P2) | 2 | Cours + Examens |
| Mathématiques | 09 Calcul intégral | 4 | Cours + Fiche + Examens (+ texte) |
| Mathématiques | 10 Équations différentielles | 1 | Cours |
| Mathématiques | 11 Géométrie dans l'espace | 5 | Cours + Fiche + Examens |
| Mathématiques | 12 Dénombrement et probabilités | 5 | Cours + Fiche + Examens |
| Mathématiques | **Examens complets 2016→2026** | **21** | Examens nat. + corrigés |
| Physique-Chimie | 01 Ondes mécaniques progressives | 8 | Cours + Exercices |
| Physique-Chimie | 02 Ondes mécaniques progress. périodiques | 2 | Cours + Exercices |
| Physique-Chimie | 03 Propagation des ondes lumineuses | 2 | Cours + Exercices |
| Physique-Chimie | 04 Ondes électromagnétiques & modulation | 1 | Cours |
| Physique-Chimie | 05 Décroissance radioactive | 2 | Cours + Exercices |
| Physique-Chimie | 06 Noyaux, masse et énergie | 2 | Cours + Exercices |
| Physique-Chimie | 07 Dipôle RC | 2 | Cours + Exercices |
| Physique-Chimie | 08 Dipôle RL | 2 | Cours + Exercices |
| Physique-Chimie | 09 Oscillations libres RLC série | 5 | Cours + Exercices |
| Physique-Chimie | 10 RLC série régime sinusoïdal forcé | 1 | Cours (SM) |
| Physique-Chimie | 11 Transformations lentes et rapides | 2 | Cours + Exercices |
| Physique-Chimie | 12 Suivi temporel – vitesse | 2 | Cours + Exercices |
| Physique-Chimie | 13 Transformations dans les 2 sens | 2 | Cours + Exercices |
| Physique-Chimie | 14 État d'équilibre | 2 | Cours + Exercices |
| Physique-Chimie | 15 Réactions acide-base | 1 | Cours |
| Physique-Chimie | 16 Dosage acido-basique | 1 | Cours |
| Physique-Chimie | 17 Lois de Newton | 1 | Cours |
| Physique-Chimie | 18 Chute libre verticale | 2 | Cours |
| Physique-Chimie | 19 Mouvements plans | 2 | Cours |
| Physique-Chimie | 20 Évolution spontanée | 1 | Cours |
| Physique-Chimie | 21 Transformations spontanées (piles) | 1 | Cours |
| Physique-Chimie | 22 Satellites et planètes | 1 | Cours |
| Physique-Chimie | 23 Rotation autour d'un axe fixe | 1 | Cours |
| Physique-Chimie | 24 Systèmes mécaniques oscillants | 2 | Cours |
| Physique-Chimie | 25 Électrolyse | 1 | Cours |
| Physique-Chimie | 26 Aspects énergétiques des oscillations | 2 | Cours |
| Physique-Chimie | 27 Atome et mécanique de Newton | 1 | Cours |
| Physique-Chimie | 28 Estérification et hydrolyse | 1 | Cours |
| Physique-Chimie | 29 Contrôle de l'évolution | 1 | Cours |
| Physique-Chimie | **Examens complets 2021→2026** | **27** | Examens nat. + corrigés |
| SVT | U1 Consommation matière organique / énergie | 14 | Cours + Documents + Exercices |
| SVT | U2 Expression de l'information génétique / génie génétique | 16 | Cours + Documents + Exercices |
| SVT | U3 Reproduction sexuée / génétique humaine | 17 | Cours + Documents + Exercices |
| SVT | U4 Génétique des populations | 2 | Cours + Documents |
| SVT | U5 Immunologie | 8 | Cours + Documents |
| SVT | U6 Chaînes de montagnes / tectonique | 16 | Cours + Documents + Exercices |
| SVT | U7 Écosystèmes | 10 | Examens + Documents (pollution) |
| SVT | **Examens complets 2021→2026** | **16** | Examens nat. + corrigés |

**Total ≈ 260 documents** (liens directs PDF + textes capturés), tous PDF ou texte, dédoublonnés.

## 5. Limites connues
- Certains fascicules YouSVT « élève » manquent côté serveur (les versions « professeur » sont données en secours).
- Les fichiers `*_partiel.txt` sont des extrais (limitation de lecture PDF à 30 pages / pages manquantes) :
  le **PDF complet** reste accessible via le lien direct indiqué en tête de chaque fichier.
- Les cours « partiel » d'AlloSchool (Cours 1..6) couvrent le même chapitre que le « Doc » : seul le Doc complet
  est référencé pour éviter les doublons.
- Examens nationaux avant 2016 : disponibles en livres complets (liens dans les dossiers Examens).
