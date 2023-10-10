import pigpio
import time
from flask import Flask, request,jsonify


SERVO_PIN = 18

app = Flask(__name__)
pi = pigpio.pi()
pi.set_mode(SERVO_PIN, pigpio.OUTPUT)

def set_servo_angle(pi,pin,angle):
    pulse_width = int((angle/180.0 * 2000) + 500)
    pi.set_servo_pulsewidth(pin,pulse_width)

def open_door():
    
    set_servo_angle(pi,SERVO_PIN,120)


def close_door():
  
    set_servo_angle(pi,SERVO_PIN,10)

def stop_servo():
    pi.set_servo_pulsewidth(SERVO_PIN,0)
    pi.stop()


@app.route("/", methods = ['POST'])
def recieve():
    
    if request.is_json:
        data = request.get_json()
        print(f"JSON Recieved: {data}")
        door_pos = int(data['door_position'])

        if door_pos == 0:
            close_door()
        
        if door_pos == 1:
            open_door()


        return jsonify(message = "Data Recieved", data = data),200
    else:
        return jsonify(message = "Bad Request: Expecting Content-Type:application/json"), 400

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 1717)