from peewee import Model, CharField, ForeignKeyField
from peewee_async import PooledPostgresqlDatabase

db = PooledPostgresqlDatabase(
    'iot_management',
    user='iot_user',
    password='199400',
    host='localhost',
    port=5432
)

class BaseModel(Model):
    class Meta:
        database = db

class ApiUser(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

class Location(BaseModel):
    name = CharField()

class Device(BaseModel):
    name = CharField()
    type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(ApiUser, backref='devices')

def create_tables():
    with db:
        db.create_tables([ApiUser, Location, Device])

if __name__ == '__main__':
    create_tables()
