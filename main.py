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
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f"{self.name} ({self.category})")

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


root = Tk()
root.geometry("1400x800")
root.title("System zarządzania siecią telewizyjną")


map_widget = tkintermapview.TkinterMapView(root, width=1400, height=400, corner_radius=5)
map_widget.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)


Label(root, text="Typ obiektu:").grid(row=0, column=0, sticky=W)
type_options = ["Sieć", "Pracownik", "Widz"]
selected_type = StringVar(value=type_options[0])
type_menu = OptionMenu(root, selected_type, *type_options)
type_menu.grid(row=0, column=1, sticky=W)


Label(root, text="Nazwa / Imię:").grid(row=1, column=0, sticky=W)
entry_name = Entry(root, width=30)
entry_name.grid(row=1, column=1, sticky=W)

Label(root, text="Miejscowość:").grid(row=2, column=0, sticky=W)
entry_location = Entry(root, width=30)
entry_location.grid(row=2, column=1, sticky=W)

Label(root, text="Sieć (dla widza/pracownika):").grid(row=3, column=0, sticky=W)
entry_extra = Entry(root, width=30)
entry_extra.grid(row=3, column=1, sticky=W)

entities = []

def add_entity():
    name = entry_name.get()
    location = entry_location.get()
    category = selected_type.get()
    extra = entry_extra.get() if category in ["Pracownik", "Widz"] else None

    entity = NetworkTV(name, location, category, extra)
    entities.append(entity)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_extra.delete(0, END)
    entry_name.focus()

    show_entities()


def show_entities():
    listbox.delete(0, END)
    for idx, entity in enumerate(entities):
        display = f"{idx + 1}. {entity.name} ({entity.location})"
        if entity.category == "Widz" and entity.extra:
            display += f" → {entity.extra}"
        listbox.insert(END, display)


def remove_entity():
    try:
        i = listbox.curselection()[0]
        entities[i].marker.delete()
        entities.pop(i)
        show_entities()
    except IndexError:
        pass



def edit_entity():
    try:
        i = listbox.curselection()[0]
        entity = entities[i]

        selected_type.set(entity.category)  # ← DODAJ TO

        entry_name.delete(0, END)
        entry_name.insert(0, entity.name)
        entry_location.delete(0, END)
        entry_location.insert(0, entity.location)
        entry_extra.delete(0, END)
        if entity.extra:
            entry_extra.insert(0, entity.extra)

        button_add.config(text="Zapisz", command=lambda: update_entity(i))
    except IndexError:
        pass




def update_entity(i):
    name = entry_name.get()
    location = entry_location.get()
    category = selected_type.get()
    extra = entry_extra.get() if category in ["Pracownik", "Widz"] else None

    entities[i].marker.delete()  # stary marker znika

    new_entity = NetworkTV(name, location, category, extra)
    entities[i] = new_entity  # podmiana obiektu

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_extra.delete(0, END)
    entry_name.focus()

    button_add.config(text="Dodaj", command=add_entity)

    show_entities()  # ← to powoduje odświeżenie listy — musi być TU!




button_add = Button(root, text="Dodaj", command=add_entity)
button_add.grid(row=1, column=2, padx=10)

button_remove = Button(root, text="Usuń", command=remove_entity)
button_remove.grid(row=2, column=2, padx=10)

button_edit = Button(root, text="Edytuj", command=edit_entity)
button_edit.grid(row=3, column=2, padx=10)




listbox = Listbox(root, width=80)
listbox.grid(row=5, column=0, columnspan=3, pady=10)





root.mainloop()