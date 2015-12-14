from abc import ABCMeta, abstractmethod, abstractstaticmethod

from bs4 import BeautifulSoup
import requests


class AbstractNovel:
    """
    abstract novel class

    Attributes:
        url: The novel url
        single_thread: A bool represent whether use single thread grab novel information
        volume_name: A string represent the volume name
        volume_number: A string represent the volume number
        book_name: A string represent the book name
        author: A string represent the author
        illustrator: A string represent the illustrator
        introduction: A string represent the introduction
        chapters: A list represent the chapter
        cover_url: A string represent the cover_url
        date: A string represent the date the book last updated (As specified in ISO 8601)
        novel_information: A list contains dict which represent the novel information
    """

    __metaclass__ = ABCMeta

    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}

    def __init__(self, url, single_thread=False):
        self.url = url
        self.single_thread = single_thread
        self.volume_name = ''
        self.volume_number = ''
        self.author = ''
        self.illustrator = ''
        self.introduction = ''
        self.chapters = []
        self.cover_url = ''
        self.date = ''
        self.novel_information = []

    def __str__(self):
        return '{}:{}'.format(self.__name__, self.url)

    @abstractstaticmethod
    def check_url(url):
        """check whether the url match this website"""
        pass

    @property
    def book_name(self):
        return self.volume_name + ' ' + self.volume_number

    def parse_page(self, url):
        """
        parse page with BeautifulSoup

        Args:
            url: A string represent the url to be parsed

        Return:
            A BeatifulSoup element
        """
        r = requests.get(url, headers=self._HEADERS)
        r.encoding = 'utf-8'
        return BeautifulSoup(r.text, 'lxml')

    @abstractmethod
    def extract_novel_information(self):
        """extract novel information"""
        pass

    @abstractmethod
    def get_novel_information(self):
        """
        return the novel information

        Return:
            A list contains dict, dict usually has these information: volume_name, volume_number, book_name,
            author, illustrator, introduction, chapters, cover_url, date
        """
        pass
