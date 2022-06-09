# ptp.py - patrolling the polls master script

import argparse
import utils
import os

data_dir = "./tmp_data"

class PeruElectionResultsScraper:
    def __init__(self, name, acta_range, url, json_url, election, overwrite=False, website_version="2021"):
        self.working_dir = data_dir+"/"+name
        self.acta_range = acta_range
        self.url = url
        self.json_url = json_url
        self.election = election
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

    def dump_csvs(self):
        utils.peru_dump_locales(
            acta_range = self.acta_range,
            source_dir = self.working_dir,
            destination_file = self.working_dir + "/locales.csv",
            election = self.election
        )

        utils.peru_dump_votes(
            acta_range = self.acta_range,
            source_dir = self.working_dir,
            destination_file = self.working_dir + "/votes.csv",
            election = self.election
        )
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=str,
                        help="name of the job to run")
    args = parser.parse_args()
    if args.job == "peru_regional_and_municipal_2018":
        job = PeruElectionResultsScraper(
            name = args.job,
            acta_range = range(1, 91000),
            url = "https://resultadoshistorico.onpe.gob.pe/PRERM2018/Actas/Numero",
            json_url = "https://resultadoshistorico.onpe.gob.pe/v1/mesas/detalle",
            website_version = "2018",
            election = "regional",
        )
        job.pull_jsons()
        job.dump_csvs()

    elif args.job == "peru_second_presidential_2021":
        job = PeruElectionResultsScraper(
            name = args.job,
            acta_range = range(1, 91000),
            url = "https://resultadoshistorico.onpe.gob.pe/SEP2021/Actas/Numero",
            json_url = "https://resultadoshistorico.onpe.gob.pe/assets/json/SEP2021/mesas/detalle",
            election = "president",
        )
        job.pull_pdfs()
        job.pull_jsons()
        job.dump_csvs()
        

    else:
        raise ValueError(f"unknown job {args.job}")
        
