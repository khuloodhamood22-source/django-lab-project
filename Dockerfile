FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="/$VIRTUAL_ENV/bin:$PATH"

ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static

WORKDIR $APP_HOME

EXPOSE 8000

COPY requirements.txt $APP_HOME/requirements.txt
RUN pip install -r requirements.txt

COPY . $APP_HOME/