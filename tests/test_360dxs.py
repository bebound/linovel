import os
import sys

sys.path.append(os.path.dirname(os.path.abspath('__file__')))

from novel_360dxs import Dxs


class TestDxs:
    novel = Dxs('http://qitawenku.360dxs.com/book_3037.html')

    def test_all(self):
        assert self.novel.extract_novel_information() is None

    def test_bookname(self):
        assert self.novel.novel_information[0]['book_name'] == 'No game No life游戏人生'

    def test_author(self):
        assert self.novel.novel_information[0]['author'] == '榎宫佑'

    def test_chapters(self):
        assert len(self.novel.novel_information[0]['chapters']) == 7

    def test_volume_number(self):
        assert self.novel.novel_information[0]['volume_number'] == '第一卷'

    def test_volume_name(self):
        assert self.novel.novel_information[0]['volume_name'] == '听说游戏玩家兄妹要征服幻想世界'

    def test_filename(self):
        assert self.novel.novel_information[0]['filename'] == 'No game No life游戏人生 第一卷 听说游戏玩家兄妹要征服幻想世界'
