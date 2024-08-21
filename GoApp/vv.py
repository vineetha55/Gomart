import requests

def get_location_from_eircode(eircode):
    url = f"https://nominatim.openstreetmap.org/search?q={eircode}&format=json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}  # Replace 'YourApp/1.0' with your own user agent string
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("hii")
        data = response.json()
        print(data)
        if data:
            print("hello")
            # Extracting latitude and longitude from the response
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            return None, None
    else:
        print("Error:", response.status_code)
        return None, None

# Example usage
eircode = 'D02 AF30'  # Replace with the desired Eircode
latitude, longitude = get_location_from_eircode(eircode)
if latitude and longitude:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Location not found or error occurred")


import requests

def get_address_from_coordinates(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    headers = {'User-Agent': 'YourApp/1.0'}  # Replace 'YourApp/1.0' with your own user agent string
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'display_name' in data:
            address = data['display_name']
            return address
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None

# Example usage
latitude = 53.349805
longitude = -6.26031
address = get_address_from_coordinates(latitude, longitude)
if address:
    print("Address:", address)
else:
    print("Address not found or error occurred")




