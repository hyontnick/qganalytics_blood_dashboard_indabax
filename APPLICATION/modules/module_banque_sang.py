import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Dictionnaire de traductions pour le module Banque de Sang
translations = {
    "fr": {
        "header": "🩺 Banque de Sang 2019",
        "filters_subheader": "🔎 Filtres",
        "blood_group": "Groupe Sanguin",
        "sex": "Sexe",
        "age": "Âge",
        "donation_type": "Type de Donation",
        "analysis_subheader": "📈 Analyse des Dons",
        "pie_blood_group": "#### 🍰 % par Groupe Sanguin",
        "pie_donation_type": "#### 🎯 % par Type de Donation",
        "heatmap_title": "#### 🔥 Corrélation Groupe Sanguin et Sexe",
        "bar_blood_group": "#### 🩺 Dons par Groupe Sanguin",
        "bar_sex": "#### 👥 Dons par Sexe",
        "temporal_trends": "#### 📅 Tendances Temporelles",
        "display_by": "Afficher par",
        "display_options": ["Mois", "Jour", "Heure"],
        "month_label": "Mois",
        "day_label": "Jour du Mois",
        "hour_label": "Heure (0-23)",
        "donations_label": "Nombre de Dons",
        "details_subheader": "🔍 Détails",
        "total_donations": "🩺 <b>Total des dons filtrés</b> : {}",
        "average_age": "🎂 <b>Âge moyen</b> : {} ans",
        "percent_men": "👨 <b>Pourcentage Hommes</b> : {:.2%}",
        "percent_women": "👩 <b>Pourcentage Femmes</b> : {:.2%}",
        "most_common_group": "🩺 <b>Groupe le plus fréquent</b> : {}",
        "dominant_phenotype": "🧬 <b>Phénotype dominant</b> : {}",
        "unique_groups": "🔢 <b>Groupes uniques</b> : {}",
        "export_button": "Exporter les données filtrées (CSV)",
        "export_filename": "banque_sang_2020_filtre.csv",
        "no_donation_data": "ℹ️ Données sur le type de donation non disponibles."
    },
    "en": {
        "header": "🩺 Blood Bank 2019",
        "filters_subheader": "🔎 Filters",
        "blood_group": "Blood Group",
        "sex": "Gender",
        "age": "Age",
        "donation_type": "Donation Type",
        "analysis_subheader": "📈 Donation Analysis",
        "pie_blood_group": "#### 🍰 % by Blood Group",
        "pie_donation_type": "#### 🎯 % by Donation Type",
        "heatmap_title": "#### 🔥 Blood Group and Gender Correlation",
        "bar_blood_group": "#### 🩺 Donations by Blood Group",
        "bar_sex": "#### 👥 Donations by Gender",
        "temporal_trends": "#### 📅 Temporal Trends",
        "display_by": "Display by",
        "display_options": ["Month", "Day", "Hour"],
        "month_label": "Month",
        "day_label": "Day of Month",
        "hour_label": "Hour (0-23)",
        "donations_label": "Number of Donations",
        "details_subheader": "🔍 Details",
        "total_donations": "🩺 <b>Total Filtered Donations</b> : {}",
        "average_age": "🎂 <b>Average Age</b> : {} years",
        "percent_men": "👨 <b>Percentage Men</b> : {:.2%}",
        "percent_women": "👩 <b>Percentage Women</b> : {:.2%}",
        "most_common_group": "🩺 <b>Most Common Group</b> : {}",
        "dominant_phenotype": "🧬 <b>Dominant Phenotype</b> : {}",
        "unique_groups": "🔢 <b>Unique Groups</b> : {}",
        "export_button": "Export Filtered Data (CSV)",
        "export_filename": "blood_bank_2020_filtered.csv",
        "no_donation_data": "ℹ️ Donation type data not available."
    }
}

@st.cache_data
def load_banque_sang():
    df = pd.read_csv('../datas/2020_clean.csv')
    df['horodateur'] = pd.to_datetime(df['horodateur'])
    df['mois'] = df['horodateur'].dt.month_name()
    df['jour'] = df['horodateur'].dt.day
    df['heure'] = df['horodateur'].dt.hour
    return df

def show_banque_sang(df_unused=None, lang="fr"):
    st.header(translations[lang]["header"])
    
    # CSS amélioré
    st.markdown("""
        <style>
        .main-container {border: 2px solid #e0e0e0; padding: 15px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px;}
        .detail-box {background-color: #f5f5f5; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
        .stat-card {background-color: #ffffff; padding: 10px; margin: 5px 0; border-radius: 8px; border: 1px solid #d0d0d0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); font-size: 16px; color: #333333; transition: transform 0.2s;}
        .stat-card:hover {transform: scale(1.05);}
        h3 {color: #2E7D32; margin-top: 0;}
        </style>
    """, unsafe_allow_html=True)

    # Charger les données
    df_banque = load_banque_sang()

    # Filtres dynamiques
    st.subheader(translations[lang]["filters_subheader"])
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        groupes = st.multiselect(translations[lang]["blood_group"], options=df_banque['groupe_sanguin_abo__rhesus'].unique(), default=df_banque['groupe_sanguin_abo__rhesus'].unique())
    with col_f2:
        sexes = st.multiselect(translations[lang]["sex"], options=df_banque['sexe'].unique(), default=df_banque['sexe'].unique())
    with col_f3:
        age_range = st.slider(translations[lang]["age"], min_value=int(df_banque['age'].min()), max_value=int(df_banque['age'].max()), value=(int(df_banque['age'].min()), int(df_banque['age'].max())))
    with col_f4:
        type_de_donation = st.multiselect(translations[lang]["donation_type"], options=df_banque['type_de_donation'].unique(), default=df_banque['type_de_donation'].unique())

    # Filtrer les données
    df_filtered = df_banque[
        (df_banque['groupe_sanguin_abo__rhesus'].isin(groupes)) &
        (df_banque['sexe'].isin(sexes)) &
        (df_banque['age'].between(age_range[0], age_range[1])) &
        (df_banque['type_de_donation'].isin(type_de_donation))
    ]

    # Section 1 : Analyse des Dons
    st.subheader(translations[lang]["analysis_subheader"])
    with st.container():
        col_pie1, col_pie2, col_heat = st.columns([1, 1, 2])
        with col_pie1:
            st.markdown(translations[lang]["pie_blood_group"])
            fig_pie1 = px.pie(
                df_filtered['groupe_sanguin_abo__rhesus'].value_counts().reset_index(),
                values='count', names='groupe_sanguin_abo__rhesus',
                color_discrete_sequence=px.colors.qualitative.Pastel2,
                height=250, hole=0.3,
                hover_data={'count': True},
                labels={'count': translations[lang]["donations_label"]}
            )
            fig_pie1.update_traces(textinfo='percent+label', hovertemplate="%{label}: %{value} dons (%{percent})")
            fig_pie1.update_layout(margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
            st.plotly_chart(fig_pie1, use_container_width=True)

        with col_pie2:
            st.markdown(translations[lang]["pie_donation_type"])
            if 'type_de_donation' in df_filtered.columns and not df_filtered['type_de_donation'].isna().all():
                fig_pie2 = px.pie(
                    df_filtered['type_de_donation'].value_counts().reset_index(),
                    values='count', names='type_de_donation',
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    height=250, hole=0.3,
                    hover_data={'count': True},
                    labels={'count': translations[lang]["donations_label"]}
                )
                fig_pie2.update_traces(textinfo='percent+label', hovertemplate="%{label}: %{value} dons (%{percent})")
                fig_pie2.update_layout(margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
                st.plotly_chart(fig_pie2, use_container_width=True)
            else:
                st.write(translations[lang]["no_donation_data"])

        with col_heat:
            st.markdown(translations[lang]["heatmap_title"])
            heatmap_data = pd.crosstab(df_filtered['groupe_sanguin_abo__rhesus'], df_filtered['sexe'])
            fig_heat = px.imshow(
                heatmap_data, text_auto=True, color_continuous_scale='RdBu_r',
                labels=dict(x=translations[lang]["sex"], y=translations[lang]["blood_group"], color=translations[lang]["donations_label"]),
                height=350
            )
            fig_heat.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_heat, use_container_width=True)

        col_bar1, col_bar2 = st.columns(2)
        with col_bar1:
            st.markdown(translations[lang]["bar_blood_group"])
            fig_bar1 = px.bar(
                df_filtered['groupe_sanguin_abo__rhesus'].value_counts().reset_index(),
                x='groupe_sanguin_abo__rhesus', y='count',
                labels={'groupe_sanguin_abo__rhesus': translations[lang]["blood_group"], 'count': translations[lang]["donations_label"]},
                color='groupe_sanguin_abo__rhesus', color_discrete_sequence=px.colors.qualitative.Pastel1,
                height=300
            )
            fig_bar1.update_traces(hovertemplate="%{x}: %{y} dons")
            fig_bar1.update_layout(showlegend=False, bargap=0.2, margin=dict(l=10, r=10, t=20, b=20))
            st.plotly_chart(fig_bar1, use_container_width=True)

        with col_bar2:
            st.markdown(translations[lang]["bar_sex"])
            fig_bar2 = px.bar(
                df_filtered['sexe'].value_counts().reset_index(),
                x='sexe', y='count',
                labels={'sexe': translations[lang]["sex"], 'count': translations[lang]["donations_label"]},
                color='sexe', color_discrete_sequence=px.colors.qualitative.Set1,
                height=300
            )
            fig_bar2.update_traces(hovertemplate="%{x}: %{y} dons")
            fig_bar2.update_layout(showlegend=False, bargap=0.2, margin=dict(l=10, r=10, t=20, b=20))
            st.plotly_chart(fig_bar2, use_container_width=True)

        st.markdown(translations[lang]["temporal_trends"])
        period = st.selectbox(translations[lang]["display_by"], translations[lang]["display_options"], key="period_select")
        if period == translations[lang]["display_options"][0]:  # Mois/Month
            time_data = df_filtered.groupby('mois').size().reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']).reset_index(name='Dons')
            fig_time = px.area(
                time_data, x='mois', y='Dons',
                labels={'mois': translations[lang]["month_label"], 'Dons': translations[lang]["donations_label"]},
                color_discrete_sequence=['#2E7D32'],
                height=300
            )
        elif period == translations[lang]["display_options"][1]:  # Jour/Day
            time_data = df_filtered.groupby('jour').size().reset_index(name='Dons')
            fig_time = px.area(
                time_data, x='jour', y='Dons',
                labels={'jour': translations[lang]["day_label"], 'Dons': translations[lang]["donations_label"]},
                color_discrete_sequence=['#2E7D32'],
                height=300
            )
        else:  # Heure/Hour
            time_data = df_filtered.groupby('heure').size().reset_index(name='Dons')
            fig_time = px.area(
                time_data, x='heure', y='Dons',
                labels={'heure': translations[lang]["hour_label"], 'Dons': translations[lang]["donations_label"]},
                color_discrete_sequence=['#2E7D32'],
                height=300
            )
        fig_time.update_traces(hovertemplate="%{x}: %{y} dons")
        fig_time.update_layout(margin=dict(l=20, r=20, t=20, b=20), xaxis={'tickangle': -45}, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_time, use_container_width=True)

    # Section 2 : Détails + Exportation
    st.subheader(translations[lang]["details_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='stat-card'>{translations[lang]['total_donations'].format(len(df_filtered))}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['average_age'].format(int(df_filtered['age'].mean()))}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['percent_men'].format((df_filtered['sexe'] == 'M').mean())}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['percent_women'].format((df_filtered['sexe'] == 'F').mean())}</div>", unsafe_allow_html=True)
        with col2:
            most_common_group = df_filtered['groupe_sanguin_abo__rhesus'].mode()[0] if not df_filtered.empty else "N/A"
            st.markdown(f"<div class='stat-card'>{translations[lang]['most_common_group'].format(most_common_group)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['dominant_phenotype'].format(df_filtered['phenotype'].mode()[0] if not df_filtered.empty else 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['unique_groups'].format(df_filtered['groupe_sanguin_abo__rhesus'].nunique())}</div>", unsafe_allow_html=True)

        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=translations[lang]["export_button"],
            data=csv,
            file_name=translations[lang]["export_filename"],
            mime="text/csv"
        )