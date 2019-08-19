import sys
import os
import warnings
import pandas as pd

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from data.data_utils import schema_heuristics

data_folder = os.path.abspath("../example_data")


# Schema inference should at least be able to handle the easy cases
class TestSchemaInference:

    def test_iris_dataset(self):
        df = pd.read_csv(os.path.join(data_folder, "iris.csv"))

        types, subtypes = schema_heuristics.infer_types(df, is_sample=False)

        assert types["sepal_length"] == "float"
        assert types["sepal_width"] == "float"
        assert types["petal_length"] == "float"
        assert types["petal_width"] == "float"
        assert types["species"] == "categorical"

    def test_churn_dataset(self):
        df = pd.read_csv(os.path.join(data_folder, "churn.csv"))

        types, subtypes = schema_heuristics.infer_types(df, is_sample=False)

        assert types["number_vmail_messages"] == "integer"
        assert types["total_day_minutes"] == "float"
        assert types["international_plan"] == "categorical"
        assert subtypes["international_plan"] == "binary"
        assert types["churn"] == "categorical"
        assert subtypes["churn"] == "binary"

    def test_gtd_dataset(self):
        df = pd.read_csv(os.path.join(data_folder, "gtd_11to14_0615dist.csv"))
        sample = df.sample(n=50, replace=True)

        types, subtypes = schema_heuristics.infer_types(sample, is_sample=True)

        assert types["summary"] == "string"
        assert types["latitude"] == "float"
        assert types["longitude"] == "float"
        assert subtypes["latitude"] == "latitude"
        assert subtypes["longitude"] == "longitude"

