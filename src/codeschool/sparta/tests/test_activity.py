from codeschool.accounts.factories import UserFactory
from codeschool.models import User
from codeschool.sparta.models import SpartaActivity, UserGrade
from codeschool.sparta.models.activity import read_csv_file

import pytest
from mock import patch, Mock, MagicMock, mock
from types import SimpleNamespace


class TestActivity:
    activity_class = SpartaActivity
    submission_payload = {}

    @pytest.fixture
    def activity(self):
        cls = self.activity_class
        result = cls(title='Test', id=1)
        result.specific = result
        return result

    # Mocked fixtures
    user = pytest.fixture(lambda self: Mock(id=2, username='user'))

    def test_read_csv(self):
        data = read_csv_file('a;1\nb;2')
        assert data[0] == ('a', 1.0)

    def test_create_user_grades(self, activity: SpartaActivity):
        csv_data = 'a;1\nb;2'
        users = [User(username='a'), User(username='b')]

        def patched(**kwargs):
            return users

        with patch.object(User.objects, 'filter', patched):
            print(activity, type(activity))
            objs = activity.populate_from_csv(csv_data, commit=False)

        assert len(objs) == 2
        grade1, grade2 = objs
        assert grade1.grade == 1.0

    def test_create_post_grade_csv(self, activity: SpartaActivity):
        csv_data_should_be = 'a;1\nb;4\nc;5\n'

        with patch.object(UserGrade, 'user', None):
            users = [
                Mock(spec=User, id=1, username='a'),
                Mock(spec=User, id=2, username='b'),
                Mock(spec=User, id=3, username='c')
            ]

            users_grade = [
                UserGrade(user=users[0], grade=1, activity=activity),
                UserGrade(user=users[1], grade=2, post_grade=4, activity=activity),
                UserGrade(user=users[2], grade=3, post_grade=5, activity=activity)
            ]


            ns = SimpleNamespace(all=lambda: users_grade, select_related=lambda self: ns)

            with patch.object(SpartaActivity, 'user_grades', ns):
                csv = activity.create_post_grade_csv()

                assert csv == csv_data_should_be


class TestUserGrade:
    @pytest.fixture
    def activity_with_grades(self):
        # Creating students and their grades in database to be able to change the grade
        grades = [10,100,50,80]
        teacher, *students = UserFactory.create_batch(5)
        activity = SpartaActivity.objects.create(teacher=teacher, groups_size=2, title='Sparta')
        for student, grade in zip(students, grades):
            UserGrade.objects.create(grade=grade, activity=activity, user=student)
        return (activity, students)

    @pytest.mark.django_db
    def test_grade_update_of_a_single_user(self, activity_with_grades):
        activity, students = activity_with_grades
        first_student = students[0]
        new_grade = 75
        mapping = {str(first_student.pk): new_grade}

        UserGrade.update_activity_grades(activity, mapping)

        first_student_grade = activity.user_grades.get(user=first_student)
        assert first_student_grade.grade == new_grade

    @pytest.mark.django_db
    def test_grades_update_of_two_users(self, activity_with_grades):
        activity, students = activity_with_grades
        second_student = students[1]
        third_student = students[2]
        second_new_grade = 0
        third_new_grade = 35.5
        mapping = {
            str(second_student.pk): second_new_grade,
            str(third_student.pk): third_new_grade,
        }

        UserGrade.update_activity_grades(activity, mapping)

        second_student_grade = activity.user_grades.get(user=second_student)
        assert second_student_grade.grade == second_new_grade

        third_student_grade = activity.user_grades.get(user=third_student)
        assert third_student_grade.grade == third_new_grade