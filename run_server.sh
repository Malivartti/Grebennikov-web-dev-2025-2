#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/lab2
gunicorn app:application