import logging
from aiohttp import web
from peewee_async import Manager, PooledPostgresqlDatabase
from playhouse.shortcuts import model_to_dict
from models import ApiUser, Device, Location

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = PooledPostgresqlDatabase(
    'iot_management',
    user='iot_user',
    password='199400',
    host='localhost',
    port=5432
)

objects = Manager(database)
database.allow_sync = False


async def create_device(request):
    try:
        data = await request.json()
        logger.info(f"Received data for device creation: {data}")

        # Проверка существования связанных объектов
        location = await objects.get(Location, id=data['location'])
        api_user = await objects.get(ApiUser, id=data['api_user'])

        device = await objects.create(Device,
                                      name=data['name'],
                                      type=data['type'],
                                      login=data['login'],
                                      password=data['password'],
                                      location=location,
                                      api_user=api_user)
        logger.info(f"Device created: {device.name}")
        return web.json_response({'id': device.id})
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def get_device(request):
    device_id = request.match_info['id']
    try:
        device = await objects.get(Device, id=device_id)
        logger.info(f"Device retrieved: {device.name}")
        return web.json_response(model_to_dict(device))
    except Device.DoesNotExist:
        return web.json_response({'error': 'Device not found'}, status=404)
    except Exception as e:
        logger.error(f"Error retrieving device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def update_device(request):
    device_id = request.match_info['id']
    try:
        data = await request.json()
        logger.info(f"Received data for device update: {data}")

        device = await objects.get(Device, id=device_id)

        if 'name' in data:
            device.name = data['name']
        if 'type' in data:
            device.type = data['type']
        if 'login' in data:
            device.login = data['login']
        if 'password' in data:
            device.password = data['password']
        if 'location' in data:
            location = await objects.get(Location, id=data['location'])
            device.location = location
        if 'api_user' in data:
            api_user = await objects.get(ApiUser, id=data['api_user'])
            device.api_user = api_user

        await objects.update(device)
        logger.info(f"Device updated: {device.name}")
        return web.json_response(model_to_dict(device))
    except Device.DoesNotExist:
        return web.json_response({'error': 'Device not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating device: {e}")
        return web.json_response({'error': str(e)}, status=500)


async def delete_device(request):
    device_id = request.match_info['id']
    try:
        device = await objects.get(Device, id=device_id)
        await objects.delete(device)
        logger.info(f"Device deleted: {device.name}")
        return web.json_response({'status': 'deleted'})
    except Device.DoesNotExist:
        return web.json_response({'error': 'Device not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting device: {e}")
        return web.json_response({'error': str(e)}, status=500)


app = web.Application()
app.add_routes([
    web.post('/devices', create_device),
    web.get('/devices/{id}', get_device),
    web.put('/devices/{id}', update_device),
    web.delete('/devices/{id}', delete_device)
])

if __name__ == '__main__':
    web.run_app(app)
