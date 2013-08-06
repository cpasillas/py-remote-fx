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
EOF
}

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
volume=1

while getopts "h?v:c:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  volume=$OPTARG
        ;;
    c)  config_file=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

echo "volume=$volume, config_file='$config_file', Leftovers: $@"

# End of file
if [ $config_file ]
then
    sudo python firefight.py -v $volume -c $config_file
else
    sudo python firefight.py -v $volume
fi
