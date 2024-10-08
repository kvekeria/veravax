"""empty message

Revision ID: 8e5e26a2ad0c
Revises: 572585662f47
Create Date: 2024-02-02 22:15:05.273655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e5e26a2ad0c'
down_revision = '572585662f47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default='now()', nullable=False),
    sa.Column('series_complete_janssen_5plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_moderna_5plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_pfizer_5plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_janssen_12plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_moderna_12plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_pfizer_12plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_janssen_18plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_moderna_18plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_pfizer_18plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_janssen_65plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_moderna_65plus', sa.Integer(), nullable=True),
    sa.Column('series_complete_pfizer_65plus', sa.Integer(), nullable=True),
    sa.Column('additional_doses_moderna', sa.Integer(), nullable=True),
    sa.Column('additional_doses_pfizer', sa.Integer(), nullable=True),
    sa.Column('additional_doses_janssen', sa.Integer(), nullable=True),
    sa.Column('second_booster_moderna', sa.Integer(), nullable=True),
    sa.Column('second_booster_pfizer', sa.Integer(), nullable=True),
    sa.Column('second_booster_janssen', sa.Integer(), nullable=True),
    sa.Column('distributed_janssen', sa.Integer(), nullable=True),
    sa.Column('distributed_moderna', sa.Integer(), nullable=True),
    sa.Column('distributed_pfizer', sa.Integer(), nullable=True),
    sa.CheckConstraint('created_at IS NOT NULL OR series_complete_janssen_5plus IS NOT NULL OR series_complete_moderna_5plus IS NOT NULL OR series_complete_pfizer_5plus IS NOT NULL OR series_complete_janssen_12plus IS NOT NULL OR series_complete_moderna_12plus IS NOT NULL OR series_complete_pfizer_12plus IS NOT NULL OR series_complete_janssen_18plus IS NOT NULL OR series_complete_moderna_18plus IS NOT NULL OR series_complete_pfizer_18plus IS NOT NULL OR series_complete_janssen_65plus IS NOT NULL OR series_complete_moderna_65plus IS NOT NULL OR series_complete_pfizer_65plus IS NOT NULL OR additional_doses_moderna IS NOT NULL OR additional_doses_pfizer IS NOT NULL OR additional_doses_janssen IS NOT NULL OR second_booster_moderna IS NOT NULL OR second_booster_pfizer IS NOT NULL OR second_booster_janssen IS NOT NULL OR distributed_janssen IS NOT NULL OR distributed_moderna IS NOT NULL OR distributed_pfizer IS NOT NULL', name='at_least_one'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('location', 'date', name='date_location_uc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_data')
    # ### end Alembic commands ###
