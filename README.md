![Jaaxman](https://github.com/shirakiya/jaaxman/blob/master/app/static/img/logo_stacked_512.png)

# Jaaxman
[![CircleCI](https://circleci.com/gh/shirakiya/jaaxman/tree/master.svg?style=svg)](https://circleci.com/gh/shirakiya/jaaxman/tree/master)  
  
Jaaxman list [arXiv](https://arxiv.org/) papers in Japanese.

## Required
- Python>=3.6
- Node.js>=8.6
- MySQL5.6
    - database: `jaaxman` (charaset=utf8mb4)

## Environment Variables
| Key                   | default       |
|-----------------------|---------------|
| RUN_MODE              | 'development' |
| MYSQL_USER            | 'root'        |
| MYSQL_PASSWORD        | ''            |
| MYSQL_HOST            | 'localhost'   |
| GOOGLE_API_KEY        | None          |
| AWS_ACCESS_KEY_ID     | None          |
| AWS_SECRET_ACCESS_KEY | None          |
| SSH_PRIVATE_KEY_FILE  | None          |
| MACKEREL_APIKEY       | None          |
| SLACK_URL             | None          |


## SetUp
```
git clone https://github.com/shirakiya/jaaxman.git path/to/repos
cd path/to/repos

pip install -r requirements.txt

# if not exists database
mysql -u <db user> -p -e 'CREATE database jaaxman CHARACTER SET utf8mb4;'

python manage.py migrate

npm install
```


## Start
### Application
```
# app
python manage.py runserver

# frontend JavaScript
npm start
```

### Job
```
python manage.py <fetchrss|registerrss>
```

- `fetchrss`: Fetch RSS from arxiv.org and save paper datas to database.
- `registerrss`: Save arxiv.org subjects to fetch.


# Infla
## Build AMI
```
cd packer
packer build <gateway|app|job>.json
```

## Deploy
```
python manage.py deploy <app|job> <tarball name>
```
