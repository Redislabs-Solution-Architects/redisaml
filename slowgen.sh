#!/bin/bash

# update

while True; do
    COUNT=100; python3 generate.py
    sleep_duration=$((2 + $RANDOM % 10));
    # echo $sleep_duration;
    sleep $sleep_duration;
done