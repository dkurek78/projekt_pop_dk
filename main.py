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

def list_entities(category):
    lst = get_current_list(category)
    for i, network_tv in enumerate(lst, start=1):
        info = f"{i}. {network_tv.name} ({network_tv.location})"
        if network_tv.category == "Widz" and network_tv.extra:
            info += f" → {network_tv.extra}"
        print(info)
