FROM python:3.9-slim-buster

WORKDIR /smart_park

RUN apt-get update \
    && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python
ENV PATH="VIRTUAL_ENV/bin:$PATH"

COPY . .

RUN pip install -r requirements.txt

COPY activation.py ../usr/local/lib/python3.9/site-packages/torch/nn/modules/

CMD ["python", "run_process1.py"]