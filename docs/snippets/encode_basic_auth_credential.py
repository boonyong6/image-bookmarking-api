import argparse
import base64
from typing import Protocol


class ArgsProtocol(Protocol):
    client_id: str
    client_secret: str


def main(argv: list[str]):
    arg_parser = argparse.ArgumentParser(description="Basic auth credentials encoder.")
    arg_parser.add_argument("client_id")
    arg_parser.add_argument("client_secret")
    args: ArgsProtocol = arg_parser.parse_args(args=argv)

    client_id = args.client_id
    client_secret = args.client_secret
    credentials = f"{client_id}:{client_secret}"
    credentials = base64.b64encode(credentials.encode("utf-8"))
    print(f"{credentials=}")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
