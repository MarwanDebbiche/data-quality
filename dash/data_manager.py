import pandas as pd
import pandas_profiling
import pickle
import os
import base64
import io


class DataManager:
    DATA_PATH = "data"

    def __init__(self):
        if os.path.exists(f"{self.DATA_PATH}/df.csv"):
            self.data = pd.read_csv(f"{self.DATA_PATH}/df.csv")
            if not os.path.exists(f"{self.DATA_PATH}/profile_report.pickle"):
                self.profile_report = self._generate_report()
                self._save_data()
            else:
                with open(f"{self.DATA_PATH}/profile_report.pickle", "rb") as f:
                    self.profile_report = pickle.load(f)
        else:
            self.data = None
            self.profile_report = None

    def _generate_report(self):
        return self.data.profile_report(style={'full_width':True})

    def _save_data(self):
        if self.data is not None:
            self.data.to_csv(f"{self.DATA_PATH}/df.csv", index=False)
            with open(f"{self.DATA_PATH}/profile_report.pickle", "wb") as f:
                pickle.dump(self.profile_report, f)

    def process_file(self, content, filename, overwrite=False):
        if self.data is None:
            overwrite = True

        _, content_string = content.split(",")
        decoded = base64.b64decode(content_string)

        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep=None, engine='python')
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))

        if overwrite:
            self.data = df
        else:
            self.data = pd.concat([self.data, df]).reset_index(drop=True)

        self.profile_report = self._generate_report()
        self._save_data()

    def get_dataset_stats(self, n_top_var_w_missing_val=5):
        n_obs, n_var = self.data.shape
        missing_count = self.data.isna().sum().sum()
        missing_count_percent = 100.0 * self.data.isna().sum().sum() / (n_obs * n_var)
        missing_count_per_var = self.data.isna().sum().sort_values(ascending=False)
        variables_with_missing_values = (
            pd.DataFrame(
                missing_count_per_var[missing_count_per_var > 0]
                .head(n_top_var_w_missing_val)
            )
            .reset_index()
            .rename(columns={"index": "variable", 0: "count"})
            .to_dict(orient="records")
        )
        return {
            "n_obs": n_obs, "n_var": n_var,
            "missing_count": missing_count,
            "missing_count_percent": missing_count_percent,
            "variables_with_missing_values": variables_with_missing_values
        }


class SimpleDataManager:
    DATA_PATH = "data"

    def __init__(self):
        if os.path.exists(f"{self.DATA_PATH}/df.csv"):
            self.data = pd.read_csv(f"{self.DATA_PATH}/df.csv")
        else:
            self.data = None

    def _save_data(self):
        if self.data is not None:
            self.data.to_csv(f"{self.DATA_PATH}/df.csv", index=False)

    def process_file(self, content, filename, overwrite=False):
        if self.data is None:
            overwrite = True

        _, content_string = content.split(",")
        decoded = base64.b64decode(content_string)

        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep=None, engine='python')
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))

        if overwrite:
            self.data = df
        else:
            self.data = pd.concat([self.data, df]).reset_index(drop=True)

        self._save_data()

    def generate_profiling_report(self, save=True):
        profile = self.data.profile_report(title='Profiling Report')
        if save:
            profile.to_file(output_file=f"{self.DATA_PATH}/profiling-report.html")

        return profile

    def get_dataset_stats(self, n_top_var_w_missing_val=5):
        n_obs, n_var = self.data.shape
        missing_count = self.data.isna().sum().sum()
        missing_count_percent = 100.0 * self.data.isna().sum().sum() / (n_obs * n_var)
        missing_count_per_var = self.data.isna().sum().sort_values(ascending=False)
        variables_with_missing_values = (
            pd.DataFrame(
                missing_count_per_var[missing_count_per_var > 0]
                .head(n_top_var_w_missing_val)
            )
            .reset_index()
            .rename(columns={"index": "variable", 0: "count"})
            .to_dict(orient="records")
        )
        return {
            "n_obs": n_obs, "n_var": n_var,
            "missing_count": missing_count,
            "missing_count_percent": missing_count_percent,
            "variables_with_missing_values": variables_with_missing_values
        }


if __name__ == "__main__":
    data_manager = DataManager()
