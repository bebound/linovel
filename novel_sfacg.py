import html
import re
import threading

from novel import AbstractNovel


class SFAcg(AbstractNovel):
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
        url_checker = re.compile(r'http://book.sfacg.com/Novel/(\d+)/MainIndex/')
        return True if url_checker.search(url) else False

    @staticmethod
    def find_cover_url(soup):
        return 'http://rs.sfacg.com/web/novel/images/NovelCover/Big/2017/03/afa9292d-1b33-40b4-92b7-6834e1126f08.jpg'

    def find_date(self, soup):
        self.date=None


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
        i = src.select('span#ChapterBody')[0].contents[1].contents
        lines = []
        for j in i:
            if not hasattr(j,'text'):
                lines.append(j.strip())
            else:
                if j.name=='img':
                    lines.append('[img]' + j.attrs['src'] + '[\img]')
                else:
                    lines.append(j.text.strip())
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
            chapter_name = soup.select('div.list_menu_title')[0].text
            self.print_info(chapter_name)
            chapter_content = self.get_chapter_content(soup)
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
        links_tag=src.find_next('div',{'class':'catalog-list'}).contents[1].find_all('li')
        links=[]        
        for index in range(len(links_tag)):            
            links.append('http://book.sfacg.com'+links_tag[index].find('a').attrs['href'])        
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
        self.book_name = soup.select('h1.story-title')[0].text
        self.author = ''
        self.introduction = ''
        self.cover_url = self.find_cover_url(soup)
        self.find_date(soup)

    def parse_vollist(self):
        soup = self.parse_page(self.url)
        volumes=soup.find_all('div',{'class':'catalog-hd'})
        self.extract_common_information(soup)
        for volume in volumes:
            self.parse_book(volume)

    def extract_novel_information(self):
        """extract novel information"""
        self.parse_vollist()
        self.print_info('Extract {} completed'.format(self.book_name))

    def get_novel_information(self):
        return self.novel_information
