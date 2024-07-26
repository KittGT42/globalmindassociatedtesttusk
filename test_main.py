import pytest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from peewee_async import Manager, PooledPostgresqlDatabase
from models import ApiUser, Device, Location
from main import create_device, get_device, update_device, delete_device, create_location, create_api_user

# Настройки подключения к тестовой базе данных PostgreSQL
TEST_DB = {
    'database': 'iot_management',
    'user': 'iot_user',
    'password': '199400',
    'host': 'localhost',
    'port': 5432,
}
test_db = PooledPostgresqlDatabase(**TEST_DB)
objects = Manager(test_db)

class DeviceManagementTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = web.Application()
        app.router.add_post('/devices', create_device)
        app.router.add_get('/devices/{id}', get_device)
        app.router.add_put('/devices/{id}', update_device)
        app.router.add_delete('/devices/{id}', delete_device)
        app.router.add_post('/locations', create_location)
        app.router.add_post('/api_users', create_api_user)

        # Подключаемся к базе данных
        test_db.bind([ApiUser, Device, Location], bind_refs=False, bind_backrefs=False)
        if not test_db.is_closed():
            test_db.close()
        test_db.connect()
        test_db.create_tables([ApiUser, Device, Location])
        return app

    async def tearDownAsync(self):
        await super().tearDownAsync()
        test_db.drop_tables([ApiUser, Device, Location])
        test_db.close()

    async def test_create_location(self):
        payload = {"name": "Test Location"}
        resp = await self.client.request("POST", "/locations", json=payload)
        json_response = await resp.json()
        print("Create Location Response:", json_response)

        assert resp.status == 201
        assert 'id' in json_response
        assert json_response['name'] == "Test Location"

    async def test_create_api_user(self):
        payload = {"name": "Test User", "email": "test@example.com", "password": "password"}
        resp = await self.client.request("POST", "/api_users", json=payload)
        json_response = await resp.json()
        print("Create API User Response:", json_response)

        assert resp.status == 201
        assert 'id' in json_response
        assert json_response['name'] == "Test User"

    async def test_create_device(self):
        # Создание локации для устройства
        location_payload = {"name": "Test Location"}
        location_resp = await self.client.request("POST", "/locations", json=location_payload)
        location_json = await location_resp.json()
        print("Location Response:", location_json)

        # Создание API пользователя для устройства
        user_payload = {"name": "Test User", "email": "test@example.com", "password": "password"}
        user_resp = await self.client.request("POST", "/api_users", json=user_payload)
        user_json = await user_resp.json()
        print("User Response:", user_json)

        device_payload = {
            "name": "Test Device",
            "type": "sensor",
            "login": "testlogin",
            "password": "testpassword",
            "location": location_json['id'],
            "api_user": user_json['id']
        }
        resp = await self.client.request("POST", "/devices", json=device_payload)
        json_response = await resp.json()
        print("Device Response:", json_response)

        assert resp.status == 201
        assert 'id' in json_response

    async def test_get_device(self):
        # Создание локации и API пользователя
        location_payload = {"name": "Test Location"}
        location_resp = await self.client.request("POST", "/locations", json=location_payload)
        location = await location_resp.json()

        user_payload = {"name": "Test User", "email": "test@example.com", "password": "password"}
        user_resp = await self.client.request("POST", "/api_users", json=user_payload)
        user = await user_resp.json()

        # Создание устройства
        device_payload = {
            "name": "Test Device",
            "type": "sensor",
            "login": "testlogin",
            "password": "testpassword",
            "location": location['id'],
            "api_user": user['id']
        }
        device_resp = await self.client.request("POST", "/devices", json=device_payload)
        device = await device_resp.json()
        print("Created Device Response:", device)

        # Получение устройства по ID
        get_resp = await self.client.request("GET", f"/devices/{device['id']}")
        assert get_resp.status == 200
        get_json_response = await get_resp.json()
        print("Get Device Response:", get_json_response)

        assert get_json_response['name'] == "Test Device"
        assert get_json_response['type'] == "sensor"

    async def test_update_device(self):
        # Создание локации и API пользователя
        location_payload = {"name": "Test Location"}
        location_resp = await self.client.request("POST", "/locations", json=location_payload)
        location = await location_resp.json()

        user_payload = {"name": "Test User", "email": "test@example.com", "password": "password"}
        user_resp = await self.client.request("POST", "/api_users", json=user_payload)
        user = await user_resp.json()

        # Создание устройства
        device_payload = {
            "name": "Test Device",
            "type": "sensor",
            "login": "testlogin",
            "password": "testpassword",
            "location": location['id'],
            "api_user": user['id']
        }
        device_resp = await self.client.request("POST", "/devices", json=device_payload)
        device = await device_resp.json()
        print("Created Device Response:", device)

        # Обновление устройства
        update_payload = {"name": "Updated Device"}
        update_resp = await self.client.request("PUT", f"/devices/{device['id']}", json=update_payload)
        update_json_response = await update_resp.json()
        print("Update Device Response:", update_json_response)

        assert update_resp.status == 200
        assert update_json_response['name'] == "Updated Device"

    async def test_delete_device(self):
        # Создание локации и API пользователя
        location_payload = {"name": "Test Location"}
        location_resp = await self.client.request("POST", "/locations", json=location_payload)
        location = await location_resp.json()

        user_payload = {"name": "Test User", "email": "test@example.com", "password": "password"}
        user_resp = await self.client.request("POST", "/api_users", json=user_payload)
        user = await user_resp.json()

        # Создание устройства
        device_payload = {
            "name": "Test Device",
            "type": "sensor",
            "login": "testlogin",
            "password": "testpassword",
            "location": location['id'],
            "api_user": user['id']
        }
        device_resp = await self.client.request("POST", "/devices", json=device_payload)
        device = await device_resp.json()
        print("Created Device Response:", device)

        # Удаление устройства
        delete_resp = await self.client.request("DELETE", f"/devices/{device['id']}")
        delete_json_response = await delete_resp.json()
        print("Delete Device Response:", delete_json_response)

        assert delete_resp.status == 200
        assert delete_json_response['status'] == "deleted"

        # Проверка, что устройство больше не существует
        get_resp = await self.client.request("GET", f"/devices/{device['id']}")
        get_json_response = await get_resp.json()
        print("Get Deleted Device Response:", get_json_response)

        assert get_resp.status == 404
        assert get_json_response['error'] == "Device not found"

# Запуск тестов
if __name__ == '__main__':
    pytest.main()
