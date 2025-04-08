import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Dictionnaire de traductions pour le module Analyse de Sentiment
translations = {
    "fr": {
        "header": "💬 Analyse de Sentiment des Retours",
        "demo_subheader": "📊 Qui ressent quoi ?",
        "bar_age_title": "##### 👤 Sentiment par Âge",
        "bar_age_x": "Âge",
        "bar_age_y": "Nombre",
        "bar_age_tooltip": "<p class='tooltip'>Barres empilées : combien de retours par âge et sentiment.</p>",
        "bar_sentiment_title": "##### 📊 Répartition des Sentiments",
        "bar_sentiment_x": "Sentiment",
        "bar_sentiment_y": "Nombre",
        "bar_sentiment_tooltip": "<p class='tooltip'>Barres : longueur = nombre de retours par sentiment.</p>",
        "bar_age_gender_title": "##### 👥 Sentiment par Âge et Genre",
        "bar_age_gender_x": "Âge",
        "bar_age_gender_y": "Nombre",
        "bar_age_gender_facet": "Genre",
        "bar_age_gender_tooltip": "<p class='tooltip'>Barres : compare Positif, Négatif, Neutre par âge et genre.</p>",
        "temporal_subheader": "⏳ Quand et où les sentiments changent-ils ?",
        "trend_title": "##### 📅 Tendances Temporelles (2019)",
        "trend_x": "Mois (2019)",
        "trend_y": "Nombre",
        "trend_tooltip": "<p class='tooltip'>Aire : évolution des sentiments mois par mois.</p>",
        "trend_no_data": "ℹ️ Aucune donnée temporelle disponible pour cette analyse.",
        "dynamic_title": "##### 🌍 Sentiment par Région ou Religion",
        "dynamic_filter_label": "Voir par",
        "dynamic_filter_options": ["Religion", "Arrondissement"],
        "dynamic_bar_y": "Nombre",
        "dynamic_bar_tooltip": "<p class='tooltip'>Barres : compare les sentiments par {}</p>",
        "details_subheader": "🔍 Zoom sur les détails",
        "total_feedback": "<div class='stat-card'>📊 <b>Total des retours</b> : {}</div>",
        "positive": "<div class='stat-card'>😊 <b>Positifs</b> : {} ({:.2%})</div>",
        "negative": "<div class='stat-card'>😞 <b>Négatifs</b> : {} ({:.2%})</div>",
        "neutral": "<div class='stat-card'>😐 <b>Neutres</b> : {} ({:.2%})</div>",
        "examples_title": "<div class='stat-card'>📝 <b>Exemples :</b></div>",
        "example_positif": "<div class='stat-card'>😊 <b>Positif</b> : {}</div>",
        "example_négatif": "<div class='stat-card'>😞 <b>Négatif</b> : {}</div>",
        "example_neutre": "<div class='stat-card'>😐 <b>Neutre</b> : {}</div>",
        "export_button": "Exporter les sentiments (CSV)",
        "export_filename": "sentiment_analysis.csv",
        "no_text_error": "❌ Aucune donnée textuelle trouvée dans 'si_autres_raison_preciser'.",
        "spinner": "Analyse des sentiments en cours...",
        "sentiment_labels": {"Positif": "Positif", "Négatif": "Négatif", "Neutre": "Neutre"}
    },
    "en": {
        "header": "💬 Sentiment Analysis of Feedback",
        "demo_subheader": "📊 Who feels what?",
        "bar_age_title": "##### 👤 Sentiment by Age",
        "bar_age_x": "Age",
        "bar_age_y": "Count",
        "bar_age_tooltip": "<p class='tooltip'>Stacked bars: number of feedback by age and sentiment.</p>",
        "bar_sentiment_title": "##### 📊 Sentiment Breakdown",
        "bar_sentiment_x": "Sentiment",
        "bar_sentiment_y": "Count",
        "bar_sentiment_tooltip": "<p class='tooltip'>Bars: length = number of feedback by sentiment.</p>",
        "bar_age_gender_title": "##### 👥 Sentiment by Age and Gender",
        "bar_age_gender_x": "Age",
        "bar_age_gender_y": "Count",
        "bar_age_gender_facet": "Gender",
        "bar_age_gender_tooltip": "<p class='tooltip'>Bars: compare Positive, Negative, Neutral by age and gender.</p>",
        "temporal_subheader": "⏳ When and where do sentiments change?",
        "trend_title": "##### 📅 Temporal Trends (2019)",
        "trend_x": "Month (2019)",
        "trend_y": "Count",
        "trend_tooltip": "<p class='tooltip'>Area: evolution of sentiments month by month.</p>",
        "trend_no_data": "ℹ️ No temporal data available for this analysis.",
        "dynamic_title": "##### 🌍 Sentiment by Region or Religion",
        "dynamic_filter_label": "View by",
        "dynamic_filter_options": ["Religion", "District"],
        "dynamic_bar_y": "Count",
        "dynamic_bar_tooltip": "<p class='tooltip'>Bars: compare sentiments by {}</p>",
        "details_subheader": "🔍 Zoom into Details",
        "total_feedback": "<div class='stat-card'>📊 <b>Total Feedback</b> : {}</div>",
        "positive": "<div class='stat-card'>😊 <b>Positive</b> : {} ({:.2%})</div>",
        "negative": "<div class='stat-card'>😞 <b>Negative</b> : {} ({:.2%})</div>",
        "neutral": "<div class='stat-card'>😐 <b>Neutral</b> : {} ({:.2%})</div>",
        "examples_title": "<div class='stat-card'>📝 <b>Examples:</b></div>",
        "example_positif": "<div class='stat-card'>😊 <b>Positive</b> : {}</div>",
        "example_négatif": "<div class='stat-card'>😞 <b>Negative</b> : {}</div>",
        "example_neutre": "<div class='stat-card'>😐 <b>Neutral</b> : {}</div>",
        "export_button": "Export Sentiments (CSV)",
        "export_filename": "sentiment_analysis.csv",
        "no_text_error": "❌ No textual data found in 'si_autres_raison_preciser'.",
        "spinner": "Analyzing sentiments...",
        "sentiment_labels": {"Positif": "Positive", "Négatif": "Negative", "Neutre": "Neutral"}
    }
}

@st.cache_data
def load_data():
    url_volontaire = "https://raw.githubusercontent.com/hyontnick/qganalytics_blood_dashboard_indabax/refs/heads/main/APPLICATION/datas/volontaire_clean_corrige.csv"
    url_dates = "https://raw.githubusercontent.com/hyontnick/qganalytics_blood_dashboard_indabax/refs/heads/main/APPLICATION/datas/dates_2019_extraites.csv"
    df_volontaires = pd.read_csv(url_volontaire)
    df_dates = pd.read_csv(url_dates)
    df_merged = df_volontaires.merge(df_dates, left_index=True, right_index=True, how='left')
    return df_merged

def analyze_sentiment(texts):
    """Analyse vectorisée des sentiments avec VADER."""
    analyzer = SentimentIntensityAnalyzer()
    negative_keywords = [
        "maladie", "chronique", "drogue", "infarctus", "angine", "artérite",
        "consommation", "endoscopie", "ménopause"
    ]
    
    texts = texts.fillna("Inconnu").str.lower()
    scores = [analyzer.polarity_scores(text) for text in texts]
    compounds = np.array([score['compound'] for score in scores])
    has_negative = texts.str.contains('|'.join(negative_keywords), case=False, na=False)
    
    sentiments = np.where(compounds >= 0.05, "Positif",
                          np.where((compounds <= -0.05) | has_negative, "Négatif", "Neutre"))
    sentiments = np.where(texts.isin(["", "aucune", "inconnu", "aucune information"]), "Neutre", sentiments)
    return pd.Series(sentiments, index=texts.index)

def show_sentiment(df_unused=None, lang="fr"):
    st.header(translations[lang]["header"])

    # CSS moderne et intuitif
    st.markdown("""
        <style>
        .main-container {border: 2px solid #e0e0e0; padding: 15px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px;}
        .detail-box {background-color: #f5f5f5; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
        .stat-card {background-color: #ffffff; padding: 10px; margin: 5px 0; border-radius: 8px; border: 1px solid #d0d0d0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); font-size: 16px; color: #333333; transition: transform 0.2s;}
        .stat-card:hover {transform: scale(1.05);}
        h3 {color: #2E7D32; margin-top: 0;}
        .tooltip {font-size: 14px; color: #757575;}
        .center-button {display: flex; justify-content: center; margin-top: 20px;}
        </style>
    """, unsafe_allow_html=True)

    # Charger les données
    if df_unused is None:
        df = load_data()
    else:
        df = df_unused.copy()

    # Vérifier la colonne textuelle
    if 'si_autres_raison_preciser' not in df.columns:
        st.write(translations[lang]["no_text_error"])
        return

    # Préparer les données
    df_text = df[['si_autres_raison_preciser', 'age', 'genre', 'religion', 'arrondissement_de_residence']].copy()
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    if date_cols:
        df_text['date_enregistrement'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
    else:
        df_text['date_enregistrement'] = pd.NaT
    df_text['age_group'] = pd.cut(df_text['age'], bins=[0, 25, 35, 45, 65, 100], labels=['18-25', '26-35', '36-45', '46-65', '66+'])

    # Analyse des sentiments
    with st.spinner(translations[lang]["spinner"]):
        df_text['sentiment'] = analyze_sentiment(df_text['si_autres_raison_preciser'])

    # Ligne 1 : Analyse Démographique
    st.subheader(translations[lang]["demo_subheader"])
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(translations[lang]["bar_age_title"])
            fig1 = px.bar(
                df_text.groupby(['age_group', 'sentiment']).size().reset_index(name='count'),
                x='age_group', y='count', color='sentiment',
                barmode='stack', labels={'age_group': translations[lang]["bar_age_x"], 'count': translations[lang]["bar_age_y"]},
                color_discrete_map={translations[lang]["sentiment_labels"]["Positif"]: '#2E7D32', translations[lang]["sentiment_labels"]["Négatif"]: '#C62828', translations[lang]["sentiment_labels"]["Neutre"]: '#757575'},
                height=300, hover_data={'count': True}
            )
            fig1.update_traces(hovertemplate=f"{translations[lang]['bar_age_x']}: %{{x}}<br>{translations[lang]['bar_sentiment_x']}: %{{customdata[0]}}<br>{translations[lang]['bar_age_y']}: %{{y}}", customdata=df_text.groupby(['age_group', 'sentiment']).size().reset_index()[['sentiment']])
            fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(translations[lang]["bar_age_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["bar_sentiment_title"])
            fig2 = px.bar(
                df_text['sentiment'].value_counts().reset_index(),
                x='count', y='sentiment', orientation='h',
                color='sentiment', color_discrete_map={translations[lang]["sentiment_labels"]["Positif"]: '#2E7D32', translations[lang]["sentiment_labels"]["Négatif"]: '#C62828', translations[lang]["sentiment_labels"]["Neutre"]: '#757575'},
                labels={'sentiment': translations[lang]["bar_sentiment_x"], 'count': translations[lang]["bar_sentiment_y"]},
                height=300
            )
            fig2.update_traces(hovertemplate=f"{translations[lang]['bar_sentiment_x']}: %{{y}}<br>{translations[lang]['bar_sentiment_y']}: %{{x}}", textposition='auto', text=df_text['sentiment'].value_counts())
            fig2.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(translations[lang]["bar_sentiment_tooltip"], unsafe_allow_html=True)

        with col3:
            st.markdown(translations[lang]["bar_age_gender_title"])
            df_age_genre = df_text.groupby(['age_group', 'genre', 'sentiment']).size().reset_index(name='count')
            fig3 = px.bar(
                df_age_genre,
                x='age_group', y='count', color='sentiment',
                barmode='group', facet_col='genre',
                labels={'age_group': translations[lang]["bar_age_gender_x"], 'count': translations[lang]["bar_age_gender_y"], 'genre': translations[lang]["bar_age_gender_facet"]},
                color_discrete_map={translations[lang]["sentiment_labels"]["Positif"]: '#2E7D32', translations[lang]["sentiment_labels"]["Négatif"]: '#C62828', translations[lang]["sentiment_labels"]["Neutre"]: '#757575'},
                height=300
            )
            fig3.update_traces(hovertemplate=f"{translations[lang]['bar_age_gender_x']}: %{{x}}<br>{translations[lang]['bar_age_gender_facet']}: %{{customdata[0]}}<br>{translations[lang]['bar_sentiment_x']}: %{{customdata[1]}}<br>{translations[lang]['bar_age_gender_y']}: %{{y}}", customdata=df_age_genre[['genre', 'sentiment']])
            fig3.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(translations[lang]["bar_age_gender_tooltip"], unsafe_allow_html=True)

    # Ligne 2 : Analyse Temporelle + Sentiment par Région/Religion
    st.subheader(translations[lang]["temporal_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["trend_title"])
            if 'date_enregistrement' in df_text.columns and not df_text['date_enregistrement'].isna().all():
                df_text['mois'] = df_text['date_enregistrement'].dt.strftime('%B')
                time_data = df_text.groupby(['mois', 'sentiment']).size().reset_index(name='count')
                fig4 = px.area(
                    time_data, x='mois', y='count', color='sentiment',
                    labels={'mois': translations[lang]["trend_x"], 'count': translations[lang]["trend_y"]},
                    color_discrete_map={translations[lang]["sentiment_labels"]["Positif"]: '#2E7D32', translations[lang]["sentiment_labels"]["Négatif"]: '#C62828', translations[lang]["sentiment_labels"]["Neutre"]: '#757575'},
                    height=350, category_orders={'mois': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}
                )
                fig4.update_traces(hovertemplate=f"{translations[lang]['trend_x']}: %{{x}}<br>{translations[lang]['bar_sentiment_x']}: %{{customdata[0]}}<br>{translations[lang]['trend_y']}: %{{y}}", customdata=time_data[['sentiment']])
                fig4.update_layout(margin=dict(l=20, r=20, t=20, b=20), xaxis={'tickangle': -45})
                st.plotly_chart(fig4, use_container_width=True)
                st.markdown(translations[lang]["trend_tooltip"], unsafe_allow_html=True)
            else:
                st.write(translations[lang]["trend_no_data"])

        with col2:
            st.markdown(translations[lang]["dynamic_title"])
            filter_by = st.selectbox(translations[lang]["dynamic_filter_label"], translations[lang]["dynamic_filter_options"], key="dynamic_filter")
            if filter_by == translations[lang]["dynamic_filter_options"][0]:  # Religion
                df_dynamic = df_text.groupby(['religion', 'sentiment']).size().reset_index(name='count')
                x_axis = 'religion'
            else:  # Arrondissement/District
                df_dynamic = df_text.groupby(['arrondissement_de_residence', 'sentiment']).size().reset_index(name='count')
                x_axis = 'arrondissement_de_residence'
            
            fig5 = px.bar(
                df_dynamic, x=x_axis, y='count', color='sentiment',
                barmode='group', labels={x_axis: filter_by, 'count': translations[lang]["dynamic_bar_y"]},
                color_discrete_map={translations[lang]["sentiment_labels"]["Positif"]: '#2E7D32', translations[lang]["sentiment_labels"]["Négatif"]: '#C62828', translations[lang]["sentiment_labels"]["Neutre"]: '#757575'},
                height=300
            )
            fig5.update_traces(hovertemplate=f"{filter_by}: %{{x}}<br>{translations[lang]['bar_sentiment_x']}: %{{customdata[0]}}<br>{translations[lang]['dynamic_bar_y']}: %{{y}}", customdata=df_dynamic[['sentiment']])
            fig5.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown(translations[lang]["dynamic_bar_tooltip"].format(filter_by.lower()), unsafe_allow_html=True)

    # Ligne 3 : Détails
    st.subheader(translations[lang]["details_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            sentiment_counts = df_text['sentiment'].value_counts()
            total = len(df_text)
            st.markdown(translations[lang]["total_feedback"].format(total), unsafe_allow_html=True)
            st.markdown(translations[lang]["positive"].format(sentiment_counts.get("Positif", 0), sentiment_counts.get("Positif", 0)/total), unsafe_allow_html=True)
            st.markdown(translations[lang]["negative"].format(sentiment_counts.get("Négatif", 0), sentiment_counts.get("Négatif", 0)/total), unsafe_allow_html=True)
            st.markdown(translations[lang]["neutral"].format(sentiment_counts.get("Neutre", 0), sentiment_counts.get("Neutre", 0)/total), unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["examples_title"], unsafe_allow_html=True)
            example_keys = {
                "fr": {"Positif": "example_positif", "Négatif": "example_négatif", "Neutre": "example_neutre"},
                "en": {"Positif": "example_positif", "Négatif": "example_négatif", "Neutre": "example_neutre"}
            }
            for sentiment in ["Positif", "Négatif", "Neutre"]:
                example = df_text[df_text['sentiment'] == sentiment]['si_autres_raison_preciser'].iloc[0] if sentiment in df_text['sentiment'].values else "Aucun" if lang == "fr" else "None"
                key = example_keys[lang][sentiment]
                st.markdown(translations[lang][key].format(example), unsafe_allow_html=True)

        # Bouton d’exportation centré
        csv = df_text[['si_autres_raison_preciser', 'sentiment', 'age', 'genre', 'religion', 'arrondissement_de_residence']].to_csv(index=False).encode('utf-8')
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        st.download_button(
            label=translations[lang]["export_button"],
            data=csv,
            file_name=translations[lang]["export_filename"],
            mime="text/csv"
        )
        st.markdown("</div>", unsafe_allow_html=True)
