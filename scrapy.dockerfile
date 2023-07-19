FROM python:3.8-slim-buster

LABEL author="TadeasDed"
LABEL description="Scrapy Image for Luxonis demo"
LABEL version="1.0"

# install  dependencies
COPY /scrapy_project/requirements.txt .
RUN pip install -r requirements.txt

# copy content from scrapy_project to /scrapy_project
COPY /scrapy_project/. /scrapy_project

# final configuration
CMD ["python", "scrapy_project/spider-run.py"]