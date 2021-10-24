import requests
import re
import os
import threading
import sys
import mkdir
import cpfiles

reload(sys)

sys.setdefaultencoding('utf-8')


class NovelSpider:

    def __init__(self):
        self.session = requests.Session()
        self.novels_folder_created_flag = False

    def get_novel(self, novel_url, no):
        novel_dir = 'C:/Users/Hang Yang/Desktop/novels/novel' + bytes(no)
        src_dir = 'C:/Users/Hang Yang/Desktop/novels/novel-original'
        dest_dir = novel_dir
        cpfiles.copy_files(src_dir, dest_dir)
        index_html = self.download(novel_url, 'gbk')
        # print(index_html)
        title = re.findall(r'<h2>(.*?)<i class="icon-book-status icon-book-status-finished"></i></h2>', index_html, re.S)[0]
        pic = re.findall(r'<div class="pic">(.*?)</div>', index_html, re.S)[0]
        image = re.findall(r'<img src="(.*?)" id="htmlBookPic".*?>', pic, re.S)[0]
        # print(title)
        # print(image)
        novel_chapter_infos = self.get_chapter_info(novel_url, index_html, 10)
        # self.save_novel(novel_chapter_infos, title)  # save novels in this project's Include folder
        self.build_novel_chapter_content(no, title, image, novel_chapter_infos)
        self.build_novel_content(no, novel_chapter_infos)

    def download(self, url, encoding):
        response = self.session.get(url)
        response.encoding = encoding
        html = response.text
        return html

    @staticmethod
    def get_chapter_info(novel_url, index_html, number):
        div = re.findall(r'<div class="bd">(.*?)</div>', index_html, re.S)[0]
        # print(div)
        ul = re.findall(r'<ul id="htmlChapterList" class="float-list fill-block">(.*?)</ul>', div, re.S)[0]
        # print(ul)
        li = re.findall(r'<li>(.*?)</li>', ul, re.S)
        # print(li)
        list = []
        for i in range(number):
            i = li[i]
            # print(i)
            link = re.findall(r'<a href="(.*?)" title=".*?" class="name ">.*?</a>', i, re.S)[0]
            link = novel_url + link
            title = re.findall(r'<a href=".*?" title=".*?" class="name ">(.*?)</a>', i, re.S)[0]
            # print(title)
            # print(link)
            pair = (title, link)
            list.append(pair)
        return list

    def get_content(self, chapter_url, encoding):
        chapter_html = self.download(chapter_url, encoding)
        content = re.findall(r'<div id="htmlContent" class="page-content ">(.*?)<div class="reward"', chapter_html, re.S)[0]
        # content = content.replace('<p>', '')
        # content = content.replace('</p>', '')
        # print(content)
        return content

    def save_novel(self, novel_chapter_infos, title):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\novels'
        if not self.novels_folder_created_flag:
            self.novels_folder_created_flag = mkdir.mkdir(dir_path)
        with open(dir_path + '/%s.txt' % title, 'w') as fb:
            for novel_chapter_info in novel_chapter_infos:
                title = novel_chapter_info[0]
                title = title.replace('&nbsp;', ' ')
                fb.write('%s\n' % title)
                content = self.get_content(novel_chapter_info[1], 'gbk')
                fb.write('%s\n' % content)
            fb.close()

    def build_novel_chapter_content(self, no, title, image, novel_chapter_infos):
        with open('C:/Users/Hang Yang/Desktop/novels/novel' + bytes(no) + '/0.html', 'r+') as f:
            content = f.read()
            content_new = re.sub(r'<h1.*?></h1>', '<h1 style="font-style: italic; margin-left: 60px;">' + title + '</h1>', content)
            content_new = re.sub(r'<img src=.*?>', '<img src="' + image + '" width="200">', content_new)

            index = 0
            for novel_chapter_info in novel_chapter_infos:
                content_new = re.sub(r'<a href=.*?class="name' + bytes(index + 1) + '"></a>',
                                         '<a href="' + bytes(index + 1) + '.html' + '" title="' + novel_chapter_info[0]
                                         + '" class="name' + bytes(index + 1) + '">' + novel_chapter_info[0] + '</a>', content_new)
                index += 1

            # print(content_new)
            f.seek(0, 0)
            f.write(content_new)
            f.close()

    def build_novel_content(self, no, novel_chapter_infos):
        index = 1
        for novel_chapter_info in novel_chapter_infos:
            novel_content = self.get_content(novel_chapter_info[1], 'gbk')
            f = open('C:/Users/Hang Yang/Desktop/novels/novel' + bytes(no) + '/' + bytes(index) + '.html', 'r+')
            content = f.read()
            content_new = re.sub(r'<h1></h1>', '<h1>' + novel_chapter_info[0] + '</h1>', content)
            content_new = re.sub(r'<div id="htmlContent" class="page-content ">\W*</div>', '<div id="htmlContent" class="page-content ">' + novel_content + '</div>', content_new, re.S)
            # print(content_new)
            f.seek(0, 0)
            f.write(content_new)
            index += 1
        f.close()
