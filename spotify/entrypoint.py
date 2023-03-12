import argparse
from spotify.spoty import run
from spotify.spoty.utils import create_csv, create_dataframe


def add_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="Query to search for",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        required=True,
        choices=["track", "album", "playlist"],
        help="Type of query to search for",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        default=50,
        help="Limit of results to return",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        default="output",
        help="Output directory",
    )

    args = parser.parse_args()
    return args


def main():
    args = add_arguments()
    obj = run(args.query, args.type, args.limit)
    print(obj)
    df = create_dataframe(obj)
    create_csv(df, args.output)



if __name__ == "__main__":
    main()
