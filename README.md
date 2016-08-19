# Linovel

[![Build Status][image-1]][1]
![Python Version][image-2]

Generate EPUB from various website

Supported website:

- [360℃小说][2]
- [轻小说文库][3]

 If you find any other website, please open an issue and tell me.

![iPhone截图][image-3]

## Requirements

- [Python3][4]
- [requests][5]
- [BeautifulSoup4][6]
- [docopt][7]
- [lxml][8]

## Quick start
`pip install -r requirements.txt`

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
	    linovel.py -s http://qitawenku.360dxs.com/book_3037.html
	    linovel.py -o d:/ -f=azw3 http://qitawenku.360dxs.com/book_3037.html
![lknovel截图][image-4]

### Generate format other than epub
This feature require Calibre, a ebook managing software, installed and only works on Mac OS X for now. To use it, just add `-f` argument with the format you wish to output.

For example:
`python3 linovel.py -f mobi http://qitawenku.360dxs.com/book_3037.html`

Available output formats:
* AZW3
* EPUB
* FB2
* HTML
* HTMLZ
* LIT
* LRF
* MOBI
* OEB
* PDB
* PDF
* PML
* RB
* RTF
* SNB
* TCR
* TXT
* TXTZ

### Contribution

Read [this][9] if you want to let linovel support more website


The previous repo is [lknovel][10]

[1]:	https://travis-ci.org/bebound/linovel
[2]:	http://www.360dxs.com
[3]:	http://zhannei.baidu.com/cse/search?q=&s=135999764005104892&srt=dateModified&nsid=0&area=1
[4]:	http://www.python.org/getit/
[5]:	http://docs.python-requests.org/en/latest/
[6]:	http://www.crummy.com/software/BeautifulSoup/
[7]:	https://github.com/docopt/docopt
[8]:	http://lxml.de
[9]:	https://github.com/bebound/linovel/blob/master/CONTRIBUTION.md
[10]:	https://github.com/bebound/lknovel

[image-1]:	https://travis-ci.org/bebound/linovel.svg?branch=master
[image-2]:	https://img.shields.io/badge/python-3.4%203.5-blue.svg
[image-3]:	https://raw.github.com/bebound/linovel/master/screenShot/total.png
[image-4]:	https://raw.github.com/bebound/linovel/master/screenShot/2.png