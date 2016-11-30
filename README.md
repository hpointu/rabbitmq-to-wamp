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

# The `-p` flag

The goal of this project is to have a working prototype for the feature provided by the `-p` flag.

My approach was to write my own version of the ApplicationRunner which is not a runner aymore as it doesn't take car of any event loop. It just assumes it's there.

The way I communicate with the ApplicationSession is by keeping a reference to the current session in my "runner".
