# ptp.py - patrolling the polls master script

import argparse
import utils

data_dir = "./tmp_data"

class Peru2021Scraper:
    def pull_pdfs(self):
        utils.peru_pull_pdfs(
            url="https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero/",
            # actual:
            # acta_range = range(75000, 84000),
            acta_range = range(75000, 75010),
            destination_folder = data_dir
        )
        
    def pull_jsons(self):
        utils.peru_pull_json(
            url = "https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/Actas/Numero/",
            acta_range = range(1,20),
            destination_folder = data_dir
        )

    def dump_csv(self):
        utils.peru_dump_acta_data_with_locales(
            acta_range = range(1, 90997),
            source_dir = data_dir,
            destination_file = data_dir + "/results.csv"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=str,
                        help="name of the job to run")
    args = parser.parse_args()
    if args.job == "peru_2021":
        job = Peru2021Scraper()
    else:
        raise ValueError(f"unknown job {args.job}")
        
    job.pull_pdfs()
    job.pull_jsons()
    job.dump_csv()
