import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, OSM
from bokeh.transform import factor_cmap
from bokeh.models.tools import WheelZoomTool
from bokeh.models import ColumnDataSource

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 

import streamlit as st
import pickle

# page configuration
st.set_page_config(
page_title="PySecuRoute v1.0",
layout="wide",
)

# sidebar navigator
st.sidebar.header('PySecuRoute v1.0')
st.sidebar.title('Sommaire')
nav = st.sidebar.radio('',['1. Présentation','2. Exploration','3. Analyse','4. Modélisation','5. Conclusion'])

"""
# PySecuRoute v1.0
### Datascientest - Bootcamp Data Analyst (Avril 2021-Juin 2021)
#### `Pascal INDICE` | `Kikala TRAORÉ` | `Christophe WARDIUS` | `Hervé HOUY`
---
"""

if nav == '1. Présentation':
	"""
	## 1. Présentation
	---
	
	### Présentation du projet
	
	Les accidents corporels sont courants et les répertorier permet de les étudier afin d’identifier
	les différents cas qui ont impliqué des blessures plus ou moins graves. Prédire la gravité
	d’un accident en fonction de ses différentes caractéristiques peut être utile pour proposer
	une solution qui a comme but de réduire la fréquence des accidents graves.

	**Données**

	Plusieurs jeux de données répertorient l’intégralité des accidents corporels de la circulation
	intervenus durant une année précise en France métropolitaine et dans les DOM-TOM. Ces
	jeux de données comprennent des informations de localisation de l’accident ainsi que des
	informations concernant les caractéristiques de l’accident et son lieu, les véhicules impliqués
	et leurs victimes.

	Nous avons choisi d'exploiter les données dont les sources sont téléchargeables au lien suivant :

	[https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019/)

	### Organisation et répartition des tâches

	Nous avons choisi ce projet pour la __volumétrie__ et la __variété__ des informations mises à disposition sur un sujet concret qui impacte notre vie au quotidien :

	les déplacements sur les routes françaises et la sécurité routière qui en découle.
	Pourtant, nous ne sommes probablement pas les personnes les plus impactées par le trafic routier.

	Venant de _Caen_, _Le Mans_, _Roanne_ et même _Saint-Denis de La Réunion_, le trafic routier des grandes agglomérations et les accidents récurrents ne sont pas notre lot de désagrément quotidien.

	Mais comme le sujet essentiel de ce projet Data est axé sur la __gravité des blessures corporels__ et la mortalité des accidentés de la route, nous verrons aussi que les spécificités géographiques peuvent donner des informations parlantes et exploitables pour un assureur ou un organisme travaillant dans le large périmètre de la sécurité routière.

	**Répartition des tâches** :

	La répartition des tâches dans l'équipe s'est faite naturellement par affinité sur les sujets et sur les compétences de chacun.

	Notre équipe est composée de profils professionnels aux parcours complètement différents.

	Ces différences de profil et de personnalité ont nourri la richesse des échanges et permis de trouver une vraie complémentarité dans la répartition des tâches :

	__Kikala__: Enseignant, Chercheur, formé au renseignement d'intéret économique, adepte du Zen de Python depuis quelques années, s'est orienté naturellement sur l'exploitation, la mise en forme des données, le data processing.

	Son expérience en Python nous a permis de débuter rapidement le projet et de transmettre ses actuces.

	__Christophe__: Chercheur en Archéologie et Géographie, a pu retrouver facilement ses repères en fouillant la documentation et les hyperparamètres d'un nombre important de modèles de Machine Learning.

	Passionné d'informatique et de programmation web, nous avons pu profiter de ses talents de développeur, de facilitateur de mise à disposition d'environnement cloud pour exécuter les traitements lourds sur un volume important de données.

	__Hervé__: Analyste fonctionnel, Consultant en Assistance en Maitrise d'Ouvrage, a pu continuer de questionner, analyser, détecter les écarts en s'orientant vers la production de graphiques, en requétant et contrôlant l'intégrité des données avant le traitement de Machine Learning.

	__Pascal__ : sa formation en Gestion et Commerce, son attrait pour les tableaux et les statistiques l'ont orienté vers la partie DataVizualiation avec de nombreux graphiques à étudier en liaison avec les résultats du Machine Learning.

	Les parties rédaction, relecture et critique ont été équitablement partagée dans l'équipe.

	### Avancement et suivi du projet

	A l'aide de _Slack_, _codeshare.io_ et des réunions _Zoom_, nous avons pu communiquer régulièrement sur l'avancé du projet et sur nos tâches respectives.

	Nos réunions hebdomadaires avec Maxime de DataScientest, et ses conseils pertinents, ont permis d'aller à l'essentiel et d'éviter de nous égarer facilement vu le vaste sujet étudié, dans le temps restreint rythmé par les certifications hebdomadaires et obligatoires de cette riche formation.

	### Pourquoi PySecuRoute ?
	
	* Pour __Py__thon, langage ubiquitaire en tant que Data Analyst, et plus généralement en Data Science.
	* Notre sensibilité commune sur la __Sécu__rité __Rout__ière
	"""

elif nav == '2. Exploration':
	"""
		## 2. Exploration des données
		---
	"""
		
	if st.checkbox("Description des données"):
		"""
		### Description des données
		---

		Pour chaque accident corporel (soit un accident survenu sur une voie ouverte à la circulation publique,
		impliquant au moins un véhicule et ayant fait au moins une victime ayant nécessité des soins), des
		saisies d’information décrivant l’accident sont effectuées par l’unité des forces de l’ordre (police,
		gendarmerie, etc.) qui est intervenue sur le lieu de l’accident. Ces saisies sont rassemblées dans
		une fiche intitulée bulletin d’analyse des accidents corporels. L’ensemble de ces fiches constitue le
		fichier national des accidents corporels de la circulation dit « Fichier BAAC » administré par
		l’Observatoire national interministériel de la sécurité routière "ONISR".

		Les bases de données, extraites du fichier BAAC, répertorient l'intégralité des accidents corporels de
		la circulation, intervenus durant une année précise en France métropolitaine, dans les départements
		d’Outre-mer (Guadeloupe, Guyane, Martinique, La Réunion et Mayotte depuis 2012) et dans les autres
		territoires d’outre-mer (Saint-Pierre-et-Miquelon, Saint-Barthélemy, Saint-Martin, Wallis-et-Futuna,
		Polynésie française et Nouvelle-Calédonie ; disponible qu’à partir de 2019 dans l’open data) avec une
		description simplifiée. Cela comprend des informations de localisation de l’accident, telles que
		renseignées ainsi que des informations concernant les caractéristiques de l’accident et son lieu, les
		véhicules impliqués et leurs victimes.

		Par rapport aux bases de données agrégées 2005-2010 et 2006-2011 actuellement disponibles sur le
		site [www.data.gouv.fr](https://www.data.gouv.fr), les bases de données de 2005 à 2019 sont désormais annuelles et composées
		de 4 fichiers (Caractéristiques – Lieux – Véhicules – Usagers) au format csv. 
		
		"""
		
	if st.checkbox("Exploitation des données"):
		"""
		### Exploitation des données
		---
	
		Ayant relevé une incompatibilité entre les datasets antérieurs et postérieurs à 2018, nous avons choisi de fusionner dans un DataFrame l'ensemble des bases de données de 2005 à 2017

		"""
		
	if st.checkbox("Identification des données"):
		"""
		### Identification des données
		---
		
		Afin de faciliter le téléchargement des données, l'ensemble des informations sur les jeux de données est agrégé dans un fichier master JSON :

		* data.json
		"""
		# chargement du 'df_master' des jeu de données
		data = json.load(open('data.json','r'))
		df_master = pd.json_normalize(data['distribution'])
		st.write(df_master.head())
		
	if st.checkbox("Restriction de l'exploration sur les des données sur la période 2005-2017"):
		"""
		### Restriction de l'exploration sur les des données sur la période 2005-2017
		
		
		
		La note de Description des bases de données annuelles des accidents corporels de la circulation routière
		Années de 2005 à 2019 (téléchargeable ici) émet un avertissement :

		Les données sur la qualification de blessé hospitalisé depuis l’année 2018 ne peuvent être comparées aux années précédentes suite à des modifications de process de saisie des forces de l’ordre. L’indicateur « blessé hospitalisé » n’est plus labellisé par l’autorité de la statistique publique depuis 2019.

		Nous avons donc choisi de restreindre une partie de l'exploration des données sur la période 2005-2017, ce qui consitue :

		* 13` années
			
		`4` datasets au format CSV par année :
		* Caractéristiques,
		* Lieux,
		* Véhicules,
		* Usagers.
			
		Soit `52` fichiers CSV à consolider dans un `DataFrame`.

		On remarque qu'une erreur s'est produite avec le fichier `caracteristiques_2009.csv` que l'on traitera donc séparément.
		(Il s'agit en fait d'un fichier _TSV_)
		
		"""
		
	if st.checkbox("Modèle de données"):
		"""
		### Modèle de données
		---
		
		### Descriptifs des fichiers à disposition:
		
		#### Caractéristiques :

		Circonstances générales de l’accident notamment la __date__, les __conditions atmostphériques__ et la __situation géographique__.

		Identifiant(s) du fichier :

		`Num_Acc`: Numéro d'identifiant de l’accident
		
		* LIEUX

		Description du lieu principal de l’accident même si celui-ci s’est déroulé à une intersection

		Identifiant(s) du fichier :

		`Num_Acc`: Numéro d'identifiant de l’accident
		
		* VEHICULES

		Véhicules impliqués dans l'accident avec les caractériques du véhicules

		Identifiant(s) du fichier :

		`Num_Acc` : Numéro d'identifiant de l’accident
		`Num_Veh` : Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés)
		
		* USAGERS

		Usagers impliqués dans l'accident avec caractéristiques propres à l'usager et les conséquences de l'accident (gravité)

		Identifiant(s) du fichier :

		`Num_Acc` : Numéro de l’accident
		`Num_Veh` : Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés)
		`place` : Permet de situer la place occupée dans le véhicule par l'usager au moment de l'accident

		Chaque ligne correspond à un usager, en terme de données il peut y avoir des "faux" doublons notamment pour les usagers de transport en commun.
		"""
		
	if st.checkbox("Constitution du jeu de données à explorer"):
		
		"""
		### Constitution du jeu de données à explorer
		
		_Principe_:
		Notre étude portant sur la gravité des blessures corporels des usagers, nous devons avoir l'ensembles des données concernant les usagers des accidents sur notre période de 2005 à 2017.

		Pour constituer le jeu de données à explorer, nous prendrons donc le fichier `Usagers` comme fichier "Maitre" et nous ferons toutes les jointures nécessaires avec ce fichier.

		_Pour chaque année de données récupérées_:
		* Création de _4 dataframes_ correspondants aux chargements des _4 fichiers csv_ de l'année.
		* Création d'un _dataframe global_ de l'année résultat des jointures des 4 dataframes de l'année
		* _Concaténation_ de l'ensemble des dataframes globaux pour créer un dataframe final de notre période 2005 à 2017
		
		_Ajout des colonnes 'département' et 'région'_

		Nous avons fait le choix de pouvoir localiser les accidents. Pour cela, nous utiliserons 2 dictionnaires Python téléchargeables [ici](https://gist.github.com/mlorant/b4d7bb6f96c47776c8082cf7af44ad95)

		Ces deux dictionnaires listent les régions et départements français. Dans notre dataframe, le département est renseigné dans la colonne __'dep'__.

		Création des colonnes :
		* 'departement'
		* 'region'
		"""	
	
	if st.checkbox('Data cleaning'):
		"""

		Nous avons effectué un _data cleaning_ des données avec notamment :
		* une gestion des NaN
		* remplacement des NaN par le mode le cas échéant.
		"""
		
		"""
		```
		nan_mode_cols = ['place','secu','lartpc','larrout','env1','infra','situ','vosp','nbv','plan','prof',
						 'surf','circ','actp','locp','etatp','an_nais','obsm','obs','trajet',
						 'manv','choc','senc','atm']

		for col in nan_mode_cols:
			df[col] = df[col].fillna(df[col].mode()[0])

		```
		"""
		"""
		* une conversion de la majorité des colonnes grâce à la fonction pd.to_numeric(...

		Exemple de fonction créée pour le projet et permettant d'afficher la répartition des NaN's :

		"""
		"""
		```
		def show_nan_rep(dataframe):
			missing_count = dataframe.isnull().sum()  the count of missing values
			value_count = dataframe.isnull().count()  the count of all values 
			missing_percentage = round(missing_count / value_count * 100,2)  the percentage of missing values
			missing_df = pd.DataFrame({'nbre': missing_count, '%': missing_percentage})  create a dataframe
			print("Champs vides :")
			print(missing_df.sort_values(by='nbre', ascending=False))
			plt.figure(figsize=(8,8))
			missing_df['%'].sort_values(ascending=False)[:15].plot.pie(autopct="%.1f%%")
			plt.title('Répartition des données manquantes par colonne');
		```
		"""
		"""
		Exemple de fonction créée pour sonder les modalités de chaque colonne :
		"""
		"""
		```
		for i in df.columns[1:]:
			x = df[i].sort_values().unique()
			print('Pour la colonne ',i,', les valeurs sont :',x)
		```
		"""
		"""

		On fait le choix de supprimer les colonnes `v2`, `v1`, `gps`, `pr1`, `pr`, `adr` et `voie` qui de part le caractère erratique de leurs modalités n'apporteront pas de valeur ajoutée à notre étude.

		On conserve les colonnes lat et long pour l'instant.
		"""

	if st.checkbox('Conclusions et export'):
		"""	
		Nous ne proposons pas le code associé dans le présent rapport, vu que le CSV est disponible sur un site internet personnel, à cause de sa grande taille (444Mo) ne pouvant pas être hébergé sur GitHub et la durée potentielle de réalisation.

		[Le lien du CSV global 2005-2017](https://christophe-wardius.fr/projets/pysecuroute/dataset_v3/df_global_v3.csv)

		`df.to_csv('...`
		
		Nous avons fait le choix d'héberger le fichier global 2005-2017 sur le site personnel de Christophe W., car le CSV global a une taille de `444Mo` et GitHub ne permet pas de stocker un tel fichier. 

		En outre, nous avons décidé de proposer un CSV par année pour les besoins de la visualisation de données. Ceux-ci sont disponibles directement sur le GitHub du projet au sein du dossier 'dataset'.
		"""

elif nav == '3. Analyse':
	"""
		## 3. Analyse et Visualisation des données
	"""
	
	"""
	###### Afin d'optimiser le temps de chargement et l'affichage, nous avons fait le choix de __filtrer__ les données de visualisation __par année__.
	---	
	"""
	"""
	##### Sélectionnez une année d'étude (de 2005 à 2017)
	"""
	annee = st.selectbox("", np.arange(2005,2018,1))

	@st.cache(suppress_st_warning=True,allow_output_mutation=True,max_entries=None,ttl=60*3)
	def preprocess():
		
		# chargement des df par année
		df = {}
		
		#chargement des données depuis le cloud
		df[annee] = pd.read_csv('https://www.jazzreal.org/static/df_'+str(annee)+'_v3.csv')
		
		# sampling du df à 10%
		df[annee] = df[annee].sample(frac=0.10, replace=False, random_state=1234)
		
		# gestion des dates
		df[annee].an=df[annee].an+2000
		df[annee]['date']=pd.to_datetime((df[annee].an*10000+df[annee].mois*100+df[annee].jour).apply(str),format='%Y%m%d', exact=False, errors='coerce')
		df[annee]['day']= df[annee].date.dt.weekday
		
		# conversion de la longitude en 'float64'
		df[annee]['long'] = pd.to_numeric(df[annee]['long'], errors='coerce')
		
		# conversion du CRS en mercator
		k = 6378137
		df[annee]["x"] = (df[annee]['long'] / 100000)* (k * np.pi / 180.0)
		df[annee]["y"] = np.log(np.tan((90 + df[annee]['lat']/100000) * np.pi / 360.0)) * k
		
		# data cleaning
		df[annee].dropna()
		
		print('(done) loading csv file for '+str(annee))

		return df[annee]
	
	# chargement des dataframes
	df = preprocess()
	
	df['date']= pd.to_datetime((df.an*10000+df.mois*100+df.jour).apply(str),format='%Y%m%d', exact=False, errors='coerce')
	df['day']= df.date.dt.day_name()
	df['day']= pd.Categorical(df['day'],['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],ordered=True)
	df['age']= df.an-df.an_nais
	
	df_non_indemnes = df[df['grav']!=1]
	df_tues = df[df['grav']==2]
	
	print('(done) : preprocessing completed.')
	
	# ajout année sur le sidebar	 
	st.sidebar.markdown("### Analyses sur l'année : "+str(annee))
	
	# recherche par mot-clés
	"""
	##### Recherche de visualisations par mot-clés (en minuscule, séparé par des espaces)
	"""
	search = st.text_input('')
	"""
	###### exemples de mot-clés : `carte` `région` `département` `gravité` `mois` `jour` `heure` `véhicule` `route` `collision` `sexe`
	"""

	# graphiques

	
	## tableau des régions avec le plus d'accidentés pour comparé avec le plus de blessés
	def Tableau_Des_Régions_Avec_Le_Plus_D_accidentés_Pour_Comparé_Avec_Le_Plus_De_Blessés():
		x1 = pd.crosstab(df.grav, df.region, rownames=['gravite'], colnames=['region'])
		st.write(x1)


	## tableau des régions avec le plus de tués pour comparé avec le plus de blessés
	def Tableau_Des_Régions_Avec_Le_Plus_De_Tués_Pour_Comparé_Avec_Le_Plus_De_Blessés():
		x2 = pd.crosstab(df_tues.grav, df_tues.region, rownames=['nombre de Tués'], colnames=['region'])
		st.write(x2)

	## tableau des départements avec le plus de tués
	def Tableau_Des_Départements_Avec_Le_Plus_De_Tués():
		x3 = pd.crosstab(df_tues.grav, df_tues.departement, rownames=['nombre de Tués'], colnames=['departement'])
		st.write(x3)

	## tableau des régions avec le plus de blessés pour comparaison
	def Tableau_Des_Régions_Avec_Le_Plus_De_Blessés_Pour_Comparaison():
		x4 = pd.crosstab(df.grav, df.region, rownames=['gravite'], colnames=['region'])
		st.write(x4)

	## distribution des accidentés par région/département
	def Distribution_Des_Accidentés_Par_Régiondépartement():
		x5 = pd.pivot_table(df, index=['region', 'departement'], values='grav', aggfunc='count')
		st.write(x5)

	## tableau des nombre de tués par région et département
	def Tableau_Des_Nombre_De_Tués_Par_Région_Et_Département():
		pd.set_option("max_rows", None)
		x6 = pd.pivot_table(df_tues, index=['region', 'departement'], values='grav', aggfunc='count')
		st.write(x6)


	## palmarès des régions avec le plus et le moins d'accidentés
	def Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_Daccidentés():
		max_col = df['region'].value_counts().head(5)
		min_col = df['region'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col.index, y=max_col, order=max_col.index, ax=ax1)
		ax1.set_ylabel('nombre')
		ax1.title.set_text("5 régions avec le plus d'accidents corporels")
		labels = ax1.get_xticklabels()
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col.index, y=min_col, order=min_col.index, ax=ax2)
		ax2.title.set_text("5 regions avec le moins d'accidents corporels")
		ax2.set_ylabel('nombre')
		plt.xticks(rotation=45);
		st.pyplot(fig)

	## palmarès des régions avec le plus et le moins de tués
	def Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_De_Tués():
		max_col = df_tues['region'].value_counts().head(5)
		min_col = df_tues['region'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col.index, y=max_col, order=max_col.index, ax=ax1)
		ax1.title.set_text("5 régions avec le plus d'accidents mortels")
		labels = ax1.get_xticklabels()
		ax1.set_ylabel('nombre')
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col.index, y=min_col, order=min_col.index, ax=ax2)
		ax2.title.set_text("5 régions avec le moins d'accidents mortels")
		ax2.set_ylabel('nombre')
		plt.xticks(rotation=45);
		st.pyplot(fig)
	
	## palmarès des départements avec le plus d'accidents corporels
	def Palmarès_Des_Départements_Avec_Le_Plus_Daccidents_Corporels():
		max_col = df['departement'].value_counts().head(5)
		min_col = df['departement'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col.index, y=max_col, order=max_col.index, ax=ax1)
		ax1.title.set_text("5 départements avec le plus d'accidents corporels")
		labels = ax1.get_xticklabels()
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col.index, y=min_col, order=min_col.index, ax=ax2)
		ax2.title.set_text("5 départements avec le moins d'accidents corporels")
		plt.xticks(rotation=45);
		st.pyplot(fig)

	## palmarès des Départements avec le plus et le moins de Tués
	def Palmarès_Des_Départements_Avec_Le_Plus_Et_Le_Moins_De_Tués():
		max_col_tues = df_tues['departement'].value_counts().head(5)
		min_col_tues = df_tues['departement'].value_counts().tail(5)
		fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16,6), sharey=True)
		sns.barplot(x=max_col_tues.index, y=max_col_tues, order=max_col_tues.index, ax=ax1)
		ax1.title.set_text("5 départements avec le plus de Tués")
		labels = ax1.get_xticklabels()
		plt.setp(labels, rotation=45, horizontalalignment='right')
		sns.barplot(x=min_col_tues.index, y=min_col_tues, order=min_col_tues.index, ax=ax2)
		ax2.title.set_text("5 départements avec le moins de Tués")
		plt.xticks(rotation=45);
		st.pyplot(fig)

	## distribution des accidenté(e)s par gravité de blessure
	def Distribution_Des_Accidentées_Par_Gravité_De_Blessure():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav",data=df)
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures");
		st.pyplot(fig)
	
	##BOKEH##
	## carte intéractive des accidentés par gravité
	def Carte_Intéractive_Des_Accidentés_Par_Gravité():
		df_geo = df[['lat','long','grav','an']]
		df_geo['lat'] = pd.to_numeric(df_geo['lat'], errors='coerce')
		df_geo['long'] = pd.to_numeric(df_geo['long'], errors='coerce')
		df_geo['lat'] = df_geo['lat'] / 100000
		df_geo['long'] = df_geo['long'] / 100000
		k = 6378137
		df_geo["x"] = (df_geo['long'])* (k * np.pi / 180.0)
		df_geo["y"] = np.log(np.tan((90 + df_geo['lat']) * np.pi / 360.0)) * k
		tile_provider = get_provider(OSM)
		tools = "pan,wheel_zoom,reset"
		p = figure(x_range=(-1000000, 2000000), y_range=(5000000, 7000000),
				   x_axis_type="mercator", y_axis_type="mercator",
				   tools=tools,
				   plot_width=800,
				   plot_height=600,
				   title='Accidents de la route par gravité ('+str(annee)+')'
				   )
		p.add_tile(tile_provider)
		geo_source_1 = ColumnDataSource(data=df_geo[df_geo['grav'] == 1])
		geo_source_2 = ColumnDataSource(data=df_geo[df_geo['grav'] == 2])
		geo_source_3 = ColumnDataSource(data=df_geo[df_geo['grav'] == 3])
		geo_source_4 = ColumnDataSource(data=df_geo[df_geo['grav'] == 4])
		p1 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_1, color='green', legend_label='Indemne')
		p2 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_4, color='yellow', legend_label='Blessé léger')
		p3 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_3, color='orange', legend_label='Blessé hospitalisé')
		p4 = p.circle(x='x', y='y', size=5, alpha=0.5, source=geo_source_2, color='red', legend_label='Tué')
		p.xgrid.grid_line_color = None
		p.ygrid.grid_line_color = None
		p.xaxis.major_label_text_color = None
		p.yaxis.major_label_text_color = None
		p.xaxis.major_tick_line_color = None  
		p.xaxis.minor_tick_line_color = None  
		p.yaxis.major_tick_line_color = None  
		p.yaxis.minor_tick_line_color = None  
		p.yaxis.axis_line_color = None
		p.xaxis.axis_line_color = None
		p.legend.click_policy = "hide"
		st.bokeh_chart(p)
	
	## distribution des accidentés par mois
	def Distribution_Des_Accidentés_Par_Mois():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="mois", data=df);
		plt.legend(labels=['Janvier',
						   'Février',
						   'Mars',
						   'Avril',
						   'Mai',
						   'Juin',
						   'Juillet',
						   'Août',
						   'Septembre',
						   'Octobre',
						   'Novembre',
						   'Décembre'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des mois de l'année");
		st.pyplot(fig)
	
	## distribution des accidentés par jour de la semaine
	def Distribution_Des_Accidentés_Par_Jour_De_La_Semaine():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="day", data=df);
		plt.legend(labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des jours de la semaine");
		st.pyplot(fig)
	
	## distribution par heure / minutes
	def Distribution_Par_Heure_Minutes():
		fig, ax = plt.subplots(figsize=(11,5))
		sns.kdeplot(x='hrmn',hue='grav',multiple="stack",data=df)
		plt.legend(labels=['Blessé léger','Blessé hospitalisé','Tué','Indemne'])
		plt.xticks([0,500,1000,1500,2000],['0:00','5:00','10:00','15:00','20:00'])
		plt.xlim(right=2500)
		plt.xlabel('Heures')
		plt.ylabel('Densité')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de l'heure");
		st.pyplot(fig)
		
	## graphique par catégorie de véhicule
	def Graphique_Par_Catégorie_De_Véhicule():
		fig, ax = plt.subplots(figsize=(15,15))
		sns.countplot(x="grav", hue="catv", data=df);
		plt.legend(labels=['01 - Bicyclette',
						   '02 - Cyclomoteur <50cm3',
						   '03 - Voiturette (Quadricycle à moteur carrossé)',
						   '04 - scooter immatriculé',
						   '05 - motocyclette',
						   '06 - side-car',
						   '07 - VL seul',
						   '08 - VL + caravane',
						   '09 - VL + remorque',
						   '10 - VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque',
						   '11 - VU (10) + caravane',
						   '12 - VU (10) + remorque',
						   '13 - PL seul 3,5T <PTCA <= 7,5T',
						   '14 - PL seul > 7,5T',
						   '15 - PL > 3,5T + remorque',
						   '16 - Tracteur routier seul',
						   '17 - Tracteur routier + semi-remorque',
						   '18 - transport en commun',
						   '19 - tramway',
						   '20 - Engin spécial',
						   '21 - Tracteur agricole',
						   '30 - Scooter < 50 cm3',
						   '31 - Motocyclette > 50 cm3 et <= 125 cm3',
						   '32 - Scooter > 50 cm3 et <= 125 cm3',
						   '33 - Motocyclette > 125 cm3',
						   '34 - Scooter > 125 cm3',
						   '35 - Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)',
						   '36 - Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)',
						   '37 - Autobus',
						   '38 - Autocar',
						   '39 - Train',
						   '40 - Tramway',
						   '99 - Autre véhicule'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de véhicule');
		st.pyplot(fig)
	
	## graphique par catégorie de route
	def Graphique_Par_Catégorie_De_Route():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="catr", data=df);
		plt.legend(labels=['1 - Autoroute',
						   '2 - Route nationale',
						   '3 - Route Départementale',
						   '4 - Voie Communale',
						   '5 - Hors réseau public',
						   '6 - Parc de stationnement ouvert à la circulation publique',
						   '9 - autre'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de route');
		st.pyplot(fig)
	
	## graphique par type de collision
	def Graphique_Par_Type_De_Collision():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="col", data=df);
		plt.legend(labels=['Deux véhicules - frontale',
						   'Deux véhicules - par l’arrière',
						   'Deux véhicules - par le coté',
						   'Trois véhicules et plus – en chaîne',
						   'Trois véhicules et plus - collisions multiples',
						   'Autre collision',
						   'Sans collision'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction du type de collision");
		st.pyplot(fig)

	## proportion masculin / féminin (accidentés) (sexe)
	def Proportion_Masculin_Féminin_accidentés():
		fig, ax = plt.subplots(figsize=(5,5))
		sns.countplot(x="sexe",data=df)
		plt.xticks([0,1],['M','F'])
		plt.xlabel("Sexe de l'accidenté(e)")
		plt.ylabel("nombre Usagers")
		plt.title('Distribution des accidentés par sexe');
		st.pyplot(fig)

	## proportion masculin/féminin ( tués ) (sexe)
	def Proportion_Masculinféminin_Tués_():
		fig, ax = plt.subplots(figsize=(5,5))
		sns.countplot(x="sexe",data=df_tues)
		plt.xticks([0,1],['M','F'])
		plt.xlabel("Sexe de l'accidenté(e)")
		plt.ylabel("nombre de Tués")
		plt.title("Distribution des Tué(e)s par sexe");
		st.pyplot(fig)

	## proportion masculin/féminin ( tués par âge )
	def Proportion_Masculinféminin_Tués_Par_Age_():
		g = sns.FacetGrid(df_tues, col='sexe')
		g.map(plt.hist, 'age');
		st.pyplot(g)

	## graphique par sexe
	def Graphique_Par_Sexe():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="sexe", data=df);
		plt.legend(labels=['M','F'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du blessé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du sexe');
		st.pyplot(fig)
	
	## distribution des accidenté(e)s par gravité des blessures en fonction de l'âge
	def Distribution_Des_Accidentées_Par_Gravité_Des_Blessures_En_Fonction_De_Lâge():
		fig, ax = plt.subplots(figsize=(11,5))
		sns.kdeplot(x='age',hue='grav',multiple="stack",data=df)
		plt.legend(labels=['Blessé léger','Blessé hospitalisé','Tué','Indemne'])
		plt.xlim(right=110)
		plt.xlabel('Age')
		plt.ylabel('Densité')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de l'âge");
		st.pyplot(fig)
	
	## graphique par catégorie d'usager
	def Graphique_Par_Catégorie_Dusager():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="catu", data=df);
		plt.legend(labels=['1 - Conducteur',
						   '2 - Passager',
						   '3 - Piéton',
						   '4 - Pieton Roller/Trotinette'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des catégories d'usagers");
		st.pyplot(fig)
	
	## graphique par type de trajet
	def Graphique_Par_Type_De_Trajet():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="trajet", data=df);
		plt.legend(labels=['Non renseigné',
						   'Domicile – travail',
						   'Domicile – école',
						   'Courses – achats',
						   'Utilisation professionnelle',
						   'Promenade – loisirs',
						   'Autre'])
		plt.xticks([0,1,2,3],['Indemne',
							  'Tué',
							  'Blessé hospitalisé',
							  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du type de trajet');	
		st.pyplot(fig)
	
	# FIN VISUALISATIONS #
	######################
	
	graphs = {
	"tableau des régions avec le plus d'accidentés pour comparé avec le plus de blessés":Tableau_Des_Régions_Avec_Le_Plus_D_accidentés_Pour_Comparé_Avec_Le_Plus_De_Blessés,
	"tableau des régions avec le plus de tués pour comparé avec le plus de blessés":Tableau_Des_Régions_Avec_Le_Plus_De_Tués_Pour_Comparé_Avec_Le_Plus_De_Blessés,
	"tableau des départements avec le plus de tués":Tableau_Des_Départements_Avec_Le_Plus_De_Tués,
	"tableau des régions avec le plus de blessés pour comparaison":Tableau_Des_Régions_Avec_Le_Plus_De_Blessés_Pour_Comparaison,
	"distribution des accidentés par région/département":Distribution_Des_Accidentés_Par_Régiondépartement,
	"tableau des nombre de tués par région et département":Tableau_Des_Nombre_De_Tués_Par_Région_Et_Département,
	"palmarès des régions avec le plus et le moins d'accidentés":Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_Daccidentés,
	"palmarès des régions avec le plus et le moins de tués":Palmarès_Des_Régions_Avec_Le_Plus_Et_Le_Moins_De_Tués,
	"palmarès des départements avec le plus d'accidents corporels":Palmarès_Des_Départements_Avec_Le_Plus_Daccidents_Corporels,
	"palmarès des Départements avec le plus et le moins de Tués":Palmarès_Des_Départements_Avec_Le_Plus_Et_Le_Moins_De_Tués,
	"distribution des accidenté(e)s par gravité de blessure":Distribution_Des_Accidentées_Par_Gravité_De_Blessure,
	"carte intéractive des accidentés par gravité":Carte_Intéractive_Des_Accidentés_Par_Gravité,
	"distribution des accidentés par mois":Distribution_Des_Accidentés_Par_Mois,
	"distribution des accidentés par jour de la semaine":Distribution_Des_Accidentés_Par_Jour_De_La_Semaine,
	"distribution par heure / minutes":Distribution_Par_Heure_Minutes,
	"graphique par catégorie de véhicule":Graphique_Par_Catégorie_De_Véhicule,
	"graphique par catégorie de route":Graphique_Par_Catégorie_De_Route,
	"graphique par type de collision":Graphique_Par_Type_De_Collision,
	"proportion masculin / féminin (accidentés) ( sexe )":Proportion_Masculin_Féminin_accidentés,
	"proportion masculin/féminin ( tués ) ( sexe )":Proportion_Masculinféminin_Tués_,
	"proportion masculin/féminin ( tués par âge ) ( sexe )":Proportion_Masculinféminin_Tués_Par_Age_,
	"graphique par sexe":Graphique_Par_Sexe,
	"distribution des accidenté(e)s par gravité des blessures en fonction de l'âge":Distribution_Des_Accidentées_Par_Gravité_Des_Blessures_En_Fonction_De_Lâge,
	"graphique par catégorie d'usager":Graphique_Par_Catégorie_Dusager,
	"graphique par type de trajet":Graphique_Par_Type_De_Trajet,
	}

	
	# sélection et affichage des graphiques par mot-clés
	for key,value in graphs.items():
		for word in search.split():
			if word in key:
				if st.checkbox(key):
					value()

elif nav == '4. Modélisation':
	
	if st.checkbox('Présentation du modèle'):
		"""
		### Présentation du modèle
		En complément des analyses réalisées grâce aux dataviz’, nous avons voulu réaliser du Machine Learning afin de voir si on pouvait prédire la gravité d’un accident corporel en France.


		### Données
		Les données utilisées sont celles fournies par le Ministère de l’Intérieur, moins 19 variables que nous avons jugées inutiles ou redondantes. Nous avons enlevé toutes les variables de localisation géographiques (hormis le code INSEE de la commune), ainsi que les informations temporelles et les numéros d’accident et de véhicule. En voici la liste exhaustive : `dep`, `v2`, `v1`, `gps`, `pr1`, `pr`, `adr`, `voie`, `long`, `lat`, `Num_Acc`, `num_veh`, `an`, `mois`, `jour`, `hrmn`, `departement`, `region`, `an_nais`.

		L’étendue des données porte toujours sur __les années 2005 à 2017 incluses__.

		La gestion des _NaN_, pour les variables quantitatives, suit le choix de l’ensemble du projet, soit l’utilisation du mode. Concernant les variables quantitatives, les observations sont supprimées.


		### Tests et améliorations du ML
		Après plusieurs essais, le choix a été fait de ne pas réaliser les modélisations sur tout le dataset de ML, mais après une diminution de ce dataset par regroupement sur le numéro d'accident (`Num_Acc`), en ne conservant que la gravité (`grav`) la plus élevée lors de chaque accident.

		Ce choix nous a semblé judicieux pour plusieurs raisons :

		* donner de meilleures prédictions,
		* réduire le temps de calcul,
		* correspondre le mieux à une logique d’assureur, qui pourrait être notre client ici.

		Par contre, il y aura une conséquence : __la gravité la moins élevée (modalité '1' = 'indemne') n’est que très peu observée__. De fait, elle sera absente du jeu de test et donc des résultats de la modélisation.


		### Données utilisées
		Le jeu de données utilisé pour les prédictions de Machine Learning comprend donc _1 100 476 observations_ et _33 variables explicatives potentielles_.

		### Choix des modèles
		Dans un but d’interprétabilité des résultats et de test de robustesse, nous avons opté pour l’__arbre de décision__ (DecisionTree).


		### Résultats avec DecisionTree

		#### Hyperparamètres utilisés
		Après différents tests de recherche des meilleurs hyperparamètres via la fonction GridSearchCV, il s’est avéré que les meilleurs étaient : `{'criterion': 'gini', 'max_depth': 14}`.


		#### Taux de prédiction
		Le taux de réussite de prédiction du modèle sur le jeu d'entraînement s'élève à __73,03%__.

		Le taux de réussite de prédiction du modèle sur le jeu de test, c’est-à-dire en conditions réelles d’utilisation, s'élève à __70,52%__.


		#### Rapport d’évaluation
		Le rapport d’évaluation du modèle sur l’échantillon de test est le suivant :
		"""
		st.image('PySecuRoute-DecisionTree-01-Rapport-evaluation.png')
		"""
		La moyenne montre des scores satisfaisants, avec un recall légèrement supérieur au score f1 et à la précision, respectivement 71 et 68%.


		#### Matrice de confusion (heatmap et tableau)
		Dans le détail, la matrice de confusion représentée visuellement ci-dessous par un heatmap montre son meilleur taux de prédiction des accidents corporels sur les cas les moins graves (modalité '4' = 'blessé léger'), alors que les autres prédictions présentent un nombre élevé de mauvaises prévisions par le modèle.
		"""
		st.image('PySecuRoute-DecisionTree-02-Matrice-confusion-heatmap.png')
		"""
		En chiffres, cela donne le tableau ci-dessous. Les effectifs visualisés de cette façon sont plus parlants. En outre, il nous permet de calculer que pour la modalité '3' (='blessé hospitalisé`) par exemple, le pourcentage de mauvaises prédictions s’élève à 58,7% et à 0,6%, soit un taux de prévisions correctes 40,7%.
		"""
		st.image('PySecuRoute-DecisionTree-03-Matrice-confusion-tableau.png')
		"""
		#### Top 10 des variables explicatives
		Un autre résultat est le top 10 des variables explicatives déterminé par notre modèle de DecisionTree :
		"""
		st.image('PySecuRoute-DecisionTree-04-Top10-Importance-variables-explicatives-tableau.png')
		"""
		Il se caractérise par la prévalence de la catégorie de la route (`catr`), suivi de près par le code INSEE de la commune (`com`), puis par l’usage ou non de certains équipements de sécurité (`secu`) et le nombre total de voies de circulation (`nbv`) et enfin par le type de collision (`col`) pour le top 5.

		A elles cinq, ces variables expliquent 55,5% de la prédiction de notre modèle.


		#### Conclusions et pistes d’améliorations avec DecisionTree
		La modélisation avec DecisionTree se révèle acceptable avec son taux de bonnes prédictions de __70,52%__, mais présente de nombreuses limites en termes de robustesse. La plus importante d’entre-elles est le biais de prédiction vers les accidents corporels les moins graves (indemnes exclus).

		Les pistes d’améliorations avec ce modèle de Machine Learning seraient :
		* dans le jeu de données, de supprimer les modalités non prédites, soit la modalité la moins grave : '1' (= les indemnes),
		* d’opérer une stratification en fonction des modalités présentes au moment de créer les jeux de données d’entraînement et de test,
		* de réaliser un graphique visuel de l'arbre de décision. Vu le très grand nombre de nœuds, les images créées ont été inexploitables. Il faudrait peut-être chercher un package interactif pour un tel arbre de décision.

		Les autres pistes d’améliorations seraient :
		* choisir un modèle de Machine Learning plus adapté au type qualitatif de notre jeu de données et à son nombre élevé d’observations (largement supérieur au seuil des 100k observations), comme __SGDClassifier__ par exemple.
		* tester une modélisation Machine Learning dans une bibliothèque plus adaptée au Big Data, telle que __PySpark__.
		"""

	if st.checkbox('Implémentation du modèle'):
		"""
		#### Préambule
		Au-delà de réaliser une modélisation de Machine Learning capable de prédire correctement les accidents corporels en France, nous vous proposons de vous essayer à la simulation.
		
		Vous trouverez ci-dessous un formulaire qui vous permet de choisir les paramètres d’un accident fictif pour lequel la modélisation va vous prédire, dans la limite de ses capacités, la gravité de l’usager. Vous pouvez choisir différents paramètres sur l’accident, comme son lieu, son type, ainsi que la présence et l’utilisation ou non de certains équipements de sécurité.
		
		Nous avons supprimé la variable du code INSEE de la commune ('com') à cause des complexités que son implémentation requérait pour qu’un utilisateur la sélectionne de façon ergonomique et intuitive. Cela a pour conséquence de baisser légèrement le taux de réussite de prédiction du modèle, passant de 70,5 à 70,1%. 
		"""
		# Chargement du modèle entraîné via pickle
		pickle_fichier = open('clf_dt3-pickle.pkl', 'rb') 
		classifier_pickle = pickle.load(pickle_fichier)
	 
		# Fonction qui réalisera la prédiction en utilisant les données entrées par l'utilisateur
		def prediction(catr_select, secu_select, nbv_select, col_select, agg_select, situ_select, obsm_select, larrout_select, obs_select):
			# Pre-processing des entrées de l'utilisateur    
			# Catégorie de route
			catr_switch = {
					'Autoroute':1,
					'Route Nationale':2,
					'Route Départementale':3,
					'Voie Communale':4,
					'Hors réseau public':5,
					'Parc de stationnement public':6,
					'Autre':9
					}
					
			catr = catr_switch[catr_select]
			# Présence et utilisation d'équipement de sécurité
			secu_switch = {
					'Ceinture utilisée':11,
					'Ceinture non utilisée':12,
					'Ceinture, utilisation indéterminable':13,
					'Casque utilisé':21,
					'Casque non utilisé':22,
					'Casque, utilisation indéterminable':23,
					'Dispositif enfants utilisé':31,
					'Dispositif enfants non utilisé':32,
					'Dispositif enfants, utilisation indéterminable':33,
					'Equipement réfléchissant utilisé':41,
					'Equipement réfléchissant non utilisé':42,
					'Equipement réfléchissant, utilisation indéterminable':43,
					'Autre équipement utilisé':91,
					'Autre équipement non utilisé':92,
					'Autre équipement, utilisation indéterminable':93
					}
			secu = secu_switch[secu_select]
			
			# Type de collision
			col_switch = {
					'Deux véhicules, collision frontale':1,
					'Deux véhicules, collision par l\'arrière':2,
					'Deux véhicules, collision par le coté':3,
					'Trois véhicules et plus, collision en chaîne':4,
					'Trois véhicules et plus, collisions multiples':5,
					'Autres types de collision':6,
					'Aucune collision':7
					}
			col = col_switch[col_select]
			
			# En/hors agglomération
			agg_switch = {
					'Hors agglomération':1,
					'En agglomération':2
					}
			agg = agg_switch[agg_select]
			
			# Situation de l'accident
			situ_switch = {
						'Sur chaussée':1,
						"Sur bande d'arrêt d'urgence":2,
						'Sur accotement':3,
						'Sur trottoir':4,
						'Sur piste cyclable':5
					}
			situ = situ_switch[situ_select]
			
			# Obstacle mobile heurté
			obsm_switch = {
					'Piéton':1,
					'Véhicule':2,
					'Véhicule sur rail':4,
					'Animal domestique':5,
					'Animal sauvage':6,
					'Autre':9
					}
			obsm = obsm_switch[obsm_select]
			
			# Obstacle fixe heurté
			obs_switch = {
					'Véhicule en stationnement':1,
					'Arbre':2,
					'Glissière métallique':3,
					'Glissière béton':4,
					'Autre type de glissière':5,
					'Bâtiment, mur, pile de pont':6,
					'Support de signalisation verticale ou poste d\'appel d\'urgence':7,
					'Poteau':8,
					'Mobilier urbain':9,
					'Parapet':10,
					'Ilot, refuge, borne haute':11,
					'Bordure de trottoir':12,
					'Fossé, talus, paroi rocheuse':13,
					'Autre obstacle fixe sur la chaussée':14,
					'Autre obstacle fixe sur le trottoir ou l\'accotement':15,
					'Sortie de chaussée sans obstacle':16
					}
			obs = obs_switch[obs_select]
			
			# Largeur de route
			larrout = larrout_select
			
			# Nombre de voies
			nbv = nbv_select
	 
			# Réalisation de la prediction personnalisée 
			prediction = classifier_pickle.predict( 
				[[catr, secu, nbv, col, agg, situ, obsm, larrout, obs]]
				)

			# ~ nos prédictions renvoient les modalités : 2,3,4 
			return prediction  

		# Fonction de création de la page web Streamlit
		def main_model():
			 
			catr_select = st.selectbox('Catégorie de route', [	'Autoroute',
			'Route Nationale',
			'Route Départementale',
			'Voie Communale',
			'Hors réseau public',
			'Parc de stationnement public',
			'Autre'])
			
			secu_select = st.selectbox("Présence et utilisation d'équipement de sécurité", ['Ceinture utilisée',
					'Ceinture non utilisée',
					'Ceinture, utilisation indéterminable',
					'Casque utilisé',
					'Casque non utilisé',
					'Casque, utilisation indéterminable',
					'Dispositif enfants utilisé',
					'Dispositif enfants non utilisé',
					'Dispositif enfants, utilisation indéterminable',
					'Equipement réfléchissant utilisé',
					'Equipement réfléchissant non utilisé',
					'Equipement réfléchissant, utilisation indéterminable',
					'Autre équipement utilisé',
					'Autre équipement non utilisé',
					'Autre équipement, utilisation indéterminable'])

			col_select = st.selectbox('Type de collision',['Deux véhicules, collision frontale',
			'Deux véhicules, collision par l\'arrière',
			'Deux véhicules, collision par le coté',
			'Trois véhicules et plus, collision en chaîne',
			'Trois véhicules et plus, collisions multiples',
			'Autres types de collision',
			'Aucune collision'
			])

			agg_select = st.selectbox('En/hors agglomération',['Hors agglomération',
			'En agglomération'
			])

			situ_select = st.selectbox("Situation de l'accident",['Sur chaussée',
						"Sur bande d'arrêt d'urgence",
						'Sur accotement',
						'Sur trottoir',
						'Sur piste cyclable'])

			obsm_select = st.selectbox("Obstacle mobile heurté",['Piéton',
			'Véhicule',
			'Véhicule sur rail',
			'Animal domestique',
			'Animal sauvage',
			'Autre'])
			
			obs_select = st.selectbox("Obstacle fixe heurté",['Véhicule en stationnement',
			'Arbre',
			'Glissière métallique',
			'Glissière béton',
			'Autre type de glissière',
			'Bâtiment, mur, pile de pont',
			'Support de signalisation verticale ou poste d\'appel d\'urgence',
			'Poteau',
			'Mobilier urbain',
			'Parapet',
			'Ilot, refuge, borne haute',
			'Bordure de trottoir',
			'Fossé, talus, paroi rocheuse',
			'Autre obstacle fixe sur la chaussée',
			'Autre obstacle fixe sur le trottoir ou l\'accotement',
			'Sortie de chaussée sans obstacle'])
			
			larrout_select = st.selectbox("Largeur de la route (en m)",np.arange(1,1000,1))
			
			nbv_select = st.selectbox("Nombre de voies",np.arange(1,10,1))
			
			if st.button("Prédire"): 
				result = prediction(catr_select, secu_select, nbv_select, col_select, agg_select, situ_select, obsm_select, larrout_select, obs_select)
				if result == 2:
					st.success('Tué')
				elif result == 3:
					st.success('Blessé hospitalisé')
				elif result == 4:
					st.success('Blessé léger') 
			    

		"""
		### Prédiction
		---
		#### Veuillez sélectionner les modalités des variables explicatives ci-dessous :
			""" 
			
		main_model()

elif nav == '5. Conclusion':
	"""
	La __Dataviz'__ a confirmé en majorité les __prédictions de gravité__ issues du __Machine Learning__ et de la table de __corrélation de Pearson__.
	
	Les variables catégorielles significatives sont :
	* Sexe
	* Âge
	* Catégorie de véhicule
	* Catégorie d'usager
	* Catégorie de route
	* Type de collision
	* Mois
	* Jour
	* Heure

	Les données étudiées sont essentiellement des données de __constat__, et non pas d'enquête.
	Elles complètent parfaitement les variables généralement mises en évidence par les _campagnes de prévention routière_ (vitesse, alcoolémie et téléphone).

	Il serait intéressant de pouvoir réaliser ces mêmes analyses sur les périodes de confinement, afin d'analyser l'impact du Covid sur la circulation routière.
	"""
