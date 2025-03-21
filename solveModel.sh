#!/usr/bin/env bash



FILE=$1
NAME=`basename $FILE .xml`
TGT="output/$NAME.txt"
ERRORS="errors/$NAME.txt"

if ! python main.py -i $FILE -o $TGT; then
	echo "$FILE"	>> errors.txt
	python main.py -i $FILE -o $TGT	>> $ERRORS 2>&1
fi

