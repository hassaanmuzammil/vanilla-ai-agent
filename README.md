# vanilla-ai-agent

An end-to-end AI agent built from first principles — minimal libraries, no shortcuts, just raw logic and code.

## 🛠️ Setup

Setup [uv](https://github.com/astral-sh/uv) and install packages
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e .
```

## Setup Chainlit Database
```sh
cd database
docker compose up -d chainlit_db
```
Execute the following script to apply the physical data model: [`Chainlit DB Schema`](./database/scripts/chainlit_schema.sql)

## Setup Dummy Target Database (For testing purposes)
```sh
cd database
docker compose up -d postgres_db
```
Execute the following script to apply the physical data model: 
- [`DB Schema`](./database/scripts/schema.sql)
- [`Dummy Data`](./database/scripts/dummy_data.sql)


## 🚀 Run the App
Start the Chainlit UI (make sure required environment variables are set):

```bash
chainlit run main.py --host 0.0.0.0 --port 8000 -h
```

## Text-to-SQL Example

Watch a demo of `vanilla-ai-agent` in action:

[🎥 Demo Video](docs/sample.mov)

