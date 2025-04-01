alias grestart="service gunicorn restart"
alias gerestart="service gunicorn_global_region restart"
alias athensrestart="service gunicorn_athens restart"
alias larnacarestart="service gunicorn_larnaca restart"
alias madridrestart="service gunicorn_madrid restart"
alias limassolrestart="service gunicorn_limassol restart"
alias monacorestart="service gunicorn_monaco restart"
alias parisrestart="service gunicorn_paris restart"
alias cannesrestart="service gunicorn_cannes restart"
alias venvac="source .venv/bin/activate"
alias pullbranches="~/bin/pullbranches.sh"
# alias blumenhorizon='ssh -YX root@ip'
# alias blumenhorizon2='ssh -YX root@ip'
# alias mergebranches='~/bin/merge-branches.sh'

send() {
   if [[ -z "$1" || -z "$2" ]]; then
       echo "Ошибка: Нужно указать и исходный путь, и путь назначения."
       return 1
   fi
   rsync -av -e ssh "$1" "$2"
}