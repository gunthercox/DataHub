#!/bin/sh

echo "Sending request to remove expired events." >> /dev/stdout

curl --verbose -X "DELETE" http://nginx:8080

echo "Request to remove expired events completed." >> /dev/stdout
