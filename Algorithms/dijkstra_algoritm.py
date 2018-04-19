from classes import stations as st

class linked_list():
    def __init__(self, path):
        self.path = path # misschien moeten we de route struct hiervoor gebruiken
        self.next_node = None
        self.time = self.path.time # di werkt alleen als we de route struct hiervoor gebruiken

def create_distance_list(station_list):
    for index1 in range(len(station_list) - 1):
        for index2 in range(index1 + 1, len(station_list):

        # dijksta algoritme
        # kijk naar hamilton cycles in vollendige grafen en doe hier slimme dingen mee.

def dijkstra(station_list, begin_station, end_station):
    for neighbor in station_list[begin_station]:

        node = linked_list(placeholder) # vervangen met path
        node.next_node = root.next_node #hoe doe ik dit?
        root.next_node = node #werkt dit?







    # bepaalt met dijkstra algoritme een lijst van afstanden tussen kritieke stations
    # schrijf een greedy

    # dit is allemaal onzin denk ik, beter is: doe dit gewoon voor alle punten naar alle punten
    # 
