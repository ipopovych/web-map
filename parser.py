# Parses locations.list file, extracts data, finds locations coordinates
# Saves results as Python objects to files.
# Google Maps Geocoding API key required


from pobjects import save_obj as save
from pobjects import load_obj as load
from collections import defaultdict
import googlemaps


def parse_file(path):
    """
    Returns data from file as dictionary with years as keys.
    Made for locations.list IMDB file.
    :param path: string, name of the file to process
    :return years_dict: dict[year]:(dict[film]:[locations,])
    """
    with open(path, "r", encoding="utf-8", errors='ignore') as data:
        years_dict = defaultdict(dict)
        locations = set()

        for i in range(14):
            next(data)
        for line in data:
            s = line.find("(")+1
            e = line.find(")")
            location = line[line.find('\t') + 1:].strip()
            if "\t" in location:
                location = location[0:location.find('\t')]
            locations.add(location)
            try:
                key = int(line[s:e])
            except ValueError:
                try:
                    key = int(line[line.find('(', s+1)+1:line.find(')', e+1)])
                except ValueError:
                    pass

            if '"' in line:
                try:
                    years_dict[key][(line[1:line.find('"', line.find('"')+1)])].append(location)
                except KeyError:
                    years_dict[key][(line[1:line.find('"', line.find('"') + 1)])] = [location]
            else:
                try:
                    years_dict[key][(line[0:line.find('(')-1])].append(location)
                except KeyError:
                    years_dict[key][(line[0:line.find('(') - 1])] = [location]
    return years_dict, locations


def coordinates(location):
    """
    Returns geocode of given location using  Google Maps Geocoding API.
    :param location: string, name of location
    :return: list, google geocode of location

    >>> coordinates('Los Angeles, California, USA')
    [{'address_components': [{'long_name': 'Los Angeles', 'short_name':
    'Los Angeles', 'types': ['locality', 'political']}, {'long_name':
    'Los Angeles County', 'short_name': 'Los Angeles County', 'types':
    ['administrative_area_level_2', 'political']}, {'long_name': 'California',
    'short_name': 'CA', 'types': ['administrative_area_level_1', 'political']},
     {'long_name': 'United States', 'short_name': 'US', 'types': ['country',
     'political']}], 'formatted_address': 'Los Angeles, CA, USA', 'geometry':
     {'bounds': {'northeast': {'lat': 34.3373061, 'lng': -118.1552891},
     'southwest': {'lat': 33.7036519, 'lng': -118.6681759}}, 'location':
     {'lat': 34.0522342, 'lng': -118.2436849}, 'location_type': 'APPROXIMATE',
     'viewport': {'northeast': {'lat': 34.3373061, 'lng': -118.1552891},
     'southwest': {'lat':33.7036519, 'lng': -118.6681759}}}, 'place_id':
     'ChIJE9on3F3HwoAR9AhGJW_fL-I', 'types': ['locality', 'political']}]
    """
    return gmaps.geocode(location)


def loc_dict(locations):
    """
    Returns a dictionary with coordinates of given locations.
    :param locations: set of strings with locations
    :return loc_dict: dictionary, keys - location strings, values - geo data
    """
    loc_dict = {}
    for location in locations:
        a = coordinates(location)
        # Getting locations with geo coordinates only
        if a:
            loc_dict[location] = a
    return loc_dict


def update_loc_dict(new_file_name, file_name="loc_dict"):
    """
    Updates loc_dict with locations new file and saves it as python object.
    :param new_file_name: string, name of file with new data
    :param file_name: string, name of file to update, default "loc_dict"
    :return loc_dict: dictionary, keys - location strings, values - geo data
    """
    loc_dict = load(file_name)
    loc_dict_new = {}
    locations_new = parse_file(new_file_name)[1]
    for location in locations_new:
        if not (location in loc_dict):
            if location in loc_dict_new:
                pass
            else:
                try:
                    a = coordinates(location)
                    # Getting locations with geo coordinates only
                    if a:
                        loc_dict_new[location] = a
                except:
                    save(loc_dict_new, 'part_loc_dict')
                    print("Failed processing. \
                    Processed data saved as 'part_loc_dict.pkl'")
                    break
    loc_dict.update(loc_dict_new)
    save(loc_dict, "loc_dict")
    return loc_dict


def update_years_dict(new_file_name, file_name="years_dict"):
    """
    Updates years_dict with data from new file and saves it as python object.
    :param new_file_name: string, name of file with new data
    :param file_name: string, name of file to update, default "years_dict"
    :return years_dict: updated dictionary dict[year]:(dict[film]:[locations,])
    """
    years_dict_new = parse_file(new_file_name)[0]
    save(years_dict_new, file_name)
    return years_dict_new


#gmaps = googlemaps.Client(key='<your Google Maps Geocoding API key>')  # INSERT API KEY HERE!
#years_dict, locations = parse_file("locations.list")
#locations_dict = loc_dict(locations)
#save(years_dict,'years_dict')
#save(locations_dict, 'locations_dict')
