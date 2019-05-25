import os
from flask import Flask, request, jsonify
import json
from datetime import datetime, date, time
from sklearn.externals import joblib

app = Flask(__name__)

@app.route("/info", methods=['GET'])
def info():
    print ("Request GET received")
    return "Request GET received"


@app.route("/prediction", methods=['POST'])
def prediction():
    '''
    Calculate the prediction to park in a parking (id), in a especific hour (time) in a specific day (date)
    Parameters:
    id : The id of the parking
    date : The day to do the prediction in format 'yyyy-dd-mm'
    time : The hour to do the prediction in format 'hh:mm:ss'
    :return: int
    '''

    data = json.loads(request.data)
    id_parking = data['parkingId']
    date_to_prediction = data['date']
    time_to_prediction = data['time']

    date_to_prediction_array = date_to_prediction.split('-')

    year_to_prediction = int(date_to_prediction_array[0])
    month_to_prediction = int(date_to_prediction_array[1])
    day_to_prediction = int(date_to_prediction_array[2])

    #Time_zone 0-6, refers to the hours of day
    time_zone = calculate_time_zone(time_to_prediction)

    #Day of week is from 0 to 6, refers to (Monday =0, Tuesday=1, Wednesday =2, Thursday=3, Friday =4, Saturday =5, Sunday=6)
    day_of_week = day_week(year_to_prediction, month_to_prediction, day_to_prediction)

    #Working_day 0 = is not_working_day, 1 = is working day
    working_day = is_working_day(day_of_week, day_to_prediction, month_to_prediction)

    # Load file train method
    load_model = joblib.load('training_model.pkl')

    #Call to prediction model
    prediction = load_model.predict([[id_parking, time_zone, day_of_week, working_day]])

    #return "La Franja horaria es: "+str(time_zone)+", dia de la semana:"+str(day)+", ¿es laborable ? "+str(working_day)
    #return json.dumps({'predict': int(prediction[0])})
    return jsonify({'prediction': int(prediction[0])})


def calculate_time_zone(actual_time):
    '''
    Calculate the time_zone of the hour.
    # From 7 to 10: time_zone = 0
    # From 10 to 13: time_zone = 1
    # From 13 to 16: time_zone = 2
    # From 16 to 19: time_zone = 3
    # From 19 to 22: time_zone = 4
    # From 22 to 0: time_zone = 5
    # From 00 to 7: time_zone = 6
    :param actual_time:
    :return:
    '''


    actual_time_array=actual_time.split(':')
    actual_hour = time(int(actual_time_array[0]), int(actual_time_array[1]), int(actual_time_array[2]))
    time_zone = None

    #Declare our time_zones
    time_zone_1 = time(7, 0, 0)
    time_zone_2 = time(10, 0, 0)
    time_zone_3 = time(13, 0, 0)
    time_zone_4 = time(16, 0, 0)
    time_zone_5 = time(19, 0, 0)
    time_zone_6 = time(22, 0, 0)
    time_zone_7 = time(0, 0, 0)

    if time_zone_1 <= actual_hour < time_zone_2:
        time_zone = 0

    if time_zone_2 <= actual_hour < time_zone_3:
        time_zone = 1

    if time_zone_3 <= actual_hour < time_zone_4:
        time_zone = 2

    if time_zone_4 <= actual_hour < time_zone_5:
        time_zone = 3

    if time_zone_5 <= actual_hour < time_zone_6:
        time_zone = 4

    if time_zone_6 <= actual_hour < time_zone_7:
        time_zone = 5

    if time_zone_7 <= actual_hour < time_zone_1:
        time_zone = 6

    return time_zone


def day_week(year, month, day):
    '''
    Return the day of week of the date
    :param actual_date:
    :return:
    '''

    final_date = date(year, month, day)
    day_week = datetime.isoweekday(final_date)

    #Day_week from 0 to 6
    day_week = day_week - 1

    return day_week


def is_working_day(day_week, day_to_prediction, month_to_prediction):
    '''
    Return if the day is a working day or not
    :param day_week:
    :return:
    '''

    ##If is Saturday or Sunday is not working_day
    if day_week > 4:
        is_workday = 0
    #Else test if is a free day
    else:
        is_workday = is_free_day(day_to_prediction, month_to_prediction)

    return is_workday

def is_free_day(day_to_prediction, month_to_prediction):

    final_day = day_to_prediction
    final_month = month_to_prediction
    free_days=[]

    free_days.append(date(year=2019, month=1, day=1))
    free_days.append(date(year=2019, month=1, day=6))
    free_days.append(date(year=2019, month=2, day=28))
    free_days.append(date(year=2019, month=5, day=1))
    free_days.append(date(year=2019, month=8, day=15))
    free_days.append(date(year=2019, month=8, day=19))
    free_days.append(date(year=2019, month=9, day=8))
    free_days.append(date(year=2019, month=10, day=12))
    free_days.append(date(year=2019, month=11, day=1))
    free_days.append(date(year=2019, month=12, day=6))
    free_days.append(date(year=2019, month=12, day=8))
    free_days.append(date(year=2019, month=12, day=25))

    for day in free_days:
        if day.month == final_month and day.day == final_day:
            is_workday = 0
            return is_workday
        else:
            is_workday = 1

    return is_workday

if __name__ == "__main__":
    debug = False
    if os.getenv('DEBUG') == 'True':
        debug = True
    app.run(port=8085, host="0.0.0.0", debug=debug)
