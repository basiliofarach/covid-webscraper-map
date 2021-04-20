# Create a webscrapping program using jupyter to get information about covid 19 cases - Done
# Make a python file to create an output.csv - Done
# With the output create an html file for the map, and then create a javascript or django file to render it
# Create a server to run after the process is completed, or during the process start
# Create formulas to analyze the obtained data

def map():
    import folium
    import pandas as pd
    import numpy as np
    import updateMap.webscraper

    pd.options.mode.chained_assignment = None
    map = folium.Map(location=[14.06,-87.40], zoom_start=2)

    fgc=folium.FeatureGroup(name="Total Covid Cases")
    fgp=folium.FeatureGroup(name="Population")
    fgm=folium.FeatureGroup(name="Mortality By Total Cases")
    fgmc=folium.FeatureGroup(name="Mortality By Closed Cases")

    data=pd.read_csv("updateMap/output.csv")
    data.rename( columns={'Unnamed: 0':'Index'}, inplace=True )
    data.to_html("covidMap/templates/covidMap/data.html", index=False, classes='container highlight striped')
    data.columns = [c.replace(' ', '_') for c in data.columns]


    with open('./covidMap/templates/covidMap/data.html', 'r+') as original: data_file = original.read()
    with open('./covidMap/templates/covidMap/data.html', 'w') as modified: modified.write("{% extends 'header.html' %}\n{% block body %}\n" + data_file + "\n{% endblock %}")


    base_url='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    country_borders = f'{base_url}/world-countries.json'
    print(country_borders)

    #In this section it's gonna be added modified dataframes and formulas to use in the Choropleths, this is made to leave the original data unmodified
    sortedm_df = data[['Country','Total_Deaths', 'Total_Cases']]
    sortedm_df['Mortality_Rate'] = sortedm_df.apply(lambda row: row.Total_Deaths/row.Total_Cases, axis = 1)

    sortedmc_df = data[['Country','Total_Deaths', 'Total_Cases', 'Total_Recovered']]
    sortedmc_df['Total_Recovered'] = sortedmc_df['Total_Recovered'].replace(0, np.nan).dropna(axis=0, how='any').astype(float)
    sortedmc_df.dropna(subset=['Total_Recovered'], inplace=True)
    sortedmc_df['Mortality_Closed'] = sortedmc_df.apply(lambda row: row.Total_Deaths/(row.Total_Deaths + row.Total_Recovered), axis = 1)

    # Set the Choropleths
    fgc = folium.Choropleth(
            geo_data=country_borders,
            name='COVID-19',
            data=data,
            columns=['Country', 'Total_Cases'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            nan_fill_color='white',
            overlay=False,
            highlight=True,
            legend_name="Total Cases",
            tiles='stamenwatercolor'
        )

    fgp = folium.Choropleth(
            geo_data=country_borders,
            name='Population',
            data=data,
            columns=['Country', 'Population'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            nan_fill_color='white',
            overlay=False,
            highlight=True,
            legend_name="Population",
            tiles='stamenwatercolor'
        )

    fgm = folium.Choropleth(
            geo_data=country_borders,
            name='Mortality',
            data=sortedm_df,
            columns=['Country', 'Mortality_Rate'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            nan_fill_color='white',
            overlay=False,
            highlight=True,
            legend_name="Mortality",
            tiles='stamenwatercolor'
        )

    fgmc = folium.Choropleth(
            geo_data=country_borders,
            name='Mortality by Closed',
            data=sortedmc_df,
            columns=['Country', 'Mortality_Closed'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            nan_fill_color='white',
            overlay=False,
            highlight=True,
            legend_name="Mortality by Closed",
            tiles='stamenwatercolor'
        )


    #This sections defines the hover
    style_font = "font-size: 13px; font-weight: bold"

    fgc.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_font, labels=False))

    fgp.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_font, labels=False))

    fgm.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_font, labels=False))

    fgmc.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_font, labels=False))

    """fgp.geojson.add_child(
        folium.features.GeoJson(
            data,
            style_function=style_font,
            control=False,
            highlight_function=highlight_function,
            tooltip=folium.features.GeoJsonTooltip(fields=['Country','Population'],
                    aliases=['Country','Population'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                    sticky=True
                )
        )
    )"""

    map.add_child(fgc)
    map.add_child(fgp)
    map.add_child(fgm)
    map.add_child(fgmc)
    map.add_child(folium.LayerControl())
    map.save("./covidMap/templates/covidMap/Map1.html")

    with open('./covidMap/templates/covidMap/Map1.html', 'r+') as original: map_file = original.read()
    if "{% extends 'header.html' %}\n{% block body %}\n" not in map_file:
        with open('./covidMap/templates/covidMap/Map1.html', 'w') as modified: modified.write("{% extends 'header.html' %}\n{% block body %}\n" + map_file + "\n{% endblock %}")
