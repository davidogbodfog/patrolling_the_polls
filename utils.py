# utils.py

import csv
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


def peru_pull_pdfs(url, acta_range, destination_folder):
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)

    for i in acta_range:
        try:
            print ("getting pdf for acta number:", i)
            driver.get(url)
            acta_number = str(i).zfill(6)
            print (acta_number)

            elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[2]/div/div/div/form/div/input")
            elem.send_keys(acta_number)
            elem.send_keys(Keys.RETURN)

            time.sleep(1.5)

            pdf_elem = driver.find_element_by_xpath("/html/body/onpe-root/onpe-layout-container/onpe-onpe-actas-nume/form/div/div[3]/div[1]/div/div[2]/div/a")
            pdf_url = pdf_elem.get_attribute("href")
            print("pdf url:", pdf_url)
            os.system("curl -o "+destination_folder+"/"+acta_number+".pdf \""+pdf_url +"\"")

        except:
            continue

    driver.close()


def peru_pull_json(url, acta_range, destination_folder):
    for acta_number in acta_range:
        try:
            acta_number = str(acta_number).zfill(6)
            json_url = "https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero/"+acta_number
            os.system("curl -o "+destination_folder+"/"+acta_number+".json "+json_url)

        except:
            print(f"exception pulling json {acta_number}")
            continue


def peru_dump_acta_data_with_locales(acta_range, destination_file, source_dir):
    with open(destination_file, 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['acta_number', 'code', 'locale', 'dept', 'prov', 'dist', 'habiles'])
        for i in acta_range:
            try: 
                acta_number = str(i).zfill(6)
                with open(source_dir+"//"+acta_number+".json", 'r') as f:
                    results = json.loads(f.read())
                    obj = results["procesos"]["regional"]["gobernador"]
                    code = obj["CCODI_UBIGEO"]
                    locale = obj["TNOMB_LOCAL"]
                    dept = obj["DEPARTAMENTO"]
                    prov = obj["PROVINCIA"]
                    dist = obj["DISTRITO"]
                    habiles = obj["NNUME_HABILM"]
                    writer.writerow([acta_number, code, locale.encode('utf-8'), dept.encode('utf-8'), prov.encode('utf-8'), dist.encode('utf-8'), habiles])

                    print(acta_number)
                    print(code)

            except:
                 continue


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
