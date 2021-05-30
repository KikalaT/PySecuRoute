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
		df[annee] = pd.read_csv('https://christophe-wardius.fr/projets/pysecuroute/dataset_v3/df_'+str(annee)+'_v3.csv')
		
		df[annee].an=df[annee].an+2000
		df[annee]['date']=pd.to_datetime((df[annee].an*10000+df[annee].mois*100+df[annee].jour).apply(str),format='%Y%m%d', exact=False, errors='coerce')
		df[annee]['day']= df[annee].date.dt.weekday
		
		# conversion en 'float64'
		df[annee]['long'] = pd.to_numeric(df[annee]['long'], errors='coerce')
		
		# conversion du CRS en mercator
		k = 6378137
		df[annee]["x"] = (df[annee]['long'] / 100000)* (k * np.pi / 180.0)
		df[annee]["y"] = np.log(np.tan((90 + df[annee]['lat']/100000) * np.pi / 360.0)) * k
		
		# data cleaning
		df[annee].dropna()
		
		print('(done) loading csv file for '+str(annee))

	return df
	
df_ = preprocess()
print('(done) : preprocessing completed.')

# sidebar navigator
st.sidebar.header('PySecuRoute v1.0')
st.sidebar.title('Sommaire')
nav = st.sidebar.radio('',['1. Présentation','2. Exploration','3. Visualisation','4. Modélisation','5. Conclusion'])

"""
# PySecuRoute v1.0
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
	
	st.sidebar.markdown("### Analyses sur l'année : "+str(annee))
	
	## GRAPHIQUES
	###############
	
	
	# carte intéractive BOKEH
	
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def France_Accidents_de_la_route_par_gravité():
		# chargement du fond de carte
		tile_provider = get_provider(OSM)

		# boîte à outils
		tools = "pan,wheel_zoom,box_zoom,reset"

		# Création de la figure

		p = figure(x_range=(-1000000, 2000000), y_range=(5000000, 7000000),
				   x_axis_type="mercator", y_axis_type="mercator",
				   tools=tools,
				   plot_width=800,
				   plot_height=600,
				   title='(France) Accidents de la route par gravité ('+str(annee)+')\n* Échantillon de 30% *'
				   )

		p.add_tile(tile_provider)

		# source
		
		# sampling du df à 30%
		df_bokeh = df_[annee].sample(frac=0.3, replace=True, random_state=1)
		geo_source_1 = ColumnDataSource(data=df_bokeh[df_bokeh['grav'] == 1])
		geo_source_2 = ColumnDataSource(data=df_bokeh[df_bokeh['grav'] == 2])
		geo_source_3 = ColumnDataSource(data=df_bokeh[df_bokeh['grav'] == 3])
		geo_source_4 = ColumnDataSource(data=df_bokeh[df_bokeh['grav'] == 4])

		# points
		p1 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_1, color='green', legend_label='Indemne')
		p2 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_2, color='red', legend_label='Tué')
		p3 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_3, color='orange', legend_label='Blessé hospitalisé')
		p4 = p.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_4, color='yellow', legend_label='Blessé léger')


		# paramètres de la figure
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
		p.legend.label_text_font_size = "9pt"
		p.legend.click_policy = "hide" 

		st.bokeh_chart(p)
	if st.checkbox("Carte intéractive de la gravité des accidentés (France)"):
		France_Accidents_de_la_route_par_gravité()
		
	# Distribution des accidentés par mois
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_par_mois():
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
	if st.checkbox("Distribution des accidentés par mois"):
		distribution_des_accidentés_par_mois()
		
	# Distribution des accidentés par jour de la semaine
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_par_jour_de_la_semaine():
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
	if st.checkbox("Distribution des accidentés par jour de la semaine"):
		distribution_des_accidentés_par_jour_de_la_semaine()
	
	# Distribution des accidentés par heure de la journée
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_par_heure_de_la_journée():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.kdeplot(df_[annee].hrmn/100,ax=ax,shade=True,cut=0)
		plt.xlabel('Heures')
		plt.ylabel('Densité')
		plt.title('Distribution des accidentés par heure de la journée ('+str(annee)+')')
		st.pyplot(fig)
	if st.checkbox("Distribution des accidentés par heure de la journée"):
		distribution_des_accidentés_par_heure_de_la_journée()
		
	# ~ Distribution des accidentés par sexe
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_par_sexe():
		fig, ax = plt.subplots(figsize=(5,5))
		sns.countplot(x="sexe",data=df_[annee])
		plt.xticks([0,1],['M','F'])
		plt.xlabel("Sexe de l'accidenté(e)")
		plt.title('Distribution des accidentés par sexe')
		st.pyplot(fig)
	if st.checkbox("Distribution des accidentés par sexe"):
		distribution_des_accidentés_par_sexe()
	
	# Distribution des accidenté(e)s par obstacles mobiles
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_obstacles_mobiles():
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
	if st.checkbox("Distribution des accidenté(e)s par obstacles mobiles"):
		distribution_des_accidenté_e_s_par_obstacles_mobiles()
	
	#### Distribution des accidenté(e)s par catégorie de `véhicule`
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_catégorie_de_véhicule():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="catv",data=df_[annee])
		plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,
					18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],['01 - Bicyclette',
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
		plt.xticks(rotation=90)
		plt.xlabel("Catégorie de véhicule")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par catégorie de véhicule');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par catégorie de `véhicule`"):
		distribution_des_accidenté_e_s_par_catégorie_de_véhicule()
	
# ~ Distribution des accidenté(e)s par catégorie de route
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_catégorie_de_route():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="catr",data=df_[annee])
		plt.xticks([0,1,2,3,4,5,6],['1 - Autoroute',
									'2 - Route nationale',
									'3 - Route Départementale',
									'4 - Voie Communale',
									'5 - Hors réseau public',
									'6 - Parc de stationnement ouvert à la circulation publique',
									'9 - autre'])
		plt.xticks(rotation=90)
		plt.xlabel("Catégorie de route")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par catégorie de route')
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par catégorie de route"):
		distribution_des_accidenté_e_s_par_catégorie_de_route()
	
	# Distribution des accidenté(e)s par types de choc
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_types_de_choc():
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
	if st.checkbox("Distribution des accidenté(e)s par types de choc"):
		distribution_des_accidenté_e_s_par_types_de_choc()
	
	# Distribution des accidenté(e)s par types de collision
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_types_de_collision():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="col",data=df_[annee])
		plt.xticks(rotation=40)
		plt.xlabel("Type de collision")
		plt.title('Distribution des accidenté(e)s par types de collisions ('+str(annee)+')');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par types de collision"):
		distribution_des_accidenté_e_s_par_types_de_collision()

	# Distribution des accidenté(e)s par motif de trajet
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_motif_de_trajet():
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
	if st.checkbox("Distribution des accidenté(e)s par motif de trajet"):
		distribution_des_accidenté_e_s_par_motif_de_trajet()
	
	# Distribution des accidenté(e)s par type d'accompagnement
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_type_d_accompagnement():
		fig, ax = plt.subplots()
		sns.countplot(x="etatp",data=df_[annee])
		plt.xticks([0,1,2,3],['Non renseigné','Seul','Accompagné','En groupe'])
		plt.xlabel("Accompagnement de l'accidenté(e)")
		plt.title('Distribution des accidentés par accompagnement ('+str(annee)+')');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par type d'accompagnement"):
		distribution_des_accidenté_e_s_par_type_d_accompagnement()
	
	# Distribution des accidenté(e)s par infrastructure
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_infrastructure():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="infra",data=df_[annee])
		plt.xticks([0,1,2,3,4,5,6,7],
					['Aucun','Souterrain / Tunnel','Pont / Autopont',"Bretelle d’échangeur ou de raccordement",
					'Voie ferrée','Carrefour aménagé','Zone piétonne','Zone de péage'],
					rotation=60)
		plt.xlabel("Type d'infrastructure")
		plt.title('Distribution des accidenté(e)s par infrastructure ('+str(annee)+')');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par infrastructure"):
		distribution_des_accidenté_e_s_par_infrastructure()
	
	# ~ Distribution des accidenté(e)s par localisation
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_localisation():
		fig, ax = plt.subplots(figsize=(5,5))
		sns.countplot(x="agg",data=df_[annee])
		plt.xticks([0,1],['Hors agglomération','En agglomération'])
		plt.ylabel('Nombre')
		plt.xlabel("Localisation")
		plt.title('Distribution des accidenté(e)s par localisation')
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par localisation"):
		distribution_des_accidenté_e_s_par_localisation()
	
	# ~ Distribution des accidenté(e)s par situation de l'accident
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_situation_de_l_accident():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="situ",data=df_[annee])
		plt.xticks([0,1,2,3,4,5],['Aucun',
								  'Sur chaussée',
								  'Sur bande d’arrêt d’urgence',
								  'Sur accotement',
								  'Sur trottoir',
								  'Sur piste cyclable'])
		plt.xticks(rotation=30)
		plt.xlabel("Situation de l'accident")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par situation de l'accident");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par situation de l'accident"):
		distribution_des_accidenté_e_s_par_situation_de_l_accident()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav",data=df_[annee])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures()
	
	#### Distribution des accidenté(e)s par gravité des blessures en fonction des `mois de l'année`
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_mois_de_l_année():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="mois", data=df_[annee]);
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
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des mois de l'année");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des `mois de l'année`"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_mois_de_l_année()
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction des jours de la semaine
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_jours_de_la_semaine():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="day", data=df_[annee]);
		plt.legend(labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des jours de la semaine");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des jours de la semaine"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_mois_de_l_année()
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction de l'heure
	
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_l_heure():
		fig, ax = plt.subplots(figsize=(11,5))
		sns.kdeplot(x='hrmn',hue='grav',multiple="stack",data=df_[annee])
		plt.legend(labels=['Blessé léger','Blessé hospitalisé','Tué','Indemne'])
		plt.xticks([0,500,1000,1500,2000],['0:00','5:00','10:00','15:00','20:00'])
		plt.xlim(right=2500)
		plt.xlabel('Heures')
		plt.ylabel('Densité')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de l'heure");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction de l'heure"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_l_heure()
		
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction du sexe
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_sexe():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="sexe", data=df_[annee]);
		plt.legend(labels=['M','F'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du sexe');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction du sexe"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_sexe()
		
	#### Distribution des accidenté(e)s par gravité des blessures en fonction des obstacles `fixes` & `mobiles`
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_obstacles_fixes_mobiles():
		fig, ax = plt.subplots(figsize=(15,15))
		sns.countplot(x="grav", hue="obs", data=df_[annee]);
		plt.legend(labels=['Sans objet',
					   'Véhicule en stationnement',
					   'Arbre','Glissière métallique',
					   'Glissière béton',
					   'Autre glissière',
					   'Bâtiment, mur, pile de pont',
					   'Support de signalisation verticale ou poste d’appel d’urgence',
					   'Poteau',
					   'Mobilier urbain',
					   'Parapet',
					   'Ilot, refuge, borne haute',
					   'Bordure de trottoir',
					   'Fossé, talus, paroi rocheuse',
					   'Autre obstacle fixe sur chaussée',
					   'Autre obstacle fixe sur trottoir ou accotement',
					   'Sortie de chaussée sans obstacle',
					   'Buse – tête d’aqueduc'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des obstacles fixes rencontrés");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des obstacles `fixes` & `mobiles`"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_obstacles_fixes_mobiles()
		
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction des obstacles mobiles rencontrés
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_obstacles_mobiles_rencontrés():
		
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="obsm", data=df_[annee]);
		plt.legend(labels=['Aucun',
					   'Piéton',
					   'Véhicule',
					   'Véhicule sur rail',
					   'Animal domestique',
					   'Animal sauvage',
					   'Autre'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des obstacles mobiles rencontrés");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des obstacles mobiles rencontrés"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_obstacles_mobiles_rencontrés()
	
	#### Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de `véhicule`
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_catégories_de_véhicule():
		fig, ax = plt.subplots(figsize=(20,20))
		sns.countplot(x="grav", hue="catv", data=df_[annee]);
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
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de véhicule');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de `véhicule`"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_catégories_de_véhicule()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de route
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_catégories_de_route():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="catr", data=df_[annee]);
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
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de route');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des catégories de route"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_catégories_de_route()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction des catégories d'usagers
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_catégories_d_usagers():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="catu", data=df_[annee]);
		plt.legend(labels=['1 - Conducteur',
					   '2 - Passager',
					   '3 - Piéton'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des catégories d'usagers");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des catégories d'usagers"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_catégories_d_usagers()
	
	#### Distribution des accidenté(e)s par gravité des blessures en fonction des types de `point de choc`
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_types_de_point_de_choc():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="choc", data=df_[annee]);
		plt.legend(labels=['Aucun',
					   'Avant',
					   'Avant droit',
					   'Avant gauche',
					   'Arrière',
					   'Arrière droit',
					   'Arrière gauche',
					   'Côté droit',
					   'Côté gauche',
					   'Chocs multiples (tonneaux)'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du type de point de choc');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des types de `point de choc`"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_types_de_point_de_choc()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction du type de collision
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_type_de_collision():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="col", data=df_[annee]);
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
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction du type de collision");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction du type de collision"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_type_de_collision()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction du type de trajet
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_type_de_trajet():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="trajet", data=df_[annee]);
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
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction du type de trajet');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction du type de trajet"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_type_de_trajet()
	
	#### Distribution des accidenté(e)s par gravité des blessures en fonction de variables complémentaires
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_variables_complémentaires():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="agg", data=df_[annee]);
		plt.legend(labels=['Hors agglomération','En agglomération'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction de la localisation');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction de variables complémentaires"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_variables_complémentaires()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction du type d'aménagement / d'infrastructure
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_type_d_aménagement_d_infrastructure():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="infra", data=df_[annee]);
		plt.legend(labels=['Aucun',
					   'Souterrain - tunnel',
					   'Pont - autopont',
					   'Bretelle d’échangeur ou de raccordement',
					   'Voie ferrée',
					   'Carrefour aménagé',
					   'Zone piétonne',
					   'Zone de péage'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction du type d'aménagement / d'infrastructure");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction du type d'aménagement / d'infrastructure"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_du_type_d_aménagement_d_infrastructure()
		
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction de la situation de l'accident
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_la_situation_de_l_accident():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="situ", data=df_[annee]);
		plt.legend(labels=['Aucun',
					   'Sur chaussée',
					   'Sur bande d’arrêt d’urgence',
					   'Sur accotement',
					   'Sur trottoir',
					   'Sur piste cyclable'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de la situation de l'accident");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction de la situation de l'accident"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_la_situation_de_l_accident()
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction des conditions d'éclairage
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_conditions_d_éclairage():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="grav", hue="lum", data=df_[annee]);
		plt.legend(labels=['Plein jour',
					   'Crépuscule ou aube',
					   'Nuit sans éclairage public',
					   'Nuit avec éclairage public non allumé',
					   'Nuit avec éclairage public allumé'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction des conditions d'éclairage");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des conditions d'éclairage"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_conditions_d_éclairage()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction des conditions atmosphériques
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_conditions_atmosphériques():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="atm", data=df_[annee]);
		plt.legend(labels=['Normale',
					   'Pluie légère',
					   'Pluie forte',
					   'Neige - grêle',
					   'Brouillard - fumée',
					   'Vent fort - tempête',
					   'Temps éblouissant',
					   'Temps couvert',
					   'Autre'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par gravité des blessures en fonction des conditions atmosphériques');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction des conditions atmosphériques"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_des_conditions_atmosphériques()
	
	# ~ Distribution des accidenté(e)s par gravité des blessures en fonction de l'état de la surface
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_l_état_de_la_surface():
		fig, ax = plt.subplots(figsize=(10,10))
		sns.countplot(x="grav", hue="surf", data=df_[annee]);
		plt.legend(labels=['Non renseigné',
					   'Normale',
					   'Mouillée',
					   'Flaques',
					   'Inondée',
					   'Enneigée',
					   'Boue',
					   'Verglacée',
					   'Corps gras – huile',
					   'Autre'])
		plt.xticks([0,1,2,3],['Indemne',
						  'Tué',
						  'Blessé hospitalisé',
						  'Blessé léger'])
		plt.xlabel("Gravité du bléssé")
		plt.ylabel('Nombre')
		plt.title("Distribution des accidenté(e)s par gravité des blessures en fonction de l'état de la surface");
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par gravité des blessures en fonction de l'état de la surface"):
		distribution_des_accidenté_e_s_par_gravité_des_blessures_en_fonction_de_l_état_de_la_surface()
		
	# ~ Distribution des accidenté(e)s par conditions atmosphériques
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidenté_e_s_par_conditions_atmosphériques():
		fig, ax = plt.subplots(figsize=(10,5))
		sns.countplot(x="atm",data=df_[annee])
		plt.xticks([0,1,2,3,4,5,6,7,8],['Normale',
										'Pluie légère',
										'Pluie forte',
										'Neige - grêle',
										'Brouillard - fumée',
										'Vent fort - tempête',
										'Temps éblouissant',
										'Temps couvert',
										'Autre'])
		plt.xticks(rotation=20)
		plt.xlabel("Conditions atmosphériques")
		plt.ylabel('Nombre')
		plt.title('Distribution des accidenté(e)s par conditions atmosphériques');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidenté(e)s par conditions atmosphériques"):
		distribution_des_accidenté_e_s_par_conditions_atmosphériques()
		
	# Distribution des accidentés en fonction des `conditions atmosphériques`
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_en_fonction_des_conditions_atmosphériques():
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
	if st.checkbox("Distribution des accidentés en fonction des `conditions atmosphériques`"):
		distribution_des_accidentés_en_fonction_des_conditions_atmosphériques()
	
	# ~ Distribution des accidentés en région Île-de-France suivant la météo
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_en_région_île_de_france_suivant_la_météo():
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
	if st.checkbox("Distribution des accidentés en région Île-de-France suivant la météo"):
		distribution_des_accidentés_en_région_île_de_france_suivant_la_météo()
	
	# ~ Distribution des accidentés en région Auvergne-Rhône-Alpes suivant la météo
	@st.cache(suppress_st_warning=True, allow_output_mutation=True)
	def distribution_des_accidentés_en_région_auvergne_rhône_alpes_suivant_la_météo():
		fig, ax = plt.subplots(figsize=(15,15))
		sns.countplot(x=df_[annee].atm, hue=df_[annee].mois,data=df_[annee][df_[annee].region=='Auvergne-Rhône-Alpes'], palette='hls')
		ax.xaxis.set_ticklabels(labels_atm, rotation=60)
		plt.xlabel('Conditions atmosphériques')
		plt.ylabel('Occurrence\n(échelle log)')
		plt.title('Distribution des accidentés en région Auvergne-Rhône-Alpes suivant la météo ('+str(annee)+')')
		plt.yscale('log')
		plt.legend(loc='best');
		st.pyplot(fig)
	if st.checkbox("Distribution des accidentés en région Auvergne-Rhône-Alpes suivant la météo"):
		distribution_des_accidentés_en_région_auvergne_rhône_alpes_suivant_la_météo()
	

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
