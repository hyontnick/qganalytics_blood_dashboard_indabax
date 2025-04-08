---

### README - Tableau de Bord de Gestion des Dons de Sang

Bienvenue dans le **Tableau de Bord de Gestion des Dons de Sang**, une application web interactive développée pour analyser les données de dons de sang et prédire l’éligibilité des donneurs potentiels. Ce projet allie modernité, convivialité et puissance analytique pour répondre aux besoins des professionnels de la santé et des gestionnaires de banques de sang.

---

#### 🌟 Fonctionnalités du Tableau de Bord
Ce tableau de bord offre une expérience utilisateur riche et intuitive grâce aux modules suivants :

- **Banque de Sang** :
  - Visualisation compacte et interactive des données de dons de 2019.
  - Graphiques en barres (dons par groupe sanguin et sexe) et en camemberts (répartition des groupes sanguins et types de donation).
  - Filtres dynamiques : groupe sanguin, sexe, âge et mois, permettant une exploration personnalisée.
  - Statistiques détaillées : total des dons, âge moyen, pourcentages par sexe, groupe le plus fréquent.

- **Prédiction d’Éligibilité** :
  - Formulaire interactif pour saisir les informations personnelles, physiques et sociales d’un donneur potentiel.
  - Prédiction en temps réel de l’éligibilité au don de sang via une API REST déployée.
  - Visualisation des résultats avec une jauge de probabilité (Plotly) et un historique des prédictions.
  - Support bilingue (français/anglais) pour une accessibilité accrue.

- **Visualisation des Données** *(Nouveau)* :
  - Tableau interactif affichant les détails des donneurs (nom, email, téléphone, résultat d’éligibilité, etc.) avec possibilité de défilement pour explorer jusqu’à 100 lignes ou plus.
  - Graphiques avancés : âge moyen par genre, éligibilité par profession, tendances des prédictions dans le temps, historique des dons.
  - Statistiques clés : total des utilisateurs, âge moyen, taux d’hémoglobine moyen, pourcentage éligible.
  - Téléchargement des données en CSV pour une analyse hors ligne.
  - Sécurité renforcée : accès réservé aux administrateurs via une clé spécifique (ex. "blood2025").

- **Prédictions des Besoins en Sang avec IA** *(Nouveau)* :
  - Analyse prédictive des besoins en sang basée sur les données historiques de dons, utilisant un modèle de séries temporelles (Prophet).
  - Visualisation interactive des tendances passées et futures avec Plotly, incluant les dons historiques, les prédictions et les intervalles de confiance.
  - Options personnalisables : période de prédiction ajustable (7 à 90 jours) avec mise à jour en temps réel.
  - Insights et alertes : moyenne prévue des dons et avertissements en cas de pénurie potentielle (ex. moins de 10 dons/jour).

- **Design et Expérience Utilisateur** :
  - Interface moderne avec des cadres stylisés, animations subtiles et tooltips informatifs.
  - Organisation optimisée pour minimiser le défilement et maximiser la lisibilité.
  - Support bilingue complet (français/anglais) pour tous les modules.

---

#### 🛠️ Outils Utilisés
Ce projet repose sur une stack technologique robuste et bien intégrée :

- **Streamlit** : Framework Python pour créer l’interface web interactive et dynamique.
- **Pandas** : Manipulation et analyse des données de dons de sang.
- **Plotly** : Visualisations graphiques avancées (barres, camemberts, jauges, séries temporelles) avec interactivité (zoom, hover).
- **Prophet** : Modèle de prédiction des séries temporelles pour anticiper les besoins en sang.
- **FastAPI** : Création d’une API REST rapide et légère pour le modèle de prédiction.
- **Scikit-learn & Joblib** : Chargement et exécution du modèle Random Forest pour les prédictions.
- **SQLite3** : Gestion de la base de données locale `blood_donation_users.db`.
- **Render** : Plateforme de déploiement cloud pour héberger l’API.
- **Git & GitHub** : Gestion de version et collaboration sur le code source.
- **Python 3.11** : Langage principal, choisi pour sa polyvalence et sa communauté.

---

#### ⚙️ Hypothèses Faites Lors du Développement
Certaines hypothèses ont guidé le développement pour assurer une implémentation efficace :

- **Qualité des Données** :
  - Les données dans `2020_clean.csv` et `blood_donation_users.db` sont supposées propres, avec des valeurs cohérentes pour les colonnes comme `groupe_sanguin_abo__rhesus`, `sexe`, `age`, `timestamp`, etc.
  - Les dates dans `horodateur` ou `timestamp` sont au format valide pour une conversion en `pd.to_datetime`.

- **Modèle de Prédiction** :
  - Le modèle Random Forest (`eligibility_model_rf_no_leak.pkl`) est supposé entraîné sur des données représentatives et sans fuite de données.
  - Les catégories dans le formulaire (ex. profession, religion) correspondent aux mappings définis dans l’API.

- **Déploiement** :
  - L’API déployée sur Render reste disponible et fonctionnelle dans les limites du tier gratuit (sommeil après 15 min d’inactivité).
  - Les fichiers `.pkl` sont accessibles dans la structure du dépôt GitHub.

- **Expérience Utilisateur** :
  - Les utilisateurs ont un écran d’au moins 800px de hauteur pour une visualisation optimale sans défilement excessif.
  - Une connexion internet stable est disponible pour interagir avec l’API.

---

#### 🚀 Instructions pour Exécuter le Tableau de Bord et Interagir avec les Visualisations

##### Prérequis
- Python 3.11+ installé.
- Git pour cloner le dépôt.
- Accès à une connexion internet pour l’API déployée.

##### Étapes d’Installation
1. **Cloner le Dépôt** :
   ```bash
   git clone https://github.com/hyontnick/qganalytics_blood_dashboard_indabax.git
   cd mon-tableau-de-bord
   ```

2. **Installer les Dépendances** :
   Créez un environnement virtuel (optionnel mais recommandé) et installez les packages :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Le fichier `requirements.txt` devrait inclure :
   ```
   streamlit==1.32.0
   pandas==2.2.1
   plotly==5.20.0
   prophet==1.1.5
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
   Exécutez l’application Streamlit :
   ```bash
   streamlit run dashboard.py
   ```
   Ouvre ton navigateur à `http://localhost:8501`. Mot de passe : `QG ANALYTICS`

##### Comment Interagir avec les Visualisations
Le tableau de bord est conçu pour une interaction fluide et intuitive. Voici comment tirer parti des nouvelles fonctionnalités :

- **Module "Visualisation des Données"** :
  - **Tableau** : Affiche les 10 premières lignes par défaut (jusqu’à 100+ lignes avec défilement). Survole les emails et numéros pour envoyer des messages.
  - **Graphiques** : Explore les tendances (ex. âge par genre, éligibilité par profession) avec zoom et hover.
  - **Téléchargement** : Clique sur "Télécharger les données" pour exporter en CSV.
  - **Accès** : Réservé aux admins (clé : "blood2025").

- **Module "Prédictions des Besoins en Sang"** :
  - **Graphique** : Visualise les dons passés (vert) et prédictions futures (rouge) avec intervalles de confiance (orange).
  - **Personnalisation** : Ajuste la période (7-90 jours) avec le slider et clique sur "Mettre à jour" pour recalculer.
  - **Insights** : Vérifie la moyenne prévue et les alertes de pénurie.
  - **Bilingue** : Passe entre français et anglais pour tester les traductions.

- **Conseils d’Interaction** :
  - **Zoom et Déplacement** : Utilise la barre d’outils Plotly (en haut à droite des graphiques) pour zoomer, déplacer ou exporter en PNG.
  - **Réactivité** : Les changements dans les filtres ou options sont reflétés instantanément.
  - **Bilingue** : Utilise le sélecteur de langue pour une expérience adaptée.

---

#### 🌐 Utilisation de l’API de Prédiction
Le module de prédiction repose sur une API REST FastAPI déployée sur Render à l’adresse :  
`https://api-blood-donation.onrender.com/predict`

- **Fonctionnement** :
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

- **Déploiement de l’API** :
  - **Structure** :
    - Fichier principal : `api.py`.
    - Fichiers modèles : `eligibility_model_rf_no_leak.pkl`, `scaler_no_leak.pkl`, et un autre `.pkl` (si applicable).
    - Dépendances dans `requirements.txt` incluant `fastapi`, `uvicorn`, `scikit-learn`, etc.
  - **Instructions Locales (optionnel)** :
    - Lance l’API localement :
      ```bash
      uvicorn api:app --reload --host 0.0.0.0 --port 8000
      ```
    - Teste avec une requête POST via `curl` ou Postman.
  - **Déploiement sur Render** :
    - Pousse le dossier `mon-api` sur GitHub.
    - Configure un service web sur Render avec :
      - **Build Command** : `pip install -r requirements.txt`
      - **Start Command** : `uvicorn api:app --host 0.0.0.0 --port 10000`
    - URL publique : `https://api-blood-donation.onrender.com`.

---

#### 📝 Notes Finales
Ce tableau de bord est conçu pour être à la fois un outil analytique puissant et une interface utilisateur intuitive. Les nouvelles fonctionnalités, comme la visualisation avancée des données et les prédictions des besoins en sang, apportent une dimension révolutionnaire pour la gestion proactive des dons. Toute suggestion ou amélioration est la bienvenue ! Pour toute question, contactez [hyontnick@gmail.com] ou ouvrez une issue sur le dépôt GitHub.

Développé avec 💡 et ❤️ pour optimiser la gestion des dons de sang.

---

### Instructions
1. Remplacez le contenu de votre fichier `README` actuel par celui ci-dessus.
2. Assurez-vous que les versions des dépendances dans `requirements.txt` correspondent à celles listées (ajustez si nécessaire avec `pip show`).
3. Testez les liens et instructions pour confirmer qu’ils sont à jour avec votre projet.