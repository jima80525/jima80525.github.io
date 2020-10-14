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
