# Map My World - API

  

## Getting Started

  

Map My World API is a platform that provides a REST API to explore and review different locations and categories around the world, such as restaurants, parks and museums. It allows users to add new locations and categories, as well as get recommendations based on location-category combinations not reviewed in the last 30 days, prioritizing those that have never been reviewed. The API is designed to be clear, efficient and well-structured, following coding and documentation best practices.

  

Based on technologies such as FastAPI, Python, Alembic and Docker, simply clone the project and configure the environment variables to get started without any problems.

  

## Contenido

  

1. [Access to the Application](#access-to-the-application)

2. [Installation](#installation)

3. [How to Use](#how-to-use)

4. [Project Structure](#project-structure)

5. [Authors and Contact](#authors-and-contact)

  

## Access to the Application

  

Interactive API documentation is available at:

  

- [Swagger UI (ReDoc)](http://localhost:5001/redoc): Swagger's interactive user interface.

- [Swagger UI](http://localhost:5001/docs): Swagger's interactive user interface.

  

## Installation

  

Follow the instructions in the README.md file to install and run the project locally. API documentation will be available at http://localhost:5001/docs after execution.

  

1.  **Clone the Repository:**

  

```bash

git  clone  https://github.com/danielcinome/map_my_world_api.git

cd  map_my_world_api

```

  

2.  **Virtual Environment Configuration (Optional, but recommended):**

  Python version → Python 3.9.18

```bash
python  -m  venv  venv

source  venv/bin/activate  # For Unix-based systems (Linux/Mac)

```

  

3.  **Installs Units:**

  

```bash

pip  install  -r  requirements.txt

```

  

4.  **Environment Variables Configuration:**

  

```

SECRET_KEY

ALGORITHM # Use case -> HS256

SQLALCHEMY_DATABASE_URL # You can use SupaBase

```

  

* To generate the SECRET_KEY you can use:

```bash

openssl rand -hex 32

```

  

5.  **Initialize the Database:**
  
 ![F3-0](https://usijibigyuixwbbmwhws.supabase.co/storage/v1/object/public/map_my_world/model_db_map_my_world.png)

```bash

alembic revision --autogenerate -m "Your comment"

alembic  upgrade  head

```

  

6.  **Docker Installation:**

  

If you want to make use of docker, run the following command

  

```bash

docker-compose  up  --build

```

  

## How to Use

  

To execute the project use the command:

  

```bash

# Example of command or code

python  runner.py  # You can use or

make  dev

```

  
  

If you do not have your own user, you must generate a registration from `/user/create`.

  

- Then **click** on **Authorize** and enter your authentication credentials, once authenticated you will be able to use the mentioned services.

  

![F2-2](https://i.ibb.co/rt7FsgL/Captura-de-pantalla-2023-12-17-a-la-s-7-47-50-p-m.png)

  
  

## Project Structure

  

The current structure of the project is organized as follows:

  

```plaintext

│── alembic/

│── app/

│── api/

│ │── core/

│ │── crud/

│ │── login/

│ │── user/

│ │── category/

│ │── location/

│ │── recommendation/

│── db/

│ │── postgres/

│ │── engine.py

│ │── testing/

│ │── engine.py

│── models/

│ │── models.py

│── tests/

│── main.py

│── requirements.txt

│── docker-compose.yaml

│── Dockerfile

│── Makefile

│── README.md

│── runner.py

```

  

-  **alembic/**: Contains files related to Alembic, a database migration tool for SQLAlchemy. It is used to manage changes in the database schema.

-  **app/**: Main directory of the application source code.

-  **api/**: Contains modules that define the API paths.

-  **db/**: It contains modules related to **database session** management for both **production** and **testing**.

-  **integration/**: Contains the adaptive design pattern for the handling of project-specific data.

-  **models/**: Contains `models.py`, where the data models used in the application are defined.

  

-  `main.py`: Main entry point of the application.

  

-  **requirements.txt**: File that lists the project dependencies.

-  **docker-compose.yaml**: Configuration for Docker Compose.

-  **Dockerfile**: File to build the Docker image.

-  **README.md**: Main documentation of the project.

-  `runner.py`: File to run or start the application.

  
  

## Authors and Contact

- Daniel Chinome

- Contact: danielchinomedev@gmail.com

- [LinkedIn](https://www.linkedin.com/in/danielchinome/)