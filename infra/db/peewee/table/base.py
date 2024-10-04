from peewee import DatabaseProxy, Model

DB_PROXY = DatabaseProxy()


class PeeweeTable(Model):
    class Meta:
        database = DB_PROXY