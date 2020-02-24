import requests
import time
import json
import re
import logging
from definitions import DIR_DATA
import urllib.parse as parse

def get_pdf(filing_id, page_range = "",watermark="0"):

    logging.info(f'Scraping SFI with ID: {filing_id}')

    # encode URL fragments
    page_range_encoded = parse.quote(page_range)
    watermark_encoded = parse.quote(watermark)

    # create a session
    s = requests.Session()

    # get document page
    # we access this endpoint in order to get cookies that we need to generate a key
    logging.info("Send GET request to DocView page...")
    url = f"https://www.ethicsrulings.pa.gov/WebLink/DocView.aspx?id={filing_id}&dbid=0&repo=EthicsLF8"
    r = s.get(url)
    assert (r.status_code == 200), "Error accessing DocView page"

    # post GeneratedPDF endpoint
    # we access this endpoint in order to get a key from the response body that we will use to get the actual PDF
    logging.info("Send POST request to GeneratePDF endpoint...")

    gen_pdf_url = f"https://www.ethicsrulings.pa.gov/WebLink/GeneratePDF10.aspx?key={filing_id}&PageRange=" \
                  f"{page_range_encoded}&Watermark={watermark_encoded}"
    r = s.post(gen_pdf_url)
    assert (r.status_code == 200), "Error accessing GeneratedPDF endpoint"

    # get key
    # The response body we get appears to be malformed: you'll get a key in the first line and then some html junk.
    # We get the key by just taking the first line.
    key = r.text.splitlines()[0].strip()
    assert (key), "No key found"

    # double check what our key looks like, should be something like: c307abb8-3d15-4cbf-95f3-b2f4f91a374f​
    logging.info(f"Key provided: {key}")

    # wait for pdf to be downloadable
    # the resource at this endpoint tells the client whether the PDF is ready to download. We keep checking it
    # until it tells us the PDF is ready.
    check_pdf_generated_url = "https://www.ethicsrulings.pa.gov/WebLink/DocumentService.aspx/PDFTransition"
    payload = {"Key": key}
    logging.info("Waiting for PDF to be generated...")
    max_iterations_to_wait = 5
    sleep_time = 1
    try:
        for count in range(0, max_iterations_to_wait):
            time.sleep(sleep_time)
            payload_str = json.dumps(payload)
            r = s.post(check_pdf_generated_url, data=payload_str)
            r_json = r.json()
            pdf_is_ready = r_json["data"]["success"]
            if pdf_is_ready:
                logging.info("PDF ready for download!")
                break
            else:
                logging.info("PDF not ready for download, waiting further...")
        else:
            logging.error(f'Timeout: PDF not ready after {max_iterations_to_wait * sleep_time} seconds')
    except json.decoder.JSONDecodeError as e:
        logging.error(e)
        quit()

    # get pdf
    # we access a different endpoint to download the actual PDF. The end part of the URL - filename - seems to be
    # arbitrary. You can use any word here as long as it ends with '.pdf' and the file will download. The
    # important thing is the key in the URL.
    filename = f"{filing_id}.pdf"
    logging.info('Downloading PDF...')
    download_pdf_url = f"https://www.ethicsrulings.pa.gov/WebLink/PDF/{key}/{filename}"
    r = s.get(download_pdf_url)
    assert (r.status_code == 200), "Something went wrong with PDF download"
    download_path = DIR_DATA / filename
    with open(download_path, 'wb') as f:
        f.write(r.content)
        logging.info(f'PDF downloaded as: {filename}')