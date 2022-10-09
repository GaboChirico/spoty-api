import argparse
from spoty import Spoty
from models import Query
from utils import LOGGER, create_dataframe, create_csv


def args_parser():
    args_parser = argparse.ArgumentParser(description='Spoty')
    args_parser.add_argument(
        '-q', 
        '--query', 
        type=str, 
        help='Query to search',
        required=True
    )
    args_parser.add_argument(
        '-t', 
        '--type', 
        type=str, 
        help='Type of search',
        required=True
    )
    args_parser.add_argument(
        '-l', 
        '--limit',
        type=int, 
        help='Limit of search'
    )
    args = args_parser.parse_args()
    return args


def main(query, type, limit):
    query = Query(query, type, limit)
    spoty = Spoty(query)()
    create_csv(create_dataframe(spoty, index=False, ids=False))
    print(spoty)


if __name__ == "__main__":
    args = args_parser()
    main(query=args.query, type=args.type, limit=args.limit)
