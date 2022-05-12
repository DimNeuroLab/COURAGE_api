# pulling the python image
FROM python:3.8
#-alpine

# copy requirements into the image
COPY ./requirements.txt /COURAGE_api/requirements.txt

# switch working directory
WORKDIR /COURAGE_api

# install the dependencies and packages in the requirements file
# RUN apt-get -y install libc-dev
# RUN pip install -U pip
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /COURAGE_api

RUN python3 -m pip install .

# configure the container to run in an executed manner
ENTRYPOINT ["python"]

CMD ["app/app.py"]
