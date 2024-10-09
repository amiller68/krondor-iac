# NOTE (amiller68): most of this file is autogenerated
#  Additions are explicitly noted
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
# NOTE (amiller68): import our models and os
from app.database.database import SyncDatabase, Base 
from dotenv import load_dotenv

import os

# NOTE (amiller68): get the database URL from the environment.
#  The default is intentionally malformed to force common configuration path
# NOTE (amiller68): 'models' calls `load_dotenv` so we don't need to do it here.
#  Note that this means .env is going to overwrite anything you set directly
load_dotenv()
database_path = os.getenv("DATABASE_PATH")

# Note (amiller68): Initialize our client -- in turn updating Base
SyncDatabase(database_path)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# NOTE (amiller68): specify the database URL from the environment
database_url = f"sqlite:///{database_path}"
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

print("Detected tables:")
for table in Base.metadata.tables:
    print(f"- {table}")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# NOTE (amiller68): enable our models
target_metadata = None 

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = engine_from_config(
                config.get_section(config.config_ini_section), prefix='sqlalchemy.')

    with engine.connect() as connection:
        context.configure(
                    connection=connection,
                    target_metadata=target_metadata
                    )

        with context.begin_transaction():
            context.run_migrations()

def process_revision_directives(context, revision, directives):
    # This function will be called for each migration script that's generated.
    # We can use it to modify the migration script if needed.
    if config.cmd_opts.autogenerate:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("No changes detected; no migration script generated.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()