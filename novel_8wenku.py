import html
import re
import threading

from novel import AbstractNovel


class WenkuNoBQ(AbstractNovel):
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
        url_checker = re.compile(r'http://www.8wenku.com/book/(\d+)')
        return True if url_checker.search(url) else False

    @staticmethod
    def find_cover_url(soup):
        img = soup.select('div.imgbox a img')
        url = img[0]['src']
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
        i = src.select('div.article-body')[0]
        lines = []
        for j in i.text.split('\n'):
            if j.strip():
                lines.append(j.strip())
        if len(lines)>=3:
            lines = lines[2:-1]
        for i in re.findall(r'src="(http.*?(jpg|png))', str(i)):
            lines.append('[img]' + i[0] + '[\img]')
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
            chapter_name = soup.select('div.article-title h1')[0].text
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
        title = re.search(r'<a href="/volume/(.*?)">(.*?)</a>', str(src)).group(2).strip()
        if len(title.split()) >= 2:
            index = title.find('卷')
            self.volume_number, self.volume_name = title[:index + 1], title[index + 2:]
        else:
            self.volume_number = title
            self.volume_name = ''
        self.print_info('{} {}'.format(self.volume_number, self.volume_name))

    def extract_volume_url(self, src):
        links_tag=src.find_next('div',{'class':'abook_contents_list'}).contents[1].find_all('li',{'class':'vip'})
        links=re.findall(r'href="(.*?)"',str(links_tag))
        for index in range(len(links)):
            links[index]=links[index].replace('&amp;','&')
            links[index]='http://www.8wenku.com'+links[index]
        
        self.chapter_links = links

    def parse_book(self, tag):
        self.extract_volume_name(str(tag))
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
        self.book_name = soup.select('div.tit_bg h2.tit')[0].text
        self.author = ''
        self.introduction = soup.select('div.summary p.desc')[0].text
        self.cover_url = self.find_cover_url(soup)
        self.find_date(soup)

    def parse_vollist(self):
        soup = self.parse_page(self.url)
        volumes = soup.find_all('div',{'class':'hd'})
        self.extract_common_information(soup)
        for volume in volumes[0:-3]:
            self.parse_book(volume)

    def extract_novel_information(self):
        """extract novel information"""
        self.parse_vollist()
        self.print_info('Extract {} completed'.format(self.book_name))

    def get_novel_information(self):
        return self.novel_information
