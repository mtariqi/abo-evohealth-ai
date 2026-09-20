FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs
RUN pip install --no-cache-dir .
ENTRYPOINT ["abo-evohealth"]
CMD ["demo", "--config", "configs/demo.yaml"]

