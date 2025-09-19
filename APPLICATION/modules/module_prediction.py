# module_prediction.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
from notifications import save_user_data  

# URL de l’API FastAPI
API_URL = "https://api-blood-donation-gl.onrender.com/predict"

# Dictionnaire de traductions
translations = {
    "fr": {
        "header": "🤖 Prédiction d’Éligibilité au Don de Sang",
        "personal_info": "👤 Informations Personnelles",
        "name_label": "👤 Nom",
        "name_help": "Votre nom complet",
        "email_label": "📧 Email",
        "email_help": "Votre adresse email valide (ex. exemple@domaine.com)",
        "phone_label": "📱 Numéro de téléphone",
        "phone_help": "Numéro de 9 chiffres (ex. 6XXXXXXXX)",
        "age_label": "🎂 Âge",
        "age_help": "Âge entre 18 et 65 ans",
        "age_tooltip": "<p class='tooltip'>Âge requis pour le don de sang.</p>",
        "gender_label": "👤 Genre",
        "gender_help": "Sélectionnez votre genre",
        "education_label": "📚 Niveau d’étude",
        "education_help": "Votre niveau d’éducation",
        "physical_measures": "📏 Mesures Physiques",
        "height_label": "📏 Taille (cm)",
        "height_help": "Taille en centimètres",
        "weight_label": "⚖️ Poids (kg)",
        "weight_help": "Poids en kilogrammes",
        "hemoglobin_label": "🩺 Taux d’hémoglobine (g/dL)",
        "hemoglobin_help": "Taux minimum requis : 12.5 pour femmes, 13 pour hommes",
        "social_situation": "🏡 Situation Sociale",
        "marital_status_label": "💍 Situation matrimoniale",
        "marital_status_help": "Votre statut matrimonial",
        "profession_label": "💼 Profession",
        "profession_help": "Votre domaine professionnel",
        "arrondissement_label": "🏡 Arrondissement",
        "arrondissement_help": "Votre lieu de résidence",
        "identity_experience": "🌍 Identité et Expérience",
        "nationality_label": "🌍 Nationalité",
        "nationality_help": "Votre nationalité",
        "religion_label": "⛪ Religion",
        "religion_help": "Votre religion",
        "has_donated_label": "💉 A déjà donné ?",
        "has_donated_help": "Avez-vous déjà donné du sang ?",
        "donation_history": "📅 Historique de Don",
        "last_donation_label": "📅 Date du dernier don (si oui)",
        "last_donation_help": "Indiquez la date de votre dernier don si applicable",
        "predict_button": "🚀 Prédire",
        "predict_help": "Cliquez pour obtenir votre éligibilité",
        "result_eligible": "<div class='result-eligible'>✅ Éligible<br>{:.2f}% de chances</div>",
        "result_not_eligible": "<div class='result-not-eligible'>❌ Non éligible<br>{:.2f}% de chances</div>",
        "gauge_title": "Probabilité d’éligibilité (%)",
        "result_tooltip": "<p class='tooltip'>Résultat : La jauge montre vos chances d’être éligible. Plus c’est vert, mieux c’est !</p>",
        "warning_inconsistent": "⚠️ Attention : Le résultat semble incohérent avec les probabilités. Vérifiez vos données ou contactez un expert.",
        "error_api": "Erreur lors de l’appel à l’API : {}",
        "history_title": "📜 Historique des Prédictions",
        "history_entry": "**{} - {}** : {} (Éligible: {:.2f}%, Non éligible: {:.2f}%)",
        "clear_history_button": "🗑️ Effacer l’historique",
        "history_cleared": "Historique effacé !",
        "result_message": "Votre résultat a été enregistré. Vous recevrez une confirmation sous peu à {}.",
        "copy_button": "📋 Copier le résultat"
    },
    "en": {
        "header": "🤖 Blood Donation Eligibility Prediction",
        "personal_info": "👤 Personal Information",
        "name_label": "👤 Name",
        "name_help": "Your full name",
        "email_label": "📧 Email",
        "email_help": "Your valid email address (e.g., example@domain.com)",
        "phone_label": "📱 Phone Number",
        "phone_help": "9-digit number (e.g., 6XXXXXXXX)",
        "age_label": "🎂 Age",
        "age_help": "Age between 18 and 65",
        "age_tooltip": "<p class='tooltip'>Age required for blood donation.</p>",
        "gender_label": "👤 Gender",
        "gender_help": "Select your gender",
        "education_label": "📚 Education Level",
        "education_help": "Your education level",
        "physical_measures": "📏 Physical Measurements",
        "height_label": "📏 Height (cm)",
        "height_help": "Height in centimeters",
        "weight_label": "⚖️ Weight (kg)",
        "weight_help": "Weight in kilograms",
        "hemoglobin_label": "🩺 Hemoglobin Level (g/dL)",
        "hemoglobin_help": "Minimum required: 12.5 for women, 13 for men",
        "social_situation": "🏡 Social Situation",
        "marital_status_label": "💍 Marital Status",
        "marital_status_help": "Your marital status",
        "profession_label": "💼 Profession",
        "profession_help": "Your professional field",
        "arrondissement_label": "🏡 District",
        "arrondissement_help": "Your place of residence",
        "identity_experience": "🌍 Identity and Experience",
        "nationality_label": "🌍 Nationality",
        "nationality_help": "Your nationality",
        "religion_label": "⛪ Religion",
        "religion_help": "Your religion",
        "has_donated_label": "💉 Has donated before?",
        "has_donated_help": "Have you ever donated blood?",
        "donation_history": "📅 Donation History",
        "last_donation_label": "📅 Date of last donation (if yes)",
        "last_donation_help": "Indicate the date of your last donation if applicable",
        "predict_button": "🚀 Predict",
        "predict_help": "Click to get your eligibility",
        "result_eligible": "<div class='result-eligible'>✅ Eligible<br>{:.2f}% chance</div>",
        "result_not_eligible": "<div class='result-not-eligible'>❌ Not Eligible<br>{:.2f}% chance</div>",
        "gauge_title": "Eligibility Probability (%)",
        "result_tooltip": "<p class='tooltip'>Result: The gauge shows your chances of being eligible. The greener, the better!</p>",
        "warning_inconsistent": "⚠️ Warning: The result seems inconsistent with the probabilities. Check your data or contact an expert.",
        "error_api": "Error during API call: {}",
        "history_title": "📜 Prediction History",
        "history_entry": "**{} - {}** : {} (Eligible: {:.2f}%, Not eligible: {:.2f}%)",
        "clear_history_button": "🗑️ Clear History",
        "history_cleared": "History cleared!",
        "result_message": "Your result has been recorded. You will receive a confirmation soon at {}.",
        "copy_button": "📋 Copy Result"
    }
}

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 9

def validate_email(email):
    return "@" in email and "." in email.split("@")[-1]

def show_prediction(df_unused=None, lang="fr"):
    st.header(translations[lang]["header"])

    # CSS
    st.markdown("""
        <style>
        .main-container {border: 2px solid #e0e0e0; padding: 20px; border-radius: 15px; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;}
        .input-box {background-color: #f9f9f9; padding: 10px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 10px;}
        .predict-button {background-color: #4CAF50; color: white; font-size: 18px; padding: 12px 24px; border-radius: 12px; border: none; cursor: pointer; transition: all 0.3s ease;}
        .predict-button:hover {background-color: #45a049; transform: scale(1.05); box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
        .result-eligible {background-color: #e8f5e9; color: #2E7D32; padding: 20px; border-radius: 12px; font-size: 20px; border-left: 5px solid #4CAF50; animation: fadeIn 0.5s;}
        .result-not-eligible {background-color: #ffebee; color: #c62828; padding: 20px; border-radius: 12px; font-size: 20px; border-left: 5px solid #F44336; animation: fadeIn 0.5s;}
        .tooltip {font-size: 12px; color: #757575; margin-top: 5px;}
        @keyframes fadeIn {from {opacity: 0;} to {opacity: 1;}}
        </style>
    """, unsafe_allow_html=True)

    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []

    with st.form(key='predict_form'):
        # Section 1 : Informations Personnelles
        st.subheader(translations[lang]["personal_info"])
        col1, col2, col3 = st.columns(3)
        with col1:
            nom = st.text_input(translations[lang]["name_label"], help=translations[lang]["name_help"])
        with col2:
            email = st.text_input(translations[lang]["email_label"], help=translations[lang]["email_help"])
        with col3:
            numero_telephone = st.text_input(translations[lang]["phone_label"], help=translations[lang]["phone_help"], max_chars=9)

        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input(translations[lang]["age_label"], min_value=18, max_value=65, value=25, help=translations[lang]["age_help"])
            st.markdown(translations[lang]["age_tooltip"], unsafe_allow_html=True)
        with col2:
            genre = st.selectbox(translations[lang]["gender_label"], ["Homme", "Femme"], index=0, help=translations[lang]["gender_help"])
        with col3:
            niveau_detude = st.selectbox(translations[lang]["education_label"], ["Aucun", "Primaire", "Secondaire", "Universitaire", "Pas Précisé"], index=3, help=translations[lang]["education_help"])

        # Section 2 : Mesures Physiques
        st.subheader(translations[lang]["physical_measures"])
        col1, col2, col3 = st.columns(3)
        with col1:
            taille = st.number_input(translations[lang]["height_label"], min_value=100.0, max_value=250.0, value=170.0, step=0.1, help=translations[lang]["height_help"])
        with col2:
            poids = st.number_input(translations[lang]["weight_label"], min_value=30.0, max_value=200.0, value=70.0, step=0.1, help=translations[lang]["weight_help"])
        with col3:
            taux_dhemoglobine = st.number_input(translations[lang]["hemoglobin_label"], min_value=5.0, max_value=20.0, value=13.5, step=0.1, help=translations[lang]["hemoglobin_help"])

        # Section 3 : Situation Sociale
        st.subheader(translations[lang]["social_situation"])
        col1, col2, col3 = st.columns(3)
        with col1:
            situation_matrimoniale_sm = st.selectbox(translations[lang]["marital_status_label"], ["Célibataire", "Divorcé(e)", "Marié(e)", "Veuf(ve)"], index=0, help=translations[lang]["marital_status_help"])
        with col2:
            profession = st.selectbox(translations[lang]["profession_label"], ["Administration", "Agriculture", "Artisans", "Bâtiment", "Commerce", "Divers", "Hôtellerie", "Informatique", "Sans emploi", "Santé", "Sécurité", "Techniciens", "Transport", "Éducation", "Étudiants"], index=0, help=translations[lang]["profession_help"])
        with col3:
            arrondissement_de_residence = st.selectbox(translations[lang]["arrondissement_label"], ["Douala (Non précisé)", "Douala I", "Douala II", "Douala III", "Douala IV", "Douala V", "Douala VI", "Non précisé"], index=2, help=translations[lang]["arrondissement_help"])

        # Section 4 : Identité et Expérience
        st.subheader(translations[lang]["identity_experience"])
        col1, col2, col3 = st.columns(3)
        with col1:
            nationalite = st.selectbox(translations[lang]["nationality_label"], ["Camerounaise", "R A S"], index=0, help=translations[lang]["nationality_help"])
        with col2:
            religion = st.selectbox(translations[lang]["religion_label"], ["Christianisme", "Croyances générales", "Croyances traditionnelles", "Islam", "Non religieux"], index=0, help=translations[lang]["religion_help"])
        with col3:
            a_til_elle_deja_donne_le_sang = st.selectbox(translations[lang]["has_donated_label"], ["Oui", "Non"], index=1, help=translations[lang]["has_donated_help"])

        # Section 5 : Date du Dernier Don
        st.subheader(translations[lang]["donation_history"])
        si_oui_preciser_la_date_du_dernier_don = st.date_input(
            translations[lang]["last_donation_label"],
            value=None,
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            help=translations[lang]["last_donation_help"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button(label=translations[lang]["predict_button"], help=translations[lang]["predict_help"], type="primary")

    if submit:
        # Validation des champs
        if not nom:
            st.error("Veuillez entrer votre nom.")
            return
        if not validate_email(email):
            st.error("Veuillez entrer un email valide (ex. exemple@domaine.com).")
            return
        if not validate_phone(numero_telephone):
            st.error("Veuillez entrer un numéro de téléphone valide (9 chiffres, ex. 6XXXXXXXX).")
            return

        # Préparer les données pour l’API
        data = {
            "age": age,
            "niveau_detude": niveau_detude,
            "genre": genre,
            "taille": taille,
            "poids": poids,
            "situation_matrimoniale_sm": situation_matrimoniale_sm,
            "profession": profession,
            "arrondissement_de_residence": arrondissement_de_residence,
            "nationalite": nationalite,
            "religion": religion,
            "a_til_elle_deja_donne_le_sang": a_til_elle_deja_donne_le_sang,
            "si_oui_preciser_la_date_du_dernier_don": si_oui_preciser_la_date_du_dernier_don.strftime("%Y-%m-%d") if si_oui_preciser_la_date_du_dernier_don else "",
            "taux_dhemoglobine": taux_dhemoglobine
        }

        # Données pour l’historique et la BD
        user_info = {
            "nom": nom,
            "email": email,
            "numero_telephone": numero_telephone,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }

        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            result = response.json()

            # Ajouter le résultat à user_info
            user_info["result"] = result["result"]
            user_info["probability_eligible"] = result["probability_eligible"]
            user_info["probability_not_eligible"] = result["probability_not_eligible"]

            # Stocker dans l’historique et la BD
            st.session_state.prediction_history.append(user_info)
            save_user_data(user_info)

            # Message de résultat
            result_text = f"Résultat : {result['result']}\nProbabilité d’éligibilité : {result['probability_eligible'] * 100:.2f}%"
            st.success(translations[lang]["result_message"].format(email))

            # Affichage du résultat
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    if result["result"] == "Éligible":
                        st.markdown(translations[lang]["result_eligible"].format(result["probability_eligible"] * 100), unsafe_allow_html=True)
                    else:
                        st.markdown(translations[lang]["result_not_eligible"].format(result["probability_not_eligible"] * 100), unsafe_allow_html=True)
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result["probability_eligible"] * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': translations[lang]["gauge_title"]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#4CAF50" if result["result"] == "Éligible" else "#F44336"},
                            'steps': [{'range': [0, 50], 'color': "#ffebee"}, {'range': [50, 100], 'color': "#e8f5e9"}],
                            'threshold': {'line': {'color': "black", 'width': 4}, 'value': 50}
                        }
                    ))
                    fig.update_layout(height=200)
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown(translations[lang]["result_tooltip"], unsafe_allow_html=True)

                # Option pour copier le résultat
                st.text_area("Votre résultat", result_text, height=100)
                if st.button(translations[lang]["copy_button"]):
                    st.write("Résultat copié dans le presse-papiers !")
                    st.session_state["clipboard"] = result_text  # Simulation, nécessite pyperclip ou JavaScript pour copie réelle

            if (result["result"] == "Éligible" and result["probability_eligible"] < 0.5) or \
               (result["result"] == "Non éligible" and result["probability_eligible"] >= 0.5):
                st.warning(translations[lang]["warning_inconsistent"])

        except requests.exceptions.RequestException as e:
            st.error(translations[lang]["error_api"].format(str(e)))

    # Historique des prédictions
    if st.session_state.prediction_history:
        with st.expander(translations[lang]["history_title"], expanded=False):
            for entry in reversed(st.session_state.prediction_history[-5:]):
                st.write(translations[lang]["history_entry"].format(entry["timestamp"], entry["nom"], entry["result"], entry["probability_eligible"] * 100, entry["probability_not_eligible"] * 100))
            if st.button(translations[lang]["clear_history_button"]):
                st.session_state.prediction_history = []
                st.success(translations[lang]["history_cleared"])
