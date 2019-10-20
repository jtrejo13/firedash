FROM heroku/miniconda

# Grab requirements.txt
ADD ./requirements.txt /tmp/requirements.txt

# Grab environment.yml
ADD ./environment.yml /tmp/environment.yml

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./firedash /opt/firedash/
WORKDIR /opt/firedash

RUN conda update conda
RUN conda env create -f /tmp/environment.yml

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
