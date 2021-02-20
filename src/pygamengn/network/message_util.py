import io
import json
import logging
import struct
import sys

#############################################
# ServerMessage
#############################################


def json_encode(obj, encoding):
    return json.dumps(obj, ensure_ascii=False).encode(encoding)


def json_decode(json_bytes, encoding):
    tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding, newline="")
    obj = json.load(tiow)
    tiow.close()
    return obj


def create_message(content_bytes, content_type, content_encoding):
    jsonheader = {
        "byteorder": sys.byteorder,
        "content-type": content_type,
        "content-encoding": content_encoding,
        "content-length": len(content_bytes),
    }
    jsonheader_bytes = json_encode(jsonheader, "utf-8")
    message_hdr = struct.pack(">H", len(jsonheader_bytes))
    message = message_hdr + jsonheader_bytes + content_bytes

    return message


def create_response_json_content(action, value):
    if action == "search":
        request_search = {
            "morpheus": "Follow the white rabbit. \U0001f430",
            "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
            "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
        }
        answer = request_search.get(value) or f'No match for "{value}".'
        content = {"result": answer}
    else:
        content = {"result": f'Error: invalid action "{action}".'}
    content_encoding = "utf-8"
    response = {
        "content_bytes": json_encode(content, content_encoding),
        "content_type": "text/json",
        "content_encoding": content_encoding
    }
    return response


def create_response_binary_content(request):
    response = {
        "content_bytes": b"First 10 bytes of request: " + request[:10],
        "content_type": "binary/custom-server-binary-type",
        "content_encoding": "binary",
    }
    return response

#############################################
# ClientMessage
#############################################


def process_response_json_content(response):
    result = response.get("result")
    logging.debug(f"Received response: {result}")


def process_response_binary_content(response):
    logging.debug(f"Received response: {repr(response)}")
