from __future__ import print_function

from inputs import get_gamepad, KEYS_AND_BUTTONS
import tello as tello_lib

tello = tello_lib.Tello('', 8889, command_timeout=0.03)

tello.flightSpeedCoefficient = 0.2

BTN_STATE_PRESSED = 1
BTN_LAND = "BTN_NORTH"
BTN_TAKE_OFF = "BTN_WEST"

STICK_FLIP_Y = "ABS_HAT0Y"
STICK_FLIP_X = "ABS_HAT0X"

STICK_FLY_X = "ABS_X"
STICK_FLY_Y = "ABS_Y"
STICK_FLY_Z = "ABS_Z"

STICK_SPEED = "ABS_RZ"


def main():
    while 1:
        events = get_gamepad()
        for event in events:
            if event.code in button_map and event.state == BTN_STATE_PRESSED:
                button_map[event.code]()
            if event.code in stick_map:
                axis = event.code[-1:]
                stick_map[event.code](axis, event.state)


def set_velocity(axis, velocity):
    velocity = 128-velocity
    velocity = velocity * -1
    velocity = int(round(velocity*100/128, 0))
    if axis == "X":
        velocity = int(velocity * tello.flightSpeedCoefficient)
        flight_state["left_right"] = velocity
    elif axis == "Y":
        velocity = int(velocity * tello.flightSpeedCoefficient)
        flight_state["front_back"] = velocity * -1
    elif axis == "Z":
        flight_state["yaw"] = velocity

    update_rc()


def set_flightSpeedCoefficient(unused, velocity):
    tello.flightSpeedCoefficient = round((255.0 - velocity)/255, 2)


def update_rc():
    tello.send_command(
        "rc {left_right:0} {front_back:0} {up_down:0} {yaw:0}".format(** flight_state))


def flip(axis, direction):
    if axis == "Y":
        if direction == -1:
            tello.flip("f")
        elif direction == 1:
            tello.flip("b")
    elif axis == "X":
        if direction == -1:
            tello.flip("l")
        elif direction == 1:
            tello.flip("r")


button_map = {
    BTN_TAKE_OFF: tello.takeoff,
    BTN_LAND: tello.land,
}

stick_map = {
    STICK_FLIP_Y: flip,
    STICK_FLIP_X: flip,
    STICK_FLY_X: set_velocity,
    STICK_FLY_Y: set_velocity,
    STICK_FLY_Z: set_velocity,
    STICK_SPEED: set_flightSpeedCoefficient,
}

flight_state = {"front_back": 0, "left_right": 0, "up_down": 0, "yaw": 0}

if __name__ == "__main__":
    main()
