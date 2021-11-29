from dataclasses import dataclass
from apyori import apriori
from app.models import SingletonModel
import pandas as pd
import psycopg2 as pg
import os
from sklearn.cluster import DBSCAN
import hashlib

@dataclass(frozen=True)
class Rule:
    antecedent: set
    consequent: str
    confidence: float

    def match(self, pred: dict) -> bool:
        pred_set = set(pred.values())
        return self.antecedent.issubset(pred_set)

    def to_json(self):
        return {
            "antecedent": list(self.antecedent),
            "consequent": self.consequent,
            "confidence": self.confidence,
        }



class ModelDBSCAN(metaclass=SingletonModel):
    _columns_drop = [
        "signup_md_key_ups",
        "signup_md_key_downs"
    ]

    def __init__(self) -> None:
        self.conn = self.connect_db()

    def connect_db(self):
        pg_user = os.getenv("PG_USER")
        pg_pwd = os.getenv("PG_PWD")
        pg_host = os.getenv("PG_HOST")
        pg_port = os.getenv("PG_PORT")
        pg_dbname = os.getenv("PG_DBNAME")
        return pg.connect(f"dbname='{pg_dbname}' user='{pg_user}' host='{pg_host}' port='{pg_port}' password='{pg_pwd}'")

    def predict(self, pred: dict) -> list[dict]:
        self.df = self.get_dataframe()
        self.add_pred(pred)
        self.model = self._build_model()
        self._build_rules()
        pred =  self.model.labels_[-1]
        print(self.model.labels_)
        return hashlib.blake2b(str(pred).encode(), digest_size=5).hexdigest()

    def get_dataframe(self):
        sql = "SELECT signup_md_key_ups, signup_md_key_downs FROM signup_metadata"
        df = pd.read_sql(sql, con=self.conn)
        key_ups_columns = df['signup_md_key_ups'].apply(pd.Series)
        key_downs_columns = df['signup_md_key_downs'].apply(pd.Series)
        df = pd.concat([df, key_ups_columns], axis=1)
        df = pd.concat([df, key_downs_columns], axis=1)
        df.drop(columns=self._columns_drop, inplace=True)
        n = len(df.columns)
        cols = []
        for i, col in enumerate(df.columns):
            if i < (n // 2):
                cols.append("UP" + str(col))
            else:
                cols.append("DOWN" + str(col))    
        df.columns = cols
        df.fillna(0, inplace=True)
        return df
    
    def add_pred(self, pred):
        cols = len(self.df.columns)
        print(len(pred["keyups"]) + len(pred["keydowns"]), cols)
        line = list(pred["keyups"]) + pred["keydowns"]
        row = len(self.df)
        self.df.loc[row] = line

    def _build_model(self):
        return DBSCAN(eps=210,min_samples=2,algorithm='auto')
    
    def _build_rules(self):
        self.model.fit(self.df)
        return 

    @property
    def records(self):
        return [[str(cell) for cell in line] for line in self.df.to_numpy()]
