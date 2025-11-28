"""Add cascade delete to foreign keys

Revision ID: 723a69bf82a6
Revises: 05ea06bb8443
Create Date: 2025-11-20 18:43:06.433781

"""
from alembic import op
import sqlalchemy as sa


revision = '723a69bf82a6'
down_revision = '05ea06bb8443'
branch_labels = None
depends_on = None

def upgrade():
    # ASSETS table - USER_ID with CASCADE
    op.drop_constraint('SQL251120040639200', 'ASSETS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040639200', 'ASSETS', 'USERS',
        ['USER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='CASCADE'
    )
    
    # ASSETS table - MANAGER_ID with SET NULL
    op.drop_constraint('SQL251120040639190', 'ASSETS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040639190', 'ASSETS', 'USERS',
        ['MANAGER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='SET NULL'
    )
    
    # PROJECTS table - USER_ID with CASCADE
    op.drop_constraint('SQL251120040639970', 'PROJECTS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040639970', 'PROJECTS', 'USERS',
        ['USER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='CASCADE'
    )
    
    # PROJECTS table - MANAGER_ID with SET NULL
    op.drop_constraint('SQL251120040639960', 'PROJECTS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040639960', 'PROJECTS', 'USERS',
        ['MANAGER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='SET NULL'
    )
    
    # REQUEST table - USER_ID with CASCADE
    op.drop_constraint('SQL251120040640770', 'REQUEST', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040640770', 'REQUEST', 'USERS',
        ['USER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='CASCADE'
    )
    
    # REQUEST table - MANAGER_ID with SET NULL
    op.drop_constraint('SQL251120040640760', 'REQUEST', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040640760', 'REQUEST', 'USERS',
        ['MANAGER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='SET NULL'
    )
    
    # USER_CERT table - USER_ID with CASCADE
    op.drop_constraint('SQL251120040641420', 'USER_CERT', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040641420', 'USER_CERT', 'USERS',
        ['USER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='CASCADE'
    )
    
    # USER_CERT table - MANAGER_ID with SET NULL
    op.drop_constraint('SQL251120040641380', 'USER_CERT', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040641380', 'USER_CERT', 'USERS',
        ['MANAGER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='SET NULL'
    )
    
    # USER_SKILLS table - USER_ID with CASCADE
    op.drop_constraint('SQL251120040641980', 'USER_SKILLS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040641980', 'USER_SKILLS', 'USERS',
        ['USER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='CASCADE'
    )
    
    # USER_SKILLS table - MANAGER_ID with SET NULL
    op.drop_constraint('SQL251120040641970', 'USER_SKILLS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key(
        'SQL251120040641970', 'USER_SKILLS', 'USERS',
        ['MANAGER_ID'], ['USER_ID'],
        source_schema='FSQ87086', referent_schema='FSQ87086',
        ondelete='SET NULL'
    )

def downgrade():
    # Reverse all operations - recreate with NO ACTION
    
    # ASSETS
    op.drop_constraint('SQL251120040639200', 'ASSETS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040639200', 'ASSETS', 'USERS', ['USER_ID'], ['USER_ID'], 
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    op.drop_constraint('SQL251120040639190', 'ASSETS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040639190', 'ASSETS', 'USERS', ['MANAGER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    # PROJECTS
    op.drop_constraint('SQL251120040639970', 'PROJECTS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040639970', 'PROJECTS', 'USERS', ['USER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    op.drop_constraint('SQL251120040639960', 'PROJECTS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040639960', 'PROJECTS', 'USERS', ['MANAGER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    # REQUEST
    op.drop_constraint('SQL251120040640770', 'REQUEST', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040640770', 'REQUEST', 'USERS', ['USER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    op.drop_constraint('SQL251120040640760', 'REQUEST', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040640760', 'REQUEST', 'USERS', ['MANAGER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    # USER_CERT
    op.drop_constraint('SQL251120040641420', 'USER_CERT', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040641420', 'USER_CERT', 'USERS', ['USER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    op.drop_constraint('SQL251120040641380', 'USER_CERT', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040641380', 'USER_CERT', 'USERS', ['MANAGER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    # USER_SKILLS
    op.drop_constraint('SQL251120040641980', 'USER_SKILLS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040641980', 'USER_SKILLS', 'USERS', ['USER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')
    
    op.drop_constraint('SQL251120040641970', 'USER_SKILLS', schema='FSQ87086', type_='foreignkey')
    op.create_foreign_key('SQL251120040641970', 'USER_SKILLS', 'USERS', ['MANAGER_ID'], ['USER_ID'],
                          source_schema='FSQ87086', referent_schema='FSQ87086')