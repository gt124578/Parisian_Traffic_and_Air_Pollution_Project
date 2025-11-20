



## Modules



import sqlite3 as sq
import pandas as pd
import os
from pathlib import Path
from matplotlib import pyplot as plt
from datetime import *
import numpy as np
import time

np.set_printoptions(precision=5, suppress=True)        #permet d'enlever l'écriture scientifique



##Mise en place de la table sur laquelle on va travailler



Path(r'F:\TIPE\Programmes/tableur.db').touch()          #Accès à la base de données : tableur.db

path='F:\TIPE\Programmes/tableur.db'
connection=sq.connect(path)

cur=connection.cursor()


#tabdonnées est le nom de la table correspondant à tableur.db



##Fonction d'accès à la table tabdonnées


def SQL(a):
    cur.execute(a)
    return(cur.fetchall())



##Aménagement des données disponibles



def liste_date():                                      #créer une liste de tuple (dater,nombre de voitures)
    jour=date(2014, 1, 1)
    liste_jours=[]
    ind=0
    while jour.isoformat()!='2018-01-01':
        liste_jours.append((jour.isoformat(),int(SQL("select sum(q) from tabdonnées where t_1h like"+ " '" + jour.isoformat() + "%' ")[0][0])))
        jour+=timedelta(days=1)
        print(ind)
        ind+=1
    return(liste_jours)                                #temps de réalisation : "15h25m"

exec(open("F:\TIPE\Programmes/liste_jours.py").read()) #après avoir calculé liste_jours on l'inscrit dans un .py que l'on rappelle les fois d'aprés
                                                       #pour éviter de le recalculer


def jour_semaine(h):                                   #créer une liste de listes contenant des tuples (date,nombre de voitures) correspondant à leur
    lundi_liste=[]                                     #jour de la semaine
    mardi_liste=[]
    mercredi_liste=[]
    jeudi_liste=[]
    vendredi_liste=[]
    samedi_liste=[]
    dimanche_liste=[]
    for i in range(0,len(h)):
        jour=date.fromisoformat(h[i][0]).weekday()
        if jour==0:
            lundi_liste.append(h[i])
        elif jour==1:
            mardi_liste.append(h[i])
        elif jour==2:
            mercredi_liste.append(h[i])
        elif jour==3:
            jeudi_liste.append(h[i])
        elif jour==4:
            vendredi_liste.append(h[i])
        elif jour==5:
            samedi_liste.append(h[i])
        elif jour==6:
            dimanche_liste.append(h[i])
    return([lundi_liste,mardi_liste,mercredi_liste,jeudi_liste,vendredi_liste,samedi_liste,dimanche_liste])

liste_semaine=jour_semaine(liste_jours)



##Création d'un graphique pour chaque jour de la semaine au cours de 4 années



def semaine_du_jour(z):                                 #permet de savoir à quelle semaine de l'année ce jour appartient
    smdj=[]
    for i in range(0,len(z)):
        smdj.append((date.fromisoformat(z[i][0]).isocalendar().week,z[i][1]))
    return(smdj)



def litteraljour(a):                                    #converti 0 à 6 littéralement en jour de la semaine
    t=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
    return(t[a])



def decimaljour(a):                                     #fait l'opposé de la fonction précédente
    t=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
    return(t.index(a))


def trace(Jour_litteral):                               #permet de tracer le graphique voulu en fonction du jour de la semaine sélectionné
    a=decimaljour(Jour_litteral)
    coord1=np.array(semaine_du_jour(liste_semaine[a]))
    fig = plt.figure("Les"+" "+litteraljour(a)+" sur l'année'")
    plt.scatter(coord1[:, 0], coord1[:, 1])
    plt.show()



##Création d'un graphique en fonction de la médiane du nombre de voitures de chaque semaine de l'année



def coord():                                             #permet de fusionner les listes contenant les jours respectifs de la semaine
    coordtot=[]
    for i in range(0,7):
        coordtot+=semaine_du_jour(liste_semaine[i])
    return(coordtot)



def amedian():                                           #permet de faire la médian de chaque semaine de l'année
    coordtot=coord()
    coordtot2=np.array(coordtot)
    lsem=list(coordtot2[:, 0])
    amedian=[]
    for i in range(1,53):
        lindex=[]
        lnb=[]
        if i==1:
            lindex=[index for index, value in enumerate(lsem) if value == 1]+[index for index, value in enumerate(lsem) if value == 53]
        else:
            lindex=[index for index, value in enumerate(lsem) if value == i]
        for j in range(0,len(lindex)):
            lnb.append(coordtot[lindex[j]][1])
        amedian.append((i,np.median(lnb)))
    return(amedian)

amedian=amedian()
amedian2=np.array(amedian)



fig = plt.figure("Les semaines au cours de l'année'")    #permet de tracer le graphique souhaité
plt.scatter(amedian2[:, 0], amedian2[:, 1])
plt.show()



##Création d'un graphique en fonction de la médiane de chaque jour



def smedian():                                           #effectue la médiane de chaque jour de la semaine sur 4 ans
    smedian=[]
    for i in range(0,7):
        smedian.append((i+1,np.median(np.array(semaine_du_jour(liste_semaine[i]))[:, 1])))
    return(smedian)

smedian=smedian()
smedian2=np.array(smedian)



fig = plt.figure("La semaine médiane")                   #trace le graphique réprésentant la médiane du nombre de voitures de chaque jour de la semaine
plt.scatter(smedian2[:, 0], smedian2[:, 1])
plt.show()



## FIN 1ere partie
