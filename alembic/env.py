from logging.config import fileConfig
from sqlalchemy import pool, event
from alembic import context
import sys
import os
import warnings

# Add parent directory to path FIRST
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# ============================================================
# Register DB2 implementation with warning handling
# ============================================================
from alembic.ddl import impl as alembic_impl
from alembic.ddl.impl import DefaultImpl

class DB2Impl(DefaultImpl):
    """Custom Alembic DDL implementation for IBM DB2 with warning handling"""
    __dialect__ = 'ibm_db_sa'
    transactional_ddl = True
    
    def __init__(self, dialect, connection, as_sql, transactional_ddl, output_buffer, context_opts):
        super(DB2Impl, self).__init__(
            dialect, connection, as_sql, transactional_ddl, output_buffer, context_opts
        )
    
    def _exec(self, construct, execution_options=None, multiparams=(), params=None):
        """Override _exec to handle DB2-specific warnings"""
        try:
            return super(DB2Impl, self)._exec(construct, execution_options, multiparams, params)
        except Exception as e:
            error_str = str(e)
            # SQL0605W: Index already exists (created by PK constraint)
            # This is a warning, not an error - safe to ignore
            if 'SQL0605W' in error_str or 'SQLCODE=605' in error_str:
                print(f"⚠️  DB2 Info: Index already exists (auto-created by constraint) - continuing...")
                return None
            # SQL0204N: Object does not exist (can happen during drop if already gone)
            elif 'SQL0204N' in error_str or 'SQLCODE=-204' in error_str:
                print(f"⚠️  DB2 Info: Object already dropped - continuing...")
                return None
            else:
                # Re-raise actual errors
                raise

# Register DB2 implementation globally
alembic_impl._impls['ibm_db_sa'] = DB2Impl

print("✅ DB2 dialect implementation registered")

# ============================================================
# Import application components
# ============================================================
from app.core.config import settings
from app.core.database import Base, create_db2_connection

# Import all models
from app.models.users import User
from app.models.skills import Skill
from app.models.user_skills import UserSkill
from app.models.user_cert import UserCert
from app.models.assets import Asset
from app.models.projects import Project
from app.models.request import Request

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = "db2+ibm_db://"
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
    from sqlalchemy import create_engine
    
    connectable = create_engine(
        "db2+ibm_db://",
        creator=create_db2_connection,
        poolclass=pool.NullPool,
        echo=False,
    )
    
    @event.listens_for(connectable, "connect")
    def receive_connect(dbapi_conn, connection_record):
        print("🔗 DB2 connection established for migration")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=False,
            compare_server_default=False,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()