# README - Tableau de Bord de Gestion des Dons de Sang

Bienvenue dans le **Tableau de Bord de Gestion des Dons de Sang**, une application web interactive développée pour analyser les données de dons de sang et prédire l’éligibilité des donneurs potentiels. Ce projet allie modernité, convivialité et puissance analytique pour répondre aux besoins des professionnels de la santé et des gestionnaires de banques de sang.

---

## 🌟 Fonctionnalités du Tableau de Bord

Ce tableau de bord offre une expérience utilisateur riche et intuitive grâce aux modules suivants :

1. **Banque de Sang** :
   - Visualisation compacte et interactive des données de dons de 2019.
   - Graphiques en barres (dons par groupe sanguin et sexe) et en camemberts (répartition des groupes sanguins et types de donation).
   - Filtres dynamiques : groupe sanguin, sexe, âge et mois, permettant une exploration personnalisée.
   - Statistiques détaillées : total des dons, âge moyen, pourcentages par sexe, groupe le plus fréquent.

2. **Prédiction d’Éligibilité** :
   - Formulaire interactif pour saisir les informations personnelles, physiques et sociales d’un donneur potentiel.
   - Prédiction en temps réel de l’éligibilité au don de sang via une API REST déployée.
   - Visualisation des résultats avec une jauge de probabilité (Plotly) et un historique des prédictions.
   - Support bilingue (français/anglais) pour une accessibilité accrue.

3. **Design et Expérience Utilisateur** :
   - Interface moderne avec des cadres stylisés, animations subtiles et tooltips informatifs.
   - Organisation optimisée pour minimiser le défilement et maximiser la lisibilité.

---

## 🛠️ Outils Utilisés

Ce projet repose sur une stack technologique robuste et bien intégrée :

- **Streamlit** : Framework Python pour créer l’interface web interactive et dynamique.
- **Pandas** : Manipulation et analyse des données de dons de sang.
- **Plotly** : Visualisations graphiques avancées (barres, camemberts, jauges) avec interactivité (zoom, hover).
- **FastAPI** : Création d’une API REST rapide et légère pour le modèle de prédiction.
- **Scikit-learn & Joblib** : Chargement et exécution du modèle Random Forest pour les prédictions.
- **Render** : Plateforme de déploiement cloud pour héberger l’API.
- **Git & GitHub** : Gestion de version et collaboration sur le code source.
- **Python 3.11** : Langage principal, choisi pour sa polyvalence et sa communauté.

---

## ⚙️ Hypothèses Faites Lors du Développement

Certaines hypothèses ont guidé le développement pour assurer une implémentation efficace :

1. **Qualité des Données** :
   - Les données dans `2020_clean.csv` sont supposées propres, avec des valeurs cohérentes pour les colonnes comme `groupe_sanguin_abo__rhesus`, `sexe`, `age`, etc.
   - Les dates dans `horodateur` sont au format valide pour une conversion en `pd.to_datetime`.

2. **Modèle de Prédiction** :
   - Le modèle Random Forest (`eligibility_model_rf_no_leak.pkl`) est supposé entraîné sur des données représentatives et sans fuite de données.
   - Les catégories dans le formulaire (ex. profession, religion) correspondent aux mappings définis dans l’API.

3. **Déploiement** :
   - L’API déployée sur Render reste disponible et fonctionnelle dans les limites du tier gratuit (sommeil après 15 min d’inactivité).
   - Les fichiers `.pkl` sont accessibles dans la structure du dépôt GitHub.

4. **Expérience Utilisateur** :
   - Les utilisateurs ont un écran d’au moins 800px de hauteur pour une visualisation optimale sans défilement excessif.
   - Une connexion internet stable est disponible pour interagir avec l’API. `[https://github.com/hyontnick/api_blood_donation]`

---

## 🚀 Instructions pour Exécuter le Tableau de Bord et Interagir avec les Visualisations

### Prérequis
- **Python 3.11+** installé.
- **Git** pour cloner le dépôt.
- Accès à une connexion internet pour l’API déployée.

### Étapes d’Installation
1. **Cloner le Dépôt** :
   ```bash
   git clone https://github.com/hyontnick/qganalytics_blood_dashboard_indabax.git
   cd mon-tableau-de-bord
   ```

2. **Installer les Dépendances** :
   Crée un environnement virtuel (optionnel mais recommandé) et installe les packages :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Le fichier `requirements.txt` devrait inclure :
   ```
   streamlit==1.43.2
   pandas==2.0.0
   numpy==1.24.0
   plotly==5.14.0
   folium==0.19.5
   streamlit-folium==0.24.0
   fastapi==0.115.11
   uvicorn==0.34.0
   joblib==1.2.0
   pydantic==2.8.2
   scikit-learn==1.2.2
   imblearn==0.11.0
   vaderSentiment==3.3.2
   qrcode==8.0
   pillow==9.5.0
   fuzzywuzzy==0.18.0
   python-Levenshtein==0.27.1  # Optionnel, mais recommandé pour fuzzywuzzy
   requests==2.31.0
   matplotlib==3.7.1
   networkx==3.1

   ```

3. **Lancer le Tableau de Bord** :
   Exécute l’application Streamlit :
   ```bash
   streamlit run dashboard.py
   ```
   Ouvre ton navigateur à `http://localhost:8501`.
   pwd: `QG ANALYTICS`

### Comment Interagir avec les Visualisations
Le tableau de bord est conçu pour une interaction fluide et intuitive. Voici comment tirer parti des visualisations :

#### Module "Banque de Sang" :
- **Filtres Dynamiques** :
  - En haut, utilise les 4 filtres (groupe sanguin, sexe, âge, mois) pour personnaliser les données affichées.
  - Exemple : Sélectionne "O+" dans "Groupe Sanguin" et "Juillet" dans "Mois" pour voir les dons correspondants.
- **Graphiques Interactifs** :
  - **Barres** (dons par groupe sanguin/sexe) : Passe la souris pour voir le nombre exact de dons. Clique et fais glisser pour zoomer.
  - **Camemberts** (répartition des groupes/types) : Survole pour voir les pourcentages. Clique sur une section pour la mettre en évidence.
- **Détails** :
  - Les statistiques en bas (ex. total des dons, âge moyen) se mettent à jour en fonction des filtres appliqués.

#### Module "Prédiction d’Éligibilité" :
- **Formulaire** :
  - Remplis les champs organisés en 5 sections (infos personnelles, mesures physiques, etc.).
  - Utilise les tooltips (textes gris sous les champs) pour comprendre les attentes (ex. taux d’hémoglobine minimum).
- **Résultat et Jauge** :
  - Clique sur "Prédire" pour obtenir une prédiction.
  - La jauge Plotly montre la probabilité d’éligibilité (vert > 50%, rouge < 50%). Survole-la pour voir la valeur exacte.
- **Historique** :
  - Ouvre l’expander "Historique des Prédictions" pour voir les 5 dernières prédictions.
  - Clique sur "Effacer l’historique" pour réinitialiser.

#### Conseils d’Interaction :
- **Zoom et Déplacement** : Utilise la barre d’outils Plotly (en haut à droite des graphiques) pour zoomer, déplacer ou exporter en PNG.
- **Réactivité** : Les changements dans les filtres ou le formulaire sont reflétés instantanément dans les visualisations.
- **Bilingue** : Passe à l’anglais via un sélecteur (si implémenté dans `dashboard.py`) pour tester les traductions.

---

## 🌐 Utilisation de l’API de Prédiction

Le module de prédiction repose sur une API REST FastAPI déployée sur Render à l’adresse :  
**`https://api-blood-donation.onrender.com/predict`**

### Fonctionnement
- **Endpoint** : `POST /predict`
- **Entrée** : Un objet JSON avec les 13 champs requis (exemple) :
  ```json
  {
    "age": 25,
    "niveau_detude": "Universitaire",
    "genre": "Homme",
    "taille": 170.0,
    "poids": 70.0,
    "situation_matrimoniale_sm": "Célibataire",
    "profession": "Étudiants",
    "arrondissement_de_residence": "Douala III",
    "nationalite": "Camerounaise",
    "religion": "Christianisme",
    "a_til_elle_deja_donne_le_sang": "Non",
    "si_oui_preciser_la_date_du_dernier_don": "",
    "taux_dhemoglobine": 13.5
  }
  ```
- **Sortie** : Réponse JSON avec le résultat et les probabilités :
  ```json
  {
    "result": "Éligible",
    "probability_eligible": 0.92,
    "probability_not_eligible": 0.08
  }
  ```

### Déploiement de l’API
1. **Structure** :
   - Fichier principal : `api.py`.
   - Fichiers modèles : `eligibility_model_rf_no_leak.pkl`, `scaler_no_leak.pkl`, et un autre `.pkl` (si applicable).
   - Dépendances dans `requirements.txt` incluant `fastapi`, `uvicorn`, `scikit-learn`, etc.

2. **Instructions Locales** (optionnel) :
   - Lance l’API localement :
     ```bash
     uvicorn api:app --reload --host 0.0.0.0 --port 8000
     ```
   - Teste avec une requête POST via `curl` ou Postman.

3. **Déploiement sur Render** :
   - Pousse le dossier `mon-api` sur GitHub.
   - Configure un service web sur Render avec :
     - Build Command : `pip install -r requirements.txt`
     - Start Command : `uvicorn api:app --host 0.0.0.0 --port 10000`
   - URL publique : `https://api-blood-donation.onrender.com`.

---

## 📝 Notes Finales

Ce tableau de bord est conçu pour être à la fois un outil analytique puissant et une interface utilisateur intuitive. Toute suggestion ou amélioration est la bienvenue ! Pour toute question, contactez [hyontnick@gmail.com] ou ouvrez une issue sur le dépôt GitHub.

**Développé avec 💡 et ❤️ pour optimiser la gestion des dons de sang.**

---

### Changements Ajoutés
- **Section "Comment Interagir avec les Visualisations"** : Intégrée dans "Instructions pour Exécuter le Tableau de Bord". Elle détaille comment utiliser les filtres, interagir avec les graphiques Plotly (zoom, hover), et gérer les prédictions/historique. C’est clair, précis et orienté utilisateur.

### Instructions pour Utiliser ce README
1. Crée un fichier `README.md` à la racine de ton dépôt.
2. Copie-colle ce contenu dedans.
3. Remplace les placeholders comme `https://github.com/hyontnick/qganalytics_blood_dashboard_indabax.git` par l’URL réelle de ton dépôt GitHub, et ajuste `[hyontnick@gmail.com]` si nécessaire.
4. Pousse-le sur GitHub :
   ```bash
   git add README.md
   git commit -m "Ajout du README détaillé avec instructions d’interaction"
   git push origin main
   ```
---
