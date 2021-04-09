# encoding=utf-8

# Assetnote OpenAPI/Swagger API schema parser

import logging
import argparse

from convert import convert_csv
from parse import parse_specs

def main():
    root_parser = argparse.ArgumentParser(description="Assetnote OpenAPI/Swagger API schema parser")
    action_subparser = root_parser.add_subparsers(title="action", dest="action")

    parse_parser = action_subparser.add_parser(
        "parse",
        help="Parse a directory of swagger JSON files into a single JSON file output for Kiterunner"
    )
    parse_parser.add_argument(
        "--blacklist",
        metavar="HOSTS",
        type=list,
        default=[
            "googleapis",
            "azure",
            "petstore",
            "amazon"
        ],
        help="Exclude specs with host field matching any of these strings (default googleapis, azure, petstore, amazon)"
    )
    parse_parser.add_argument(
        "--scrape-dir",
        metavar="DIR",
        type=str,
        help="Directory to read list of specs from (default ./scrape)",
        default="./scrape"
    )
    parse_parser.add_argument(
        "--output-file",
        metavar="FILE",
        type=str,
        help="File to output resulting schema to (default output.json)",
        default="output.json"
    )

    convert_parser = action_subparser.add_parser(
        "convert",
        help="Convert a file to a number of swagger JSON files in the provided output directory"
    )
    convert_parser.add_argument(
        "--file",
        metavar="FILE",
        type=str,
        help="File to convert to a number of swagger spec files.",
        required=True
    )
    convert_parser.add_argument(
        "--format",
        metavar="FORMAT",
        default="CSV",
        choices=["CSV"],
        type=str,
        help="File format to convert. Only CSV files supported. Must be in the format 'id,name,content'",
    )
    convert_parser.add_argument(
        "--scrape-dir",
        metavar="DIR",
        type=str,
        help="File to output resulting schema files to (defaults to ./scrape)",
        default="./scrape"
    )

    args = root_parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p"
    )

    if args.action == "parse":
        spec_count = parse_specs(args.scrape_dir, args.output_file, args.blacklist)
        logging.info(f"Finished parsing {spec_count}")

    elif args.action == "convert":
        if args.format == "CSV":
            convert_csv(args.file, args.scrape_dir)


if __name__ == "__main__":
    main()
