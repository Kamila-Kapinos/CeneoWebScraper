# CeneoWebScraper
Project based on Flask framework. It allows you to extact different products' opinions from Ceneo.pl using their IDs from webpage.

## To run
1. Install Python3
2. Install Mysql Server
3. Create database
4. Import into database `db/ceneo-scaper_.sql`
5. Install dependencies `pip install -r requirements.txt`
6. Set connection to database: `config/Config.py`

```
On MacBook
python3 -m venv .venv
source .venv/bin/activate
export FLASK_ENV=development
flask run
```

##Used the most important frameworks and libraries
1. Flask
2. Beautiful Soup
3. mysql-connector
4. pandas
5. matplotlib