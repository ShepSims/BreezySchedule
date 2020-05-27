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
             "Frisbee":2,
             "Horseback":1}

## Activity class definition
class Activity:
    def __init__(self, name, location):
        self.name = name
        self.location = location

## Define Open Activities and their respective locations

ACTIVITIES = {"Challenge Course":"Challenge Course",
              "Soccer":"field",
              "Football":"field",
              "Riflery": "Riflery",
              "Backyard Games":"Duke",
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

    def assign_activity(self, cabin):
        choice = self.get_next_choice(cabin)
        choice_location = ACTIVITIES[choice]

        ## Try to assign choice location to cabin during any time slot
        for x in range(len(self.open_locations)):

            ## If there is an open locaiton for this activity during an
            ## activity period, assign it and decrease location openings by 1
            ## for that activity period
            if self.open_locations[x][choice_location] != 0:
                if x == 0 and self.schedule[cabin]["A-Day"]["Period One"] == None:
                    self.schedule[cabin]["A-Day"]["Period One"] = choice
                    self.open_locations[x][choice_location] -= 1
                    cabin.picks.pop(choice)
                    break
                elif x == 1 and self.schedule[cabin]["A-Day"]["Period Two"] == None:
                    self.schedule[cabin]["A-Day"]["Period Two"] = choice
                    self.open_locations[x][choice_location] -= 1
                    cabin.picks.pop(choice)
                    break
                elif x == 2 and self.schedule[cabin]["A-Day"]["Period Three"]:
                    self.schedule[cabin]["A-Day"]["Period Three"] = choice
                    self.open_locations[x][choice_location] -= 1
                    cabin.picks.pop(choice)
                    break
                elif x == 3 and self.schedule[cabin]["B-Day"]["Period One"] == None:
                    self.schedule[cabin]["B-Day"]["Period One"] = choice
                    self.open_locations[x][choice_location] -= 1
                    cabin.picks.pop(choice)
                    break
                elif x == 4 and self.schedule[cabin]["B-Day"]["Period Two"] == None:
                    self.schedule[cabin]["B-Day"]["Period Two"] = choice
                    self.open_locations[x][choice_location] -= 1
                    cabin.picks.pop(choice)
                    break
                elif x == 5 and self.schedule[cabin]["B-Day"]["Period Three"] == None:
                    self.schedule[cabin]["B-Day"]["Period Three"] = choice
                    self.open_locations[x][choice_location] -= 1
                    cabin.picks.pop(choice)
                    break
            elif x == 5:
                increase_next_choice = cabin.picks.pop(choice)/2
                new_choice = self.get_next_choice(cabin)
                cabin.picks[new_choice]+=increase_next_choice
                self.assign_activity(cabin)

    def draft(self):
        for cabin in self.schedule:
            try:
                self.assign_activity(cabin)
            except AttributeError:
                print("You have not filled out enough of cabin",cabin.number+"'s activity preferences")
        #print(draftround)
        
            
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

## Create Older/Younger cabin splits

Younger_Camp_List = [One, Two, Three]
Older_Camp_List = [Fifteen, Sixteen, Seventeen, Eighteen]

YoungerCamp = Camp("Younger Camp", Younger_Camp_List, 0)
OlderCamp = Camp("Older Camp", Older_Camp_List, 1)


OlderSchedule = schedule(OlderCamp)

## Insert Picks

Fifteen.Picks({"Horseback":28,"Challenge Course":15, })
Sixteen.Picks({"Horseback":28,"Challenge Course":15})
Seventeen.Picks({"Horseback":28,"Challenge Course":15})

OlderSchedule.draft()
OlderSchedule.draft()
printSchedule(OlderSchedule)
