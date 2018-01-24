#!/usr/bin/env python
import argparse as ap
import os
import json

from dit_gui.load_flow import Load
from dit_gui.add_flow import Add
from dit_gui.update_flow import Update
from circuits.web import Logger, Server, Static


def run_server(host, port):
    app = Server((host, port))
    Logger().register(app)
    Static("/static", docroot="dit_gui/static").register(app)
    Load().register(app)
    Add().register(app)
    Update().register(app)
    app.run()

def parse_arguments():
    parser = ap.ArgumentParser(description='Runs the DIT GUI.')

    parser.add_argument('-s', '--host', default='0.0.0.0', help='The hostname to bind to for the server.')
    parser.add_argument('-p', '--port', type=int, default=8000, help='The port to bind to for the server.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    run_server(args.host, args.port)
