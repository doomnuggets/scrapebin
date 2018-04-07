import os

from scrapebin import constants
from scrapebin.models import Paste


class Backup(object):

    def __init__(self, backup_dir=None, data_dir=None):
        self.backup_dir = backup_dir or constants.BACKUP_DIR
        self.data_dir = data_dir or constants.DATA_DIR

    def _confirm_backup(self, paste):
        paste.update(saved=True)

    def create(self, paste):
        output_dir = os.path.join(self.backup_dir, paste.date.strftime('%Y-%M-%d'))
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, 0750)

        old_file = os.path.join(self.data_dir, paste.key)
        new_file = os.path.join(output_dir, paste.key)
        if os.path.isfile(old_file):
            os.rename(old_file, new_file)

        self._confirm_backup(paste)

    def create_all(self):
        for paste in Paste.query().filter(Paste.saved == 0):
            self.create(paste)
