import logging

from aiohttp import web

LOG = logging.getLogger(__name__)

COUNTER = 0

CLIENTS = set()


async def ping(request):
    return web.json_response({'text': 'pong'})


async def index(request):
    global COUNTER
    global CLIENTS
    if request.remote not in CLIENTS:
        CLIENTS.add(request.remote)
        COUNTER += 1
    return web.json_response({'counter': COUNTER})


async def on_startup(app):
    LOG.info('App is starting ...')


async def on_shutdown(app):
    LOG.info('App is stopping ...')


def setup_routes(app):
    app.router.add_get('/api/ping', ping, allow_head=False)
    app.router.add_get('/api/index', index, allow_head=False)


@web.middleware
async def request_errors_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as ex:
        LOG.error(f'Got en error on {handler.__name__} from {request.remote} user. {ex}')


def create_app():
    app = web.Application(middlewares=[request_errors_middleware])
    setup_routes(app)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app




if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
