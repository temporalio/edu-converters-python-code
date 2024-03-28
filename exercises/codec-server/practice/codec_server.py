"""Temporal Python Codec Server

Usage:
  codec_server.py
  codec_server.py --web <url>

Options:
  --web    Temporal Web UI URL to enable CORS for

"""
from docopt import docopt

from functools import partial
from typing import Awaitable, Callable, Iterable, List

from aiohttp import hdrs, web
from google.protobuf import json_format
from temporalio.api.common.v1 import Payload, Payloads

# TODO Part A: Import the `EncryptionCodec` class from your other code

def build_codec_server(arguments) -> web.Application:
    async def header_options(req: web.Request) -> web.Response:
        resp = web.Response()
        if arguments["--web"]==True:
            if req.headers.get(hdrs.ORIGIN) == arguments["<url>"]:
                resp.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = arguments["<url>"]
                resp.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = "POST"
                resp.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = "content-type,x-namespace"
        return resp

    # General purpose payloads-to-payloads
    async def apply(
        fn: Callable[[Iterable[Payload]], Awaitable[List[Payload]]], req: web.Request
    ) -> web.Response:
        # Read payloads as JSON
        assert req.content_type == "application/json"
        payloads = json_format.Parse(await req.read(), Payloads())

        # Apply
        payloads = Payloads(payloads=await fn(payloads.payloads))

        # Apply headers and return JSON
        resp = await header_options(req)
        resp.content_type = "application/json"
        resp.text = json_format.MessageToJson(payloads)
        return resp

    # Build app per-Namespace
    app = web.Application()
    # TODO Part A: Create a dictionary named `codecs` which maps Codecs per-namespace.
    # Use the loop below as a guide.
    for route,codec in codecs.items():
        app.add_routes(
            [
                web.post(("/" + route + "/encode"), partial(apply, codec.encode)),
                web.post(("/" + route + "/decode"), partial(apply, codec.decode)),
                web.options(("/" + route + "/decode"), header_options),
            ]
        )
    return app

if __name__ == "__main__":
    arguments = docopt(__doc__)
    web.run_app(build_codec_server(arguments), host="127.0.0.1", port=8081)