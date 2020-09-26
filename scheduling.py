'''
    A Scheduling Assistant
    
    An activity scheduling assistant is built for YMCA Camp Thunderbird,
    a branch of the YMCA of Greater Charlotte, to assist lead staff
    with scheduling cabin activities due to highly volitile procedural
    guidlines and expected on the fly changes which might become necessary
    due to COVID-19.
    
    Copyright (C) 2020 Shepherd Sims
    
    MIT License
'''
import random
import xlrd
import xlwt
import sys
## Availible locations around camp which are availible for use during land activities
                    
LOCATIONS = {"Archery":1,
             "Arts and Crafts":1,
             "Baseball":1,
             "Loop":1,
             "Duke":1,
             "Baseball Field":1,
             "Basketball Court":2,
             "Challenge Course":1,
             "Rec Hall":1,
             "Rec Hall Porch":1,
             "Ampitheatre":1,
             "Fishing":1,
             "Flagpole Field":1,
             "Chapel Point Field":1,
             "GA Field 1":1,
             "GA Field 2":1,
             "GA Field 3":1,
             "Golf Field 1":1,
             "OLS":1,
             "Riflery":1,
             "Tennis":1,
             "Volleyball":1,
             "Tree Climbing":1,
             "Gaga":1,
             "Disc Golf":2,
             "Putt Putt":1,
             "Pottery":0,
             "Dodgeball":1,
             "Digital Media":1}

## Activity class definition
class Activity:
    def __init__(self, name, location):
        self.name = name
        self.location = location

## Define Open Activities and their respective locations

ACTIVITIES = {"Archery":"Archery",
              "Arts and Crafts":"Arts and Crafts",
              "Athletic Conditioning":"Loop",
              "BYG":"Duke",
              "Basketball":["Basketball Court","Duke"],
              "Baseball":"Baseball",
              "Challenge Course":"Challenge Course",
              "Drama":["Rec Hall Porch", "Ampitheatre"],
              "Dance":["Rec Hall Porch", "Ampitheatre"],
              "Digital Media":"Digital Media",
              "Cheer":["Rec Hall Porch", "Ampitheatre"],
              "Fishing":"Fishing",
              "Soccer":["GA Field 1","GA Field 2", "GA Field 3"],
              "Softball":"Baseball",
              "Flag Football":["GA Field 1","GA Field 2", "GA Field 3"],
              "Ultimate":["GA Field 1","GA Field 2", "GA Field 3", "Chapel Point Field", "Golf Field"],
              "Lacrosse":["GA Field 1","GA Field 2", "GA Field 3"],
              "OLS":"OLS",
              "Riflery": "Riflery",
              "Tennis":"Tennis",
              "Volleyball":"Volleyball",
              "Tree Climbing":"Tree Climbing",
              "Gaga":"Gaga",
              "Disc Golf":"Disc Golf",
              "Putt Putt":"Putt Putt",
              "Pottery":"Pottery",
              "Geocaching":"OLS",
              "Dodgeball":"Dodgeball"}


## Camp class to be used in seperating and dealing with older vs younger camps
class Camp:
    def __init__(self, name, cabin_list, age_type:bool):
        self.cabin_list = cabin_list
        self.name = name
        self.type = age_type

    def get_picks(self, cabin_picks):
        for cabin in self.cabin_list:
            cabin.Picks(cabin_picks[cabin.number])

## Cabin class which stores the number of campers, their activity preferences,
class Cabin:
    def __init__(self, number, n):
        self.number = number
        self.n = n
        self.picks = None
        self.Activities = {"A-Day":{"Period One":None,
                                 "Period Two":None,
                                 "Period Three":None},
                           "B-Day":{"Period One":None,
                                 "Period Two":None,
                                 "Period Three":None}}

    def Picks(self, picks):
        self.picks = picks
        return self.picks

    
class Schedule:
    def __init__(self, activity_list = ACTIVITIES, locations = LOCATIONS):
        self.activity_list = activity_list
        self.open_locations = [{},{},{},{},{},{}]
        random_selections = {}
        for key in LOCATIONS:
            for period in self.open_locations:
                period[key] = LOCATIONS[key]
            self.open_locations
        self.schedule = {}
        self.picks = {}

    def create(self, name, cabins):
        self.name = name
        for cabin in cabins:
            self.schedule[cabin] = cabin.Activities

        for cabin in cabins:
            self.picks[cabin] = cabin.picks

    def get_top_choice(self, cabin):
        if len(cabin.picks) !=0:
            top = max(cabin.picks, key=cabin.picks.get)
            return (top)
        else:
            top = random.sample(list(ACTIVITIES),1)[0]
            return top
            
    
    def get_cabin_schedule(self, cabin):
        return self.schedule

    def assign(self, cabin, activity, location, last_location_to_try = True):
        
    ## Try to assign choice location to cabin during any time slot
##        try:
        for activity_period in range(6):

            ## Uncomment for scheulidd walk-through
##          print("Cabin",cabin.number,"Try activity",activity, "at",location, "during", activity_period, "with current:", self.schedule[cabin]["A-Day"],self.schedule[cabin]["B-Day"])
            
            ## If there is an open locaiton for this activity during a cabin's unassigned activity period, assign activity here and decrease the location's openings by 1 for that period
            if self.open_locations[activity_period][location] != 0:
                if activity_period == 0 and self.schedule[cabin]["A-Day"]["Period One"] == None and not activity == "Pottery":
                    self.schedule[cabin]["A-Day"]["Period One"] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.picks:
                        cabin.picks.pop(activity)
                    return True
                elif activity_period == 1 and self.schedule[cabin]["A-Day"]["Period Two"] == None:
                    self.schedule[cabin]["A-Day"]["Period Two"] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.picks:
                        cabin.picks.pop(activity)
                    return True
                elif activity_period == 2 and self.schedule[cabin]["A-Day"]["Period Three"] == None:
                    self.schedule[cabin]["A-Day"]["Period Three"] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.picks:
                        cabin.picks.pop(activity)
                    return True

                ## Include limitation on Putt Putt since day camp uses that location in the afternoons except friday
                elif activity_period == 3 and self.schedule[cabin]["B-Day"]["Period One"] == None and not activity == "Putt Putt":
                    self.schedule[cabin]["B-Day"]["Period One"] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.picks:
                        cabin.picks.pop(activity)
                    return True
                elif activity_period == 4 and self.schedule[cabin]["B-Day"]["Period Two"] == None and not activity == "Putt Putt":
                    self.schedule[cabin]["B-Day"]["Period Two"] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.picks:
                        cabin.picks.pop(activity)
                    return True
                elif activity_period == 5 and self.schedule[cabin]["B-Day"]["Period Three"] == None and not activity == "Putt Putt":
                    self.schedule[cabin]["B-Day"]["Period Three"] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.picks:
                        cabin.picks.pop(activity)
                    return True

            ## If you have tried to put the cabin's top activity into the schedule but there were no slots, raise their next top activity's preference score and try again
                #if activity_period == 5:
                    #print("Cabin",cabin.number,"Activity:",activity, "at",location, "during", activity_period, "with current:", self.schedule[cabin]["A-Day"],self.schedule[cabin]["B-Day"])
            if activity_period == 5 and last_location_to_try == True:
                if activity in cabin.picks:
                    increase_next_choice = cabin.picks.pop(activity)/2

                # Uncomment to see which cabin's got picks boosted because their top chioces were already taken
                # print("Cabin:",cabin.number, "gets",self.get_top_choice(cabin),"boosted by",increase_next_choice)
                
                new_activity = self.get_top_choice(cabin)
                if new_activity in cabin.picks:
                    cabin.picks[new_activity]+=increase_next_choice
                else:       
                    cabin.picks[random.sample(list(ACTIVITIES),1)[0]] = 10
                return False

    '''
    Try assigning an activity for each location that the cabin's top choice can be done at
    '''
    def assign_activity(self, cabin):
        # Get a cabin's top choice for activity and its location
        choice = self.get_top_choice(cabin)
        choice_location = ACTIVITIES[choice]

        # Check if an activity has been assigned to cabin during this iteration
        assigned = False

        # If the chosen activity can be done at multiple locations, try each opening is found or none are availible
        if type(choice_location) == list:
            for l in choice_location:

                # Mark if this location is the last availible 
                if l == choice_location[len(choice_location)-1]:
                    last_location_to_try = True
                else:
                    last_location_to_try = False
                    
                # Assign and check if the assignment finished, if so - break out of loop, if not - try again
                assigned = self.assign(cabin, choice, l, last_location_to_try)
                if assigned == True:
                    break
        else:
            assigned = self.assign(cabin, choice, choice_location)
        if assigned == False:
            self.assign_activity(cabin)
                        
    '''
    Draft one activity for each cabin, prioritizing cabins who agree that all the campers want a specific activity
    '''
    def draft(self):
        
        ## Create a dictionary of each cabin's top activity choice
        best = {}
        for cabin in self.schedule:
            if self.get_top_choice(cabin) in cabin.picks:
                best[cabin] = cabin.picks[self.get_top_choice(cabin)]
            else:
                best[cabin] = 10

        ## Sort the cabins into order which prioritizes cabins who all agree on a top activity
        best = sorted(best.items(), key = lambda x: x[1], reverse = True)

        ## Assign each cabin one activity
        for cabin in best:
            self.assign_activity(cabin[0])

    '''
    Display a list of all open locations during each activity period
    '''
    def open_activities(self):
        open_activities = {"A":[],"B":[]}
        for period in range(len(self.open_locations)):
            if period < 3:
                day = "A"
            else:
                day = "B"
            temp = {}
            for a in self.open_locations[period]:
                if self.open_locations[period][a] > 0:
                    temp[a] = self.open_locations[period][a]
            open_activities[day].append(temp)
        return open_activities

    def print_open_activities(self):
        activities = self.open_activities()
        for day in activities:
            print(day, "Day")
            count = 0
            for period in activities[day]:
                count+=1
                print("Period:",count,period)
        
            
def schedule(camp, name):
    s = Schedule()
    s.create(name, camp.cabin_list)
##    except:
##        print("Something else went wrong")
    return s

def printSchedule(schedule):
    for item in schedule.schedule:
        print("\nCabin",item.number, ":")
        for a in schedule.schedule[item]:
            print(schedule.schedule[item][a])

def assignCamps(younger, older):
    for cabin in younger:
        Younger.cabin_list.append(cabin)
    for cabin in older:
        Older.cabin_list.append(cabin)   

 ##Initialize cabins at camp
One = Cabin("One", 1)
Two = Cabin("Two", 2)
Three = Cabin("Three",3)
Four = Cabin("Four",4)
Five = Cabin("Five",5)
Six = Cabin("Six",6)
Seven = Cabin("Seven",7)
Eight = Cabin("Eight",8)
Nine = Cabin("Nine",9)
Ten = Cabin("Ten",10)
Eleven = Cabin("Eleven",11)
Twelve = Cabin("Twelve",12)
Thirteen = Cabin("Thirteen",13)
Fourteen = Cabin("Fourteen",14)
Fifteen = Cabin("Fifteen",15)
Sixteen = Cabin("Sixteen",16)
T1 = Cabin("T1",41)
T2 = Cabin("T2",42)
Seventeen = Cabin("Seventeen",17)
Eighteen = Cabin("Eighteen",18)
Nineteen = Cabin("Nineteen",19)
Twenty = Cabin("Twenty",20)
Twentyone = Cabin("Twentyone",21)
Twentytwo = Cabin("Twentytwo",22)
Twentythree = Cabin("Twentythree",23)
Twentyfour = Cabin("Twentyfour",24)
Twentyfive = Cabin("Twentyfive",25)
Twentysix = Cabin("Twentysix", 26)
Twentyseven = Cabin("Twentyseven", 27)
Twentyeight = Cabin("Twentyeight", 28)
Twentynine = Cabin("Twentynine",29)
Thirty = Cabin("Thirty",30)
Thirtyone = Cabin("Thirtyone",31)
Thirtytwo = Cabin("Thirtytwo",32)
Thirtythree = Cabin("Thirtythree",33)
Thirtyfour = Cabin("Thirtyfour",34)
Thirtyfive = Cabin("Thirtyfive",35)

workbook = xlrd.open_workbook('Land Activity Preferences.xlsx')
worksheet = workbook.sheet_by_index(0)

def get_Picks(worksheet):
    cabins = {}
    for row in range(worksheet.nrows):
        number = worksheet.cell_value(row, 0)
        if row > 0:
            cabins[number] = {}
            for col in range(worksheet.ncols):
                if col > 0:
                    if worksheet.cell_value(row, col) != xlrd.empty_cell.value:
                        cabins[number][worksheet.cell_value(0, col)] = int(worksheet.cell_value(row, col))
    return cabins
    
cabin_picks = get_Picks(worksheet)


mystyle = xlwt.easyxf('pattern: pattern solid, fore_colour blue')

def export_Picks(schedule, filename):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(schedule.name)
    if schedule.name == "Older Camp Schedule": 
        ws.write(0,1, "A-Day")
        ws.write(1,1, "9:15-10:15")
        ws.write(1,2, "10:15-11:15")
        ws.write(1,3, "11:15-12:15")
        ws.write(0,4, "B-Day")
        ws.write(1,4, "9:15-10:15")
        ws.write(1,5, "10:15-11:15")
        ws.write(1,6, "11:15-12:15")
    else:
        ws.write(0,1, "A-Day")
        ws.write(1,1, "3:00-4:00")
        ws.write(1,2, "4:00-5:00")
        ws.write(1,3, "5:00-6:00")
        ws.write(0,4, "B-Day")
        ws.write(1,4, "3:00-4:00")
        ws.write(1,5, "4:00-5:00")
        ws.write(1,6, "5:00-6:00")
    c = 2
    for item in schedule.schedule:
        ws.write(c, 0, item.number)
        i = 0
        for day in schedule.schedule[item]:
            j = 1
            for a in schedule.schedule[item][day]:
                if i == 0:
                    ws.write(c, j, schedule.schedule[item][day][a])
                else:
                    ws.write(c, j+3, schedule.schedule[item][day][a])
                j+=1
            i+=1
        c+=1
    wb.save(filename)
    
## Create Older/ounger cabin splits
Younger_Camp_List = []
Older_Camp_List = [Twentythree, Twentyfour, Twentyfive, Twentysix, Twentyseven, Twentynine, Thirty, Thirtyone, Thirtytwo, Thirtythree, Thirtyfour, Thirtyfive]

YoungerCamp = Camp("Younger Camp", Younger_Camp_List, 0)
OlderCamp = Camp("Older Camp", Older_Camp_List, 1)


## Get picks from the excel sheet
OlderCamp.get_picks(cabin_picks)
YoungerCamp.get_picks(cabin_picks)

##for cabin in Older_Camp_List:
##    print(cabin.number, cabin.Picks)

## Instatiate schedules 
OlderSchedule = schedule(OlderCamp, "Older Camp Schedule")
YoungerSchedule = schedule(YoungerCamp, "Younger Camp Schedule")

## Create random sampling of activity preferences for all cabins to use for testing
def random_sampling(camp_list):
    for cabin in camp_list:
        cabin_picks = random.sample(list(ACTIVITIES), 10)
        cabin_pick_numbers = random.sample(range(1,50), 10)
        cabin.Picks(dict(zip(cabin_picks, cabin_pick_numbers)))
        
## Uncomment for random sampling to replace
        prefs
## random_sampling(Older_Camp_List)
## random_sampling(Younger_Camp_List)

## Draft for all six periods
for i in range(6):
    YoungerSchedule.draft()
    OlderSchedule.draft()

#printSchedule(OlderSchedule)
YoungerSchedule.print_open_activities()
OlderSchedule.print_open_activities()
export_Picks(YoungerSchedule, "Younger-Schedule.xls")
export_Picks(OlderSchedule, "Older-Schedule.xls")


