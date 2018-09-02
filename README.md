In discussions of California politics or its economy, frequently someone tosses
out a statement about California being effectively a seriously-sized country in
its own right.  Undoubtedly true stuff.  Shows up repeatedly in articles like
https://www.weforum.org/agenda/2016/07/american-state-bigger-economy-than-india/.

Those statements always feel, to me, like implicit comparisons to other US
states.  So, simple slice-and-dice of very basic facts about the states using
2017 numbers so one can make explicit comparisons:

    $ ipython --no-banner

    In [1]: %run data.py

    In [2]: # Biggest states by square miles

    In [3]: area.sort_values(by='Area').tail(5)
    Out[3]:
                  Area
    State
    New Mexico  121590
    Montana     147040
    California  163695
    Texas       268596
    Alaska      665384

    In [4]: # Biggest states by population

    In [5]: population.sort_values(by='Population').tail(5)
    Out[5]:
                  Population
    State
    Pennsylvania    12805537
    New York        19849399
    Florida         20984400
    Texas           28304596
    California      39536653

    In [6]: # What's California look like vs the Tri State?

    In [7]: analyze(['CA'], ['CT', 'NY', 'NJ'])
    Out[7]:
                               State      GDP Population    Area GDP per capita GDP per area
    0                     California  2746873   39536653  163695      0.0694766      16.7804
    0  ConnecticutNew JerseyNew York  2399686   32443227   68821      0.0739657      34.8685

    In [8]: # Throwing in Pennsylvania to bring up the population?

    In [9]: analyze(['CA'], ['CT', 'NY', 'NJ'], ['CT', 'NY', 'NJ', 'PA'])
    Out[9]:
                                           State      GDP Population    Area GDP per capita GDP per area
    0                                 California  2746873   39536653  163695      0.0694766      16.7804
    0              ConnecticutNew JerseyNew York  2399686   32443227   68821      0.0739657      34.8685
    0  ConnecticutNew JerseyNew YorkPennsylvania  3151757   45248764  114875       0.069654      27.4364

Pennsylvania could be replaced with Massachusetts/Rhode Island.  Or you could
include states heading down towards Washington.  Or you could start drawing
random samples of states constrained to be +/- X million people then see if
California somehow looks like an outlier.  Etc.

Anyhow, to conclude, California's a big economy.  But it's not (at least
superficially) outsized relative to other parts of the United States
that contain similar populations.
