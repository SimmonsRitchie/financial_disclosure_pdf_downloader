import requests
import time
import json
import re
from definitions import DIR_DATA

def get_pdf(filing_id):

    # create a session
    s = requests.Session()

    # get document page
    url = f"https://www.ethicsrulings.pa.gov/WebLink/DocView.aspx?id={filing_id}&dbid=0&repo=EthicsLF8"
    s.get(url)

    # post GeneratedPDF endpoint
    gen_pdf_url = f"https://www.ethicsrulings.pa.gov/WebLink/GeneratePDF10.aspx?key={filing_id}&PageRange=1%20-%206&Watermark=0"
    r = s.post(gen_pdf_url)
    print('GeneratePDF response: ',r.text)

    # get key
    key = r.text.splitlines()[0].strip()
    assert (key), "No key found"

    # view
    print(key)

    # wait for pdf to be downloadable
    check_pdf_generated_url = "https://www.ethicsrulings.pa.gov/WebLink/DocumentService.aspx/PDFTransition"
    payload = {"Key": key}
    try:
        for count in range(0, 2):
            time.sleep(1)
            # r = s.post(check_pdf_generated_url, data=payload)
            payload_str = json.dumps(payload)
            r = s.post(check_pdf_generated_url, data=payload_str)
            r_json = r.json()
            pdf_is_ready = r_json["data"]["success"]
            print(r_json)
            print(r_json["data"]["success"])
            if pdf_is_ready:
                break
    except json.decoder.JSONDecodeError as e:
        print('Error: ',e)
        quit()


    # get pdf
    download_pdf_url = f"https://www.ethicsrulings.pa.gov/WebLink/PDF/{key}/2020" \
                       f"%20William%20Benner.pdf"
    print(download_pdf_url)
    r = s.get(download_pdf_url)
    print(r.headers)
    content_disp = r.headers['content-disposition']
    filing_name = re.findall("filename=(.+)", content_disp)[0].strip('"')
    download_path = DIR_DATA / f"{filing_id}__{filing_name}"
    with open(download_path, 'wb') as f:
        f.write(r.content)