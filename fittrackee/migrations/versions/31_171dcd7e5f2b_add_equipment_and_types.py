"""Add equipment and equipment types for workouts

Revision ID: 171dcd7e5f2b
Revises: 374a670efe23
Create Date: 2023-03-20 22:50:47.672811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '171dcd7e5f2b'
down_revision = '374a670efe23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.execute(
        """
        INSERT INTO equipment_type (label, is_active)
        VALUES 
        ('Shoe', True), ('Bike', True), ('Treadmill', True), 
        ('Bike Trainer', True), ('Kayak/Boat', True),
        ('Skis', True), ('Snowshoes', True) 
        """
    )

    op.create_table('equipment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('equipment_type_id', sa.Integer(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['equipment_type_id'], ['equipment_type.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_equipment_user_id'), ['user_id'], unique=False)

    op.create_table('equipment_workout',
    sa.Column('equipment_id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('equipment_id', 'workout_id')
    )
    with op.batch_alter_table('users_sports_preferences', schema=None) as batch_op:
        batch_op.add_column(sa.Column('default_equipment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'equipment', ['default_equipment_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_sports_preferences', schema=None) as batch_op:
        batch_op.drop_constraint('users_sports_preferences_default_equipment_id_fkey', type_='foreignkey')
        batch_op.drop_column('default_equipment_id')

    op.drop_table('equipment_workout')
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_equipment_user_id'))

    op.drop_table('equipment')
    op.drop_table('equipment_type')
    # ### end Alembic commands ###
