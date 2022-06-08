# ptp.py - patrolling the polls master script

import argparse
import utils
import os

data_dir = "./tmp_data"

class PeruElectionResultsScraper:
    def __init__(self, name, acta_range, url, json_url, json_goodies_path, overwrite=False, website_version="2021"):
        self.working_dir = data_dir+"/"+name
        self.acta_range = acta_range
        self.url = url
        self.json_url = json_url
        self.json_goodies_path = json_goodies_path
        self.overwrite = overwrite
        self.website_version = website_version

        os.makedirs(self.working_dir, exist_ok=True)
    
    
    def pull_pdfs(self):
        utils.peru_pull_pdfs(
            url=self.url,
            acta_range = self.acta_range,
            destination_folder = self.working_dir,
            overwrite = self.overwrite
        )
        
    def pull_jsons(self):
        utils.peru_pull_json(
            url = self.json_url,
            acta_range = self.acta_range,
            destination_folder = self.working_dir,
            overwrite = self.overwrite,
            website_version = self.website_version
        )

    def dump_csv(self):
        utils.peru_dump_acta_data_with_locales(
            acta_range = self.acta_range,
            source_dir = self.working_dir,
            destination_file = self.working_dir + "/results.csv",
            goodies_path = self.json_goodies_path
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=str,
                        help="name of the job to run")
    args = parser.parse_args()
    if args.job == "peru_regional_and_municipal_2018":
        job = PeruElectionResultsScraper(
            name = args.job,
            acta_range = range(1, 100),
            # acta_range = range(1, 90997),
            url = "https://resultadoshistorico.onpe.gob.pe/PRERM2018/Actas/Numero",
            json_url = "https://resultadoshistorico.onpe.gob.pe/v1/mesas/detalle",
            website_version = "2018",
            json_goodies_path = ["procesos", "regional", "gobernador"]
        )
        job.pull_jsons()
        job.dump_csv()

    elif args.job == "peru_second_presidential_2021":
        job = PeruElectionResultsScraper(
            name = args.job,
            acta_range = range(1, 100),
            # acta_range = range(1, 90997),
            url = "https://resultadoshistorico.onpe.gob.pe/SEP2021/Actas/Numero",
            json_url = "https://resultadoshistorico.onpe.gob.pe/assets/json/SEP2021/mesas/detalle",
            json_goodies_path = ["procesos", "generalPre", "presidencial"]
        )
        job.pull_pdfs()
        job.pull_jsons()
        job.dump_csv()
        

    else:
        raise ValueError(f"unknown job {args.job}")
        
