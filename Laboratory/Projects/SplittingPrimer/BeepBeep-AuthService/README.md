[![Build Status](https://travis-ci.org/giacomodeliberali/BeepBeep-AuthService.svg?branch=master)](https://travis-ci.org/giacomodeliberali/BeepBeep-AuthService)
[![Coverage Status](https://coveralls.io/repos/github/giacomodeliberali/BeepBeep-AuthService/badge.svg?branch=master)](https://coveralls.io/github/giacomodeliberali/BeepBeep-AuthService?branch=master)

# Development

## Install & setup
To install dependencies and setup the app:
```
pip install -r requirements.txt
python setup.py develop
```

## Run

To run the app launch:
```
python beepbeep/authservice/run.py
```

## Test

To run coverage launch:
```
pytest --cov-config .coveragerc --cov beepbeep/authservice --cov-report html:cov_html
```
A new html report will be generated inside the *./cov_html* folder
