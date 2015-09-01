import json
import threading
import re

from bs4 import BeautifulSoup
import requests

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}


class Novel:
    """
    get novel information for creating epub file

    Attributes:
        volume_name: A string represent the volume name
        volume_number: A string represent the volume number
        volume_author: A string represent the author
        volume_illustrator: A string represent the illustrator
        volume_introduction: A string represent the introduction
        volume_cover_url: A string represent the cover_url
        chapter_links: A string represent the chapter links
        output_dir: A stirng represent the epub save path
        cover_path: A string represent the cover path
        book_name: A string represent the book name
        chapter: A list represent the chapter
        base_path: A string represent the epub temp path

    """

    def __init__(self, url, single_thread):
        self.url = url
        self.single_thread = single_thread

        self.chapters = []
        self.volume_name = ''
        self.volume_number = ''
        self.author = ''
        self.illustrator = ''
        self.introduction = ''
        self.cover_url = ''
        self.chapters_links = []
        self.base_path = ''

    @staticmethod
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
        return BeautifulSoup(r.text)

    @staticmethod
    def find_chapter_links(soup):
        """
        extract chapter links from page

        Args:
            soup: A parsed page

        Returns:
            a list contains the book's chapter links
        """
        base_url = 'http://www.linovel.com/'
        temp_chapter_links = soup.select('div.linovel-chapter-list a')
        find_chapter_links = re.compile(r'<a href="(.*)">')
        chapter_links = []
        for i in temp_chapter_links:
            chapter_links.append(base_url + find_chapter_links.search(str(i)).group(1))
        return chapter_links

    def find_volume_name_number(self, soup):
        """get the volume name and number"""
        name_and_number = soup.select('h3')[0].string.split()
        self.volume_name = name_and_number[1].strip()
        self.volume_number = name_and_number[0].strip()
        if re.search(r'^\d+$', self.volume_number):
            self.volume_number = '第' + self.volume_number + '卷'
        self.print_info('Volume_name:' + self.volume_name + '\nVolume_number:' + self.volume_number)

    @property
    def book_name(self):
        return self.volume_name + ' ' + self.volume_number

    def find_author_illustrator(self, soup):
        """get the author and illustrator"""
        temp_author_name = soup.select('div.linovel-info p')[1]
        find_author_name = re.compile(r'<a href="/n/search/.*?">(.*?)</a>')
        find_illustrator_name = re.compile(r'<label>(.*?)</label>')
        self.author = find_author_name.search(str(temp_author_name)).group(1)
        self.illustrator = find_illustrator_name.findall(str(temp_author_name))[2]
        self.print_info('Author:' + self.author + '\nIllustrator:' + self.illustrator)

    def find_introduction(self, soup):
        """get the introduction"""
        temp_introduction = soup.select('p.linovel-info-desc')[0]
        self.introduction = temp_introduction.string

    def find_cover_url(self, soup):
        temp_cover_url = soup.select('div.linovel-cover')[1]
        find_cover_url = re.compile(r'<img src="(.*)"/>')
        self.cover_url = find_cover_url.search(str(temp_cover_url)).group(1)

    def extract_epub_info(self):
        """
        extract volume's basic info

        Args:
            soup: A parsed page

        Return:
            A dict contains the volume's info
        """
        soup = self.parse_page(self.url)

        self.find_volume_name_number(soup)
        self.find_author_illustrator(soup)
        self.find_introduction(soup)
        self.find_cover_url(soup)
        self.chapters_links = self.find_chapter_links(soup)

    @staticmethod
    def get_content(soup):
        """extract var content from html source"""
        return re.search(r'var content = ({.*?};)', str(soup).replace('\n', '')).group(1)[:-1]

    @staticmethod
    def get_new_chapter_name(content, number):
        """
        get the chapter name

        Args:
            content: str

        Returns:
            A string contain the chapter name
        """
        chapter_name = re.search(r'subTitle:"(.*?)"', content).group(1).strip()
        new_chapter_name = '第' + str(number + 1) + '章 ' + chapter_name
        return new_chapter_name

    @staticmethod
    def print_info(info):
        """print info, ignore UnicodeDecodeError"""
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
        Returns:
            chapters: list contains the content of each paragraph
        """
        chapter_content = re.search(r'content:(\[.*\])', content).group(1)
        chapter_content = json.loads(chapter_content)
        chapters = []
        for i in chapter_content:
            chapters.append(i['content'])
        return chapters

    def add_chapter(self, chapter):
        """
        add chapter
        chapter structure：a tuple (chapter number, chapter name, chapter_content)
        """
        self.chapters.append(chapter)

    def extract_chapter(self, url, number):
        """
        add each chapter's content to the Epub instance

        Args:
            url: A string represent the chapter url to be added
            epub: A Epub instance
            number: A int represent the chapter's number
        """
        try:
            soup = self.parse_page(url)
            content = self.get_content(soup)
            new_chapter_name = self.get_new_chapter_name(content, number)
            self.print_info(new_chapter_name)
            chapter_content = self.get_chapter_content(content)
            self.add_chapter((number, new_chapter_name, chapter_content))

        except Exception as e:
            print('错误', str(e) + '\nAt:' + url)
            raise e

    def parse_content(self):
        """
        start extract every chapter in epub

        Args:
            epub: The Epub instance to be created
        """
        th = []

        if not self.single_thread:
            for i, link in enumerate(self.chapters_links):
                t = threading.Thread(target=self.extract_chapter, args=(link, i))
                t.daemon = True
                t.start()
                th.append(t)
            for t in th:
                t.join()
        else:
            for i, link in enumerate(self.chapters_links):
                self.extract_chapter(link, i)

    def get_novel_information(self):
        """get novel information"""
        self.extract_epub_info()
        self.parse_content()
        self.print_info(self.book_name + ' 信息获取完成')

    def novel_information(self):
        return {'chapter': self.chapters, 'volume_name': self.volume_name, 'volume_number': self.volume_number,
                'book_name': self.book_name, 'author': self.author,
                'illustrator': self.illustrator, 'introduction': self.introduction, 'cover_url': self.cover_url}
