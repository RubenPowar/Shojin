import pandas as pd
import csv, requests, os
from dotenv import load_dotenv


# def get_coordinates(postcode):
#     file = "/Users/ruben/PycharmProjects/Shojin/files/CC1/Sources/ukpostcodes.csv"
#     # declare files to read
#
#     conversions = pd.read_csv(file, index_col=0)
#
#     # convert + extract coordinates from file's postcode
#     conversions['Combined'] = conversions['latitude'].astype(str) + ',' + conversions['longitude'].astype(str)
#     latitude = conversions.loc[conversions['postcode'] == postcode]['latitude'].iloc[0]
#     longitude = conversions.loc[conversions['postcode'] == postcode]['longitude'].iloc[0]
#     # coordinates = str(latitude) + ',' + str(longitude)
#     coordinates = [latitude, longitude]
#     return coordinates

def get_coordinates(postcode, postcode_file="/Users/ruben/PycharmProjects/Shojin/files/CC1/Sources/ukpostcodes.csv"):
    """
    Retrieves the coordinates for a given postcode from a CSV file.
    """
    try:
        data = pd.read_csv(postcode_file, index_col=0)
        latitude = data.loc[data['postcode'] == postcode, 'latitude'].iloc[0]
        longitude = data.loc[data['postcode'] == postcode, 'longitude'].iloc[0]
        return [latitude, longitude]
    except FileNotFoundError:
        print("CSV file not found.")
        return None
    except IndexError:
        print("Postcode not found in the file.")
        return None


def generate_maps_images(postcode, title, filepath, gmaps_key):
    # Enter your api key here
    # api_key = "AIzaSyAUdmgR91R-qPfxS42g0UcExPZ9DadlFtw"
    # url variable store url
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    filepath = filepath + "MapsPNGs/"
    coordinates = get_coordinates(postcode)
    # coordinates = str(coordinates_lst[0]) + ',' + str(coordinates_lst[1])


    # zoom list defines the zoom level of each savefile
    zoom_levels = 10, 12, 14, 16
    filenames = []
    # get method of requests module return response object
    for level in zoom_levels:
        full_url = f"{url}&zoom={level}&scale=2&size=1280x1280&key={gmaps_key}&markers=icon:http://tinyurl.com/shojin40|{','.join(map(str, coordinates))}"
        response = requests.get(full_url)
        # wb mode is stand for write binary mode
        # filenames.append(filepath + title + '-' + str(level) + '-image.png')
        # f = open(filepath + title + '-' + str(level) + '-image.png', 'wb')
        # # r.content gives content, in this case gives image
        # f.write(response.content)
        # # close method of file object save and close the file
        # f.close()
        if response.status_code == 200:
            filename = os.path.join(filepath, f"{title}-{level}-image.png")
            with open(filename, 'wb') as file:
                file.write(response.content)
            filenames.append(filename)
        else:
            print(f"Failed to download map for zoom level {level}.")

    return filenames



if __name__ == "__main__":
    folder_path = "/Users/ruben/PycharmProjects/Shojin/files/MapsInfo/MapsPNGs/"
    filename = '/Users/ruben/PycharmProjects/Shojin/files/CC1/Sources/TestXLS.xlsx'
    load_dotenv()
    gmaps_api_key = os.getenv('GMAPS_API_KEY')
    ws = pd.read_excel(filename, header=None)
    test_postcode = ws.loc[8, 1]
    test_title = ws.loc[1, 1]

    if not all([gmaps_api_key, folder_path, filename]):
        print("Environment variables missing.")
    else:
        generate_maps_images(test_postcode, test_title, folder_path, gmaps_api_key)



# http://tinyurl.com/45fwy5hz links to:
# https://6508127.fs1.hubspotusercontent-na1.net/hub/6508127/hubfs/Shojin%20-%20logo%20round%20small.png?width=40&height=40