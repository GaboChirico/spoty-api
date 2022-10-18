import argparse
from spoty import Spoty
from models import Query
from utils import LOGGER, create_dataframe, create_csv, check_env


def args_parser():
    args_parser = argparse.ArgumentParser(description="Spoty")
    args_parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Query to search",
        required=True,
    )
    args_parser.add_argument(
        "-t",
        "--type",
        type=str,
        help="Type of search",
        required=True,
    )
    args_parser.add_argument(
        "-l", "--limit", type=int, help="Limit of search", default=100
    )
    args = args_parser.parse_args()
    return args


def setup():
    check_env()


def main():
    LOGGER.info("Starting Spoty")
    setup()
    args = args_parser()

    query = Query(args.query, args.type, args.limit)

    spoty = Spoty(query)()
    print(spoty)

    df = create_dataframe(spoty, index=False, ids=False)
    print(df)

    create_csv(df)


if __name__ == "__main__":
    args = args_parser()
    main()
