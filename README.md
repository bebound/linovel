#linovel

Generate epub from http://www.linovel.com/

![iPhone截图](https://raw.github.com/bebound/linovel/master/screenShot/total.png)

##Requirements

- [Python3](http://www.python.org/getit/)
- [requests](http://docs.python-requests.org/en/latest/)
- [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/)
- [docopt](https://github.com/docopt/docopt)

##Quick start

###linovel
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
    

![lknovel截图](https://raw.github.com/bebound/linovel/master/screenShot/2.png)

The previous repo is [lknovel](https://github.com/bebound/lknovel)

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/bebound/lknovel/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

