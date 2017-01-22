---
layout: post
---

This is a follow-up to my [earlier complaint](/2016/10/16/asynchronous-rust/)
about asynchronous IO and event loops in Rust.

Since that time, the Rust crates [Tokio](https://tokio.rs/) and Futures have
had stable releases, and I've been playing with them a bit.

Anyway, reproducing from the Tokio docs, this is an asynchronous echo server:

```rust
extern crate futures;
extern crate tokio_core;

use futures::{Future, Stream};
use tokio_core::io::{copy, Io};
use tokio_core::net::TcpListener;
use tokio_core::reactor::Core;

fn main() {
    let mut core = Core::new().unwrap();
    let handle = core.handle();

    let addr = "127.0.0.1:12345".parse().unwrap();
    let sock = TcpListener::bind(&addr, &handle).unwrap();

    let server = sock.incoming().for_each(|(sock, _)| {
        let (reader, writer) = sock.split();

        let bytes_copied = copy(reader, writer);

        let handle_conn = bytes_copied.map(|amt| {
            println!("wrote {} bytes", amt)
        }).map_err(|err| {
            println!("IO error {:?}", err)
        });

        handle.spawn(handle_conn);

        Ok(())
    });

    core.run(server).unwrap();
}
```

For comparison, here is a strictly less functional version in C:

```C
#include <stdlib.h>
#include <unistd.h>

#include <arpa/inet.h>

#include <sys/select.h>
#include <sys/time.h>
#include <sys/types.h>

#define BUFLEN 2048

int main() {
    int ret;

    int fd = socket(PF_INET, SOCK_STREAM, 0);
    if (fd == -1) {
        exit(1);
    }

    struct sockaddr_in myaddr;
    myaddr.sin_family = AF_INET;
    myaddr.sin_port = htons(12345);
    myaddr.sin_addr.s_addr = INADDR_ANY;

    ret = bind(fd, (struct sockaddr *) &myaddr, sizeof(myaddr));
    if (ret != 0) {
        exit(1);
    }

    ret = listen(fd, 10);
    if (ret != 0) {
        exit(1);
    }

    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(fd, &readfds);
    int nfds = fd + 1;
    while (1) {
        ret = select(nfds, &readfds, NULL, NULL, NULL);
        if (ret < 0) {
            exit(1);
        }

        if (FD_ISSET(fd, &readfds)) {
            int client = accept(fd, NULL, NULL);
            if (client == -1) {
                exit(1);
            }

            FD_SET(client, &readfds);
            nfds += 1;
            continue;
        }

        for (int i = fd + 1; i < nfds; i++) {
            char buf[BUFLEN];
            ssize_t len = recv(i, &buf, BUFLEN - 1, MSG_DONTWAIT);
            if (len <= 0) {
                close(i);
            }
            buf[len] = '\0';

            ret = send(i, &buf, len, MSG_DONTWAIT);
            if (ret != len) {
                close(i);
            }
        }
    }
}
```

The C version is longer, more involved, less understandable to people not
intimately familiar with network code, and let me emphasize: less usable.  It
also includes a cast, right there in the code.

Tokio uses mio, which I criticized in my previous post for being impossible to
use by mortals (i.e., those picking it up for the first time are presented an
impossible learning curve).  As far as I can tell, my complaints have been
addressed, and I am happy.  I wish we had had this support sooner.
