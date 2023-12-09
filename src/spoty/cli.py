import os
import logging
import json
from argparse import ArgumentParser

from spoty.api.__main__ import search
from spoty.api.log import setup_logger


def _parse_args():
    """
    Parse arguments from the command line.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="String ID query to search",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        help="Type of search",
        required=True,
        choices=["track", "album", "playlist"],
    )
    parser.add_argument("-l", "--limit", type=int, help="Limit of results.", default=50)
    parser.add_argument(
        "-f",
        "--features",
        type=bool,
        help="Include audio features.",
        default=False,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file",
    )
    return parser.parse_args()


def main() -> None:
    """
    Execute the CLI.
    """
    logger = setup_logger(__name__)

    args = _parse_args()
    result = search(
        query=args.query,
        type=args.type,
        limit=args.limit,
        features=args.features,
    )
    logger.info("Result: %s" % result)
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(result.serialize(), f, indent=4)


if __name__ == "__main__":
    main()
