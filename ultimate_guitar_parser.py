#/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

"""
\beginsong{A World Of Chaos}[by={poems of the past}, cr={https://tabs.ultimate-guitar.com/tab/powfu/a-world-of-chaos-chords-3180749}]

\beginverse
[Intro: Ivri]
Spilled a \[D]glass of wine and stained the kitchen floor
We never \[F#m]used to fight but now it feels like war
\[Bm]Sadness in our home
But at \[A]least I'm not alone
\endverse
"""

def get_and_cut_html(tab_link):
	req = Request(tab_link)	
	html_page = urlopen(req)

	# get html
	soup = BeautifulSoup(html_page, "html.parser")
	tab_soup = soup.find("div", class_="js-store")

	# extract tabs
	pattern = r'content&quot;:&quot;(.*)&quot;,&quot;revision_id&quot;'
	tab_re= re.search(pattern, str(tab_soup))
	tab_str = str(tab_re.group(1))

	return tab_str

	# with open("beautifulsoup.html", "w") as file:
	#    file.write(tab_str)

def format_tab_data_to_latex(tab_data):
	
	# format chords
	chord_pattern = r'\[ch\]([A-h#785maj]*)\[/ch\]'
	chord_re = re.sub(chord_pattern, r"\\[\1]", tab_data)
	tab_data = chord_re

	print(tab_data)

	# format line returns
	return_pattern = r'\\r\\n'
	return_re = re.split(return_pattern, tab_data)

	with open("beautifulsoup.html", "w") as file:
		for line in return_re:
			file.write(str(line) + "\n")


if __name__ == '__main__':
	
	#tab_link = input("Enter the ultimate guitar web link für your tabs: ")

	test = "https://tabs.ultimate-guitar.com/tab/boywithuke/two-moons-chords-3757571"
	#test = "https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589"

	tab_data = get_and_cut_html(test)
	format_tab_data_to_latex(tab_data)
