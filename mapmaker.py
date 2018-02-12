import pobjects
import random
import folium
from folium.plugins import MarkerCluster


def get_year():
    """
    Returns user input after checking it.
    :return year: integer, given year
    """
    try:
        year = int(input("Enter a year: "))
        assert 1889 < year <= 2024 or year in [1251,1478,1874,1888,2315,
        2551,4906,5514,7921,8341], "Wrong number. Yeat between 1890 and 2024 or\
         1251, 1478, 1874, 1888, 2315, 2551, 4906, 5514, 7921, 8341"
    except ValueError:
        print("Enter integers only. Try again.")
        return get_year()
    return year


def get_number_of_locations(year, all_locations):
    """
    Returns user input after checking it.
    :param year: ineger, year
    :param all_locations: integer, number of all locations
    :return number_of_locations: integer, given number of locations
    """
    try:
        print("Enter number of films to put location tags on map.", '\n' +
              "Max available: {}".format(all_locations))
        number_of_locations = int(input("(Number < 5000 recommended): "))
        assert 0 < number_of_locations <= all_locations, "Wrong number."
    except ValueError:
        print("Enter integers only. Try again.")
        return get__number_of_locations(year, all_locations)
    return number_of_locations


def get_map_data(year, loc_dict, years_dict):
    """
    Returns data needed for map creation for given year as a list.
    :param year: integer, year
    :param loc_dict: dictionary, keys - location strings, values - geo data
    :param years_dict: dictionary, keys - years, values - film dictionaries
    :return map_data: list of tuples as (film, location, coordinates)
    :return len(map_data): integer, number of all films available for given year
    """
    map_data = []
    t = years_dict[year]
    for film in t:
        processed = []
        for location in t[film]:
            if location in loc_dict:  # check if coordinates of locat. available
                if location in processed:
                    pass
                else:
                    l = loc_dict[location]
                    coordinates = [l[0]['geometry']['location']['lat'],
                                  l[0]['geometry']['location']['lng']]
                    map_data.append((film, location, coordinates))
                    processed.append(location)
            else:
                pass
    return map_data, len(map_data)


def choose_random_data(map_data, all_locations, n_locations):
    """
    Returns n randomly chosen unique locations.( n: n_locations)
    :param map_data:  list of tuples as (film, location, coordinates)
    :param all_locations: integer, number of all films available for given year
    :param n_locations: integer, number of films to return
    :return part_map_data: list of tuples as (film, location, coordinates)
    """
    if n_locations != all_locations:
        try:
            nums = list(random.sample(list(range(0,all_locations)), n_locations))
        except ValueError:
            print('Sample size exceeded population size.' + '\n' +
                  'Random generating failed.' + '\n' +
                  'Choosing first {} locations)'.format(n_locations))
            nums = range(0, n_locations)
    else:
        nums = range(0, all_locations)
    part_map_data = []
    for i in nums:
        part_map_data.append(map_data[i])
    return part_map_data


def create_map(map_data, all_locations, n_locations, year):
    """
    Returns a folium.map object and saves it as html file.
    Map includes tags of n films and locations for given year (n: n_locations),
    and heatmap layer based on all films filmed in given year.
    :param map_data: list of tuples such as (film, location, coordinates)
    :param all_locations: integer, number of all films available for given year
    :param n_locations: integer, number of films to show tags on map
    :param year: year to make the map for
    :return map_1: folium.map object, map with films
    """
    part_map_data = choose_random_data(map_data, all_locations, n_locations)
    locations = [map_data[i][2] for i in range(all_locations)]

    map_1 = folium.Map(part_map_data[0][2], zoom_start=12,
                                            tiles='cartodbdark_matter')
    locs_cluster = MarkerCluster(name='Location Tags').add_to(map_1)
    films_cluster = MarkerCluster(name='Film Tags').add_to(map_1)
    folium.plugins.HeatMap(locations, name='Coloured Heatmap',
                                            max_zoom=25).add_to(map_1)

    for i in range(n_locations):
        popup = folium.Popup(part_map_data[i][0], parse_html=True)
        folium.Marker(part_map_data[i][2],
         popup=popup,
         icon=folium.Icon(color='black'),
         ).add_to(films_cluster)

    for i in range(n_locations):
        popup = folium.Popup(part_map_data[i][1], parse_html=True)
        folium.Marker(part_map_data[i][2],
         popup=popup,
         icon=folium.Icon(color='green'),
         ).add_to(locs_cluster)

    #folium.plugins.Search().add_to(map_1)
    folium.plugins.MeasureControl().add_to(map_1)
    folium.plugins.Fullscreen().add_to(map_1)
    folium.LayerControl().add_to(map_1)

    file_name = 'maps\Filmsmap_' + str(year) + '_tags' + str(n_locations) + '.html'
    map_1.save(file_name)
    print("Map created successfully. Saved as: {}".format(file_name))
    print("Found locations: {}.".format(all_locations) + '\n' +
          "See Heatmap layer with all locations included.")
    print("Showing on map: {} tags of randomly chosen locations.".format(
                                                                   n_locations))
    return map_1


l_dict = pobjects.load_obj('loc_dict')
y_dict = pobjects.load_obj('years_dict')
map_year = get_year()
map_data, all_locations = get_map_data(map_year, l_dict, y_dict)
n_locations = get_number_of_locations(map_year, all_locations)

print("Processing...Please wait")
if n_locations > 3000:
    print("Relax and wait. Go take a coffee.")
if n_locations > 5000:
    print("How's your coffee?")

mapa = create_map(map_data, all_locations, n_locations, map_year)
