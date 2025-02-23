import pandas as pd
import ast


class Paper:
    def __init__(self, title, url, authors=None, homepage=None, year=None, content=None, symbol=None):
        if authors is None:
            authors = []
        if homepage is None:
            homepage = []
        if type(content) is not str:
            content = ''
        if type(symbol) is not str:
            symbol = ''
        self.title = title
        self.url = url
        self.authors = authors
        self.author_homepages = homepage
        self.year = year
        self.content = content
        self.symbol = symbol
    
    def set_content(self,content):
        self.content = content

    def set_symbol(self, symbol):
        self.symbol = symbol

def read_data(path):
    papers = []
    df = pd.read_csv(path)
    length = df.shape[1]
    for index, row in df.iterrows():
        title = row[0]
        url = row[1]
        str_author = row[2]
        str_home = row[3]
        year = row[4]
        content = ''
        symbol = ''
        if length > 5:
            content = row[5]
            symbol = row[6]
        author_list = ast.literal_eval(str_author)
        home_list = ast.literal_eval(str_home)
        papers.append(Paper(title, url, authors=author_list, homepage=home_list, year=year, content=content, symbol=symbol))
    return papers
