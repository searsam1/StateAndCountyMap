
from os import name
from bs4 import BeautifulSoup
import requests

def run(debug=False):


	def clean(txt):
		res = [i if str(i).isalnum() else " " for i in txt] 
		return "".join(res)

	counties = "https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents"

	wiki_base_url = "https://en.wikipedia.org"

	r = requests.get(counties)

	links = [[i["href"] for i in link.find_all('a')] for link in 
			BeautifulSoup(r.text, 'lxml')
			.find_all(class_=["wikitable","sortable","jquery-tablesorter"])][0]

	links = [i for i in links if "county" in i.lower()]


	sesh_res = {}

	count = 0 

	with requests.session() as sesh:
	
		if debug:
			links = links[:20]
			print("\n\nDebug Mode On. Only using 20 links.\n\n")

		for link in links:
			count += 1
			r = sesh.get(wiki_base_url + "/" + link)
			assert str(r) == "<Response [200]>"
		
			latitude = BeautifulSoup(r.text, 'lxml').find(class_="latitude")
			longitude = BeautifulSoup(r.text, 'lxml').find(class_="longitude")
			if latitude and latitude: 
				print(latitude.text), print(wiki_base_url + "/" + link), print(r)
				print(f"~COUNT: {count}")
				sesh_res[link] = [

				{
				"latitude" : clean(latitude.text),
				"longitude" : clean(longitude.text)

				}, wiki_base_url + link]


			else: print("\tNo cordinates found....")

	with open("cordinates.txt", "w") as f:
		f.write(str(sesh_res))

if __name__ == "__main__":
	run(debug=True)