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
    def __init__(self, campers):
        self.campers = campers
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
        self.open_locations = locations
        self.schedule = {}

    def create(self, cabins):
        for cabin in cabins:
                self.schedule[cabin] = cabin.Activities

    def draft(self):
        print(Sixteen.picks)
        return
        
            
def schedule(camp):
    s = Schedule()
    s.create(camp.cabin_list)
    for item in s.schedule:
        print(s.schedule[item])
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
One = Cabin(8)
Two = Cabin(8)
Three = Cabin(8)
Four = Cabin(8)
Five = Cabin(8)
Six = Cabin(6)
Seven = Cabin(7)
Eight = Cabin(8)
Nine = Cabin(8)
Ten = Cabin(8)
Eleven = Cabin(8)
Twleve = Cabin(8)
Thirteen = Cabin(8)
Fourteen = Cabin(8)
Fifteen = Cabin(8)
Sixteen = Cabin(8)
Seventeen = Cabin(8)
Eighteen = Cabin(8)
Nineteen = Cabin(8)
Twenty = Cabin(8)
Twentyone = Cabin(8)
Twentytwo = Cabin(8)
Twentythree = Cabin(8)

## Create Older/Younger cabin splits

Younger_Camp_List = [One, Two, Three]
Older_Camp_List = [Fifteen, Sixteen, Seventeen]

YoungerCamp = Camp("Younger Camp", Younger_Camp_List, 0)
OlderCamp = Camp("Older Camp", Older_Camp_List, 1)


OlderSchedule = schedule(Older_Camp_List)


## Insert Picks

Sixteen.Picks({"Horseback":28,"Challenge Course":15})
