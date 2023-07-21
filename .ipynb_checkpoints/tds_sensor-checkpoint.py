import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#if defined HAS_TDS
static const uint8_t adcTdsPin      =   26;
#endif

#ifdef HAS_TEMP_ONEWIRE
static const uint8_t oneWTempPin    =   22;
#endif

#ifdef HAS_TEMP_NTC
static const uint8_t adcTempNtcPin  =   27;
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24


GPIO_TDSPIN = 26
GPIO_TEMP = 22
GPIO_TEMP_NTC = 27
    
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
TANK_VOL = 100
# read tank vol

int sensorValue = 0;
float tdsValue = 0;
float Voltage = 0;


def sensorValue():
    sensorValue = analogRead(sensorPin);
    Voltage = sensorValue*5/1024.0; //Convert analog reading to Voltage
    tdsValue=(133.42/Voltage*Voltage*Voltage - 255.86*Voltage*Voltage + 857.39*Voltage)*0.5; //Convert voltage value to TDS value
    tdsValue
    
def tdsLev():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    # distance = (TimeElapsed * 34300) / 2

    tds_level = sensorValue()
    return tds_level
 
if __name__ == '__main__':
    try:
        while True:
            dist = tdsLev()
            print ("Measured TDS = %.1f" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
