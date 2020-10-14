I've recently been using [bokeh](https://bokeh.org/) to produce some charts for my team on a regular basis and I found it a remarkable tool for the job. I particularly appreciate that it will serve web pages from my machine so that I can share the graphs without needing to install anything on my manager's machine.

During this process I created a bokeh script with several command line options to specify which data should be shown over what time frame. While running this over the course of a week or so, I struggled every morning to remember the right set of command line options to get the data I wanted on the external-facing IP address on a fresh port.

I really wanted to have a self-contained script that would launch bokeh as part of its operation, rather than remembering which command line options I needed to specify. I found [this SO article](https://stackoverflow.com/questions/51802159/how-to-embed-a-bokeh-server-in-a-standalone) which got me part of the way there, but I really wanted to specify IP address and port automatically.

Below we'll walk through my current solution, which is not perfect, but works for what I need. Hopefully it can help you out as well.

## Command Line Args

Let's start with the user interface. For this example, you'll just have one option for your graph and two options to pass to bokeh:

```python
def get_command_line_args():
    """ Read command line args, of course."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--blue", action="store_true")
    parser.add_argument(
        "-e",
        "--external",
        action="store_true",
        help="serve on local ip address instead of localhost",
    )
    parser.add_argument("-p", "--port", default="5006", help="socket port")
    args = parser.parse_args()

    args.ip_addr = get_local_ip_addr(args.external)

    if args.blue:
        args.color = "blue"
    else:
        args.color = "red"
    return args
```

The function starts with the graph option, `-b` which changes the color of the line from red to blue. You will expand this out to be whatever options you need to pass to your script, or remove it if there are none. We'll see below how this gets passed to the "script" part of my program.

The next option is `-e` which switches the bokeh server from `localhost` mode to serving the web page on an externally facing IP address. This option is just a bool, but we need to provide bokeh with a full IP address to use. You'll see that code below.

Finally the `-p` option is allowed for specifying the starting port number for serving. There is some code to retry with an increasing port number if the starting one is already in use. Again, we'll see this in another section below.

Once you've read the command line args, you can do a little processing on them. Let's skip the `get_local_ip_addr()` call at the moment and jump straight to the `-b` option. The code uses this `bool` to set a new value in `args` to indicate if the graph line should be `red` or `blue`.

> **Note:** This could also be done by reading in a string value with the color in it. There are lots of options here, but this seemed the easiest.

Now you can go and look at the IP address code.

## Get Local IP Address

The code shown here is based closely on a [Stack Overflow](https://stackoverflow.com/a/166589/6843734) answer:

```python
def get_local_ip_addr(external):
    if not external:
        return "localhost"

    # NOTE: this algorithm is not perfect. It will definitely not work if you
    # do not have an external internet connection
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # known valid external IP address
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

```

As the comment indicates, this is not foolproof but should work for many reasonable situations. It works by opening a network socket to a public DNS server run by Google. It should work with any other reliable IP address that is reachable from your machine.

Once the socket is open, you use `.getsockname()` which returns the IP address and port on the local machine for that socket.

Again, there are situations in which this will not work, but generally it will.

## Starting the Server

Once we have the command line options set up, we can get to the actual bokeh part of the code. Here is `start_server()`:

```python
def start_server(address, port, url, attempts=100):
    while attempts:
        attempts -= 1
        try:
            server = Server(
                {url: graph_it},
                num_procs=1,
                port=port,
                address=address,
                allow_websocket_origin=[f"{address}:{port}",],
            )
            server.start()
            return server, port
        except OSError as ex:
            if "Address already in use" in str(ex):
                print(f"Port {port} busy")
                port += 1
            else:
                raise ex
    raise Exception("Failed to find available port")
```

There's a bunch of code here, but the main part is creating the `Server` obejct. In `get_command_line_args()` we made sure that both `address` and `port` are set to valid values, `localhost` and `5006` by default.

These values and the passed-in `url` are used to create the `Server`:

```python
server = Server(
    {url: graph_it},
    num_procs=1,
    port=port,
    address=address,
    allow_websocket_origin=[f"{address}:{port}",],
)
```

The first parameter to the constructor maps the passed-in `url` to `graph_it()` which is a basic bokeh plot I shamelessly stole from an example online.

The `num_procs` parameter allows bokeh to use multiprocessing for the underlying tornado server to handle multiple connections. For my example, one was sufficient, but it could be handy to increase in some circumstances.

The `port` and `address` parameters are used twice, once to tell bokeh where to serve the graph, and once to allow cross-site connections to the address and port it's serving.

Once you've created the `Server` object, you call `server.start()` to get it running.

The rest of the function is a `while` loop that looks for an `Address already in use` error to try to find an open port. I found this handy while testing.

## The Graphing Function

The graphing function is the actual bokeh script you want to run. This example is the shortest function I could find without too much effort. You should replace this with the script you're passing in to bokeh.

 The interesting portion is the hack I for the color arguments. There is a way to pass command line arguments through bokeh to the script it is calling, and I suspect there's an elegant way to do something similar here, but I'll admit I went for the easy round and just made the `args` parameter a global and referenced in here:

```python
def graph_it(doc):
    global args
    p = figure(plot_width=400, plot_height=400, title="My Line Plot")
    p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2, line_color=args.color)
    doc.add_root(p)
```

If you figure out a better solution, please contact me and I'll update the example! I'd love to see it.

## Running the I/O Loop

Finally you've hit the main portion of the script which puts all these pieces together:

```python
if __name__ == "__main__":
    args = get_command_line_args()
    port = int(args.port)
    address = args.ip_addr
    url = "/"

    try:
        server, port = start_server(address, port, url)
    except Exception as ex:
        print("Failed:", ex)
        sys.exit()

    try:
        print(f"Opening Bokeh application on http://{address}:{port}{url}")
        server.io_loop.add_callback(server.show, url)
        server.io_loop.start()
    except KeyboardInterrupt:
        print("\nShutting Down")
```

You start by reading the command line arguments and setting up the `port`, `address`, and `url` parameters used to run the server.

Next you create the server and start it. Note that this routine passed back the port that it selected as it can make many attempts to find an open port.

The last block starts up the `io_loop` for the underlying tornado server which manages the I/O to your bokeh app.

## Conclusion

I hope someone found this helpful as I was happy with the solution for my particular problem and I was unable to find a good source of how to do this in my searching.

For completeness I'll include the full script below. Please contact me if you have questions or suggestions to make this article or code better!

Here's the full script:

```python
#!/usr/bin/env python3
import argparse
from bokeh.plotting import figure
from bokeh.server.server import Server
import socket
import sys


def get_local_ip_addr(external):
    if not external:
        return "localhost"

    # NOTE: this algorithm is not perfect. It will definitely not work if you
    # do not have an external internet connection
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # known valid external IP address
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr


def get_command_line_args():
    """ Read command line args, of course."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--blue", action="store_true")
    parser.add_argument(
        "-e",
        "--external",
        action="store_true",
        help="serve on local ip address instead of localhost",
    )
    parser.add_argument("-p", "--port", default="5006", help="socket port")
    args = parser.parse_args()

    args.ip_addr = get_local_ip_addr(args.external)

    if args.blue:
        args.color = "blue"
    else:
        args.color = "red"
    return args


def graph_it(doc):
    global args
    p = figure(plot_width=400, plot_height=400, title="My Line Plot")
    p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2, line_color=args.color)
    doc.add_root(p)


def start_server(address, port, url, attempts=100):
    while attempts:
        attempts -= 1
        try:
            server = Server(
                {url: graph_it},
                num_procs=1,
                port=port,
                address=address,
                allow_websocket_origin=[f"{address}:{port}",],
            )
            server.start()
            return server, port
        except OSError as ex:
            if "Address already in use" in str(ex):
                print(f"Port {port} busy")
                port += 1
            else:
                raise ex
    raise Exception("Failed to find available port")


if __name__ == "__main__":
    args = get_command_line_args()
    port = int(args.port)
    address = args.ip_addr
    url = "/"

    try:
        server, port = start_server(address, port, url)
    except Exception as ex:
        print("Failed:", ex)
        sys.exit()

    try:
        print(f"Opening Bokeh application on http://{address}:{port}{url}")
        server.io_loop.add_callback(server.show, url)
        server.io_loop.start()
    except KeyboardInterrupt:
        print("\nShutting Down")
```

