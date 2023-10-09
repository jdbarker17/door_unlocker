import pigpio
import time

SERVO_PIN = 18

def set_servo_angle(pi,pin,angle):
    pulse_width = int((angle/180.0 * 2000) + 500)
    pi.set_servo_pulsewidth(pin,pulse_width)

def main():
    pi = pigpio.pi()
    pi.set_mode(SERVO_PIN, pigpio.OUTPUT)

    
    set_servo_angle(pi,SERVO_PIN,120)
    
    time.sleep(2)

    set_servo_angle(pi,SERVO_PIN,10)
    #pi.set_servo_pulsewidth(SERVO_PIN,0)
    pi.stop()

if __name__ == "__main__":
    main()