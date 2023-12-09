from argparse import ArgumentParser

from spoty.api.__main__ import run


def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("-q", "--query", type=str, help="Query to search")
    parser.add_argument("-t", "--type", type=str, help="Type of search")
    parser.add_argument("-l", "--limit", type=int, help="Limit of results", default=50)
    parser.add_argument(
        "-f", "--features", type=bool, help="Get features", default=False
    )
    return parser.parse_args()


def call_main(args):
    return run(
        query=args.query,
        type=args.type,
        limit=args.limit,
        features=args.features,
    )


if __name__ == "__main__":
    args = _parse_args()
    call_main(args)
