FROM python:3
WORKDIR /usr/src/app
RUN ls
RUN git clone -q https://github.com/giacomodeliberali/BeepBeep-AuthService.git
WORKDIR BeepBeep-AuthService
RUN pip3 install -r ./requirements.txt --exists-action w
RUN python3 setup.py develop
EXPOSE 5050
CMD [ "python", "./beepbeep/authservice/run.py" ]