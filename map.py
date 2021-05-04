import pandas as pd
import numpy as np
import json

from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, OSM
from bokeh.transform import factor_cmap
from bokeh.models.tools import WheelZoomTool
from bokeh.models import ColumnDataSource

import streamlit as st

st.title('GeoSecuRoute')

"""
## Présentation du projet


Les accidents corporels sont courants et les répertorier permet de les étudier afin d’identifier
les différents cas qui ont impliqué des blessures plus ou moins graves. Prédire la gravité
d’un accident en fonction de ses différentes caractéristiques peut être utile pour proposer
une solution qui a comme but de réduire la fréquence des accidents graves.
Data

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

@st.cache(suppress_st_warning=True)
def preprocess():
	## chargement des données
	
	# chargement du 'df_master' des jeu de données
	data = json.load(open('data.json','r'))
	df_master = pd.json_normalize(data['distribution'])
	
	# identification des datasets présents de 2005 à 2017
	datasets = ['vehicules-2017.csv', 'usagers-2017.csv', 'lieux-2017.csv',
       'caracteristiques-2017.csv', 'vehicules_2016.csv',
       'usagers_2016.csv', 'lieux_2016.csv', 'caracteristiques_2016.csv',
       'vehicules_2015.csv', 'caracteristiques_2015.csv',
       'lieux_2015.csv', 'usagers_2015.csv', 'caracteristiques_2014.csv',
       'vehicules_2014.csv', 'lieux_2014.csv', 'usagers_2014.csv',
       'caracteristiques_2013.csv', 'vehicules_2013.csv',
       'lieux_2013.csv', 'usagers_2013.csv', 'caracteristiques_2012.csv',
       'vehicules_2012.csv', 'usagers_2012.csv', 'lieux_2012.csv',
       'caracteristiques_2011.csv', 'usagers_2011.csv',
       'vehicules_2011.csv', 'lieux_2011.csv',
       'caracteristiques_2010.csv', 'lieux_2010.csv',
       'vehicules_2010.csv', 'usagers_2010.csv',
       'caracteristiques_2009.csv', 'lieux_2009.csv',
       'vehicules_2009.csv', 'usagers_2009.csv',
       'caracteristiques_2008.csv', 'vehicules_2008.csv',
       'usagers_2008.csv', 'lieux_2008.csv', 'caracteristiques_2007.csv',
       'vehicules_2007.csv', 'lieux_2007.csv', 'usagers_2007.csv',
       'caracteristiques_2006.csv', 'lieux_2006.csv',
       'vehicules_2006.csv', 'usagers_2006.csv',
       'caracteristiques_2005.csv', 'vehicules_2005.csv',
       'lieux_2005.csv', 'usagers_2005.csv']

	# téléchargement et conversion des datasets en DataFrame
	dfs = {}
	for dataset in datasets:
		name = dataset
		url = df_master[df_master['name'] == name]['url'].values[0]
		name = name.replace('-','_')
		print(name[:-4],url)
		try:
			dfs[name[:-4]] = pd.read_csv(url, encoding = "ISO-8859-1")
		except:
			print("\nune erreur s'est produite avec :",name)
			print("\n")
			
	# import du module requests afin de télécharger le dataset 'caracteristiques_2009.csv'
	import requests
	from io import StringIO

	caracteristiques_2009 = requests.get(df_master[df_master['name'] == 'caracteristiques_2009.csv']['url'].values[0])
	caracteristiques_2009 = caracteristiques_2009.text
	caracteristiques_2009 = pd.read_csv(StringIO(caracteristiques_2009), engine='python', sep='\t')
	
	# ajout du DataFrame 'caracteristiques_2009'
	dfs['caracteristiques_2009'] = caracteristiques_2009
	
	# dictionnaire des dataframes par année
	df_annee = {}

	# variable 'annees' pour la boucle 'for'
	annees = np.arange(2005,2018,1)

	for annee in annees:
		vehicules = 'vehicules_'+str(annee)
		caracts = 'caracteristiques_'+str(annee)
		lieux = 'lieux_'+str(annee)
		usagers = 'usagers_'+str(annee)
		df_annee[annee] = pd.concat([dfs[vehicules],
				   dfs[caracts],
				   dfs[lieux],
				   dfs[usagers]],
				   join='inner',
				 axis=1)
		df_annee[annee] = df_annee[annee].loc[:,~df_annee[annee].columns.duplicated()]
	
	# création de la liste des Dataframes à concaténer
	df_s= [df_annee[annee] for annee in annees]

	# concaténation finale
	df = pd.concat(df_s,axis=0)
	df = df.reset_index().drop(columns='index')
	
	REGIONS = {
    'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
    'Bretagne': ['35', '22', '56', '29'],
    'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
    'Corse': ['2A', '2B'],
    'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    'Guadeloupe': ['971'],
    'Guyane': ['973'],
    'Hauts-de-France': ['02', '59', '60', '62', '80'],
    'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'La Réunion': ['974'],
    'Martinique': ['972'],
    'Normandie': ['14', '27', '50', '61', '76'],
    'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    'Pays de la Loire': ['44', '49', '53', '72', '85'],
    'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
	}

	DEPARTEMENTS = {
		'01': 'Ain', 
		'02': 'Aisne', 
		'03': 'Allier', 
		'04': 'Alpes-de-Haute-Provence', 
		'05': 'Hautes-Alpes',
		'06': 'Alpes-Maritimes', 
		'07': 'Ardèche', 
		'08': 'Ardennes', 
		'09': 'Ariège', 
		'10': 'Aube', 
		'11': 'Aude',
		'12': 'Aveyron', 
		'13': 'Bouches-du-Rhône', 
		'14': 'Calvados', 
		'15': 'Cantal', 
		'16': 'Charente',
		'17': 'Charente-Maritime', 
		'18': 'Cher', 
		'19': 'Corrèze', 
		'2A': 'Corse-du-Sud', 
		'2B': 'Haute-Corse',
		'21': 'Côte-d\'Or', 
		'22': 'Côtes-d\'Armor', 
		'23': 'Creuse', 
		'24': 'Dordogne', 
		'25': 'Doubs', 
		'26': 'Drôme',
		'27': 'Eure', 
		'28': 'Eure-et-Loir', 
		'29': 'Finistère', 
		'30': 'Gard', 
		'31': 'Haute-Garonne', 
		'32': 'Gers',
		'33': 'Gironde', 
		'34': 'Hérault', 
		'35': 'Ille-et-Vilaine', 
		'36': 'Indre', 
		'37': 'Indre-et-Loire',
		'38': 'Isère', 
		'39': 'Jura', 
		'40': 'Landes', 
		'41': 'Loir-et-Cher', 
		'42': 'Loire', 
		'43': 'Haute-Loire',
		'44': 'Loire-Atlantique', 
		'45': 'Loiret', 
		'46': 'Lot', 
		'47': 'Lot-et-Garonne', 
		'48': 'Lozère',
		'49': 'Maine-et-Loire', 
		'50': 'Manche', 
		'51': 'Marne', 
		'52': 'Haute-Marne', 
		'53': 'Mayenne',
		'54': 'Meurthe-et-Moselle', 
		'55': 'Meuse', 
		'56': 'Morbihan', 
		'57': 'Moselle', 
		'58': 'Nièvre', 
		'59': 'Nord',
		'60': 'Oise', 
		'61': 'Orne', 
		'62': 'Pas-de-Calais', 
		'63': 'Puy-de-Dôme', 
		'64': 'Pyrénées-Atlantiques',
		'65': 'Hautes-Pyrénées', 
		'66': 'Pyrénées-Orientales', 
		'67': 'Bas-Rhin', 
		'68': 'Haut-Rhin', 
		'69': 'Rhône',
		'70': 'Haute-Saône', 
		'71': 'Saône-et-Loire', 
		'72': 'Sarthe', 
		'73': 'Savoie', 
		'74': 'Haute-Savoie',
		'75': 'Paris', 
		'76': 'Seine-Maritime', 
		'77': 'Seine-et-Marne', 
		'78': 'Yvelines', 
		'79': 'Deux-Sèvres',
		'80': 'Somme', 
		'81': 'Tarn', 
		'82': 'Tarn-et-Garonne', 
		'83': 'Var', 
		'84': 'Vaucluse', 
		'85': 'Vendée',
		'86': 'Vienne', 
		'87': 'Haute-Vienne', 
		'88': 'Vosges', 
		'89': 'Yonne', 
		'90': 'Territoire de Belfort',
		'91': 'Essonne', 
		'92': 'Hauts-de-Seine', 
		'93': 'Seine-Saint-Denis', 
		'94': 'Val-de-Marne', 
		'95': 'Val-d\'Oise',
		'971': 'Guadeloupe', 
		'972': 'Martinique', 
		'973': 'Guyane', 
		'974': 'La Réunion', 
		'976': 'Mayotte',
	}
	
	# remplacement pour les départements de la Corse
	df['dep'] = df['dep'].replace(201,'2A0')
	df['dep'] = df['dep'].replace(202,'2B0')

	# formattage de la colonne 'dep'
	df['dep'] = df['dep'].astype('str')
	df['dep'] = df['dep'].apply(lambda x:x[:-1] if x[-1] == '0' else x)
	df['dep'] = df['dep'].apply(lambda x:x.zfill(2) if len(x) < 2 else x)
	
	# ajout de la colonne 'departement'
	for No, Dep in DEPARTEMENTS.items():
		df.loc[df.dep == No,'departement'] = Dep
    
	# ajout de la colonne 'region'
	for region, deps in REGIONS.items():
		df.loc[(df['dep'].isin(deps)), 'region'] = region
	
	# extraction des colonnes 'grav','lat','long'
	df = df[['Num_Acc','grav','lat','long','region','departement']]

	# suppression des Nan's
	df.dropna()

	# conversion en 'float64'
	df['long'] = pd.to_numeric(df['long'], errors='coerce')

	# conversion du CRS en mercator
	k = 6378137
	df["x"] = (df['long'] / 100000)* (k * np.pi / 180.0)
	df["y"] = np.log(np.tan((90 + df['lat']/100000) * np.pi / 360.0)) * k

	# suppression des Nan's
	df = df.dropna()

	# conversion de 'Num_Acc' et 'grav' en 'str'
	df['Num_Acc'] = df['Num_Acc'].astype('str')
	df['grav'] = df['grav'].astype('str')
	
	return df

df = preprocess()

# sidebar
st.sidebar.header('Outils')
st.sidebar.markdown("__Choix de l'année__")
année = st.sidebar.selectbox(
    'Année',
     np.arange(2005,2018,1)
     )
région = st.sidebar.selectbox(
    'Région',
     sorted(df['region'].unique())
     )
département = st.sidebar.selectbox(
	'Département',
	 sorted(df['departement'].unique())
	 )
     
"""
#### (France)
"""

# filtrage sur 'année'
df_ = df[df['Num_Acc'].str.startswith(str(année))]

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
		   title='(France) Accidents de la route par gravité ('+str(année)+')'
		   )

p.add_tile(tile_provider)

# source
geo_source_1 = ColumnDataSource(data=df_[df_['grav'] == '1'])
geo_source_2 = ColumnDataSource(data=df_[df_['grav'] == '2'])
geo_source_3 = ColumnDataSource(data=df_[df_['grav'] == '3'])
geo_source_4 = ColumnDataSource(data=df_[df_['grav'] == '4'])

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

"""
#### (Par Région)
"""

# filtrage sur 'année'
df_ = df[df['Num_Acc'].str.startswith(str(année))]

# chargement du fond de carte
tile_provider = get_provider(OSM)

# boîte à outils
tools = "pan,wheel_zoom,box_zoom,reset"

# Création de la figure

f = figure(x_range=(-1000000, 2000000), y_range=(5000000, 7000000),
		   x_axis_type="mercator", y_axis_type="mercator",
		   tools=tools,
		   plot_width=800,
		   plot_height=600,
		   title='('+str(région)+') Accidents de la route par gravité ('+str(année)+')'
		   )

f.add_tile(tile_provider)

# source
geo_source_5 = ColumnDataSource(data=df_[(df_['grav'] == '1') & (df_['region'] == région)])
geo_source_6 = ColumnDataSource(data=df_[(df_['grav'] == '2') & (df_['region'] == région)])
geo_source_7 = ColumnDataSource(data=df_[(df_['grav'] == '3') & (df_['region'] == région)])
geo_source_8 = ColumnDataSource(data=df_[(df_['grav'] == '4') & (df_['region'] == région)])

# points
f1 = f.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_5, color='green', legend_label='Indemne')
f2 = f.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_6, color='red', legend_label='Tué')
f3 = f.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_7, color='orange', legend_label='Blessé hospitalisé')
f4 = f.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_8, color='yellow', legend_label='Blessé léger')


# paramètres de la figure
f.xgrid.grid_line_color = None
f.ygrid.grid_line_color = None
f.xaxis.major_label_text_color = None
f.yaxis.major_label_text_color = None
f.xaxis.major_tick_line_color = None  
f.xaxis.minor_tick_line_color = None  
f.yaxis.major_tick_line_color = None  
f.yaxis.minor_tick_line_color = None  
f.yaxis.axis_line_color = None
f.xaxis.axis_line_color = None
f.legend.label_text_font_size = "9pt"
f.legend.click_policy = "hide" 

st.bokeh_chart(f)

"""
#### (Par Département)
"""

# filtrage sur 'année'
df_ = df[df['Num_Acc'].str.startswith(str(année))]

# chargement du fond de carte
tile_provider = get_provider(OSM)

# boîte à outils
tools = "pan,wheel_zoom,box_zoom,reset"

# Création de la figure

g = figure(x_range=(-1000000, 2000000), y_range=(5000000, 7000000),
		   x_axis_type="mercator", y_axis_type="mercator",
		   tools=tools,
		   plot_width=800,
		   plot_height=600,
		   title='('+str(département)+') Accidents de la route par gravité ('+str(année)+')'
		   )

g.add_tile(tile_provider)

# source
geo_source_9 = ColumnDataSource(data=df_[(df_['grav'] == '1') & (df_['departement'] == département)])
geo_source_10 = ColumnDataSource(data=df_[(df_['grav'] == '2') & (df_['departement'] == département)])
geo_source_11 = ColumnDataSource(data=df_[(df_['grav'] == '3') & (df_['departement'] == département)])
geo_source_12 = ColumnDataSource(data=df_[(df_['grav'] == '4') & (df_['departement'] == département)])

# points
g1 = g.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_9, color='green', legend_label='Indemne')
g2 = g.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_10, color='red', legend_label='Tué')
g3 = g.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_11, color='orange', legend_label='Blessé hospitalisé')
g4 = g.circle(x='x', y='y', size=5, alpha=0.3, source=geo_source_12, color='yellow', legend_label='Blessé léger')


# paramètres de la figure
g.xgrid.grid_line_color = None
g.ygrid.grid_line_color = None
g.xaxis.major_label_text_color = None
g.yaxis.major_label_text_color = None
g.xaxis.major_tick_line_color = None  
g.xaxis.minor_tick_line_color = None  
g.yaxis.major_tick_line_color = None  
g.yaxis.minor_tick_line_color = None  
g.yaxis.axis_line_color = None
g.xaxis.axis_line_color = None
g.legend.label_text_font_size = "9pt"
g.legend.click_policy = "hide" 

st.bokeh_chart(g)
