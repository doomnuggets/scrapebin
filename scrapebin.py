import os
import time
import argparse

import scrapebin.models
from scrapebin import constants
from scrapebin.database import Database
from scrapebin.pastebin import Pastebin
from scrapebin.backup import Backup


def dump_pastes_to_disk(paste_iter, database, pastebin, output_dir):

    def write_to_file(output_file, data):
        with open(output_file, 'w') as fout:
            fout.write(data)

    for paste_id, data in paste_iter:
        paste_meta = scrapebin.models.Paste.query(paste_id)
        output_directory = os.path.join(output_dir, paste_meta.human_readable_date.strftime('%Y-%m-%d'))
        output_file = os.path.join(output_directory, paste_id)
        try:
            write_to_file(output_file, data)
        except IOError:
            os.makedirs(output_directory)
            write_to_file(output_file, data)


def keep_scraping(args):
    pastebin = Pastebin()
    database = Database()
    try:
        while True:
            pastes = pb.scrape(limit=args.pastes_per_request)
            database.dump_many(pastes)
            paste_ids = [paste.get('id') for paste in pastes]
            paste_iter = pastebin.fetch_many(paste_ids)
            dump_pastes_to_disk(paste_iter, database, pastebin, args.data_dir)
            print('sleeping...')
            time.sleep(args.sleep_duration)
    except KeyboardInterrupt:
        pass


def backup_pastes(args):
    db = Database()
    backup = Backup(db)
    backup.create_all()


def main(args):
    scrapebin.models.db.create_all()
    if args.command == 'scrape':
        keep_scraping(args)
    else:
        backup_pastes(args)


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    subparsers = ap.add_subparsers(dest='command')
    sp = subparsers.add_parser('scrape')
    sp.add_argument('-s', '--sleep-duration', default=constants.SLEEP_DURATION)
    sp.add_argument('-d', '--data-dir', default=constants.DATA_DIR)
    sp.add_argument('-p', '--pastes-per-request', default=constants.PASTES_PER_REQUEST)

    bp = subparsers.add_parser('backup')
    bp.add_argument('-b', '--backup-dir', default=constants.BACKUP_DIR)

    args = ap.parse_args()
    exit(main(args))
