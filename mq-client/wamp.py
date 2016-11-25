__all__ = (
    'ApplicationSession',
    'WampRunner',
)

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


class MyProtocol(WampWebSocketClientProtocol):
    pass


class MyFactory(WampWebSocketClientFactory):
    protocol = MyProtocol


class WampRunner(object):
    session = None

    def __init__(self, url, realm, session_factory):
        self._url = url
        self._realm = realm
        self._loop = asyncio.get_event_loop()
        self._factory = session_factory
        txaio.use_asyncio()
        txaio.config.loop = self._loop

    def _create(self):
        cfg = ComponentConfig(self._realm, dict())
        try:
            self.session = self._factory(cfg)
        except Exception:
            print("Can't create the app session :'(")
        else:
            return self.session

    async def _try_connect(self):
        isSecure, host, port, resource, path, params = parse_url(self._url)
        transport_factory = MyFactory(self._create,
                                      url=self._url,
                                      serializers=None)
        return await self._loop.create_connection(
            transport_factory,
            host,
            port,
            ssl=False
        )

    async def setup_connection(self):
        connected = False
        self.session = None
        while not connected:
            try:
                transport, protocol = await self._try_connect()
                protocol.is_closed.add_done_callback(self._reconnect)
            except:
                print("Can't connect, retry in 3 sec.")
                await asyncio.sleep(3)
            else:
                connected = True
                #self.session = protocol._session

    def publish(self, topic, message):
        if self.session:
            self.session.publish(topic, message)
        else:
            print("no session")

    def _reconnect(self, f):
        print("Connection lost, reconnecting...")
        asyncio.ensure_future(self.setup_connection(), loop=self._loop)
