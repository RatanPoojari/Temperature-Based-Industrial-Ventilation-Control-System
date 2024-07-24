import time
import smbus2
import bme280
import RPi.GPIO as GPIO

address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# GPIO pins for relays
INLET_RELAY_PIN = 27  # GPIO pin connected to the Inlet fan relay module
EXHAUST_RELAY_PIN = 17  # GPIO pin connected to the Exhaust fan relay module

# Servo motor GPIO pins
EXHAUST_SERVO_PIN = 18  # GPIO pin for Exhaust servo

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(INLET_RELAY_PIN, GPIO.OUT)  # Set INLET_RELAY_PIN as output
GPIO.setup(EXHAUST_RELAY_PIN, GPIO.OUT)  # Set EXHAUST_RELAY_PIN as output

# Initialize PWM for servo motor
GPIO.setup(EXHAUST_SERVO_PIN, GPIO.OUT)  # Set EXHAUST_SERVO_PIN as output
exhaust_pwm = GPIO.PWM(EXHAUST_SERVO_PIN, 50)  # 50 Hz frequency for Exhaust servo
exhaust_pwm.start(0)

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def control_inlet_fan(status):
    # Control the Inlet fan based on status (True for ON, False for OFF)
    print("Inlet Fan Status:", status)  # Debug print
    GPIO.output(INLET_RELAY_PIN, GPIO.HIGH if status else GPIO.LOW)

def control_exhaust_fan(status):
    # Control the Exhaust fan based on status (True for ON, False for OFF)
    print("Exhaust Fan Status:", status)  # Debug print
    GPIO.output(EXHAUST_RELAY_PIN, GPIO.HIGH if status else GPIO.LOW)

def control_exhaust_servo(angle):
    # Control the Exhaust servo motor based on angle (0 to 90 degrees)
    duty_cycle = (angle / 18) + 2.5  # Convert angle to duty cycle (2.5% to 12.5%)
    print("Exhaust Servo Duty Cycle:", duty_cycle)  # Debug print
    exhaust_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Wait for the servo to reach the position

try:
    while True:
        # Read sensor data
        data = bme280.sample(bus, address)

        # Extract temperature
        temperature_celsius = data.temperature

        # Convert temperature to Fahrenheit
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

        # Print the readings
        print("Temperature: {:.2f} °C, {:.2f} °F".format(temperature_celsius, temperature_fahrenheit))

        # Control the fan and servo motors based on temperature
        if temperature_celsius > 33:
            # Temperature > 33°C: Turn on Exhaust fan and set Exhaust Servo to 90 degrees, Inlet fan off
            control_inlet_fan(False)
            control_exhaust_fan(True)
            control_exhaust_servo(90)
        elif 35 <= temperature_celsius <= 40:
            # 35°C <= Temperature <= 40°C: Turn on Inlet fan and set Inlet Servo to 90 degrees, Exhaust fan off
            control_inlet_fan(True)
            control_exhaust_fan(False)
        else:
            # Other cases: Turn off both fans and Servo
            control_inlet_fan(False)
            control_exhaust_fan(False)
            control_exhaust_servo(0)

        # Temp data reading delay
        time.sleep(2)
        
except KeyboardInterrupt:
    print('Program stopped')
finally:
    # Clean up GPIO and PWM
    GPIO.cleanup() 
    exhaust_pwm.stop()
