---
layout: post
tags:
  - tech
---

A quick post because I can't resist the "sniffing" joke.

If you do a lot of network traffic analysis, you've probably used wireshark,
tcpdump, and other tools of that nature.  However, they only work well for
*network* traffic - try to use Unix domain sockets and you're out of luck -
they don't understand them.

Unless you proxy the traffic.  Like so:

First, let the process open whatever socket you care about.

Then, move it out of the way and have `socat` listen in its stead:

```bash
mv DEFAULT.socket hidden.socket
socat UDP-LISTEN:6000,reuseaddr,fork UNIX-CONNECT:hidden.socket
```

This sets up socat to take anything from UDP port 6000 and apply it to the
(now hidden) socket, with it none the wiser.

Then we plug tcpdump in to listen on this port:

```bash
tcpdump -ni lo -s0 -f 'udp port 6000' -w /tmp/out.pcap
```

And set up the proxy entry where the socket was expecting to be:

```bash
socat UNIX-LISTEN:DEFAULT.socket,fork UDP-CONNECT:127.0.0.1:6000
```
