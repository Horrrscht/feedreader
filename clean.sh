#!/bin/sh

rm *.json
rm *.xml
rm *.pyc
rm -rf __pycache__

cp feedlist.json.old feedlist.json
