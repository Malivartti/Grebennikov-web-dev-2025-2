#!/bin/bash
gunicorn --workers=4 --reload app:application