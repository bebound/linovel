import html
import re
import threading

from novel import AbstractNovel


class Dxs(AbstractNovel):
    """
    360dxs.com class, deal with url such as:
    http://qitawenku.360dxs.com/book_3037.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chapter_links = []
        self.book_name = ''

    @property
    def filename(self):
        return ' '.join([self.book_name, self.volume_number, self.volume_name])

    @staticmethod
    def check_url(url):
        url_checker = re.compile(r'http://qitawenku.360dxs.com/book_(\d+).html')
        return True if url_checker.search(url) else False

    @staticmethod
    def find_cover_url(soup):
        src = str(soup.select('div.book-pic'))
        url = 'http://qitawenku.360dxs.com/' + re.search(r'data-original="(.*?)"', src).group(1)
        return url

    def find_date(self, soup):
        raw_date = soup.find(string=re.compile("^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"))
        self.date = raw_date.split(' ')[0]

    @staticmethod
    def print_info(info):
        """
        print info, ignore UnicodeDecodeError

        Args:
            info: a string to print
        """
        try:
            print(info)
        except UnicodeDecodeError as e:
            print('Ignored:', e)
        except UnicodeEncodeError as e:
            print('Ignored:', e)

    @staticmethod
    def get_chapter_content(src):
        content = re.findall(
            r'http://cpro.baidustatic.com/cpro/ui/c.js" type="text/javascript"></script>([\s\S]*?)<script type="text/javascript">',
            src)[1].strip()
        content = re.sub(r'<a class.*?</a>', '', content)
        content = re.sub(r'<script.*?</script>', '', content)
        return [html.unescape(i).strip() for i in content.split('\n')]

    def add_chapter(self, chapter):
        """
        add chapter

        Args:
            chapter: a tuple (chapter number, chapter name, chapter_content)
        """
        self.chapters.append(chapter)

    def extract_chapter(self, url, number):
        """
        add each chapter's content to the epub instance

        Args:
            url: A string represent the chapter url to be added
            number: A int represent the chapter's number
        """
        try:
            soup = self.parse_page(url)
            chapter_name = html.unescape(re.search(r'<li class="am-active">(.*?)</li>', str(soup)).group(1))
            self.print_info(chapter_name)
            chapter_content = self.get_chapter_content(str(soup))
            self.add_chapter((number, chapter_name, chapter_content))

        except Exception as e:
            print('错误', str(e), '\nAt:', url)
            raise e

    def parse_content(self):
        """start extract every chapter in epub"""
        print('Start parsing chapters')
        th = []

        if not self.single_thread:
            for i, link in enumerate(self.chapter_links):
                t = threading.Thread(target=self.extract_chapter, args=(link, i))
                t.daemon = True
                t.start()
                th.append(t)
            for t in th:
                t.join()
        else:
            for i, link in enumerate(self.chapter_links):
                self.extract_chapter(link, i)

    def extract_volume_name(self, src):
        title = re.search(r'<h3 class="am-text-center">(.*?)</h3>', str(src)).group(1).strip()
        if len(title.split()) == 2:
            self.volume_number, self.volume_name = title.split()
            self.print_info('{} {}'.format(self.volume_number, self.volume_name))
        else:
            self.volume_number = title
            self.print_info(self.volume_name)

    def extract_volume_url(self, src):
        links = re.findall(r'<a class="am-text-truncate" href="(.*?)">.*?</a>', str(src))
        self.chapter_links = links

    def parse_book(self, tag):
        self.extract_volume_name(str(tag))
        self.extract_volume_url(str(tag))
        self.parse_content()
        self.novel_information.append(
            {'chapters': self.chapters, 'volume_name': self.volume_name, 'volume_number': self.volume_number,
             'book_name': self.book_name, 'filename': self.filename, 'author': self.author,
             'illustrator': self.illustrator, 'introduction': self.introduction,
             'cover_url': self.cover_url, 'date': self.date, 'source': self.url})
        self.chapters = []
        self.chapter_links = []

    def extract_common_information(self, soup):
        self.book_name = soup.find('h1', {'itemprop': 'name'}).text
        self.author = soup.find('a', {'itemprop': 'author'}).text
        self.introduction = soup.find('div', {'itemprop': 'description'}).text
        self.cover_url = self.find_cover_url(soup)
        self.find_date(soup)

    def parse_vollist(self):
        soup = self.parse_page(self.url)
        volumes = soup.select('div.am-panel-bd.book-info')
        self.extract_common_information(soup)
        for volume in volumes[1:-2]:
            self.parse_book(volume)

    def extract_novel_information(self):
        """extract novel information"""
        self.parse_vollist()
        self.print_info('Extract {} completed'.format(self.book_name))

    def get_novel_information(self):
        return self.novel_information
