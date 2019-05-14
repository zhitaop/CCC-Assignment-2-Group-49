FROM python:3
ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy https://wwwproxy.unimelb.edu.au:8000
ENV no_proxy localhost, 127.0.0.1, 127.0.1.1, ubuntu, 172.26.38.142
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "harvest.py"]
