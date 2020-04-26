import sys
import json
from lxml import html


pages = {
    # "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html": "rtv",
    # "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljsÌe v razredu - RTVSLO.si.html": "rtv",
    # "../input-extraction/overstock.com/jewelry01.html": "overstock",
    # "../input-extraction/overstock.com/jewelry02.html": "overstock",
    "../input-extraction/bolha.com/Nogomet.html": "bolha",
    "../input-extraction/bolha.com/Macke.html": "bolha",
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
        data = []
        i = 1
        retries = 0
        while retries < 3:
            title = tree.xpath(f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/a//text()')
            if title:
                retries = 0
                data.append(dict(
                    Title=title[0].strip(),
                    ListPrice=tree.xpath(f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[1]/td[2]//text()[normalize-space()]')[0].strip(),
                    Price=tree.xpath(f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[2]/td[2]//text()[normalize-space()]')[0].strip(),
                    Saving=tree.xpath(f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[3]/td[2]/span//text()')[0].split()[0].strip(),
                    SavingPercent=tree.xpath(f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[3]/td[2]/span//text()')[0].split()[1].strip(),
                    Content="".join(tree.xpath(f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table/tbody/tr/td[2]//text()[normalize-space()]'))
                ))
            else:
                retries += 1
            i += 1
    elif site == "bolha":
        data = []
        titles = tree.xpath(f'//div[@class="content-main"]//ul/li/article//h3[@class="entity-title"]//text()')
        for i, title in enumerate(titles):
            data.append(dict(
                Title=title.strip(),
                Description=tree.xpath(f'//div[@class="content-main"]//ul/li/article//div[@class="entity-description-main"]//text()[normalize-space()]')[i].strip(),
                Price=tree.xpath(f'//div[@class="content-main"]//ul/li/article//div[@class="entity-prices"]//strong[@class="price price--hrk"]/text()[normalize-space()]')[i].strip() + " €",
                PublishedDate=tree.xpath(f'//div[@class="content-main"]//ul/li/article//div[@class="entity-pub-date"]/time/text()[normalize-space()]')[i].strip(),
                ImageUrl=tree.xpath(f'//div[@class="content-main"]//ul/li/article/div[@class="entity-thumbnail"]/a/img/@src')[i].strip(),
            ))

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
