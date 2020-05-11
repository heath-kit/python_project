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
        city = input("\nWhat city do you want to filter by (New York City, Chicago or Washington)? \n")
        if city not in ('New York City', 'Chicago', 'Washington'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhat month do you want to filter by (January, February, March, April, May, June, or All? \n")
        if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhat day do you want to filter by (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All)?\n")
        if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'):
            print("Sorry, I didn't catch that. Try again.")
            Continue
        else:
            break

    print('-'*80)
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
    # read the data from the appropriate city file into a DataFrame
    city = city.lower()
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #day_of_week is deprecated in pandas .23 and greater

    # filter by month if a month was given, else no filter for month will be used
    if month != 'All':
   	 	# use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    	# apply the month filter and create a new dataframe
        df = df[df['month'] == month]

    # filter by day of week if one was given, else no filter for DOW will be used
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip pairs."""

    print('\nCalculating The Most Popular Stations and Trip Pairs...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print('Most commonly used starting station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print('Most commonly used ending station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    trip_with_counts = df.groupby(['Start Station','End Station']).size().reset_index(name = 'trips')
    sort_trips = trip_with_counts.sort_values('trips', ascending = False)
    start_station = sort_trips['Start Station'].iloc[0]
    end_station = sort_trips['End Station'].iloc[0]
    print('Most commonly used combination of start station and end station for trips:', start_station, " & ", end_station)

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Durations...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('Total of travel time:', round(total_travel_time/86400), " Days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', round(mean_travel_time/60), " Minutes")

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender types:\n', gender_types)
    except KeyError:
        print("\nGender types: No data available for this city or month.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('\nEarliest birth year:', int(earliest_year))
    except KeyError:
        print("Earliest birth year: No data available for this city or month.")

    try:
        most_recent_year = df['Birth Year'].max()
        print('Most recent birth year:', int(most_recent_year))
    except KeyError:
        print("Most recent birth year: No data available for this city or month.")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('Most common birth year:', int(most_common_year))
    except KeyError:
        print("Most common birth year: No data available for this city or month.")

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Display all the stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # See if user wants to see some of the data
        print_data = input("Would you like view five rows of your filtered data for this city (yes or no)? ").lower()
        start_idx = 0

        while start_idx <= df.index[-1]:    # made sure not to get an index out of range
            print(df.iloc[start_idx:start_idx + 5])
            start_idx += 5
            if start_idx > df.index[-1]:
                print("\n** End of File **")
                break
            print_data = input("Would you like view another five rows (yes or no)? ").lower()
            if print_data.lower() != 'yes':
                break

        # Ask user if they want to start over again
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
