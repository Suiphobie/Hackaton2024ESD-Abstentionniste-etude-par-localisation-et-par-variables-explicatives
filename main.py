import pandas as pd
import streamlit as st
from streamlit_folium import st_folium, folium_static
import folium
from folium.plugins import MarkerCluster
import geopandas as gpd

st.set_page_config(layout="wide")
st.write('La France Absentionniste et ses variables explicatives')

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

