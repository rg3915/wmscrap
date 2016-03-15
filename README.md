# wmscrap

Web scraping with Python 2.7 and Redis.

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
make run PAGES=10
```

### Redis

```bash
redis-server
```

Em outra janela faça:

```bash
redis-cli
KEYS *
```