import os

from invoke import run, task

db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
env = {'PYTHONUNBUFFERED': 'TRUE', 'DATABASE_URL': db_url}


@task
def generatemigrations(context, message):
    if not message:
        raise Exception("Migration message must be defined")
    run('alembic revision --autogenerate -m "' + message + '"', env=env)


@task
def createmigration(context, message):
    if not message:
        raise Exception("Migration message must be defined")
    run('alembic revision -m "' + message + '"', env=env)


@task
def migratedb(context):
    run('alembic upgrade head', env=env, hide=False)


@task
def downgradedb(context, version):
    run('alembic downgrade ' + str(version), env=env)
