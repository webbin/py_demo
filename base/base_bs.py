from bs4 import BeautifulSoup

Html_Parser = 'html.parser'


def get_bs_parse_result(text):
    bs = BeautifulSoup(text, Html_Parser)
    return bs