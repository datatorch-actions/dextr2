FROM python:3.8

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6' -y

RUN apt install -y liblzma-dev

WORKDIR /workspace
COPY requirements_container.txt /workspace
RUN pip install numpy
RUN pip install -r requirements_container.txt
RUN python -c "from dextr.model import DextrModel; DextrModel.pascalvoc_resunet101()"
RUN pip install gunicorn==20.0.4
COPY server.py /workspace

EXPOSE 8000
ENV DEVICE=cpu
WORKDIR /workspace
CMD [ "gunicorn", "-w 6", "-b 0.0.0.0:8000", "server:app" ]