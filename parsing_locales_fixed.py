# parsing_locales.py
import json
import csv


# this code creates objects, party, gov, and consejero, for each acta number
with open('locales2.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['acta_number', 'code', 'locale', 'dept', 'prov', 'dist', 'habiles'])

    for i in reversed(range(1, 900997)):
        try: 
            acta_number = str(i).zfill(6)
            with open("/Users/mollie/Dropbox/personeros2018/"+acta_number+".json", 'r') as f:
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



