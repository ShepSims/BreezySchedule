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

## Availible locations around camp which are availible for use during land activities

LOCATIONS = {"Archery":1,
             "Arts and Crafts":1,
             "Loop":1,
             "Duke":1,
             "Baseball Field":1,
             "Basketball Court":2,
             "Challenge Course":1,
             "Rec Hall":1,
             "Rec Hall Porch":1,
             "Ampitheatre":1,
             "Fishing":1,
             "Field":5,
             "Guitar":1,
             "OLS":1,
             "Pottery":1,
             "Riflery":1,
             "Tennis":1,
             "Volleyball":1,
             "Tree Climbing":1,
             "Gaga":1,
             "Frisbee":2}

## Activity class definition
class Activity:
    def __init__(self, name, location):
        self.name = name
        self.location = location

## Define Open Activities and their respective locations

Challenge_Course = Activity("Challege Course", "challenge course")

Soccer = Activity("Soccer", "field")

Football = Activity("Football", "field")

Riflery = Activity("Riflery", "riflery")

BYG = Activity("Backyard Games","duke")

ACTIVITIES = [Challenge_Course,
              Soccer,
              Football,
              Riflery,
              BYG]


## Camp class to be used in seperating and dealing with older vs younger camps
class Camp:
    def __init__(self, name, cabin_list, age_type:bool):
        self.cabin_list = cabin_list
        self.name = name
        self.type = age_type

## Cabin class which stores the number of campers, their activity preferences,
class Cabin:
    def __init__(self, campers, active = False):
        self.campers = campers
        self.active = active
        self.a_day_activities = {"Period One":None,
                                 "Period Two":None,
                                 "Period Three":None}
        self.b_day_activities = {"Period One":None,
                                 "Period Two":None,
                                 "Period Three":None}

    def Picks(self, picks):
        self.picks = picks
        return picks
    
class Schedule:
    def __init__(self, activity_list = ACTIVITIES, locations = LOCATIONS):
        self.activity_list = activity_list
        self.open_locations = locations
        self.schedule = {}

    def create(self, cabins):
        for cabin in cabins:
            if cabin.active:
                self.schedule[cabin] = [cabin.a_day_activities, cabin.b_day_activities]

    def draft(self, picks):
        return
        
            
def schedule(camp):
    s = Schedule()
    s.create(camp.cabin_list)
    print(s.schedule[22])
##    except NameError:
##        print("You have likely not filled out all active cabin's activity preferences")
##    except:
##        print("Something else went wrong")

def assignCamps(younger, older):
    for cabin in younger:
        Younger.cabin_list.append(cabin)
    for cabin in older:
        Older.cabin_list.append(cabin)
    

def Change_Schedule(self, current_activity, desired_activity):
    return
        

## Initialize cabins at camp
Cabin_One = Cabin(1, True)
Cabin_Two = Cabin(2)
Cabin_Three = Cabin(3)
Cabin_Four = Cabin(4)
Cabin_Five = Cabin(5)
Cabin_Six = Cabin(6)
Cabin_Seven = Cabin(7, True)
Cabin_Eight = Cabin(8)
Cabin_Nine = Cabin(9)
Cabin_Ten = Cabin(10)
Cabin_Eleven = Cabin(11)
Cabin_Twleve = Cabin(12)
Cabin_Thirteen = Cabin(13, True)
Cabin_Fourteen = Cabin(14)
Cabin_Fifteen = Cabin(15)
Cabin_Sixteen = Cabin(16)
Cabin_Seventeen = Cabin(17)
Cabin_Eighteen = Cabin(18)
Cabin_Nineteen = Cabin(19)
Cabin_Twenty = Cabin(20)
Cabin_Twentyone = Cabin(21)
Cabin_Twentytwo = Cabin(22)
Cabin_Twentythree = Cabin(23, True)

## Create Older/Younger cabin splits

Younger_Camp_List = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,23,24,25,15,16]
Older_Camp_List = [26,27,28,15,16,17,30,31,32,33,34,35,18,19,20,21,22]

YoungerCamp = Camp("Younger Camp", Younger_Camp_List, 0)
OlderCamp = Camp("Older Camp", Older_Camp_List, 1)


OlderSchedule = schedule(OlderCamp)
