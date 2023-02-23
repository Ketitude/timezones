from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from flask import Flask, request, jsonify

import datetime
import pytz

app = Flask(__name__)

@app.get('/timezone')
def get_timezone_endpoint():
    location = request.args.get('location')
    geolocator = Nominatim(user_agent="anyName")
    tf = TimezoneFinder()

    coords = geolocator.geocode(location)
    timezone = tf.timezone_at(lng=coords.longitude, lat=coords.latitude)
    print(timezone)
    tz=pytz.timezone(timezone)
    time=datetime.datetime.now(tz)
    if time.minute<10:
        stringify=str(time.hour)+":"+"0"+str(time.minute)
    else:
        stringify=str(time.hour)+":"+str(time.minute)
    return jsonify({"timezone":timezone,
                        "time": stringify})
   
    
@app.get('/timezoneutc')
def get_timezoneutc_endpoint():
        hor=request.args.get('hours')
        min=request.args.get('minutes')
        utc = pytz.utc
        hour=int(hor)
        current_time = datetime.datetime.utcnow()

        current_time_utc = utc.localize(current_time)
        print(current_time_utc)

        if hour==current_time_utc.hour:

            utc='UTC Normal'
            time=str(hour)+":"+min
            
            return jsonify({"timezone":utc,
                            "time": time})  
        elif hour>current_time_utc.hour and hour<24 and int(min)<60 and int(min)>0:
            hours=hour
            hour=hour-current_time_utc.hour
            utc='UTC: +'+str(hour)+':00'
            time=str(hours)+":"+min
            
            return jsonify({"timezone":utc,
                            "time": time})  
        elif hour<current_time_utc.hour and hour>0 and int(min)<60 and int(min)>0:
            hour=current_time_utc.hour-hour
            utc='UTC: -'+str(hour)+':00'
            time=hor+":"+min
            
            return jsonify({"timezone":utc,
                        "time": time})
        else:
            return jsonify({"error":"Unesi ispravno vreme."}) 
        
if __name__ == '__main__':
    app.run()