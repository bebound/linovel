# !/usr/bin/env python3
"""linovel

Usage:
    linovel.py
    linovel.py [-s] [-o | --output=<output_dir>] [-c | --cover=<cover_path>] [-f | --format=<out_format>] <url>...
    linovel.py <url>... [-s] [-o | --output=<output_dir>] [-c | --cover=<cover_path>] [-f | --format=<out_format>]
    linovel.py -h | --help
    linovel.py -v | --version

Arguments:
    <url>                                      Novel url

Options:
    -s                                         Single thread
    -o=<output_dir> --output=<output_dir>      Output folder
    -c=<cover_path> --cover=<cover_path>       Cover path
    -f=<out_format> --format=<out_format>      Output format
    -h --help                                  Show this screen
    -v --version                               Show version

Examples:
    linovel.py -s http://old.linovel.com/n/vollist/492.html
    linovel.py -o d:/ -f=azw3 http://old.linovel.com/n/book/1578.html
"""
import sys

from docopt import docopt

from epub import Epub
from novel_oldlinovel import OldLinovel

_SINGLE_THREAD = False


def is_single_thread():
    single = input("Single Thread(Y/N)?:")
    return True if single.lower() == 'y' else False


def start(urls, output_dir=None, cover_path=None, out_format='epub'):
    """
    start the job using url

    Args:
        urls: A string represent the urls which was input by user
        output_dir: A string represent the path of the output EPUB file
        cover_path: A string represent the path of the EPUB cover
        out_format: A string represent the output file format
    """
    for url in urls:
        for cls in [OldLinovel]:
            if cls.check_url(url):
                novel = OldLinovel(url, _SINGLE_THREAD)
                novel.extract_novel_information()
                books = novel.get_novel_information()
                for book in books:
                    epub = Epub(output_dir=output_dir, cover_path=cover_path, out_format=out_format, **book)
                    epub.generate_file()
                break
        else:
            print('URL "{}" is invalid'.format(url))


def main():
    global _SINGLE_THREAD
    if len(sys.argv) > 1:
        urls = arguments['<url>']
        _SINGLE_THREAD = arguments['-s']
        output_dir = None if not arguments['--output'] else arguments['--output'][0]
        cover_path = None if not arguments['--cover'] else arguments['--cover'][0]
        out_format = 'epub' if not arguments['--format'] else arguments['--format'][0]
    else:
        urls = input('Please input urls（separate with space）:').split()
        if is_single_thread():
            _SINGLE_THREAD = True
        output_dir = None
        cover_path = None
        out_format = 'epub'
    if urls:
        start(urls, output_dir, cover_path, out_format)
    else:
        raise RuntimeError('No url')


if __name__ == '__main__':
    arguments = docopt(__doc__, version='linovel 2.0')
    sys.exit(main())
