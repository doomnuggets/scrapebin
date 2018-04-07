import datetime
import time

from active_alchemy import ActiveAlchemy
from sqlalchemy.types import TypeDecorator, DateTime, Integer

from scrapebin.config import cfg


db = ActiveAlchemy(cfg.get('database', 'uri'))


class Paste(db.Model):
    __tablename__ = 'tbl_paste'
    __primary_key__ = 'key'
    id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(60))
    date = db.Column(db.String(30))
    size = db.Column(db.String(50))
    expire = db.Column(db.String(10))
    user = db.Column(db.String(120))
    syntax = db.Column(db.String(120))
    backup_created = db.Column(db.Boolean, default=0)

    def __init__(self, **kwargs):
        self.id = kwargs.get('key')
        self.title = kwargs.get('title')
        self.date = kwargs.get('date')
        self.size = kwargs.get('size')
        self.expire = kwargs.get('expire')
        self.user = kwargs.get('user')
        self.syntax = kwargs.get('syntax')
        self.backup_created = kwargs.get('backup_created', False)

    @property
    def human_readable_date(self):
        return datetime.datetime.utcfromtimestamp(int(self.date))


db.create_all()
