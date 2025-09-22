
# Étude sur l'Abstention et ses Variables Explicatives

**Application interactive** pour visualiser et analyser les corrélations entre l'abstention électorale et des variables socio-économiques en France.

![Carte interactive de l'abstention et de l'IPS sur Streamlit Cloud Community](https://hackathon2024esd.streamlit.app/)
[Disclaimer : Parfois, l'app crash et ne se redémarre pas, dû à la nature des community cloud de Streamlit. Ne pas hésiter à me ping ou alors lancer la carte en local !] 


---

## 📌 Description

Cette application permet d'explorer les liens entre l'abstention électorale et des indicateurs socio-économiques, tels que l'**Indice de Position Sociale (IPS)** des établissements scolaires. Elle propose une **carte interactive multicouches** pour visualiser ces données par département, ainsi que des filtres pour affiner l'analyse.

---

## 🌍 Fonctionnalités

### 1. **Carte Interactive**
- Visualisation des **départements français** avec leur taux d'abstention.
- Superposition des **établissements scolaires** (collèges et lycées) ayant un **IPS inférieur à 100**.
- Filtres par :
  - Année de rentrée scolaire.
  - Type d'établissement (collège, lycée, etc.).
  - Élection (présidentielles, législatives, etc.).

### 2. **Données Intégrées**
- **Indice de Position Sociale (IPS)** : Données issues de l'Éducation nationale.
- **Taux d'abstention** : Données électorales agrégées.
- **Contours géographiques** : Départements français (OpenStreetMap).

### 3. **Prochaines Évolutions possibles**
- Ajout de couches supplémentaires :
  - Taux de chômage par département.
  - Répartition démographique.
  - Accès aux infrastructures culturelles.

---

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Bibliothèques requises : `pandas`, `streamlit`, `folium`, `geopandas`, `streamlit-folium`

### Étapes
1. Cloner ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/votre-depot.git
   cd votre-depot
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancer l'application :
   ```bash
   streamlit run app.py
   ```

---

## 📂 Structure des Données

Les données utilisées proviennent des sources suivantes :
- [Annuaire de l'Éducation nationale](https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/)
- [Contours des départements français (OpenStreetMap)](https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/)
- [Données des élections agrégées](https://www.data.gouv.fr/fr/datasets/donnees-des-elections-agregees/)
- [IPS des établissements scolaires](https://data.education.gouv.fr/explore/?sort=modified&q=IPS)

Les fichiers de données doivent être placés dans le même répertoire que l'application :
- `colleges.csv`
- `lycees.csv`
- `annuaire.csv`
- `finalresultelec.csv`
- `contour-des-departements.geojson`

---

## 🎯 Utilisation

1. **Filtres** :
   - Sélectionnez une année de rentrée scolaire.
   - Choisissez le type d'établissement.
   - Sélectionnez une élection.

2. **Carte** :
   - Les départements sont colorés selon leur taux d'abstention.
   - Les établissements scolaires avec un IPS < 100 sont marqués en rouge.

3. **Légende** :
   - Passez la souris sur un département pour voir son taux d'abstention et les statistiques de l'IPS.

---

## 👥 Équipe

### Conception de la Carte
- [Tahina Duroussy](https://www.linkedin.com/in/tahina-duroussy-94420b161/)
- [Christelle Emery](https://www.linkedin.com/in/christelle-emery-6a0b20245/)
- [Thibault Le Balier](https://www.linkedin.com/in/thibault-le-balier-5b9905189/)
- [Armelle Tchoua](https://www.linkedin.com/in/armelletchoua01fr/)
- [Olivier Schneider](https://www.linkedin.com/in/olivier-schneider-chef-de-projet-digital/)
- [Laura Moy](https://www.linkedin.com/in/laura-moy-2503/)
- [Nasstya Fakhreddine](https://www.linkedin.com/in/nasstya-fakhreddine-3825781a9/)

### Développement
- [Anoussone Simuong](https://www.linkedin.com/in/anousimuong/)
- [Melanie Orellana](https://www.linkedin.com/in/mélanie-orellana-031465173/)

---

## 📊 Analyse Complémentaire

L'application inclut des visuels Power BI pour approfondir l'analyse de l'abstention par géolocalisation. Pour y accéder, cliquez sur le bouton **"Accéder à la version complète"** dans l'application.

---

## 📝 Notes pour le futur
- Les données sont mises à jour devrait être mise  à jour régulièrement pour refléter les dernières élections et indicateurs socio-économiques.
- Cette application est un outil d'analyse et ne prétend pas établir de causalité entre les variables.
- Le code meriterait un bon coup de refactoring et d'optimisation. 
