import os
import time
import argparse

from scrapebin.models import Paste
from scrapebin import constants
from scrapebin.database import Database
from scrapebin.pastebin import Pastebin


def dump_pastes_to_disk(paste_iter, output_dir):

    def write_to_file(output_file, data):
        with open(output_file, 'w') as fout:
            fout.write(data)

    for paste_id, data in paste_iter:
        paste_meta = Paste.query().filter(Paste.id == paste_id)
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
            pastes = pastebin.scrape(limit=args.pastes_per_request)
            database.dump_many(pastes)
            paste_ids = [paste.get('id') for paste in pastes]
            paste_iter = pastebin.fetch_many(paste_ids)
            dump_pastes_to_disk(paste_iter, args.data_dir)
            print('sleeping...')
            time.sleep(args.sleep_duration)
    except KeyboardInterrupt:
        pass


def main(args):
    scrapebin.models.db.create_all()
    keep_scraping(args)


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--sleep-duration', default=constants.SLEEP_DURATION)
    ap.add_argument('-d', '--data-dir', default=constants.DATA_DIR)
    ap.add_argument('-p', '--pastes-per-request', default=constants.PASTES_PER_REQUEST)

    args = ap.parse_args()
    exit(main(args))
