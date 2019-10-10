import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


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
    while True:
            city = input('\nEnter name of the city to analyze from (chicago, New York City, Washington): ')
            city = city.lower().strip()
            if city in ['chicago', 'new york city','washington']:
                break
            else:
                print('\nIncorrect input try again')


    # get user input for month (all, january, february, ... , june)
    while True:
            month = input('\nEnter name of month you wnat to analyze from January to June or all : ')
            month = month.lower().strip()
            if month in ['all','january', 'february','march','april','may','june']:
                break
            else:
                print('\nIncorrect input try again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('\nEnter name of day you wnat to analyze from Monday to Sunday or all : ')
            day = day.lower().strip()
            if day in ['all','sunday', 'monday','tuesday','wednesday','thursday' ,'friday' ,'saturday']:
                break
            else:
                print('\nIncorrect input try again')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name



    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the months list to get the corresponding int

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost popular month was: ', popular_month)
    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('\nMost popular day of the week was: ', popular_day_of_week)
    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['start_hour'].mode()[0]
    print('\nMost popular start hour was: ', popular_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost popular start station was: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost popular end station was: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = '('+df['Start Station']+') to ('+df['End Station']+')'
    popular_trip = df['trip'].mode()[0]
    print('\nMost popular trip was: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60
    hours_total_travel_time = int(total_travel_time // 60)
    minutes_total_travel_time = int(total_travel_time % 60)
    print('\nTotal travel time was: {} hours and {} minutes '.format(hours_total_travel_time, minutes_total_travel_time))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    minutes_mean_travel_time = int(mean_travel_time // 60)
    seconds_mean_travel_time = int(mean_travel_time % 60)
    print('\nMean travel time was: {} minutes and {} seconds '.format(minutes_mean_travel_time, seconds_mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def value_counts_printer(sr):
    """Displays all possible value in a column and thier occurence"""
    vc_sr = sr.value_counts()
    for i in range(vc_sr.size):
        print('\nThe number of {}s was : {}'.format(vc_sr.index[i], vc_sr.values[i]))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    value_counts_printer(df['User Type'])

    # Display counts of gender, try and except to account for wahington's data
    try:
        value_counts_printer(df['Gender'])
    except Exception as e:
        print('\nGender data is not available')



    # Display earliest, most recent, and most common year of birth, try and except to account for wahington's data
    try:
        print('\nEarliest year of birth was: ', int(df['Birth Year'].min()))
        print('\nMost recent year of birth was: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth was: ', int(df['Birth Year'].mode()[0]))
    except Exception as e:
        print('\nBirth year data is not available')





    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data upon user request"""
    i = 0
    q_text = ' '
    while True:
        restart = input('\nWould you like to see{}5 lines of raw data? Enter yes or no.\n'.format(q_text))
        q_text = ' another '
        if restart.lower() != 'yes':
            break
        print(df[i:i+5])
        i = i+5






def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        unmodified_df = df.copy()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(unmodified_df)


        restart = input('\nWould you like to run another query? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
