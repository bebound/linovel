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
    linovel.py -s http://www.linovel.com/n/vollist/492.html
    linovel.py -o d:/ -f=azw3 http://www.linovel.com/n/book/1578.html
"""
import re
import sys

from bs4 import BeautifulSoup
from docopt import docopt
import requests

from epub import Epub
from novel import Novel

_SINGLE_THREAD = False
_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}


def is_single_thread():
    single = input("Single Thread(Y/N)?:")
    return True if single.lower() == 'y' else False


def check_url(url):
    """
    check input url

    Args:
        url: A string represent the url which was input by user

    Returns:
        return 'vollist' if the url represent a vollist
        return 'book' if the url represent a book
        return False if the url is neither vollist nor booklist
    """
    vollist = re.compile(r'http://www.linovel.com/n/vollist/(\d+).html')
    book = re.compile(r'http://www.linovel.com/n/book/(\d+).html')
    if vollist.search(url):
        return 'vollist'
    elif book.search(url):
        return 'book'
    else:
        return False


def grab_volume(url, output_dir, cover_path, out_format):
    """
    grab volume
    
    Args:
        url: A string represent the url which was input by user
        output_dir: A string represent the path of the output EPUB file
        cover_file: A string represent the path of the EPUB cover
        out_format: A string represent the output format
    """
    try:
        print('Getting:' + url)
        novel = Novel(url=url, single_thread=_SINGLE_THREAD)
        novel.get_novel_information()
        epub = Epub(output_dir=output_dir, cover_path=cover_path, out_format=out_format, **novel.novel_information())
        epub.generate_file()

    except Exception as e:
        print('错误', str(e) + '\nAt:' + url)
        raise e


def parse_page(url):
    """
    parse page with BeautifulSoup

    Args:
        url: A string represent the url to be parsed

    Return:
        A BeatifulSoup element
    """
    r = requests.get(url, headers=_HEADERS)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')


def grab_booklist(url, output_dir, cover_path, out_format):
    """
    grab each volume in the booklist

    Args:
        url: A string represent the booklist
        output_dir: A string represent the path of the output EPUB file
        cover_file: A string represent the path of the EPUB cover
        out_format: A string represent the output format
    """
    soup = parse_page(url)
    volume_links = soup.select('li.linovel-book-item h3 a')
    for volume in volume_links:
        volume_link = 'http://www.linovel.com' + volume['href']
        grab_volume(volume_link, output_dir, cover_path, out_format)


def start(urls, output_dir=None, cover_path=None, out_format='epub'):
    """
    start the job using url

    Args:
        urls: A string represent the urls which was input by user
        output_dir: A string represent the path of the output EPUB file
        cover_file: A string represent the path of the EPUB cover
    """
    for url in urls:
        check_result = check_url(url)
        if check_result == 'book':
            grab_volume(url, output_dir, cover_path, out_format)
        elif check_result == 'vollist':
            grab_booklist(url, output_dir, cover_path, out_format)
        else:
            print('请输入正确的网址，例如：\nhttp://www.linovel.com/n/vollist/492.html'
                  '\nhttp://www.linovel.com/n/book/1578.html')


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
    arguments = docopt(__doc__, version='linovel 1.0')
    sys.exit(main())
