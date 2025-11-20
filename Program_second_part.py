




## Modules



import sqlite3 as sq
import pandas as pd
import time
import os
from pathlib import Path
import datetime
import statistics
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import inconsistent
from scipy.cluster.hierarchy import fcluster
from sklearn.cluster import MiniBatchKMeans as mbkm
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from matplotlib.patches import Ellipse
import folium
from geopy.geocoders import Nominatim
import time
from pprint import pprint
import osmnx as ox
import networkx as nx

np.set_printoptions(precision=5, suppress=True)                                         #permet d'enlever l'écriture scientifique



##Mise en place de la table sur laquelle on va travailler



Path(r'F:\TIPE\Programmes/tableur.db').touch()                                          #Accès à la base de données : tableur.db

path='F:\TIPE\Programmes/tableur.db'
connection=sq.connect(path)

cur=connection.cursor()


#tabdonnées est le nom de la table correspondant à tableur.db



##Fonction d'accès à la table tabdonnées


def SQL(a):
    cur.execute(a)
    return(cur.fetchall())



##Aménagement des données disponibles



nom_rues=SQL("SELECT DISTINCT libelle from tabdonnées where q<>'None'")                #liste (de tuple) regroupant chaque nom de rues pour les rues ayant un trafic connu
def libelle1():                                                                        #programme transformant nom_rues en liste (de caractères)
    g=[]
    for i in range(0,len(nom_rues)):
        print("libelle : ",str(i)+"/"+str(len(nom_rues)-1))                            #avancement du programme
        g.append(nom_rues[i][0])
    return(g)

liste_rues=libelle1()

def aposte(g):                                                                         #programme supprimant les apostrophes dans les noms de rues (problématique pour le traitement de données)
    for i in range (0,len(g)):
        print("aposte : ",str(i)+"/"+str(len(g)-1))                                    #avancement du programme
        for j in range (0,len(g[i])):
            if g[i][j]=="'":
                o=list(tuple(g[i]))
                o[j]="_"
                g[i]="".join(o)
    return(g)

liste_rues2=aposte(liste_rues)


z=[]
def VR2(depart,z):                                                                     #programme donnant le nombre totales de voitures ayant circulé par rues sur 4 ans
                                                                                       # (type tuple : (identifiant de la rues (iu_ac), nombre de voitures))
    try :
        for i in range (depart,len(liste_rues2)):
            var=i                                                                      #avancement du programme
            print("VR2 : ",str(i)+"/"+str(len(liste_rues2)-1))
            z.append(SQL("SELECT distinct iu_ac from tabdonnées where libelle like '"+liste_rues2[i]+"'")+SQL("SELECT SUM(q) from tabdonnées where libelle like '"+liste_rues2[i]+"'"))
    except :
        from odf import opendocument, text, teletype                                   #sauvegarde du resultat dans un document .odt si il y a un souci
        import sys
        from odf.opendocument import OpenDocumentText
        from odf.style import Style, TextProperties
        from odf.text import H, P, Span
        sys.path.insert(0,"E:/TIPE/Programmes")
        textdoc = opendocument.load(u"E:/TIPE/Programmes/Value.odt")
        texts = textdoc.getElementsByType(text.P)
        ustyle = Style(name="Underline", family="text")
        uprop = TextProperties(color='#000000')
        ustyle.addElement(uprop)
        textdoc.automaticstyles.addElement(ustyle)
        t=P(text="")
        t.addElement(Span(stylename=ustyle, text=z))
        texts[0].parentNode.insertBefore(t,texts[0])
        texts[0].parentNode.removeChild(texts[0])
        textdoc.save("E:/TIPE/Programmes/Value"+str(4)+".odt")
    return(z) #nb de voitures totales par rue

VR2=VR2(0,z) #temps de réalisation : "3j3h50m37s"

exec(open("F:\TIPE\Programmes/Valeur VR4.py").read())                                  #après avoir calculé VR2 on l'inscrit dans un .py que l'on rappelle les fois d'aprés
                                                                                       #pour éviter de recalculer VR2



## Pré-traitement (clustering)



def extract(list):                                                                     #extrait les iu_ac (identifiants) de chaque rues
    y=[]
    for i in range(0,len(list)):
        y.append(list[i][0])
    return(y)

VR20=extract(VR2)

def new_ref(list):                                                                     #permet de créer une nouvelle référence (0 à 610) pour chaque rue (liste de tuple de la forme (référence, nom))
    u=[]
    t0=time.time()
    try :
        for i in range(0,len(list)):
            print("new_ref.chargement : ",str(i)+"/"+str(len(list)-1),time.time()-t0)  #avancement du programme
            u.append(tuple([i])+SQL("select distinct libelle from tabdonnées where iu_ac="+str(list[i]))[0])
    except :
        from odf import opendocument, text, teletype
        import sys
        from odf.opendocument import OpenDocumentText
        from odf.style import Style, TextProperties
        from odf.text import H, P, Span
        sys.path.insert(0,"E:/TIPE/Programmes")
        textdoc = opendocument.load(u"E:/TIPE/Programmes/Value.odt")
        texts = textdoc.getElementsByType(text.P)
        ustyle = Style(name="Underline", family="text")
        uprop = TextProperties(color='#000000')
        ustyle.addElement(uprop)
        textdoc.automaticstyles.addElement(ustyle)
        t=P(text="")
        t.addElement(Span(stylename=ustyle, text=id_lib))
        texts[0].parentNode.insertBefore(t,texts[0])
        texts[0].parentNode.removeChild(texts[0])
        textdoc.save("E:/TIPE/Programmes/id_lib.odt")
    return(u)

id_lib=new_ref(VR20) #temps de réalisation : "1j8h24m32s"

exec(open("F:\TIPE\Programmes/id_lib.py").read())                                       #même idée que pour VR2


def VR2_new_ref(list):                                                                  #liste de tuple de la forme (nouvelle référence, nombre de voitures)
    y=[]
    for i in range(0,len(list)):
        y.append(tuple([i])+tuple([list[i][1]]))
    return(y)

VR2_2=VR2_new_ref(VR2)



conn3 = sq.connect('F:\TIPE\Programmes/tabVRIII.db')                                    #utilisation d'une nouvelle table nommé tab_VRIII pour un accès plus efficient par la suite7
cur3 = conn3.cursor()

cur3.execute('''CREATE TABLE IF NOT EXISTS tab_VRIII(rues,nb_voitures)''')

def insert_into(liste):                                                                 #cette nouvelle table va contenir VR2_2
    sql = "INSERT INTO tab_VRIII(rues,nb_voitures) VALUES (?, ?)"
    cur3.executemany(sql, liste)
    conn3.commit()
    cur3.close()
    conn3.close()

insert_into(VR2_2)



##Clustering



conn3 = sq.connect('F:\TIPE\Programmes/tabVRIII.db')                                    #réouverture de la table tab_VRIII contenant maintenant VR2_2
cur3 = conn3.cursor()

cur3.execute('''CREATE TABLE IF NOT EXISTS tab_VRIII(rues,nb_voitures)''')


def SQL3(a):                                                                            #commande pour accéder à la table
    cur3.execute(a)
    return(cur3.fetchall())



VR2_3=SQL3("SELECT rues,nb_voitures from tab_VRIII")

X=np.array(VR2_3)
print(X.shape)   # 611 échantillons en 2 dimensions
plt.figure(0)
plt.scatter(X[:, 0], X[:, 1])
plt.show()                                                                              #on trace un graphique nombre de voitures en fonction de la rue



kmeans = KMeans(2, random_state=0)                                                      #on utilise la méthode des kmeans pour déterminer les rues où le passage est très important
labels1 = kmeans.fit(X).predict(X)
fig = plt.figure(1)
fig.suptitle('Clustering by KMeans', fontsize=16)
plt.scatter(X[:, 0], X[:, 1], c=labels1, s=40, cmap='viridis');
plt.show()                                                                              #on trace un graphique nombre de voitures en fonction de la rue



##défition de la liste de tuples (rue,couleur) associés via clustering



def rues_en_couleurs():                                                                 #créer une liste de tuples (référence de la rues, couleur)
    rues=SQL3("SELECT rues from tab_VRIII")
    rues_couleurs=[]
    for i in range (0,len(rues)):
        print("rues/couleurs.chargement : ",str(i)+"/"+str(len(rues)-1))
        rues_couleurs.append(tuple([rues[i][0]]+[list(labels1)[i]]))                    #label1 est un tableau regroupant les couleur de chaque point
                                                                                        #le 0 représente la couleur (dominante) des rues à faible densité et 1 représente la couleur des autres rues
    return(rues_couleurs)

rues_couleurs=rues_en_couleurs()


def libelle(liste):                                                                     #permet de récuperer le nom d'une rue en s'appuyant sur id_lib
    g=[]
    for i in range(0,len(liste)):
        g.append(liste[i][1])
    return(g)


def correction_libelle(liste,i):                                                        #permet de recorriger le nom d'une rue une nouvelle fois si celle-ci n'est pas reconnu (cas particulier)
    p=libelle(liste)
    j=0
    while p[i][j]!="_":
        oh=list(tuple(p[i]))                                                            #permet de créer une liste de longueur n contenant les n caractères d'un mot de longueur n
        oh[j]="_"
        p[i]="".join(oh)
        j+=1
    return(p[i])


e=list(labels1)
def compter_couleurs():                                                                 #compte le nombre de rues ayant une circulation dense et celles ayant une circulation passable
    nb_dense=0
    nb_moyen=0
    for i in range (0,len(e)):
        if e[i]==1:
            nb_dense+=1
        elif e[i]==0:
            nb_moyen+=1
    return(nb_dense,nb_moyen)



##différentiation des données en fonction de la circulation



def rues_denses(d):                                                                      #création d'une liste (de tuple (référence, nom de la rue)) contenant les rues à forte circulation
    r=[]
    for i in range (0,len(d)):
        print("rues_denses.chargement : ",str(i)+"/"+str(len(d)-1))
        if d[i][1]==1:
            r.append(id_lib[i])
    return(r)


ref_rues_denses=rues_denses(rues_couleurs)




def rues_claires(d):                                                                     #même chose pour les rues où il y a peu de circulation
    r=[]
    for i in range (0,len(d)):
        print("rues_claires.chargement : ",str(i)+"/"+str(len(d)-1))
        if d[i][1]==0:
            r.append(id_lib[i])
    return(r)


ref_rues_claires=rues_claires(rues_couleurs)



## Transcription de chaque rue en coordonnées GPS



app = Nominatim(user_agent="tutorial")

def coord_gps_rd():                                                                     #création de la liste des coordonnées gps des rues à forte circulation
    coord_gps=[]
    for i in range (0,len(ref_rues_denses)):
        print("coord_gps_rd.chargement : ",str(i)+"/"+str(len(ref_rues_denses)-1))      #avancement du programme
        try:
            location = app.geocode(ref_rues_denses[i][1]+", Paris").raw                 #la difficulté est de faire en sorte que le module reconnaisse la rue et renvoi les coordonnées
        except:                                                                         #on tente de corriger le libelle de la rue si cela ne marche pas
            try:
                location = app.geocode(correction_libelle(ref_rues_denses,i)+", Paris").raw
            except:                                                                     #si cela ne marche pas on signale le problème et on continue
                print("problème avec",ref_rues_denses[i][1])
        coord_gps.append(tuple([float(location['boundingbox'][0])]+[float(location['boundingbox'][1])]+[float(location['boundingbox'][2])]+[float(location['boundingbox'][3])]+[location['display_name']]))                                                            #on créer alors un liste de tuple (coordonnées gps, nom de la rue données par le gps)
    return(coord_gps)


coord_gps_rd=coord_gps_rd()



## Création de la carte (où les rues ayant un fort trafic sont tracées en rouges)



ox.config(log_console=True, use_cache=True)

def dessin_de_la_carte():
        print("Initialisation (Création de la carte de Paris)")
        G = ox.graph_from_place("Paris,France",network_type='drive')
        graph_map1 = ox.plot_graph_folium(G, graph_map=None,                           #on colorie toutes les rues intramuros de Paris en bleu
                                                    popup_attribute=None,
                                                    tiles='cartodbpositron',
                                                    zoom=19,
                                                    fit_bounds=True,
                                                    edge_color='#00ccff',
                                                    edge_width=2,
                                                    edge_opacity=.3)
        graph_map1.save('F:\TIPE\Résultats/Paris.html')                                #on sauvegarde cette carte
        for i in range(0,len(coord_gps_rd)):
            print("dessin_de_la_carte : ",str(i)+"/"+str(len(coord_gps_rd)-1))         #avancement du programme
            G1 = ox.graph_from_point((coord_gps_rd[i][0],coord_gps_rd[i][3]), dist=200, network_type='drive',truncate_by_edge=True, clean_periphery=True)
            graph_map1 = ox.plot_graph_folium(G1, graph_map=graph_map1,                #on trace sur la carte créée précédemment les rues à fort trafic en rouge
                                                        popup_attribute=None,
                                                        tiles='cartodbpositron',
                                                        zoom=19,
                                                        fit_bounds=True,
                                                        edge_color='#ff0000',
                                                        edge_width=2,
                                                        edge_opacity=1)
            graph_map1.save(r'F:\TIPE\Résultats/Carte_Paris_Finale.html')              #on sauvegarde la carte
        return("Carte Créée")                                                          #il ne reste que plus consulter le fichier pour voir le résultat



## FIN 2de partie




