import logging
import sys
import math
import socket
from rpibotics.rover_sj17 import Rover
from rpibotics.hmc5983 import convert_radians_to_degrees_minutes

# root = logging.getLogger()
# root.setLevel(logging.DEBUG)
# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# root.addHandler(ch)

ROVER_HOSTNAME = socket.gethostname()

# from rpibotics import image_processor

MOBILITY_SYSTEM_CONFIG = {
    'motor_left'           : {'gpio_pin_ena': 12,
                              'gpio_pin_in1': 20,
                              'gpio_pin_in2': 16,
                              'frequency'   : 100.0},
    'motor_right'          : {'gpio_pin_ena': 13,
                              'gpio_pin_in1': 26,
                              'gpio_pin_in2': 19,
                              'frequency'   : 100.0},
    'encoder_left'         : {'gpio_pin'  : 8,
                              'slit_count': 20},
    'encoder_right'        : {'gpio_pin'  : 7,
                              'slit_count': 20},
    'obstacle_sensor_left' : {'gpio_pin': 17},
    'obstacle_sensor_right': {'gpio_pin': 27},
    'pid'                  : {'kp': 300.0,
                              'ki': 200.0,
                              'kd': 0.0},
    'initial_duty_cycle'   : {'duty_cycle_left' : 70.0,
                              'duty_cycle_right': 70.0},
    'wheel_diameter'       : 0.065,
    'wheel_distance'       : 0.08276
}

DHT_SENSOR_CONFIG = {
    'gpio_pin': 24
}

MAG_CONFIG = {
    'port'       : 1,
    'address'    : 0x1E,
    'max_gauss'  : 1.3,
    'declination': (11, 55)
}

LANCE_CONFIG = {
    'gpio_pin'         : 21,
    'duty_cycle_open'  : 3,
    'duty_cycle_closed': 12
}

IMAGING_CONFIG = {
    'path': "/var/www/html/rover_img/",
}

if ROVER_HOSTNAME == 'rover1':
    MOBILITY_SYSTEM_CONFIG['initial_duty_cycle']['duty_cycle_left'] = 70.0
    MOBILITY_SYSTEM_CONFIG['initial_duty_cycle']['duty_cycle_right'] = 80.0
    MOBILITY_SYSTEM_CONFIG['wheel_distance'] = 0.08276
    LANCE_CONFIG['duty_cycle_open'] = 13.0
    LANCE_CONFIG['duty_cycle_closed'] = 2.9
elif ROVER_HOSTNAME == 'rover5':
    MOBILITY_SYSTEM_CONFIG['initial_duty_cycle']['duty_cycle_left'] = 70.0
    MOBILITY_SYSTEM_CONFIG['initial_duty_cycle']['duty_cycle_right'] = 80.0
    MOBILITY_SYSTEM_CONFIG['wheel_distance'] = 0.08276
    LANCE_CONFIG['duty_cycle_open'] = 11.8
    LANCE_CONFIG['duty_cycle_closed'] = 2.7

MY_ROVER = Rover(mobility_system_config=MOBILITY_SYSTEM_CONFIG,
                 dht_sensor_config=DHT_SENSOR_CONFIG,
                 mag_config=MAG_CONFIG,
                 lance_config=LANCE_CONFIG,
                 imaging_config=IMAGING_CONFIG)


def stop():
    print('Stopping... ', end='')
    MY_ROVER.mob.stop()
    print('done')


def forward(target_distance=0.3):
    print('Driving forward... ', end='')
    MY_ROVER.mob.go_forward(target_distance=target_distance)
    print('done')


def backward(target_distance=0.3):
    print('Driving backward... ', end='')
    MY_ROVER.mob.go_backward(target_distance=target_distance)
    print('done')


def right(target_angle=90.0):
    print('Turning right... ', end='')
    MY_ROVER.mob.turn_right(target_angle=target_angle)
    print('done')


def left(target_angle=90.0):
    print('Turning left... ', end='')
    MY_ROVER.mob.turn_left(target_angle=target_angle)
    print('done')


def isblocked():
    print('Checking if front is blocked... ', end='')
    front_is_blocked = MY_ROVER.mob.front_is_blocked()
    if front_is_blocked:
        print('yes')
    else:
        print('no')
    return front_is_blocked


def temperature():
    print('Measuring temperature... ', end='')
    t = round(MY_ROVER.dht.measure_temperature(), 1)
    print('{0:.1f}\N{DEGREE SIGN}C'.format(t))
    return t


def humidity():
    print('Measuring humidity... ', end='')
    h = round(MY_ROVER.dht.measure_humidity(), 1)
    print('{0:.1f}%'.format(h))
    return h


def heading():
    print('Measuring heading... ', end='')
    h = math.degrees(MY_ROVER.mag.get_heading())
    d, m = convert_radians_to_degrees_minutes(h)
    print('{:d}\N{DEGREE SIGN} {:d}\''.format(d, m))
    return d, m


def zmag():
    print('Measuring magnetic flux in z direction... ', end='')
    x, y, z = MY_ROVER.mag.get_data()
    print('{0:.1f}% Gs'.format(z))
    return round(z, 1)


def arm():
    print('Arming lance... ', end='')
    MY_ROVER.lance.arm()
    print('done')


def disarm():
    print('Disarming lance... ', end='')
    MY_ROVER.lance.disarm()
    print('done')


def image():
    print('Capturing image... ')
    i = MY_ROVER.capture_image()
    print('done http://{}/rover_img/{}'.format(
        ROVER_HOSTNAME, i.replace(IMAGING_CONFIG['path'], '')))
    return i
