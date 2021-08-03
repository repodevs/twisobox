start:
	uvicorn main:app --reload

db-generate:
	alembic revision --autogenerate -m "${msg}"

db-upgrade:
	alembic upgrade head

db-upgrade-sql:
	alembic upgrade head --sql

db-downgrade:
	alembic downgrade -1
