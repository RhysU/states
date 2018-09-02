#!/usr/bin/env python
import pathlib

import bs4
import pandas

source_path = pathlib.Path(__file__).parent
data_path = source_path / 'data'


def load_postal():
    df = pandas.read_csv(data_path / 'postal.csv')
    return df.set_index('State').Abbreviation.to_frame()


postal = load_postal()


# Data contains more then just states, hence merge as filtering step.
def load_gdp():
    df = pandas.read_csv(data_path / 'gdp.csv',
                          engine='python', skiprows=4, skipfooter=6)
    renaming = {'Area': 'State', '2017': 'GDP'}
    df = df[list(renaming.keys())]
    df = df.rename(columns=renaming)
    df = df.set_index('State')
    df = postal.merge(df, how='inner', left_index=True, right_index=True)
    df = df.GDP.to_frame()
    return df


gdp = load_gdp()


# Data contains more then just states, hence merge as filtering step.
def load_population():
    df = pandas.read_csv(data_path / 'population.csv')
    renaming = {'GEO.display-label': 'State', 'respop72017': 'Population'}
    df = df[list(renaming.keys())]
    df = df.rename(columns=renaming)
    df = df.set_index('State')
    df = postal.merge(df, how='inner', left_index=True, right_index=True)
    df = df.Population.astype(int).to_frame()
    return df


population = load_population()

# https://stackoverflow.com/questions/46242664
# https://stackoverflow.com/questions/32063985
def load_area():
    with (data_path / 'state-area.html').open('r') as f:
        soup = bs4.BeautifulSoup(f.read(), features="html.parser")

    table = soup.find('table')
    for div in soup.find_all("sup"):
        div.decompose()

    rows = []
    for row in table.findAll('tr'):
        cells = []
        for cell in row.findAll(["th","td"]):
            text = cell.text.replace(',', '')
            cells.append(text)
        rows.append(cells)

    df = pandas.DataFrame(rows)
    df = df.iloc[:, :2]
    df.columns = 'State', 'Area'
    df = df.set_index('State')
    df = postal.merge(df, how='inner', left_index=True, right_index=True)
    df = df.Area.astype(int).to_frame()
    return df

area = load_area()


def perform_merge():
    df = pandas.concat((postal, gdp, population, area), axis=1, sort=False)
    df.index.name = 'State'
    df = df.reset_index(drop=False)
    df = df.set_index('Abbreviation')
    df = df.sort_index()
    return df


merged = perform_merge()


def summarize(*abbreviations):
    abbreviations = list(sorted(set(abbreviations)))
    assert abbreviations
    df = merged
    df = df.query('index in @abbreviations')
    df = df.sum(axis=0)
    return df


def analyze(*abbreviation_groups):
    rows = []
    for abbreviations in abbreviation_groups:
        series = summarize(*abbreviations)
        rows.append(series.to_frame().T)
    df = pandas.concat(rows, axis=0)
    df['GDP per capita'] = df.GDP / df.Population
    df['GDP per area'] = df.GDP / df.Area
    return df
