# Code créée par la AlexisCorp


# Importation des differents modules

import re
import pandas as pd
from Classes import Author
import string
from collections import Counter
import numpy as np

# Importation des differentes Classes
from Classes import ArxivDocument
from Classes import RedditDocument



# Defnitions de patrons

def singleton(cls):

    instance = [None]

    def wrapper(*args, **kwargs):

        if instance[0] is None:

            instance[0] = cls(*args,**kwargs)

        return instance[0]

    return wrapper

        
class generatorofparticules:

    @staticmethod

    def factory(type, nom):         # Polymorphisme de classe

        if type == "Arxiv": return ArxivDocument(nom)       # Renvoie vers la classe ArxivDocument 

        if type == "Reddit": return RedditDocument(nom)     # Renvoie vers la classe RedditDocument

        assert 0, "Error 404" + type


# ===============  CLASSE CORPUS ===============

@singleton #Patron de conception

class Corpus:

    def __init__(self, nom):

        self.nom = nom      # Nom

        self.authors = {}   # Auteurs

        self.aut2id = {}    # Id d'auteur

        self.id2doc = {}    # Id du document

        self.ndoc = 0       # Nombre de documents

        self.naut = 0       # Nombre d'autheur

        self.all_documents_text = ""        # Regroupement de tout les textes
        
        self.vocabulary = set()     # Vocabulaire du corpus sous set
        

# ============ Fonction ADD d'ajout des documents ============
        
    def add(self, doc):

        if doc.auteur not in self.aut2id:

            self.naut += 1

            self.authors[self.naut] = Author(doc.auteur)

            self.aut2id[doc.auteur] = self.naut

        self.authors[self.aut2id[doc.auteur]].add(doc.texte)
        
        self.all_documents_text += doc.texte + " "

        self.ndoc += 1

        self.id2doc[self.ndoc] = doc



# ===============  REPRESENTATION ===============

    def show(self, n_docs=-1, tri="abc"):

        docs = list(self.id2doc.values())

        if tri == "abc":  # Tri alphabétique

            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]

        elif tri == "123":  # Tri temporel

            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))


    def __repr__(self):

        docs = list(self.id2doc.values())

        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

    
# ===============  SPECIFICITE ===============


# ============ Fonction SEARCH pour trouver les mots dans leur contexte ============

    def search(self, keyword):
        
        # Utilise les expressions regulieres pour trouver les passages des mots
        
        matches = re.finditer(r'\b' + re.escape(keyword) + r'\b', self.all_documents_text, flags=re.IGNORECASE)

        # Collecter les passages
        
        passages = []
        
        context_window = 15  # Ajuster la taille de la fenetre de contexte
        
        for match in matches:
            
            start_index = max(0, match.start() - context_window)
            
            end_index = min(len(self.all_documents_text), match.end() + context_window)
            
            passage = self.all_documents_text[start_index:end_index]
            
            passages.append(passage)

        return passages

    
# ============ Fonction CONCORDE pour trouver les mots dans leur contexte predefini ============

    def concorde(self, expression, context_size):
        
        # Utilise les expressions regulieres pour trouver les passages des mots
        
        matches = re.finditer(expression, self.all_documents_text, flags=re.IGNORECASE)

       # Collecter les passages
    
        concordances = []
        
        for match in matches:
            
            start_index = max(0, match.start() - context_size)
            
            end_index = min(len(self.all_documents_text), match.end() + context_size)
            
            conc_left = self.all_documents_text[start_index:match.start()]
            
            conc_right = self.all_documents_text[match.end():end_index]
            
            concordance = {
                
                'contexte_gauche': conc_left,
                
                'motif_trouvé': match.group(),
                
                'contexte_droit': conc_right
                
            }
            
            concordances.append(concordance)

        # Convertir en DataFrame
        
        concordances_df = pd.DataFrame(concordances)
        
        return concordances_df

    
# ============ Fonction NETTOYER_TEXTE pour nettoyer le texte en parametre ============

    def nettoyer_texte(self, texte):
  

        cleaned_text = texte.lower()  # Convertir en minuscule
    
        cleaned_text = re.sub(r'\n', ' ', cleaned_text)     # Remplace les nouvelles lignes par des espaces
        
        cleaned_text = re.sub(r'\d+', ' ', cleaned_text)    # Remplace les chiffres par des espaces
        
        cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)# Remplace les ponctuations par des espaces
        
        return cleaned_text

# ============ Fonction CONSTRUIRE_VOCABULAIRE pour la creation du vocabulaire du corpus ============

    def construire_vocabulaire(self):
        
        for id, doc in self.id2doc.items():
            
            cleaned_text = self.nettoyer_texte(doc.texte)    # Appel de la fonction nettoyer_texte
            
            words = re.split(r'[\s,;.:!?\-"\']+', cleaned_text)    # Tokenization
            
            self.vocabulary.update(words)    # Mise à jour du vocabulaire 
            







#   Code créée par la AlexisCorp pour le AlexisCorp Search# Correction de G. Poux-Médard, 2021-2022

import re

from Classes import Author

from Classes import ArxivDocument

from Classes import RedditDocument

def singleton(cls):

    instance = [None]

    def wrapper(*args, **kwargs):

        if instance[0] is None:

            instance[0] = cls(*args,**kwargs)

        return instance[0]

    return wrapper

        

class generatorofparticules:



    @staticmethod

    def factory(type, nom):

        if type == "Arxiv": return ArxivDocument(nom)

        if type == "Reddit": return RedditDocument(nom)

        assert 0, "Error 404" + type







# =============== 2.7 : CLASSE CORPUS ===============

@singleton

class Corpus:

    def __init__(self, nom):

        self.nom = nom

        self.authors = {}

        self.aut2id = {}

        self.id2doc = {}

        self.ndoc = 0

        self.naut = 0



    def add(self, doc):

        if doc.auteur not in self.aut2id:

            self.naut += 1

            self.authors[self.naut] = Author(doc.auteur)

            self.aut2id[doc.auteur] = self.naut

        self.authors[self.aut2id[doc.auteur]].add(doc.texte)



        self.ndoc += 1

        self.id2doc[self.ndoc] = doc



# =============== 2.8 : REPRESENTATION ===============

    def show(self, n_docs=-1, tri="abc"):

        docs = list(self.id2doc.values())

        if tri == "abc":  # Tri alphabétique

            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]

        elif tri == "123":  # Tri temporel

            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]



        print("\n".join(list(map(repr, docs))))



    def __repr__(self):

        docs = list(self.id2doc.values())

        docs = list(sorted(docs, key=lambda x: x.titre.lower()))



        return "\n".join(list(map(str, docs)))
