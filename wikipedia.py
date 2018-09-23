# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import os


def lssdjt(mouth):
    """当月每天 历史上的今天"""

    u = '历史上的今天/{}月'.format(mouth)

    r = requests.get("https://zh.wikipedia.org/zh-cn/Wikipedia:{}".format(u))
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.findAll('dl')

    day = 1
    for i in a[1:]:
        for m, n in zip(i.findAll('dt'), i.findAll('dd')):
            print(mouth, day, m.text.replace('年', ''), n.text)
        day += 1
        print('\n')


def lssdjt_more(mouth, day):
    """更多历史上的今天"""

    u = '{}月{}日'.format(mouth, day)

    r = requests.get("https://zh.wikipedia.org/zh-cn/{}".format(u))
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.findAll('ul')

    for i in a:
        for n in i.findAll('li'):
            if '年：' in n.text:
                print(mouth, day, n.text)


def lssdjt_sj(m):
    """ 大事记：世纪 """

    u = '{}世纪'.format(m)
    if os.path.isfile('wikipedia/世纪/S{}.tex'.format(m)):
        return

    r = requests.get("https://zh.wikipedia.org/zh-cn/{}".format(u))
    r.encoding = 'utf8'

    fh = open('wikipedia/世纪/S{}.tex'.format(m), 'w', encoding='utf8')
    fh.write(r'{\large \bfseries ' + '{}世纪'.format(m) + '}\n' + '\n' + r'\vspace{0.1cm}' + '\n\n')

    soup0 = BeautifulSoup(r.text.split('<div id="toc"')[0], "lxml")
    a0 = soup0.findAll('p')
    if a0:
        for a in a0:
            fh.write(a.text + '\n')
        fh.write('\n' + r'\vspace{0.1cm}' + '\n\n')
    else:
        pass

    reg = r'成就">重要事件、发展与成就(.*?)<h2>'
    a = re.findall(reg, r.text, re.S)

    if a:
        aa = re.findall(r'<li>(<b>.*?)</ul>', a[0], re.S)
        for i in aa:
            # print(i)
            soup = BeautifulSoup(i, "lxml")
            b = soup.b.text

            li = soup.findAll('li') if soup.findAll('li') else ''
            if li:
                fh.write(r'{\bfseries ' + b + '}\n' + '\n')
            for j in li:
                aaa = re.findall(r'(<ul>.*?)$', str(j), re.S)
                if aaa:
                    j = str(j).replace(aaa[0], '')
                    j = BeautifulSoup(j, "lxml")
                j = j.text.replace('——', ': ').replace('%', '\%').replace('_', '')
                if not j:
                    continue
                if j[0].isdigit():
                    fh.write(j + '\n' + '\n')
                else:
                    fh.write('•' + j + '\n' + '\n')
        fh.write(r'\vspace{0.1cm}' + '\n\n')

    def part(reg):
        reg_cpl = re.compile(reg, re.S)
        a = re.findall(reg_cpl, r.text)
        if a:
            aa = re.findall(r'(<span class="mw-headline".*?)<h\d>', a[0], re.S)
            for i in aa:
                soup = BeautifulSoup(i, "lxml")
                b = soup.select('span.mw-headline')[0].text
                if '分类' not in soup.text:
                    li = soup.findAll('li') if soup.findAll('li') else ''
                    if li: fh.write(r'{\bfseries ' + b + '}\n' + '\n')
                    for j in li:
                        aaa = re.findall(r'(<ul>.*?)$', str(j), re.S)
                        if aaa:
                            j = str(j).replace(aaa[0], '')
                            j = BeautifulSoup(j, "lxml")
                        j = j.text.replace('——', ': ').replace('%', '\%')
                        if not j:
                            continue
                        if j[0].isdigit():
                            fh.write(j + '\n' + '\n')
                        else:
                            fh.write('•' + j + '\n' + '\n')

    reg = r'成就">重要事件、发展与成就(.*?)<h2>'
    part(reg)

    reg = r'id="重要人物">重要人物(.*?)<h2>'
    part(reg)

    fh.write(r'\vspace{0.6cm}' + '\n\n')

    fh.close()

    print("世纪:", m)


def lssdjt_dj_1(m):
    """ 大事记：代纪  公元前"""

    u = '前{}年代'.format(m)
    if os.path.isfile('wikipedia/年代/BC{}.tex'.format(m)):
        return

    r = requests.get("https://zh.wikipedia.org/zh-cn/{}".format(u))
    r.encoding = 'utf8'

    reg = r'记">大事记</span>(.*?)<h2>'
    a = re.findall(reg, r.text, re.S)
    if a:
        soup = BeautifulSoup(a[0], "lxml")
        li = soup.findAll('li')
        with open('wikipedia/年代/BC{}.tex'.format(m), 'w', encoding='utf8') as fh:
            fh.write(r'{\bfseries ' + '前{}年代'.format(m) + '}\n' + '\n' + r'\vspace{0.1cm}' + '\n\n')
            for i in li:
                i = i.text.replace('——', ': ').replace('%', '\%')
                if i[0].isdigit():
                    fh.write(i + '\n' + '\n')
                else:
                    fh.write('•' + i + '\n' + '\n')
            fh.write(r'\vspace{0.1cm}' + '\n\n')

    print("公元前代纪:", m)


def lssdjt_dj_2(m):
    """公元后"""

    u = '{}年代'.format(m)
    if os.path.isfile('wikipedia/年代/{}.tex'.format(m)):
        return

    r = requests.get("https://zh.wikipedia.org/zh-cn/{}".format(u))
    r.encoding = 'utf8'

    reg = r'记">大事记</span>(.*?)<h2>'
    a = re.findall(reg, r.text, re.S)
    if not a:
        return
    soup = BeautifulSoup(a[0], "lxml")
    li = soup.findAll('li')
    if li:
        with open('wikipedia/年代/{}.tex'.format(m), 'w', encoding='utf8') as fh:
            fh.write(r'{\bfseries ' + '{}年代'.format(m) + '}\n' + '\n' + r'\vspace{0.1cm}' + '\n\n')
            for i in li:
                i = i.text.replace('——', ': ').replace('%', '\%')
                if i[0].isdigit():
                    fh.write(i + '\n' + '\n')
                else:
                    fh.write('•' + i + '\n' + '\n')
            fh.write(r'\vspace{0.1cm}' + '\n\n')

    print("公元后代纪:", m)


def lssdjt_nj(m):
    """ 大事记：年纪"""

    u = '{}年'.format(m)
    if os.path.isfile('wikipedia/年/{}.tex'.format(m)):
        return

    r = requests.get("https://zh.wikipedia.org/zh-cn/{}".format(u))
    r.encoding = 'utf8'
    soup0 = BeautifulSoup(r.text, "lxml")
    td = soup0.findAll('td', {'align': "center"})
    if td:
        td = td[4].text

    reg = r'记">大事记</span>(.*?)<h2>'
    a = re.findall(reg, r.text, re.S)
    if not a:
        return
    soup = BeautifulSoup(a[0], "lxml")
    li = soup.findAll('li')

    with open('wikipedia/年/{}.tex'.format(m), 'w', encoding='utf8') as fh:
        fh.write(r'\subsection*{' + '{}年'.format(m) + '}\n' + '\n')
        fh.write(r'{\itshape \bfseries ' + td + '}\n' + '\n' + r'\vspace{0.1cm}' + '\n\n')
        for i in li:
            i = i.text.replace('——', ': ').replace('%', '\%').replace('&', '\&')
            if i[0].isdigit():
                fh.write(i + '\n' + '\n')
            else:
                fh.write('•' + i + '\n' + '\n')

    print("年纪:", m)


def lssdjt_yj(y, m):
    """  大事记：月纪"""

    u = '{}年{}月'.format(y, m)
    if os.path.isfile('wikipedia/月/{}.{}.tex'.format(y, m)):
        return
    r = requests.get("https://zh.wikipedia.org/zh-cn/{}".format(u))
    r.encoding = 'utf8'

    reg = r'class="mw-headline"(.*?)<h2>'

    list_ = re.findall(reg, r.text, re.S)

    reg2 = r'">(\d.*?)</span><span class="mw-editsection">'

    days = []
    for i in list_:
        j = re.findall(reg2, i, re.S)
        if j:
            days.append(j[0].replace('</a>', ''))

    filename = 'wikipedia/月/{}.{}.tex'.format(y, m)
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'a', encoding='utf8') as fh:
        fh.write(r'\section*{' + '{}年{}月'.format(y, m) + '}\n' + '\n')

    if y < 2010 or (y == 2010 and m == 1):
        list_.reverse()
        days.reverse()
    else:
        pass

    if y < 2013 or (y == 2013 and m in [1, 2, 3, 4]) or (y == 2015 and m != 1) or y > 2015:

        for i, n in zip(list_, days):
            soup = BeautifulSoup(i, "lxml")
            li = soup.findAll('li')
            with open(filename, 'a', encoding='utf8') as fh:
                fh.write(r'{\bfseries ' + n + '}\n' + '\n')
                for j in li:
                    item = j.text
                    reg3 = r'。([^。]*?)$'
                    xx = re.findall(reg3, item, re.S)
                    if xx:
                        item = item.replace(xx[0], '')
                    re_dic = {
                        '%': '\%',
                        '^': ' ',
                        '#': ' ',
                        '&': '\&',
                        '$': '\$',
                        '_': ' ',
                        '{': ' ',
                    }
                    for k, v in re_dic.items():
                        item = item.replace(k, v)

                    if len(item) > 10:
                        fh.write('•' + item + '\n' + '\n')
    else:
        for i, n in zip(list_, days):
            with open(filename, 'a', encoding='utf8') as fh:
                fh.write(r'{\bfseries' + n + '}\n' + '\n')

                reg4 = r'<dl>(.*?)</ul>'
                l2 = re.findall(reg4, i, re.S)
                for x in l2:
                    soup = BeautifulSoup(x)
                    dt = soup.findAll('dt')
                    li = soup.findAll('li')
                    fh.write(r'{\bfseries ' + dt[0].text + '}\n' + '\n')
                    for j in li:
                        item = j.text
                        reg3 = r'。([^。]*?)$'
                        xx = re.findall(reg3, item, re.S)
                        if xx:
                            item = item.replace(xx[0], '')
                        re_dic = {
                            '%': '\%',
                            '^': ' ',
                            '#': ' ',
                            '&': '\&',
                            '$': '\$',
                            '_': ' ',
                            '{': ' ',
                        }
                        for k, v in re_dic.items():
                            item = item.replace(k, v)
                        fh.write('•' + item + '\n' + '\n')

    print("月纪", y, m)


def main():
    # 世纪
    for i in range(1, 22):
        lssdjt_sj(i)
    for i in range(1, 31):
        lssdjt_sj('前' + str(i))
    for i in [31, 33, 35, 40, 41]:
        lssdjt_sj('前' + str(i))

    # 代记
    m = 10
    for i in range(200):
        if m > 700:
            break
        lssdjt_dj_1(m)
        m += 10

    m = 0
    for i in range(200):
        if m > 1900:
            break
        lssdjt_dj_2(m)
        m += 10

    # 年记
    for i in range(1835, 2003):
        lssdjt_nj(i)

    # 月记
    for i in range(2003, 2019):
        for j in range(1, 13):
            lssdjt_yj(i, j)


def main2():
    """laTex 编辑"""
    get = []
    for file_ in os.listdir('wikipedia/年代/'):
        if file_.endswith('.tex'):
            get.append(file_.replace('.tex', ''))
    BC, AD = [], []
    for i in get:
        if i[0].isdigit():
            AD.append(int(i))
        else:
            BC.append(int(i.replace('BC', '')))
    AD.sort()
    BC.sort()
    BC.reverse()
    for i in BC:
        print('\input{年代/BC' + str(i) + '}')
    for i in AD:
        print('\input{年代/' + str(i) + '}')

    for i in range(1835, 2004):
        print('\input{年/' + str(i) + '}')

    # 世纪
    for i in [31, 33, 35, 40, 41][::-1]:
        print('\input{{世纪/S前{}}}'.format(i))
    for i in list(range(1, 31))[::-1]:
        print('\input{{世纪/S前{}}}'.format(i))
    for i in range(1, 22):
        print('\input{{世纪/S{}}}'.format(i))


if __name__ == '__main__':
    main()
    main2()
