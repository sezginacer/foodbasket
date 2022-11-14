## FoodBasket - Delivery Hero Tech Hub Challenge Project
![workflow](https://github.com/sezginacer/foodbasket/actions/workflows/pipeline.yml/badge.svg)
[![codecov](https://codecov.io/gh/sezginacer/foodbasket/branch/master/graph/badge.svg?token=L6LRM6TX8B)](https://codecov.io/gh/sezginacer/foodbasket)
- In order to run the project, execute in the project root directory `docker-compose up`.
There may be a problem with PostgreSQL when running project with *docker* for the first time. 
  PostgreSQL may be unavailable for the first time of running `docker-compose up`. Terminating it 
  and running `docker-compose up` again solves the problem.
- There is a script `scripts/initial.py` for initializing database with the data mentioned in 
[the project description](https://github.com/sezginacer/foodbasket/blob/master/doc-files/yemeksepeti-python-odevi.pdf).
  No need to execute it, since it's included in *docker* command. But it can be run as follows:
  `python manage.py runscript initial`
- In order to start the demo, first run `workers.py` and then `order_populator.py` in 
  another shell.
    ```sh
    docker-compose exec web sh
    cd demo
    python workers.py
    ```
    ```sh
    docker-compose exec web sh
    cd demo
    python order_populator.py
    ```

## Database Diagram
![Flowchart](https://github.com/sezginacer/foodbasket/blob/master/doc-files/database.png?raw=true)

## API Documentation
- Both [v2](https://github.com/sezginacer/foodbasket/blob/master/doc-files/foodbasket-postman-collection-v2.json?raw=true) & 
[v2.1](https://github.com/sezginacer/foodbasket/blob/master/doc-files/foodbasket-postman-collection-v2.1.json?raw=true) 
Postman collections are added.

### Notes
- `black` and `isort` are used for linting.
- Tests for services and all available endpoints are written.
- CI/CD integrated with the project using Github Action. It checks linting and runs tests.
- `/users/register/` and `/users/token/` endpoints are throttled. Both can be accessed separately 
  five times per minute.
- Localization is supported within the project and Turkish & English are supported languages. When 
  you add `Accept-Language: en-us` or `Accept-Language: tr-tr` header to the request, labels 
  are translated to preferred language.
- `RedisPubSub` is written and used for the project. `DummyPubSub` is also written in order to 
  configure it default `PubSub` class for pipeline tests.
- Passwords for all users are set to *12345*
