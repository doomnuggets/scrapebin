from sqlalchemy.exc import IntegrityError

import scrapebin.models


class Database(object):

    def __init__(self, db=None):
        self.db = db or scrapebin.models.db

    def dump_paste(self, paste_meta):
        """Dump a paste's metadata into the database."""
        paste = scrapebin.models.Paste(**paste_meta)
        self.db.session.add(paste)
        self.db.commit()
        return paste

    def dump_many(self, json_data):
        """Dump all paste metadata from a JSON blob into the database."""
        for paste in json_data:
            try:
                yield self.dump_paste(paste)
            except IntegrityError as e:
                print(e)
                self.db.session.rollback()
