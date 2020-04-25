import sys
import json
from lxml import html


pages = {
    # "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html": "rtv",
    # "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljsÌe v razredu - RTVSLO.si.html": "rtv",
    "../input-extraction/overstock.com/jewelry01.html": "overstock",
    "../input-extraction/overstock.com/jewelry02.html": "overstock",
}


def regex(page, site):
    print("Start regex extraction")
    pass


def xpath(page, site):
    print("Start XPath extraction")
    tree = html.fromstring(page)
    data = dict()

    if site == "rtv":
        data = dict(
            Author=tree.xpath('//*[@id="main-container"]//*[@class="article-meta"]//div[@class="author-name"]/text()')[0].strip(),
            PublishedTime=tree.xpath('//*[@id="main-container"]//*[@class="publish-meta"]/text()')[0].strip(),
            Title=tree.xpath('//*[@id="main-container"]//header/h1/text()')[0].strip(),
            SubTitle=tree.xpath('//*[@id="main-container"]//header/div[@class="subtitle"]/text()')[0].strip(),
            Lead=tree.xpath('//*[@id="main-container"]//header/p[@class="lead"]/text()')[0].strip(),
            Content="".join([p + "\n" for p in tree.xpath('//*[@id="main-container"]//div[@class="article-body"]//*[not(self::script)]/text()[normalize-space()]')])
        )
    elif site == "overstock":
        data = dict(
            Title='',
            ListPrice='',
            Price='',
            Saving='',
            SavingPercent='',
            Content=''
        )

    return json.dumps(data)


def main():
    method = sys.argv[1]
    algorithm = None

    if method == 'A':
        algorithm = regex
    elif method == 'B':
        algorithm = xpath
    elif method == 'C':
        print("Start Automatic Web extraction")
        pass

    data = []

    for page, site in pages.items():
        page_content = open(page, 'rb').read()
        data.append(algorithm(page_content, site))

    print("Extraction done")


if __name__ == "__main__":
    main()
