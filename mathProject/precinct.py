# Precinct.py

class Precinct:

    # Initializer of the precinct object.

    # Precinct - name of the precinct. The assumption is that the GEO_ID for the
    #   precinct is used here, however other values can be used.
    # Population - the population of the precinct
    # White - The total number of Caucasian people in the precinct.
    # Black - The total number of African-American people in the precinct.
    # Hispanic - The total number of Hispanic people in the precinct.
    # Neighbors - an array of integers containing the GEO_IDs of the surrounding
    #   precincts.
    # District - The district that the precinct is in. The default is 0, or
    # being in no district.

    def __init__(self, precinct, population, white, black, \
        neighbors, hispanic, district = 0):
        self.__neighbor_arr = []
        self.__precinct = int(precinct)
        self.__population = int(population)
        self.__white = int(white)
        self.__black = int(black)
        self.__hispanic = hispanic
        for x in neighbors:
            self.__neighbor_arr.append(x)
        self.__district = int(district)
    
    def set_precinct(self, precinct):
        self.__precinct = precinct

    def get_precinct(self):
        return self.__precinct

    def set_district(self, district):
        self.__district = district

    def get_district(self):
        return int(self.__district)

    def set_population(self, population):
        self.__population = population

    def get_population(self):
        return self.__population

    def set_white(self, white):
        self.__white = white

    def get_white(self):
        return self.__white

    def set_black(self, black):
        self.__black = black

    def get_black(self):
        return self.__black

    def set_hispanic(self, hispanic):
        self.__hispanic = hispanic

    def get_hispanic(self):
        return self.__hispanic
        
    def set_neighbors(self, *neighbors):
        del neighbor_arr[:]
        for x in neighbors:
            neighbor_arr.append(x)

    def get_neighbors(self):
        return self.__neighbor_arr

    def add_neighbor(self, neighbor):
            neighbor_arr.append(neighbor)

    def delete_neighbor(self, neighbor):
        neighbor_arr.remove(neighbor)

    # 'equal to' and 'less than' methods are here for ordering purposes.

    def __eq__(self, other):
        return self.__precinct == other

    def __lt__(self, other):
        return self.get_precinct() < other.get_precinct()
        
    def __str__(self):
        return str(self.__precinct) + ", "
