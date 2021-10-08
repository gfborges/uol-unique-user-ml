from dataclasses import dataclass
from apyori import apriori
from app.models import SingletonModel
import pandas as pd
import psycopg2 as pg
import os

@dataclass(frozen=True)
class Rule:
    antecedent: set
    consequent: str
    confidence: float

    def match(self, pred: dict) -> bool:
        pred_set = pred.items()
        return self.antecedent.issubset(pred_set)

    def to_json(self):
        return {
            "antecedent": self.antecedent,
            "consequent": self.consequent,
            "confidence": self.confidence,
        }
        
class DeviceModel(metaclass=SingletonModel):
    _column_to_drop=[
        'user_id',
        'signup_md_id',
        'signup_md_end_date',
        'signup_md_start_date',
        'signup_md_paste_count',
        'user_phone',
        'user_email',
        'user_name',
        'user_is_admin',
        'signup_md_device_name', 
        'signup_md_cpu_cores',
        'user_password'
    ]

    def __init__(self) -> None:
        self.df = self.get_dataframe()
        self.model = self._build_model()
        self.rules: list[Rule] = self._build_rules()


    def connect_db(self):
        pg_user = os.getenv("PG_USER")
        pg_pwd = os.getenv("PG_PWD")
        pg_host = os.getenv("PG_HOST")
        pg_port = os.getenv("PG_PORT")
        pg_dbname = os.getenv("PG_DBNAME")
        return pg.connect(f"dbname='{pg_dbname}' user='{pg_user}' host='{pg_host}' port='{pg_port}' password='{pg_pwd}'")


    def get_dataframe(self):
        sql = "SELECT * FROM users JOIN signup_metadata USING(user_id)"
        df = pd.read_sql(sql, con=self.connect_db())
        df.drop(columns=self._column_to_drop, inplace=True)
        return df


    @property
    def records(self):
        return [[str(cell) for cell in line] for line in self.df.to_numpy()]


    def _build_model(self):
        return apriori(self.records, min_length=2, min_support=0.2, min_confidence=0.2, min_lift=3)
    
    def _build_rules(self):
        rules = []
        deviceIds = frozenset(self.df['signup_md_device_id'].unique())
        for record in self.model:
            for stat in record.ordered_statistics:
                if stat.items_add.issubset(deviceIds):
                    rule = Rule(
                        confidence=stat.confidence,
                        antecedent=stat.items_base,
                        consequent=stat.items_add,
                    )
                    rules.append(rule)
        return rules
    
    def predict(self, pred: dict) -> list[dict]:
        matches = set([rule for rule in self.rules if rule.match(pred)])
        return [rule.to_json() for rule in matches]