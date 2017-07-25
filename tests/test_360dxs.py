import os
import sys

sys.path.append(os.path.dirname(os.path.abspath('__file__')))

from novel_360dxs import Dxs


class TestDxs:
    novel = Dxs('http://dianjiwenku.360dxs.com/book_1672.html')

    def test_all(self):
        assert self.novel.extract_novel_information() is None

    def test_bookname(self):
        assert self.novel.novel_information[0]['book_name'] == '线上游戏的老婆不可能是女生？'

    def test_author(self):
        assert self.novel.novel_information[0]['author'] == '听猫芝居'

    def test_chapters(self):
        assert len(self.novel.novel_information[0]['chapters']) == 7

    def test_volume_number(self):
        assert self.novel.novel_information[0]['volume_number'] == '第一卷'

    def test_volume_name(self):
        assert self.novel.novel_information[0]['volume_name'] == ''

    def test_filename(self):
        assert self.novel.novel_information[0]['filename'] == '线上游戏的老婆不可能是女生？ 第一卷'
