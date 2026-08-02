FROM surnet/alpine-python-wkhtmltopdf:3.11.4-0.12.6-small

WORKDIR /home

# Setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

RUN apk update

# Install pre-reqs
# psycopg2
RUN apk add postgresql-dev gcc python3-dev musl-dev
# pillow
RUN apk add zlib-dev jpeg-dev gcc musl-dev

# Install tools
RUN apk add nano wget

# Install SSL certs
RUN wget https://gu-st.ru/content/lending/russian_trusted_sub_ca_pem.crt && mv russian_trusted_sub_ca_pem.crt /usr/local/share/ca-certificates/ && wget https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt && mv russian_trusted_root_ca_pem.crt /usr/local/share/ca-certificates/ && update-ca-certificates

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip && pip install pipenv && pipenv install --deploy --system

# Install cron jobs
RUN apk add supercronic shadow
COPY crontab .
RUN chmod 0644 crontab

# Install application
COPY ./src /home
