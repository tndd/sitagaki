from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SQLAlchemyClient:
    def __init__(self, engine):
        pass

    def insert_models(self, models):
        pass

    def execute_query(self, query):
        pass
