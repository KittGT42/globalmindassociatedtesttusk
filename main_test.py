from aiohttp import web
from peewee_async import Manager, PooledPostgresqlDatabase
from models import ApiUserTest, DeviceTest, LocationTest
from playhouse.shortcuts import model_to_dict

db = PooledPostgresqlDatabase(
    'test_global_mindass',
    user='***',
    password='***',
    host='localhost',
    port=5432
)

objects = Manager(db)
db.allow_sync = False


# Создаем таблицы, если их нет
# create_tables()

async def create_device(request):
    try:
        data = await request.json()
        print(f"Received data for device creation: {data}")

        required_fields = ['name', 'type', 'login', 'password', 'location', 'api_user']
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")
                raise ValueError(f"Missing field: {field}")

        device = await objects.create(DeviceTest, name=data['name'], type=data['type'], login=data['login'],
                                      password=data['password'], location=data['location'], api_user=data['api_user'])
        print(f"Device created: {device.name}")
        return web.json_response({'id': device.id}, status=201)
    except Exception as e:
        print(f"Error creating device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def get_device(request):
    device_id = request.match_info['id']
    print(f"Attempting to retrieve device with id: {device_id}")
    try:
        device = await objects.get(DeviceTest, id=device_id)
        print(f"Device retrieved: {device.name} with id {device.id}")
        return web.json_response(model_to_dict(device), status=200)
    except DeviceTest.DoesNotExist:
        print(f"Device not found with id: {device_id}")
        return web.json_response({'error': 'Device not found'}, status=404)
    except Exception as e:
        print(f"Error retrieving device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def update_device(request):
    device_id = request.match_info['id']
    print(f"Attempting to update device with id: {device_id}")
    try:
        data = await request.json()
        print(f"Received data for device update: {data}")
        device = await objects.get(DeviceTest, id=device_id)

        for key, value in data.items():
            setattr(device, key, value)

        await objects.update(device)
        updated_device = await objects.get(DeviceTest, id=device_id)
        print(f"Device updated: {updated_device.name}")
        return web.json_response(model_to_dict(updated_device), status=200)
    except DeviceTest.DoesNotExist:
        print(f"Device not found with id: {device_id}")
        return web.json_response({'error': 'Device not found'}, status=404)
    except Exception as e:
        print(f"Error updating device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def delete_device(request):
    device_id = request.match_info['id']
    print(f"Attempting to delete device with id: {device_id}")
    try:
        device = await objects.get(DeviceTest, id=device_id)
        await objects.delete(device)
        print(f"Device deleted: {device.name}")
        return web.json_response({'status': 'deleted'}, status=200)
    except DeviceTest.DoesNotExist:
        print(f"Device not found with id: {device_id}")
        return web.json_response({'error': 'Device not found'}, status=404)
    except Exception as e:
        print(f"Error deleting device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def create_location(request):
    try:
        data = await request.json()
        print(f"Received data for location creation: {data}")
        location = await objects.create(LocationTest, name=data['name'])
        print(f"Location created with id {location.id} and name {location.name}")
        return web.json_response({'id': location.id, 'name': location.name}, status=201)
    except Exception as e:
        print(f"Error creating location: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def create_api_user(request):
    try:
        data = await request.json()
        print(f"Received data for API user creation: {data}")
        api_user = await objects.create(ApiUserTest, name=data['name'], email=data['email'], password=data['password'])
        print(f"API user created with id {api_user.id} and name {api_user.name}")
        return web.json_response({'id': api_user.id, 'name': api_user.name}, status=201)
    except Exception as e:
        print(f"Error creating API user: {e}")
        return web.json_response({'error': str(e)}, status=500)


app = web.Application()
app.router.add_post('/locations', create_location)
app.router.add_post('/devices', create_device)
app.router.add_post('/api_users', create_api_user)
app.router.add_get('/devices/{id}', get_device)
app.router.add_put('/devices/{id}', update_device)
app.router.add_delete('/devices/{id}', delete_device)

if __name__ == '__main__':
    web.run_app(app, port=8080)
