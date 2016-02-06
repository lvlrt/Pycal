#!/usr/bin/python
"""
PYCAL v1.01
changelog:
-

TODO view met de hele maand -> cal..
TODO kleuren systeem voor iets gebruiken
TODO ondersteuning voor verschillende agenda's
TODO een -C functie voor de config file... en dan het absolute pad
TODO beter aangeven waar hij de todo opslaagt en de config import ook doen voor vanaf de iphone
TODO bij add als er geen event is gegeven een goede error
TODO wat als er een false is? dus bij elk functiegebruik een false optie en een deftige error msg
TODO rm optie of replace optie? -> alleen event vervangen?
TODO sterretje of reoccuring
TODO update systeem uit gcal?
TODO balkjes interface voor ls?? (low prior)
"""
import os
import fileinput, sys
import datetime
from datetime import date
import sys
#TODO: include file met birthdays etc...
from config import *
#TODO :sterretje
def isnumber(testval):
    try: 
        int(testval)
        return True
    except ValueError:
        return False
def extract_timepoints_fromline(line):
    return line[:line.find(" ")]
def extract_startendpoint(timepointsstring):
    #takes the argument and splits it if necesairy to te start and end.
    if timepointsstring.count("-") == 1:
        split_place = timepointsstring.find("-")
        start_point = timepointsstring[:split_place]
        end_point = timepointsstring[split_place+1:]
    else:
        print("Incorrect number of times specified")
        return timepointsstring, timepointsstring;
        #fixed here
    return start_point, end_point;
def extract_daymonthyear(datestring):
    #takes the datestring and turns it into day month year
    #00.00.00 00.00 00
    day=""
    month=""
    year=""
    datearray = datestring.split(".")
    len_datearray=len(datearray)
    if len_datearray < 4:
        day = datearray[0]
    else:
        print("Too much dots in date specification")
        return False;
    if len_datearray > 1:
        month = datearray[1]
    if len_datearray == 3 :
        year = datearray[2]
    return day, month, year;
def extract_hourminutes(hourminutesstring):
    #takes a format of 0000 and extracts an hour and minutes from it.
    hour = hourminutesstring[:2]
    minutes = hourminutesstring[2:]
    return hour, minutes;
def fill_zero(x):
    if len(x) == 1:
        x = "0"+x
    return x;
def create_date(day, month, year):
    day= str(day)
    if len(day) == 1:
        day = "0" + day
    month =str(month)
    if len(month) ==1:
        month = "0"+ month
    year = str(year)
    day = fill_zero(day)
    month = fill_zero(month)
    return day + '.' + month + '.' + year;
def checkday(day):
    if 0 < day < 32:
        return True;
    else:
        print("ERROR: Day is out of boundries")
        return False;
def checkmonth(month):
    if 0 < month < 13:
        return True;
    else:
        print("ERROR: Month is out of boundries")
        return False;    
####Function Usage beyond this line
def checkandfill_blankdate(day, month, year, time, followday, followmonth, followyear, followtime):
    #input check, bij elke ingevulde waarde -> defenities van maken
    start = False
    if followday == "":
        #in geval van start, anders is het gewoon de startdatum in het end piping
        start = True
        followdate = datetime.datetime.now()
        followday = int(followdate.strftime("%d"))
        followmonth = int(followdate.strftime("%m"))
        followyear = int(followdate.strftime("%y"))
        followtime = 0
    #Hier heb ik zowiso ne followtime van alles.
    time = int(time)
    followtime = int(followtime)
    if year =="":
        if month == "":
            if day == "":
                if time <= followtime:
                    #extra if
                    if start != True:
                        followday = followday+1
                day = followday
            else:
                time = int(time)
                if isnumber(day):
                    day = int(day)
                    if checkday(day) == False:
                        return False;
                    if day < followday:
                        followmonth= followmonth + 1
                else:
                    return False;
            month = followmonth
            if month > 12:
                month = 1
                followyear = followyear + 1
        else:
            time = int(time)
            if isnumber(day):
                day = int(day)
                if checkday(day) == False:
                    return False;
            else:
                return False;
            if isnumber(month):
                month = int(month)
                if checkmonth(month) == False:
                    return False;
                if month < followmonth:
                    followyear= followyear + 1
            else:
                return False;
        nextmonth = month + 1
        nextmonth_year = followyear
        if nextmonth > 12:
            nextmonth = 1
            nextmonth_year = nextmonth_year + 1
        if day > (date(nextmonth_year, nextmonth , 1) - date(followyear, month, 1)).days:
            day = 1
            month = month + 1
        if month > 12:
            month = 1
            followyear = followyear + 1

        year = followyear
    else:
        if isnumber(day):
            day = int(day)
            if checkday(day) == False:
                return False;
        else:
            return False;
        if isnumber(month):
            month = int(month)
            if checkmonth(month) == False:
                return False;
        else:
            return False;
        if isnumber(year):
            year = int(year)
        """print(day, month, year, time)
        print(followday, followmonth, followyear, followtime)
        continue_test = False
        if year > followyear:
            continue_test = True
        elif year == followyear:
            if month > followmonth:
                continue_test = True
            elif month == followmonth:
                if day > followday:
                    continue_test = True
                elif day == followday:
                    if time > followtime:
                        continue_test = True
        if continue_test!=True:
            print("ERROR: Event ends before it starts")
            return False;"""
    return day, month, year;
def extract_time(timestring):
    #takes the timesrting and makes it a good formatted (0000) time
    len_timestring = len(timestring)
    if len_timestring ==4:
        time = timestring
    elif len_timestring==2:
        time = timestring + "00"
    elif len_timestring==3:
        time = "0" + timestring
    elif len_timestring == 1: 
        time = "0" + timestring + "00"
    elif len_timestring==0:
        time = "0000"
    else: 
        print("Specified time-format too long")
        return False;
    return time;
def extract_datetime(pointstring):
    #datetimestring = uit het eerste argument alles voor de -
    #this function processes everything to a Type of event, day, month, year and time
    pointstring_count=pointstring.count(":")
    if pointstring_count==0:
        time = extract_time("")
        date = pointstring
    elif pointstring_count==1:
        split_place = pointstring.find(":")
        date = pointstring[:split_place]
        time = extract_time(pointstring[split_place+1:])
    else:
        print("Incorrect format of time")
        return False;
    return date, time;
def filter_lines_date(calendar, day, month, year, ask_date):
    ls = []
    f = open(calendar, 'r')
    line_nr = 1
    for line in f:
        add = False
        add_start = False
        check = False
        #TODO: here it is not possible to execute the line beneath
        (start_point, end_point) = extract_startendpoint(extract_timepoints_fromline(line))
        (start_date, start_time) = extract_datetime(start_point)
        (end_date, end_time) = extract_datetime(end_point)
        (start_day, start_month, start_year) = extract_daymonthyear(start_date)
        (end_day, end_month, end_year) = extract_daymonthyear(end_date)
        event = line[line.find(" ")+1:-1]
        if isnumber(start_day):
            if isnumber(end_day):
                if isnumber(start_month):
                    if isnumber(end_month):
                        if isnumber(start_year):
                            if isnumber(end_year):
                                f_start_day = int(start_day)
                                f_end_day = int(end_day)
                                f_start_month = int(start_month)
                                f_end_month = int(end_month)
                                f_start_year = int(start_year)
                                f_end_year = int(end_year)
                                check = True
        if check == True:
            if f_start_year < year < f_end_year:
                add=True
            else:
                if f_start_year < year:
                    add_start=True
                elif f_start_year == year:
                    if f_start_month < month:
                        add_start=True
                    elif f_start_month == month:
                        if f_start_day <= day:
                            add_start=True
                if add_start==True:
                    if f_end_year > year:
                        add=True
                    elif f_end_year == year:
                        if f_end_month > month:
                            add=True
                        elif f_end_month == month:
                            if f_end_day >=day:
                                add=True
        else:
            print("error in file: line:" + str(line_nr))
        if add==True:
            ls.append([line_nr, start_date, start_time, end_date, end_time, event])
            high_line_nr = line_nr
        line_nr = line_nr+1
    ls.sort(key=lambda x: x[4])
    ls.sort(key=lambda x: x[3])
    ls.sort(key=lambda x: x[2])
    ls.sort(key=lambda x: x[1])
    len_ls=len(ls)
    ls_nr = 0
    #TODO
    #efficienter hieronder door vergelijking te maken met huidige datum om zeveel mogelijk weg te laten, de ls[ls_nr] vervangen door kortere versies en ev de tekeningen erbij steken
    while ls_nr < len_ls:
        if ls[ls_nr][1] == ls[ls_nr][3]:
            print(str(ls[ls_nr][0]) + " "*(len(str(high_line_nr))-len(str(ls[ls_nr][0]))) +"| " + ls[ls_nr][2] + "-" + ls[ls_nr][4] + " |" + ls[ls_nr][5])
        elif ask_date == ls[ls_nr][1]:
            print(str(ls[ls_nr][0]) + " "*(len(str(high_line_nr))-len(str(ls[ls_nr][0]))) + "| " + ls[ls_nr][2] + "-" + ls[ls_nr][3] + ":" + ls[ls_nr][4] + " |" + ls[ls_nr][5])
        elif ask_date == ls[ls_nr][3]:
            print(str(ls[ls_nr][0]) + " "*(len(str(high_line_nr))-len(str(ls[ls_nr][0]))) + "| " + ls[ls_nr][1] + ":" + ls[ls_nr][2] + "-" + ls[ls_nr][4] + " |" + ls[ls_nr][5])
        else:
            print(str(ls[ls_nr][0]) + " "*(len(str(high_line_nr))-len(str(ls[ls_nr][0]))) + "| " + ls[ls_nr][1] + ":" + ls[ls_nr][2] + "-" + ls[ls_nr][3] + ":" + ls[ls_nr][4] + " |" + ls[ls_nr][5])
        ls_nr += 1
    f.close()
    return; 
def list_events_day(calendar, date):
    if date == "today":
        translatedate = datetime.datetime.now()
        day =int(translatedate.strftime("%d"))
        month=int(translatedate.strftime("%m"))
        year=int(translatedate.strftime("%y"))
        date = create_date(day, month, year)
        print("Today ~" + translatedate.strftime("%a")  + " " + date + ':')
        filter_lines_date(calendar, day, month, year, date)
    elif date == "0":
        translatedate = datetime.datetime.now()
        day =int(translatedate.strftime("%d"))
        month=int(translatedate.strftime("%m"))
        year=int(translatedate.strftime("%y"))
        date = create_date(day, month, year)
        print("Today ~" + translatedate.strftime("%a")  + " " + date + ':')
        filter_lines_date(calendar, day, month, year, date)
    elif date[0] == "+":
        add = int(date[1:])
        translatedate = datetime.datetime.now()+ (datetime.timedelta(days=1))*add
        day =int(translatedate.strftime("%d"))
        month=int(translatedate.strftime("%m"))
        year=int(translatedate.strftime("%y"))
        date = create_date(day, month, year)
        print("+"+ str(add) + " ~" + translatedate.strftime("%a")  + " " + date + ':')
        filter_lines_date(calendar, day, month, year, date)
    elif date[0] == "-":
        add = int(date[1:])
        translatedate = datetime.datetime.now()- (datetime.timedelta(days=1))*add
        day =int(translatedate.strftime("%d"))
        month=int(translatedate.strftime("%m"))
        year=int(translatedate.strftime("%y"))
        date = create_date(day, month, year)
        print("-"+ str(add) + " ~" + translatedate.strftime("%a")  + " " + date + ':')
        filter_lines_date(calendar, day, month, year, date)
        
    ###hier een range met - en dat laten oplossen door de pointstrings en dan inrementies met de translatedate en vergelijken
    elif date.count("-") == 1:
        split_place = timepointsstring.find("-")
        start_point = timepointsstring[:split_place]
        end_point = timepointsstring[split_place+1:]
    
    else:
        (start_date, start_time) = extract_datetime(date)
        (start_day, start_month, start_year) = extract_daymonthyear(start_date)
        day, month, year = checkandfill_blankdate(start_day, start_month, start_year, start_time, "", "", "", "")
        date = create_date(day, month, year)
        print(date + ':')
        ##TODO hier de date naar de echte date omvormen
        filter_lines_date(calendar, day, month, year, date)
    """elif date = "monday":

    elif date = "mon":

    elif date = "tuesday":

    elif date = "tue":

    elif date = "wednesday":

    elif date = "wed":

    elif date = "thurday":

    elif date = "thu":

    elif date = "friday":

    elif date = "fri":
    
    elif date = "saturday":

    elif date = "sat":

    elif date = "sunday":

    elif date = "sun":
    else:
    """
    return;
def add_event(date, event, calendar):
    (start_point, end_point) = extract_startendpoint(date)
    (start_date, start_time) = extract_datetime(start_point)
    (end_date, end_time) = extract_datetime(end_point)
    (start_day, start_month, start_year) = extract_daymonthyear(start_date)
    (end_day, end_month, end_year) = extract_daymonthyear(end_date)
    start_day, start_month, start_year = checkandfill_blankdate(start_day, start_month, start_year, start_time, "", "", "", "")
    start_date=create_date(start_day, start_month, start_year)
    end_day, end_month, end_year = checkandfill_blankdate(end_day, end_month, end_year, end_time, start_day, start_month, start_year, start_time)
    end_date=create_date(end_day, end_month, end_year)
    #onderstaande writen naar file
    append = start_date + ":" + start_time + "-" + end_date + ":" + end_time + " " + event
    print("ADDED: " +"'"+ append + "'" + " to " + calendar)
    print("ON LINE:")
    os.system('echo $(($(wc -l < ' + calendar+ ')+1))')
    f = open(calendar, "a")
    f.write(append + "\n")
    f.close()
    
def delete_event(calendar, line_nr):
    start= sys.argv[2]
    start = int(start)
 
    for line in fileinput.input(calendar, inplace=1, backup='.orig'):
        if start <= fileinput.lineno() <start+1:
            pass
        else:
            print(line[:-1])
    fileinput.close()

    print("DELETED:")
    os.system('grep -F -x -v -f '+ calendar + ' ' +calendar+'.orig')
    
####SCRIPT beyong this line
len_sysargv = len(sys.argv)
if len_sysargv == 1:
    list_events_day(calendarfile , "today")
    #print today as in day format
    
elif sys.argv[1] == "ls":
    if len_sysargv == 2:
        #list of all coming events, measures the widht and if a print line exceeds it will substract it from the amount of screenspace left + 1 line left for the new command
        #start by printing the next 5
        list_events_day(calendarfile , "today")
    elif len_sysargv == 3:
        list_events_day(calendarfile , sys.argv[2])
    else:
        print("too much arguments")
    """elif sys.argv[1] = "list":
    #same as above"""
   
elif len_sysargv != 2:
    if sys.argv[1] == "a":
        arg_event = 3
        event = sys.argv[arg_event]
        arg_event = 4
        while arg_event < len_sysargv:
            event = event + " " + sys.argv[arg_event]
            arg_event = arg_event+1
        add_event(sys.argv[2], event, calendarfile)
        #add a new event
        # 2 is zowiso de tijd en 3 is de event en dat aan elkaar plakken in ne file, ni zo moeilijk?
        """elif sys.argv[1] = "add":

        elif sys.argv[1] = "d":

        elif sys.argv[1] = "day":

            #Whole day        
            start_hour = 0000
            #function above check that the time is bigger -> otherwise its the next day
            end_hour = 0000    """
    elif sys.argv[1] =="rm":
        line_nr=sys.argv[2]
        delete_event(calendarfile, line_nr)