#!/usr/bin/env python
# coding: utf-8

import txredisapi
from twisted.internet import defer, reactor

@defer.inlineCallbacks
def main():
    # run two redis servers, one at port 6379 and another in 6380
    conn = yield txredisapi.RedisShardingConnection(["localhost:6379", "localhost:6380"])
    print repr(conn)

    keys = ["test:%d" % x for x in xrange(100)]
    for k in keys:
        yield conn.set(k, "foobar")
    result = yield conn.mget(*keys)
    print result

    # testing tags
    keys = ["test{lero}:%d" % x for x in xrange(100)]
    for k in keys:
        yield conn.set(k, "foobar")

    result = yield conn.mget(*keys)
    print result

if __name__ == "__main__":
    main().addCallback(lambda ign: reactor.stop())
    reactor.run()
