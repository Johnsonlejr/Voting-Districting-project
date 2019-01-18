# district.py

import precinct

class District:

    full_list = []

    def __init__(self, name, precinct_list = None, avg_population = 0):             # creating a district object
        self.__name = name                                                          # assigning the district's name and list of precincts contained within the district
        self.__precinct_list = precinct_list
        if precinct_list is None:                                                   # if the district contains no precincts, setting all of the district's
            self.__precinct_list = []                                               # attributes to zero
            self.__total_population = 0
            self.__total_black = 0
            self.__total_white = 0
            self.__total_hispanic = 0
            self.__percent_black = 0
            self.__percent_white = 0
            self.__percent_hispanic = 0
            self.__is_average = False
            self.__is_black_opportunity_district = False
            self.__is_white_opportunity_district = False
            self.__is_hispanic_opportunity_district = False
            self.__candidate = 'undetermined'
        else:                                                                       # else go through each precinct in the district and get its information to build the
            for precinct in self.__precinct_list:                                   # information of the district
                self.__total_population += precinct.get_population()                # finding the total population of the district
                self.__total_black += precinct.get_black()                          # finding the black population of the district
                self.__total_white += precinct.get_white()                          # finding the white population of the district
                self.__total_hispanic += precinct.get_hispanic()                    # finding the hispanic population of the district
                self.calculate_percentages()                                        # calculating the percentage of each race/ethnicity in the district
                if avg_population > 0:                                              # making sure the population is positive to avoid division by zero
                    self.calculate_population_is_avg(avg_population)                # finding whether the population is within 10% of the avg
                self.calculate_candidate()                                          # finding the district's city council candidate assuming worst-case RPV

    def get_name(self):                                                             # accessor method for the district's name
        return self.__name

    def get_precincts(self):                                                        # accessor method for the list of precincts within the district
        return self.__precinct_list

    def reset_precincts(self):
        self.__precinct_list = []
        self.__total_population = 0
        self.__total_black = 0
        self.__total_white = 0
        self.__total_hispanic = 0
        self.__percent_black = 0
        self.__percent_white = 0
        self.__percent_hispanic = 0

    def get_total_population(self):                                                 # accessor method for the population of the district
        return self.__total_population

    def get_total_white(self):                                                      # accessor method for the white population of the district
        return self.__total_white
    
    def get_total_black(self):                                                      # accessor method for the black population of the district
        return self.__total_black

    def get_total_hispanic(self):                                                   # accessor method for the hispanic population of the district
        return self.__total_hispanic

    def get_num_precincts(self):
        return len(self.__precinct_list)

    def get_percentages(self):
        return ([self.__percent_black, self.__percent_white,
        self.__percent_hispanic])

    def set_full_list(self, list):                                                  # mutator method for the list of all precincts, including ones outside of this district
        global full_list
        full_list = list

    def get_full_list(self):                                                        # accessor method for the list of all precincts, including ones outside of this district
        global full_list
        return full_list

    def append(self, precinct):                                                     # method to add a precinct to the district
        self.__precinct_list.append(precinct)                                       # appending the precinct to the district's list of precincts 
        self.__total_population += precinct.get_population()                        # updating the district's total population
        self.__total_black += precinct.get_black()                                  # updating the district's black population
        self.__total_white += precinct.get_white()                                  # updating the district's white population
        self.__total_hispanic += precinct.get_hispanic()                            # updating the district's hispanic population
        self.calculate_percentages()                                                # recalculating the percentages of each race/ethnicity

    def remove(self, precinct):                                                     # method to remove a precinct from the district
        self.__precinct_list.remove(precinct)                                       # removing the precinct from the district's list of precincts
        self.__total_population -= precinct.get_population()                        # updating the district's total population
        self.__total_black -= precinct.get_black()                                  # updating the district's black population
        self.__total_white -= precinct.get_white()                                  # updating the district's white population
        self.__total_hispanic -= precinct.get_hispanic()                            # updating the district's hispanic population
        self.calculate_percentages()                                                # recalculating the percentages of each race/ethnicity

    def calculate_percentages(self):                                                            # calculating the percentages of each race/ethnicity
        if self.__total_population > 0:                                                         # checking that the population is positive to avoid division by zero
            self.__percent_black = self.__total_black / self.__total_population * 100           # calculating the percentage of black residents out of the total population
            self.__percent_white = self.__total_white / self.__total_population * 100           # calculating the percentage of white residents out of the total population
            self.__percent_hispanic = self.__total_hispanic / self.__total_population * 100     # calculating the percentage of hispanic residents out of the total population
            return self.__percent_black, self.__percent_white, self.__percent_hispanic          # returning the percentages of each race/ethnicity
    
    def calculate_population_is_avg(self, avg_population):                                      # calculating whether the population of the district is within 10% of the average population
        lower_bound = avg_population * 0.9                                                      # setting a lower bound equal to 90 percent of the population
        upper_bound = avg_population * 1.1                                                      # setting an upper bound equal to 110 percent of the population
        if lower_bound < self.__total_population < upper_bound:                                 # if the district's population is within 10% of the population
            self.__is_avg = True                                                                # setting the is_avg variable to True
        else:
            self.__is_avg = False                                                               # else, setting is_avg to False
        return self.__is_avg                                                                    # return the boolean is_avg

    def calculate_candidate(self):                                                              # finding the candidate assuming worst-case RPV
        if self.__percent_black < self.__percent_white > \
            self.__percent_hispanic:                                                            # if the white population is greater than the black and hispanic populations, setting the candidate to white
            self.__candidate = 'white'
        elif self.__percent_white < self.__percent_black  >\
        self.__percent_hispanic:                                                                # if the black population is greater than the white and hispanic populations, setting the candidate to black
            self.__candidate = 'black'
        elif self.__percent_black < self.__percent_hispanic >\
        self.__percent_white:                                                                   # if the hispanic population is greater than the white and black populations, setting the candidate to hispanic
            self.__candidate = 'hispanic'
        else:                                                                                   # else if there is not a population which is greater than the others, the candidate cannot be determined
            self.__candidate = 'undetermined'
        return self.__candidate                                                                 # returning the race/ethnicity of the candidate

    def is_connected(self):                                                                     # method determining whether the district is connected/continuous
        precinct_a = self.__precinct_list[0]                                                    # naming the first precinct in the district's precinct list Precinct A
        connected_to_a = []                                                                     # creating a list that will contain precincts connected to Precinct A
        connected_to_a.append(precinct_a)                                                       # adding Precinct A to the list of precincts connected to A (Precinct A is always connected to itself)
        for precinct in connected_to_a:                                                         # for each precinct listed as being connected to Precinct A
            for neighbor in precinct.get_neighbors():                                           # get its neighbors, and for each neighbor,
                for place in full_list:
                    if place.get_precinct() == int(neighbor):
                        temp = place
                if (temp.get_district() == precinct.get_district()                          # if the neighbor is in the same district as the precinct
                    and temp not in connected_to_a):                                         # and the neighbor is not already in the list of precincts connected to A
                        connected_to_a.append(temp)                                         # add the neighbor to the list of precincts that are connected to Precinct A
        for item in self.in_one_list(self.__precinct_list, connected_to_a):
            print(item)
        return len(self.__precinct_list) == len(connected_to_a)                                 # compare the number of precincts in the district to the number of precincts that are
                                                                                                # connected to Precinct A and return True if they are equal
    def in_one_list(self, list1, list2):
        list3 = [value for value in list1 if value not in list2]
        return list3

    def switch(self, district, precinct):                                                       # method to flip a precinct from one district to another
        district.remove(precinct)                                                               # removing the precinct from its original district
        self.append(precinct)                                                                   # adding the precinct to this district (the precinct's "new" district)

    def create_one_step_away(self, precinct_list):                                              # method that creates a district one step away/flips one precinct
        border_list = []                                                                        # creating a list that will contain all precincts on the border of the district
        for precinct in precinct_list:                                                          # for each precinct in the district,
            for neighbor in precinct.get_neighbors:                                             # get its neighbors, and for each neighbor,
                if (neighbor.get_district() != precinct.get_district()                          # if the neighbor is outside this district
                    and precinct not in border_list):                                            # and the precinct is not already in the list of bordering precincts
                        border_list.append(precinct)                                            # add the precinct to the list of precincts on the border of the district
        random_index_precinct = random.randint(0, len(border_list) - 1)                         # choosing a random index from the list of the bordering precincts
        random_precinct = border_list[random_index]                                             # getting the border precinct at the random index
        neighbors = random_precinct.get_neighbors()                                             # getting the neighbors of the random border precinct
        random_index_neighbor = random.randint(0, len(neighbors) - 1)                           # getting a random index from the list of neighbors
        random_neighbor = neighbors[random_index_neighbor]                                      # getting the random neighbor at that index
        while random_neighbor.get_district() == random_precinct.get_district():                 # while the random neighbor is in the same district as the random precinct
            random_index_neighbor = random.randint(0, len(neighbors) - 1)                       # reassigning the random index from the neighbor list
            random_neighbor = neighbors[random_index_neighbor]                                  # reassigning the random neighbor
        self.switch(random_neighbor.get_district(), random_neighbor)                            # flipping the random neighbor precinct

    def is_opportunity_district(self, minority, max_percentage):                                   # method to determine whether a district is an opportunity district
            if minority == "black"  and self.__percent_black > max_percentage:                                           # compare the black population to the given threshold, if it is greater than the threshold,
                return True
            elif (minority == "hispanic" and self.__percent_hispanic >
                max_percentage):                                                                    # compare the black population to the given threshold, if it is greater than the threshold,
                return True
            elif minority == "white" and self.__percent_white > max_percentage:                                           # compare the black population to the given threshold, if it is greater than the threshold,
                return True

            return False
        

    def __str__(self):                                                                          # string conversion method for a district
        string = ""                                                                             # formatting the district's information
        string += str(self.__name) + ": "

        self.__precinct_list.sort()

        for precinct in range(len(self.__precinct_list) - 2):
            string += (str(self.__precinct_list
                [precinct].get_precinct()) + ", ")

        string += str(self.__precinct_list[-1].get_precinct())

        return string
