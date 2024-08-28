Create a conda env with python 3.11 as its version

$ conda create -n comply python=3.11
$ conda activate comply

$ gh auth login
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser
Complete the process

mkdir complylaw

cd complylaw

# To Run in UAT
$ . bin/cldev.sh -s uat -t

# To Run in PROD
$ . bin/cldev.sh -s prod -t

$ pip install -r requirements.txt
$ cd ui-systests
# To run in Local
$ pytest webapp/login/test_login.py

# To run in Browserstack
$ pytest webapp/login/test_login.py -B browserstack

# To run for iphone Safari Browser in browserstack
$ pytest webapp/login/test_login.py -B browserstack -N iphone

# To run for android Chrome Browser in browserstack
$ pytest webapp/login/test_login.py -B browserstack -N android

# To create a PR
$ gh pr create --title "<Title for the feature>"