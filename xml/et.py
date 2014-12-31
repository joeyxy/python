#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree

doc = ElementTree(file="recipe.xml")
ingredients = doc.find('ingredients')

for item in ingredients.findall('item'):
	num = item.get('num')
	units = item.get('units','')
	text = item.text.strip()
	quantity = "%s %s" % (num,units)
	print("%-10s %s" % (quantity,text))
