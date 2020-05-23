import csv
import pandas as pd
import numpy as np
import random
from sdeutils.file.field.column_field import ColumnField

MAX_ROW_NB = 100


class CsvFile:
    def __init__(self, path):
        self.path = path
        self.row_nb = None
        self.df = None
        with open(path, errors="ignore", encoding="utf-8-sig") as csv_file:
            sniffer = csv.Sniffer()
            csv_file_lines = csv_file.readlines(10)
            csv_file_sample = "\n".join(csv_file_lines)
            self.dialect = sniffer.sniff(csv_file_sample)
            self.delimiter = self.dialect.delimiter
            self.quotechar = self.dialect.quotechar
            self.escapechar = self.dialect.escapechar
            self.has_header = self.get_has_header()

            if self.has_header:
                csv_file.seek(0)
                reader = csv.reader(csv_file, self.dialect)
                self.header = next(reader)
            else:
                self.header = None

    def get_has_header(self):
        df = pd.read_csv(self.path, sep=self.delimiter, nrows=100, header=None)
        first_row = df.iloc[[0]]
        other_rows = df.iloc[1:-1]

        header_result = 0

        for col in df.columns:
            header = list(first_row[col])[0]
            col_values = list(other_rows[col])
            col_obj = ColumnField(col_values)
            is_header = col_obj.get_header_compatibility(header)

            if is_header:
                header_result += 1
            else:
                header_result -= 1

        if header_result > 0:
            return True
        else:
            return False

    def get_basic_info(self):
        res = {}
        res["has_header"] = self.has_header
        res["delimiter"] = self.delimiter
        res["quotechar"] = self.quotechar
        res["escapechar"] = self.escapechar

        return res

    def get_fields_info(self):
        row_nb = self.get_row_nb()
        df = self.get_converted_df()
        res = []
        res.append("row nb: {}".format(row_nb))
        res.append("col nb: {}".format(len(df.columns)))
        for c in df.columns:
            res.append("*" * 10)
            res.append("column name: {}".format(c))
            res.append("column type: {}".format(df[c].dtype))

        return "\n".join(res)

    def get_converted_df(self, max_row_nb=None):
        dataset = {}
        try:
            if self.df is None:
                self.df = self.get_df()
        except Exception:
            print("self.df already exists")

        df = self.get_df(max_row_nb=max_row_nb)

        for c in df.columns:
            col = ColumnField(list(df[c]))
            value_list = col.refined_values
            dataset[c] = value_list

        return pd.DataFrame(data=dataset)

    def get_df(self, max_row_nb=None):
        try:
            if self.df is None:
                if self.has_header:
                    header = 0
                else:
                    header = None
                arg = {
                    "dialect": self.dialect,
                    "error_bad_lines": False,
                    "header": header,
                }
                self.df = pd.read_csv(self.path, **arg)
                self.df = self.df.replace(np.nan, "", regex=True)
        except Exception:
            print("self.df already exists")

        if max_row_nb is None:
            return self.df
        else:
            row_nb = self.get_row_nb()
            if row_nb > max_row_nb:
                ids = random.sample(range(row_nb), max_row_nb)
                df_sample = self.df.iloc[ids].reset_index(drop=True)
                return df_sample
            else:
                return self.df

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
