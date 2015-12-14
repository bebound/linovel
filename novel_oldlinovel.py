import json
import threading
import re

import requests

from novel import AbstractNovel


class OldLinovel(AbstractNovel):
    """
    old linovel class, deal with url such as:
    http://old.linovel.com/n/vollist/492.html or
    http://old.linovel.com/n/book/1578.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chapter_links = []

    @staticmethod
    def check_url(url):
        vollist = re.compile(r'http://old.linovel.com/n/vollist/(\d+).html')
        book = re.compile(r'http://old.linovel.com/n/book/(\d+).html')
        return True if vollist.search(url) or book.search(url) else False

    @staticmethod
    def is_vollist(url):
        vollist = re.compile(r'http://old.linovel.com/n/vollist/(\d+).html')
        return True if vollist.search(url) else False

    def find_volume_name_number(self, soup):
        """
        get the volume name and number

        Args:
            soup: bs4 parsed page
        """
        name = soup.select('h1')[1].string.strip()
        self.volume_name = name
        name_and_number = soup.select('h3')[0].string.split()
        self.volume_number = name_and_number[0].strip()
        if re.search(r'^\d+$', self.volume_number):
            self.volume_number = '第' + self.volume_number + '卷'
        self.print_info('Volume_name:{}\nVolume_number:'.format(self.volume_name, self.volume_number))

    def find_author_illustrator(self, soup):
        """
        get the author and illustrator

        Args:
            soup: bs4 parsed page
        """
        temp_author_name = soup.select('div.linovel-info p')[1]
        find_author_name = re.compile(r'<a href="/n/search/.*?">(.*?)</a>')
        find_illustrator_name = re.compile(r'<label>(.*?)</label>')
        self.author = find_author_name.search(str(temp_author_name)).group(1)
        self.illustrator = find_illustrator_name.findall(str(temp_author_name))[2]
        self.print_info('Author: {}\nIllustrator:{}'.format(self.author, self.illustrator))

    def find_introduction(self, soup):
        """
        get the novel introduction

        Args:
            soup: bs4 parsed page
        """
        introduction = soup.select('p.linovel-info-desc')[0].get_text()
        self.introduction = introduction

    def find_cover_url(self, soup):
        temp_cover_url = soup.select('div.linovel-cover')[0]
        find_cover_url = temp_cover_url.find('img')
        cover_url = find_cover_url['src']
        r = requests.get(cover_url)
        self.cover_url = r.url.replace('!min250jpg', '')

    def find_date(self, soup):
        raw_date = soup.find_all(string=re.compile("^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"))
        self.date = raw_date[0].split(' ')[0]

    @staticmethod
    def find_chapter_links(soup):
        """
        extract chapter links from page

        Args:
            soup: bs4 parsed page

        Return:
            chapter_links: a list contains chapter links
        """
        base_url = 'http://old.linovel.com/'
        temp_chapter_links = soup.select('div.linovel-chapter-list a')
        find_chapter_links = re.compile(r'<a href="/(.*)">')
        chapter_links = []
        for i in temp_chapter_links:
            chapter_links.append(base_url + find_chapter_links.search(str(i)).group(1))
        return chapter_links

    def extract_epub_info(self, url):
        """
        extract volume's basic info

        Args:
            url: epub url
        """
        print('Getting:{}'.format(url))
        soup = self.parse_page(url)

        self.find_volume_name_number(soup)
        self.find_author_illustrator(soup)
        self.find_introduction(soup)
        self.find_cover_url(soup)
        self.find_date(soup)
        self.chapter_links = self.find_chapter_links(soup)

    @staticmethod
    def get_content(soup):
        """
        extract var content from html source

        Args:
            soup: bs4 parsed page

        Return:

        """
        return re.search(r'var content=({.*?};)', str(soup).replace('\n', '')).group(1)[:-1]

    @staticmethod
    def get_new_chapter_name(content, number):
        """
        get the chapter name

        Args:
            content: a string represent the content of chapter
            number: a int represent the sequence of chapter

        Return:
            A string contain the chapter name
        """
        chapter_name = re.search(r'subTitle:"(.*?)"', content).group(1).strip()
        new_chapter_name = '第' + str(number + 1) + '章 ' + chapter_name
        return new_chapter_name

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

    @staticmethod
    def get_chapter_content(content):
        """
        extract chapter content from content

        Args:
            content: str

        Return:
            chapters: list contains the content of each paragraph
        """
        content = re.sub(r'(title|subTitle|series_id|chapter_id|vol_id|chapterIndexs|index|content|isSpace):', r'"\1":',
                         content)
        content = re.sub(r'(![01])}', r'"\1"}', content)
        chapter_content = json.loads(content)['content']
        chapters = []
        for i in chapter_content:
            chapters.append(i['content'])
        return chapters

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
            content = self.get_content(soup)
            chapter_name = self.get_new_chapter_name(content, number)
            self.print_info(chapter_name)
            chapter_content = self.get_chapter_content(content)
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

    def parse_book(self, url=''):
        target = self.url if not url else url
        self.extract_epub_info(target)
        self.parse_content()
        self.novel_information.append(
                {'chapters': self.chapters, 'volume_name': self.volume_name, 'volume_number': self.volume_number,
                 'book_name': self.book_name, 'author': self.author,
                 'illustrator': self.illustrator, 'introduction': self.introduction,
                 'cover_url': self.cover_url, 'date': self.date})
        self.chapters = []
        self.chapter_links = []

    def parse_vollist(self):
        soup = self.parse_page(self.url)
        volume_links = soup.select('li.linovel-book-item h3 a')
        for volume in volume_links:
            volume_url = 'http://old.linovel.com' + volume['href']
            self.parse_book(volume_url)

    def extract_novel_information(self):
        """extract novel information"""
        if self.is_vollist(self.url):
            self.parse_vollist()
        else:
            self.parse_book()
        self.print_info('Extract {} completed'.format(self.book_name))

    def get_novel_information(self):
        return self.novel_information
