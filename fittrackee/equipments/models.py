from datetime import datetime, timedelta
from typing import Dict

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.schema import UniqueConstraint

from fittrackee import db

BaseModel: DeclarativeMeta = db.Model


WorkoutEquipment = db.Table(
    'workout_equipments',
    db.Column(
        'workout_id',
        db.Integer,
        db.ForeignKey('workouts.id', ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        'equipment_id',
        db.Integer,
        db.ForeignKey('equipments.id', ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Equipment(BaseModel):
    __tablename__ = 'equipments'
    # a single user can only have one equipment with the same label
    __table_args__ = (
        UniqueConstraint(
            'label',
            'user_id',
            name='equipment_user_label_unique',
        ),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True, nullable=False
    )
    label = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(200), default=None, nullable=True)
    equipment_type_id = db.Column(
        db.Integer, db.ForeignKey('equipment_types.id')
    )
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    workouts = db.relationship(
        'Workout', secondary=WorkoutEquipment, back_populates='equipments'
    )

    def __repr__(self) -> str:
        return f'<Equipment {self.id!r} {self.label!r}>'

    def __init__(
        self,
        label: str,
        equipment_type_id: int,
        description: str,
        user_id: int,
        is_active: bool,
    ) -> None:
        self.label = label
        self.equipment_type_id = equipment_type_id
        self.description = description
        self.user_id = user_id
        self.is_active = is_active

    def serialize(self) -> Dict:
        serialized_equipment = {
            'id': self.id,
            'user_id': self.user_id,
            'label': self.label,
            'equipment_type': self.equipment_type.serialize(),
            'description': self.description,
            'creation_date': self.creation_date,
            'is_active': self.is_active,
            'total_distance': float(sum([w.distance for w in self.workouts])),
            'total_duration': str(
                sum([w.duration for w in self.workouts], timedelta())
            ),
            'workouts_count': len(self.workouts),
        }
        return serialized_equipment


class EquipmentType(BaseModel):
    __tablename__ = 'equipment_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    equipments = db.relationship(
        'Equipment',
        lazy='select',
        backref=db.backref(
            'equipment_type', lazy='joined', single_parent=True
        ),
    )

    def __repr__(self) -> str:
        return f'<EquipmentType {self.label!r}>'

    def __init__(self, label: str, is_active: bool) -> None:
        self.label = label
        self.is_active = is_active

    def serialize(self, is_admin: bool = False) -> Dict:
        serialized_equipment_type = {
            'id': self.id,
            'label': self.label,
            'is_active': self.is_active,
        }
        if is_admin:
            serialized_equipment_type['has_equipments'] = (
                len(self.equipments) > 0
            )
        return serialized_equipment_type