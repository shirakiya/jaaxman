![Jaaxman](https://github.com/shirakiya/jaaxman/blob/master/app/static/img/logo_stacked_512.png)

# Jaaxman
[![CircleCI](https://circleci.com/gh/shirakiya/jaaxman/tree/master.svg?style=svg)](https://circleci.com/gh/shirakiya/jaaxman/tree/master)  
  
Jaaxman list [arXiv](https://arxiv.org/) papers in Japanese.

## Required
- Python>=3.6.3
- Node.js>=8.12.0
- MySQL5.6
    - database: `jaaxman` (charaset=utf8mb4)
    - e.g. `mysql -u <db user> -p -e 'CREATE database jaaxman CHARACTER SET utf8mb4;'`

## Environment Variables
| Key                         | default                         |
|-----------------------------|---------------------------------|
| RUN_MODE                    | 'development'                   |
| ASSETS_BASE_URL             | 'http://localhost:8001/assets/' |
| MYSQL_USER                  | 'root'                          |
| MYSQL_PASSWORD              | ''                              |
| MYSQL_HOST                  | 'localhost'                     |
| API_TOKEN                   | None                            |
| GOOGLE_API_KEY              | None                            |
| AWS_ACCESS_KEY_ID           | None                            |
| AWS_SECRET_ACCESS_KEY       | None                            |
| SSH_PRIVATE_KEY_FILE        | None                            |
| SLACK_URL                   | None                            |
| TWITTER_CONSUMER_KEY        | None                            |
| TWITTER_CONSUMER_SECRET     | None                            |
| TWITTER_ACCESS_TOKEN        | None                            |
| TWITTER_ACCESS_TOKEN_SECRET | None                            |


# Use Docker
At first, it is necessary to install [Docker Community Edition](https://www.docker.com/community-edition) and [Docker Compose](https://docs.docker.com/compose/).

## SetUp
```
git clone https://github.com/shirakiya/jaaxman.git path/to/repos
cd path/to/repos

cp backend/env.sample backend/env
vim backend/env  # => write collect environment variables
```

## Start
### Application
```
docker-compose up
```

### Job
```
docker-compose exec backend python manage.py <fetchrss|registerrss>
```

### Test
```
docker-compose exec -e RUN_MODE=test backend python manage.py test
```


# Jobs
- `fetchrss`: Fetch RSS from arxiv.org and save paper datas to database.
- `registerrss`: Save arxiv.org subjects to fetch.


# Infla
## Build AMI
At first, prepare `packer/ansible/vault_password` file to decrypt vault.

```
echo '{ansible-vault-password}' > packer/ansible/vault_password
```

Build AMI by `packer build` command.

```
cd packer
packer build <gateway|app|job>.json
```

## Deploy
```
cd backend/
python manage.py deploy <app|job> <tarball name>
```
