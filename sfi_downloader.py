
from pathlib import Path
from definitions import DIR_DATA
from sfi_downloader.helper.misc import delete_dir_contents
from sfi_downloader.scrape.get_pdf import get_pdf

def main():

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
