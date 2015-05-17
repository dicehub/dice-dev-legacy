# Standard Python modules
# =======================
import os
import csv


class DakotaTableCsv:
    def __init__(self, path, table_dat_name="table_out.dat", table_csv_name="table_out.csv"):
        self.path = path
        self.table_dat_name = table_dat_name
        self.table_csv_name = table_csv_name

        self.table_file_full_path = os.path.join(path, table_dat_name)
        self.csv_file_full_path = os.path.join(path, table_csv_name)

        if not os.path.exists(self.csv_file_full_path):
            if os.path.exists(self.table_file_full_path):
                self.convert_table_to_csv(self.table_file_full_path, self.csv_file_full_path)

    @staticmethod
    def convert_table_to_csv(file_in_path, file_out_path):
        with open(file_in_path) as fin, open(file_out_path, 'w') as fout:
            o = csv.writer(fout)
            for line in fin:
                o.writerow(line.split())