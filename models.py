from peewee import Model, CharField, ForeignKeyField
from peewee_async import PooledPostgresqlDatabase

db = PooledPostgresqlDatabase(
    'iot_management',
    user='iot_user',
    password='199400',
    host='localhost',
    port=5432
)

test_db = PooledPostgresqlDatabase(
    'test_global_mindass',
    user='kittgt',
    password='kittgt',
    host='localhost',
    port=5432
)


class BaseModel(Model):
    class Meta:
        database = db


class BaseModelForTest(Model):
    class Meta:
        database = test_db


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
    location = ForeignKeyField(Location, backref='devices', on_delete='CASCADE')
    api_user = ForeignKeyField(ApiUser, backref='devices', on_delete='CASCADE')


class ApiUserTest(BaseModelForTest):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()


class LocationTest(BaseModelForTest):
    name = CharField()


class DeviceTest(BaseModelForTest):
    name = CharField()
    type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(LocationTest, backref='devices')
    api_user = ForeignKeyField(ApiUserTest, backref='devices')


def create_tables():
    with db:
        db.create_tables([ApiUser, Location, Device])


def create_tables_test_db():
    with test_db:
        test_db.create_tables([ApiUserTest, LocationTest, DeviceTest])

def drop_tables_test_db():
    with test_db:
        test_db.drop_tables([ApiUserTest, LocationTest, DeviceTest])

def drop_tables():
    with db:
        db.drop_tables([ApiUser, Location, Device])

if __name__ == '__main__':
    create_tables()
