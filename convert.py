import csv
import sys
from os import listdir
from os.path import isfile, join
import logging


def convert_csv(csv_file, scrape_dir):
    csv.field_size_limit(sys.maxsize)

    existing_files = [f.rsplit('.', 1)[1] for f in listdir(scrape_dir) if isfile(join(scrape_dir, f))]
    idx = max(int(x) for x in existing_files if x.isdigit()) + 1

    with open(csv_file) as file:
        reader = csv.reader(file)

        for row in reader:
            current_file = f"{scrape_dir}/swagger.json.{idx}"

            try:
                with open(current_file, "x") as f:
                    f.write(row[2])

                logging.info(f"Wrote {current_file} from csv: {csv_file}")
            except FileExistsError:
                logging.warning(f"Failed to write {current_file} from csv: {csv_file}")
                continue
            finally:
                idx += 1
