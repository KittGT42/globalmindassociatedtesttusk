import unittest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from main_test import create_device, get_device, update_device, delete_device, create_location, create_api_user
from models import drop_tables_test_db, create_tables_test_db, drop_tables, create_tables


class MyAppTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.router.add_post('/locations', create_location)
        app.router.add_post('/devices', create_device)
        app.router.add_post('/api_users', create_api_user)
        app.router.add_get('/devices/{id}', get_device)
        app.router.add_put('/devices/{id}', update_device)
        app.router.add_delete('/devices/{id}', delete_device)
        return app

    def setUp(self):
        create_tables_test_db()
        # create_tables()

    def tearDown(self):
        drop_tables_test_db()
        # drop_tables()

    @unittest_run_loop
    async def test_create_api_user(self):
        ## Create API User
        payload = {
            "name": "Test User",
            "email": "test_user@example.com",
            "password": "test_password"
        }
        resp = await self.client.post('/api_users', json=payload)
        assert resp.status == 201
        data = await resp.json()
        assert 'id' in data
        assert data['name'] == "Test User"
        user_id = data['id']
        ## Create Location
        payload = {
            "name": "Test Location3",
        }
        resp = await self.client.post('/locations', json=payload)
        assert resp.status == 201
        data = await resp.json()
        assert 'id' in data
        assert data['name'] == "Test Location3"
        location_id = data['id']
        ## Create Device
        payload = {
            "name": "Test Device",
            "type": "sensor",
            "login": "test_login",
            "password": "test_password",
            "location": location_id,
            "api_user": user_id
        }
        resp = await self.client.post('/devices', json=payload)
        assert resp.status == 201
        data = await resp.json()
        assert 'id' in data
        device_id = data['id']
        ## Get Device
        get_resp = await self.client.get(f'/devices/{device_id}')
        assert get_resp.status == 200
        get_data = await get_resp.json()
        assert get_data['name'] == "Test Device"
        ## Update Device
        update_payload = {
            "name": "Updated Device",
            "type": "updated_sensor"
        }
        update_resp = await self.client.put(f'/devices/{device_id}', json=update_payload)
        assert update_resp.status == 200
        update_data = await update_resp.json()
        assert update_data['name'] == "Updated Device"
        assert update_data['type'] == "updated_sensor"
        ## Delete Device
        delete_resp = await self.client.delete(f'/devices/{device_id}')
        assert delete_resp.status == 200
        delete_data = await delete_resp.json()
        assert delete_data['status'] == 'deleted'


if __name__ == '__main__':
    unittest.main()
