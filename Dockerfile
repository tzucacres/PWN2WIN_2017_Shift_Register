FROM python:3.11-slim

WORKDIR /app

COPY crap.txt netlist.v solve3.py ./

RUN pip install --no-cache-dir z3-solver

CMD ["python", "solve3.py"]
