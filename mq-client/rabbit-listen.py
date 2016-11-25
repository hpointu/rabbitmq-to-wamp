import asyncio
import click
import asynqp
from settings import WAMP, RABBIT


class Consumer(object):

    def __init__(self, host, port, callback):
        self.queue_name = "xsource"
        self.callback = callback
        self.host = host
        self.port = port
        self._tasks = set()

    async def connect(self):
        cc = await asynqp.connect(host=self.host, port=self.port)
        channel = await cc.open_channel()
        queue = await channel.declare_queue(self.queue_name, durable=False)
        await queue.consume(self.handle_msg)

    def handle_msg(self, message):
        # We want to keep track of the tasks to be able to
        # terminate properly if needed.
        loop = asyncio.get_event_loop()
        t = loop.create_task(self.callback(message.body))
        # t = asyncio.ensure_future(self.callback(message.body))
        # t.add_done_callback(lambda t: self._tasks.remove(t))
        self._tasks.add(t)


async def _fake_store(message):
    await asyncio.sleep(0.5)
    print("Stored: %s" % message)


class MessageHandler(object):
    def __init__(self, store, publish):
        self.wamp_session = None
        self.storage = None

        if publish:
            # connect `wamp_sesstion` to the wamp router
            pass
        if store:
            # connect/init storage (will acutally be a motor client)
            self.storage = _fake_store

    async def handle(self, message):
        if self.storage:
            await self.storage(message)

        if self.wamp_session:
            await self.wamp_session.publish('has.been.stored', message)



@click.command()
@click.option('-p', '--publish', default=False)
@click.option('-s', '--store', default=False)
def main(store, publish):
    #h = MessageHandler(store, publish)
    c = Consumer(RABBIT['host'], RABBIT['port'], _fake_store)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(c.connect()))
    loop.run_forever()


if __name__ == "__main__":
    main()
