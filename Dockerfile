FROM python:3.7.12

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6' -y

RUN apt install -y liblzma-dev

WORKDIR /workspace
RUN wget https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp37-cp37m-linux_x86_64.whl
COPY requirements_container.txt /workspace
#COPY torch-1.4.0+cpu-cp37-cp37m-linux_x86_64.whl /workspace
#RUN pip install numpy
RUN pip install -r requirements_container.txt
RUN python -c "from dextr.model import DextrModel; DextrModel.pascalvoc_resunet101()"
RUN pip install gunicorn==20.0.4
COPY server.py /workspace

EXPOSE 8000
ENV DEVICE=cpu
WORKDIR /workspace
CMD [ "gunicorn", "-w 1", "-b 0.0.0.0:8000", "-t 60", "server:app" ]
