from typing import Dict, Optional

from flask import Flask

from fittrackee import db
from fittrackee.equipment.models import Equipment, EquipmentType
from fittrackee.users.models import User, UserSportPreference
from fittrackee.workouts.models import Sport, Workout


class TestEquipmentModel:
    @staticmethod
    def assert_equipment_model(equip: Equipment) -> Dict:
        assert 1 == equip.id
        assert 'Test bike equipment' == equip.label
        assert '<Equipment 1 \'Test bike equipment\'>' == str(equip)

        serialized_equip = equip.serialize()
        assert serialized_equip['id'] == equip.id
        assert serialized_equip['user_id'] == 1
        assert serialized_equip['label'] == equip.label
        assert serialized_equip['equipment_type'] == 2
        assert serialized_equip['description'] == 'A bike for testing purposes'
        assert serialized_equip['is_active'] is True
        return serialized_equip

    def test_equipment_model_without_workout(
        self, 
        app: Flask, 
        user_1: User,
        equipment_type_1_shoe: EquipmentType,
        equipment_type_2_bike: EquipmentType,
        equipment_1_bike: Equipment,
    ) -> None:
        serialized_equip = self.assert_equipment_model(equipment_1_bike)
        assert len(serialized_equip['workouts']) == 0
        assert serialized_equip['total_distance'] == 0
        assert serialized_equip['total_duration'] == '0:00:00'

    def test_equipment_model_with_workout(
        self,
        app: Flask,
        sport_1_cycling: Sport,
        equipment_type_1_shoe: EquipmentType,
        equipment_type_2_bike: EquipmentType,
        user_1: User,
        workout_cycling_user_1: Workout,
        equipment_1_bike: Equipment
    ) -> None:
        equipment_1_bike.workouts.append(workout_cycling_user_1)
        db.session.add(equipment_1_bike)
        db.session.commit()
        serialized_equip = self.assert_equipment_model(equipment_1_bike)
        assert serialized_equip['total_distance'] == 10.0
        assert serialized_equip['total_duration'] == '1:00:00'
        assert len(serialized_equip['workouts']) == 1


class TestEquipmentTypeModel:
    @staticmethod
    def assert_equipment_type_model(
        equip_type: EquipmentType, is_admin: Optional[bool] = False
    ) -> Dict:
        assert 1 == equip_type.id
        assert 'Shoe' == equip_type.label
        assert '<EquipmentType \'Shoe\'>' == str(equip_type)

        serialized_equip = equip_type.serialize(is_admin=is_admin)
        assert serialized_equip['id'] == equip_type.id
        assert serialized_equip['label'] == equip_type.label
        assert serialized_equip['is_active'] is True
        return serialized_equip

    def test_equipment_type_model(
        self, 
        app: Flask, 
        user_1: User,
        equipment_type_1_shoe: EquipmentType,
        equipment_type_2_bike: EquipmentType,
        equipment_1_bike: Equipment,
    ) -> None:
        serialized_equip_type = self.assert_equipment_type_model(equipment_type_1_shoe)
        assert 'has_workouts' not in serialized_equip_type

    def test_equipment_type_model_as_admin(
        self, 
        app: Flask, 
        user_1: User,
        equipment_type_1_shoe: EquipmentType,
        equipment_type_2_bike: EquipmentType,
        equipment_1_bike: Equipment,
    ) -> None:
        serialized_equip_type = self.assert_equipment_type_model(
            equipment_type_1_shoe, is_admin=True
        )
        assert serialized_equip_type['has_equipment'] is False   