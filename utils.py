# utils.py

import csv
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

def cleanup(folder, delete_invalid=True):
    # check for broken spans
    acta_range = range(100000)
    most_recent_found = -1
    for i in acta_range:
        json_filename = f"{folder}/{str(i).zfill(6)}.json"
        if os.path.exists(json_filename):
            if most_recent_found != i-1:
                print(f"missing json span {folder}: {most_recent_found+1} - {i}")
            most_recent_found = i
    print(f"missing json span {folder}: {most_recent_found+1} - {i}")


    most_recent_found = -1
    for i in acta_range:
        pdf_filename = f"{folder}/{str(i).zfill(6)}.pdf"
        if os.path.exists(pdf_filename):
            if most_recent_found != i-1:
                print(f"missing pdf span {folder}: {most_recent_found+1} - {i}")
            most_recent_found = i
    print(f"missing pdf span {folder}: {most_recent_found+1} - {i}")
    
        
    # check for invalid files
    for i, f in enumerate(os.listdir(folder)):
        if f.endswith(".json"):
            with open(f"{folder}/{f}", 'r') as jsonfile:
                data = jsonfile.read()
            try:
                json.loads(data)
            except:
                print(f"{folder}/{f} not json. deleting")
                if delete_invalid:
                    os.remove(f"{folder}/{f}")
                    
        elif f.endswith(".pdf"):
            with open(f"{folder}/{f}", 'rb') as pdffile:
                data = pdffile.read()
            if not data.startswith(b"%PDF"):
                print(f"{folder}/{f} not a pdf")
                if delete_invalid:
                    os.remove(f"{folder}/{f}")
                


def peru_pull_pdfs(url, acta_range, destination_folder, overwrite=False):
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)

    for i in acta_range:
        acta_number = str(i).zfill(6)
        outfile = destination_folder+"/"+acta_number+".pdf"
        if not overwrite and os.path.exists(outfile):
            continue
        print("pulling pdf", acta_number)
        try:
            print ("getting pdf for acta number:", acta_number)
            driver.get(url)

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
        print("pulling json", acta_number)
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


def peru_dump_locales(acta_range, destination_file, source_dir, election):
    with open(destination_file, 'w',) as csvfile:
        locales_writer = csv.writer(csvfile)
        locales_writer.writerow(['acta_number', 'code', 'locale', 'dept', 'prov', 'dist', 'habiles'])
        
        for i in acta_range:
            acta_number = str(i).zfill(6)
            try: 
                with open(source_dir+"//"+acta_number+".json", 'r') as f:
                    base_obj = json.loads(f.read())
                    if election == "president":
                        obj = base_obj["procesos"]["generalPre"]["presidencial"]
                    elif election == "regional":
                        obj = base_obj["procesos"]["regional"]["gobernador"]
                        
                    code = obj["CCODI_UBIGEO"]
                    locale = obj["TNOMB_LOCAL"]
                    dept = obj["DEPARTAMENTO"]
                    prov = obj["PROVINCIA"]
                    dist = obj["DISTRITO"]
                    habiles = obj["NNUME_HABILM"]
                    
                    locales_writer.writerow([acta_number, code, locale.encode('utf-8'), dept.encode('utf-8'), prov.encode('utf-8'), dist.encode('utf-8'), habiles])

            except Exception as e:
                 print(f"exception dumping locales for acta {i}: {e}")


def peru_dump_votes(acta_range, destination_file, source_dir, election):
    with open(destination_file, 'w') as csvfile:
        votes_writer = csv.writer(csvfile)
        if election == "president":
            votes_writer.writerow(['acta_number', 'party', 'presidente'])
        elif election == "regional":
            votes_writer.writerow(['acta_number', 'party', 'gobernador', 'consejero'])

        for i in acta_range:
            acta_number = str(i).zfill(6)
            try: 
                with open(source_dir+"//"+acta_number+".json", 'r') as f:
                    base_obj = json.loads(f.read())
                    if election == "president":
                        votos_arr = base_obj["procesos"]["generalPre"]["votos"]
                    elif election == "regional":
                        votos_arr = base_obj["procesos"]["regional"]["votos"]

                    for obj in votos_arr:
                        party = obj["AUTORIDAD"]
                        if election == "president":
                            pres = obj["congresal"]
                            votes_writer.writerow([acta_number, party, pres])
                        elif election == "regional":
                            gob = obj["Gobernador"]
                            cons = obj["Consejero"]
                            votes_writer.writerow([acta_number, party, gob, cons])
                        
            except Exception as e:
                 print(f"exception dumping votes for acta {i}: {e}")

