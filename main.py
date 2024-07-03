import pandas as pd
import streamlit as st
from streamlit_folium import st_folium, folium_static
import folium
from folium.plugins import MarkerCluster
import geopandas as gpd

st.set_page_config(layout="wide")
st.markdown("# Étude sur l'Abstention et ses Variables Explicatives.")
st.markdown("Cette carte représente une étude croisée sur l'abstention électorale et ses possibles variables explicatives.")
introcol1, introcol2 = st.columns(2)

with introcol1:
    st.markdown("""
    
    ## Volets de l'étude
    - **Exploration des Données d'Abstention**: Analyse via Power BI des données de l'abstention par localisation (département, commune, etc.).
    - **Carte Interactive Multicouches**:
      - *Couche fonctionnelle actuelle* : **Indice de Position Sociale (IPS)** des établissements scolaires (collèges et lycées). Cette couche permet de visualiser tous les établissements ayant un IPS inférieur à 100 et de les comparer avec le taux d'abstention par département.
    """)

with introcol2:
    st.markdown(""" 
    ## Prochaines Évolutions
    - Ajout de nouvelles couches sur la carte interactive :
      - Taux de chômage par département.
      - Répartition démographique de la population.
      - Accès aux infrastructures culturelles.
    """)


@st.cache_data
def load_data():
    colleges = pd.read_csv('colleges.csv', sep=';')
    lycees = pd.read_csv('lycees.csv', sep=';')
    annuaire = pd.read_csv('annuaire.csv', sep=';')
    election_data = pd.read_csv('finalresultelec.csv', sep=',')
    return colleges, lycees, annuaire, election_data

@st.cache_data
def process_data(colleges, lycees, annuaire):
    etablissements = pd.concat([colleges, lycees], ignore_index=True)
    etablissements = etablissements.merge(annuaire, on='uai')
    return etablissements

@st.cache_data
def load_and_prepare_geojson(etablissements):
    departement = gpd.read_file("contour-des-departements.geojson")
    etablissements_gdf = gpd.GeoDataFrame(
        etablissements,
        geometry=gpd.points_from_xy(etablissements.long, etablissements.lat)
    )
    return departement, etablissements_gdf

# Use the functions
colleges, lycees, annuaire, election_data = load_data()
etablissements = process_data(colleges, lycees, annuaire)
departement, etablissements_gdf = load_and_prepare_geojson(etablissements)


# Widgets for filtering data
with st.sidebar:
    st.markdown('# La France Abstentionniste et ses variables explicatives')
    st.write('Filtre de la carte')
    annee_selectionnee = st.selectbox(
        'Choisir l\'année de la rentrée scolaire:',
        options=etablissements['rentree_scolaire'].unique()
    )
    types_etablissement = st.multiselect(
        'Choisir le type d\'établissement:',
        options=etablissements['Type_etablissement'].unique(),
        default=etablissements['Type_etablissement'].unique()
    )
    id_election_selected = st.selectbox(
        'Choisir une élection',
        options=election_data['id_election'].unique()
    )
    st.markdown("""
    Vous retrouverez tous les datasets utilisés :
    - [Annuaire de l'Éducation nationale](https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/table/?disjunctive.type_etablissement&disjunctive.code_postal&disjunctive.nom_commune&disjunctive.code_departement&disjunctive.appartenance_education_prioritaire&disjunctive.libelle_academie&disjunctive.libelle_region&disjunctive.ministere_tutelle)
    - [Contours des départements français issus d'OpenStreetMap](https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/)
    - [Données des élections agrégées](https://www.data.gouv.fr/fr/datasets/donnees-des-elections-agregees/)
    - [IPS des établissements scolaires (collèges & lycées)](https://data.education.gouv.fr/explore/?sort=modified&q=IPS)
    - [Bureaux de vote et adresses de leurs électeurs](https://www.data.gouv.fr/fr/datasets/bureaux-de-vote-et-adresses-de-leurs-electeurs/)
    - [Communes de france - Base  des codes postaux](https://www.data.gouv.fr/fr/datasets/communes-de-france-base-des-codes-postaux/)
    """)

    st.markdown("""
    # Crédits de la Carte

    Cette carte a été imaginée par :
    - [Tahina Duroussy](https://www.linkedin.com/in/tahinaduroussy/)
    - [Christelle Emery](https://www.linkedin.com/in/christelleemery/)
    - [Thibault Le Balier](https://www.linkedin.com/in/thibaultlebalier/)
    - [Armelle Tchoua](https://www.linkedin.com/in/armelletchoua/)
    - [Olivier Schneider](https://www.linkedin.com/in/olivierschneider/)
    - [Laura Moy](https://www.linkedin.com/in/lauramoy/)
    - [Nasstya Fakhreddine](https://www.linkedin.com/in/nasstyafakhreddine/)

    Et a été développée par :
    - [Anoussone Simuong](https://www.linkedin.com/in/anousimuong/)
    - [Melanie Orellana](https://www.linkedin.com/in/melanieorellana/)
    """)

# Filter establishments by year, type, and IPS
etablissements_filtrés = etablissements_gdf[
    (etablissements_gdf['ips'] < 100) &
    (etablissements_gdf['rentree_scolaire'] == annee_selectionnee) &
    (etablissements_gdf['Type_etablissement'].isin(types_etablissement))
]

# Filter election data based on selected election ID
filtered_election_data = election_data[election_data['id_election'] == id_election_selected]

# Filtrer les établissements qui se trouvent dans les limites du département
etablissements_dans_departement = gpd.sjoin(etablissements_filtrés, departement, how='inner', predicate='within')

# Group the filtered establishments by department code and calculate statistics
stats_by_dept = etablissements_dans_departement.groupby('code_du_departement')['ips'].agg(['min', 'median', 'max']).reset_index()

# Merge the statistics back with the election data to include the Abstention Rate
dept_stats = pd.merge(stats_by_dept, filtered_election_data, left_on='code_du_departement', right_on='code_du_departement')

# Adjusted merge with the corrected column from GeoDataFrame
departement_stats = departement.merge(dept_stats, left_on='code', right_on='code_du_departement', how='left')

# Create a map with Folium
map = folium.Map(location=[46.2276, 2.2137], zoom_start=6)

# Define a function for the style (optional)
def style_function(feature):
    return {
        'fillColor': '#a6cee3',
        'color': '#1f78b4',
        'weight': 2,
        'dashArray': '5, 5'
    }

choropleth = folium.Choropleth(
    geo_data=departement,
    data=filtered_election_data,
    columns=["code_du_departement", "Abstention_Rate"],
    key_on="feature.properties.code",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    name="Abstentions en %",
    highlight=True,
    smooth_factor=0,
    show=True,
).add_to(map)


# Add the updated GeoJson layer with tooltips using the correct DataFrame
folium.GeoJson(
    departement_stats,
    name='Départements',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['code', 'min', 'median', 'max', 'Abstention_Rate'],
        aliases=['Dept Code:', 'Min IPS:', 'Median IPS:', 'Max IPS:', 'Abstention Rate:'],
        localize=True,
        labels=True,
        sticky=False
    )
).add_to(map)

# Marker cluster for establishments
marker_cluster = MarkerCluster(name="Etablissements Scolaire avec moins de 100 IPS").add_to(map)
for index, row in etablissements_dans_departement.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"{row.get('nom_left')}: IPS={row['ips']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(marker_cluster)



folium.LayerControl(collapsed=False).add_to(map)
# Display the map in Streamlit
folium_static(map, width=1200, height=800)

st.markdown(""" ### Note
Les données et les couches ajoutées permettront d'approfondir l'analyse de l'abstention et de ses corrélations avec différents facteurs socio-économiques.
""")

st.write("Découvrez un tableau power BI avec des analyse sur l'abstentions par  géolocalisation dans notre étude complete")

col1, col2 = st.columns(2)

with col1:
    st.image('image1.png')
with col2:
    st.image('image2.png')

st.button('Accéder à la version complète')
