# env.py (inside your alembic folder)

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database.db import Base  # Adjust this import based on your actual path

# Import the Alembic config
config = context.config  # This should be initialized automatically

# Set the target metadata for autogenerate migrations
target_metadata = Base.metadata

# Other Alembic configurations...


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option(
        "sqlalchemy.url")  # Get URL from Alembic config
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
