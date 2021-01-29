# Scheduling

A scheduling assistant built for YMCA Camp Thunderbird during the COVID-19 pandemic to assist with rapid schedule prototyping and deployment.

This repository contains everything you need to use python-based program "breezyschedule.py" to create optimized schedules for groups (or individuals with some tinkering).

<b>To use<b/>

Download/Install Python3

Clone this repository to your local machine.
```git clone https://github.com/ShepSims/BreezySchedule/"```

Add availible activities and cabins to respective arrays in BreezySchedule.py

Update Land Activity Preferences.xls with the group's preferences and save as xls.  

In a terminal shell cd'ed into the folder you cloned into

```source bin/activate```
```python3 -m BreezySchedule```


*Note that xlrd/xlwt does not support xlsx filetypes produced by Excel 2010 or newer so you'll need to convert them by clicking File/SaveAs in excel and selecting xls if you create a new file instead of using the provided "Land Activity Preferences.xls"*

<b> How it works<b/>

The core algorithmic processes live in the draft and assign methods of the Schedule class, comprehensively explained below for convenience.  


```
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
                best[cabin] = random.randint(0,10)

        ## Sort the cabins into order which prioritizes cabins who all agree on a top activity
        best = sorted(best.items(), key = lambda x: x[1], reverse = True)

        ## Assign each cabin one activity
        for cabin in best:
            self.assign_activity(cabin[0])
```
If you do not understand what is going on here and would like to, please familiarize yourself with the data structures of each class then continue reading below
```
best = {}
for cabin in self.schedule:
   if self.get_top_choice(cabin) in cabin.prefs:
        best[cabin] = cabin.prefs[self.get_top_choice(cabin)]
   else:
        best[cabin] = random.randint(0,10)
```
Draft creates an empty dictionary called "best" then goes through all cabins in the schedule getting their top activity preference's weight, where weight is defined to be 
  1.  The placement of the activity in the cabins preference list if they have not yet expirienced any draft rounds where they did not get their first pick
  2.  The increased weight of the next-best activity if a cabin is unsuccessful in securing a top pick at any point
  3.  A random integer, if there are no longer any activities on the cabin's list which have open activity location times
  
Note:  This does NOT choose the activities for each cabin, but creates a dictionary with each cabin as keys and maximum weight of activities as its value
  
```
best = sorted(best.items(), key = lambda x: x[1], reverse = True)
```
The best dictionary is converted into a sorted list where cabins with the highest weights are first and lowest weights are last.  This represents giving preference 
to cabins who have either had their preferences boosted due to unavailable previous choices or noted that they greatly preferred certain activities as a cabin.

```
for cabin in best:
            self.assign_activity(cabin[0])
```
Loop through the cabins, now in order by weight, and assign an activity to each.
After the last assignment of each draft round, each cabin will have added one activity to any period in its schedule.  
The period which is filled is determined by the assign method
  
```
def assign(self, cabin, activity, location, last_location_to_try = True):
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
             .
             .
             .
```
I believe that there is likely a slicker way to do this, but for the time being this works perfectly for its intended use!
```
def assign(self, cabin, activity, location, last_location_to_try = True):
```
Draft passes a cabin and activity to assign_activity, then each location is passed from assign_activity individually as a parameter to assign  
```
if self.open_locations[activity_period][location] != 0:
```
If any activity period and location combination have openings, further conditions are checked
```
if activity_period == 0 and self.schedule[cabin]['A-Day']['Period One'] == None and not activity == 'Pottery': # Day Camp uses pottery during A-Day Period 1
                    self.schedule[cabin]['A-Day']['Period One'] = activity
                    self.open_locations[activity_period][location] -= 1
                    if activity in cabin.prefs:
                        cabin.prefs.pop(activity)
```
The first line here ensures that the activity period is free for the cabin, then, since day camp uses pottery during this period, we ensure that pottery is NOT being assigned to any cabin during this time slot
If all conditions are correctly met to be allowed to assign, the activity is added to the cabins schedule, then that location is marked as used in self.open_locations and the activity is removed from the cabin's preference list, since we don't want to reassign this activity to this cabin.
```
if activity_period == 5 and last_location_to_try == True:
                if activity in cabin.prefs:
                    increase_next_choice = cabin.prefs.pop(activity)/2
```
If all activity periods are checked and none are found to have acceptable scheduling conditions with the location, and this is the last location to check for the given activity, then determine increase increment of the weight of the current cabin's next activity preference so that they will have first* pick in the next round
```
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
```
Select the next best option for the current cabin based on their preferences and increase its weight.  If there is no next best option because all choices have been exhausted, store. In either case, return false so that assign_activity will run again and assign the cabin an activity. 
NOTE: This is stored and returned so that you can offer them a choice before other cabins if they would like to change their schedule.

                   
