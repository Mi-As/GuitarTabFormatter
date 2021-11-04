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

# chord_pattern = r'\[ch\]([A-h#785maj]*)\[/ch\]'
chord_pattern = r'\[ch\](.*?)\[/ch\]'
tabline_pattern = r'\[tab\](.*?)\[/tab\]'
return_pattern = r'\\r\\n'

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

	# format tablines
	while(re.search(tabline_pattern, tab_data)):
		new_tabline = join_chords_and_text(re.search(tabline_pattern, tab_data).group(1))
		tabline_re = re.sub(tabline_pattern, new_tabline, tab_data, count=1)
		tab_data = str(tabline_re)

	# format line returns
	return_pattern = r'\\r\\n'
	return_re = re.split(return_pattern, tab_data)

	with open("beautifulsoup.html", "w") as file:
	 	for line in return_re:
	 		file.write(str(line) + "\n")

def join_chords_and_text(tabline):

	
	return_re = re.split(return_pattern, tabline)

	if not len(return_re) == 2:
		return "Error"

	new_tabline = return_re[1] + 10*" "
	tmp = 0
	for match in re.finditer(chord_pattern, return_re[0]):

		position = match.span()[0] + tmp
		new_tabline = f'{new_tabline[:position]}\\[{match.group(1)}]{new_tabline[position:]}'

		tmp += len(match.group(1))+3

	return new_tabline.strip()


if __name__ == '__main__':
	
	#tab_link = input("Enter the ultimate guitar web link für your tabs: ")

	tab_link = "https://tabs.ultimate-guitar.com/tab/boywithuke/two-moons-chords-3757571"
	# tab_link = "https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589"

	tab_data = get_and_cut_html(tab_link)
	format_tab_data_to_latex(tab_data)
