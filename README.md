# Linovel

Generate epub from various website

Supported website:

- [360℃小说](http://www.360dxs.com)
- [轻小说文库](http://www.wenku8.com)

 If you find any other website, please open an issue and tell me.

![iPhone截图][image-1]

## Requirements

- [Python3][1]
- [requests][2]
- [BeautifulSoup4][3]
- [docopt][4]
- [lxml][5]

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
![lknovel截图][image-2]

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

Read [this](https://github.com/bebound/linovel/blob/master/CONTRIBUTION.md) if you want to let Linovel support more website


The previous repo is [lknovel][6]

[1]:	http://www.python.org/getit/
[2]:	http://docs.python-requests.org/en/latest/
[3]:	http://www.crummy.com/software/BeautifulSoup/
[4]:	https://github.com/docopt/docopt
[5]:	http://lxml.de
[6]:	https://github.com/bebound/lknovel

[image-1]:	https://raw.github.com/bebound/linovel/master/screenShot/total.png
[image-2]:	https://raw.github.com/bebound/linovel/master/screenShot/2.png
