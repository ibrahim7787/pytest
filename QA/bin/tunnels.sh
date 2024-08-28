# Make sure user is sourcing this script
# https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [ $sourced -eq 0 ]; then
    echo "This script should be sourced, use . or source as in front of script name"
    exit 1
fi


if [ -z "$env" ]
then
  export env=$TT_STAGE
fi

#${BASH_SOURCE[0]:-${(%):-%x}}))) intends to support both bash and zsh rather than $BASH_SOURCE which fails for zsh
# see https://stackoverflow.com/questions/9901210/bash-source0-equivalent-in-zsh.
REPODIR=$(dirname $(dirname $(realpath ${BASH_SOURCE[0]:-${(%):-%x}})))

if [ ! -f $REPODIR/.env.$env ]; then
  echo
  echo "ERROR: $REPODIR/.env.$env does not exist"
  kill -INT $$
fi

echo "Sourcing $REPODIR/.env.$env"
source $REPODIR/.env.$env