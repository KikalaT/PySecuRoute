import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# ~ from bokeh.plotting import figure
# ~ from bokeh.tile_providers import get_provider, OSM
# ~ from bokeh.transform import factor_cmap
# ~ from bokeh.models.tools import WheelZoomTool
# ~ from bokeh.models import ColumnDataSource

import streamlit as st

# page configuration
st.set_page_config(
page_title="PySecuRoute v1.0",
layout="wide",
)

# pré-processing (mise en cache pour gain de performance)
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def preprocess():
	## chargement des données
	
	# chargement du 'df_master' des jeu de données
	data = json.load(open('data.json','r'))
	df_master = pd.json_normalize(data['distribution'])
	
	# chargement des df par année
	df = {}
	annees = np.arange(2005,2018,1)
	
	for annee in annees:
		df[annee] = pd.read_csv('https://www.jazzreal.org/static/df_'+str(annee)+'_v3.csv')
		df[annee].an=df[annee].an+2000
		df[annee]['date']=pd.to_datetime((df[annee].an*10000+df[annee].mois*100+df[annee].jour).apply(str),format='%Y%m%d', exact=False, errors='coerce')
		df[annee]['day']= df[annee].date.dt.weekday
		
		# ~ # conversion en 'float64'
		# ~ df['long'] = pd.to_numeric(df['long'], errors='coerce')
		
		# ~ # conversion du CRS en mercator
		# ~ k = 6378137
		# ~ df["x"] = (df['long'] / 100000)* (k * np.pi / 180.0)
		# ~ df["y"] = np.log(np.tan((90 + df['lat']/100000) * np.pi / 360.0)) * k
		
		# data cleaning
		df[annee].dropna()
	
	return df
	
df_ = preprocess()

# sidebar navigator
st.sidebar.header('PySecuRoute')
st.sidebar.title('Sommaire')
nav = st.sidebar.radio('',['1. Présentation','2. Exploration','3. Visualisation','4. Modélisation','5. Conclusion'])

"""
# PySecuRoute
### Datascientest - Bootcamp Data Analyst (Avril 2021-Juin 2021)
#### `Pascal INDICE` | `Kikala TRAORÉ` | `Christophe WARDIUS` | `Hervé HOUY`
---
"""

if nav == '1. Présentation':
	"""
	## 1. Présentation du projet


	Les accidents corporels sont courants et les répertorier permet de les étudier afin d’identifier
	les différents cas qui ont impliqué des blessures plus ou moins graves. Prédire la gravité
	d’un accident en fonction de ses différentes caractéristiques peut être utile pour proposer
	une solution qui a comme but de réduire la fréquence des accidents graves.

	Plusieurs jeux de données répertorient l’intégralité des accidents corporels de la circulation
	intervenus durant une année précise en France métropolitaine et dans les DOM-TOM. Ces
	jeux de données comprennent des informations de localisation de l’accident ainsi que des
	informations concernant les caractéristiques de l’accident et son lieu, les véhicules impliqués
	et leurs victimes.

	Nous avons choisi d'exploiter les données dont les sources sont téléchargeables au lien suivant :

	[source](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019/#_)

	## Description des données

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
	site www.data.gouv.fr, les bases de données de 2005 à 2019 sont désormais annuelles et composées
	de 4 fichiers (Caractéristiques – Lieux – Véhicules – Usagers) au format csv. 
	"""

elif nav == '2. Exploration':
	"""
		## 2. Exploration des données
		
		TODO...
	"""
	
elif nav == '3. Visualisation':
	"""
		## 3. Visualisation des données
	"""
	
	annee = st.selectbox('Choisir une année (2005 à 2017)', np.arange(2005,2018,1))
	
	## GRAPHIQUES
	###############
	
	# ~ # carte intéractive BOKEH

	# ~ # chargement du fond de carte
	# ~ tile_provider = get_provider(OSM)

	# ~ # boîte à outils
	# ~ tools = "pan,wheel_zoom,box_zoom,reset"

	# ~ # Création de la figure

	# ~ p = figure(x_range=(-1000000, 2000000), y_range=(5000000, 7000000),
			   # ~ x_axis_type="mercator", y_axis_type="mercator",
			   # ~ tools=tools,
			   # ~ plot_width=800,
			   # ~ plot_height=600,
			   # ~ title='(France) Accidents de la route par gravité ('+str(annee)+')'
			   # ~ )

	# ~ p.add_tile(tile_provider)

	# ~ # source
	# ~ geo_source_1 = ColumnDataSource(data=df_[annee][df_[annee]['grav'] == 1])
	# ~ geo_source_2 = ColumnDataSource(data=df_[annee][df_[annee]['grav'] == 2])
	# ~ geo_source_3 = ColumnDataSource(data=df_[annee][df_[annee]['grav'] == 3])
	# ~ geo_source_4 = ColumnDataSource(data=df_[annee][df_[annee]['grav'] == 4])

	# ~ # points
	# ~ p1 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_1, color='green', legend_label='Indemne')
	# ~ p2 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_2, color='red', legend_label='Tué')
	# ~ p3 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_3, color='orange', legend_label='Blessé hospitalisé')
	# ~ p4 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_4, color='yellow', legend_label='Blessé léger')


	# ~ # paramètres de la figure
	# ~ p.xgrid.grid_line_color = None
	# ~ p.ygrid.grid_line_color = None
	# ~ p.xaxis.major_label_text_color = None
	# ~ p.yaxis.major_label_text_color = None
	# ~ p.xaxis.major_tick_line_color = None  
	# ~ p.xaxis.minor_tick_line_color = None  
	# ~ p.yaxis.major_tick_line_color = None  
	# ~ p.yaxis.minor_tick_line_color = None  
	# ~ p.yaxis.axis_line_color = None
	# ~ p.xaxis.axis_line_color = None
	# ~ p.legend.label_text_font_size = "9pt"
	# ~ p.legend.click_policy = "hide" 

	# ~ st.bokeh_chart(p)
	
	# Distribution des accidentés par mois
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="mois", data=df_[annee], palette='hls')
	plt.xlabel('Mois')
	plt.ylabel('Nombre')
	plt.title('Distribution des accidentés par mois ('+str(annee)+')')
	plt.xticks(ticks=np.arange(1,13,1),
			   labels=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'],
			   rotation=60
			  );
	st.pyplot(fig)

	# Distribution des accidentés par jour de la semaine"""
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(df_[annee].day);
	plt.xlabel('Jours')
	plt.ylabel('Nombre')
	plt.title('Distribution des accidentés par jour de la semaine ('+str(annee)+')')
	plt.xticks(ticks=np.arange(0,7,1),
			   labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'],
			   rotation=60
			  );
	st.pyplot(fig)
	 
	# Distribution des accidentés par heure de la journée"""        
	fig, ax = plt.subplots(figsize=(10,5))
	sns.kdeplot(df_[annee].hrmn/100,ax=ax,shade=True,cut=0)
	plt.xlabel('Heures')
	plt.ylabel('Densité')
	plt.title('Distribution des accidentés par heure de la journée ('+str(annee)+')')
	st.pyplot(fig)

	# Distribution des accidenté(e)s par obstacles mobiles"""
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="obsm",data=df_[annee])
	plt.xticks([0,1,2,3,4,5,6],['Aucun',
								'Piéton',
								'Véhicule',
								'Véhicule sur rail',
								'Animal domestique',
								'Animal sauvage',
								'Autre'])
	plt.xticks(rotation=40)
	plt.xlabel("Type d'obstacle mobile")
	plt.title('Distribution des accidenté(e)s par obstacles mobiles ('+str(annee)+')')
	st.pyplot(fig)

	# Distribution des accidenté(e)s par types de choc"""
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="choc",data=df_[annee])
	plt.xticks([0,1,2,3,4,5,6,7,8,9],['Aucun',
									  'Avant',
									  'Avant droit',
									  'Avant gauche',
									  'Arrière',
									  'Arrière droit',
									  'Arrière gauche',
									  'Côté droit',
									  'Côté gauche',
									  'Chocs multiples (tonneaux)'])
	plt.xticks(rotation=40)
	plt.xlabel("Type de choc")
	plt.title('Distribution des types de choc des accidenté(e)s ('+str(annee)+')');
	st.pyplot(fig)

	# Distribution des accidenté(e)s par types de collision"""
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="col",data=df_[annee])
	plt.xticks(rotation=40)
	plt.xlabel("Type de collision")
	plt.title('Distribution des accidenté(e)s par types de collisions ('+str(annee)+')');
	st.pyplot(fig)

	# Distribution des accidenté(e)s par motif de trajet"""
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="trajet",data=df_[annee])
	plt.xticks([0,1,2,3,4,5,6],['Non renseigné',
								'Domicile – travail',
								'Domicile – école',
								'Courses – achats',
								'Utilisation professionnelle',
								'Promenade – loisirs',
								'Autre'])
	plt.xticks(rotation=40)
	plt.xlabel("Type de trajet")
	plt.title('Distribution des accidenté(e)s par motif de trajet ('+str(annee)+')');
	st.pyplot(fig)

	# Distribution des accidenté(e)s par type d'accompagnement"""
	fig, ax = plt.subplots()
	sns.countplot(x="etatp",data=df_[annee])
	plt.xticks([0,1,2,3],['Non renseigné','Seul','Accompagné','En groupe'])
	plt.xlabel("Accompagnement de l'accidenté(e)")
	plt.title('Distribution des accidentés par accompagnement ('+str(annee)+')');
	st.pyplot(fig)

	# Distribution des accidenté(e)s par infrastructure"""
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="infra",data=df_[annee])
	plt.xticks([0,1,2,3,4,5,6,7],
				['Aucun','Souterrain / Tunnel','Pont / Autopont',"Bretelle d’échangeur ou de raccordement",
				'Voie ferrée','Carrefour aménagé','Zone piétonne','Zone de péage'],
				rotation=60)
	plt.xlabel("Type d'infrastructure")
	plt.title('Distribution des accidenté(e)s par infrastructure ('+str(annee)+')');
	st.pyplot(fig)

	# Distribution de la gravité des accidenté(e)s par rapport au sexe"""
	df_[annee]['sexe'] = df_[annee]['sexe'].replace({1:'homme',2:'femme'})
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="grav", hue="sexe", data=df_[annee])
	plt.xticks([0,1,2,3],['Indemne','Tué','Blessé hospitalisé','Blessé léger'],rotation=40)
	plt.title('Distribution de la gravité des accidenté(e)s par rapport au sexe ('+str(annee)+')');
	st.pyplot(fig)

	# 12. Distribution de la gravité des accidenté(e)s par rapport au type de trajet
	df_[annee]['trajet'] = df_[annee]['trajet'].replace({ 0 : 'Non renseigné',
							1 : 'Domicile – travail', 2 : 'Domicile – école', 3 : 'Courses – achats',
							4 : 'Utilisation professionnelle', 5 : 'Promenade – loisirs', 9 : 'Autre'}
							)
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="grav", hue="trajet", data=df_[annee])
	plt.xticks([0,1,2,3],['Indemne','Tué','Blessé hospitalisé','Blessé léger'],rotation=40)
	plt.title('Distribution de la gravité des accidenté(e)s par rapport au type de trajet');
	st.pyplot(fig)

	# 13. Distribution de la gravité des accidenté(e)s par rapport au type de collision
	df_[annee]['col'] = df_[annee]['col'].replace({
											1 : 'Deux véhicules - frontale', 2 : 'Deux véhicules – par l’arrière',
											 3 : 'Deux véhicules – par le coté', 4 : 'Trois véhicules et plus – en chaîne',
											  5 : 'Trois véhicules et plus - collisions multiples', 6 : 'Autre collision',
											   7 : 'Sans collision'}
											   )
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="grav", hue="col", data=df_[annee])
	plt.xticks([0,1,2,3],['Indemne','Tué','Blessé hospitalisé','Blessé léger'],rotation=40)
	plt.title('Distribution de la gravité des accidenté(e)s par rapport au type de collision ('+str(annee)+')');
	st.pyplot(fig)

	# Distribution de la gravité des accidenté(e)s par rapport à la place de l'accidenté(e)s
	fig, ax = plt.subplots(figsize=(10,5))
	sns.countplot(x="grav", hue="place", data=df_[annee])
	plt.xticks([0,1,2,3],['Indemne','Tué','Blessé hospitalisé','Blessé léger'],rotation=40)
	plt.title("Distribution de la gravité des accidenté(e)s par rapport à la place de l'accidenté(e)s ("+str(annee)+')');
	
	col1, col2 = st.beta_columns(2)
	with col1:
		st.image('place.png')
	with col2:
		st.pyplot(fig)

	# Distribution des accidentés en fonction des `conditions atmosphériques`
	labels_atm = ['Normale','Pluie légère','Pluie forte','Neige - grêle','Brouillard - fumée','Vent fort - tempête','Temps éblouissant','Temps couvert','Autre']

	fig, ax = plt.subplots(figsize=(20,15))
	g = sns.countplot(x=df_[annee].atm, hue=df_[annee].region, data=df_[annee], palette='hls')
	ax.xaxis.set_ticklabels(labels_atm, rotation=60)
	plt.xlabel('Conditions atmosphériques')
	plt.ylabel('Occurrence\n(échelle log)')
	plt.title('Distribution des accidentés suivant la météo ('+str(annee)+')')
	plt.yscale('log')
	plt.legend(loc='upper center');
	st.pyplot(fig)

	"""__Observations__ : Pour l'Île-de-France certaines conditions atmosphériques ont une répercussion sur le nombre d'accidentés :

			- Pluie légère 
			- Pluie forte
			- Temps couvert"""

	"""zoom sur l'Île-de-France"""
	fig, ax = plt.subplots(figsize=(15,15))
	df_[annee].mois = df_[annee].mois.replace({1:'Janvier',2:'Février',3:'Mars',
							   4:'Avril',5:'Mai',6:'Juin',7:'Juillet',
							   8:'Août',9:'Septembre',10:'Octobre',
							   11:'Novembre',12:'Décembre'}
							 )
	sns.countplot(x=df_[annee].atm, hue=df_[annee].mois ,data=df_[annee][df_[annee].region=='Île-de-France'], palette='hls')
	ax.xaxis.set_ticklabels(labels_atm, rotation=60)
	plt.xlabel('Conditions atmosphériques')
	plt.ylabel('Occurrence\n(échelle log)')
	plt.title('Distribution des accidentés en région Île-de-France suivant la météo ('+str(annee)+')')
	plt.yscale('log')
	plt.legend(loc='best');
	st.pyplot(fig)

	"""zoom sur Auvergne-Rhônes-Alpes"""
	fig, ax = plt.subplots(figsize=(15,15))
	sns.countplot(x=df_[annee].atm, hue=df_[annee].mois,data=df_[annee][df_[annee].region=='Auvergne-Rhône-Alpes'], palette='hls')
	ax.xaxis.set_ticklabels(labels_atm, rotation=60)
	plt.xlabel('Conditions atmosphériques')
	plt.ylabel('Occurrence\n(échelle log)')
	plt.title('Distribution des accidentés en région Auvergne-Rhône-Alpes suivant la météo ('+str(annee)+')')
	plt.yscale('log')
	plt.legend(loc='best');
	st.pyplot(fig)


elif nav == '4. Modélisation':
	"""
		## 4. Modélisation
		
		TODO...
	"""
	
elif nav == '5. Conclusion':
	"""
		## 5. Conclusion
		
		TODO...
	"""
