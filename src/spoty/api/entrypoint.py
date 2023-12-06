from argparse import ArgumentParser

from spoty.api.__main__ import main


def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("-q", "--query", type=str, help="Query to search")
    parser.add_argument("-t", "--type", type=str, help="Type of search")
    parser.add_argument("-l", "--limit", type=int, help="Limit of results", default=50)
    parser.add_argument("-f", "--features", type=bool, help="Get features", default=False)
    parser.add_argument("-tf", "--time_format", type=bool, help="Format time", default=False)
    return parser.parse_args()


def call_main():
    args = _parse_args()
    return main(
        query=args.query,
        type=args.type,
        limit=args.limit,
        features=args.features,
        time_format=args.time_format,
    )


if __name__ == "__main__":
    print(call_main())
