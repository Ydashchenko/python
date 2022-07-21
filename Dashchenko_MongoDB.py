from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt
import requests

cluster = MongoClient("mongodb+srv://madjonga123:AS@cluster0.xumzj.mongodb.net/PTC002?retryWrites=true&w=majority")
db = cluster['PTC002']
collection = db['users']

API_KEY = 'a675b50f5ea049ba999bdd984c55be19'

# 1
def add_user():
    name = input('Введите имя: ')
    interests = (input('Введите интересы: ')).split(", ")
    address = input('Введите адрес: ')
    params = {
        'key': API_KEY,
        'q': address
    }
    base_url = 'https://api.opencagedata.com/geocode/v1/json'
    response = requests.get(base_url, params=params).json()
    location = {
        'latitude': response['results'][0]['geometry']['lat'],
        'longitude': response['results'][0]['geometry']['lng'],
        'address': response['results'][0]['components']['town']
    }

    post = {
        'name': name,
        'interests': interests,
        'location': location
    }

    print('Отлично, пользователь добавлен в базу!')
    return collection.insert_one(post)

# 2 
def the_closest():

    def distance(target_lat, target_lon, nearest_lat, nearest_lon):
     
        # The math module contains a function named
        # radians which converts from degrees to radians.
        target_lat = radians(target_lat)
        target_lon = radians(target_lon)
        nearest_lat = radians(nearest_lat)
        nearest_lon = radians(nearest_lon)
  
      
        # Haversine formula
        dlat = nearest_lat - target_lat
        dlon = nearest_lon - target_lon
        a = sin(dlat / 2)**2 + cos(target_lat) * cos(nearest_lat) * sin(dlon / 2)**2
 
        c = 2 * asin(sqrt(a))
    
        # Radius of earth in meters
        r = 6372795
      
        # calculate the result in meters
        the_distance_itself = int(c * r)
        return the_distance_itself
     
    wanted_address = input('Введите желаемый адрес: ')
    params = {
        'key': API_KEY,
        'q': wanted_address
    }
    base_url = 'https://api.opencagedata.com/geocode/v1/json'
    response = requests.get(base_url, params=params).json()

    distances = []
    
    users = list(collection.find())
    for c in collection.find():
        distances.append(distance(response['results'][0]['geometry']['lat'], response['results'][0]['geometry']['lng'], c['location']['latitude'], c['location']['longitude']))
    index_of_nearest_point = distances.index(min(distances))
    nearest_point = users[index_of_nearest_point]
    nearest_user_lat = users[index_of_nearest_point]['location']['latitude']
    nearest_user_lng = users[index_of_nearest_point]['location']['longitude']
    nearest_user_lat_lng = str(nearest_user_lat) + '+' + str(nearest_user_lng)
    params = {
        'key': API_KEY,
        'q': nearest_user_lat_lng
    }
    response2 = requests.get(base_url, params=params).json()
    final_address = str(response2['results'][0]['components']['road']) + ', ' + str(response2['results'][0]['components']['house_number'])
    finale = 'Ближайший к вам человек:\n' + str(nearest_point['name']) + ', ' + final_address + '. Интересы: ' + str(", ".join(nearest_point['interests'])) + '.'
    return finale

# Main Code
if __name__ == '__main__':
    choice = ''
    while choice != '3':
        choice = input("Для добавления нового пользователя введите '1'. Для поиска ближайшего пользователя к указанному адресу введите '2'. Для выхода введите '3': ")
        if choice == '1':
            add_user()
        if choice == '2':
            print(the_closest())






