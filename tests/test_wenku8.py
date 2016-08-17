import os
import sys

sys.path.append(os.path.dirname(os.path.abspath('__file__')))

from novel_wenku8 import Wenku


class TestWenku:
    novel = Wenku('http://www.wenku8.com/book/1269.htm')

    def test_all(self):
        assert self.novel.extract_novel_information() is None

    def test_bookname(self):
        assert self.novel.novel_information[0]['book_name'] == '游戏人生No game No life'

    def test_author(self):
        assert self.novel.novel_information[0]['author'] == '榎宫佑'

    def test_chapters(self):
        assert len(self.novel.novel_information[0]['chapters']) == 7

    def test_volume_number(self):
        assert self.novel.novel_information[0]['volume_number'] == '第一卷'

    def test_volume_name(self):
        assert self.novel.novel_information[0]['volume_name'] == '听说游戏玩家兄妹要征服幻想世界'

    def test_filename(self):
        assert self.novel.novel_information[0]['filename'] == '第一卷 听说游戏玩家兄妹要征服幻想世界'
