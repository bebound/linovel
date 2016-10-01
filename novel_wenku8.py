import re
import threading

from novel import AbstractNovel


class Wenku(AbstractNovel):
    """
    wenku8.com class, deal with url such as:
    http://www.wenku8.com/book/1269.htm
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
        url_checker = re.compile(r'http://www.wenku8.com/book/(\d+).htm')
        return True if url_checker.search(url) else False

    @staticmethod
    def find_cover_url(soup):
        img = soup.select('div#content table img')
        return img[0]['src']

    def find_date(self, soup):
        date = soup.find(string=re.compile("^\d{4}-\d{2}-\d{2}"))
        self.date = date

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
    def get_chapter_content(soup):
        i = soup.select('div#content')[0]
        lines = []
        is_img = False
        if 'divimage' in str(i):
            is_img = True
            for i in re.findall(r'src="(http.*?(jpg|png))', str(i)):
                lines.append('[img]' + i[0] + '[\img]')
        else:
            for j in i.text.split('\n'):
                if j.strip():
                    lines.append(j.strip())
        return lines if is_img else lines[1:-1]

    def add_chapter(self, chapter):
        """
        add chapter

        Args:
            chapter: a tuple (chapter number, chapter name, chapter_content)
        """
        self.chapters.append(chapter)

    def extract_chapter(self, volume_title, url, number):
        """
        add each chapter's content to the epub instance

        Args:
            url: A string represent the chapter url to be added
            number: A int represent the chapter's number
        """
        try:
            soup = self.parse_page(url, 'gbk')
            chapter_name = soup.select('div#title')[0].text[len(volume_title):].strip()
            self.print_info(chapter_name)
            chapter_content = self.get_chapter_content(soup)
            self.add_chapter((number, chapter_name, chapter_content))

        except Exception as e:
            print('错误', str(e), '\nAt:', url)
            raise e

    def parse_content(self, volume_title, urls):
        """start extract every chapter in epub"""
        print('Start parsing chapters')
        th = []

        if not self.single_thread:
            for i, url in enumerate(urls):
                t = threading.Thread(target=self.extract_chapter, args=(volume_title, url, i))
                t.daemon = True
                t.start()
                th.append(t)
            for t in th:
                t.join()
        else:
            for i, url in enumerate(urls):
                self.extract_chapter(volume_title, url, i)

    def extract_volume_name(self, title):
        if '卷' in title:
            index = title.find('卷')
            self.volume_number, self.volume_name = title[:index+1], title[index+2:]
            self.print_info('{} {}'.format(self.volume_number, self.volume_name))
        else:
            self.volume_number = title
            self.volume_name = ''
            self.print_info(self.volume_number)

    def parse_book(self, volume_title, urls):
        self.extract_volume_name(volume_title)
        self.parse_content(volume_title, urls)
        self.novel_information.append(
            {'chapters': self.chapters, 'volume_name': self.volume_name, 'volume_number': self.volume_number,
             'book_name': self.book_name, 'filename': self.filename, 'author': self.author,
             'illustrator': self.illustrator, 'introduction': self.introduction,
             'cover_url': self.cover_url, 'date': self.date, 'source': self.url})
        self.chapters = []
        self.chapter_links = []

    def get_book_name(self, soup):
        return re.search(r'《(.*)》小说打包', str(soup)).group(1)

    def get_author_name(self, soup):
        return re.search(r'<meta content=".*是([\w\s]+?)所写的轻小说', str(soup)).group(1)

    def get_introduction(self, soup):
        span = soup.select('div#content table span')
        start = False
        introduction = ''
        for i in span:
            if i.text == '内容简介：':
                start = True
                continue
            if i.text == '同分类小说推荐':
                break
            elif start:
                introduction += i.text
        return introduction

    def extract_common_information(self, soup):
        self.book_name = self.get_book_name(soup)
        self.author = self.get_author_name(soup)
        self.introduction = self.get_introduction(soup)
        self.cover_url = self.find_cover_url(soup)
        self.find_date(soup)

    def get_volumes_url(self, soup):
        url = re.search(r'<a href="(http://www.wenku8.com/novel/.*?index.htm)">小说目录</a>', str(soup)).group(1)
        return url

    def extract_volumes(self, soup):
        """parse the novle content page, start parse each volume"""
        url = self.get_volumes_url(soup)
        soup = self.parse_page(url, 'gbk')
        td = soup.select('table td')
        newtd = []
        for t in td:
            if len(t) > 1:
                newtd.extend(t)
            else:
                newtd.append(t)
        volume_titles = []
        chapter_urls = []
        single_volume_urls = []
        for i in newtd:
            if i['class'] == ['vcss']:
                if single_volume_urls:
                    chapter_urls.append(single_volume_urls)
                    single_volume_urls = []
                volume_titles.append(i.text.strip())
            elif str(i) != '<td class="ccss"> </td>':
                chapter_url = re.search(r'href="(\d+\.htm)"', str(i)).group(1)
                page_url = url.replace('index.htm', chapter_url)
                single_volume_urls.append(page_url)
        if single_volume_urls:
            chapter_urls.append(single_volume_urls)

        for title, urls in zip(volume_titles, chapter_urls):
            self.parse_book(title, urls)

    def parse_vollist(self):
        soup = self.parse_page(self.url, 'gbk')
        self.extract_common_information(soup)
        self.extract_volumes(soup)

    def extract_novel_information(self):
        """extract novel information"""
        self.parse_vollist()
        self.print_info('Extract {} completed'.format(self.book_name))

    def get_novel_information(self):
        return self.novel_information
