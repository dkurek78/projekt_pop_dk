import requests
from bs4 import BeautifulSoup



class NetworkTV:
    def __init__(self, name, location, category, extra=None):
        self.name = name
        self.location = location
        self.category = category
        self.extra = extra
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]



networks = []
employees = []
viewers = []



def get_current_list(category):
    if category == "Sieć":
        return networks
    elif category == "Pracownik":
        return employees
    elif category == "Widz":
        return viewers
    return None



def add_entity(name, location, category, extra=None):
    entity = NetworkTV(name, location, category, extra)
    get_current_list(category).append(entity)

def delete_entity(category, index):
    lst = get_current_list(category)
    if 0 <= index < len(lst):
        lst.pop(index)

def update_entity(category, index, name, location, extra=None):
    lst = get_current_list(category)
    if 0 <= index < len(lst):
        lst[index] = NetworkTV(name, location, category, extra)

def list_entities(category):
    lst = get_current_list(category)
    for i, entity in enumerate(lst, start=1):
        info = f"{i}. {entity.name} ({entity.location})"
        if entity.category == "Widz" and entity.extra:
            info += f" → {entity.extra}"
        print(info)