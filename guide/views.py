# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import State,City,touristSpot
from .states import get_data

# Create your views here.

def storeStates():
	states = get_data()
	print states
	for state in states:
		print state	
		try:
			new_state = State(name = state)
			new_state.save()
		except Exception as e:
			raise e


def storeCities():
	states = get_data()
	print "cities"
	for state in states:
		fk = State.objects.get(name=state)
		print "fk"
		for city in states[state]:
			print city
			if(city[len(city)-1] == '*'):
				city = city.split("*")[0]
			print city
			try:
				new_city = City(name = city,state = fk)
				new_city.save()
			except Exception as e:
				print e
		
def scrape():
	import urllib2
	from bs4 import BeautifulSoup

	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	url = "https://www.holidify.com/collections/tourist-places-in-india"
	response = opener.open(url)
	page = response.read()
	soup = BeautifulSoup(page)
	mydivs = soup.findAll("div", { "class" : "col-md-6 col-xs-12 resultColumn nopaddingMobile" })
	anchors = []
	for div in mydivs:
		anchors.append(div.findAll("a", { "class" : "resultName" }))
	cities = []
	states = []
	for place in anchors:
		try:
			pair = place[0].contents[0].split(",")
			city = pair[0].split(" ")[1]
			cities.append(city)
			print city
	

			state = pair[1].split(" ")[1]
			states.append(state)
			if State.objects.filter(name = state).exists():
				fk = State.objects.get(name=state)
				new_city = City(name = pair[0],state = fk)
				new_city.save()
			else:
				new_state = State(name = state)
				new_state.save()
				fk = State.objects.get(name=state)
				new_city = City(name = pair[0],state = fk)
		except Exception as e:
			print e
	
	print cities
	anchorData = []
	for city in cities:
		try:
			url = "https://www.holidify.com/places/" + city		
			print url
			response = opener.open(url)
			page = response.read()
			soup = BeautifulSoup(page)
			mydivs = soup.findAll("div", { "class" : "textColor attrCardName" })
			anchors = []
			for div in mydivs:
				anchors.append("https://www.holidify.com/" + div.find("a")["href"])
			anchorData.append(anchors)
				
		except Exception as e:
			print e
	
	finalData = {}
	cityNo = 0
	print "hello"
	for city in cities:
		try:
			print "currently on city : " + str(city) + "\n"
			
			fk = City.objects.get(name = city)
			
			finalData[city] = []
			spots = []
			for link in anchorData[cityNo]:
				#scrape from this link
				url = link
				response = opener.open(url)
				page = response.read()
				soup = BeautifulSoup(page)
				#name = soup.select('h1.h1Style')[0].text.strip()
				divs = soup.findAll("div", { "class" : "row infoSpace" })
				name = divs[0].find("h2",{"class": "headingForMiddleSection" }).text.split(" ")[2]
				duration = divs[1].find("div",{"class":"col-md-10 col-xs-10 nopaddingLeft"})
				duration.span.clear()
				duration = duration.text.split(" ")[0]
				print "fetching for " + str(name) + "link is : " + link + "\n"
				p = soup.findAll("p",{"class":"textColor infoSpace"})
				description = p[0].text
				description = description + p[1].text
				#description = (description[:9997] + '..') if len(description) > 10000 else description
				spot = {
						"name":name,
						"duration":duration[0],
						"description": description

				}
				print  spot  
				print "\n"
				spots.append(spot)

				new_spot = touristSpot(name=name,description=description,duration=int(duration),city=fk)
				new_spot.save()
			
			cityNo = cityNo+1
			finalData[city].append(spots)
			print finalData
			
		except Exception as e:
			print e
		
def index(request):
	
	#storeStates()
	#storeCities()
	scrape()
	return render(request,'pages/index.html',{'data':'you are at index page'})