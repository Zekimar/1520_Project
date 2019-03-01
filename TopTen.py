import pandas as pd

url = 'https://www.imdb.com/chart/boxoffice/'


# this function return an array of strings contains  current top ten movies in theatre. It parse the website specified
# in the url variable above.
def movies():
    dfs = pd.read_html(url)
    m = []
    for name in dfs[0]['Title']:
        m.append(name)
    return m


if __name__ == '__main__':
    for x in movies():
        print(x)
