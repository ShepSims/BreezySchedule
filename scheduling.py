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
             "Flagpole Field":1,
             "GA Field 1":1,
             "GA Field 2":1,
             "GA Field 3":1,
             "Chapel Point Field":1,
             "Golf Field 1":1,
             "Golf Field 2":1,
             "Guitar":1,
             "OLS":1,
             "Pottery":1,
             "Riflery":1,
             "Tennis":1,
             "Volleyball":1,
             "Tree Climbing":1,
             "Gaga":1,
             "Disc Golf":2,
             "Horseback":1}

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
              "Challenge Course":"Challenge Course",
              "Drama":["Rec Hall","Rec Hall Porch", "Ampitheatre"],
              "Dance":["Rec Hall","Rec Hall Porch", "Ampitheatre"],
              "Cheer":["Rec Hall","Rec Hall Porch", "Ampitheatre"],
              "Fishing":"Fishing",
              "Soccer":["GA Field 1","GA Field 2", "GA Field 3", "Golf Field 1", "Golf Field 2"],
              "Flag Football":["GA Field 1","GA Field 2", "GA Field 3", "Chapel Point Field", "Golf Field 1", "Golf Field 2"],
              "Ultimate":["Golf Field 1", "Golf Field 2", "Chapel Point Field","GA Field 1","GA Field 2", "GA Field 3","Flagpole Field"],
              "Lacrosse":["GA Field 1","GA Field 2", "GA Field 3", "Golf Field 1", "Golf Field 2"],
              "Guitar":"Guitar",
              "OLS":"OLS",
              "Pottery":"Pottery",
              "Riflery": "Riflery",
              "Tennis":"Tennis",
              "Volleyball":"Volleyball",
              "Tree Climbing":"Tree Climbing",
              "Gaga":"Gaga",
              "Disc Golf":"Disc Golf",
              "Horseback":"Horseback"}


## Camp class to be used in seperating and dealing with older vs younger camps
class Camp:
    def __init__(self, name, cabin_list, age_type:bool):
        self.cabin_list = cabin_list
        self.name = name
        self.type = age_type

## Cabin class which stores the number of campers, their activity preferences,
class Cabin:
    def __init__(self, number, campers):
        self.number = number
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
        self.picked_in_this_round = False
        return self.picks

    
class Schedule:
    def __init__(self, activity_list = ACTIVITIES, locations = LOCATIONS):
        self.activity_list = activity_list
        self.open_locations = [{},{},{},{},{},{}]
        for key in LOCATIONS:
            for period in self.open_locations:
                period[key] = LOCATIONS[key]
            self.open_locations
        self.schedule = {}
        self.picks = {}

    def create(self, cabins):
        for cabin in cabins:
            self.schedule[cabin] = cabin.Activities

        for cabin in cabins:
            self.picks[cabin] = cabin.picks

    def get_next_choice(self, cabin):
        return (max(cabin.picks, key=cabin.picks.get))

    def assign(self, cabin, activity, location, last_location_to_try = True):
        try:
        ## Try to assign choice location to cabin during any time slot
            for x in range(len(self.open_locations)):
                
                ## If there is an open locaiton for this activity during an
                ## activity period, assign it and decrease location openings by 1
                ## for that activity period
                if self.open_locations[x][location] != 0:
                    if x == 0 and self.schedule[cabin]["A-Day"]["Period One"] == None:
                        self.schedule[cabin]["A-Day"]["Period One"] = activity
                        self.open_locations[x][location] -= 1
                        cabin.picks.pop(activity)
                        return True
                    elif x == 1 and self.schedule[cabin]["A-Day"]["Period Two"] == None:
                        self.schedule[cabin]["A-Day"]["Period Two"] = activity
                        self.open_locations[x][location] -= 1
                        cabin.picks.pop(activity)
                        return True
                    elif x == 2 and self.schedule[cabin]["A-Day"]["Period Three"] == None:
                        self.schedule[cabin]["A-Day"]["Period Three"] = activity
                        self.open_locations[x][location] -= 1
                        cabin.picks.pop(activity)
                        return True
                    elif x == 3 and self.schedule[cabin]["B-Day"]["Period One"] == None:
                        self.schedule[cabin]["B-Day"]["Period One"] = activity
                        self.open_locations[x][location] -= 1
                        cabin.picks.pop(activity)
                        return True
                    elif x == 4 and self.schedule[cabin]["B-Day"]["Period Two"] == None:
                        self.schedule[cabin]["B-Day"]["Period Two"] = activity
                        self.open_locations[x][location] -= 1
                        cabin.picks.pop(activity)
                        return True
                    elif x == 5 and self.schedule[cabin]["B-Day"]["Period Three"] == None:
                        self.schedule[cabin]["B-Day"]["Period Three"] = activity
                        self.open_locations[x][location] -= 1
                        cabin.picks.pop(activity)
                        return True
                elif x == 5 and last_location_to_try == True:
                    increase_next_choice = cabin.picks.pop(activity)/2
                    new_activity = self.get_next_choice(cabin)
                    cabin.picks[new_activity]+=increase_next_choice
                    self.assign_activity(cabin)
            return False
        except:
            print("You probably dont have enough activities picked out for cabin",cabin.number)

    def assign_activity(self, cabin):
        choice = self.get_next_choice(cabin)
        choice_location = ACTIVITIES[choice]
        if type(choice_location) == list:
            for l in choice_location:
                if l == len(choice_location)-1:
                    last_location_to_try = True
                else:
                    last_location_to_try = False
                # Check if the assignment finished, if so break out, if not try again
                check = self.assign(cabin, choice, l, last_location_to_try)
                if check == True:
                    break
        else:
            self.assign(cabin, choice, choice_location)

    def draft(self):
        ## Sort the cabins into order which prioritizes cabins who all agree on activities
        try:
            best = {}
            for cabin in self.schedule:
                best[cabin] = cabin.picks[self.get_next_choice(cabin)]
            best = sorted(best.items(), key = lambda x: x[1], reverse = True)
            for cabin in best:
                self.assign_activity(cabin[0])
                
        except AttributeError:
            print("You have not filled out enough of cabin",cabin.number+"'s activity preferences")

    def open_activities(self):
        for period in range(len(self.open_locations)):
            if period < 4:
                day = "A"
            else:
                day = "B"
            print(day,"Day","activity period",period%3+1,"has the following locations availible:\n",self.open_locations[period])
        
            
def schedule(camp):
    s = Schedule()
    s.create(camp.cabin_list)
##    except:
##        print("Something else went wrong")
    return s

def printSchedule(schedule):
    for item in schedule.schedule:
        print("Cabin",item.number, "schedule: ",schedule.schedule[item])

def assignCamps(younger, older):
    for cabin in younger:
        Younger.cabin_list.append(cabin)
    for cabin in older:
        Older.cabin_list.append(cabin)
    

def Change_Schedule(self, current_activity, desired_activity):
    return
        

## Initialize cabins at camp
One = Cabin("One", 8)
Two = Cabin("Two", 8)
Three = Cabin("Three",8)
Four = Cabin("Four",8)
Five = Cabin("Five",8)
Six = Cabin("Six",6)
Seven = Cabin("Seven",7)
Eight = Cabin("Eight",8)
Nine = Cabin("Nine",8)
Ten = Cabin("Ten",8)
Eleven = Cabin("Eleven",8)
Twleve = Cabin("Twelve",8)
Thirteen = Cabin("Thriteen",8)
Fourteen = Cabin("Fourteen",8)
Fifteen = Cabin("Fifteen",8)
Sixteen = Cabin("Sixteen",8)
Seventeen = Cabin("Seventeen",8)
Eighteen = Cabin("Eighteen",8)
Nineteen = Cabin("Nineteen",8)
Twenty = Cabin("Twenty",8)
Twentyone = Cabin("Twentyone",8)
Twentytwo = Cabin("Twentytwo",8)
Twentythree = Cabin("Twentythree",8)
Twentyfour = Cabin("Twentyfour",8)
Twentyfive = Cabin("Twentyfive",8)
Twentysix = Cabin("Twentysix", 8)
Twentyseven = Cabin("Twentyseven", 8)
Twentyeight = Cabin("Twentyeight", 8)
Twentynine = Cabin("Twentynine",8)
Thirty = Cabin("Thirty",8)

## Create Older/Younger cabin splits

Younger_Camp_List = [One, Two, Three]
Older_Camp_List = [Fifteen, Sixteen, Seventeen, Eighteen, Nineteen, Twenty, Twentyone, Twentytwo, Twentythree, Twentyfour, Twentyfive, Twentysix, Twentyseven, Twentyeight, Twentynine, Thirty]

YoungerCamp = Camp("Younger Camp", Younger_Camp_List, 0)
OlderCamp = Camp("Older Camp", Older_Camp_List, 1)


OlderSchedule = schedule(OlderCamp)

## Insert Picks for each cabin in camps

Fifteen.Picks({"Basketball":28,"Challenge Course":15, "Soccer":14, "OLS":5, "Drama":7, "Fishing":10, "BYG":9})
Sixteen.Picks({"Horseback":2,"Challenge Course":19, "Archery":20, "Riflery":18, "Fishing":5, "Soccer":2})
Seventeen.Picks({"Horseback":18,"Challenge Course":15, "OLS":2, "Dance":4, "Drama":3, "Football":3})

##
def random_sampling(camp_list):
    for cabin in camp_list:
        cabin_picks = random.sample(list(ACTIVITIES), 10)
        cabin_pick_numbers = random.sample(range(1,50), 10)
        cabin.Picks(dict(zip(cabin_picks, cabin_pick_numbers)))
random_sampling(Older_Camp_List)

for cabin in Older_Camp_List:
    print(cabin.picks)
## Draft for all six periods
OlderSchedule.draft()
OlderSchedule.draft()
OlderSchedule.draft()
OlderSchedule.draft()
OlderSchedule.draft()
OlderSchedule.draft()

printSchedule(OlderSchedule)
OlderSchedule.open_activities()
