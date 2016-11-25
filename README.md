This project is an attempt to integrate a WAMP component inside a running loop.


# Requirements

 - python >=3.5
 - Use pip to install `requirements.txt`


# Usage

You need something to write on an "xsource" AMQP queue.

Assuming rabbitmq is running on localhost:5672 you can use this producer :

```
python rabbit_stub.py
```

This will write a dumb text message every second to a "xsource" queue using the default '' exchange.

Then the consumer is run like this :

```
python mq-client/rabbit-listen.py -s
```

# Todo: make the `-p` flag work

The `-p` flag should publish an update on the WAMP router when the message has been processed.

This doesn't work right now.
