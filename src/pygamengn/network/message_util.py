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


def process_protoheader(buffer):
    """Reads the protocol header length and returns the message length and message (without the header length bytes)."""
    header_len = 2
    if len(buffer) >= header_len:
        json_header_len = struct.unpack(">H", buffer[:header_len])[0]
        buffer = buffer[header_len:]
        return (json_header_len, buffer)
    else:
        return (None, buffer)


def process_json_header(json_header_len, buffer):
    if len(buffer) >= json_header_len:
        json_header = json_decode(buffer[:json_header_len], "utf-8")
        buffer = buffer[json_header_len:]
        validate_json_header(json_header)
        return (json_header, buffer)
    else:
        return (None, buffer)


def validate_json_header(json_header):
    for required_field in ("byteorder", "content-length", "content-type", "content-encoding"):
        if required_field not in json_header:
            raise ValueError(f'Missing required header "{reqhdr}".')

#############################################
# ClientMessage
#############################################


def process_response_json_content(response):
    result = response.get("result")
    logging.debug(f"Received response: {result}")


def process_response_binary_content(response):
    logging.debug(f"Received response: {repr(response)}")
