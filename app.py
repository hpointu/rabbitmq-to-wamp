import asyncio
import txaio
from autobahn.websocket.util import parse_url
from autobahn.asyncio.websocket import (
    WampWebSocketClientFactory,
    WampWebSocketClientProtocol,
)
from autobahn.wamp.types import ComponentConfig
from autobahn.asyncio.wamp import (
    ApplicationRunner,
    ApplicationSession,
)


class MyComp(ApplicationSession):
    async def onJoin(self, details):
        print("Hey I joined")
        await self.subscribe(self.on_msg, 'a.topic')

        self.publish('a.topic', "He joined")

    def on_msg(self, message):
        print("Received:", message)


class MyProtocol(WampWebSocketClientProtocol):
    pass


class MyFactory(WampWebSocketClientFactory):
    protocol = MyProtocol


def create():
    cfg = ComponentConfig('realm1', dict())
    try:
        session = MyComp(cfg)
    except Exception:
        self.log.failure("App session could not be created! ")
    else:
        return session


class WampRunner(object):

    def __init__(self, url, realm):
        self._url = url
        self._realm = realm
        self._loop = asyncio.get_event_loop()
        txaio.use_asyncio()
        txaio.config.loop = self._loop

    async def _try_connect(self):
        isSecure, host, port, resource, path, params = parse_url(self._url)
        # TODO : pass realm to create()
        transport_factory = MyFactory(create, url=self._url, serializers=None)
        return await self._loop.create_connection(transport_factory, host, port, ssl=False)

    async def setup_connection(self):
        connected = False
        while not connected:
            try:
                transport, protocol = await self._try_connect()
                protocol.is_closed.add_done_callback(self._reconnect)
            except:
                print("Can't connect, retry in 3 sec.")
                await asyncio.sleep(3)
            else:
                connected = True


    def _reconnect(self, f):
        print("Reconnecting...")
        asyncio.ensure_future(self.setup_connection(), loop=self._loop)



def main(url, realm):
    runner = WampRunner(url, realm)
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(runner.setup_connection())

    loop.run_forever()

main('ws://127.0.0.1:8080/ws', 'realm1')
