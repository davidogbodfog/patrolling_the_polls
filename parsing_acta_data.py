
# json_look.py
import json
#"/Users/mollie/Dropbox/ancash2018/000957.json" = "acta_num.json"

with open("/Users/mollie/Dropbox/ancash2018/000957.json", 'r') as f:
    results = json.loads(f.read())
    print(json.dumps(results, indent=4))
    print(results.keys())
    for k in results.keys():
        print("===")
        print(k)
        print(results[k])
    for obj in results["procesos"]["regional"]["consejero"]["votos"]:
        party = obj["AUTORIDAD"]
        gov = obj["Gobernador"]
        consejero = obj["Consejero"]
        

