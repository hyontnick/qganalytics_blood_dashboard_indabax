import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
from fuzzywuzzy import process
import plotly.express as px
import plotly.graph_objects as go

# Dictionnaire de traductions pour le module Cartographie des Donneurs
translations = {
    "fr": {
        "header": "📍 Cartographie de la Répartition des Donneurs",
        "map_subheader": "🗺 Où sont les donneurs ?",
        "arrondissement_map_title": "##### Carte des Arrondissements",
        "quartier_map_title": "##### Carte des Quartiers",
        "arrondissement_map_legend": "Nombre de Donneurs",
        "arrondissement_map_tooltip": "<p class='tooltip'>Carte : couleur = nombre de donneurs, cercles = taille proportionnelle.</p>",
        "quartier_map_tooltip": "<p class='tooltip'>Carte : cercles = nombre de donneurs par quartier.</p>",
        "geo_distribution_subheader": "📊 Comment les donneurs se répartissent-ils ?",
        "treemap_title": "##### 🌳 Répartition par Arrondissement",
        "treemap_tooltip": "<p class='tooltip'>Carrés : taille et couleur = nombre de donneurs.</p>",
        "sankey_title": "##### 🌐 Flux Arrondissements-Quartiers (Top 5 par Arrondissement)",
        "sankey_tooltip": "<p class='tooltip'>Flux : montre les principaux quartiers par arrondissement.</p>",
        "details_subheader": "🔍 Détails",
        "total_donors": "📊 <b>Total Donneurs</b> : {}",
        "top_arrondissement": "🏡 <b>Top Arrondissement</b> : {} ({})",
        "top_quartier": "🏠 <b>Top Quartier</b> : {} ({})",
        "unique_arrondissements": "📍 <b>Arrondissements Uniques</b> : {}",
        "export_button": "Exporter les données (CSV)",
        "export_filename": "cartographie_donneurs.csv",
        "missing_cols_error": "❌ Colonnes manquantes : {}",
        "geojson_error": "Fichier GeoJSON non trouvé. Vérifie le chemin : 'https://drive.google.com/drive/u/0/folders/1NNuAYH2WGW7WmL9z7jdzstX1nyN7z406'",
        "no_quartier_data_warning": "Pas de données GeoJSON pour les quartiers, affichage limité."
    },
    "en": {
        "header": "📍 Mapping of Donor Distribution",
        "map_subheader": "🗺 Where are the donors?",
        "arrondissement_map_title": "##### District Map",
        "quartier_map_title": "##### Neighborhood Map",
        "arrondissement_map_legend": "Number of Donors",
        "arrondissement_map_tooltip": "<p class='tooltip'>Map: color = number of donors, circles = proportional size.</p>",
        "quartier_map_tooltip": "<p class='tooltip'>Map: circles = number of donors per neighborhood.</p>",
        "geo_distribution_subheader": "📊 How are donors distributed?",
        "treemap_title": "##### 🌳 Breakdown by District",
        "treemap_tooltip": "<p class='tooltip'>Squares: size and color = number of donors.</p>",
        "sankey_title": "##### 🌐 District-Neighborhood Flow (Top 5 per District)",
        "sankey_tooltip": "<p class='tooltip'>Flow: shows the main neighborhoods per district.</p>",
        "details_subheader": "🔍 Details",
        "total_donors": "📊 <b>Total Donors</b> : {}",
        "top_arrondissement": "🏡 <b>Top District</b> : {} ({})",
        "top_quartier": "🏠 <b>Top Neighborhood</b> : {} ({})",
        "unique_arrondissements": "📍 <b>Unique Districts</b> : {}",
        "export_button": "Export Data (CSV)",
        "export_filename": "donor_mapping.csv",
        "missing_cols_error": "❌ Missing columns: {}",
        "geojson_error": "GeoJSON file not found. Check the path: 'https://drive.google.com/drive/u/0/folders/1NNuAYH2WGW7WmL9z7jdzstX1nyN7z406'",
        "no_quartier_data_warning": "No GeoJSON data for neighborhoods, limited display."
    }
}

def get_centroid(coords):
    """Calcule le centroïde à partir de coordonnées GeoJSON (Polygon ou MultiPolygon)."""
    flat_coords = []
    def flatten(c):
        if isinstance(c, (int, float)):
            return
        elif len(c) > 0 and isinstance(c[0], (int, float)):
            flat_coords.append(c)
        else:
            for sub in c:
                flatten(sub)
    
    flatten(coords)
    if not flat_coords:
        return [4.0511, 9.7679]  # Coordonnées par défaut si aucune coordonnée valide
    lat = sum(c[1] for c in flat_coords) / len(flat_coords)
    lon = sum(c[0] for c in flat_coords) / len(flat_coords)
    return [lat, lon]

def show_cartographie(df_unused, lang="fr"):
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
        .map-container {width: 100%; height: 500px;}
        </style>
    """, unsafe_allow_html=True)

    df = df_unused.copy()

    # Vérifier les colonnes nécessaires
    required_cols = ['arrondissement_de_residence', 'quartier_de_residence']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.write(translations[lang]["missing_cols_error"].format(', '.join(missing_cols)))
        return

    # Harmoniser les noms d’arrondissements
    df['arrondissement_de_residence'] = df['arrondissement_de_residence'].replace({
        'Douala 1': 'Douala I', 'Douala 2': 'Douala II', 'Douala 3': 'Douala III',
        'Douala 4': 'Douala IV', 'Douala 5': 'Douala V', 'Douala 6': 'Douala VI'
    })

    # Charger le fichier GeoJSON une seule fois
    url_geojson = "https://raw.githubusercontent.com/hyontnick/qganalytics_blood_dashboard_indabax/main/APPLICATION/map/douala_arrondissements.geojson"
    try:
        with open(url_geojson, "r") as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error(translations[lang]["geojson_error"])
        return

    # Ligne 1 : Cartes Folium
    st.subheader(translations[lang]["map_subheader"])
    with st.container():
        col1, col2 = st.columns(2)

        # Carte 1 : Arrondissements
        with col1:
            st.markdown(translations[lang]["arrondissement_map_title"])
            arrondissement_counts = df['arrondissement_de_residence'].value_counts().reset_index()
            arrondissement_counts.columns = ['arrondissement_de_residence', 'Nombre de Donneurs']
            m_arr = folium.Map(location=[4.0511, 9.7679], zoom_start=12, tiles="CartoDB Positron")

            arr_features = [f for f in geojson_data['features'] if f['properties'].get('admin_level') == "8"]
            geojson_arr = {'type': 'FeatureCollection', 'features': arr_features}

            arr_names_geojson = [f['properties'].get('name', 'Inconnu') for f in arr_features]
            arr_name_mapping = {}
            non_specified_arr_count = 0
            douala_non_precise_count = 0
            for df_name in arrondissement_counts['arrondissement_de_residence']:
                if df_name.lower() in ['non précisé', 'unknown', 'n/a', '']:
                    arr_name_mapping[df_name] = "Non précisé"
                    non_specified_arr_count += arrondissement_counts[arrondissement_counts['arrondissement_de_residence'] == df_name]['Nombre de Donneurs'].values[0]
                elif "Douala (Non précisé)" in df_name:
                    arr_name_mapping[df_name] = "Non précisé"
                    douala_non_precise_count += arrondissement_counts[arrondissement_counts['arrondissement_de_residence'] == df_name]['Nombre de Donneurs'].values[0]
                else:
                    match = process.extractOne(df_name, arr_names_geojson)
                    if match and match[1] >= 80:
                        arr_name_mapping[df_name] = match[0]
                    else:
                        arr_name_mapping[df_name] = df_name

            df['arrondissement_de_residence_mapped'] = df['arrondissement_de_residence'].map(arr_name_mapping)
            arrondissement_counts_mapped = df['arrondissement_de_residence_mapped'].value_counts().reset_index()
            arrondissement_counts_mapped.columns = ['arrondissement_de_residence_mapped', 'Nombre de Donneurs']

            # Filtrer "Non précisé" pour le Choropleth
            arrondissement_counts_valid = arrondissement_counts_mapped[arrondissement_counts_mapped['arrondissement_de_residence_mapped'] != "Non précisé"]

            for feature in arr_features:
                name = feature['properties'].get('name', 'Inconnu')
                count = arrondissement_counts_valid[arrondissement_counts_valid['arrondissement_de_residence_mapped'] == name]['Nombre de Donneurs'].values
                feature['properties']['donneurs'] = int(count[0]) if len(count) > 0 else 0

            folium.Choropleth(
                geo_data=geojson_arr,
                name="choropleth",
                data=arrondissement_counts_valid,
                columns=['arrondissement_de_residence_mapped', 'Nombre de Donneurs'],
                key_on="feature.properties.name",
                fill_color="YlOrRd",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=translations[lang]["arrondissement_map_legend"]
            ).add_to(m_arr)

            # Ajouter les marqueurs uniquement pour les arrondissements valides
            for _, row in arrondissement_counts_valid.iterrows():
                arr_name = row['arrondissement_de_residence_mapped']
                count = row['Nombre de Donneurs']
                for feature in arr_features:
                    if feature['properties'].get('name') == arr_name:
                        coords = feature['geometry']['coordinates']
                        centroid = get_centroid(coords)
                        folium.CircleMarker(
                            location=centroid,
                            radius=count / 5,
                            popup=f"{arr_name}: {count} donneurs" if lang == "fr" else f"{arr_name}: {count} donors",
                            color="#FF5722",
                            fill=True,
                            fill_color="#FF5722",
                            fill_opacity=0.7
                        ).add_to(m_arr)

            # Ajouter un marqueur séparé pour la somme de "Non précisé" et "Douala (Non précisé)"
            total_non_precise = non_specified_arr_count + douala_non_precise_count
            if total_non_precise > 0:
                popup_text = (
                    f"Non localisés: {total_non_precise} donneurs (Non précisé: {non_specified_arr_count}, Douala (Non précisé): {douala_non_precise_count})"
                    if lang == "fr" else
                    f"Unlocated: {total_non_precise} donors (Unspecified: {non_specified_arr_count}, Douala (Unspecified): {douala_non_precise_count})"
                )
                folium.CircleMarker(
                    location=[4.0511, 9.7679],
                    radius=total_non_precise / 5,
                    popup=popup_text,
                    color="red",
                    fill=True,
                    fill_color="red",
                    fill_opacity=0.7
                ).add_to(m_arr)
                folium.Marker(
                    location=[4.0511, 9.7679],
                    tooltip=popup_text,
                    icon=folium.Icon(color="red")
                ).add_to(m_arr)

            folium_static(m_arr)
            st.markdown(translations[lang]["arrondissement_map_tooltip"], unsafe_allow_html=True)

        # Carte 2 : Quartiers
        with col2:
            st.markdown(translations[lang]["quartier_map_title"])
            quartier_counts = df['quartier_de_residence'].value_counts().reset_index()
            quartier_counts.columns = ['quartier_de_residence', 'Nombre de Donneurs']
            m_quart = folium.Map(location=[4.0511, 9.7679], zoom_start=11, tiles="CartoDB Positron")

            quart_features = [f for f in geojson_data['features'] if f['properties'].get('place') == "suburb"]
            geojson_quart = {'type': 'FeatureCollection', 'features': quart_features}

            quart_names_geojson = [f['properties'].get('name', 'Inconnu') for f in quart_features]
            name_mapping = {}
            non_specified_quart_count = 0
            for df_name in quartier_counts['quartier_de_residence']:
                if df_name.lower() in ['non précisé', 'unknown', 'n/a', '']:
                    name_mapping[df_name] = "Non précisé"
                    non_specified_quart_count += quartier_counts[quartier_counts['quartier_de_residence'] == df_name]['Nombre de Donneurs'].values[0]
                else:
                    match = process.extractOne(df_name, quart_names_geojson)
                    if match and match[1] >= 60:
                        name_mapping[df_name] = match[0]
                    else:
                        name_mapping[df_name] = df_name

            df['quartier_de_residence_mapped'] = df['quartier_de_residence'].map(name_mapping)
            quartier_counts_mapped = df['quartier_de_residence_mapped'].value_counts().reset_index()
            quartier_counts_mapped.columns = ['quartier_de_residence_mapped', 'Nombre de Donneurs']

            if geojson_quart['features']:
                for _, row in quartier_counts_mapped.iterrows():
                    quart_name = row['quartier_de_residence_mapped']
                    count = row['Nombre de Donneurs']
                    if quart_name == "Non précisé":
                        continue
                    for feature in quart_features:
                        if feature['properties'].get('name') == quart_name:
                            coords = feature['geometry']['coordinates']
                            centroid = get_centroid(coords)
                            folium.CircleMarker(
                                location=centroid,
                                radius=count / 10,
                                popup=f"{quart_name}: {count} donneurs" if lang == "fr" else f"{quart_name}: {count} donors",
                                color="#1976D2",
                                fill=True,
                                fill_color="#1976D2",
                                fill_opacity=0.7
                            ).add_to(m_quart)
            else:
                st.warning(translations[lang]["no_quartier_data_warning"])

            if non_specified_quart_count > 0:
                popup_text = (
                    f"Non précisé: {non_specified_quart_count} donneurs" if lang == "fr" else
                    f"Unspecified: {non_specified_quart_count} donors"
                )
                folium.CircleMarker(
                    location=[4.0511, 9.7679],
                    radius=non_specified_quart_count / 10,
                    popup=popup_text,
                    color="red",
                    fill=True,
                    fill_color="red",
                    fill_opacity=0.7
                ).add_to(m_quart)

            folium_static(m_quart)
            st.markdown(translations[lang]["quartier_map_tooltip"], unsafe_allow_html=True)

    # Ligne 2 : Répartition Géographique
    st.subheader(translations[lang]["geo_distribution_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(translations[lang]["treemap_title"])
            fig3 = px.treemap(
                arrondissement_counts_mapped,
                path=['arrondissement_de_residence_mapped'],
                values='Nombre de Donneurs',
                color='Nombre de Donneurs',
                color_continuous_scale='YlOrRd',
                height=300
            )
            fig3.update_traces(hovertemplate="Arrondissement: %{label}<br>Nombre: %{value}" if lang == "fr" else "District: %{label}<br>Count: %{value}")
            fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(translations[lang]["treemap_tooltip"], unsafe_allow_html=True)

        with col2:
            st.markdown(translations[lang]["sankey_title"])
            top_quartiers = df.groupby(['arrondissement_de_residence_mapped', 'quartier_de_residence_mapped']).size().reset_index(name='count')
            top_quartiers = top_quartiers.groupby('arrondissement_de_residence_mapped').apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)
            sankey_data = [{'source': row['arrondissement_de_residence_mapped'], 'target': row['quartier_de_residence_mapped'], 'value': row['count']} for _, row in top_quartiers.iterrows()]
            nodes = list(set([d['source'] for d in sankey_data] + [d['target'] for d in sankey_data]))
            node_dict = {node: i for i, node in enumerate(nodes)}
            fig4 = go.Figure(data=[go.Sankey(
                node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes, color="#4CAF50"),
                link=dict(
                    source=[node_dict[d['source']] for d in sankey_data],
                    target=[node_dict[d['target']] for d in sankey_data],
                    value=[d['value'] for d in sankey_data],
                    color="#1976D2"
                )
            )])
            fig4.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown(translations[lang]["sankey_tooltip"], unsafe_allow_html=True)

    # Ligne 3 : Détails
    st.subheader(translations[lang]["details_subheader"])
    with st.container():
        col1, col2 = st.columns(2)
        total_donors = len(df)
        top_arr = arrondissement_counts_mapped[arrondissement_counts_mapped['arrondissement_de_residence_mapped'] != "Non précisé"].iloc[0]['arrondissement_de_residence_mapped']
        top_arr_count = int(arrondissement_counts_mapped[arrondissement_counts_mapped['arrondissement_de_residence_mapped'] != "Non précisé"].iloc[0]['Nombre de Donneurs'])
        top_quartier = quartier_counts_mapped[quartier_counts_mapped['quartier_de_residence_mapped'] != "Non précisé"].iloc[0]['quartier_de_residence_mapped']
        top_quartier_count = int(quartier_counts_mapped[quartier_counts_mapped['quartier_de_residence_mapped'] != "Non précisé"].iloc[0]['Nombre de Donneurs'])
        with col1:
            st.markdown(f"<div class='stat-card'>{translations[lang]['total_donors'].format(total_donors)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['top_arrondissement'].format(top_arr, top_arr_count)}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'>{translations[lang]['top_quartier'].format(top_quartier, top_quartier_count)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'>{translations[lang]['unique_arrondissements'].format(len(arrondissement_counts_mapped[arrondissement_counts_mapped['arrondissement_de_residence_mapped'] != 'Non précisé']))}</div>", unsafe_allow_html=True)

        # Bouton d’exportation
        csv = df[['arrondissement_de_residence_mapped', 'quartier_de_residence_mapped']].to_csv(index=False).encode('utf-8')
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        st.download_button(
            label=translations[lang]["export_button"],
            data=csv,
            file_name=translations[lang]["export_filename"],
            mime="text/csv"
        )
        st.markdown("</div>", unsafe_allow_html=True)
