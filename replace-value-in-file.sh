if [ $# -ne 3 ]; then
  echo "Usage: $0 <filepath(s)> <value_to_replace> <new_value>"
  exit 1
fi

FILEPATH=$1
REPLACE=$2
REPLACE_VALUE=$3

# Multiple files
if grep -q "," <<< ${FILEPATH}; then
  for FILE in $(echo $FILEPATH | sed 's/,/ /g'); do
    sed -i 's/'"${REPLACE}"'/'"${REPLACE_VALUE}"'/g' $FILE
  done
else
  # Single file
  sed -i 's/'"${REPLACE}"'/'"${REPLACE_VALUE}"'/g' $FILEPATH
fi

