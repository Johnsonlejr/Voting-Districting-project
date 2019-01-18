# Le Johnson
# mathProject.py

import sys
import copy
import random
import csv
from precinct import *
from district import *

# FILE: The file that has the information about the district, other than the
#   seed.
# NUM_WALK: The number of walks computed by the program
# CHECK_RATE: The interval that the districting is check for validity
# NUM_DISTRICTS: The amount of districts in the districting
# SPLIT_TYPE: The method of splitting up the document read from, by comma (",")
#   or by tab ("\t")
# LOWER_BOUND: The smallest percentage of current population that a district
#   can have before becoming invalid
# UPPER_BOUND: The largest percentage of current population that a district
#   can have before becoming invalid
# GOAL: The number of valid districtings required 
# OPPORTUNITY_THRESHOLD: The percentage of the total population that determines
#   if there are enough members of a minority for a district to be an
#   opporunity district

FILE = "Seguin_Blocks4.csv"
NUM_WALK = 10
CHECK_RATE = 5
NUM_DISTRICTS = 8
SPLIT_TYPE = ","
LOWER_BOUND = 0.9
UPPER_BOUND = 1.1
GOAL = 5000
OPPORTUNITY_THRESHOLD = 50

# district_arr: The array of districts objects in the districting
# previous: An array that records the last valid districting
# write_num: The number of times written to the write_file
# reader_file: The file with the seed.
# writer_file: The file written to.

district_arr = []
previous = []
write_num = 0
reader_file = None
writer_file = None

def random_walk(arr):
    
    global district_arr

    # Declaring two counters, one for the amount of flips are made and how many
    # valid districtings are found.

    flip_count = 0
    valid_districts = 0

    while valid_districts != GOAL:

        save_precincts(arr)

        for y in range(CHECK_RATE):

            # Assigns a random precinct from the precinct array to a variable
            # and the district that it's in to variables

            changer = arr[random.randint(0, len(arr) - 1)]  # Picks random Precinct from array
            current_district = district_arr[int(changer.get_district()) - 1] #Retrieves

            # Finds the neighbor array of integers of the changing precinct, picks a random
            # precinct from among them, searches for the precinct object from
            # the integer representation, and if the the two precincts share
            # the same districtm, repeats the process.

            if current_district.get_num_precincts() > 1:
                temp_arr = changer.get_neighbors()

                criteria = random.choice(temp_arr)

                precinct = None
                for place in arr:
                    if place.get_precinct() == int(criteria):
                        precinct = place

                count = 0
                while (precinct.get_district() == changer.get_district() and count
                    < 10):
                    criteria = random.choice(temp_arr)

                    precinct = None
                    for place in arr:
                        if place.get_precinct() == int(criteria):
                            precinct = place
                    count += 1

                # Changes the district of the the chosen precinct and adds and
                # removes the precinct from the two districts.

                changer.set_district(precinct.get_district())

                (district_arr[precinct.get_district() - 1].switch 
                    (current_district, changer))

                flip_count += 1

        # Determines the averages for the district and the precinct, and then
        # if the current districting is valid. If valid, finds the amount of
        # opportunity districts and writes the districting to the CSV. If not
        # valid, resets the districting to the last valid districting.

        total = 0
        for precinct in arr:
            total += precinct.get_population()

        district_avg = total / NUM_DISTRICTS
        precinct_avg = total / len(arr)
        
        if not districting_is_valid(district_arr, district_avg):
            reset_precincts(arr)
            flip_count -= CHECK_RATE
        else:
            valid_districts += 1
            write(arr)

def save_precincts(precinct_arr):

    # Empties the previous array, and adds the district of each precinct to the
    # array, in order.

    global previous
    previous = []
    for precinct in precinct_arr:
        previous.append(precinct.get_district())
    
    
def reset_precincts(precinct_arr):

    # Deletes all of the precincts in each district, and then reverts all of
    # the precincts to their last saved valid districting
    global previous
    count = 0

    
    for district in district_arr:
        district.reset_precincts()

    for num in previous:
        precinct_arr[count].set_district(num)
        district_arr[num - 1].append(precinct_arr[count])
        count += 1

            
def districting_is_valid(district_list, avg):
    
    return (districting_is_connected(district_list) and 
    districting_population_is_valid(district_list, avg))

def districting_population_is_valid(district_list, avg):

    result = True
    for district in district_list:
        if not district.calculate_population_is_avg(avg):
                result = False
    return result

def districting_is_connected(district_list):

    result = True
    for district in district_list:
        if not district.is_connected():
                result = False
    return result


def read():
    
    arr = []

    csvfile = open(FILE)
    csvfile.readline()

    # Opens the CSV and retrives the information needed to create a precinct
    # object. When using a different CSV from the last one may have to update
    # the code if the information has shifted in the CSV.

    for line in csvfile:
        neighbor_arr = []
        temp = line.split(SPLIT_TYPE)
        geo_id = temp[0]
        total_pop = int(temp[4])
        black = int(temp[5]) + int(temp[7])
        hispanic = int(temp[6])
        white = total_pop - int(temp[5]) - hispanic
        neighbor_arr = temp[-1].rsplit()

        temp_precinct = Precinct(geo_id, total_pop, white,
            black, neighbor_arr, hispanic, 0) 
        arr.append(temp_precinct)


    return arr

def write(arr):

    # Opens a CSV for reading and initializes an iterator for the CSV and an
    # "all" array to store the lines in. Adds the first line in the CSV to the array.

    global write_num
    global reader_file
    global writer_file
    all = []

    black_count = 0
    hispanic_count = 0
    for district in district_arr:
        if district.is_opportunity_district("black", OPPORTUNITY_THRESHOLD):
            black_count += 1
        elif district.is_opportunity_district("hispanic", OPPORTUNITY_THRESHOLD):
            hispanic_count += 1

    if write_num == 0:
        writer_file.write("GEO ID,Seed, ,Districtings")
        for item in arr:
            writer_file.write("\n" + str(item.get_precinct()) + ","
                + str(item.get_district()) + ", ")
        writer_file.write("\n \nBlack Opportunity Districts:,")
        writer_file.write(str(black_count) + ", ")
        writer_file.write("\nHispanic Opportunity Districts:,")
        writer_file.write(str(hispanic_count) + ", ")
        write_num += 1
        writer_file.seek(0)
    else:
        count = 0
        writer_file.seek(0)
        reader = csv.reader(writer_file)
        for item in reader:
            if item[0].isnumeric() and count < len(arr):
                district = str(arr[count].get_district())
                item.append(district)
                count += 1
            all.append(item)

        all[-2].append(str(black_count))
        all[-1].append(str(hispanic_count))

        writer_file.seek(0)
        writer = csv.writer(writer_file, lineterminator='\n')
        writer.writerows(all)
        write_num += 1
        print(write_num)
    print("written!")

    # If the item in the first cell of each line is a fully numeric string
    # (Generally searching for the GEO ID), then get the district that the
    # precinct is currently in and append it to the end of the line, then add
    # it to the "all" array.


    # Opens the file for writing, deleting the file, and completely rewrites
    # the CSV file. There is probably a better and more efficient way to write
    # this.

def main():
    
    if len(sys.argv) != 3:
        print("\nUsage: python main_code.py 'File that contains the"
        " districting seed' 'File to write the results to'\n")

        print("\nWarning: The second file entered will be deleted and written"
        " over. Make sure it is an empty file!\n")
        sys.exit(1)

    global reader_file
    global writer_file
    reader_file = open(sys.argv[1])
    writer_file = open(sys.argv[2], "w+")

    # Creates the amount of districts specified by the NUM_DISTRICTS variable.

    for x in range(NUM_DISTRICTS):
        district_arr.append(District(x + 1))

    # Opens the file specified by the user in the command line argument, and if
    # the first cell of the line is numeric (Expecting the GEO_ID of the
    # precinct to be here), save the district value to an array.

    district = []
    csvfile = open(sys.argv[1])
    csvfile.readline()
    for line in csvfile:
        line = line.split(",")
        if line[0].isnumeric():
            district.append(line[2].rstrip())


    # Creates the precinct array and gives this list to the district objects.

    precinct_arr = read()
    district_arr[0].set_full_list(precinct_arr)

    # Iterates through the precinct array and assigns each object a district
    # value from the array where the values were stored.

    total = 0
    count = 0


    for precinct in precinct_arr:
        precinct.set_district(district[count])
        district_arr[int(district[count]) - 1].append(precinct)
        count += 1

    # Calculates the total popuation, the average population for each district
    # and then shows the user if the districting is valid.

    for precinct in precinct_arr:
        total += precinct.get_population()
    avg = total / NUM_DISTRICTS
    

    write(precinct_arr)

    reader_file.close()
    writer_file.close()
main()
