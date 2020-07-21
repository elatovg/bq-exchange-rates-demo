#!/usr/bin/env bash
# Static Global Variables
GCS_BUCKET="<your_bucket>"
GCS_FOLDER="<your_folder>"
GCS_URL="gs://${GCS_BUCKET}/${GCS_FOLDER}"

# https://openexchangerates.org/api/historical/2012-07-10.json?app_id=$APP_ID
OE_API_KEY="<your_openexchange_api_key>"
OE_BASE_URL="https://openexchangerates.org/api/historical"

# for testing
# START_DATE="2020-05-13"
# END_DATE="2020-05-15"
START_DATE="2020-06-01"
END_DATE="2020-06-15"

# Binaries
CURL="/usr/bin/curl"
GSUTIL="/opt/google-cloud-sdk/bin/gsutil"
DATE="/usr/local/bin/gdate"

temp_date="${START_DATE}"
while [ "${temp_date}" != "${END_DATE}" ]; do 
  # echo ${temp_date}
  oe_url="${OE_BASE_URL}/${temp_date}.json?app_id=${OE_API_KEY}"
  json_file="${temp_date}.json"
  # echo "will curl the following url: ${oe_url}"

  ${CURL} -s "${oe_url}" -o ${json_file}
  echo "uploading ${json_file} to ${GCS_URL}"
  ${GSUTIL} -q cp ${json_file} ${GCS_URL}
  temp_date=$(${DATE} -I -d "${temp_date} + 1 day")
done
