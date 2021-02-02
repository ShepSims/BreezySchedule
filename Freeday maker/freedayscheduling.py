'''
    Free Day Scheduling Assistant
    
    An activity scheduling assistant is built for YMCA Camp Thunderbird,
    a branch of the YMCA of Greater Charlotte, to assist with
    scheduling cabin activities on free days.
    
    Copyright (C) 2020 Shepherd Sims
    
    MIT License
'''
import random
import xlrd
import xlwt

## Configure limitations on open locations day to day here 

LIMITATIONS = {"Ski":[1,2,3,4,5,6,7,8],
               "Sail":[9,10,11,12,13,14,15,16],
               "Tree Climbing":[0],
               "OLS":[9,10,11,12,13,14,15,16]}

## Locations around camp which are availible for use during land activities
        
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
             "GA Field 1":1,
             "GA Field 2":1,
             "GA Field 3":1,
             "Chapel Point Field":1,
             "Golf Field 1":1,
             "Golf Field 2":1,
             "OLS":1,
             "Riflery":1,
             "Tennis":1,
             "Volleyball":1,
             "Tree Climbing":1,
             "Gaga":1,
             "Disc Golf":2,
             "Putt Putt":0,
             "Ski": 2,
             "Water Toys":3,
             "Rec Swim":2,
             "Pool":3,
             "Paddle":2,
             "Sail":0,
             "Slip n Slide":0,
             "Pottery":0}

## Activity class definition
class Activity:
    def __init__(self, name, location):
        self.name = name
        self.location = location

##  All Activities at camp and their respective possible locations

ACTIVITIES = {"Archery":"Archery",
              "Arts and Crafts":"Arts and Crafts",
              "Athletic Conditioning":"Loop",
              "BYG":"Duke",
              "Basketball":["Basketball Court","Duke"],
              "Baseball":"Baseball",
              "Challenge Course":"Challenge Course",
              "Drama":["Rec Hall Porch", "Ampitheatre"],
              "Dance":["Rec Hall Porch", "Ampitheatre"],
              "Cheer":["Rec Hall Porch", "Ampitheatre"],
              "Fishing":"Fishing",
              "Soccer":["GA Field 1","GA Field 2", "GA Field 3", "Golf Field 1", "Golf Field 2"],
              "Flag Football":["GA Field 1","GA Field 2", "GA Field 3", "Chapel Point Field", "Golf Field 1", "Golf Field 2"],
              "Ultimate":["Golf Field 1", "Golf Field 2", "Chapel Point Field","GA Field 1","GA Field 2", "GA Field 3","Flagpole Field"],
              "Lacrosse":["GA Field 1","GA Field 2", "GA Field 3", "Golf Field 1", "Golf Field 2"],
              "OLS":"OLS",
              "Riflery": "Riflery",
              "Softball":"Baseball Field",
              "Tennis":"Tennis",
              "Volleyball":"Volleyball",
              "Tree Climbing":"Tree Climbing",
              "Gaga":"Gaga",
              "Disc Golf":"Disc Golf",
              "Putt Putt":"Putt Putt",
              "Pool":"Pool",
              "Ski":"Ski",
              "PATTL":"Paddle",
              "Sail":"Sail",
              "Water Toys":"Water Toys",
              "Rec Swim":"Rec Swim",
              "Slip n Slide":"Slip n Slide",
              "Pottery":"Pottery"}

## Cabin class which stores the number of campers, their activity preferences,
class Cabin:
    def __init__(self, number, n, periods):
        self.number = number
        self.n = n
        self.picks = {}
        self.periods = periods
        self.Activities = {}
        
        for i in range(len(periods)):
            self.Activities[self.periods[i]] = None

    def Picks(self, picks):
        self.picks = picks
        return self.picks
    
## Camp class to be used in seperating and dealing with older vs younger camps
class Camp:
    def __init__(self, name, cabin_list, age_type:bool):
        self.cabin_list = cabin_list
        self.name = name
        self.type = age_type

    def get_picks(self, cabin_picks):
        for cabin in self.cabin_list:
            cabin.Picks(cabin_picks[cabin.number])

    
class Schedule:
    def __init__(self, activity_list = ACTIVITIES, locations = LOCATIONS):
        self.activity_list = activity_list
        self.open_locations = [{},{},{},{},{},{},{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
        for key in LOCATIONS:
            for period in self.open_locations:
                period[key] = LOCATIONS[key]
        self.schedule = {}
        self.picks = {}

    def donothing(self):
        return

    def create(self, name, cabins, p = False):
        self.name = name
        for cabin in cabins:
            self.schedule[cabin] = cabin.Activities
                
        if p == True:
            for cabin in cabins:
                print("Cabin",cabin.n, "Schedule:",self.schedule[cabin],"\n",self.picks[cabin])

    
    ## Create random sampling of activity preferences for cabins if they dont submit prefs
    def random_sampling(self, cabin):
        choice = [0, -1, -2, -3 ,-4, 5, 4, 3, 2, 1,-6,-7,-8,-9,10]
        cabin_picks = random.sample(list(ACTIVITIES), 15)
        random.shuffle(choice)
        picks = dict(zip(cabin_picks, choice))
        return picks

    def get_top_choice(self, cabin):
        try:
            top = max(self.picks[cabin.number], key=self.picks[cabin.number].get)
            if top == '':
                self.picks[cabin.number] = self.random_sampling(cabin)
                top = max(self.picks[cabin.number], key=self.picks[cabin.number].get)
            return top
        except:
            if self.picks[cabin.number] == {}:
                try:
                    self.picks[cabin.number] = cabin.picks
                except:
                    self.picks[cabin.number] = self.random_sampling(cabin)
                finally:
                    return self.get_top_choice(cabin)

            # All else fails, give random
            return random.sample(self.activity_list)
    
    def get_cabin_schedule(self, cabin):
        return self.schedule[cabin]

    '''
    Draft one activity for each cabin, prioritizing cabins who agree that all the campers want a specific activity
    '''
    def draft(self):
        
        ## Create a dictionary of each cabin's top activity choice
        best_all_cabins = {}
        for cabin in self.schedule:
            try:
                best_all_cabins[cabin] = self.get_top_choice(cabin)
            except KeyError:
                best_all_cabins[cabin] = random.randint(0,5)

        ## Sort the cabins into order which prioritizes cabins who all agree on a top activity
        best_all_cabins = sorted(best_all_cabins.items(), key = lambda x: x[1], reverse = True)

        ## Assign each cabin one activity
        for cabin in best_all_cabins:
            if None in cabin[0].Activities.values():
                self.assign_activity(cabin[0])

    '''
    Try to assign a cabin to an activity at a specific location
    '''
    def assign(self, cabin, activity, location, last_location_to_try = True):
        
    ## Try to assign choice location to cabin during any time slot
        try:
            for activity_period in range(16):
                ## Uncomment for scheduling walk-through
                print("Cabin",cabin.number,"Try activity",activity, "at",location, "during", activity_period, "with",self.open_locations[activity_period][activity],"openings:",  "and current",self.schedule[cabin])
                
                ## If there is an open locaiton for this activity during a cabin's unassigned activity period, assign activity here and decrease the location's openings by 1 for that period
                if self.open_locations[activity_period][location] != 0 and not (activity in LIMITATIONS and activity_period in LIMITATIONS[activity]):
                    #print("Cabin",cabin.n,"Activity Period:",activity_period, "Activities:",cabin.Activities, "Activity:" ,activity, "Open: ",self.open_locations[activity_period][activity])
                    if activity_period in cabin.Activities and cabin.Activities[activity_period] == None:
                        self.schedule[cabin][activity_period] = activity
                        self.open_locations[activity_period][location] -= 1
                        self.picks[cabin.number].pop(activity)
                        print("Success")
                        return True
                    
                ## If you have tried to put the cabin's top activity into the schedule but there were no slots, raise their next top activity's preference score and try again
                if activity_period == 15 and last_location_to_try == True:
                    increase_next_choice = self.picks[cabin.number].pop(activity)/2

                    #Uncomment to see which cabin's got picks boosted because their top chioces were already taken
                    #print("Cabin:",cabin.number, "gets",self.get_top_choice(cabin),"boosted by",increase_next_choice)
                    
                    new_activity = self.get_top_choice(cabin)
                    self.picks[cabin.number][new_activity]+=increase_next_choice
                    return False
        except:
            #print(cabin.n, "Current",cabin.Activities)
            #print ("Sorry you didn't get",activity, "cabin",cabin.n)
            print("Exeption raised")
            
        
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
            print("Try!")
            self.assign_activity(cabin)
            

    def random_activity():
        return random.sample(self.activity_list, 1)

    '''
    Display a list of all open locations during each activity period
    '''
    def open_activities(self):
        open_activities = {}
        for period in range(len(self.open_locations)):
            temp = {}
            for a in self.open_locations[period]:
                if self.open_locations[period][a] > 0:
                    temp[a] = self.open_locations[period][a]
            open_activities[period]=temp
        return open_activities

    def print_open_activities(self):
        activities = self.open_activities()
        for period in activities:
            print("Period:",period, activities[period])

    def get_picks(self, filename):
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        cabins = {}
        for row in range(worksheet.nrows):
            number = worksheet.cell_value(row, 0)
            if row > 0:
                cabins[number] = {}
                for col in range(worksheet.ncols):
                    if col > 0:
                        if worksheet.cell_value(row, col) != xlrd.empty_cell.value:
                            cabins[number][worksheet.cell_value(0, col)] = int(worksheet.cell_value(row, col))
        for cabin in cabins:
            # If they provided picks, use them
            if cabins[cabin] != {}:
                self.picks[cabin] = cabins[cabin]
            # Otherwise, assign random with -5 to 5 as scores
            else:
                self.picks[cabin] = self.random_sampling(cabin)

        for cabin in self.schedule:
            cabin.picks = self.picks[cabin.number]
            
def schedule(camp, name, p = False):
    s = Schedule()
    s.create(name, camp.cabin_list, p)
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

## Choose cabin's timeslots
Younger = [0,1,3,4,5,8,9,11,12,13]
Older = [0,1,2,4,5,6,7, 8, 9, 10, 12, 13, 14, 15]

## Instantiate cabins
#One = Cabin("One", 1,Younger)
#Two = Cabin("Two", 2, Younger)
Three = Cabin("Three",3,Younger)
Four = Cabin("Four",4,Younger)
Five = Cabin("Five",5,Younger)
Six = Cabin("Six",6,Younger)
Seven = Cabin("Seven",7,Younger)
Eight = Cabin("Eight",8,Younger)
Nine = Cabin("Nine",9,Younger)
Ten = Cabin("Ten",10,Younger)
Eleven = Cabin("Eleven",11,Younger)
#Twelve = Cabin("Twelve",12)
#Thirteen = Cabin("Thirteen",13)
#Fourteen = Cabin("Fourteen",14)
Fifteen = Cabin("Fifteen",15,Older)
Sixteen = Cabin("Sixteen",16,Older)
#Seventeen = Cabin("Seventeen",[2,4,6])
#Eighteen = Cabin("Eighteen",18)
Nineteen = Cabin("Nineteen",19,Older)
Twenty = Cabin("Twenty",20,Older)
Twentyone = Cabin("Twentyone",21,Older)
Twentytwo = Cabin("Twentytwo",22,Older)
#Twentythree = Cabin("Twentythree",23)
#Twentyfour = Cabin("Twentyfour",24)
Twentyfive = Cabin("Twentyfive",25, Older)
#Twentysix = Cabin("Twentysix", 26,Older)
Twentyseven = Cabin("Twentyseven", 27,Older)
#Twentyeight = Cabin("Twentyeight", 28)
#Twentynine = Cabin("Twentynine",29)
Thirty = Cabin("Thirty",30,Older)
#Thirtyone = Cabin("Thirtyone",[)
Thirtytwo = Cabin("Thirtytwo",32,Older)
Thirtythree = Cabin("Thirtythree",33,Older)
Thirtyfour = Cabin("Thirtyfour",34,Older)
Thirtyfive = Cabin("Thirtyfive",35, Older)

workbook = xlrd.open_workbook('Freeday Prefs.xls')
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
    ws = wb.add_sheet(schedule.name, cell_overwrite_ok=True)
    ws.write(0,1, "Sat AM 1")
    ws.write(0,2, "Sat AM 2")
    ws.write(0,3, "Sat AM 3")
    ws.write(0,4, "Sat PM 1")
    ws.write(0,5, "Sat PM 2")
    ws.write(0,6, "Sat PM 3")
    ws.write(0,7, "Sat PM 4")
    ws.write(0,8, "Sat PM 5")
    ws.write(0,9, "Sun AM 1")
    ws.write(0,10, "Sun AM 2")
    ws.write(0,11, "Sun AM 3")
    ws.write(0,12, "Sun PM 1")
    ws.write(0,13, "Sun PM 2")
    ws.write(0,14, "Sun PM 3")
    ws.write(0,15, "Sun PM 4")
    ws.write(0,16, "Sun PM 5")
    
    c = 1
    for cabin in schedule.schedule:
        ws.write(c, 0, cabin.number)
        i = 0
        for period in schedule.schedule[cabin]:
            if schedule.schedule[cabin][period] != None:
                ws.write(c, period+1, schedule.schedule[cabin][period])
                
        c+=1
    wb.save(filename)
    
## Create Older/ounger cabin splits
Younger_Camp_List = [Four, Five, Six, Eight, Nine, Ten, Eleven, Twentyfive]
Older_Camp_List = [Twentyseven, Fifteen, Sixteen, Thirty, Thirtytwo, Thirtythree, Thirtyfour, Thirtyfive, Nineteen, Twenty, Twentyone, Twentytwo]
ALL_CAMP = Younger_Camp_List + Older_Camp_List

YoungerCamp = Camp("Younger Camp", Younger_Camp_List, 0)
OlderCamp = Camp("Older Camp", Older_Camp_List, 1)
ALLCAMP = Camp("All Camp", ALL_CAMP, 2)

#OlderCamp.get_picks(cabin_picks)
##for cabin in Older_Camp_List:
##    print(cabin.number, cabin.Picks)
#YoungerCamp.get_picks(cabin_picks)

OlderSchedule = schedule(OlderCamp, "Older Camp Schedule")
YoungerSchedule = schedule(YoungerCamp, "Younger Camp Schedule")
ALL_CAMP_SCHEDULE = schedule(ALLCAMP, "All Camp Schedule")
ALL_CAMP_SCHEDULE.get_picks('Freeday Prefs.xls')

        
## Uncomment for random sampling to test without excell input
## random_sampling(Older_Camp_List)
## random_sampling(Younger_Camp_List)

## Draft for all six periods
for i in range(14):
    ALL_CAMP_SCHEDULE.draft()

#printSchedule(OlderSchedule)
#YoungerSchedule.print_open_activities()
#ALL_CAMP_SCHEDULE.print_open_activities()
#printSchedule(ALL_CAMP_SCHEDULE)

export_Picks(ALL_CAMP_SCHEDULE, "Freeday.xls")


