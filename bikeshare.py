import time
import pandas as pd
import numpy as np

# load the files
CITY_DATA = {
    'chicago':'chicago.csv',
    'new york city':'new_york_city.csv',
    'washington':'washington.csv'
}

def input_city():
    # find out which city we want to look at
    print(' ')
    print('Welcome to the best place to learn about US Bikeshare data!')
    print(' ')
    print('First, we need to select which city you\'d like to analyze')
    print(' ')
    print('Chicago: 1')
    print('New York City: 2')
    print('Washington: 3')
    print(' ')
    city = input('Please type the number of the city you\'re interested in: ')
    while True:     # we use a while loop to catch unexpected user inputs
            if city == '1':
                print('The Windy City is beautiful this time of year. Great choice!')
                return 'chicago'
            if city == '2':
                print('NYC huh? Not my first pick, but I respect it. New York City coming up!')
                return 'new york city'
            if city == '3':
                print('Washington? Really...? I don\'t approve. But I suppose we can run with it...')
                return 'washington'
            else:     # the else allows us to keep trying until we hit an acceptable input
                print('I hate to be a bother but would you mind using the numbers 1, 2, or 3?')
                print('1, 2, and 3 correspond to Chicago, NYC, or Washington, respectively')
                city = input('Please type the number of the city you\'re interested in: ')
    return city

def which_filters():
    # find out which filter the user would like to apply
    print(' ')
    print('Anyway, now that we have the city, would you like to filter the data by month or day of the week?')
    print(' ')
    filter = input('You can reply: "month", "day", or "none" depending on your preference: ')
    print(' ')
    filter = filter.lower()

    while True:
        if filter == "month":
            print(' ')
            print('Fantastic news! We shall indeed filter the data by month!')
            return 'month'
        if filter == "day":
            print(' ')
            print('Phenomenal. We will filter by day of the week.')
            return 'day_of_week'
        elif filter == "none":
            print(' ')
            print('Alright, kind of lame, but no filter will be applied to the data.')
            return "none"
        filter = input('Hmm. Please choose "month", "day", or "none": ').lower()

def month_data(m):
    # to figure out which month the user would like
    if m == 'month':
        print(' ')
        month = input('Ahh, so, which month would you like? We have January, February, March, April, May, or June: ')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('So close! But please type "January", "February", "March", "April", "May", or "June": ')
        return month.strip().lower()
    else:
        return 'none'

def day_data(d):
    # to figure out which day of the week the user would like
    if d == 'day_of_week':
        print(' ')
        day = input('Ahh, so, which day would you prefer? We can offer you any of the 7 days of the week: ')
        while day.lower().strip() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input('So close! But please type "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", or "Sunday": ')
        return day.lower().strip()
    else:
        return 'none'

def load_data(city):
    # time to load the data
    print(' ')
    print('Let me run to the back and grab that data for you.')
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    return df

def time_filters(df, time, month, day):
    # first we filter by month, then by day of the week
    print('Data loaded. Now computing statistics... \n')
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if time == 'day_of_week':
        days = ['Monday', 'Tuesday',
        'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    return df

def pop_month(df):
    # asking for the most commmon month in the filtered data
    print('Question 1, let\'s look at popular times of travel.')
    print('What is the most common month for travel?')
    m = df.month.mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    pop_month = months[m - 1]
    return pop_month

def pop_day_of_week(df):
    # same idea as month but with most common day of the week
    print('What about the most common day of the week?')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def pop_hour(df):
    # same idea as month but with most common hour
    print('How about the most common hour of the day?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]

def common_start_end_trip(df):
    # here we use similar code to find the most stations
    print('Question 2, let\'s look at popular stations and trips.')
    print('What\'s the most common starting station?')
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print(start_station)
    print('How about the most common ending station?')
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    print('And what about the most popular trip in general?')
    common_trip = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    return start_station, end_station, common_trip

def trip_duration(df):
    # looking for travel time as defined by end minus start times
    print('Question 3, let\'s check out trip durations.')
    print('So what about trip duration? What are the total travel and average travel times?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split()[0]
    print('The total travel time was ' + total_days + ' days')
    print('The average travel time was ' + avg_days + ' days')
    return total_ride_time, avg_ride_time

def user_info(df):
    # looking for the count of each user type
    print('Question 4, what about the users? What\'s the count of each type?')
    return df['User Type'].value_counts()

def user_gender(df):
    # looking for count of male and female users
    try:
        print('So what is the gender breakdown amongst users?')
        return df['Gender'].value_counts()
    except:
        print('Sorry, there is no gender data for Washington...')

def birth_year(df):
    # looking for early, late, and most common birth years
    try:
        print('What about the birth years of users?')
        early = np.min(df['Birth Year'])
        print ("\nThe earliest birth year is " + str(early))
        late = np.max(df['Birth Year'])
        print ("The latest birth year is " + str(late))
        most_common= df['Birth Year'].mode()[0]
        print ("The most common year of birth is " + str(most_common))
        return early, late, most_common
    except:
        print('Hmm, sorry - no birth year data available for your selected filters')

def process(i, df):
    # calculate how long each stat takes to compute by subtracting start time from current time
    start_time = time.time()
    which_function = i(df)
    print(' ')
    print(' ')
    print(which_function)
    print("This calculation only took %s seconds!!" % (time.time() - start_time))
    print(' ')

def raw_data(df):
    # show raw data that was used to compute stats 5 lines at a time
    row_index = 0
    more_data = input("So. Would you like to see some of the raw data? Please type 'yes' or 'no': ").lower()
    while True:
        if more_data == 'no':
            return
        if more_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        more_data = input("This is crazy, but do you want to see even more data?! Please type 'yes' or 'no': ").lower()

def main():
    # runs calculations to answer the questions presented for the user's city
    city = input_city()
    df = load_data(city)
    filter = which_filters()
    month = month_data(filter)
    day = day_data(filter)

    df = time_filters(df, filter, month, day)
    raw_data(df)

    list_of_functions = [pop_month, pop_day_of_week, pop_hour, common_start_end_trip, trip_duration, user_info, user_gender, birth_year]

    # adds the time to compute each stat
    for i in list_of_functions:
        process(i, df)

    # user option to restart the whole thing - maybe we should thank the user for using our analysis??
    restart = input("\n * Would you like to do it again and perform another analysis? Type \'yes\' or \'no\'.\n")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        main()

if __name__ == '__main__':
    main()
