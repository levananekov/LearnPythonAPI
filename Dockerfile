FROM python
WORKDIR /code

COPY pyproject.toml poetry.lock /code/
COPY lib /code/
COPY tests /code/

RUN pip install --no-compile --upgrade pip \
 && pip install --no-compile poetry
RUN poetry install

ENV TEST_STAGE=${TEST_STAGE}

CMD python