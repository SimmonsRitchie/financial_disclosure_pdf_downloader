
from pathlib import Path
import logging
from definitions import DIR_DATA
from pdf_downloader.helper.misc import delete_dir_contents
from pdf_downloader.scrape.get_pdf import get_pdf
from logs.config.logging import logs_config

def main():

    # init logging
    logs_config()
    logging.info('Beginning scrape')

    # filing ID
    filing_id = "336397"

    # create or clean up PDF download dir
    if DIR_DATA.is_dir():
        # delete files from previous run
        delete_dir_contents(DIR_DATA)
    else:
        DIR_DATA.mkdir()

    # get pdf
    get_pdf(filing_id)


if __name__ == '__main__':
    main()
