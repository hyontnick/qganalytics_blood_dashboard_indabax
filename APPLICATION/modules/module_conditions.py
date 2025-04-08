import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dictionnaire de traductions pour le module Conditions de Santé
translations = {
    "fr": {
        "header": "🏥 Conditions de Santé & Éligibilité",
        "eligibility_subheader": "📊 Qui peut donner ?",
        "treemap_title": "##### 🌳 Répartition par Éligibilité",
        "treemap_tooltip": "<p class='tooltip'>Carrés : taille = nombre de donneurs par statut.</p>",
        "bar_title": "##### 📈 Total par Éligibilité",
        "bar_x": "Éligibilité",
        "bar_y": "Nombre",
        "bar_tooltip": "<p class='tooltip'>Barres : combien dans chaque catégorie.</p>",
        "conditions_subheader": "🩺 Pourquoi certains ne peuvent pas donner ?",
        "heatmap_title": "##### 🔥 Conditions par Âge",
        "heatmap_x": "Condition",
        "heatmap_y": "Âge",
        "heatmap_color": "Nombre",
        "heatmap_tooltip": "<p class='tooltip'>Couleurs : rouge = plus de donneurs affectés.</p>",
        "sankey_title": "##### 🌐 Lien Conditions-Éligibilité",
        "sankey_tooltip": "<p class='tooltip'>Flux : montre combien chaque condition bloque les donneurs.</p>",
        "sankey_no_data": "ℹ️ Pas assez de données pour le flux.",
        "details_subheader": "🔍 Détails",
        "total_donors": "📊 <b>Total Donneurs</b> : {}",
        "eligible": "✅ <b>Éligibles</b> : {} ({:.2%})",
        "most_common_condition": "🩺 <b>Condition la plus fréquente</b> : {}",
        "affected_by_condition": "📉 <b>Affectés</b> : {}",
        "export_button": "Exporter les données (CSV)",
        "export_filename": "conditions_sante.csv",
        "missing_cols_error": "❌ Colonnes manquantes : {}"
    },
    "en": {
        "header": "🏥 Health Conditions & Eligibility",
        "eligibility_subheader": "📊 Who can donate?",
        "treemap_title": "##### 🌳 Breakdown by Eligibility",
        "treemap_tooltip": "<p class='tooltip'>Squares: size = number of donors per status.</p>",
        "bar_title": "##### 📈 Total by Eligibility",
        "bar_x": "Eligibility",
        "bar_y": "Count",
        "bar_tooltip": "<p class='tooltip'>Bars: how many in each category.</p>",
        "conditions_subheader": "🩺 Why can’t some donate?",
        "heatmap_title": "##### 🔥 Conditions by Age",
        "heatmap_x": "Condition",
        "heatmap_y": "Age",
        "heatmap_color": "Count",
        "heatmap_tooltip": "<p class='tooltip'>Colors: red = more affected donors.</p>",
        "sankey_title": "##### 🌐 Conditions-Eligibility Link",
        "sankey_tooltip": "<p class='tooltip'>Flow: shows how many each condition blocks.</p>",
        "sankey_no_data": "ℹ️ Not enough data for the flow.",
        "details_subheader": "🔍 Details",
        "total_donors": "📊 <b>Total Donors</b> : {}",
        "eligible": "✅ <b>Eligible</b> : {} ({:.2%})",
        "most_common_condition": "🩺 <b>Most Common Condition</b> : {}",
        "affected_by_condition": "📉 <b>Affected</b> : {}",
        "export_button": "Export Data (CSV)",
        "export_filename": "health_conditions.csv",
        "missing_cols_error": "❌ Missing columns: {}"
    }
}

def show_conditions(df_unused, lang="fr"):
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
    required_cols = ['age', 'eligibilite_au_don'] + [col for col in df.columns if 'raison_de_non_eligibilite_totale_' in col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.write(translations[lang]["missing_cols_error"].format(', '.join(missing_cols)))
        return

    # Identifier les conditions de santé
    health_conditions_cols = [col for col in df.columns if 'raison_de_non_eligibilite_totale_' in col]
    health_conditions = [col.replace('raison_de_non_eligibilite_totale_', '') for col in health_conditions_cols]
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 65, 100], labels=['18-25', '26-35', '36-45', '46-65', '66+'])

    # Ligne 1 : Vue d’ensemble de l’éligibilité
    st.subheader(translations[lang]["eligibility_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["treemap_title"])
            fig1 = px.treemap(
                df['eligibilite_au_don'].value_counts().reset_index(),
                path=['eligibilite_au_don'], values='count',
                color='eligibilite_au_don',
                color_discrete_map={'Eligible': '#4CAF50', 'Définitivement non-eligible': '#F44336', 'Inconnu': '#B0BEC5'},
                height=300
            )
            hover_label = "Éligibilité" if lang == "fr" else "Eligibility"
            fig1.update_traces(hovertemplate=f"{hover_label}: %{{label}}<br>{translations[lang]['bar_y']}: %{{value}}")
            fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(translations[lang]["treemap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["bar_title"])
            fig2 = px.bar(
                df['eligibilite_au_don'].value_counts().reset_index(),
                x='eligibilite_au_don', y='count',
                labels={'eligibilite_au_don': translations[lang]["bar_x"], 'count': translations[lang]["bar_y"]},
                color='eligibilite_au_don',
                color_discrete_map={'Eligible': '#4CAF50', 'Définitivement non-eligible': '#F44336', 'Inconnu': '#B0BEC5'},
                height=300
            )
            fig2.update_traces(hovertemplate=f"{translations[lang]['bar_x']}: %{{x}}<br>{translations[lang]['bar_y']}: %{{y}}")
            fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(translations[lang]["bar_tooltip"], unsafe_allow_html=True)

    # Ligne 2 : Impact des Conditions de Santé
    st.subheader(translations[lang]["conditions_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["heatmap_title"])
            condition_counts_by_age = pd.DataFrame(index=['18-25', '26-35', '36-45', '46-65', '66+'])
            for col, name in zip(health_conditions_cols, health_conditions):
                counts = df[df[col] == 'Oui'].groupby('age_group').size()
                condition_counts_by_age[name] = counts.reindex(condition_counts_by_age.index, fill_value=0)
            condition_counts_by_age = condition_counts_by_age.fillna(0)
            fig3 = px.imshow(
                condition_counts_by_age,
                text_auto=True, color_continuous_scale='RdBu_r',
                labels=dict(x=translations[lang]["heatmap_x"], y=translations[lang]["heatmap_y"], color=translations[lang]["heatmap_color"]),
                height=400
            )
            fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(translations[lang]["heatmap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["sankey_title"])
            sankey_data = []
            conditions_total = {name: df[col].value_counts().get('Oui', 0) for col, name in zip(health_conditions_cols, health_conditions)}
            ineligible_status = 'Définitivement non-eligible' if lang == "fr" else 'Permanently ineligible'
            for col, condition in zip(health_conditions_cols, conditions_total.keys()):
                count = conditions_total[condition]
                if count > 0:
                    ineligible_count = len(df[(df[col] == 'Oui') & (df['eligibilite_au_don'] == 'Définitivement non-eligible')])
                    sankey_data.append({'source': condition, 'target': ineligible_status, 'value': ineligible_count})
            if sankey_data:
                nodes = list(set([d['source'] for d in sankey_data] + [d['target'] for d in sankey_data]))
                node_dict = {node: i for i, node in enumerate(nodes)}
                fig4 = go.Figure(data=[go.Sankey(
                    node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes, color="#4CAF50"),
                    link=dict(
                        source=[node_dict[d['source']] for d in sankey_data],
                        target=[node_dict[d['target']] for d in sankey_data],
                        value=[d['value'] for d in sankey_data],
                        color="#FF5722"
                    )
                )])
                fig4.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig4, use_container_width=True)
                st.markdown(translations[lang]["sankey_tooltip"], unsafe_allow_html=True)
            else:
                st.write(translations[lang]["sankey_no_data"])

    # Ligne 3 : Détails
    st.subheader(translations[lang]["details_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        total_donors = len(df)
        eligible_count = len(df[df['eligibilite_au_don'] == 'Eligible'])
        condition_df = pd.DataFrame({
            'Condition': health_conditions,
            'Nombre de Donneurs': [df[col].value_counts().get('Oui', 0) for col in health_conditions_cols]
        }).sort_values(by='Nombre de Donneurs', ascending=False)
        with col1:
            st.markdown(f"<div class='stat-card'>{translations[lang]['total_donors'].format(total_donors)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['eligible'].format(eligible_count, eligible_count/total_donors)}</div>", unsafe_allow_html=True)
        with col2:
            most_common_condition = condition_df.iloc[0]['Condition'] if not condition_df.empty else "N/A"
            most_common_count = int(condition_df.iloc[0]['Nombre de Donneurs']) if not condition_df.empty else 0
            st.markdown(f"<div class='stat-card'>{translations[lang]['most_common_condition'].format(most_common_condition)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['affected_by_condition'].format(most_common_count)}</div>", unsafe_allow_html=True)

        # Bouton d’exportation
        export_cols = ['age', 'eligibilite_au_don'] + health_conditions_cols
        csv = df[export_cols].to_csv(index=False).encode('utf-8')
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
        'eligibilite_au_don': ['Eligible', 'Définitivement non-eligible', 'Eligible', 'Inconnu', 'Définitivement non-eligible'],
        'raison_de_non_eligibilite_totale_maladie_chronique': ['Non', 'Oui', 'Non', 'Non', 'Oui'],
        'raison_de_non_eligibilite_totale_poids_insuffisant': ['Non', 'Non', 'Non', 'Oui', 'Non']
    })
    show_conditions(df_test, lang="fr")  # Test avec français par défaut