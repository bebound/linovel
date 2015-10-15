# linovel

Generate epub from http://www.linovel.com/

![iPhone截图][image-1]

## Requirements

- [Python3][1]
- [requests][2]
- [BeautifulSoup4][3]
- [docopt][4]
- [lxml][5]

## Quick start

### linovel
`pip install -r requirements.txt`

	Usage:
	    linovel.py
	    linovel.py [-s] [-o | --output=<output_dir>] [-c | --cover=<cover_path>] <url>...
	    linovel.py <url>... [-s] [-o | --output=<output_dir>] [-c | --cover=<cover_path>]
	    linovel.py -h | --help
	    linovel.py -v | --version
	
	Arguments:
	    <url>                                      Novel url
	
	Options:
	    -s                                         Single thread
	    -o=<output_dir> --output=<output_dir>      Output folder
	    -c=<cover_path> --cover=<cover_path>       Cover path
	    -h --help                                  Show this screen
	    -v --version                               Show version
	
	Examples:
	    linovel.py -s http://www.linovel.com/n/vollist/492.html
	    linovel.py -o d:/ http://www.linovel.com/n/book/1578.html

![lknovel截图][image-2]

The previous repo is [lknovel][6]

[![Bitdeli Badge][image-3]][7]

[1]:	http://www.python.org/getit/
[2]:	http://docs.python-requests.org/en/latest/
[3]:	http://www.crummy.com/software/BeautifulSoup/
[4]:	https://github.com/docopt/docopt
[5]:	http://lxml.de
[6]:	https://github.com/bebound/lknovel
[7]:	https://bitdeli.com/free "Bitdeli Badge"

[image-1]:	https://raw.github.com/bebound/linovel/master/screenShot/total.png
[image-2]:	https://raw.github.com/bebound/linovel/master/screenShot/2.png
[image-3]:	https://d2weczhvl823v0.cloudfront.net/bebound/lknovel/trend.png