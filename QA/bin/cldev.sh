
# Make sure user is sourcing this script
# https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [ $sourced -eq 0 ]; then
    echo "This script should be sourced, use . or source as in front of script name"
    exit 1
fi

OPTIND=1 # because this script is sourced

usage() { echo "Usage: $0 -s <Stage>" 1>&2; kill -INT $$; }
do_tunnel=0

while getopts "s:t" opt; do
    case $opt in
        s)  stage=${OPTARG} ;;
        t)  do_tunnel=1;;
        ?)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

echo $stage
if [ -z $stage ]; then
  echo "Must supply a stage argument"
  usage
fi
export CL_STAGE=$stage


unset stage

echo "Setting up for $CL_STAGE stage"

if [ $CL_STAGE = 'prod' ]
then
    export CL_URL="https://www.comply.law/"
else
    export CL_URL="https://uatlms.techraq.com/"
fi

#${BASH_SOURCE[0]:-${(%):-%x}}))) intends to support both bash and zsh
# see https://stackoverflow.com/questions/9901210/bash-source0-equivalent-in-zsh.
REPODIR=$(dirname $(dirname $(realpath ${BASH_SOURCE[0]:-${(%):-%x}})))
echo "Repo dir is: " $REPODIR


export REPODIR="$(cygpath -w $REPODIR)";
export PYTHONPATH="$REPODIR";

echo "PYTHONPATH --> ${PYTHONPATH}"
export LOCALDEV=1


if [ $do_tunnel -eq 1 ]
then
    env=$CL_STAGE source $REPODIR/bin/tunnels.sh
else
    echo "Sourcing $REPODIR/.env.$CL_STAGE"
    source $REPODIR/.env.$CL_STAGE
fi