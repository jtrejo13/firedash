FROM heroku/miniconda

# Grab requirements.txt.
ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./firedash /opt/firedash/
WORKDIR /opt/firedash

RUN conda env create -f environment.yml

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
