import csv
import pandas as pd
import numpy as np
import random
from sdeutils.file.field.cast.cast import Cast

MAX_ROW_NB = 100


class CsvFile:
    def __init__(self, path):
        self.path = path
        self.row_nb = None
        self.df = None
        self.df_sample = None
        with open(path, errors="ignore", encoding="utf-8-sig") as csv_file:
            sniffer = csv.Sniffer()
            csv_file_lines = csv_file.readlines(100)
            csv_file_sample = "\n".join(csv_file_lines)
            self.dialect = sniffer.sniff(csv_file_sample)
            self.has_header = sniffer.has_header(csv_file_sample)
            self.delimiter = self.dialect.delimiter
            self.quotechar = self.dialect.quotechar
            self.escapechar = self.dialect.escapechar

            if self.has_header:
                csv_file.seek(0)
                reader = csv.reader(csv_file, self.dialect)
                self.header = next(reader)
            else:
                self.header = None

    def get_basic_info(self):
        res = {}
        res["has_header"] = self.has_header
        res["delimiter"] = self.delimiter
        res["quotechar"] = self.quotechar
        res["escapechar"] = self.escapechar

        return res

    def get_fields_info(self):
        res = {}
        header_count = 1
        df = self.get_df_sample()

        for c in df.columns:
            if self.has_header:
                h = c
            else:
                h = "col_{}"
                header_count += 1
            res[h] = {}
            res[h]["field_name"] = c
            res[h]["values"] = list(df[c])
            res[h]["cast_repartition"] = Cast.cast_list(
                [Cast(elt) for elt in res[h]["values"]]
            )

        return res

    def get_df(self):
        if self.df is not None:
            return self.df
        else:
            arg = {"dialect": self.dialect, "error_bad_lines": False}
            self.df = pd.read_csv(self.path, **arg)
            self.df = self.df.replace(np.nan, "", regex=True)
            return self.df

    # def get_df_casted(self):
    #     arg = {"dialect": self.dialect, "error_bad_lines": False}
    #     self.df = pd.read_csv(self.path, **arg)
    #     self.df = self.df.replace(np.nan, "", regex=True)
    #
    #     for col in self.df.columns:
    #         field = Field(list(self.df[col]))
    #         est_cst = field.estimated_cast
    #
    #     return self.df

    def get_df_sample(self, max_row_nb=MAX_ROW_NB):
        row_nb = self.get_row_nb()
        df = self.get_df()
        if row_nb > max_row_nb:
            ids = random.sample(range(row_nb), max_row_nb)
            self.df_sample = df.iloc[ids].reset_index(drop=True)
            return self.df_sample
        else:
            self.df_sample = self.df
            return self.df_sample

    def get_row_nb(self):
        if self.row_nb:
            return self.row_nb
        else:
            if self.df is not None:
                self.row_nb = len(self.df.index)
            else:
                h = 0
                if self.has_header:
                    h = 1
                with open(self.path, errors="ignore") as csv_file:
                    self.row_nb = len(csv_file.readlines()) - h
        return self.row_nb

    def __str__(self):
        attr_dict = self.__dict__
        all_attr = attr_dict.keys()
        attr_to_disp = [attr for attr in all_attr if attr not in ["dialect"]]
        res = []
        for attr in attr_to_disp:
            res.append("{}: {}".format(attr, attr_dict[attr]))

        return "\n".join(res)


if __name__ == "__main__":
    path = r"C:\Users\sebde\PycharmProjects\monus\data\E1366516.csv"
    csv_file = CsvFile(path)

    print(csv_file.get_df())

    # df = csv_file.get_df_casted()
