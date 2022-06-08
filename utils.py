# utils.py

import csv
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


def peru_pull_pdfs(url, acta_range, destination_folder, overwrite=False):
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)

    for i in acta_range:
        acta_number = str(i).zfill(6)
        outfile = destination_folder+"/"+acta_number+".pdf"
        if not overwrite and os.path.exists(outfile):
            continue
        try:
            print ("getting pdf for acta number:", i)
            driver.get(url)
            print (acta_number)

            elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[2]/div/div/div/form/div/input")
            elem.send_keys(acta_number)
            elem.send_keys(Keys.RETURN)

            time.sleep(1.5)

            pdf_elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[3]/div[1]/div/div[2]/div/a")
            pdf_url = pdf_elem.get_attribute("href")
            print("pdf url:", pdf_url)
            os.system("curl -o "+outfile+" \""+pdf_url +"\"")

        except:
            continue

    driver.close()


def peru_pull_json(url, acta_range, destination_folder, overwrite=False, website_version="2021"):
    for acta_number in acta_range:
        acta_number = str(acta_number).zfill(6)
        outfile = f"{destination_folder}/{acta_number}.json"
        if not overwrite and os.path.exists(outfile):
            continue
        try:
            if website_version == "2021":
                json_url = url+"/"+acta_number+".json"
            elif website_version == "2018":
                json_url = url+"/"+acta_number
            header = "-H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0'"
            cmd = f"curl {header} -o {outfile} {json_url}"
            os.system(cmd)

        except:
            print(f"exception pulling json {acta_number}")
            continue


def peru_dump_acta_data_with_locales(acta_range, destination_file, source_dir, goodies_path):
    with open(destination_file, 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['acta_number', 'code', 'locale', 'dept', 'prov', 'dist', 'habiles'])
        for i in acta_range:
            try: 
                acta_number = str(i).zfill(6)
                with open(source_dir+"//"+acta_number+".json", 'r') as f:
                    obj = json.loads(f.read())
                    for item in goodies_path:
                        obj = obj[item]
                    code = obj["CCODI_UBIGEO"]
                    locale = obj["TNOMB_LOCAL"]
                    dept = obj["DEPARTAMENTO"]
                    prov = obj["PROVINCIA"]
                    dist = obj["DISTRITO"]
                    habiles = obj["NNUME_HABILM"]
                    writer.writerow([acta_number, code, locale.encode('utf-8'), dept.encode('utf-8'), prov.encode('utf-8'), dist.encode('utf-8'), habiles])

            except Exception as e:
                 print(e)


def peru_2018():
    # note: not used or working, just saving this for the record
    with open('data2.csv', 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['acta_number', 'party', 'gov', 'consejero'])

        for i in reversed(range(1, 900997)):
            try: 
                acta_number = str(i).zfill(6)
                with open(source_dir+"/"+acta_number+".json", 'r') as f:
                    results = json.loads(f.read())
                    for obj in results["procesos"]["regional"]["votos"]:
                        party = obj["AUTORIDAD"]
                        gov = obj["Gobernador"]
                        consejero = obj["Consejero"]     
                        writer.writerow([acta_number, party, gov, consejero])

                        print(party)
                        print(gov)
                        print(consejero)

            except:
                 continue
