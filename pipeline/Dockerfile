FROM python:3.13.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

#inslatts the dependencies from uv.lock
RUN uv sync --locked

COPY pipeline.py .

#ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
ENTRYPOINT ["python", "pipeline.py"]

#RUN pip install pandas pyarrow




