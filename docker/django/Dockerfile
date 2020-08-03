FROM python:3.7.4
ENV PYTHONUNBUFFERED 1

# Copy the requirements file and install the requirements
COPY ./requirements.txt /requirements.txt
COPY ./test_requirements.txt /test_requirements.txt
RUN pip install -r /requirements.txt
RUN pip install -r /test_requirements.txt

ADD . /app
ADD ./docker /docker

RUN chmod +x /docker/django/start.sh
RUN chmod +x /docker/django/wait_for_postgres.py

WORKDIR /app/
CMD ["/docker/django/start.sh"]
