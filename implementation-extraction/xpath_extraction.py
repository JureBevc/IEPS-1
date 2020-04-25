import json
from lxml import html


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
            Content="".join(tree.xpath('//*[@id="main-container"]//div[@class="article-body"]//text()')),
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
