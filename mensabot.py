# coding: utf8

from errbot.botplugin import BotPlugin
from errbot import botcmd
from urllib.request import urlopen
from lxml import etree
from datetime import datetime
from random import choice

class MensaBot(BotPlugin):

	def __init__(self):
		super(MensaBot, self).__init__()

	@botcmd
	def mensa(self, mess, args):
		""" Prints the menu @Mensa Uni Karlsruhe for this day (before 2pm) or the next day (2pm and after) in a compact form. """
		result = {}
		lines = ["1", "2", "3", "4/5", "SB", "6"]
		html = etree.HTML(urlopen("http://www.studentenwerk-karlsruhe.de/de/essen/?view=ok&STYLE=popup_plain&c=adenauerring&p=1").read())
		
		# Show table for next day after 2pm
		tableindex = 1
		if datetime.now().hour >= 14:
			tableindex = 2
		
		# Each row represents a line.
		rows = [r for r in html.xpath("/html/body/table/tr/td/div/table[" + str(tableindex) + "]/tr") if len(r)]
		for idx, row in enumerate(rows):
			# Don't show special lines like Curry Queen, Cafeteria etc.
			if idx >= len(lines):
				break

			# Each row inside the subtable represents a food item
			for food in row[1].xpath("table/tr"):
				if len(food) < 2:
					continue
			
				# Don't display food items which cost less than €1 or have no assigned price.
				price_nodes = food[1].xpath("span[contains(@class,'price_1')]/text()")
				if len(price_nodes) == 0:
					continue

				price = price_nodes[0].strip()
				if price.startswith("0,"):
					continue
				
				# Display only the bold-face part of the food name
				foodname = food[0].xpath("span/b")[0].text.strip()
				
				# Append food and price to results
				if lines[idx] not in result:
					result[lines[idx]] = []
					
				result[lines[idx]].append(foodname + " " + price)

		result = " ".join(["[" + key + "] " + ", ".join(result[key]) for key in lines if key in result])

		comments = ["Guten Appetit!",
			"Bon appétit!",
			"Enjoy your meal!",
			"¡Buen provecho!",
			"Buon appetito!",
			"多吃点!",
			"прия́тного аппети́та!",
			"Smacznego!",
			"Brought to you by the one and only Mensabot™ – since 1803.",
			"(Disclaimer: Mensabot™ übernimmt keine Verantwortung für erlittene oder eingebildete Lebensmittelvergiftungen.)",
			"(Apropos: Wann gehen wir mal wieder Blut spenden?)",
			"(Es steht mir ja nicht zu, das zu kommentieren, aber ich empfehle heute Linie " + choice(["1", "2", "3", "4/5", "6", "42", "9 3/4"]) + ".)",
			"(Ich sag’s ja nur ungern, aber da ist heute nix dabei. Auf zur Schnitzelbar!)",
			"(Wenn’s mal nicht geschmeckt hat: Mail an verpflegung@studentenwerk-karlsruhe.de)",]

		if "omlette" in result.lower():
			comments.append("(P.S. Wann wird „Omelette“ mal richtig geschrieben?)")
		if "spinat" in result.lower():
			comments.append("(Spinat habe ich übrigens noch nie gemocht.)")
		if "medaillon" in result.lower():
			comments.append("(Bullshit-Bingo: Medaillon!)")
		if "bolognese" in result.lower():
			comments.append("(Also Bolognese kann ich auch zu Hause kochen.!)")
		if "sahnesoße" in result.lower():
			comments.append("(Warnung: Sahnesoße ist mit 70% Wahrscheinlichkeit einfach nur Wasser.)")
		if "paella" in result.lower():
			comments.append("(Hach, Paella. Das erinnert mich an meine Zeit in Barcelona. Sonne, Sommer, Strand … jemand neidisch?)")
		if "schlemmer" in result.lower():
			comments.append("(Also Namen ausdenken können die sich, das muss man ihnen lassen.)")
		if "fagottini" in result.lower():
			comments.append("(Fagottini … fagöttlich!)")
		if "kaiser" in result.lower():
			comments.append("(Schon gewusst? Die Mensaleitung ist von Monarchisten durchsetzt.)")
		if "gulasch" in result.lower():
			comments.append("(Gulasch? Erinnert mich an die GPN. Schöne Zeiten!)")
		if "vegetarisches schnitzel" in result.lower():
			comments.append("(Übrigens: Schon mal was von einem Oxymoron gehört?)")
		if "weißwein" in result.lower() or "rotwein" in result.lower():
			comments.append("Prost!")
		if "bifteki" in result.lower():
			comments.append("(Das müsste eigentlich Bifteki™ heißen.)")

		if datetime.now().weekday() == 2:
			comments.append("(Heute ist Eintopftag! All glory to the Erbseneintopf!)")
		if datetime.now().weekday() == 4:
			comments.append("(Übrigens gibt es heute kein Abendessen in der Mensa. Tja, Pech.)")

		return result + ". " + choice(comments)
