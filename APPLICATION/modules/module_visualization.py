# module_visualization.py
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import urllib.parse

DB_PATH = "blood_donation_users.db"

# Traductions
translations = {
    "fr": {
        "title": "📊 Visualisation des Données des Utilisateurs",
        "table_title": "📋 Tableau des utilisateurs",
        "no_data": "Aucune donnée disponible dans la base de données.",
        "charts_title": "📈 Analyses graphiques",
        "age_gender_chart": "Âge moyen par genre",
        "profession_eligibility_chart": "Éligibilité par profession",
        "prediction_trend_chart": "Évolution des prédictions dans le temps",
        "donation_history_chart": "Historique des dons",
        "time_unit_month": "Mois",
        "time_unit_day": "Jours",
        "time_unit_hour": "Heures",
        "details_title": "🔍 Détails de la base de données",
        "total_users": "Nombre total d’utilisateurs : <b>{}</b>",
        "avg_age": "Âge moyen : <b>{:.1f}</b> ans",
        "avg_hemoglobin": "Taux d’hémoglobine moyen : <b>{:.1f}</b> g/dL",
        "eligible_percent": "Pourcentage éligible : <b>{:.1f}%</b>",
        "download_button": "Télécharger les données (CSV)"
    },
    "en": {
        "title": "📊 User Data Visualization",
        "table_title": "📋 User Table",
        "no_data": "No data available in the database.",
        "charts_title": "📈 Data Insights",
        "age_gender_chart": "Average Age by Gender",
        "profession_eligibility_chart": "Eligibility by Profession",
        "prediction_trend_chart": "Prediction Trend Over Time",
        "donation_history_chart": "Donation History",
        "time_unit_month": "Months",
        "time_unit_day": "Days",
        "time_unit_hour": "Hours",
        "details_title": "🔍 Database Details",
        "total_users": "Total users: <b>{}</b>",
        "avg_age": "Average age: <b>{:.1f}</b> years",
        "avg_hemoglobin": "Average hemoglobin: <b>{:.1f}</b> g/dL",
        "eligible_percent": "Eligible percentage: <b>{:.1f}%</b>",
        "download_button": "Download Data (CSV)"
    }
}

# CSS
st.markdown("""
    <style>
    .stat-card { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 16px; }
    .center-button { display: flex; justify-content: center; margin-top: 20px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background-color: #f2f2f2; }
    tr:hover { background-color: #f5f5f5; }
    a { text-decoration: none; color: #1E90FF; }
    a:hover { text-decoration: underline; }
    .sent-indicator { margin-left: 5px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, email TEXT, numero_telephone TEXT, age INTEGER, niveau_detude TEXT, genre TEXT, taille REAL, poids REAL, situation_matrimoniale_sm TEXT, profession TEXT, arrondissement_de_residence TEXT, nationalite TEXT, religion TEXT, a_til_elle_deja_donne_le_sang TEXT, si_oui_preciser_la_date_du_dernier_don TEXT, taux_dhemoglobine REAL, result TEXT, probability_eligible REAL, probability_not_eligible REAL, timestamp TEXT, email_sent TEXT DEFAULT NULL, whatsapp_sent TEXT DEFAULT NULL)''')
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if "email_sent" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN email_sent TEXT DEFAULT NULL")
    if "whatsapp_sent" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN whatsapp_sent TEXT DEFAULT NULL")
    conn.commit()
    conn.close()

def get_data():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users ORDER BY timestamp DESC", conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["email_sent"] = pd.to_datetime(df["email_sent"], errors="coerce")
    df["whatsapp_sent"] = pd.to_datetime(df["whatsapp_sent"], errors="coerce")
    return df

def generate_message(nom, result, probability_eligible, lang):
    message = (f"Bonjour {nom},\n\nNous avons le plaisir de vous informer que votre éligibilité au don de sang a été évaluée.\n"
               f"Résultat : {result}\nProbabilité d’éligibilité : {probability_eligible * 100:.2f}%\n\n"
               f"Merci de votre intérêt pour le don de sang !\nÉquipe Blood Donation") if lang == "fr" else (
               f"Hello {nom},\n\nWe are pleased to inform you that your eligibility for blood donation has been evaluated.\n"
               f"Result: {result}\nEligibility probability: {probability_eligible * 100:.2f}%\n\n"
               f"Thank you for your interest in blood donation!\nBlood Donation Team")
    return urllib.parse.quote(message)

def show_visualization(df_unused=None, lang="fr"):
    df = get_data()
    if df.empty:
        st.warning(translations[lang]["no_data"])
        return

    st.subheader(translations[lang]["table_title"])
    df_display = df[["id", "nom", "email", "numero_telephone", "result", "probability_eligible", "timestamp", "email_sent", "whatsapp_sent"]].copy()

    # Limiter aux 10 premières lignes par défaut
    df_display_limited = df_display.head(10)  # Affiche uniquement les 10 premières lignes

    # Générer le HTML pour le tableau
    html_table = "<table><thead><tr>"
    for col in ["id", "nom", "email", "numero_telephone", "result", "probability_eligible", "timestamp"]:
        html_table += f"<th>{col}</th>"
    html_table += "</tr></thead><tbody>"
    for _, row in df_display.iterrows():  # On itère sur toutes les lignes pour permettre le scroll complet
        email_link = f"mailto:{row['email']}?subject={urllib.parse.quote('Résultat de votre éligibilité')}&body={generate_message(row['nom'], row['result'], row['probability_eligible'], lang)}"
        whatsapp_link = f"https://wa.me/+237{row['numero_telephone']}?text={generate_message(row['nom'], row['result'], row['probability_eligible'], lang)}"
        email_indicator = "✅" if pd.notna(row["email_sent"]) else "❌"
        whatsapp_indicator = "✅" if pd.notna(row["whatsapp_sent"]) else "❌"
        html_table += f"<tr><td>{row['id']}</td><td>{row['nom']}</td><td><a href='{email_link}'>{row['email']}</a><span class='sent-indicator'>{email_indicator}</span></td><td><a href='{whatsapp_link}'>{row['numero_telephone']}</a><span class='sent-indicator'>{whatsapp_indicator}</span></td><td>{row['result']}</td><td>{row['probability_eligible']:.2f}</td><td>{row['timestamp']}</td></tr>"
    html_table += "</tbody></table>"

    # Ajouter un conteneur avec défilement
    st.markdown(f"""
        <div style='max-height: 300px; overflow-y: auto; border: 1px solid #ddd; border-radius: 5px;'>
            {html_table}
        </div>
    """, unsafe_allow_html=True)

    st.subheader(translations[lang]["charts_title"])
    col1, col2 = st.columns(2)
    with col1:
        age_gender = df.groupby("genre")["age"].mean().reset_index()
        fig_age = go.Figure(data=[go.Bar(x=age_gender["genre"], y=age_gender["age"], marker_color=["#2196F3", "#E91E63"], text=age_gender["age"].round(1), textposition="auto")])
        fig_age.update_layout(title=translations[lang]["age_gender_chart"], xaxis_title="Genre" if lang == "fr" else "Gender", yaxis_title="Âge moyen (ans)" if lang == "fr" else "Average Age (years)", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(size=14), bargap=0.2)
        st.plotly_chart(fig_age, use_container_width=True)
    with col2:
        time_unit = st.selectbox("Unité de temps", [translations[lang]["time_unit_month"], translations[lang]["time_unit_day"], translations[lang]["time_unit_hour"]], key="time_unit_select")
        if time_unit == translations[lang]["time_unit_month"]:
            df["time_group"] = df["timestamp"].dt.to_period("M").astype(str)
        elif time_unit == translations[lang]["time_unit_day"]:
            df["time_group"] = df["timestamp"].dt.date.astype(str)
        else:
            df["time_group"] = df["timestamp"].dt.floor("H").astype(str)
        trend_data = df.groupby(["time_group", "result"]).size().reset_index(name="count")
        fig_trend = px.line(trend_data, x="time_group", y="count", color="result", title=translations[lang]["prediction_trend_chart"], color_discrete_map={"Éligible": "#4CAF50", "Non éligible": "#F44336"})
        fig_trend.update_layout(xaxis_title="Temps" if lang == "fr" else "Time", yaxis_title="Nombre de prédictions" if lang == "fr" else "Number of Predictions", font=dict(size=14))
        st.plotly_chart(fig_trend, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        prof_elig = df.groupby(["profession", "result"]).size().reset_index(name="count")
        fig_prof = px.treemap(prof_elig, path=["profession", "result"], values="count", title=translations[lang]["profession_eligibility_chart"], color="result", color_discrete_map={"Éligible": "#4CAF50", "Non éligible": "#F44336"})
        fig_prof.update_layout(font=dict(size=14))
        st.plotly_chart(fig_prof, use_container_width=True)
    with col4:
        donation_history = df["a_til_elle_deja_donne_le_sang"].value_counts().reset_index()
        donation_history.columns = ["has_donated", "count"]
        fig_donation = go.Figure(data=[go.Pie(labels=donation_history["has_donated"], values=donation_history["count"], hole=0.4, marker_colors=["#FF9800", "#9E9E9E"], textinfo="label+percent", pull=[0.1, 0])])
        fig_donation.update_layout(title=translations[lang]["donation_history_chart"], font=dict(size=14))
        st.plotly_chart(fig_donation, use_container_width=True)

    st.subheader(translations[lang]["details_title"])
    with st.container():
        col1, col2 = st.columns(2)
        total_users = len(df)
        eligible_count = len(df[df['result'] == 'Éligible'])
        most_recent = df["timestamp"].iloc[0].strftime("%Y-%m-%d %H:%M:%S") if not df.empty else "N/A"
        avg_prob_eligible = df["probability_eligible"].mean() * 100 if not df.empty else 0
        with col1:
            st.markdown(f"<div class='stat-card'>{translations[lang]['total_users'].format(total_users)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['eligible_percent'].format(eligible_count / total_users * 100 if total_users > 0 else 0)}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'>Dernière soumission : <b>{most_recent}</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>Probabilité moyenne d’éligibilité : <b>{avg_prob_eligible:.1f}%</b></div>", unsafe_allow_html=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        st.download_button(label=translations[lang]["download_button"], data=csv, file_name="blood_donation_data.csv", mime="text/csv")
        st.markdown("</div>", unsafe_allow_html=True)