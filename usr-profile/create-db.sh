#!/usr/bin/env bash

# Define the directory where the script is located
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
db=${dir}/profiles.db

# First, remove the database if it already exists
if [ -f $db ]; then
    rm $db
fi
# Create the database
sqlite3 $db < ${dir}/schema.sql
# Insert some data
sqlite3 $db < ${dir}/data.sql