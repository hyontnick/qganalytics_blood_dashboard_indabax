import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Dictionnaire de traductions pour le module Profilage des Donneurs
translations = {
    "fr": {
        "header": "🔬 Profilage des Donneurs Idéaux",
        "clustering_subheader": "🧩 Regroupement des Donneurs",
        "n_clusters_label": "Nombre de groupes",
        "n_clusters_help": "Choisissez combien de profils distincts créer",
        "treemap_title": "##### 🌳 Répartition des Groupes",
        "treemap_tooltip": "<p class='tooltip'>Carrés : taille = nombre de donneurs par groupe.</p>",
        "heatmap_title": "##### 🔥 Caractéristiques par Groupe",
        "heatmap_x": "Caractéristique",
        "heatmap_y": "Groupe",
        "heatmap_color": "Valeur Moyenne",
        "heatmap_tooltip": "<p class='tooltip'>Couleurs : rouge = valeur élevée, bleu = faible.</p>",
        "profiles_subheader": "📈 Exploration des Profils",
        "parallel_title": "##### 📏 Comparaison des Groupes",
        "parallel_age": "Âge",
        "parallel_hemoglobin": "Hémoglobine",
        "parallel_cluster": "Groupe",
        "parallel_tooltip": "<p class='tooltip'>Lignes : chaque couleur = un groupe, montre âge et hémoglobine.</p>",
        "ideal_subheader": "🌟 Profil Idéal et Détails",
        "avg_age": "<div class='stat-card'>🎂 <b>Âge moyen</b> : {:.1f} ans</div>",
        "hemoglobin": "<div class='stat-card'>🩺 <b>Taux Hémoglobine</b> : {:.2f} g/dL</div>",
        "gender": "<div class='stat-card'>🚻 <b>Genre dominant</b> : {}</div>",
        "profession": "<div class='stat-card'>💼 <b>Profession</b> : {}</div>",
        "arrondissement": "<div class='stat-card'>🏡 <b>Arrondissement</b> : {}</div>",
        "eligibility": "<div class='stat-card'>✅ <b>Éligibilité</b> : {}</div>",
        "insight": """
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px solid #2E7D32; text-align: center; font-size: 18px; color: #2E7D32;'>
                <b>Insight</b> : Le groupe <span style='font-weight: bold; color: #388E3C;'>{}</span> est le <span style='font-style: italic;'>profil idéal</span> avec <span style='font-weight: bold;'>{}</span> donneurs, grâce à une <span style='color: #4CAF50;'>bonne santé (éligible)</span> et un <span style='color: #4CAF50;'>taux d’hémoglobine élevé</span>.
            </div>
        """,
        "export_button": "Exporter les données (CSV)",
        "export_filename": "profilage_donneurs.csv",
        "missing_cols_error": "❌ Colonnes manquantes : {}"
    },
    "en": {
        "header": "🔬 Profiling of Ideal Donors",
        "clustering_subheader": "🧩 Donor Clustering",
        "n_clusters_label": "Number of clusters",
        "n_clusters_help": "Choose how many distinct profiles to create",
        "treemap_title": "##### 🌳 Cluster Distribution",
        "treemap_tooltip": "<p class='tooltip'>Squares: size = number of donors per cluster.</p>",
        "heatmap_title": "##### 🔥 Characteristics by Cluster",
        "heatmap_x": "Characteristic",
        "heatmap_y": "Cluster",
        "heatmap_color": "Average Value",
        "heatmap_tooltip": "<p class='tooltip'>Colors: red = high value, blue = low.</p>",
        "profiles_subheader": "📈 Profile Exploration",
        "parallel_title": "##### 📏 Cluster Comparison",
        "parallel_age": "Age",
        "parallel_hemoglobin": "Hemoglobin",
        "parallel_cluster": "Cluster",
        "parallel_tooltip": "<p class='tooltip'>Lines: each color = a cluster, shows age and hemoglobin.</p>",
        "ideal_subheader": "🌟 Ideal Profile and Details",
        "avg_age": "<div class='stat-card'>🎂 <b>Average Age</b> : {:.1f} years</div>",
        "hemoglobin": "<div class='stat-card'>🩺 <b>Hemoglobin Level</b> : {:.2f} g/dL</div>",
        "gender": "<div class='stat-card'>🚻 <b>Dominant Gender</b> : {}</div>",
        "profession": "<div class='stat-card'>💼 <b>Profession</b> : {}</div>",
        "arrondissement": "<div class='stat-card'>🏡 <b>District</b> : {}</div>",
        "eligibility": "<div class='stat-card'>✅ <b>Eligibility</b> : {}</div>",
        "insight": """
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px solid #2E7D32; text-align: center; font-size: 18px; color: #2E7D32;'>
                <b>Insight</b>: Cluster <span style='font-weight: bold; color: #388E3C;'>{}</span> is the <span style='font-style: italic;'>ideal profile</span> with <span style='font-weight: bold;'>{}</span> donors, due to <span style='color: #4CAF50;'>good health (eligible)</span> and a <span style='color: #4CAF50;'>high hemoglobin level</span>.
            </div>
        """,
        "export_button": "Export Data (CSV)",
        "export_filename": "donor_profiling.csv",
        "missing_cols_error": "❌ Missing columns: {}"
    }
}

def show_profilage(df_unused, lang="fr"):
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
    required_cols = ['age', 'genre', 'profession', 'arrondissement_de_residence', 'eligibilite_au_don', 'taux_dhemoglobine']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.write(translations[lang]["missing_cols_error"].format(', '.join(missing_cols)))
        return

    # Préparation des données pour le clustering
    clustering_cols = ['age', 'taux_dhemoglobine']  # Numériques
    categorical_cols = ['genre', 'profession', 'arrondissement_de_residence', 'eligibilite_au_don']
    df_encoded = pd.get_dummies(df[categorical_cols], columns=categorical_cols)
    df_clustering = pd.concat([df[clustering_cols], df_encoded], axis=1)
    scaler = StandardScaler()
    df_clustering_scaled = scaler.fit_transform(df_clustering)

    # Clustering avec K-means
    st.subheader(translations[lang]["clustering_subheader"])
    n_clusters = st.slider(translations[lang]["n_clusters_label"], 2, 10, 4, help=translations[lang]["n_clusters_help"])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(df_clustering_scaled)

    # Ligne 1 : Visualisation des Clusters
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["treemap_title"])
            fig1 = px.treemap(
                df.groupby(['cluster']).size().reset_index(name='count'),
                path=['cluster'], values='count',
                color='cluster', color_continuous_scale=px.colors.sequential.Viridis,
                height=350
            )
            hover_label = "Groupe" if lang == "fr" else "Cluster"
            fig1.update_traces(hovertemplate=f"{hover_label}: %{{label}}<br>{translations[lang]['heatmap_color'].split()[0]}: %{{value}}")
            fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(translations[lang]["treemap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["heatmap_title"])
            cluster_summary = df.groupby('cluster').agg({
                'age': 'mean',
                'taux_dhemoglobine': 'mean',
                'genre': 'count'
            }).reset_index()
            fig2 = px.imshow(
                cluster_summary.set_index('cluster')[['age', 'taux_dhemoglobine']],
                text_auto=True, color_continuous_scale='RdBu_r',
                labels=dict(x=translations[lang]["heatmap_x"], y=translations[lang]["heatmap_y"], color=translations[lang]["heatmap_color"]),
                height=350
            )
            fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(translations[lang]["heatmap_tooltip"], unsafe_allow_html=True)

    # Ligne 2 : Analyse Multidimensionnelle
    st.subheader(translations[lang]["profiles_subheader"])
    with st.container():
        st.markdown(translations[lang]["parallel_title"])
        fig3 = px.parallel_coordinates(
            df,
            color='cluster',
            dimensions=['age', 'taux_dhemoglobine'],
            labels={
                'age': translations[lang]["parallel_age"],
                'taux_dhemoglobine': translations[lang]["parallel_hemoglobin"],
                'cluster': translations[lang]["parallel_cluster"]
            },
            color_continuous_scale=px.colors.sequential.Viridis,
            height=400
        )
        fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(translations[lang]["parallel_tooltip"], unsafe_allow_html=True)

        # Analyse des clusters
        cluster_summary = df.groupby('cluster').agg({
            'age': 'mean',
            'taux_dhemoglobine': 'mean',
            'genre': lambda x: x.mode()[0],
            'profession': lambda x: x.mode()[0],
            'arrondissement_de_residence': lambda x: x.mode()[0],
            'eligibilite_au_don': lambda x: x.mode()[0],
            'cluster': 'count'
        }).rename(columns={'cluster': translations[lang]["heatmap_color"].split()[0] + " de Donneurs"})
        st.dataframe(cluster_summary.style.format({
            'age': '{:.1f}',
            'taux_dhemoglobine': '{:.2f}',
            translations[lang]["heatmap_color"].split()[0] + ' de Donneurs': '{:d}'
        }))

    # Ligne 3 : Profil Idéal et Détails
    st.subheader(translations[lang]["ideal_subheader"])
    with st.container():
        ideal_cluster = cluster_summary[cluster_summary['eligibilite_au_don'] == 'Eligible'].sort_values(by='taux_dhemoglobine', ascending=False).index[0]
        ideal_profile = cluster_summary.loc[ideal_cluster]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["avg_age"].format(ideal_profile['age']), unsafe_allow_html=True)
            st.markdown(translations[lang]["hemoglobin"].format(ideal_profile['taux_dhemoglobine']), unsafe_allow_html=True)
            st.markdown(translations[lang]["gender"].format(ideal_profile['genre']), unsafe_allow_html=True)
        with col2:
            st.markdown(translations[lang]["profession"].format(ideal_profile['profession']), unsafe_allow_html=True)
            st.markdown(translations[lang]["arrondissement"].format(ideal_profile['arrondissement_de_residence']), unsafe_allow_html=True)
            st.markdown(translations[lang]["eligibility"].format(ideal_profile['eligibilite_au_don']), unsafe_allow_html=True)

        st.markdown(translations[lang]["insight"].format(ideal_cluster, int(ideal_profile[translations[lang]["heatmap_color"].split()[0] + ' de Donneurs'])), unsafe_allow_html=True)

        # Bouton d’exportation
        csv = df[['age', 'taux_dhemoglobine', 'genre', 'profession', 'arrondissement_de_residence', 'eligibilite_au_don', 'cluster']].to_csv(index=False).encode('utf-8')
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
        'profession': ['Étudiant', 'Employé', 'Manager', 'Retraité', 'Employé'],
        'arrondissement_de_residence': ['Arr1', 'Arr2', 'Arr1', 'Arr3', 'Arr2'],
        'eligibilite_au_don': ['Eligible', 'Non Eligible', 'Eligible', 'Eligible', 'Non Eligible'],
        'taux_dhemoglobine': [13.5, 12.0, 14.0, 13.8, 11.5]
    })
    show_profilage(df_test, lang="fr")  # Test avec français par défaut