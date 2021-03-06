import logging
from datetime import datetime
from definitions import DIR_DATA
from pdf_downloader.helper.misc import delete_dir_contents
from pdf_downloader.scrape.get_pdf import get_pdf
from logs.config.logging import logs_config
import time

def main():

    # init logging
    scrape_start_time = datetime.now()
    logs_config()
    logging.info('Beginning scrape')

    # SET VARS
    # list of target filing IDs
    list_of_filing_ids = [
        "336344",  # samuel doctor
        "331887",  # phil heasley
        "332791",  # Andre Del Valle
        "209028"  # thomas murt
    ]
    sleep_time = 5

    # create or clean up PDF download dir
    if DIR_DATA.is_dir():
        # delete files from previous run
        delete_dir_contents(DIR_DATA)
    else:
        DIR_DATA.mkdir()

    # get pdf
    for filing_id in list_of_filing_ids:
        get_pdf(filing_id)
        # sleep in order to avoid overloading Ethics Commission website
        logging.info(f'Sleeping for {sleep_time} seconds...')
        time.sleep(sleep_time)
        logging.info('...Finished sleeping!')

    # complete
    scrape_end_time = datetime.now()
    scrape_duration = (scrape_end_time - scrape_start_time).total_seconds()
    logging.info(f'Total scrape time: {scrape_duration /60} minutes')
    logging.info(f'Time per item scraped: {round(scrape_duration / len(list_of_filing_ids), 2)} sec')
    logging.info("Scrape complete")


if __name__ == '__main__':
    main()
