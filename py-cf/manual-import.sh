#!/usr/bin/env bash
# Static Global Variables
START_DATE="2020-06-01"
END_DATE="2020-06-15"

# Binaries
PYTHON="/usr/local/bin/python3"
DATE="/usr/local/bin/gdate"

temp_date="${START_DATE}"
while [ "${temp_date}" != "${END_DATE}" ]; do 
  echo ${temp_date}
  QUERY_DATE="${temp_date}" ${PYTHON} main.py
  temp_date=$(${DATE} -I -d "${temp_date} + 1 day")
done
