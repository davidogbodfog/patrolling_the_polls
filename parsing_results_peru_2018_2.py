
# json_look.py
import json
import csv


# this code creates objects, party, gov, and consejero, for each acta number
with open('data2.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['acta_number', 'party', 'gov', 'consejero'])

    for i in reversed(range(1, 900997)):
        try: 
            acta_number = str(i).zfill(6)
            with open("/Users/mollie/Dropbox/personeros2018/"+acta_number+".json", 'r') as f:
                results = json.loads(f.read())

                 #print(json.dumps(results, indent=4))
                #print(results.keys())
                #for k in results.keys():
                 #   print("===")
                  #  print(k)
                   # print(results[k])
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
