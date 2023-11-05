# Vacancies portal backend

A backend developed with django framework (python), it is important to consider that it was used aws s3 to save curriculum files, so you will need this service to run the project, otherwise you will need to use another service and configure it by yourself

## Installation

1. Clone repository
2. Initialize a virtual environment
3. Install dependencies from `requirements.txt` with
```
pip install -r requirements.txt
```
4. Copy `.env.template` file and rename it to `.env` and fill needed variables
5. Run project with
```
python manage.py runserver
```