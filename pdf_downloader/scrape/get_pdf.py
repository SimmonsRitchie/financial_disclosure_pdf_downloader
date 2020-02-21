import requests
import time
import json
import re
import logging
from definitions import DIR_DATA


def get_pdf(filing_id):

    logging.info(f'Scraping SFI with ID: {filing_id}')

    # create a session
    s = requests.Session()

    # get document page
    logging.info("GET DocView page...")
    url = f"https://www.ethicsrulings.pa.gov/WebLink/DocView.aspx?id={filing_id}&dbid=0&repo=EthicsLF8"
    r = s.get(url)
    assert (r.status_code == 200), "Error accessing DocView page"

    # post GeneratedPDF endpoint
    logging.info("POST GeneratePDF endpoint...")
    gen_pdf_url = f"https://www.ethicsrulings.pa.gov/WebLink/GeneratePDF10.aspx?key={filing_id}&PageRange=1%20-%206&Watermark=0"
    r = s.post(gen_pdf_url)
    assert (r.status_code == 200), "Error accessing GeneratedPDF endpoint"

    # get key
    key = r.text.splitlines()[0].strip()
    assert (key), "No key found"

    # view
    logging.info(f"Key provided: {key}")

    # wait for pdf to be downloadable
    check_pdf_generated_url = "https://www.ethicsrulings.pa.gov/WebLink/DocumentService.aspx/PDFTransition"
    payload = {"Key": key}
    logging.info("Waiting for PDF to be generated...")
    max_iterations_to_wait = 5
    sleep_time = 1
    try:
        for count in range(0, max_iterations_to_wait):
            time.sleep(sleep_time)
            # r = s.post(check_pdf_generated_url, data=payload)
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
    logging.info('Downloading PDF...')
    download_pdf_url = f"https://www.ethicsrulings.pa.gov/WebLink/PDF/{key}/2020" \
                       f"%20William%20Benner.pdf"
    r = s.get(download_pdf_url)
    assert (r.status_code == 200), ""
    content_disp = r.headers['content-disposition']
    filing_name = re.findall("filename=(.+)", content_disp)[0].strip('"')
    filename = f"{filing_id}__{filing_name}"
    download_path = DIR_DATA / filename
    with open(download_path, 'wb') as f:
        f.write(r.content)
        logging.info(f'PDF downloaded as: {filename}')