from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

WAMP = {
    'router': 'ws://127.0.0.1:8080/ws',
    'realm': 'market',
}


class Stub(ApplicationSession):
    def onJoin(self, details):
        self.publish('has.been.stored', "COUCOU")


r = ApplicationRunner(WAMP['router'], WAMP['realm'])
r.run(Stub)
