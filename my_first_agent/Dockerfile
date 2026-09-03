FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["adk", "api-server", "--host", "0.0.0.0", "--port", "8080", "--agent", "my_first_agent.agent:root_agent"]