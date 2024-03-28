from geopy.geocoders import Nominatim
geolocator = Nominatim(timeout = 20, user_agent = "JZ_Sreality")
latitude = 49.734061604
longitude = 18.615677485
location = geolocator.reverse([latitude, longitude])
print(location.address)