import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Dictionnaire de traductions pour le module Fidélisation des Donneurs
translations = {
    "fr": {
        "header": "🤝 Fidélisation des Donneurs",
        "overview_subheader": "📊 Vue d’ensemble",
        "pie_title": "##### 🍰 Récurrence des Dons",
        "pie_tooltip": "<p class='tooltip'>Donut : proportion des donneurs récents, anciens et jamais.</p>",
        "trend_title": "##### 📅 Tendances Temporelles",
        "trend_x": "Année",
        "trend_y": "Nombre de Dons",
        "trend_tooltip": "<p class='tooltip'>Aire : évolution des dons par année.</p>",
        "trend_no_data": "ℹ️ Pas de données de dates pour les dons.",
        "demo_subheader": "👥 Qui donne ?",
        "heatmap_title": "##### 🔥 Récurrence par Âge",
        "heatmap_x": "Récurrence",
        "heatmap_y": "Âge",
        "heatmap_color": "Nombre",
        "heatmap_tooltip": "<p class='tooltip'>Couleurs : rouge = plus de donneurs, bleu = moins.</p>",
        "treemap_title": "##### 💼 Récurrence par Profession",
        "treemap_tooltip": "<p class='tooltip'>Carrés : taille = nombre de donneurs par profession.</p>",
        "geo_subheader": "🏡 Où donnent-ils ?",
        "geo_filter_label": "Voir par",
        "geo_filter_options": ["Arrondissement", "Quartier"],
        "geo_bar_title": "##### 🏡 Récurrence Géographique",
        "geo_bar_y": "Nombre",
        "geo_bar_tooltip": "<p class='tooltip'>Barres : compare les donneurs par {}</p>",
        "details_subheader": "🔍 Détails",
        "total_volunteers": "👥 <b>Total des volontaires</b> : {}",
        "recent_donors": "⏳ <b>Récents (<3 ans)</b> : {} ({:.2%})",
        "never_donated": "🚫 <b>Jamais donné</b> : {} ({:.2%})",
        "old_donors": "⌛ <b>Anciens (3+ ans)</b> : {} ({:.2%})",
        "avg_age_recurrent": "🎂 <b>Âge moyen des récurrents</b> : {:.1f} ans",
        "export_button": "Exporter les données (CSV)",
        "export_filename": "fidelisation_donneurs.csv",
        "missing_cols_error": "❌ Colonnes manquantes : {}",
        "recurrence_labels": {
            "Récent (<3 ans)": "Récent (<3 ans)",
            "Ancien (3+ ans)": "Ancien (3+ ans)",
            "Jamais": "Jamais"
        }
    },
    "en": {
        "header": "🤝 Donor Retention",
        "overview_subheader": "📊 Overview",
        "pie_title": "##### 🍰 Donation Recurrence",
        "pie_tooltip": "<p class='tooltip'>Donut: proportion of recent, past, and never donors.</p>",
        "trend_title": "##### 📅 Temporal Trends",
        "trend_x": "Year",
        "trend_y": "Number of Donations",
        "trend_tooltip": "<p class='tooltip'>Area: evolution of donations by year.</p>",
        "trend_no_data": "ℹ️ No date data available for donations.",
        "demo_subheader": "👥 Who donates?",
        "heatmap_title": "##### 🔥 Recurrence by Age",
        "heatmap_x": "Recurrence",
        "heatmap_y": "Age",
        "heatmap_color": "Count",
        "heatmap_tooltip": "<p class='tooltip'>Colors: red = more donors, blue = fewer.</p>",
        "treemap_title": "##### 💼 Recurrence by Profession",
        "treemap_tooltip": "<p class='tooltip'>Squares: size = number of donors by profession.</p>",
        "geo_subheader": "🏡 Where do they donate?",
        "geo_filter_label": "View by",
        "geo_filter_options": ["District", "Neighborhood"],
        "geo_bar_title": "##### 🏡 Geographic Recurrence",
        "geo_bar_y": "Count",
        "geo_bar_tooltip": "<p class='tooltip'>Bars: compare donors by {}</p>",
        "details_subheader": "🔍 Details",
        "total_volunteers": "👥 <b>Total Volunteers</b> : {}",
        "recent_donors": "⏳ <b>Recent (<3 years)</b> : {} ({:.2%})",
        "never_donated": "🚫 <b>Never Donated</b> : {} ({:.2%})",
        "old_donors": "⌛ <b>Past (3+ years)</b> : {} ({:.2%})",
        "avg_age_recurrent": "🎂 <b>Average Age of Recurring Donors</b> : {:.1f} years",
        "export_button": "Export Data (CSV)",
        "export_filename": "donor_retention.csv",
        "missing_cols_error": "❌ Missing columns: {}",
        "recurrence_labels": {
            "Récent (<3 ans)": "Recent (<3 years)",
            "Ancien (3+ ans)": "Past (3+ years)",
            "Jamais": "Never"
        }
    }
}

@st.cache_data
def load_data():
    url_volontaire = "https://raw.githubusercontent.com/hyontnick/qganalytics_blood_dashboard_indabax/refs/heads/main/APPLICATION/datas/volontaire_clean_corrige.csv"
    df = pd.read_csv(url_volontaire)
    return df

def show_fidelisation(df_unused=None, lang="fr"):
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

    # Vérifier les colonnes nécessaires
    required_cols = ['a_til_elle_deja_donne_le_sang', 'si_oui_preciser_la_date_du_dernier_don', 'age', 'profession', 'arrondissement_de_residence', 'quartier_de_residence']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.write(translations[lang]["missing_cols_error"].format(', '.join(missing_cols)))
        return

    # Préparer les données
    df['si_oui_preciser_la_date_du_dernier_don'] = pd.to_datetime(df['si_oui_preciser_la_date_du_dernier_don'], errors='coerce')
    current_year = datetime.now().year
    df['annees_depuis_dernier_don'] = df.apply(
        lambda row: (current_year - row['si_oui_preciser_la_date_du_dernier_don'].year) if row['a_til_elle_deja_donne_le_sang'] == 'Oui' and pd.notna(row['si_oui_preciser_la_date_du_dernier_don']) else None,
        axis=1
    )
    df['recurrence'] = df['annees_depuis_dernier_don'].apply(
        lambda x: translations[lang]["recurrence_labels"]["Récent (<3 ans)"] if pd.notna(x) and x < 3 else translations[lang]["recurrence_labels"]["Ancien (3+ ans)"] if pd.notna(x) else translations[lang]["recurrence_labels"]["Jamais"]
    )
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 65, 100], labels=['18-25', '26-35', '36-45', '46-65', '66+'])

    # Ligne 1 : Analyse Globale
    st.subheader(translations[lang]["overview_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["pie_title"])
            fig1 = px.pie(
                df['recurrence'].value_counts().reset_index(),
                values='count', names='recurrence',
                color='recurrence', color_discrete_map={
                    translations[lang]["recurrence_labels"]["Récent (<3 ans)"]: '#2E7D32',
                    translations[lang]["recurrence_labels"]["Ancien (3+ ans)"]: '#FFB300',
                    translations[lang]["recurrence_labels"]["Jamais"]: '#757575'
                },
                height=300, hole=0.4,
                hover_data=['count']
            )
            fig1.update_traces(hovertemplate=f"{translations[lang]['heatmap_x']}: %{{label}}<br>{translations[lang]['geo_bar_y']}: %{{value}} (%{{percent}})")
            fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(translations[lang]["pie_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["trend_title"])
            if df['si_oui_preciser_la_date_du_dernier_don'].notna().any():
                df_time = df[df['a_til_elle_deja_donne_le_sang'] == 'Oui'].groupby(df['si_oui_preciser_la_date_du_dernier_don'].dt.year).size().reset_index(name='count')
                fig2 = px.area(
                    df_time, x='si_oui_preciser_la_date_du_dernier_don', y='count',
                    labels={'si_oui_preciser_la_date_du_dernier_don': translations[lang]["trend_x"], 'count': translations[lang]["trend_y"]},
                    color_discrete_sequence=['#2E7D32'],
                    height=300
                )
                fig2.update_traces(hovertemplate=f"{translations[lang]['trend_x']}: %{{x}}<br>{translations[lang]['trend_y']}: %{{y}}")
                fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown(translations[lang]["trend_tooltip"], unsafe_allow_html=True)
            else:
                st.write(translations[lang]["trend_no_data"])

    # Ligne 2 : Analyse Démographique
    st.subheader(translations[lang]["demo_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["heatmap_title"])
            heatmap_data = df.groupby(['age_group', 'recurrence']).size().unstack(fill_value=0)
            fig3 = px.imshow(
                heatmap_data, text_auto=True, color_continuous_scale='RdBu_r',
                labels=dict(x=translations[lang]["heatmap_x"], y=translations[lang]["heatmap_y"], color=translations[lang]["heatmap_color"]),
                height=300
            )
            fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(translations[lang]["heatmap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["treemap_title"])
            fig4 = px.treemap(
                df.groupby(['profession', 'recurrence']).size().reset_index(name='count'),
                path=['profession', 'recurrence'], values='count',
                color='recurrence', color_discrete_map={
                    translations[lang]["recurrence_labels"]["Récent (<3 ans)"]: '#2E7D32',
                    translations[lang]["recurrence_labels"]["Ancien (3+ ans)"]: '#FFB300',
                    translations[lang]["recurrence_labels"]["Jamais"]: '#757575'
                },
                height=300
            )
            fig4.update_traces(hovertemplate=f"Profession: %{{label}}<br>{translations[lang]['geo_bar_y']}: %{{value}}")
            fig4.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown(translations[lang]["treemap_tooltip"], unsafe_allow_html=True)

    # Ligne 3 : Analyse Géographique
    st.subheader(translations[lang]["geo_subheader"])
    with st.container():
        filter_by = st.selectbox(translations[lang]["geo_filter_label"], translations[lang]["geo_filter_options"], key="geo_filter")
        st.markdown(translations[lang]["geo_bar_title"])
        if filter_by == translations[lang]["geo_filter_options"][0]:  # Arrondissement/District
            df_geo = df.groupby(['arrondissement_de_residence', 'recurrence']).size().reset_index(name='count')
            x_axis = 'arrondissement_de_residence'
        else:  # Quartier/Neighborhood
            df_geo = df.groupby(['quartier_de_residence', 'recurrence']).size().reset_index(name='count')
            x_axis = 'quartier_de_residence'
        fig5 = px.bar(
            df_geo, x=x_axis, y='count', color='recurrence',
            barmode='group', labels={x_axis: filter_by, 'count': translations[lang]["geo_bar_y"]},
            color_discrete_map={
                translations[lang]["recurrence_labels"]["Récent (<3 ans)"]: '#2E7D32',
                translations[lang]["recurrence_labels"]["Ancien (3+ ans)"]: '#FFB300',
                translations[lang]["recurrence_labels"]["Jamais"]: '#757575'
            },
            height=350
        )
        fig5.update_traces(hovertemplate=f"{filter_by}: %{{x}}<br>{translations[lang]['heatmap_x']}: %{{customdata[0]}}<br>{translations[lang]['geo_bar_y']}: %{{y}}", customdata=df_geo[['recurrence']].values)
        fig5.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown(translations[lang]["geo_bar_tooltip"].format(filter_by.lower()), unsafe_allow_html=True)

    # Ligne 4 : Détails
    st.subheader(translations[lang]["details_subheader"])
    with st.container():
        col1, col2, col3 = st.columns(3)
        recurrence_counts = df['recurrence'].value_counts()
        total = len(df)
        recent_label = translations[lang]["recurrence_labels"]["Récent (<3 ans)"]
        past_label = translations[lang]["recurrence_labels"]["Ancien (3+ ans)"]
        never_label = translations[lang]["recurrence_labels"]["Jamais"]
        with col1:
            st.markdown(f"<div class='stat-card'>{translations[lang]['total_volunteers'].format(total)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['recent_donors'].format(recurrence_counts.get(recent_label, 0), recurrence_counts.get(recent_label, 0)/total)}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'>{translations[lang]['never_donated'].format(recurrence_counts.get(never_label, 0), recurrence_counts.get(never_label, 0)/total)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['avg_age_recurrent'].format(df[df['recurrence'] != never_label]['age'].mean())}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-card'>{translations[lang]['old_donors'].format(recurrence_counts.get(past_label, 0), recurrence_counts.get(past_label, 0)/total)}</div>", unsafe_allow_html=True)

        # Bouton d’exportation centré
        csv = df[['a_til_elle_deja_donne_le_sang', 'si_oui_preciser_la_date_du_dernier_don', 'recurrence', 'age', 'profession', 'arrondissement_de_residence', 'quartier_de_residence']].to_csv(index=False).encode('utf-8')
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        st.download_button(
            label=translations[lang]["export_button"],
            data=csv,
            file_name=translations[lang]["export_filename"],
            mime="text/csv"
        )
        st.markdown("</div>", unsafe_allow_html=True)
