#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

def get_touchpad_status(outs, ins, measurements=5):
    y = []
    for i in range(measurements):
        x = []
        for out_idx, out in enumerate(outs):
            GPIO.output(out, GPIO.HIGH)
            time.sleep(0.001)  # wait 1ms (pins can do > 200kHz)
            for in_idx, _in in enumerate(ins):
                # print(f"{out_idx}/{in_idx}:{GPIO.input(_in)} {GPIO.input(_in) == GPIO.HIGH}")
                if GPIO.input(_in) == GPIO.HIGH:
                    x.append(out_idx * len(ins) + in_idx)
            GPIO.output(out, GPIO.LOW)
            time.sleep(0.01)  # wait 10ms (pins can do > 200kHz)
        y.append(x)
        time.sleep(0.1)
    return y

def print_touchpad_status(y):
    z = set()
    occurances = {}
    for x in y:
        z.update(x)
    for val in z:
        occurances[val] = sum([sum([1 for v in x if v == val]) for x in y])
    print("".join([f"{k}({v})   " for k,v in occurances.items()]))

def main():
    outs = [23, 22, 27, 17]
    ins = [16, 26, 13, 12, 6, 5]

    GPIO.setmode(GPIO.BCM)
    for out in outs:
        print(f"Configuring pin {out} as output")
        GPIO.setup(out, GPIO.OUT, initial=GPIO.LOW)

    for _in in ins:
        print(f"Configuring pin {_in} as input")
        GPIO.setup(_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        x = get_touchpad_status(outs, ins)
        print_touchpad_status(x)
        time.sleep(1)

if __name__ == "__main__":
    main()
