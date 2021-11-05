#/usr/bin/python3
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import sys
import re

# BUG: if space, chord sometimes does not fit corrctly


class TabFormatter:


	def __init__(self, tab_link):
		self.tab_link = tab_link
		self.outfile = "TabFormatter.txt"

		self._chord_pattern = r'\[ch\](.*?)\[/ch\]'
		self._tabline_pattern = r'\[tab\](.*?)\[/tab\]'
		self._return_pattern = r'\\r\\n'


	def write_latex_tab(self):

		tab_data = self.get_html_cut()

		# format tablines
		while(re.search(self._tabline_pattern, tab_data)):

			tab_line = re.search(self._tabline_pattern, tab_data).group(1)
			new_tabline = self._join_chords_and_text(tab_line)
			new_tabline_re = re.sub(self._tabline_pattern, new_tabline, tab_data, count=1)

			tab_data = str(new_tabline_re)

		# format no lyrics lines
		tab_data = re.sub(self._chord_pattern, r'\\[\1]', tab_data)

		# format line returns
		return_re = re.split(self._return_pattern, tab_data)

		# wirte to file
		with open(self.outfile, "w") as file:

			file.write("\\beginsong{todo}[by={todo},\ncr={" + self.tab_link + "}]\n\n\\beginverse")

			last_was_retrun = False
			for line in return_re:
				if not line and not last_was_retrun:
					file.write("\\endverse\n\n\\beginverse")
					last_was_retrun = True
				else:
					last_was_retrun = False
				file.write(str(line) + "\n")

			file.write("\\endverse\n\n\\endsong")

	def write_text_tab(self):

		tab_data = self.get_html_cut()

		tab_data = re.sub(self._chord_pattern, r'\1', tab_data) # format chords
		tab_data = re.sub(self._tabline_pattern, r'\1', tab_data) # format lines		
		return_re = re.split(self._return_pattern, tab_data) # format line returns

		# write to file
		with open(self.outfile, "w") as file:

			for line in return_re:
				file.write(str(line) + "\n")


	def get_html_cut(self):
		req = Request(self.tab_link)
		try:
			html_page = urlopen(req)
		except HTTPError as r:
			print(f"ERROR: HTTPError for url {self.tab_link}")
			sys.exit()

		# get html
		soup = BeautifulSoup(html_page, "html.parser")
		tab_soup = soup.find("div", class_="js-store")

		# extract tabs
		pattern = r'content&quot;:&quot;(.*)&quot;,&quot;revision_id&quot;'
		tab_re= re.search(pattern, str(tab_soup))

		if tab_re is None:
			print(f"ERROR: Cannot extract tabs, only ultimate-guitar tabs supported")
			sys.exit()

		tab_str = str(tab_re.group(1))

		return tab_str


	def _join_chords_and_text(self, tabline):

		return_re = re.split(self._return_pattern, tabline)

		if not len(return_re) == 2:
			return "Error"

		new_tabline = return_re[1] + 10*" "
		tmp = 0
		for match in re.finditer(self._chord_pattern, return_re[0]):

			position = match.span()[0] + tmp
			new_tabline = f'{new_tabline[:position]}\\[{match.group(1)}]{new_tabline[position:]}'

			len_chord_bef = match.span()[1]-match.span()[0]
			len_chord_aft = len(match.group(1))+4
			tmp = tmp - len_chord_bef + len_chord_aft

		return new_tabline.strip()



if __name__ == '__main__':
	
	tab_link = input("Enter the ultimate guitar web link for your tabs:\n")
	TabFormatter(tab_link).write_text_tab()
