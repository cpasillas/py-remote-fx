#!/bin/bash
# Argument = -v volume -c config_file

show_help()
{
cat << EOF
usage: $0 options

This script run the test1 or test2 over a machine.

OPTIONS:
   -h, -?    Show this message
   -v INT    Volume, INT is an integer
   -c FILE   Path to config file (e.g. /home/me/myconfig.cfg)
   -w        Rely on user to open admin command prompt in Windows
EOF
}

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
volume=1

while getopts "h?v:c:w?" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  volume=$OPTARG
        ;;
    c)  config_file=$OPTARG
        ;;
    w)  win7=1
        ;;
    esac
done

shift $((OPTIND-1))

if [ -z $config_file ]
then
  echo "Config file must be specified with -c"
  exit 1
fi

[ "$1" = "--" ] && shift

echo "Leftover args: $@"
command="python firefight.py -v $volume -c $config_file"
echo "Running command: $command"

# End of file
if [ $win7 ]
then
  $command
else
  sudo $command
fi
