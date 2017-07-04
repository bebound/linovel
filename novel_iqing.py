import html
import re
import threading
import json

from novel import AbstractNovel


class IQing(AbstractNovel):
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
        url_checker = re.compile(r'http://www.iqing.in/book/(\d+)')
        return True if url_checker.search(url) else False

    @staticmethod
    def find_cover_url(soup):
        img = soup.select('div#book-top div img')
        url = img[0]['src']
        return url

    def find_date(self, soup):
        self.date = ''

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
        i = src['results']
        lines = []
        for j in i:
            if j['type']==0:
                for note in j['value'].split('\n'):
                    lines.append(note)
            else:
                lines.append('[img]' +j['value'] + '[\img]')
        return lines

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
            iqing_chap_json=json.loads(soup.text)
            chapter_name = iqing_chap_json['chapter_title']
            self.print_info(chapter_name)
            chapter_content = self.get_chapter_content(iqing_chap_json)
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
        title = src.contents[1].text
        if len(title.split()) >= 2:
            index = title.find('卷')
            self.volume_number, self.volume_name = title[:index + 1], title[index + 2:]
        else:
            self.volume_number = title
            self.volume_name = ''
        self.print_info('{} {}'.format(self.volume_number, self.volume_name))

    def extract_volume_url(self, src):
        lis=src.contents[3].find_all('li',{'class':'chapter'})
        links=[]
        for index in range(len(lis)):
            read_url=lis[index].find('a').attrs['href'].replace('/read/','')
            links.append('http://www.iqing.in/content/'+read_url+'/chapter')        
        self.chapter_links = links

    def parse_book(self, tag):
        self.extract_volume_name(tag)
        self.extract_volume_url(tag)
        self.parse_content()
        self.novel_information.append(
            {'chapters': self.chapters, 'volume_name': self.volume_name, 'volume_number': self.volume_number,
             'book_name': self.book_name, 'filename': self.filename, 'author': self.author,
             'illustrator': self.illustrator, 'introduction': self.introduction,
             'cover_url': self.cover_url, 'date': self.date, 'source': self.url})
        self.chapters = []
        self.chapter_links = []

    def extract_common_information(self, soup):
        self.book_name = soup.select('div.book-title h1')[0].text
        self.author = ''
        self.introduction = soup.select('p.intro')[0].text
        self.cover_url = self.find_cover_url(soup)
        self.find_date(soup)

    def parse_vollist(self):
        soup = self.parse_page(self.url)
        volumes = soup.find_all('li',{'class':'volume'})
        self.extract_common_information(soup)
        for volume in volumes:
            self.parse_book(volume)

    def extract_novel_information(self):
        """extract novel information"""
        self.parse_vollist()
        self.print_info('Extract {} completed'.format(self.book_name))

    def get_novel_information(self):
        return self.novel_information
