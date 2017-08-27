import pytest
from codeschool.sparta.models import organize_groups
from codeschool.sparta.models import SpartaActivity, SpartaGroup, SpartaMembership, UserGrade, create_initial_groups
from codeschool.accounts.factories import UserFactory


class TestOrganizeGroups:
    def test_groups_user_quantity_less_group_size(self):
        users = {'paul': 9, 'john': 10, 'ringo': 6, 'george': 8}
        expect_groups = [{'john': 10, 'paul': 9, 'george': 8, 'ringo': 6}]
        assert organize_groups(users, 5) == expect_groups

    def test_groups_quantity_of_members(self):
        users = {
            'george': 8, 'italo': 5.5, 'john': 10, 'maria': 4.6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9,
            'ringo': 6, 'sebastian': 8.5, 'carol': 8
        }
        quantity_users_first = len(organize_groups(users, 5)[0])
        quantity_users_second = len(organize_groups(users, 5)[1])
        assert quantity_users_first == 6
        assert quantity_users_second == 5

    def test_groups_members_expect(self):
        users = {
            'george': 8.5, 'italo': 5.5, 'john': 10, 'maria': 4.6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9
        }
        expect_groups = [
            {'john': 10, 'paul': 0, 'bartolomeu': 8, 'maria': 4.6},
            {'george': 8.5, 'eduardo': 1, 'italo': 5.5, 'joao': 4.9}
        ]
        assert organize_groups(users, 4) == expect_groups

    def test_groups_menbers_remaining_one(self):
        users = {
            'george': 8.5, 'italo': 5.5, 'john': 10, 'maria': 4.6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9, 'barbara': 5
        }
        expect_groups = [
            {'john': 10, 'paul': 0, 'bartolomeu': 8, 'maria': 4.6, 'barbara': 5},
            {'george': 8.5, 'eduardo': 1, 'italo': 5.5, 'joao': 4.9}
        ]
        assert organize_groups(users, 4) == expect_groups

    def test_groups_menbers_remaining_two(self):
        users = {
            'george': 8.5, 'italo': 5.5, 'john': 10, 'maria': 4.6, 'hugo': 6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9, 'barbara': 5
        }
        expect_groups = [
            {'john': 10, 'paul': 0, 'bartolomeu': 8, 'maria': 4.6, 'barbara': 5},
            {'george': 8.5, 'eduardo': 1, 'hugo': 6, 'joao': 4.9, 'italo': 5.5}
        ]
        assert organize_groups(users, 4) == expect_groups


class TestCreateInitialGroups:
    @pytest.mark.django_db
    def test_create_two_groups_with_two_students(self):
        # Creating students and their grades in database to be able to create initial groups
        grades = [10,100,50,80]
        teacher, *students = UserFactory.create_batch(5)
        activity = SpartaActivity.objects.create(teacher=teacher, groups_size=2, title='Sparta')
        user_grades = [
            UserGrade.objects.create(grade=grade, activity=activity, user=student)
            for student, grade in zip(students, grades)
        ]

        create_initial_groups(activity)

        groups =  activity.groups.all()
        assert len(groups) == 2

        g1, g2 = groups
        u1, u2, u3, u4 = students
        assert {u1, u2}.issubset(g1.members.all())