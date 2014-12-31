#!/usr/bin/env python

from xml.dom import minidom
doc = minidom.parse("recipe.xml")

ingredients = doc.getElementsByTagName("ingredients")[0]
items = ingredients.getElementsByTagName("item")


for item in items:
	num = item.getAttribute("num")
	units = item.getAttribute("units")
	text = item.firstChild.data.strip()
	quantity = "%s %s" % (num,units)
	print ("%-10s %s" % (quantity,text))
