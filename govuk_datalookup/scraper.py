import sys
from optparse import OptionParser

from .fetch import process_url

parser = OptionParser()
parser.add_option("--url", dest="url",
                  help="A Gov.uk data publication page")


def main():
    (options, args) = parser.parse_args()
    if not options.url:
        print "A URL is required, please specify with --url"
        sys.exit(1)

    print process_url(options.url)
