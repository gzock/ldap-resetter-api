from python:3.6-alpine

RUN apk add gcc openldap-dev musl-dev

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD python3 ldap-resetter-api.py
