'''
    BreezySchedule
    
    An activity scheduling assistant built for YMCA Camp Thunderbird to substantially lower time necessary to make optimal schedules.
    
    Originally created to make possible rapid adaptation to volatile CDC guidelines for summer camps during the COVID-19 outbreak.


    External packages:
        random - Used to generate sudo-random numbers
        xlrd   - Used to read from xlxs files
        xlwt   - Used to write to xlxs files        

    Copyright (C) 2020 Shepherd Sims
    
    MIT License
    
'''
import random
import xlrd
import xlwt

class Camp:
    '''
    Camps are used to define groups of cabins running on different schedules

    parameters:
    cabin_list  - A list of the cabins in Camp object (ex. [One, Two, Three])
    name        - Name of the camp (ex. 'Older' or 'Younger')
    '''
    
    def __init__(self, name, cabin_list):
        '''
        Initializes Camp object

        parameters:
            name        - Name of the camp (ex. 'Older' or 'Younger')
            cabin_list  - A complete list of the cabin objects in a Camp (ex. [One, Two, Three])
        '''
        
        self.cabin_list = cabin_list
        self.name = name

    def get_prefs(self, cabin_prefs):
        '''
        Gets and stores the activity prefereces for each Cabin in Camp
        '''
        for cabin in self.cabin_list:
            cabin.prefs = cabin_prefs[cabin.number]
            

class Cabin:
    '''
    Cabin objects store activity preferences and schedules for a particular cabin

    Attributes:
        number     - The cabin number as string (ex. 'One')
        n          - The cabin number as int (ex. 1)
        prefs      - The cabin's activity preferences, empty until global function get_prefs is invoked
        Activities - The cabin's assigned schedule of activities
    '''
    
    def __init__(self, number, n):
        '''
        Initializes a Cabin object with no prefs and an empty schedule
        
        parameters:
            number - The cabin number as string (ex. 'One')
            n      - The cabin number as int (ex. 1)
        '''
        self.number = number
        self.n = n
        self.prefs = None
        self.schedule = {'A-Day':{'Period One':None,
                                 'Period Two':None,
                                 'Period Three':None},
                           'B-Day':{'Period One':None,
                                 'Period Two':None,
                                 'Period Three':None}}

    
class Schedule:
    '''
    Schedule objects contain all information about schedules for the associated cabins and locations

    Attributes:
        activity_list  - A dictionary of all activities and potential locations for those activities (ex. {'Archery':'Archery','Basketball':['Basketball Courts','Duke Pavillion'],...})
        name           - The name of the schedule (ex. 'YoungerSchedule' or 'OlderSchedule')
        open_locations - A list containing dictionaries of locations and their available times (ex. {'Archery':1,'Basketball Courts':4, 'Duke Pavillion':1})
        periods        - The number of unique time periods in a schedule as an int (ex. 6)
        prefs          - A dictionary of preferences for each cabin object in the schedule (ex. {One:{'Archery':10,'Basketball':4,...},Two:{'BYG':10, 'Tree Climbing':6,...},...})
        sad_cabins     - After schedule has been flushed out, this contains a dictionary of all cabins that did not get ALL activities from their preferences (Would be good to allow them to switch to other open activities)
        schedule       - A dictionary of schedules for each cabin object being scheduled
            format:
                {Cabin:{'A-Day':{A-Day Schedule}, 'B-Day':{B-Day Schedule}}, Cabin:{'A-Day':{A-Day Schedule}, 'B-Day':{B-Day Schedule}],...]
            ex:
                {One:{'A-Day':{'Period One':'Archery', 'Period Two':'BYG', 'Period Three':'Tennis'}, 'B-Day':{'Period One':'ATC', 'Period Two':'Pottery', 'Period Three':'Tennis'}}, Tw...]
    '''
    def __init__(self, name, cabins, periods, activity_list, locations):
        '''
        Initializes Schedule object with empty schedules for each cabin object and parameters inherited from Globals unless defined when calling this constructor

        Required parameters:
            name - A name for the schedule (ex. 'Younger Camp Schedule' or 'Older Camp Schedule')
            cabins - A list of Cabin objects for which the schedule is to be made (ex. [One, Two, Three, Four])
        '''
        self.name = name
        self.periods = periods
        self.activity_list = activity_list
        self.open_locations = []
        self.locations = locations
        for i in range(periods):
            self.open_locations.append({})
        random_selections = {}
        for key in self.locations:
            for period in self.open_locations:
                period[key] = self.locations[key]
            self.open_locations
        self.schedule = {}
        self.prefs = {}
        for cabin in cabins:
            self.schedule[cabin] = cabin.schedule
            self.prefs[cabin] = cabin.prefs
        self.sad_cabins = {}

    def get_top_choice(self, cabin):
        '''
        Gets the most desired activity for the cabin if their choices have not all been tried yet, else returns a random activity

        parameters:
            cabin - The cabin to get top activitiy preference from

        returns:
            top - The cabin's top choice for next activity assignment
        '''
        if len(cabin.prefs) !=0:
            top = max(cabin.prefs, key=cabin.prefs.get)
            return top
        else:
            top = random.sample(list(self.activity_list),1)[0]
            return top
            

    def assign(self, cabin, activity, location, last_location_to_try = True):
        '''
        Assigns parameterized activity to cabin's schedule if possible, otherwise increases the weight of cabin's next activity preference

        parameters:
            cabin                - The cabin whose schedule is to be updated (ex. One)
            activity             - The activity trying to be assigned (ex. 'Basketball')
            location             - The location the cabin will be at if the activity is successfully assigned (ex. 'Duke Pavillion' or 'Basketball Courts')
            last_location_to_try - Boolean value noting if this is the last possible location to try to assign the current activity (ex. True)
            
        returns:
            {boolean} - True if the cabin was assigned an activity, else False
        
        '''
        for activity_period in range(self.periods):

            ## Uncomment for scheduling walk-through
            ## print('Cabin',cabin.number,'Try activity',activity, 'at',location, 'during', activity_period, 'with current:', self.schedule[cabin]['A-Day'],self.schedule[cabin]['B-Day'])
            
            ## If there is an open locaiton for this activity during a cabin's unassigned activity period, assign activity here and decrease the location's openings by 1 for that period
            if self.open_locations[activity_period][location] != 0:
                
                if activity_period == 0 and self.schedule[cabin]['A-Day']['Period One'] == None and not activity == 'Pottery': # Day Camp uses pottery during A-Day Period 1
                    self.schedule[cabin]['A-Day']['Period One'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
                    return True
                elif activity_period == 1 and self.schedule[cabin]['A-Day']['Period Two'] == None:
                    self.schedule[cabin]['A-Day']['Period Two'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
                    return True
                elif activity_period == 2 and self.schedule[cabin]['A-Day']['Period Three'] == None:
                    self.schedule[cabin]['A-Day']['Period Three'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
                    return True
                elif activity_period == 3 and self.schedule[cabin]['B-Day']['Period One'] == None and not activity == 'Putt Putt': # Day Camp uses Putt Putt in the afternoons on B Days
                    self.schedule[cabin]['B-Day']['Period One'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
                    return True
                elif activity_period == 4 and self.schedule[cabin]['B-Day']['Period Two'] == None and not activity == 'Putt Putt': # Day Camp uses Putt Putt in the afternoons on B Days
                    self.schedule[cabin]['B-Day']['Period Two'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
                    return True
                elif activity_period == 5 and self.schedule[cabin]['B-Day']['Period Three'] == None and not activity == 'Putt Putt': # Day Camp uses Putt Putt in the afternoons on B Days
                    self.schedule[cabin]['B-Day']['Period Three'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
                    return True

            ## If no open locations found, increase weight of next cabin activity preference to maintain fair scheduling
            if activity_period == 5 and last_location_to_try == True:
                if activity in cabin.prefs:
                    increase_next_choice = cabin.prefs.pop(activity)/2

                # Uncomment to see which cabin's got prefs boosted because their top chioces were already taken
                # print('Cabin:',cabin.number, 'gets',self.get_top_choice(cabin),'boosted by',increase_next_choice)
                
                new_activity = self.get_top_choice(cabin)
                if new_activity in cabin.prefs:
                    cabin.prefs[new_activity]+=increase_next_choice
                else:
                    cabin.prefs[random.sample(list(self.activity_list),1)[0]] = 10
                    # Store which cabins got the short straw
                    try:
                        self.sad_cabins[cabin.number] +=1
                    except KeyError:
                        self.sad_cabins[cabin.number]=1
                return False


    def assign_activity(self, cabin):
        '''
        Loops through each location of a cabin's top choice activity, assigning to the cabin's schedule if an poen location is found

        parameters:
            cabin - The cabin to try to assign top activity choice to
        '''
        # Get a cabin's top choice for activity and its location
        choice = self.get_top_choice(cabin)
        choice_location = self.activity_list[choice]

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
                        
    
    def draft(self):
        '''
        Creates a dictionary of each cabin's top activity preference, then iteratively calls assign_activity in order of each preference's weight 
        '''
        ## Create a dictionary of each cabin's top activity choice
        best = {}
        for cabin in self.schedule:
            if self.get_top_choice(cabin) in cabin.prefs:
                best[cabin] = cabin.prefs[self.get_top_choice(cabin)]
            else:
                best[cabin] = 10

        ## Sort the cabins into order which prioritizes cabins who all agree on a top activity
        best = sorted(best.items(), key = lambda x: x[1], reverse = True)

        ## Assign each cabin one activity
        for cabin in best:
            self.assign_activity(cabin[0])

    def open_activities(self):
        '''
        Returns a data strcuture representing all open activity times in Schedule
        
        returns:
            open_activities - A dictionary of dictionaries of lists showing all open locations for each day/period in schedule
        '''
        open_activities = {'A':[],'B':[]}
        for period in range(len(self.open_locations)):
            if period < 3:
                day = 'A'
            else:
                day = 'B'
            temp = {}
            for a in self.open_locations[period]:
                if self.open_locations[period][a] > 0:
                    temp[a] = self.open_locations[period][a]
            open_activities[day].append(temp)
        return open_activities

    def print_open_activities(self):
        '''
        Prints all open activity times in Schedule 
        '''
        activities = self.open_activities()
        for day in activities:
            print(day, 'Day')
            count = 0
            for period in activities[day]:
                count+=1
                print('Period:',count,period)
        

def printSchedule(schedule):
    '''
    Prints the schedule

    parameters:
        scheudle - a Schedule object
    '''
    for item in schedule.schedule:
        print('\nCabin',item.number, ':')
        for a in schedule.schedule[item]:
            print(schedule.schedule[item][a])

def get_Prefs(worksheet):
    '''
    Gets and stores the activity choices for each entry in the provided worksheet 

    parameters:
        worksheet - An excel sheet from which to pull entries (ex. 'Activities.xlxs')

            format:
    
                cabin     Archery     Art     BYG     . . . 
                One         10         9       2
                Two         8          10      1
                Three       3          8       7
                .
                .
                .
        
    returns:
        cabins - A dictionary of cabins keys and preference dictionary values

            format:
                {Cabin_number:{Activity preferences}, Cabin_number:{Activity preferences},...}
     
             example:
                {'One':{'Archery':10, 'Baseball':3,...}, 'Two':{'Tree Climbing':10, 'BYG':1,...},...}
    '''
    prefs = {}
    for row in range(worksheet.nrows):
        number = worksheet.cell_value(row, 0)
        if row > 0:
            prefs[number] = {}
            for col in range(worksheet.ncols):
                if col > 0:
                    if worksheet.cell_value(row, col) != xlrd.empty_cell.value:
                        prefs[number][worksheet.cell_value(0, col)] = int(worksheet.cell_value(row, col))
    return prefs


def export_Schedule(schedule, filename):
    '''
    Exports the provided schedule to filename.xlsx

    parameters:
        schedule - a Schedule object
        filename - desired filename without extension
    '''
    wb = xlwt.Workbook()
    ws = wb.add_sheet(schedule.name)
    if schedule.name == 'Older Camp Schedule': 
        ws.write(0,1, 'A-Day')
        ws.write(1,1, '9:15-10:15')
        ws.write(1,2, '10:15-11:15')
        ws.write(1,3, '11:15-12:15')
        ws.write(0,4, 'B-Day')
        ws.write(1,4, '9:15-10:15')
        ws.write(1,5, '10:15-11:15')
        ws.write(1,6, '11:15-12:15')
    else:
        ws.write(0,1, 'A-Day')
        ws.write(1,1, '3:00-4:00')
        ws.write(1,2, '4:00-5:00')
        ws.write(1,3, '5:00-6:00')
        ws.write(0,4, 'B-Day')
        ws.write(1,4, '3:00-4:00')
        ws.write(1,5, '4:00-5:00')
        ws.write(1,6, '5:00-6:00')
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

def main():
    '''
    This main function 

    0. Defines globals
    1. Initializes all cabins
    2. Opens the preference workbook and copies them into cabin_prefs
    3. Defines splits (by age here, but any desired split may be used by changing assignment to camp lists)
    4. Initializes camps
    5. Drafts activities into cabin schedules
    6. Exports finished schedules into .xls files

        Global Variables:
        LOCATIONS  - Availible land activity areas around camp
        ACTIVITIES - Activities and their possible locations
        PERIODS    - Number of periods in a generic schedule
        
    '''
    
    LOCATIONS = {'Archery':1,
                 'Arts and Crafts':1,
                 'Baseball':1,
                 'Loop':1,
                 'Duke':1,
                 'Baseball Field':1,
                 'Basketball Court':2,
                 'Challenge Course':1,
                 'Rec Hall':1,
                 'Rec Hall Porch':1,
                 'Ampitheatre':1,
                 'Fishing':1,
                 'Flagpole Field':1,
                 'Chapel Point Field':1,
                 'GA Field 1':1,
                 'GA Field 2':1,
                 'GA Field 3':1,
                 'Golf Field 1':1,
                 'OLS':1,
                 'Riflery':1,
                 'Tennis':1,
                 'Volleyball':1,
                 'Tree Climbing':1,
                 'Gaga':1,
                 'Disc Golf':2,
                 'Putt Putt':1,
                 'Pottery':0,
                 'Dodgeball':1,
                 'Digital Media':1}

    ACTIVITIES = {'Archery':'Archery',
                  'Arts and Crafts':'Arts and Crafts',
                  'Athletic Conditioning':'Loop',
                  'BYG':'Duke',
                  'Basketball':['Basketball Court','Duke'],
                  'Baseball':'Baseball',
                  'Challenge Course':'Challenge Course',
                  'Drama':['Rec Hall Porch', 'Ampitheatre'],
                  'Dance':['Rec Hall Porch', 'Ampitheatre'],
                  'Digital Media':'Digital Media',
                  'Cheer':['Rec Hall Porch', 'Ampitheatre'],
                  'Fishing':'Fishing',
                  'Soccer':['GA Field 1','GA Field 2', 'GA Field 3'],
                  'Softball':'Baseball',
                  'Flag Football':['GA Field 1','GA Field 2', 'GA Field 3'],
                  'Ultimate':['GA Field 1','GA Field 2', 'GA Field 3', 'Chapel Point Field', 'Golf Field'],
                  'Lacrosse':['GA Field 1','GA Field 2', 'GA Field 3'],
                  'OLS':'OLS',
                  'Riflery': 'Riflery',
                  'Tennis':'Tennis',
                  'Volleyball':'Volleyball',
                  'Tree Climbing':'Tree Climbing',
                  'Gaga':'Gaga',
                  'Disc Golf':'Disc Golf',
                  'Putt Putt':'Putt Putt',
                  'Pottery':'Pottery',
                  'Geocaching':'OLS',
                  'Dodgeball':'Dodgeball'}
    PERIODS = 6

    ## Initialize cabins
    One = Cabin('One', 1)
    Two = Cabin('Two', 2)
    Three = Cabin('Three',3)
    Four = Cabin('Four',4)
    Five = Cabin('Five',5)
    Six = Cabin('Six',6)
    Seven = Cabin('Seven',7)
    Eight = Cabin('Eight',8)
    Nine = Cabin('Nine',9)
    Ten = Cabin('Ten',10)
    Eleven = Cabin('Eleven',11)
    Twelve = Cabin('Twelve',12)
    Thirteen = Cabin('Thirteen',13)
    Fourteen = Cabin('Fourteen',14)
    Fifteen = Cabin('Fifteen',15)
    Sixteen = Cabin('Sixteen',16)
    T1 = Cabin('T1',41)
    T2 = Cabin('T2',42)
    Seventeen = Cabin('Seventeen',17)
    Eighteen = Cabin('Eighteen',18)
    Nineteen = Cabin('Nineteen',19)
    Twenty = Cabin('Twenty',20)
    Twentyone = Cabin('Twentyone',21)
    Twentytwo = Cabin('Twentytwo',22)
    Twentythree = Cabin('Twentythree',23)
    Twentyfour = Cabin('Twentyfour',24)
    Twentyfive = Cabin('Twentyfive',25)
    Twentysix = Cabin('Twentysix', 26)
    Twentyseven = Cabin('Twentyseven', 27)
    Twentyeight = Cabin('Twentyeight', 28)
    Twentynine = Cabin('Twentynine',29)
    Thirty = Cabin('Thirty',30)
    Thirtyone = Cabin('Thirtyone',31)
    Thirtytwo = Cabin('Thirtytwo',32)
    Thirtythree = Cabin('Thirtythree',33)
    Thirtyfour = Cabin('Thirtyfour',34)
    Thirtyfive = Cabin('Thirtyfive',35)

    workbook = xlrd.open_workbook('Land Activity Preferences.xlsx')
    worksheet = workbook.sheet_by_index(0)

    cabin_prefs = get_Prefs(worksheet)

    mystyle = xlwt.easyxf('pattern: pattern solid, fore_colour blue')

    ## Create Older/Younger camp splits
    Younger_Cabin_List = [One, Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Eleven, Twelve, Thirteen, Fourteen, Fifteen, Twentythree, Twentyfour, Twentyfive]
    Older_Cabin_List = [Sixteen, Seventeen, Eighteen, Nineteen, Twenty, Twentyone, Twentytwo, Twentysix, Twentyseven, Twentynine, Thirty, Thirtyone, Thirtytwo, Thirtythree, Thirtyfour, Thirtyfive]

    ## Initialize Camp objects
    YoungerCamp = Camp('Younger Camp', Younger_Cabin_List)
    OlderCamp = Camp('Older Camp', Older_Cabin_List)


    ## Get cabin preferences from the excel preference sheet
    OlderCamp.get_prefs(cabin_prefs)
    YoungerCamp.get_prefs(cabin_prefs)

    ## Instantiate schedules for camps
    OlderSchedule = Schedule('Older Camp Schedule', OlderCamp.cabin_list, PERIODS, ACTIVITIES, LOCATIONS)
    YoungerSchedule = Schedule('Younger Camp Schedule', YoungerCamp.cabin_list, PERIODS, ACTIVITIES, LOCATIONS)

    ## Run draft for all activity periods
    for i in range(PERIODS):
        YoungerSchedule.draft()
        OlderSchedule.draft()
        

    ''' Uncomment to print schedules'''
    #printSchedule(YoungerSchedule)
    #printSchedule(OlderSchedule)


    '''Uncomment to view  open activities'''
    #YoungerSchedule.print_open_activities()
    #OlderSchedule.print_open_activities()

    '''Export schedules to xlxs files'''
    export_Schedule(YoungerSchedule, 'Younger-Schedule.xls')
    export_Schedule(OlderSchedule, 'Older-Schedule.xls')

    '''Uncomment to print cabins which had suboptimal assignments'''
    print(YoungerSchedule.sad_cabins)
    print(OlderSchedule.sad_cabins)

if __name__ == "__main__":
    main()
