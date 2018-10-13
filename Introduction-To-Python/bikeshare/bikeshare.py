import time
import pandas as pd
import numpy as np
import datetime as dt
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


MONTH_DATA = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # variables for storing the answer of each query 
    city = ""
    month = -1          # -1 is a dummy value to consider the option that month filter is not selcetd
    day=-1              # -1 is a dummy value to consider the option that day filter is not selcetd
    timeFilter = ""

    #some expected answers designed as a list to check for the answer of the user
    timeOptions = ['month', 'day', 'both', 'none']
    monthOptions = ["january", "february", "march", "april", "may", "june"]

    # Welcoming the user
    print('\nHello! Let\'s explore some US bikeshare data!\n\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = (str(input(
                "Would you like to know more bike share infromation about Chicago, New York city,or Washington?\n"))).strip().lower()
            if(city in CITY_DATA):
                break
            else:
                print("\nBad answer, please choose city from the above ones")
        except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
        finally:
             print('-'*40)
    

    # asking for time filter type that is needed for the query
    while True:
            try:
                timeFilter = (str(input(
                    "Would you like to filter the data by month, day, both? Type none for no time filter\n"))).strip().lower()
                if(timeFilter in timeOptions):
                    break
                else:
                    print("\nBad answer, please choose correct time option")
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
            finally:
                print('-'*40)

    # get user input for month (all, january, february, ... , june)
    if(timeFilter == 'month' or timeFilter == 'both'):
        while True:
            try:
                month = (
                    str(input("Which month? please any month from January till June\n"))).strip().lower()
                if(month in monthOptions):
                    month = MONTH_DATA[month]
                    break
                else:
                    print("\nBad answer, please choose from the above choices")
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
            finally:
                print('-'*40)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if(timeFilter == 'day' or timeFilter == 'both'):
        while True:
            try:
                day = int(input("Which day? Please enter your answer in numbers (e.g.: 1=Monday)\n"))
                if (day>=1 and day<=7):
                    day-=1 #0-index because in date format Monday is 0.
                    break
                else:
                    print("\nBad answer, please choose from a number from 1 to 7 (e.g.: 1=Monday)")
            except ValueError :
                print("You entered your answer in characters so please choose a number (e.g.: 1=Monday)")
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
            finally:
                print('-'*40)
    print('\n')
    print('#'*130)
    return city, month, day

def loading_data(city):
    """
    Loading data by the city that is stated by the answers. 
    Args:
        (str) city - name of the city to analyze.
    Returns:
        df - Pandas DataFrame containing city data.
    """

    df = pd.read_csv('./{}'.format(CITY_DATA[city]))
    #removing the white spaces and lowercased the string in order to access the column weel
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    #wrapping the time in data frame form object to datetime64 to get over the month and weekday easily.
    df['start_time'] = pd.to_datetime(df.start_time)
    df['end_time'] = pd.to_datetime(df.end_time)

    return df

def filtering_data(city,month, day):
    """
    Filtering data by month and day if applicable.

    Args:
        (str) city - name of the city to analyze.
        (int) month - the month in, int format, to filter by.
        (int) day - the day of week, int format, to filter by.
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = loading_data(city)

    if(day > -1):
        df = df[df.start_time.dt.weekday == day]

    if(month > -1):
        df = df[df.start_time.dt.month == month]

    return df

def getTheBest(df,query):
    """
    Getting the 5 best common start/end stations.

    Args:
        (pandas) df - Pandas DataFrame containing city data filtered by month and day
        (str) query - the type of station (start or end) that will be filtered with 
    """

    stations = df.groupby(query).start_station.count().sort_values(ascending=False).iloc[0:5]
    print('\n\t\tHere is the 5 most commonly used {}s'.format(query))
    print("-"*110)
    for i in range(5):
        name = stations.iloc[[i]].index[0]
        count = stations.iloc[[i]][0]
        print('{:55}{}'.format(name, count))
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time() 
    

    # display most commonly used start station
    getTheBest(df,'start_station')


    # display most commonly used end station
    getTheBest(df,'end_station')

    # display most frequent combination of start station and end station trip

    groups = df.groupby(['start_station', 'end_station']).user_type.count().sort_values(ascending=False).iloc[0:5]
    print(groups.iloc[[2]].index[0])
    print('\n\t\tHere is the 5 most commonly  start station')
    print("  Start station\t\t\t\t\t  End station\t\t\t\tNumber of times")
    print("-"*110)


    for i in range(5):
        station_tuple = groups.iloc[[i]].index[0]
        start_station = station_tuple[0]
        end_station = station_tuple[1]
        count = groups.iloc[[i]][0]
        print('{:47}{:47}{}'.format(start_station, end_station, count))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('#'*130)

def trip_calculation(sum_seconds,query):
    """
    Calculating the trip durations.

    Args:
        (float) sum_seconds - sum of all trip durations represented in seconds.
        (str) query - the type of filtering that need to be applied on trip duration eg :(mean , sum ,min).
    """
    out = dt.timedelta(seconds=sum_seconds)
    seconds = sum_seconds
    days = out.days
    hours = seconds/60/60
    mins = seconds/60

    print("\n\t\t\t\tHere is the {} of all trips durations".format(query))
    print("-"*110)
    print(" Num days: \t\t\t\t\t{} day/s\n Num hours: \t\t\t\t\t{} hour/s\n Num mins: \t\t\t\t\t{} min/s\n Num seconds: \t\t\t\t\t{} seconds\n".format(
        days, hours, mins, seconds))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    sum_seconds = int(df.trip_duration.sum())
    trip_calculation(sum_seconds,'sum')
    
    # display mean travel time
    sum_seconds = int(df.trip_duration.mean())
    trip_calculation(sum_seconds, 'average')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('#'*130)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

   # Display counts of user types
    grouping_users = df.groupby(['user_type']).user_type.count()
    customer   = grouping_users.loc['Customer']
    subscriber = grouping_users.loc['Subscriber']
    print("\n\t\t\t\t\tHere is the types of users")
    print("-"*110)
    print(" Customer: \t\t\t\t\t{}\n Subscriber: \t\t\t\t\t{}".format(
        customer, subscriber))


    # Display counts of gender
    if('gender' in list(df.columns)):
        grouping_users = df.groupby(['gender']).user_type.count()
        male = grouping_users.loc['Male']
        female = grouping_users.loc['Female']
        print("\n\t\t\t\t\tHere is the gender of users")
        print("-"*110)
        print(" Male: \t\t\t\t\t\t{}\n Female: \t\t\t\t\t{}\n".format(male, female))
    
    if('birth_year' in list(df.columns)):
        # Creating the age column
        now = dt.datetime.now()
        df['age'] = now.year-df['birth_year']
    
        # Display the mean of all ages
        print("\n\n\t\t\t\t\tHere is the gender of users: {}\n".format(int(df.age.mean())))
        print("-"*110)

        # Display most common ages of users
        print("\n\t\t\t\t\tHere is the 5 most common ages of users")
        ages = df.groupby('age').age.count().sort_values(ascending=False).iloc[0:5]
        print("-"*110)
        for i in range(5):
            age = int(ages.iloc[[i]].index[0])
            count = ages.iloc[i]
            print("{:55}\t\t{}".format(age,count))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('#'*130)


def printing_helper(query, max, min,sorted):
    """
    Formatting style of string to print the max and min values of time stats.

    Args:
        (str) query - the type of query (month or day or hour) that will be filtered with
        (int) max - the max value of sorted dataSeries
        (int) min - the min value of sorted dataSeries
        (panda.DataSeries) sorted - sorted dataseries of start_time column by specific value eg: (month or day or hour)
    """
    max_count = sorted.iloc[0]
    min_count = sorted.iloc[sorted.size-1]
    print("\n\t\t\tHere is most common {} and the least one".format(query))
    print("-"*110)
    print(" Most : \t\t{}\t\twtih freq\t\t{}".format(max, max_count))
    print(" Least : \t\t{}\t\twtih freq\t\t{}".format(min, min_count))


def time_stats(city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #loading the data frame that is specified by the city that is already choosen
    df = loading_data(city)

    # display the most common month and the least one
    sorted_months = (df.start_time.dt.month).value_counts(
    ).sort_values(ascending=False)
    
    # in case that the list is <5 and this means there is some months not occured in the list but i don't have to get it.
    size = sorted_months.size
    max = calendar.month_abbr[sorted_months.index[0]]
    min = calendar.month_abbr[sorted_months.index[size-1]]
    printing_helper('month', max, min, sorted_months)

    # display the most common day of week and the least one
    sorted_days = (df.start_time.dt.weekday_name).value_counts(
    ).sort_values(ascending=False)
    size = sorted_days.size
    max = sorted_days.index[0]
    min = sorted_days.index[size-1]
    printing_helper('day', max, min,sorted_days)

    # display the most common start hour and the least one
    sorted_hours = (df.start_time.dt.hour).value_counts(
    ).sort_values(ascending=False)
    size = sorted_hours.size
    max = sorted_hours.index[0]
    min = sorted_hours.index[size-1]
    printing_helper('hour', max, min,sorted_hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('#'*130)


def main():
    while True:
        start_time = time.time()
        city, month, day = get_filters()
        df = filtering_data(city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        time_stats(city)

        print("\nThese all operations took %s seconds." % (time.time() - start_time))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
