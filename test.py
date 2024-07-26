import pytest
import json
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from main import app, database, objects
from models import Device, ApiUser, Location

class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return app

    async def setUpAsync(self):
        await objects.create(ApiUser, id=1, name="Test User", email="test@example.com", password="password")
        await objects.create(Location, id=1, name="Test Location")

    async def tearDownAsync(self):
        await objects.execute(Device.delete().where(Device.id != 0))
        await objects.execute(ApiUser.delete().where(ApiUser.id != 0))
        await objects.execute(Location.delete().where(Location.id != 0))

    @unittest_run_loop
    async def test_create_device(self):
        data = {
            "name": "Test Device",
            "type": "sensor",
            "login": "test_login",
            "password": "test_password",
            "location": 1,
            "api_user": 1
        }
        resp = await self.client.post('/devices', json=data)
        assert resp.status == 201
        response_data = await resp.json()
        assert 'id' in response_data

    @unittest_run_loop
    async def test_get_device(self):
        device = await objects.create(Device, name="Test Device", type="sensor", login="test_login", password="test_password", location=1, api_user=1)
        resp = await self.client.get(f'/devices/{device.id}')
        assert resp.status == 200
        response_data = await resp.json()
        assert response_data['name'] == device.name

    @unittest_run_loop
    async def test_update_device(self):
        device = await objects.create(Device, name="Test Device", type="sensor", login="test_login", password="test_password", location=1, api_user=1)
        update_data = {
            "name": "Updated Device"
        }
        resp = await self.client.put(f'/devices/{device.id}', json=update_data)
        assert resp.status == 200
        response_data = await resp.json()
        assert response_data['name'] == "Updated Device"

    @unittest_run_loop
    async def test_delete_device(self):
        device = await objects.create(Device, name="Test Device", type="sensor", login="test_login", password="test_password", location=1, api_user=1)
        resp = await self.client.delete(f'/devices/{device.id}')
        assert resp.status == 200
        response_data = await resp.json()
        assert response_data['status'] == 'deleted'

    @unittest_run_loop
    async def test_create_location(self):
        data = {
            "name": "New Location"
        }
        resp = await self.client.post('/locations', json=data)
        assert resp.status == 201
        response_data = await resp.json()
        assert response_data['name'] == "New Location"

    @unittest_run_loop
    async def test_create_api_user(self):
        data = {
            "name": "New API User",
            "email": "new_user@example.com",
            "password": "new_password"
        }
        resp = await self.client.post('/api_users', json=data)
        assert resp.status == 201
        response_data = await resp.json()
        assert response_data['name'] == "New API User"

if __name__ == '__main__':
    pytest.main()
