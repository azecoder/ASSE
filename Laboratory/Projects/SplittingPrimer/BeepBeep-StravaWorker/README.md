[![Build Status](https://travis-ci.com/giacomodeliberali/BeepBeep-StravaWorker.svg?branch=master)](https://travis-ci.com/giacomodeliberali/BeepBeep-StravaWorker) [![Coverage Status](https://coveralls.io/repos/github/giacomodeliberali/BeepBeep-StravaWorker/badge.svg?branch=master)](https://coveralls.io/github/giacomodeliberali/BeepBeep-StravaWorker?branch=master)

# BeepBeep-StravaWorker

The other repo of data-service is [https://github.com/giacomodeliberali/BeepBeep-DataService](https://github.com/giacomodeliberali/BeepBeep-DataService)

## Development

To start the celery worker type:
```
source key.sh
celery worker -A datapump.datapump -B
```

## Test

To run pytest launch `pytest --cov-config .coveragerc --cov datapump`