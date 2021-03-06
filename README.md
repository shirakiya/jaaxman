![Jaaxman](https://github.com/shirakiya/jaaxman/blob/master/backend/app/static/img/logo_stacked_512.png)

# Jaaxman
[![CircleCI](https://circleci.com/gh/shirakiya/jaaxman/tree/master.svg?style=svg)](https://circleci.com/gh/shirakiya/jaaxman/tree/master)  
  
Jaaxman list [arXiv](https://arxiv.org/) papers in Japanese.

## Required
- Python>=3.6.2
- Node.js>=8.12.0
- MySQL5.6

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
| SLACK_URL                   | None                            |
| TWITTER_CONSUMER_KEY        | None                            |
| TWITTER_CONSUMER_SECRET     | None                            |
| TWITTER_ACCESS_TOKEN        | None                            |
| TWITTER_ACCESS_TOKEN_SECRET | None                            |
| ROLLBAR_ACCESS_TOKEN        | None                            |


# Use Docker
At first, it is necessary to install [Docker Community Edition](https://www.docker.com/community-edition) and [Docker Compose](https://docs.docker.com/compose/).


## Start
### Application
```
$ make up
```

### Job
```
$ make run/<fetchrss|regsiterrss>
```

### Test
```
# test all
$ make test

# test only backend
$ make test/backend
```


# Jobs
- `fetchrss`: Fetch RSS from arxiv.org and save paper datas to database.
- `registerrss`: Save arxiv.org subjects to fetch.
