from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.models import IPLookup  # Import your models
import os

# this is the Alembic Config object, which provides access to the .ini file.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.environ.get("DB_USER"))
config.set_section_option(section, "DB_PASS", os.environ.get("DB_PASS"))
config.set_section_option(section, "DB_HOST", os.environ.get("DB_HOST"))


# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your models' metadata here.
target_metadata = Base.metadata

def run_migrations_offline():
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
