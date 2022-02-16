import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June']
days =  ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('would you likse to see data for chicago, new york city, or washington?\n').lower()
    #check for city name validity
    while city not in(CITY_DATA.keys()):
        print('please input valid city name\n')
        city = input('would you likse to see data for chicago, new york city, or washington?\n').lower()
    #choose type of time filter
    Filter = input('would you like to filter data by month, day, both or not at all? Type "none" for no time filter\n').lower()
    #check for time filter validity
    check_Filter = ['month', 'day', 'both', 'none']
    while Filter not in(check_Filter):
        print('please input valid input.\n')
        Filter = input('would you like to filter data by month, day, both or not at all? Type "none" for no time filter\n').lower()
    if Filter == 'month':
        # get user input for month (all, january, february, ... , june)
        month = input('which month? January, February, March, April, May, or June?\n').title()
        while month not in(months):
            print('please input valid input.\n')
            month = input('which month? January, February, March, April, May, or June?\n').title()
        day = days
    elif Filter == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? \n').title()
        while day not in(days):
            print('please input valid input.\n')
            day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? \n').title()
        month = months
    elif Filter == 'both':
        month = input('which month? January, February, March, April, May, or June?\n').title()
        while month not in(months):
            print('please input valid input.\n')
            month = input('which month? January, February, March, April, May, or June?\n').title()
        day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? \n').title()
        while day not in(days):
            print('please input valid input.\n')
            day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday? \n').title()
    elif Filter == 'none':
        month = months
        day = days



    print('-'*40)
    return city, month, day, Filter


def load_data(city, month, day, Filter):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    filename = CITY_DATA.get(city)

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the Start Time column to month, day, and hour
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # set dates
    if Filter == 'month':
        df = df[df['month'] == month.title()]


    if Filter == 'day':
        df = df[df['day'] == day.title()]

    if Filter == 'both':
        df = df[df['month'] == month.title()]
        df = df[df['day'] == day.title()]


    return df


def time_stats(df, Filter):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month = df['month'].mode()[0]


    # display the most common day of week
    popular_day = df['day'].mode()[0]

    # display the most common start hour
    hour = df['hour'].mode()[0]
    count = df['hour'].count()
    print("Most common hour:{}, count:{}, Filter:{}".format(hour, count, Filter))
    if Filter == 'day' or Filter == 'both':
        print("Most common month:", common_month)
    if Filter == 'month' or Filter == 'both':
        print("Most common day:", popular_day)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, Filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most common start station:{}".format(common_start_station))


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most common end station:{}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("Most common end station:{}".format(frequent_combination).split("||"))
    count = df['Start Station'].count()
    print("count:{}, Filter:{}".format(count, Filter))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, Filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("total travel time:{}".format(total_travel))


    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("mean travel time:{}".format(mean_travel))
    count = df['Trip Duration'].count()
    print("count:{}, Filter:{}".format(count, Filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, Filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("counts of user types:{}".format(user_counts))


    # Display counts of gender
    if city == 'chicago' or city == 'new_york_city':
        gender_counts = df['Gender'].value_counts()
        print("counts of user types:{}".format(gender_counts))
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print("earliest_birth:{}, recent_birth:{}, common_birth:{}".format(earliest_birth, recent_birth, common_birth))
    count = df['Birth Year'].count()
    print("count:{}, Filter:{}".format(count, Filter))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    end_loc = 5
    while view_data == 'yes':
        print(df.iloc[start_loc:end_loc])
        start_loc += 5
        end_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display.lower() != 'yes':
            break


def main():
    while True:
        city, month, day, Filter= get_filters()
        df = load_data(city, month, day, Filter)

        time_stats(df, Filter)
        station_stats(df, Filter)
        trip_duration_stats(df, Filter)
        user_stats(df, city, Filter)
        show_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
