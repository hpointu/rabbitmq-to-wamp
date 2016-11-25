from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

WAMP = {
    'router': 'ws://127.0.0.1:8080/ws',
    'realm': 'market',
}


class Stub(ApplicationSession):
    async def onJoin(self, details):
        await self.subscribe(self._handler, 'has.been.stored')

    def _handler(self, message):
        print(message)


r = ApplicationRunner(WAMP['router'], WAMP['realm'])
r.run(Stub)
