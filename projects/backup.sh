#!/bin/bash

# This checks if the number of arguments is correct
# If the number of arguments is incorrect ( $# != 2) print error message and exit
if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit
fi

# This checks if argument 1 and argument 2 are valid directory paths
if [[ ! -d $1 ]] || [[ ! -d $2 ]]
then
  echo "Invalid directory path provided"
  exit
fi

targetDirectory=$1
destinationDirectory=$2

echo "$targetDirectory"
echo "$destinationDirectory"

currentTS=`date +%s`

backupFileName="backup-$currentTS.tar.gz"

# We're going to:
  # 1: Go into the target directory
  # 2: Create the backup file
  # 3: Move the backup file to the destination directory

# define variables...

origAbsPath=`pwd`

cd $destinationDirectory # <-
destDirAbsPath=`pwd`

cd $origAbsPath # <-
cd $destinationDirectory # <-

yesterdayTS=($currentTS - 86400)

# Declare toBackup array
declare -a toBackup

# Run through files in curr directory and append to toBackup array
for file in $(ls)
do
  if ((`date -r $file +%s` > $yesterdayTS))
  then toBackup+=($file)
  fi
done

# save array into a tar.gz file
tar -czvf $backupFileName ${toBackup[@]} .
# move that file to current directory
mv $backupFileName $destDirAbsPath
