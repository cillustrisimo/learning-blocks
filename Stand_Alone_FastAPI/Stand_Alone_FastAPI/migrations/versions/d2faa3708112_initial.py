"""initial

Revision ID: d2faa3708112
Revises: 
Create Date: 2023-09-24 06:25:58.742080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2faa3708112'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('academicSessions',
    sa.Column('sourcedId', sa.String(length=256), nullable=False),
    sa.Column('status', sa.Enum('active', 'tobedeleted', 'inactive', name='enum1'), nullable=False),
    sa.Column('dateLastModified', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('gradingPeriod', 'semester', 'schoolYear', 'term', name='enum2'), nullable=False),
    sa.Column('startDate', sa.Date(), nullable=True),
    sa.Column('EndDate', sa.Date(), nullable=True),
    sa.Column('parentSourcedId', sa.String(length=256), nullable=False),
    sa.Column('SchoolYear', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('sourcedId', 'parentSourcedId'),
    sa.UniqueConstraint('parentSourcedId'),
    sa.UniqueConstraint('sourcedId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('academicSessions')
    # ### end Alembic commands ###