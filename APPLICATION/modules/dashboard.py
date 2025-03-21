import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
import os
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt
from module_cartographie import show_cartographie
from module_conditions import show_conditions
from module_profilage import show_profilage
from module_campagnes import show_campagnes
from module_fidelisation import show_fidelisation
from module_sentiment import show_sentiment
from module_prediction import show_prediction
from module_banque_sang import show_banque_sang

# Configuration de la page
st.set_page_config(layout="wide", page_title="Blood Donation Dashboard", page_icon="🩸")

# Charger les données
@st.cache_data
def load_data():
    url_volontaire = "https://drive.google.com/file/d/1uYSDE9100RH0yw48c9vp0AM0L5Yx7d_C/view?usp=sharing"
    url_2020 = "https://drive.google.com/file/d/1ywzNWhJZ8Fj23wIlg7kkHtdjmIS4t1FE/view?usp=sharing"
    url_dates = "https://drive.google.com/file/d/1yPEPJ_lBJiXxR0KnRoEwt85e8lx6a6af/view?usp=sharing"
    df_volontaire = pd.read_csv(url_volontaire)
    df_2020 = pd.read_csv(url_2020)
    df_dates = pd.read_csv(url_dates)
    #df_volontaire = pd.read_csv('datas/volontaire_clean_corrige.csv')
    #df_2020 = pd.read_csv('datas/2020_clean.csv')
    #df_dates = pd.read_csv('datas/dates_2019_extraites.csv')
    df_dates['date_de_remplissage_de_la_fiche'] = pd.to_datetime(df_dates['date_de_remplissage_de_la_fiche'])
    return df_volontaire, df_2020, df_dates

df_volontaire, df_2020, df_dates = load_data()

# Dictionnaire de traductions
translations = {
    "fr": {
        "login_title": "Connexion",
        "username_label": "👤 Nom d’utilisateur",
        "username_placeholder": "Utilisateur",
        "password_label": "🔒 Mot de passe",
        "password_placeholder": "Mot de passe",
        "login_button": "Se connecter",
        "login_error": "❌ Identifiants incorrects",
        "theme_label": "🎨 Thème",
        "language_label": "🌐 Langue",
        "logout_button": "🚪 Déconnexion",
        "logout_help": "Se déconnecter de l'application",
        "welcome": "Bienvenue",
        "dashboard_title": "Tableau de Bord - Gestion des Dons de Sang",
        "app_title": "QG ANALYTICS",
        "navigation": "Navigation",
        "filters_info": "Filtres & Infos",
        "age": "Âge",
        "arrondissement": "Arrondissement",
        "arrondissement_warning": "Sélectionnez au moins un arrondissement.",
        "period": "Période (2019)",
        "genre": "Genre",
        "genre_warning": "Sélectionnez au moins un genre.",
        "health_conditions": "Conditions de Santé (Non-Éligibilité)",
        "health_conditions_help": "Sélectionnez les conditions pour filtrer les non-éligibles.",
        "no_conditions_info": "Aucune condition sélectionnée : tous inclus.",
        "dynamic_filter": "Filtre Dynamique",
        "choose_field": "Choisir un champ",
        "no_values_info": "Aucune valeur sélectionnée pour {dynamic_column} : toutes incluses.",
        "volunteers_filtered": "Volontaires filtrés",
        "average_age": "Âge moyen",
        "eligible": "Éligibles",
        "top_arrondissements": "Top des Volontaires par Arrondissement",
        "arrondissement_col": "Arrondissement",
        "volunteers_col": "Nombre de Volontaires",
        "network_arrondissements": "Réseau des Arrondissements",
        "details": "Détails",
        "period_detail": "Période",
        "genres_selected": "Genres sélectionnés",
        "total_volunteers": "Volontaires total",
        "total_eligible": "Éligibles total",
        "donations_2019": "Dons 2019",
        "about_dashboard": "À Propos du Dashboard",
        "about_text": """
            Ce tableau de bord est conçu pour analyser et visualiser les informations liées aux dons de sang à Douala. 
            Il offre des outils pour explorer les données, identifier des tendances et optimiser la gestion des campagnes de don. 
            Les fonctionnalités incluent des analyses géographiques, des profils statistiques et des prédictions d’éligibilité.
            **Développeurs :** Bleriot Hyonta (Chef de projet), Kappe Moko (Membre)  
            **Pour :** INDABAX CAMEROON
        """,
        "qr_caption": "Scannez pour une version mobile",
        "modules": {
            "📍 Cartographie des Donneurs": "📍 Cartographie des Donneurs",
            "🏥 Conditions de Santé": "🏥 Conditions de Santé",
            "🔬 Profilage des Donneurs": "🔬 Profilage des Donneurs",
            "📅 Analyse des Campagnes": "📅 Analyse des Campagnes",
            "🤝 Fidélisation des Donneurs": "🤝 Fidélisation des Donneurs",
            "💬 Analyse de Sentiment": "💬 Analyse de Sentiment",
            "🤖 Prédiction d’Éligibilité": "🤖 Prédiction d’Éligibilité",
            "🩸 Banque de Sang": "🩸 Banque de Sang"
        }
    },
    "en": {
        "login_title": "Login",
        "username_label": "👤 Username",
        "username_placeholder": "User",
        "password_label": "🔒 Password",
        "password_placeholder": "Password",
        "login_button": "Log In",
        "login_error": "❌ Incorrect credentials",
        "theme_label": "🎨 Theme",
        "language_label": "🌐 Language",
        "logout_button": "🚪 Logout",
        "logout_help": "Log out of the application",
        "welcome": "Welcome",
        "dashboard_title": "Dashboard - Blood Donation Management",
        "app_title": "QG ANALYTICS",
        "navigation": "Navigation",
        "filters_info": "Filters & Info",
        "age": "Age",
        "arrondissement": "District",
        "arrondissement_warning": "Select at least one district.",
        "period": "Period (2019)",
        "genre": "Gender",
        "genre_warning": "Select at least one gender.",
        "health_conditions": "Health Conditions (Non-Eligibility)",
        "health_conditions_help": "Select conditions to filter non-eligible volunteers.",
        "no_conditions_info": "No conditions selected: all included.",
        "dynamic_filter": "Dynamic Filter",
        "choose_field": "Choose a field",
        "no_values_info": "No values selected for {dynamic_column}: all included.",
        "volunteers_filtered": "Filtered Volunteers",
        "average_age": "Average Age",
        "eligible": "Eligible",
        "top_arrondissements": "Top Volunteers by District",
        "arrondissement_col": "District",
        "volunteers_col": "Number of Volunteers",
        "network_arrondissements": "District Network",
        "details": "Details",
        "period_detail": "Period",
        "genres_selected": "Selected Genders",
        "total_volunteers": "Total Volunteers",
        "total_eligible": "Total Eligible",
        "donations_2019": "Donations 2019",
        "about_dashboard": "About the Dashboard",
        "about_text": """
            This dashboard is designed to analyze and visualize information related to blood donations in Douala. 
            It provides tools to explore data, identify trends, and optimize donation campaign management. 
            Features include geographic analysis, statistical profiles, and eligibility predictions.
            **Developers:** Bleriot Hyonta (Project Lead), Kappe Moko (Member)  
            **For:** INDABAX CAMEROON
        """,
        "qr_caption": "Scan for mobile version",
        "modules": {
            "📍 Cartographie des Donneurs": "📍 Donor Mapping",
            "🏥 Conditions de Santé": "🏥 Health Conditions",
            "🔬 Profilage des Donneurs": "🔬 Donor Profiling",
            "📅 Analyse des Campagnes": "📅 Campaign Analysis",
            "🤝 Fidélisation des Donneurs": "🤝 Donor Retention",
            "💬 Analyse de Sentiment": "💬 Sentiment Analysis",
            "🤖 Prédiction d’Éligibilité": "🤖 Eligibility Prediction",
            "🩸 Banque de Sang": "🩸 Blood Bank"
        }
    }
}

# Fonction pour appliquer le thème
def set_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
            .main {background-color: #1e1e1e; color: #ffffff;}
            .sidebar .sidebar-content {background-color: #2b2b2b; color: #ffffff;}
            .stButton>button {background-color: #4CAF50; color: white; border-radius: 5px; transition: all 0.3s;}
            .stButton>button:hover {background-color: #45a049;}
            .stat-box {background-color: #333333; color: #ffffff; padding: 15px; border-radius: 10px; margin: 10px; text-align: center;}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .main {background-color: #ffffff; color: #000000;}
            .sidebar .sidebar-content {background-color: #f0f2f6; color: #000000;}
            .stButton>button {background-color: #4CAF50; color: white; border-radius: 5px; transition: all 0.3s;}
            .stButton>button:hover {background-color: #45a049;}
            .stat-box {background-color: #e8f5e9; color: #000000; padding: 15px; border-radius: 10px; margin: 10px; text-align: center;}
            </style>
        """, unsafe_allow_html=True)

# Fonction de connexion
def show_login():
    lang = st.session_state.get('lang', 'fr')
    theme = st.session_state.get('theme', 'Light')
    set_theme(theme)

    st.markdown("""
        <style>
        .login-container {
            max-width: 350px; margin: 80px auto; padding: 25px; border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1); background: linear-gradient(135deg, #ffffff, #f9f9f9);
            border: 1px solid #e5e5e5;
        }
        .dark-theme .login-container {
            background: linear-gradient(135deg, #2a2a2a, #333333); border: 1px solid #404040;
        }
        h1 {text-align: center; color: #2E7D32; font-family: 'Arial', sans-serif; font-size: 28px;}
        .dark-theme h1 {color: #4CAF50;}
        .stTextInput > div > input {border-radius: 8px; padding: 12px; border: 1px solid #d0d0d0;}
        .dark-theme .stTextInput > div > input {background-color: #3a3a3a; color: #ffffff; border: 1px solid #505050;}
        .login-button {background: linear-gradient(90deg, #4CAF50, #66BB6A); color: white; padding: 12px; border-radius: 10px; width: 100%;}
        .error-box {background-color: #ffebee; color: #c62828; padding: 12px; border-radius: 8px; border-left: 4px solid #F44336;}
        .dark-theme .error-box {background-color: #4a2c2c;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h1>🩸 QG ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='login-container{' dark-theme' if theme == 'Dark' else ''}'>", unsafe_allow_html=True)
    st.markdown(f"<h1>{translations[lang]['login_title']}</h1>", unsafe_allow_html=True)

    with st.form("login_form"):
        username_input = st.text_input(
            translations[lang]["username_label"],
            placeholder=translations[lang]["username_placeholder"],
            key="username_input"
        )
        password_input = st.text_input(
            translations[lang]["password_label"],
            type="password",
            placeholder=translations[lang]["password_placeholder"],
            key="password_input"
        )
        submit = st.form_submit_button(translations[lang]["login_button"], type="primary")

        if submit:
            if username_input and password_input == "QG ANALYTICS":
                st.session_state.logged_in = True
                st.session_state.user = username_input
                st.session_state.selected_module = "📍 Cartographie des Donneurs"
                st.rerun()
            else:
                st.markdown(f"<div class='error-box'>{translations[lang]['login_error']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        theme_options = {"Light": "Light", "Dark": "Dark"}
        selected_theme = st.selectbox(
            translations[lang]["theme_label"],
            list(theme_options.keys()),
            index=0 if theme == "Light" else 1,
            key="theme_selector"
        )
        if st.session_state.theme != selected_theme:
            st.session_state.theme = selected_theme
            st.rerun()
    with col2:
        lang_options = {"🇫🇷 Français": "fr", "🇬🇧 English": "en"}
        selected_lang = st.selectbox(
            translations[lang]["language_label"],
            list(lang_options.keys()),
            index=0 if lang == "fr" else 1,
            key="lang_selector"
        )
        if st.session_state.lang != lang_options[selected_lang]:
            st.session_state.lang = lang_options[selected_lang]
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Fonction principale du tableau de bord
def show_dashboard():
    lang = st.session_state.get('lang', 'fr')
    set_theme(st.session_state.theme)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
            <h1 style='font-family: Arial; font-size: 2.5em; color: #FFFFFF; padding: 10px 20px; 
            background: linear-gradient(90deg, #4CAF50, #81C784); border-radius: 12px;'>
            <span style='font-size: 1.2em; vertical-align: middle; margin-right: 10px;'>🩺</span>
            {translations[lang]['dashboard_title']}
            </h1>
        """, unsafe_allow_html=True)
    with col2:
        username = st.session_state.get('user', 'Utilisateur' if lang == 'fr' else 'User')
        st.markdown(f"""
            <div style='text-align: right; color: #388E3C; font-size: 20px; padding: 8px 12px; 
            background: #E8F5E9; border-radius: 8px;'>
            <span style='font-size: 24px; margin-right: 8px;'>👋</span>
            {translations[lang]['welcome']}, <span style='font-weight: bold; color: #2E7D32;'>{username}</span>
            </div>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #2E7D32; text-align: center;'>🩸 {translations[lang]['app_title']}</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button(translations[lang]["logout_button"], key="logout", help=translations[lang]["logout_help"]):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.session_state.selected_module = None
            st.rerun()
        st.markdown("---")
        st.header(translations[lang]["navigation"])
        modules = {
                "📍 Cartographie des Donneurs": lambda df: show_cartographie(df, lang),  # Si les autres modules ont aussi besoin de lang
                "🏥 Conditions de Santé": lambda df: show_conditions(df, lang),
                "🔬 Profilage des Donneurs": lambda df: show_profilage(df, lang),
                "📅 Analyse des Campagnes": lambda df: show_campagnes(df, lang),
                "🤝 Fidélisation des Donneurs": lambda df: show_fidelisation(df, lang),
                "💬 Analyse de Sentiment": lambda df: show_sentiment(df, lang),
                "🤖 Prédiction d’Éligibilité": lambda df: show_prediction(df, lang),
                "🩸 Banque de Sang": lambda df: show_banque_sang(df, lang)  # Banque de Sang avec lang
            }
        for module_key, module_func in modules.items():
            if st.button(translations[lang]["modules"][module_key], key=module_key, use_container_width=True):
                st.session_state.selected_module = module_key

    with st.sidebar:
        st.header(translations[lang]["filters_info"])
        age_range = st.slider(translations[lang]["age"], 18, 65, (18, 65))
        arrondissements = st.multiselect(translations[lang]["arrondissement"], df_volontaire['arrondissement_de_residence'].unique())
        if not arrondissements:
            st.warning(translations[lang]["arrondissement_warning"])
            arrondissements = df_volontaire['arrondissement_de_residence'].unique().tolist()
        period = st.date_input(translations[lang]["period"], [df_dates['date_de_remplissage_de_la_fiche'].min(), df_dates['date_de_remplissage_de_la_fiche'].max()])
        genre = st.multiselect(translations[lang]["genre"], df_volontaire['genre'].unique())
        if not genre:
            st.warning(translations[lang]["genre_warning"])
            genre = df_volontaire['genre'].unique().tolist()

        health_conditions_cols = [col for col in df_volontaire.columns if 'raison_de_non_eligibilite_totale_' in col]
        health_conditions = [col.replace('raison_de_non_eligibilite_totale_', '') for col in health_conditions_cols]
        selected_conditions = st.multiselect(translations[lang]["health_conditions"], health_conditions, help=translations[lang]["health_conditions_help"])
        if not selected_conditions:
            st.info(translations[lang]["no_conditions_info"])

        st.subheader(translations[lang]["dynamic_filter"])
        dynamic_column = st.selectbox(translations[lang]["choose_field"], df_volontaire.columns)
        dynamic_values = st.multiselect(f"{translations[lang]['no_values_info'].split(' ')[0]} {dynamic_column}", df_volontaire[dynamic_column].dropna().unique())
        if not dynamic_values:
            st.info(translations[lang]["no_values_info"].format(dynamic_column=dynamic_column))

    df_volontaire_filtered = df_volontaire[
        (df_volontaire['age'].between(age_range[0], age_range[1])) &
        (df_volontaire['arrondissement_de_residence'].isin(arrondissements)) &
        (df_volontaire['genre'].isin(genre))
    ]
    if selected_conditions:
        condition_filter = df_volontaire_filtered[health_conditions_cols].eq('Oui').any(axis=1)
        df_volontaire_filtered = df_volontaire_filtered[condition_filter]
    if dynamic_values:
        df_volontaire_filtered = df_volontaire_filtered[df_volontaire_filtered[dynamic_column].isin(dynamic_values)]
    if len(period) == 2:
        df_dates_filtered = df_dates[
            (df_dates['date_de_remplissage_de_la_fiche'].dt.date >= period[0]) &
            (df_dates['date_de_remplissage_de_la_fiche'].dt.date <= period[1])
        ]
    else:
        df_dates_filtered = df_dates

    df_merged_filtered = df_volontaire_filtered.merge(df_dates_filtered, left_index=True, right_index=True, how='left')

    col1, col2 = st.columns([3, 1])
    with col1:
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.markdown(f"<div class='stat-box'><h3>👥 {len(df_volontaire_filtered)}</h3><p>{translations[lang]['volunteers_filtered']}</p></div>", unsafe_allow_html=True)
        with col_stats2:
            st.markdown(f"<div class='stat-box'><h3>🎂 {int(df_volontaire_filtered['age'].mean())}</h3><p>{translations[lang]['average_age']}</p></div>", unsafe_allow_html=True)
        with col_stats3:
            st.markdown(f"<div class='stat-box'><h3>✅ {len(df_volontaire_filtered[df_volontaire_filtered['eligibilite_au_don'] == 'Eligible'])}</h3><p>{translations[lang]['eligible']}</p></div>", unsafe_allow_html=True)

        if not st.session_state.selected_module:
            st.session_state.selected_module = "📍 Cartographie des Donneurs"
        data_to_pass = df_volontaire_filtered if st.session_state.selected_module != "📅 Analyse des Campagnes" else df_merged_filtered
        modules[st.session_state.selected_module](data_to_pass)

    with col2:
        st.subheader(translations[lang]["top_arrondissements"])
        top_arrondissements = df_volontaire_filtered['arrondissement_de_residence'].value_counts().reset_index()
        top_arrondissements.columns = [translations[lang]["arrondissement_col"], translations[lang]["volunteers_col"]]
        st.dataframe(
            top_arrondissements,
            column_config={
                translations[lang]["arrondissement_col"]: translations[lang]["arrondissement_col"],
                translations[lang]["volunteers_col"]: st.column_config.ProgressColumn(
                    translations[lang]["volunteers_col"],
                    format="%d",
                    min_value=0,
                    max_value=max(top_arrondissements[translations[lang]["volunteers_col"]]),
                    width="medium"
                )
            },
            use_container_width=True,
            height=320  # Optionnel : fixe une hauteur pour un rendu cohérent
        )

        st.subheader(translations[lang]["network_arrondissements"])
        G = nx.Graph()
        for arr, count in top_arrondissements.itertuples(index=False):
            G.add_node(arr, size=count * 10)
        for i in range(len(top_arrondissements) - 1):
            G.add_edge(top_arrondissements[translations[lang]["arrondissement_col"]][i], top_arrondissements[translations[lang]["arrondissement_col"]][i+1])
        pos = nx.circular_layout(G)
        fig, ax = plt.subplots()
        nx.draw(G, pos, with_labels=True, node_size=[G.nodes[node]['size'] for node in G.nodes()], node_color="#4CAF50", edge_color="gray", font_size=10, ax=ax)
        st.pyplot(fig)

        st.header(translations[lang]["details"])
        st.write(f"{translations[lang]['volunteers_filtered']}: {len(df_volontaire_filtered)}")
        st.write(f"{translations[lang]['period_detail']}: {period[0]} to {period[1] if len(period) > 1 else 'Not defined'}")
        st.write(f"{translations[lang]['genres_selected']}: {', '.join(genre)}")
        st.write(f"{translations[lang]['total_volunteers']}: {len(df_volontaire)}")
        st.write(f"{translations[lang]['total_eligible']}: {len(df_volontaire[df_volontaire['eligibilite_au_don'] == 'Eligible'])}")
        st.write(f"{translations[lang]['donations_2019']}: {len(df_2020)}")

        with st.expander(translations[lang]["about_dashboard"]):
            st.write(translations[lang]["about_text"])

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data("https://example.com/douala_dashboard")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#4CAF50", back_color="white")
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption=translations[lang]["qr_caption"])

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Light'
    if 'user' not in st.session_state:
        st.session_state.user = ""
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None
    if 'lang' not in st.session_state:
        st.session_state.lang = 'fr'

    if not st.session_state.logged_in:
        show_login()
    else:
        show_dashboard()
