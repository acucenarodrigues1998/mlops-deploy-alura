FROM python:3.12-slim

ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=BASIC_AUTH_PASSWORD_ARG

COPY ./requirements.txt /usr/requirements.txt

WORKDIR /usr

RUN pip3 install -r requirements.txt

COPY ./mlops_deploy_course /usr/mlops_deploy_course
COPY ./models /usr/models

ENTRYPOINT [ "python3" ]
CMD [ "mlops_deploy_course/app/main.py" ]