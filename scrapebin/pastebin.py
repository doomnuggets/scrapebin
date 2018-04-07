import os
import requests

class Pastebin(object):

    def scrape(self, limit=50):
        """Scrape the last N paste metadata from pastebin.
        The optional limit parameter restricts how many pastes are returned."""
        scrape_url = 'https://pastebin.com/api_scraping.php?limit={}'.format(limit)
        scrape_response = requests.get(scrape_url)
        return scrape_response.json()

    def fetch(self, paste_key):
        """Download a paste by it's identifier (key)."""
        paste_url = 'https://pastebin.com/api_scrape_item.php?i={}'.format(paste_key)
        response = requests.get(paste_url)
        return response.content

    def fetch_many(self, paste_keys):
        """Fetch multiple pastes identified by their paste key."""
        for paste_key in paste_keys:
            yield paste_key, self.fetch(paste_key)
