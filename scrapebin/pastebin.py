import os
import requests

class Pastebin(object):

    def scrape(self, limit=50):
        """Scrape the last N paste metadata from pastebin.
        The optional limit parameter restricts how many pastes are returned."""
        scrape_url = 'https://pastebin.com/api_scraping.php?limit={}'.format(limit)
        scrape_response = requests.get(scrape_url)
        return scrape_response.json()

    def fetch(self, paste_id):
        """Download a paste by it's identifier (key)."""
        paste_url = 'https://pastebin.com/api_scrape_item.php?i={}'.format(paste_id)
        response = requests.get(paste_url)
        return response.content

    def fetch_many(self, paste_ids):
        """Fetch multiple pastes identified by their key."""
        for paste_id in paste_ids:
            yield paste_id, self.fetch(paste_id)
