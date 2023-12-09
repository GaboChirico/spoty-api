import logging
from argparse import ArgumentParser

from spoty.api.__main__ import search
from spoty.api.log import setup_logger


def _parse_args():
    """
    Parse arguments from the command line.
    """
    parser = ArgumentParser()
    parser.add_argument("-q", "--query", type=str, help="Id to search", required=True)
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        help="Type of search",
        required=True,
        choices=["track", "album", "playlist"],
    )
    parser.add_argument("-l", "--limit", type=int, help="Limit of results", default=50)
    parser.add_argument(
        "-f", "--features", type=bool, help="Get features", default=False
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
    # logger.debug(result)
    # logger.info(result.serialize())


if __name__ == "__main__":
    main()
