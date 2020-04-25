import sys

regex = __import__("implementation-extraction.regex_extraction").regex_extraction.regex
xpath = __import__("implementation-extraction.xpath_extraction").xpath_extraction.xpath

pages = {
    "input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html": "RTV",
    "input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljsÌe v razredu - RTVSLO.si.html": "RTV",
    "input-extraction/overstock.com/jewelry01.html": "overstock",
    "input-extraction/overstock.com/jewelry02.html": "overstock",
}


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
        page_content = open(page, 'r').read()
        data.append(algorithm(page_content, site))

    print("Extraction done")


if __name__ == "__main__":
    main()
