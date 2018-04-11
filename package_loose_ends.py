import os

from scrapebin.models import Paste

for root, dirs, files in os.walk('pastes'):
    for f in files:
        loose_file = os.path.join(root, f)
        target_file = os.path.join('pastes', p.human_readable_date.strftime('%Y-%m-%d'), p.id)
        os.rename(loose_file, target_file)
