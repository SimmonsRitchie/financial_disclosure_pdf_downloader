
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
    list_of_filing_ids = [
        "336344",  # samuel doctor
        "331887",  # phil heasley
        "332791"
    ]
    filing_id = "336344"

    # create or clean up PDF download dir
    if DIR_DATA.is_dir():
        # delete files from previous run
        delete_dir_contents(DIR_DATA)
    else:
        DIR_DATA.mkdir()

    # get pdf
    for filing_id in list_of_filing_ids:
        get_pdf(filing_id)

    # complete
    logging.info("Scrape complete")


if __name__ == '__main__':
    main()
