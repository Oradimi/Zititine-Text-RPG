##### IMPORTATIONS #####

import cmd
import sys
import os
import time
from random import randint
from enum import Enum
from copy import deepcopy

"""from pygame import mixer # Load the required library
mixer.init()
mixer.music.load('D:/Users/Logan/Desktop/STUFF LOGAN/Music/Kancolle Event OST (CD version)/001. 全艦娘、突撃！.wav')
mixer.music.play()"""

screen_width = 100
fail = False #variable
clear = False #variable

########################
##### SETUP OBJETS #####
########################

class Item:
	"""Un objet quelconque avec un nom.
	"""
	def __init__(self, name):
		self.name = name

#====> Setup équipements

class Equipment:
	"""Les équipements avec un nom peuvent augmenter :
	> attaque, armure, agilité
	"""
	def __init__(self, name, atk, arm, agi):
		self.name = name
		self.atk = atk
		self.arm = arm
		self.agi = agi
#====> Liste des équipements
"""Les différents équipements du jeu sont rassemblés dans des catégories,
   et chacune est une liste avec plusieurs objets listés, avec :
   > nom, attaque, armure, agilité
"""
helmets = [Equipment("Cheveux", 0, 0, 20),
           Equipment("Casque en cuir", 0, 1, 18),
           Equipment("Casque en fer", 0, 2, 14),
           Equipment("Casque en acier", 0, 3, 10),
           Equipment("Couronne mystique", 1, 2, 16)]

armors = [Equipment("Vêtements rapiécés", 0, 0, 30),
          Equipment("Armure en cuir", 0, 1, 27),
          Equipment("Armure en fer", 0, 3, 18),
          Equipment("Armure en acier", 0, 4, 12),
          Equipment("Robe mystique", 1, 2, 21)]

boots = [Equipment("Vieux souliers troués", 0, 0, 0),
         Equipment("Bottes en cuir", 0, 0, 5),
         Equipment("Bottes en fer", 0, 1, 0),
         Equipment("Bottes confortables", 0, 0, 10),
         Equipment("Chaussures nuage", 1, 0, 20)]

swords = [Equipment("Petite dague rouillée", 2, 0, 5),
          Equipment("Épée en bois", 3, 0, 2),
          Equipment("Épée en fer", 5, 0, 0),
          Equipment("Espadon en acier", 7, 0, -5),
          Equipment("Épée de légende", 5, 0, 5)]

shields = [Equipment("Couvercle de tonneau", 0, 2, 0),
           Equipment("Bouclier en cuivre", 0, 3, 0),
           Equipment("Bouclier en fer", 0, 4, 0),
           Equipment("Grand bouclier", 0, 6, -5),
           Equipment("Bouclier magique", 0, 5, 0)]

#====> Setup objets

class Consummable(Item):
	"""Les consommables avec un nom et une durée peuvent augmenter ou régénérer :
	> attaque, armure, agilité, PVs, PVs max
	"""
	def __init__(self, name, atk, arm, agi, hp, hpmax, duration):
		self.name = name
		self.atk = atk
		self.arm = arm
		self.agi = agi
		self.hp = hp
		self.hpmax = hpmax
		self.duration = duration
	
	def use(player, item): #fonction d'utilisation d'un consommable
		player.hpmax += item.hpmax #ajoute des PVs max
		player.hp += item.hp #régénère des PVs
		if player.hp > player.hpmax:
			player.hp = player.hpmax #si les PVs régénérés excèdent les PVs max, réduire les PVs aux PVs max
		if item.duration > 0: #si le consommable a une durée
			player.effects.append(deepcopy(item)) #ajouter le consommable dans la liste de buffs du joueur
		
"""Les différents objets du jeu sont rassemblés dans des catégories,
   et chacune est une liste avec plusieurs objets listés, avec :
   > nom, attaque, armure, agilité, PVs, PVs max, durabilité
"""
objects = [Consummable("Miche de pain", 0, 0, 0, 3, 0, 0),
		   Consummable("Potion de vitalité", 1, 0, 5, 15, 5, 2),
		   Consummable("Grand verre d'eau", 0, 0, 10, 1, 0, 3),
		   Consummable("Jus d'orange concentré", 2, 0, 0, 0, 0, 4),
		   Consummable("Rempart magique", 0, 4, -20, 0, 0, 3),
		   Consummable("Potion qui brille fort", 3, 3, 15, 5, 5, 2)]

#====> Setup inventaire

class Inventory:
	"""L'inventaire avec les objets à l'intérieur, et des fonctions pour le gérer
	"""
	def __init__(self):
		self.slots = [deepcopy(objects[0]), deepcopy(objects[0])] #Deux miches de pain dans l'inventaire, indépendantes

	def item_check(self, notice, action): #fonction qui cherche un objet pour le supprimer de l'inventaire
		print("\nVoici les objets présents dans votre inventaire :")
		for i in range(0, len(self.slots)): #pour tous les objets de l'inventaire
			print(" -", str(self.slots[i].name), "(Atq+:", str(self.slots[i].atk),
			"; Def+:", str(self.slots[i].arm), "; Agi+:", str(self.slots[i].agi), "; PV+:", str(self.slots[i].hp),
			"; PVmax+:", str(self.slots[i].hpmax), "; Durée:", str(self.slots[i].duration), "tours)") #affiche les objets du joueur sous forme de jolie liste
		found = False
		while found == False:
			choice = input(notice)
			check = -1 #vérifie la correspondance de la chose entrée avant avec un objet de l'inventaire
			found = False #indique si l'objet a été trouvé ou non
			while check < (len(self.slots) - 1) and found == False:
				check += 1
				if self.slots[check].name.lower() == choice.lower():
					found = True
					item = self.slots[check]
					action(player, item)
					self.slots.pop(check)
					return True
			if found == False and choice != "annuler" or found == False and action == do_nothing:
				print("\nNom d'objet invalide.")
			elif choice == "annuler" and action != do_nothing:
				found = True
				return False

	def add_item(self, Item): #ajoute un objet dans l'inventaire
		input(Item.name + " obtenu !")
		if len(self.slots) >= 5:
			self.item_check("\nVous n'avez plus de place dans votre inventaire.\nQue jetez-vous ?\n> ", do_nothing)
		self.slots.append(deepcopy(Item))

	def select_item(self):
		if len(self.slots) == 0:
			print("\nVotre inventaire est vide.")
			return False
		else:
			item_chosen = self.item_check("\nEntrez le nom de l'objet que vous souhaitez utiliser (entrez 'annuler' pour annuler) :\n> ", Consummable.use)
			if item_chosen == False:
				return False
			else:
				return True

player_inv = Inventory()

def do_nothing(Player, item): #fonction qui ne fait rien (si si c'est utile)
	pass

#########################
##### SETUP ENTITÉS #####
#########################

class Being:
	"""Un être quelconque :
	> nom, attaque, armure, PVs, PVs max
	"""
	def __init__(self, name, atk, arm, hp, hpmax):
		self.name = name
		self.atk = atk
		self.arm = arm
		self.hp = hp
		self.hpmax = hpmax

#====> Setup joueur

class Player(Being):
	"""Le joueur avec tous ses attributs initiaux :
	> nom, attaque, armure, agilité, PVs, PVs max
	> casque, armure, bottes, épée, bouclier
	> buffs, position
	"""
	def __init__(self):
		self.name = ""
		self.atk = 0 #attaque
		self.arm = 0 #défense
		self.agi = 0 #agilité
		self.hp = 20 #PVs
		self.hpmax = 20 #PVs maximum, ne peuvent pas excéder cette valeur
		self.helmet = helmets[0] #il s'agit du premier casque du jeu
		self.armor = armors[0] #idem, mais l'armure, etc.
		self.boot = boots[0]
		self.sword = swords[0]
		self.shield = shields[0]
		self.effects = []
		self.pos = None #position dans le monde, le nom du lieu

	def print_equip(self): #montre au joueur la liste de ses équipements avec leurs stats
		print("\nÉquipement actuel :")
		print(" -", self.helmet.name, "(Atq:", self.helmet.atk, "; Def:", self.helmet.arm, "; Agi:", self.helmet.agi, ")")
		print(" -", self.armor.name, "(Atq:", self.armor.atk, "; Def:", self.armor.arm, "; Agi:", self.armor.agi, ")")
		print(" -", self.boot.name, "(Atq:", self.boot.atk, "; Def:", self.boot.arm, "; Agi:", self.boot.agi, ")")
		print(" -", self.sword.name, "(Atq:", self.sword.atk, "; Def:", self.sword.arm, "; Agi:", self.sword.agi, ")")
		print(" -", self.shield.name, "(Atq:", self.shield.atk, "; Def:", self.shield.arm, "; Agi:", self.shield.agi, ")")

	def get_stat(self, stat):
		"""Fonction pour récupérer les stats du joueur avec les bonus de tous ses équipements :
		> son propre stat, et ceux fournis par son casque, son armure, ses bottes, son épée, son bouclier, ses buffs
		"""
		if stat == StatType.ATK: #si la fonction demande récupérer les stats d'attaque
			equip_stat = self.atk + self.helmet.atk + self.armor.atk + self.boot.atk + self.sword.atk #stats des équipements
			buff = 0
			for i in range(0, len(self.effects)):
				buff += self.effects[i].atk #addition des stats des objets de buff
			return equip_stat + buff #renvoie l'attaque totale du joueur
		if stat == StatType.ARM: #même chose pour la défense
			equip_stat = self.arm + self.helmet.arm + self.armor.arm + self.boot.arm + self.sword.arm
			buff = 0
			for i in range(0, len(self.effects)):
				buff += self.effects[i].arm
			return equip_stat + buff
		if stat == StatType.AGI: #même chose pour l'agilité
			equip_stat = self.agi + self.helmet.agi + self.armor.agi + self.boot.agi + self.sword.agi
			buff = 0
			for i in range(0, len(self.effects)):
				buff += self.effects[i].agi
			return equip_stat + buff

	def add_equipment(self, type, equipment): #fonction qui ajoute un équipement au joueur
		ditch = "\nSouhaitez-vous jeter votre équipement contre ceci ?"
		print("\nVous devez remplacer et jeter votre équipement actuel pour équipper le nouveau.")
		self.print_equip() #montre au joueur la liste de ses équipements avec leurs stats
		def equip_ditch(type):
			print(ditch, equipment.name, "(Atq:", equipment.atk, "; Def:", equipment.arm, "; Agi:", equipment.agi, ")")
			choice = input("> ")
			if choice in ["oui", "ouais", "yup"]:
				setattr(self, type, equipment) #si oui, remplace l'équipement
				input("\nÉquipement remplacé !")
			elif choice in ["non", "nan", "nope"]:
				pass #sinon, ne fait rien
			else:
				print("\nEntrez une commande valide !")
				equip_ditch(type)
		equip_ditch(type)

	def check_buff(self): #fonction qui vérifie l'état des buffs
		for decrease in range(len(self.effects) - 1, -1, -1): #pour tous les buffs du joueur
			self.effects[decrease].duration -= 1 #réduire la durée
			if self.effects[decrease].duration <= 0:
				self.effects.pop(decrease) #si la durée atteint 0, supprimer le buff
	
	def status_display(self): #fonction qui montre le statut du joueur
		print("\nNom :", self.name) #nom du joueur
		print("PVs :", self.hp, "/", self.hpmax) #PVs du joueur
		print("Atq :", self.get_stat(StatType.ATK)) #attaque du joueur
		print("Def :", self.get_stat(StatType.ARM)) #défense du joueur
		print("Agi :", self.get_stat(StatType.AGI)) #agilité du joueur
		self.print_equip() #montre au joueur la liste de ses équipements avec leurs stats
		if len(self.effects) != False: #si la liste de buffs n'est pas vide
			print("\nObjets de buff actifs :")
			for show in range(0, len(self.effects)): #montrer les buffs actifs et leurs tours restants
				print(" -", self.effects[show].name, "(" + str(self.effects[show].duration) + " tours restants)")

player = Player()

#====> Setup ennemis

class Enemy(Being):
	"""Un ennemi, avec :
	> nom, attaque, armure, PVs, PVs max
	"""
	def __init__(self, name, atk, arm, hp, hpmax):
		Being.__init__(self, name, atk, arm, hp, hpmax) #L'ennemi reprend les mêmes attributs qu'un simple être
"""Les différents ennemis du jeu dans une liste, avec :
   > nom, attaque, armure, PVs, PVs max
"""
monsters = [Enemy("Feuille", 1.3, 0, 4, 4),
			Enemy("T-rex des eaux", 6, 2, 10, 10),
			Enemy("Serpent", 4, 1, 5, 5),
			Enemy("Énorme rat ", 4, 1, 8, 8),
			Enemy("Sbire de Zititine", 8, 2, 12, 12),
			Enemy("Zititine le pas cool", 13, 4, 25, 25)]

#====> Autre

class StatType(Enum): #permet d'avoir une liste des différents stats existants
	ATK = 1
	ARM = 2
	AGI = 3

#######################
##### SETUP CARTE #####
#######################
"""
 a1 | a2 | a3 | a4
---- ---- ---- ----
 b1 | b2 | b3 | b4
---- ---- ---- ----
 c1 | c2 | c3 | c4
---- ---- ---- ----
 d1 | d2 | d3 | d4
"""
#définition de constantes
DESCRIPTION = 'description'
EVENT = 'event'
UP = 'haut', 'devant'
DOWN = 'bas', 'derrière'
LEFT = 'gauche'
RIGHT = 'droite'

room_investigated = {'a1': False, 'a2': False, 'a3': False, 'a4': False,
                     'b1': False, 'b2': False, 'b3': False, 'b4': False,
                     'c1': False, 'c2': False, 'c3': False, 'c4': False,
                     'd1': False, 'd2': False, 'd3': False, 'd4': False
                    }

#je crée un dictionaire pour la carte, et à l'intérieur les cases avec leur description etc.
carte = {
	'a1': {
		DESCRIPTION: "\nVous êtes près d'un grand arbre avec une ombre imposante.", #description du lieu (nom, ce qu'on voit autour)
		EVENT: '\nOh mon dieu, une feuille !', #description de l'évenement sur cette case
		UP: 'a1', #case au dessus
		DOWN: 'b1', #case en dessous
		LEFT: 'a1', #case  à gauche
		RIGHT: 'a2', #case à droite
	},
	'a2': {
		DESCRIPTION: '\nAutour de vous, les herbes sont de plus en plus hautes.',
		EVENT: "\nVous croisez un marchant ambulant.\nComme il est très gentil et qu'il perçoit votre désir de vengeance, vous pouvez choisir un objet gratuitement.",
		UP: 'a2',
		DOWN: 'b2',
		LEFT: 'a1',
		RIGHT: 'a3',
	},
	'a3': {
		DESCRIPTION: '\nUne petite rivière se trouve près de vous.',
		EVENT: '\nCOUREZ ! UN T-REX DES EAUX !',
		UP: 'a3',
		DOWN: 'b3',
		LEFT: 'a2',
		RIGHT: 'a4',
	},
	'a4': {
		DESCRIPTION: '\nIl y a un grand arbre.',
		EVENT: '\nOh, une miche de pain au creux du végétal !',
		UP: 'a4',
		DOWN: 'b4',
		LEFT: 'a3',
		RIGHT: 'a4',
	},
	'b1': {
		DESCRIPTION: '\nVous entrez dans une forêt.',
		EVENT: '\nDes branches, mais également une paire de bottes !',
		UP: 'a1',
		DOWN: 'c1',
		LEFT: 'b1',
		RIGHT: 'b2',
	},
	'b2': {
		DESCRIPTION: '\nUn Oiseau passe au-dessus de votre tête et percute une branche avant de tomber au sol. Pas de chance.',
		EVENT: '\nAlors que vous levez la tête pour contempler le ciel en ces jours de malheur,\nvous sentez que vous venez de marcher sur quelque chose de vivant et entendez un sifflement strident, un Serpent !',
		UP: 'a2',
		DOWN: 'c2',
		LEFT: 'b1',
		RIGHT: 'b3',
	},
	'b3': {
		DESCRIPTION: '\nVous arrivez devant un panneau qui indique : Attention méchants.',
		EVENT: '\nVisiblement, rien à signaler.',
		UP: 'a3',
		DOWN: 'c3',
		LEFT: 'b2',
		RIGHT: 'b4',
	},
	'b4': {
		DESCRIPTION: '\nIl y a une grande fontaine.',
		EVENT: '\nVous vous approchez de la fontaine.',
		UP: 'a4',
		DOWN: 'c4',
		LEFT: 'b3',
		RIGHT: 'b4',
	},
	'c1': {
		DESCRIPTION: '\nVous débarquez sur un ancien champ de bataille.',
		EVENT: '\nAlors que vous investiguez, vous sentez votre jambe se faire tirer par un fil et soudain vous vous retrouvez projeté dans les airs.',
		UP: 'b1',
		DOWN: 'd1',
		LEFT: 'c1',
		RIGHT: 'c2',
	},
	'c2': {
		DESCRIPTION: '\nVous êtes dans une clairière jonchée de corps.',
		EVENT: '\nUn cadavre semble porter un truc brillant.',
		UP: 'b2',
		DOWN: 'd2',
		LEFT: 'c1',
		RIGHT: 'c3',
	},
	'c3': {
		DESCRIPTION: "\nVous entendez un ronflement sourd mais il n'y a aucun danger apparent à l'horizon.",
		EVENT: '\nVous trébuchez et réveillez ce qui grondait, un golem de pierre dormait sous vos pieds.',
		UP: 'b3',
		DOWN: 'd3',
		LEFT: 'c2',
		RIGHT: 'c4',
	},
	'c4': {
		DESCRIPTION: '\nIl semble y avoir un feu non loin.',
		EVENT: "\nVous réveillez un sbire du grand Zititine, vous allez passer un mauvais quart d'heure.",
		UP: 'b4',
		DOWN: 'd4',
		LEFT: 'c3',
		RIGHT: 'c4',
	},
	'd1': {
		DESCRIPTION: '\nVous arrivez dans un coin un peu sombre.',
		EVENT: '\nQuelque chose attire votre attention...',
		UP: 'c1',
		DOWN: 'd1',
		LEFT: 'd1',
		RIGHT: 'd2',
	},
	'd2': {
		DESCRIPTION: "\nVous passez devant une grotte mais vous n'avez pas envie d'y aller.",
		EVENT: "\nJ'avais dit que vous n'aviez pas envie bon sang !",
		UP: 'c2',
		DOWN: 'd2',
		LEFT: 'd1',
		RIGHT: 'd3',
	},
	'd3': {
		DESCRIPTION: '\nLa brise est douce mais le danger semble proche.',
		EVENT: "\nRien à signaler, pour l'instant. Vous trouvez cependant une jolie potion au sol.",
		UP: 'c3',
		DOWN: 'd3',
		LEFT: 'd2',
		RIGHT: 'd4',
	},
	'd4': {
		DESCRIPTION: '\nIl y une grande porte. Il est inscrit "Ici vit Zititine le Malfaisant Nuisible Délétère Pernicieux Pas Beau".',
		EVENT: '\nIl est temps de venger vos morts.',
		UP: 'c4',
		DOWN: 'd4',
		LEFT: 'd3',
		RIGHT: 'd4',
	}
}

#====> Fonctions carte

def prompt(): #demande au joueur ce qu'il veut faire
	print(carte[player.pos][DESCRIPTION]) #affiche la description du lieu
	choice = input("\nQue voulez-vous faire ?\n - chercher\n - se déplacer\n - inventaire\n - statut\n> ") #on lui demande ce qu'il veut faire
	choice = choice.lower() #met tout texte entré en minuscule
	while choice not in ["chercher", "cherche", "se deplacer", "se déplacer", "inventaire", "objets", "statut", "stats", "statistiques", "quitter"]:
		choice = input("\nEntrez un choix valide.\n> ") #affiche "Entrez un choix valide." si la saisie n'est pas bonne
		choice = choice.lower()
	if choice in ["chercher"]: #si le joueur cherche, enclenche l'évènement du lieu
		event()
	elif choice in ["se deplacer", "se déplacer", "deplacer", "déplacer"]: #si le joueur se déplace
		previous_pos = player.pos
		player.pos = move() #change sa position
		if previous_pos == player.pos: #vérifie si la position du joueur est la même que la précédente
			print("\nVous ne pouvez pas aller plus loin !")
		else:
			player.check_buff()
	elif choice in ["inventaire", "objets"]: #si le joueur choisit de consulter son inventaire
		player_inv.select_item() #accède au menu de sélection de l'inventaire, dans le fichier "Objects"
	elif choice in ["statut", "stats", "statistiques"]:
		player.status_display()
	elif choice in ["quitter"]:
		sys.exit()

def move(): #retourne la case correspondante en fonction de direction du joueur
	direction = input("\nDans quelle direction souhaitez-vous aller ?\n> ") #demande ver où il veut aller
	direction = direction.lower()
	while direction not in ["haut", "bas", "gauche", "droite", "sud", "nord", "est", "ouest"]:
		direction = input("\nEntrez un choix valide.\n> ")
		direction = direction.lower()
	if direction in ["bas", "sud"]: 
		return carte[player.pos][DOWN] #si il veut aller en bas, player.pos prend la valeur DOWN 
	if direction in ["haut", "nord"]: 
		return carte[player.pos][UP] #si il veut aller en haut, player.pos prend la valeur UP 
	if direction in ["droite", "est"]: 
		return carte[player.pos][RIGHT] #si il veut aller à droite, player.pos prend la valeur RIGHT 
	if direction in ["gauche", "ouest"]:
		return carte[player.pos][LEFT] #si il veut aller à gauche, player.pos prend la valeur LEFT

def event(): #lance l'évènement de la case si elle n'est pas déjà visitée
	if room_investigated[player.pos] == False: #la case n'a pas été visité
		print(carte[player.pos][EVENT])
		pos = player.pos
		event_action(pos)
	else:
		print("\nIl n'y a plus rien à chercher dans cette zone.") #sinon, ne fais rien

def event_action(pos): #enclenche un évènement en fonction de la case
	global fail, clear
	if pos == "a1": #si le joueur est sur la case a1
		combat(player, monsters[0], player_inv, 0) #le combat avec le premier monstre se lance
	elif pos == "a2": #si le joueur est sur la case a2
		print("\nChoisissez un de ces objets :") 
		print(" - Jus d'orange concentré\n - Rempart magique") #propose 2 objets au joueur
		choice = input("> ")
		choice = choice.lower()
		if choice == "jus d'orange concentré": #si il choisit le jus d'orange concentré
			player_inv.add_item(objects[3]) #l'objet 3 s'ajoute à l'inventaire
			fail = False #succès de l'événement
		elif choice == "rempart magique": #si il choisit le rempart magique
			player_inv.add_item(objects[4]) #l'objet 4 s'ajoute à l'inventaire
			fail = False #succès de l'événement
		else:
			fail = True #échec de l'événement
	elif pos == "a3":
		combat(player, monsters[1], player_inv, 1)
		if fail == False:
			print("\nEn mourant, le T-rex vomit des Chaussures qui semblent très légères !")
			player.add_equipment("boot", boots[4])
	elif pos == "a4":
		player_inv.add_item(objects[0])
		fail = False
	elif pos == "b1":
		print("\nVous obtenez des Bottes de Cuir trop ouf !")
		player.add_equipment("boot", boots[1])
		fail = False
	elif pos == "b2":
		combat(player, monsters[2], player_inv, 0)
		if fail == False:
			print("\nÀ votre plus grand étonnement, le serpent crache une épée en mourant.")
			player.add_equipment("sword", swords[2])
	elif pos == "b3":
		print("\nMais vous trouvez une Épée en bois par terre.")
		player.add_equipment("sword", swords[1])
		fail = False
	elif pos == "b4":
		print("\nUne fontaine avec 3 verres d'eau, quelle chance !")
		player_inv.add_item(objects[2])
		player_inv.add_item(objects[2])
		player_inv.add_item(objects[2])
		fail = False
	elif pos == "c1":
		room_investigated[player.pos] = True
		fail = True
		player.pos = "a4"
	elif pos == "c2":
		player.add_equipment("armor", armors[3])
		fail = False
	elif pos == "c3":
		room_investigated[player.pos] = True
		fail = True
		player.pos = "a2"
		print("\nIl vous envoie valser à l'autre bout de la carte.")
	elif pos == "c4":
		combat(player, monsters[4], player_inv, 1)
		if fail == False:
			print("\nC'était pas simple mais vous avez pas perdu votre temps, vous obtenez une couronne qui semble puissante.")
			player.add_equipment("helmet", helmets[4])
	elif pos == "d1":
		print("\nC'est une potion qui brille fort, à boire en cas de gros problème.")
		player_inv.add_item(objects[5])
		fail = False
	elif pos == "d2":
		combat(player, monsters[3], player_inv, 0)
		if fail == False:
			print("\nC'était juste un gros rat.")
			print("\nIl y avait un gros bouclier dans son ventre, quelle chance !")
			player.add_equipment("shield", shields[3])
	elif pos == "d3":
		player_inv.add_item(objects[1])
		fail = False
	elif pos == "d4":
		print("\nDevant la porte, vous trouvez une épée qui n'a pas l'air trop mal.")
		player.add_equipment("sword", swords[3])
		print("\nBonne chance", player.name + ".")
		combat(player, monsters[5], player_inv, 1)
		if fail == False:
			print("\nVous êtes vraiment fort, maintenant vous vous suicidez parce que tuer des gens c'est pas bien.")
			clear = True
	if fail == False:
		room_investigated[player.pos] = True


##########################
##### GESTION DU JEU #####
##########################

#====> Écran Titre

def title_screen(): #présentation de l'écran titre
	print("\n================================") #graphismes du menu
	print("= Jeu d'Aventure en mode texte =")
	print("================================")
	print("           - Jouer   -          ")
	print("           - Aide    -          ")
	print("           - Quitter -          ")
	print("--------------------------------")
	title_screen_selections() #appelle la fonction qui permet de faire un choix

def title_screen_selections(): #fonction pour les différents choix du menu principal
	option = ""
	def title_options(): #fonction comprenant les différentes options
		option = input("> ")
		option = option.lower()
		if option == "jouer":
			game_setup() #lance le jeu
		elif option == "aide":
			help_menu() #affiche un menu d'aide
		elif option == "quitter":
			sys.exit() #ferme la fenêtre
	title_options()
	while option not in ['jouer', 'aide', 'quitter']: #répéter le code au-dessus tant que le joueur n'entre pas une option valide
		print("\nEntrez une commande valide !")
		title_options()

def help_menu(): #menu d'aide
	print("\n1 - Présentation du Jeu") #différentes options
	print("2 - Liste des Actions")
	print("3 - Crédits")
	print("4 - Quitter Aide")
	option = input("\nEntrez un chiffre :\n> ") #j'utilise un input simple pour éviter les crashs du type "ce n'est pas un nombre"
	option = option.lower() #réduit tout à des caractères minuscules
	if option in ["1", "présentation du jeu"]: #présentation du jeu
		print("\nCette formidable aventure vous permet d'aller venger votre mère et tout votre entourage défint de l'infâme Zititine,")
		print("prenez votre courage et surtout votre épée à deux mains et relevez le défi !")
	elif option in ["2", "liste des actions"]: #liste non exhaustive des actions possibles en jeu
		print("\nActions Hors Combat :")
		print("> Avancer (Haut, Bas, Gauche, Droite)")
		print("> Inventaire (Ouvre le menu inventaire)")
		print("> Statut (Vous pouvez voir vos statistiques)")
		print("Actions en Combat :")
		print("> Attaque (Vous jetez un dé d'attaque qui détermine si vous touchez ou non, les dégâts se basent sur votre caractéristique d'attaque et vos équipements)")
		print("> Défense (Vous vous protégez c'est bien sortez couverts !)")
		print("> Inventaire (Ouvre votre inventaire)")
		print("> Fuir (Sauve qui peut !)")
	elif option in ["3", "crédits"]: #crédits
		print("\nCopyright 2019 Studio Argouse.\nProgrammeurs : Arthur Dumez, Logan Argouse et Paul Meuley")
	elif option in ["4", "quitter", "quitter aide"]: #retour à l'écran titre
		title_screen()
	else:
		print("Entrez un numéro valide !")
	help_menu()

def game_setup(): #lancer le jeu
	player.name = str(input("\nBonjour Aventurier, vous vous apprêtez à vivre une épreuve hors du commun.\nQuel est votre nom ?\n> "))
	while player.name == "" or len(player.name) > 15:
		if player.name == "":
			player.name = str(input("\nVous vous appelez rien du tout ? C'est assez dommage...\nDonnez-vous quand même un nom pardi !\n> "))
		if len(player.name) > 15:
			player.name = str(input("\nC'est un peu long comme nom non ?\nEntrez autre chose.\n> "))
	print("\nEnchanté", player.name + ".", "\nVous allez devoir défaire l'horrible Grand méchant qui fait régner sur ces terres la prospérité et la joie.\nVous fuyez votre villa qui vient d'être rasée par Zititine le Malfaisant Nuisible Délétère Pernicieux Pas Beau.\nVous n'avez désormais plus que la vengeance en tête.")
	player.pos = "a1"
	print("\nVous ouvrez les yeux, il fait beau, et vous vous sentez prêt.")
	game_loop()

def game_loop():
	while clear == False:
		prompt()
	input("The End. (Tapez Entrez pour recommencer le jeu)")
	restart_program()

#====> Combat et événements

def combat(Player, Enemy, Inventory, Priority): #définit le déroulement d'un combat

	global defense_stance, powerful_attack, fail, clear #définit des variables globales
	fail = False
	defense_stance = False #initialise la position défensive du joueur à "non"
	powerful_attack = False #initialise la position offensive de l'ennemi à "attaque normale"
	Enemy = deepcopy(Enemy) #crée une copie de l'objet dans la mémoire de l'ordinateur pour ne pas toucher aux données d'origine

	def dmg_calculator(multiplier): #calcule les dommages en fonction d'un multiplieur
		global defense_stance
		if player_turn == True: #si le joueur attaque
			damage = int(multiplier * Player.get_stat(StatType.ATK) - Enemy.arm)
			if damage < 0:
				damage = 0 #évite les cas où les dommages seraient négatifs
			Enemy.hp -= damage #occasionne les dommages à l'ennemi
			if Enemy.hp < 0:
				Enemy.hp = 0 #évite une situation ou le personnage aurait une valeur négative de PVs
		else: #si l'ennemi attaque
			if defense_stance == True: #si le joueur est en position défensive, ajoute
				damage = int(multiplier * Enemy.atk - (Player.get_stat(StatType.ARM) + Player.shield.arm))
				defense_stance = False
			else:
				damage = int(multiplier * Enemy.atk - Player.get_stat(StatType.ARM))
			if damage < 0:
				damage = 0 #évite les cas où les dommages seraient négatifs
			Player.hp -= damage #occasionne les dommages au joueur
			if Player.hp < 0:
				Player.hp = 0
		return damage

	def dmg_display(damage): #fonction qui affiche les résultats d'une attaque en combat
		if player_turn == True: #si la fonction est utilisée pour afficher des dommages occasionnés par le joueur
			print("\nVous infligez", damage, "points de dommages à l'ennemi !")
			input("Il lui reste " + str(Enemy.hp) + " points de vie.")
		else: #si la fonction est utilisée pour afficher des dommages occasionnés par l'ennemi
			print("\nL'ennemi vous inflige", damage, "points de dommages !")
			input("Il vous reste " + str(Player.hp) + " points de vie.")

	"""Ci-dessous, le déroulement d'un combat.
	La variable "time" désigne le nombre de tours ayant passé,
	tandis que la variable "player_turn" indique True pour le tour du joueur, False pour le tour de l'ennemi
	"""

	if Priority == 1: #si l'ennemi a la priorité d'attaque, il attaque en premier
		print("\nL'ennemi a l'initiative !")
		player_turn = False
		time = 0 #définit le numéro du tour (ici à 0 car le tour ennemi ajoute un tour automatiquement)
	else: #sinon, le joueur attaque en premier
		player_turn = True
		time = 1 #définit le numéro du tour
	print("\nLe combat commence !")
	Player.check_buff()
	powerful_attack_time = [] #définit les tours sur lesquels l'ennemi va lancer sa grosse attaque
	for i in range(0, 20): #ajoute une attaque puissante tous les environs 3 tours
		powerful_attack_time.append(randint(i*3 + 2, i*3 + 4))
	while Enemy.hp > 0 and fail == False: #tant que l'ennemi est vivant
		if player_turn: #si c'est au tour du joueur
			print("\nTour", time)
			option = input("Que voulez-vous faire ?\n - attaquer\n - défense\n - inventaire\n - statut\n - fuir\n> ")
			option = option.lower() #convertit le texte entré en des caractères minuscules uniquement
			if option in ["attaquer", "attaque"]: #si le joueur choisit d'attaquer
				die = die_roll() #lance un dé à 100 faces
				if die <= int(0.2 * Player.get_stat(StatType.AGI)): #si la valeur du dé est inférieure à 20% de l'agilité du joueur
					damage = dmg_calculator(1.5) #augmente la valeur d'attaque de 50%
					input("Succès critique !")
					dmg_display(damage) #affiche des phrases qui indiquent les dommages occasionnés et les PVs restants
				elif die <= Player.get_stat(StatType.AGI): #si la valeur du dé est inférieure à l'agilité du joueur
					damage = dmg_calculator(1.0) #la valeur d'attaque est inchangée
					input("Succès !")
					dmg_display(damage)
				elif die > 100 - int(0.2 * (100 - Player.get_stat(StatType.AGI))): #si la valeur du dé est supérieure à (100 - 20%) de (100 - l'agilité du joueur)
					damage = dmg_calculator(0.0) #la valeur d'attaque est complètement annulée
					input("Échec critique !")
					dmg_display(damage)
				else: #si aucune des conditions au-dessus n'est remplie
					damage = dmg_calculator(0.5) #diminue la valeur d'attaque de 50%
					input("Échec !")
					dmg_display(damage)
				player_turn = False #passage au tour ennemi
			elif option in ["défendre", "défense"]: #si le joueur choisit de se défendre
				defense_stance = True #indique au jeu que le joueur est en position défensive
				player_turn = False
			elif option in ["inventaire", "objets"]: #si le joueur choisit de consulter son inventaire
				item_chosen = Inventory.select_item() #accède au menu de sélection de l'inventaire, dans le fichier "Objects"
				if item_chosen == False: #si aucun item n'est choisi, rejouer le tour du joueur
					player_turn = True
				else:
					player_turn = False #sinon, passer au tour de l'ennemi
			elif option in ["statut", "stats", "statistiques"]:
				Player.status_display()
			elif option in ["fuir", "oof"]: #si le joueur choisit de fuir
				die = die_roll() #lance un dé à 100 faces
				if die <= Player.get_stat(StatType.AGI): #si le dé est inférieur à l'agilité du joueur
					direction = randint(0, 3) #définit aléatoirement la case adjacente ou le joueur va fuir
					if direction == 0:
						player.pos = carte[player.pos][DOWN]
					if direction == 1:
						player.pos = carte[player.pos][UP]
					if direction == 2:
						player.pos = carte[player.pos][RIGHT]
					if direction == 3:
						player.pos = carte[player.pos][LEFT]
					print("\nSuccès !")
					input("Sauve qui peut ! (Appuyez sur Entrée)")
					player_turn = True
					fail = True #permet d'éviter que je joueur obtienne la récompense en fuyant le combat
				else:
					input("Échec !")
					player_turn = False
			else: #si l'action entrée n'est pas reconnue comme une action par le programme
				print("\nCette action n'est pas reconnue, essayez un synonyme ou un équivalent.")
			if Enemy.hp == 0: #si l'ennemi est KO, sortir directement de la boucle de combat
				print("\nL'ennemi est KO !")
				player_turn = True
		if player_turn == False: #si c'est au tour de l'ennemi
			if powerful_attack == True:
				print("\nL'ennemi se déchaîne !!")
				damage = dmg_calculator(1.8) #dommages occasionnés par l'ennemi
			else:
				print("\nL'ennemi attaque !")
				damage = dmg_calculator(1.0) #dommages occasionnés par l'ennemi
			dmg_display(damage) #affiche des phrases qui indiquent les dommages encaissés et les PVs ennemis restants
			if Priority == 0 or time > 1:
				Player.check_buff()
			player_turn = True #passage au tour du joueur
			time += 1 #ajouter 1 au compteur de tours
			if Player.hp <= 0: #si le joueur est KO, revenir à l'écran titre
				input("\nVous avez succombé...\nRetour à l'écran titre.") 
				restart_program() #le "input" permet ici au joueur de lire les deux phrases avant de revenir à l'écran titre. Il lui suffit juste d'appuyer sur "Entrée"
			if time in powerful_attack_time: #si le tour actuel correspond au tour où l'ennemi lance son attaque massive
				powerful_attack = True
				print("\nL'ennemi se prépare à porter un coup massif !")
			else:
				powerful_attack = False

def die_roll(): #simule un lancer de dé à 100 faces, et donne le résultat
	input("Lancer de dé ! (Appuyez sur Entrée pour faire défiler)")
	die = randint(1, 100) #nombre aléatoire entre 1 et 100
	print("Le résultat est un", die)
	return die #retourne la valeur du dé à la variable associée

def restart_program(): #redémarre le programme
	python = sys.executable
	os.execl(python, python, * sys.argv)

##########################
##### LANCEUR DU JEU #####
##########################

title_screen()