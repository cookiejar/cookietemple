import logging
import os
from contextlib import suppress

import click
from gevent.pywsgi import WSGIServer

from .app import app

console = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
LOG = logging.getLogger("Server")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

CURRENT_DIR = os.path.abspath(os.getcwd())
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(MODULE_DIR, "static")
TEMPLATES_PATH = os.path.join(MODULE_DIR, "templates")


@click.command()
@click.option("-d/-p", "--debug/--production", help="Enable Flask debugger", required=False)
@click.option("-l", "--listen", default="0.0.0.0", help="Listen to this address for HTTP", required=False)
@click.option("-p", "--port", default=5111, help="Listen this port for HTTP", required=False)
def main(debug, listen, port):
    app.template_folder = TEMPLATES_PATH
    app.static_folder = STATIC_PATH

    LOG.info("Starting service on http://%s:%d/", listen, port)

    if debug:
        LOG.warning("Running on debug mode not for production.")
        app.run(host=listen, port=port, debug=True)
    else:
        http_server = WSGIServer((listen, port), app)

        with suppress(KeyboardInterrupt):
            http_server.serve_forever()
