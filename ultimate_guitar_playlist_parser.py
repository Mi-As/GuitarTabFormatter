#/usr/bin/python3
import re
import sys

from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ultimate_guitar_parser import TabFormatter


class PlaylistTabFormatter:

	def __init__ (self, playlist_url, outfile="formatted_tab"):
		self.playlist_url = playlist_url
		self.outfile = outfile

	def _get_tab_urls(self):

		try:
			req = Request(self.playlist_url)
			html_page = urlopen(req)
		except HTTPError as r:
			print(f"\nERROR: HTTPError for url {self.playlist_url}")
			sys.exit()
		except ValueError as v:
			print(f"\nERROR: Enter a valid url")
			sys.exit()

		# get html
		soup = BeautifulSoup(html_page, "html.parser")
		tab_soup = soup.find("div", class_="js-store")

		# extract urls
		pattern = r'"tab_url":"([^,]*)","type_name":"Chords"}'
		tab_re= re.findall(pattern, str(tab_soup))

		# remove duplicates
		tabs_cut = tab_re[:int(len(tab_re)/2)]

		if tabs_cut is None:
			print(f"ERROR: Cannot extract tabs, only ultimate-guitar tabs supported")
			sys.exit()

		return tabs_cut

	def write_latex_tabs(self):
		tab_urls = self._get_tab_urls()

		for count, url in enumerate(tab_urls):
			TabFormatter(url, f'{self.outfile}{count}').write_latex_tab()

	def write_text_tab(self):
		tab_urls= self._get_tab_urls()

		for count, url in enumerate(tab_urls):
			TabFormatter(url, f'{self.outfile}{count}').write_text_tab()

if __name__ == '__main__':
	
	playlist_url = input("Enter the ultimate guitar playlist web link for your tabs:\n")
	PlaylistTabFormatter(playlist_url).write_text_tab()