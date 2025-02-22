import pandas as pd
import ast


class Paper:
    def __init__(self, title, url, authors=None, homepage=None, year=None):
        if authors is None:
            authors = []
        if homepage is None:
            homepage = []
        self.title = title
        self.url = url
        self.authors = authors
        self.author_homepages = homepage
        self.year = year


def read_data(path):
    papers = []
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        title = row[0]
        url = row[1]
        str_author = row[2]
        str_home = row[3]
        year = row[4]
        author_list = ast.literal_eval(str_author)
        home_list = ast.literal_eval(str_home)
        papers.append(Paper(title, url, authors=author_list, homepage=home_list, year=year))
    return papers
