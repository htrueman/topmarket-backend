## Deploy project

### Postgres
```
psql postgres
>> create database market_dev; 
>> create user market_user with password 'pass12pass';
>> grant all privileges on database market_dev to market_user;
```

### Python
```
apt install python3
apt install virtualenv
virtualenv -p python3 env
source env/bin/activate

```

### Redis

```
brew install redis-server
brew services start redis
```

### Django

```
. env.sh
pip install -r requirements.txt
python manage.py migrate

python manage.py runserver 
```

### Celery
```
celery -A top_market_platform worker -D
```
