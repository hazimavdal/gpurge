#!/bin/python3
import os
import argparse
from options import Options
from worker import Worker
from logger import Logger

REPORT_FILENAME = "gpurge.log"
DEFAULT_VERBOSITY_LEVEL = 4


def main():
    parser = argparse.ArgumentParser()

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "-l", "--list", help="a list of document paths to process. E.g. path/hellp.gdoc")
    source.add_argument("-f", "--folder", help="a folder to process")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="search recursively in the given folder")

    parser.add_argument("-t", "--trash", action="store_true",
                        default=False,
                        help="Move the remove document to trash")

    locals = parser.add_mutually_exclusive_group()
    locals.add_argument("-d", "--delete", action="store_true",
                        default=False,
                        help="delete local document")
    locals.add_argument(
        "-m", "--move", help="move all processed documents to this folder")

    save = parser.add_mutually_exclusive_group()
    save.add_argument("-i", "--inplace",
                      default=False,
                      action="store_true",
                      help="save the output in the same folder as the input")
    save.add_argument("-o", "--output",
                      help="save all documents to this folder")

    parser.add_argument("-e", "--extensions", nargs="+",
                        help="type of documents to process (gdoc, gsheet)",
                        default=["gdoc", "gsheet"])

    parser.add_argument(
        "-c", "--gdoc", help="the output format for gdoc files", default="docx")
    parser.add_argument(
        "-s", "--gsheet", help="the output format for gsheet files", default="xlsx")

    parser.add_argument(
        "-R", "--report", help="location to save the report file", default="")

    parser.add_argument("-v", "--verbosity", type=int, nargs="?",
                        help="Set verbosity level. Allowed values are 0 (DEBUG), 1 (INFO), 2 (WARN), 3 (ERROR), and 4 (FATAL)")

    args = parser.parse_args()

    if not args.verbosity:
        args.verbosity = DEFAULT_VERBOSITY_LEVEL

    if args.recursive and args.folder is None:
        parser.error("-r requires -f")

    log = Logger(args.verbosity)
    opts = Options(log, args)
    wk = Worker(log, opts)
    wk.work()

    log.save(os.path.join(args.report, REPORT_FILENAME))


if __name__ == "__main__":
    main()
