import sys
import json
import re
from lxml import html

pages = {
    "../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html": "rtv",
    "../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljsÌe v razredu - RTVSLO.si.html": "rtv",
    "../input-extraction/overstock.com/jewelry01.html": "overstock",
    "../input-extraction/overstock.com/jewelry02.html": "overstock",
    "../input-extraction/bolha.com/Nogomet.html": "bolha",
    "../input-extraction/bolha.com/Macke.html": "bolha",
}


def regex(page, site):
    def extract(text, reg):
        try:
            return re.search(reg, text).group(1)
        except AttributeError:
            return ""

    try:
        page = str(page, "utf-8")
    except (UnicodeDecodeError, AttributeError):
        try:
            page = str(page)
        except (UnicodeDecodeError, AttributeError):
            pass

    data = dict()
    if site == "rtv":
        data["Author"] = extract(page, "<div class=\"author-name\">([^<]*)</div>")
        data["PublishedTime"] = extract(page, "\s*(\d[^<]*)<br>")
        data["Title"] = extract(page, "<title>([^<]*)</title>")
        data["SubTitle"] = extract(page, "<div class=\"subtitle\">([^<]*)</div>")
        data["Lead"] = extract(page, "<p class=\"lead\">(.*)</p>")
        content = re.findall("<p[^>]*>([^<]*)</p>.*", page)
        data["Content"] = " ".join(content)
    elif site == "overstock":
        data = []
        titles = re.findall("PROD_ID[^>]*><b>([^<]*)</b></a><br>", page)
        list_price = re.findall("<b>List Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><s>([^<]*)</s></td></tr>",
                                page)
        price = re.findall(
            "<b>Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"bigred\"><b>([^<]*)</b></span></td></tr>",
            page)
        saving = re.findall(
            "<b>You Save:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"littleorange\">([^<]*)</span></td></tr>",
            page)
        content = re.findall("</td><td valign=\"top\"><span class=\"normal\">([^<]*)<br>", page)
        for i in range(len(titles)):
            data.append(dict(
                Title=titles[i],
                ListPrice=list_price[i],
                Price=price[i],
                Saving=saving[i].split(" ")[0],
                SavingPercent=saving[i].split(" ")[1],
                Content=content[i]
            ))
    elif site == "bolha":
        data = []
        titles = re.findall("<h3 class=\"entity-title\"><a[^>]*>([^<]*)</a></h3>(?=.*Zadnji oglasi)", page,
                            re.MULTILINE | re.DOTALL)
        desc = re.findall("<div class=\"entity-description-main\">\n*\s*([^<]*)<br>", page)
        price = re.findall("<strong class=\"price price--hrk\">[^\w]*([^<]*)", page)
        date = re.findall("<time class=\"date[^>]*>([^<]*)</time>", page)
        img = re.findall("<img class=\"img entity-thumbnail-img.*\ssrc=\"([^\"]*)\"", page)
        #print(price)
        for i in range(len(titles)):
            data.append(dict(
                Title=titles[i],
                Description=desc[i],
                Price=price[i].replace("&nbsp;", ""),
                PublishedDate=date[i],
                ImageUrl=img[i]
            ))
    return json.dumps(data)


def xpath(page, site):
    tree = html.fromstring(page)
    data = dict()

    if site == "rtv":
        data = dict(
            Author=tree.xpath('//*[@id="main-container"]//*[@class="article-meta"]//div[@class="author-name"]/text()')[0].strip(),
            PublishedTime=tree.xpath('//*[@id="main-container"]//*[@class="publish-meta"]/text()')[0].strip(),
            Title=tree.xpath('//*[@id="main-container"]//header/h1/text()')[0].strip(),
            SubTitle=tree.xpath('//*[@id="main-container"]//header/div[@class="subtitle"]/text()')[0].strip(),
            Lead=tree.xpath('//*[@id="main-container"]//header/p[@class="lead"]/text()')[0].strip(),
            Content="".join([p + "\n" for p in tree.xpath(
                '//*[@id="main-container"]//div[@class="article-body"]//*[not(self::script)]/text()[normalize-space()]')])
        )
    elif site == "overstock":
        data = []
        i = 1
        retries = 0
        while retries < 3:
            title = tree.xpath(
                f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/a//text()')
            if title:
                retries = 0
                data.append(dict(
                    Title=title[0].strip(),
                    ListPrice=tree.xpath(
                        f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[1]/td[2]//text()[normalize-space()]')[0].strip(),
                    Price=tree.xpath(
                        f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[2]/td[2]//text()[normalize-space()]')[0].strip(),
                    Saving=tree.xpath(
                        f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[3]/td[2]/span//text()')[0].split()[0].strip(),
                    SavingPercent=tree.xpath(
                        f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table//table//tr[3]/td[2]/span//text()')[0].split()[1].strip(),
                    Content="".join(tree.xpath(
                        f'//table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor][{i}]/td[2]/table/tbody/tr/td[2]//text()[normalize-space()]'))
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
                Description=tree.xpath(
                    f'//div[@class="content-main"]//ul/li/article//div[@class="entity-description-main"]//text()[normalize-space()]')[i].strip(),
                Price=tree.xpath(
                    f'//div[@class="content-main"]//ul/li/article//div[@class="entity-prices"]//strong[@class="price price--hrk"]/text()[normalize-space()]')[i].strip() + " €",
                PublishedDate=tree.xpath(
                    f'//div[@class="content-main"]//ul/li/article//div[@class="entity-pub-date"]/time/text()[normalize-space()]')[i].strip(),
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
        pass

    data = []

    for page, site in pages.items():
        page_content = open(page, 'rb').read()
        res = algorithm(page_content, site)
        print(res)
        data.append(res)


if __name__ == "__main__":
    main()
