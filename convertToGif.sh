#!/bin/bash

echo Converting $1 to $2
ffmpeg -i $1 $2
echo Converted $1 to $2
