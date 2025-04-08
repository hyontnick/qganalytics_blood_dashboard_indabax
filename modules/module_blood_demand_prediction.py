import streamlit as st
from prophet import Prophet
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Chemin de la base de données (déjà défini)
DB_PATH = "blood_donation_users.db"

# Traductions pour le module
translations = {
    "fr": {
        "title": "📉 Prédictions des Besoins en Sang",
        "no_data": "Pas assez de données historiques pour les prédictions.",
        "historical_donations": "Dons historiques",
        "predictions": "Prédictions",
        "upper_bound": "Limite supérieure",
        "lower_bound": "Limite inférieure",
        "chart_title": "Évolution et Prédiction des Besoins en Sang",
        "xaxis_title": "Date",
        "yaxis_title": "Nombre de dons",
        "period_label": "Période de prédiction (jours)",
        "update_button": "Mettre à jour les prédictions",
        "insights_title": "Insights",
        "avg_prediction": "Nombre moyen prévu pour les prochains {period} jours : {value:.1f}",
        "alert": "Alerte : Besoin urgent de dons prévu !"
    },
    "en": {
        "title": "📉 Blood Demand Predictions",
        "no_data": "Not enough historical data for predictions.",
        "historical_donations": "Historical Donations",
        "predictions": "Predictions",
        "upper_bound": "Upper Bound",
        "lower_bound": "Lower Bound",
        "chart_title": "Blood Demand Trends and Predictions",
        "xaxis_title": "Date",
        "yaxis_title": "Number of Donations",
        "period_label": "Prediction Period (days)",
        "update_button": "Update Predictions",
        "insights_title": "Insights",
        "avg_prediction": "Average predicted donations for the next {period} days: {value:.1f}",
        "alert": "Alert: Urgent need for donations predicted!"
    }
}

def show_blood_demand_prediction(df_unused=None, lang="fr"):
    st.subheader(translations[lang]["title"])

    # Charger les données historiques
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT timestamp FROM users ORDER BY timestamp", conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Agréger les dons par jour
    df_daily = df.groupby(df["timestamp"].dt.date).size().reset_index(name="donations")
    df_daily.columns = ["ds", "y"]  # Prophet exige 'ds' (date) et 'y' (valeur)

    if df_daily.empty or len(df_daily) < 2:
        st.warning(translations[lang]["no_data"])
        return

    # Configurer le modèle Prophet
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
    model.fit(df_daily)

    # Créer un dataframe pour les prédictions futures (30 jours par défaut)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Graphique interactif avec Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_daily["ds"], y=df_daily["y"], mode="lines+markers", name=translations[lang]["historical_donations"], line=dict(color="#4CAF50")))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name=translations[lang]["predictions"], line=dict(color="#F44336")))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines", name=translations[lang]["upper_bound"], line=dict(color="#FF9800", dash="dash"), fill=None))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines", name=translations[lang]["lower_bound"], line=dict(color="#FF9800", dash="dash"), fill="tonexty"))

    fig.update_layout(
        title=translations[lang]["chart_title"],
        xaxis_title=translations[lang]["xaxis_title"],
        yaxis_title=translations[lang]["yaxis_title"],
        legend=dict(x=0, y=1.1, orientation="h"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Options pour personnaliser la période
    period = st.slider(
        translations[lang]["period_label"],
        min_value=7, max_value=90, value=30, step=7
    )
    if st.button(translations[lang]["update_button"]):
        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)
        fig.data[1].x = forecast["ds"]
        fig.data[1].y = forecast["yhat"]
        fig.data[2].x = forecast["ds"]
        fig.data[2].y = forecast["yhat_upper"]
        fig.data[3].x = forecast["ds"]
        fig.data[3].y = forecast["yhat_lower"]
        st.plotly_chart(fig, use_container_width=True)

    # Informations supplémentaires
    st.write(f"### {translations[lang]['insights_title']}")
    avg_pred = forecast["yhat"].tail(period).mean()
    st.write(translations[lang]["avg_prediction"].format(period=period, value=avg_pred))
    if avg_pred < 10:  # Seuil d'alerte ajustable
        st.warning(translations[lang]["alert"])