# Create a webscrapping program using jupyter to get information about covid 19 cases - Done
# Make a python file to create an output.csv - Done
# With the output create an html file for the map, and then create a javascript or django file to render it
# Create a server to run after the process is completed, or during the process start
# Create formulas to analyze the obtained data

def map():
    import folium
    import pandas as pd
    import geopandas as gpd
    import updateMap.webscraper
    from branca.colormap import linear


    map = folium.Map(location=[14.06,-87.40], zoom_start=2)

    fgc=folium.FeatureGroup(name="Total Covid Cases")
    fgp=folium.FeatureGroup(name="Population By Color")
    
    folium.TileLayer('cartodbpositron').add_to(map)

    data=pd.read_csv("updateMap/output.csv")
    data_json = gpd.GeoDataFrame(data)
    total_cases=list(data["Total Cases"])
    population=list(data["Population"])

    base_url='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    country_borders = f'{base_url}/world-countries.json'
    print(country_borders)


    fgc = folium.Choropleth(
            geo_data=country_borders,
            name='COVID-19',
            data=data,
            columns=['Country', 'Total Cases'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            nan_fill_color='white'
        )

    fgp = folium.Choropleth(
            geo_data=country_borders,
            name='Population',
            data=data,
            columns=['Country', 'Population'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            nan_fill_color='white'
        )


    map.add_child(fgc)
    map.add_child(fgp)
    map.add_child(folium.LayerControl())
    map.save("./Covid_Map/templates/Covid_Map/Map1.html")
