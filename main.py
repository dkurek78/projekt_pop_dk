import requests
from bs4 import BeautifulSoup
from tkinter import *
import tkintermapview



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

root = Tk()
root.geometry("1400x800")
root.title("System zarządzania siecią telewizyjną")

# Mapa (na górze)
map_widget = tkintermapview.TkinterMapView(root, width=1400, height=400, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

# Lista (na dole)
listbox = Listbox(root, width=80)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()