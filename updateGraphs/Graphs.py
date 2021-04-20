def graph():
    from bokeh.plotting import figure, show, output_file, ColumnDataSource, reset_output, save
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.models import FactorRange
    import pandas as pd
    import numpy as np

    pd.options.mode.chained_assignment = None
    df=pd.read_csv('updateMap/output.csv')
    df.rename( columns={'Unnamed: 0':'index'}, inplace=True )
    df.columns = [c.replace(' ', '_') for c in df.columns]

    #Cases over population by country (percentage of population that got covid)

    sortedpop_df = df.sort_values(by=['Population'], inplace=False)
    sortedpop_df.dropna(subset=['Population'], inplace=True)
    sortedpop_df

    print('Graph done')


    TOOLTIPS = [
        ('Country: ', "@Country"),
        ('Population: ', '@Population{($ 0.00 a)}')

    ]

    p = figure(title="Population By Country", width=1200, height=3000, y_range=sortedpop_df.Country, tooltips=TOOLTIPS)
    p.hbar(y="Country", right='Population', height=0.8, width=0.3, source=df)

    reset_output()
    output_file("./dataGraphs/templates/dataGraphs/Population.html")
    save(p)

    #Total cases by country
    sortedtcases_df = df[['Country', 'Total_Cases']]
    sortedtcases_df = sortedtcases_df.sort_values(by=['Total_Cases'], inplace=False)
    sortedtcases_df
    world_total = sum(sortedtcases_df.Total_Cases)
    sortedtcases_df['Percentage'] = sortedtcases_df.apply(lambda row: (row.Total_Cases/world_total), axis = 1)

    TOOLTIPS = [
        ('Country: ', "@Country"),
        ('Total Cases: ', '@Total_Cases{($ 0.00 a)}'),
        ('Percentage of World Cases: ', '@Percentage{(0.00 a %)}')
    ]

    tc = figure(title="Total Cases By Country", width=1200, height=3000, y_range=sortedtcases_df.Country, tooltips=TOOLTIPS)
    tc.hbar(y="Country", right='Total_Cases', height=0.8, width=0.3, source=sortedtcases_df)

    reset_output()
    output_file("./dataGraphs/templates/dataGraphs/TotalCases.html")
    save(tc)

    #Total deaths over total cases by country (mortality)
    sortedm_df = df[['Country','Total_Deaths', 'Total_Cases']]
    sortedm_df['Mortality_Rate'] = sortedm_df.apply(lambda row: row.Total_Deaths/row.Total_Cases, axis = 1)

    sortedm_df = sortedm_df.sort_values(by=['Mortality_Rate'], inplace=False)


    TOOLTIPS = [
        ('Country: ', "@Country"),
        ('Mortality Rate: ', '@Mortality_Rate{(0.00 a %)}')
    ]

    m = figure(title="Mortality by Country", width=1200, height=3000, y_range=sortedm_df.Country, tooltips=TOOLTIPS)
    m.hbar(y="Country", right='Mortality_Rate', height=0.8, width=0.3, source=sortedm_df)

    reset_output()
    output_file("./dataGraphs/templates/dataGraphs/Mortality.html")
    save(m)

    #Total deaths over total deaths + total recovered
    sortedmc_df = df[['Country','Total_Deaths', 'Total_Cases', 'Total_Recovered']]
    sortedmc_df['Total_Recovered'] = sortedmc_df['Total_Recovered'].replace(0, np.nan).dropna(axis=0, how='any').astype(float)
    sortedmc_df.dropna(subset=['Total_Recovered'], inplace=True)
    sortedmc_df['Mortality_Closed'] = sortedmc_df.apply(lambda row: row.Total_Deaths/(row.Total_Deaths + row.Total_Recovered), axis = 1)

    sortedmc_df = sortedmc_df.sort_values(by=['Mortality_Closed'], inplace=False)


    TOOLTIPS = [
        ('Country: ', "@Country"),
        ('Mortality Rate: ', '@Mortality_Closed{(0.00 a %)}')
    ]

    mc = figure(title="Mortality by Closed Cases by Country", width=1200, height=3000, y_range=sortedmc_df.Country, tooltips=TOOLTIPS)
    mc.hbar(y="Country", right='Mortality_Closed', height=0.8, width=0.3, source=sortedmc_df)

    reset_output()
    output_file("./dataGraphs/templates/dataGraphs/MortalityClosed.html")
    save(mc)

    with open('./dataGraphs/templates/dataGraphs/Population.html', 'r+') as original: graph_file = original.read()
    if "{% extends 'graphTabs.html' %}\n{% block tabs %}\n" and "\n{% endblock %}" not in graph_file:
        with open('./dataGraphs/templates/dataGraphs/Population.html', 'w') as modified: modified.write("{% extends 'graphTabs.html' %}\n{% block tabs %}\n" + graph_file + "\n{% endblock tabs %}")

    with open('./dataGraphs/templates/dataGraphs/TotalCases.html', 'r+') as original: graph_file = original.read()
    if "{% extends 'graphTabs.html' %}\n{% block tabs %}\n" and "\n{% endblock %}" not in graph_file:
        with open('./dataGraphs/templates/dataGraphs/TotalCases.html', 'w') as modified: modified.write("{% extends 'graphTabs.html' %}\n{% block tabs %}\n" + graph_file + "\n{% endblock tabs %}")

    with open('./dataGraphs/templates/dataGraphs/Mortality.html', 'r+') as original: graph_file = original.read()
    if "{% extends 'graphTabs.html' %}\n{% block tabs %}\n" and "\n{% endblock %}" not in graph_file:
        with open('./dataGraphs/templates/dataGraphs/Mortality.html', 'w') as modified: modified.write("{% extends 'graphTabs.html' %}\n{% block tabs %}\n" + graph_file + "\n{% endblock tabs %}")

    with open('./dataGraphs/templates/dataGraphs/MortalityClosed.html', 'r+') as original: graph_file = original.read()
    if "{% extends 'graphTabs.html' %}\n{% block tabs %}\n" and "\n{% endblock %}" not in graph_file:
        with open('./dataGraphs/templates/dataGraphs/MortalityClosed.html', 'w') as modified: modified.write("{% extends 'graphTabs.html' %}\n{% block tabs %}\n" + graph_file + "\n{% endblock tabs %}")
