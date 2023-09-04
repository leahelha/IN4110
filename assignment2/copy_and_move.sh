
#Making a bash script to copy and move the polluting gas files to their own directory according to
# gas type, regardless of source

# Run example: 
#./copy_and_move.sh ./pollution_data/by_src/src_road_traffic/ H2 ./pollution_data roa
# Here src_dir=./pollution_data/by_src/src_road_traffic/,  file_name=H2 and new_dir=./pollution_data and mod=roa

#!/bin/bash

#Check if correct number of arguments
if [ ${#} -ne 4 ]; then
    echo "Use 4 command line arguments!"
    exit 1
fi 


#We choose the source directory of the .csv file and the name of the .csv file using 
# command line arguments, We also make the new file 

src_dir="$1"
file_name="$2"
new_dir="$3"

#I had to add a modification to rename the files
mod="$4"

#Give an error message is the wrong source file is given
if [ ! -d ${src_dir} ]; then
    echo "The source file does not exist."
    exit 1
fi

#Make a new directory to store the .csv copies in
#Make sure you don't make a new one if there already exists one

if [ ! -d "${new_dir}" ]; then
    mkdir "${new_dir}"
fi 


#If filename already exists in new_dir -> append new data to old filename
#Find correct file, and copy a renamed version of it into a new directory

find "$src_dir" -type f -name "$file_name".csv -exec sh -c 'cp "$1" "${2}/${3}/${4}_${3}.csv"' _ {} "$new_dir" "$file_name" "$mod" \;


#Message of completion

echo "${file_name} from ${src_dir} has been copied to ${new_dir}$"
