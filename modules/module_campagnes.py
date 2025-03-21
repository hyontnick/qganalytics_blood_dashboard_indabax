import streamlit as st
import pandas as pd
import plotly.express as px

# Dictionnaire de traductions pour le module Analyse des Campagnes
translations = {
    "fr": {
        "header": "📅 Analyse de l’Efficacité des Campagnes",
        "temporal_subheader": "📅 Quand les gens participent-ils ?",
        "heatmap_title": "##### 🔥 Participation par Mois et Âge (2019)",
        "heatmap_x": "Âge",
        "heatmap_y": "Mois",
        "heatmap_color": "Nombre",
        "heatmap_tooltip": "<p class='tooltip'>Couleurs : rouge = plus de participants, bleu = moins.</p>",
        "line_title": "##### 📈 Évolution Mensuelle (2019)",
        "line_x": "Mois",
        "line_y": "Nombre de Participants",
        "line_cumul": "Cumul",
        "line_tooltip": "<p class='tooltip'>Ligne : participants par mois, pointillés = total cumulé.</p>",
        "demo_subheader": "Analyse Démographique",
        "treemap_title": "##### 🌳 Répartition par Genre et Âge",
        "treemap_tooltip": "<p class='tooltip'>Carrés : taille = nombre de participants par genre et âge.</p>",
        "histogram_title": "##### 👤 Participants par Âge",
        "histogram_x": "Tranche d’Âge",
        "histogram_y": "Nombre",
        "histogram_tooltip": "<p class='tooltip'>Barres : nombre de participants par âge.</p>",
        "filter_label": "Voir par",
        "filter_options": ["Arrondissement", "Religion", "Niveau d’étude"],
        "area_title": "##### 📊 Participants par {}",
        "area_y": "Nombre",
        "area_tooltip": "<p class='tooltip'>Barres : nombre de participants par {}</p>",
        "details_subheader": "🔍 Détails",
        "total_participants": "📊 <b>Total des participants</b> : {}",
        "average_age": "🎂 <b>Âge moyen</b> : {} ans",
        "percent_men": "👨 <b>Pourcentage Hommes</b> : {:.2%}",
        "percent_women": "👩 <b>Pourcentage Femmes</b> : {:.2%}",
        "most_active_month": "📅 <b>Mois le plus actif</b> : {}",
        "dominant_arrondissement": "🏡 <b>Arrondissement dominant</b> : {}",
        "export_button": "Exporter les données (CSV)",
        "export_filename": "analyse_campagnes.csv",
        "missing_cols_error": "❌ Colonnes manquantes : {}"
    },
    "en": {
        "header": "📅 Campaign Effectiveness Analysis",
        "temporal_subheader": "📅 When do people participate?",
        "heatmap_title": "##### 🔥 Participation by Month and Age (2019)",
        "heatmap_x": "Age",
        "heatmap_y": "Month",
        "heatmap_color": "Count",
        "heatmap_tooltip": "<p class='tooltip'>Colors: red = more participants, blue = fewer.</p>",
        "line_title": "##### 📈 Monthly Evolution (2019)",
        "line_x": "Month",
        "line_y": "Number of Participants",
        "line_cumul": "Cumulative",
        "line_tooltip": "<p class='tooltip'>Line: participants per month, dashed = cumulative total.</p>",
        "demo_subheader": "Demographic Analysis",
        "treemap_title": "##### 🌳 Breakdown by Gender and Age",
        "treemap_tooltip": "<p class='tooltip'>Squares: size = number of participants by gender and age.</p>",
        "histogram_title": "##### 👤 Participants by Age",
        "histogram_x": "Age Group",
        "histogram_y": "Count",
        "histogram_tooltip": "<p class='tooltip'>Bars: number of participants by age.</p>",
        "filter_label": "View by",
        "filter_options": ["District", "Religion", "Education Level"],
        "area_title": "##### 📊 Participants by {}",
        "area_y": "Count",
        "area_tooltip": "<p class='tooltip'>Bars: number of participants by {}</p>",
        "details_subheader": "🔍 Details",
        "total_participants": "📊 <b>Total Participants</b> : {}",
        "average_age": "🎂 <b>Average Age</b> : {} years",
        "percent_men": "👨 <b>Percentage Men</b> : {:.2%}",
        "percent_women": "👩 <b>Percentage Women</b> : {:.2%}",
        "most_active_month": "📅 <b>Most Active Month</b> : {}",
        "dominant_arrondissement": "🏡 <b>Dominant District</b> : {}",
        "export_button": "Export Data (CSV)",
        "export_filename": "campaign_analysis.csv",
        "missing_cols_error": "❌ Missing columns: {}"
    }
}

def show_campagnes(df_unused, lang="fr"):
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

    df = df_unused.copy()

    # Vérifier les colonnes nécessaires
    required_cols = ['age', 'genre', 'arrondissement_de_residence', 'date_de_remplissage_de_la_fiche', 'religion', 'niveau_detude']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.write(translations[lang]["missing_cols_error"].format(', '.join(missing_cols)))
        return

    # Préparer les données
    df['date_de_remplissage_de_la_fiche'] = pd.to_datetime(df['date_de_remplissage_de_la_fiche'], errors='coerce')
    df['mois'] = df['date_de_remplissage_de_la_fiche'].dt.strftime('%B')
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 65, 100], labels=['18-25', '26-35', '36-45', '46-65', '66+'])

    # Ligne 1 : Tendances Temporelles
    st.subheader(translations[lang]["temporal_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["heatmap_title"])
            heatmap_data = df.groupby(['mois', 'age_group']).size().unstack(fill_value=0)
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            heatmap_data = heatmap_data.reindex(month_order, fill_value=0)
            fig1 = px.imshow(
                heatmap_data, text_auto=True, color_continuous_scale='RdBu_r',
                labels=dict(x=translations[lang]["heatmap_x"], y=translations[lang]["heatmap_y"], color=translations[lang]["heatmap_color"]),
                height=350
            )
            fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(translations[lang]["heatmap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["line_title"])
            df_month = df['mois'].value_counts().reset_index().sort_values(by='mois', key=lambda x: pd.Categorical(x, categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True))
            df_month['cumul'] = df_month['count'].cumsum()
            fig2 = px.line(
                df_month, x='mois', y='count',
                labels={'mois': translations[lang]["line_x"], 'count': translations[lang]["line_y"]},
                color_discrete_sequence=['#2E7D32'],
                height=350,
                markers=True
            )
            fig2.add_scatter(x=df_month['mois'], y=df_month['cumul'], mode='lines', name=translations[lang]["line_cumul"], line=dict(color='#FFB300', dash='dash'))
            fig2.update_traces(hovertemplate=f"{translations[lang]['line_x']}: %{{x}}<br>{translations[lang]['line_y']}: %{{y}}")
            fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(translations[lang]["line_tooltip"], unsafe_allow_html=True)

    # Ligne 2 : Analyse Démographique
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["treemap_title"])
            fig3 = px.treemap(
                df.groupby(['genre', 'age_group']).size().reset_index(name='count'),
                path=['genre', 'age_group'], values='count',
                color='genre', color_discrete_map={'Homme': '#1976D2', 'Femme': '#F06292'},
                height=300
            )
            fig3.update_traces(hovertemplate=f"Genre: %{{label}}<br>{translations[lang]['histogram_y']}: %{{value}}")
            fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(translations[lang]["treemap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["histogram_title"])
            fig5 = px.histogram(
                df, x='age_group',
                labels={'age_group': translations[lang]["histogram_x"], 'count': translations[lang]["histogram_y"]},
                color_discrete_sequence=['#FFB300'],
                height=300
            )
            fig5.update_traces(hovertemplate=f"{translations[lang]['histogram_x']}: %{{x}}<br>{translations[lang]['histogram_y']}: %{{y}}")
            fig5.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown(translations[lang]["histogram_tooltip"], unsafe_allow_html=True)

    # Ligne 3 : Filtre Dynamique
    with st.container():
        filter_by = st.selectbox(translations[lang]["filter_label"], translations[lang]["filter_options"], key="demo_filter")
        st.markdown(translations[lang]["area_title"].format(filter_by))
        if filter_by == translations[lang]["filter_options"][0]:  # Arrondissement/District
            df_demo = df['arrondissement_de_residence'].value_counts().reset_index()
            x_axis = 'arrondissement_de_residence'
        elif filter_by == translations[lang]["filter_options"][1]:  # Religion
            df_demo = df['religion'].value_counts().reset_index()
            x_axis = 'religion'
        else:  # Niveau d’étude/Education Level
            df_demo = df['niveau_detude'].value_counts().reset_index()
            x_axis = 'niveau_detude'
        fig4 = px.area(
            df_demo, x=x_axis, y='count',
            labels={x_axis: filter_by, 'count': translations[lang]["area_y"]},
            color_discrete_sequence=['#1E88E5'],
            height=300
        )
        fig4.update_traces(hovertemplate=f"{filter_by}: %{{x}}<br>{translations[lang]['area_y']}: %{{y}}")
        fig4.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown(translations[lang]["area_tooltip"].format(filter_by.lower()), unsafe_allow_html=True)

    # Ligne 4 : Détails
    st.subheader(translations[lang]["details_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='stat-card'>{translations[lang]['total_participants'].format(len(df))}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['average_age'].format(int(df['age'].mean()))}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['percent_men'].format((df['genre'] == 'Homme').mean())}</div>", unsafe_allow_html=True)
        with col2:
            most_common_month = df['mois'].mode()[0] if not df['mois'].isna().all() else "N/A"
            st.markdown(f"<div class='stat-card'>{translations[lang]['most_active_month'].format(most_common_month)}</div>", unsafe_allow_html=True)
            most_common_arr = df['arrondissement_de_residence'].mode()[0] if not df.empty else "N/A"
            st.markdown(f"<div class='stat-card'>{translations[lang]['dominant_arrondissement'].format(most_common_arr)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['percent_women'].format((df['genre'] == 'Femme').mean())}</div>", unsafe_allow_html=True)

        # Bouton d’exportation centré
        csv = df[['age', 'genre', 'arrondissement_de_residence', 'date_de_remplissage_de_la_fiche', 'religion', 'niveau_detude', 'mois', 'age_group']].to_csv(index=False).encode('utf-8')
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        st.download_button(
            label=translations[lang]["export_button"],
            data=csv,
            file_name=translations[lang]["export_filename"],
            mime="text/csv"
        )
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    # Exemple d’appel avec un DataFrame fictif pour tester
    df_test = pd.DataFrame({
        'age': [20, 30, 40, 50, 60],
        'genre': ['Homme', 'Femme', 'Homme', 'Femme', 'Homme'],
        'arrondissement_de_residence': ['Arr1', 'Arr2', 'Arr1', 'Arr3', 'Arr2'],
        'date_de_remplissage_de_la_fiche': ['2019-01-01', '2019-03-15', '2019-06-20', '2019-09-10', '2019-12-05'],
        'religion': ['Rel1', 'Rel2', 'Rel1', 'Rel3', 'Rel2'],
        'niveau_detude': ['Bac', 'Licence', 'Master', 'Bac', 'Doctorat']
    })
    show_campagnes(df_test, lang="fr")  # Test avec français par défaut