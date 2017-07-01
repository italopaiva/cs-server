from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.apps import apps

from codeschool import models
from codeschool.utils.phrases import phrase, random_sparta_phrase
from itertools import cycle



class SpartaGroup(models.TimeStampedModel):
    """
    Represents a group of students in a Sparta activity.
    """

    activity = models.ForeignKey('SpartaActivity', related_name='groups')
    name = models.CharField(
        _('Name'),
        blank=True,
        max_length=40,
    )
    members = models.ManyToManyField(
        models.User,
        through='SpartaMembership',
        related_name='sparta_groups'
    )

    @property
    def learner(self):
        role = SpartaMembership.ROLE_LEARNER
        return SpartaMembership.objects.filter(group=self, role=role)

    @property
    def tutors(self):
        role = SpartaMembership.ROLE_TUTOR
        return SpartaMembership.objects.filter(group=self, role=role)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        unique_together = [
            ('name', 'activity'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            return super().save(*args, **kwargs)

        max_iter = 10
        for n in range(max_iter):
            try:
                self.name = random_sparta_phrase()
                return super().save(*args, **kwargs)
            except IntegrityError:
                if n == max_iter - 1:
                    raise


class SpartaMembership(models.TimeStampedModel):
    """
    Describes the membership relation for each group
    """

    ROLE_TUTOR = 0
    ROLE_LEARNER = 1
    ROLE_MAPPING = {
        'learner': ROLE_LEARNER,
        'tutor': ROLE_TUTOR,
    }

    user = models.ForeignKey(models.User, related_name='+')
    group = models.ForeignKey(SpartaGroup, related_name='+')
    role = models.IntegerField(
        choices=[
            (ROLE_TUTOR, _('tutor')),
            (ROLE_LEARNER, _('learner')),
        ]
    )

    class Meta:
        unique_together = [
            ('user', 'group', 'role'),
        ]



def organize_groups(mapping, group_size):
    """
    Receives a mapping from users to grades and return a list of groups
    with the approximate ``group_size``.

    It tries to match users with the best grades with the users with the
    worst grades.

    Args:
        mapping (map):
            A dictionary from users to their respective grades.
        group_size (int):
            The desired group size.
    Examples:

        >>> users = {'john': 10, 'paul': 9, 'george': 8, 'ringo': 6}
        >>> organize_groups(users, 2)
        [{'john': 10,'ringo': 6}, {'paul': 8, 'george': 8}]
    """
    users_quantity = len(mapping)

    if group_size > users_quantity:
        return [mapping.copy()]

    n_groups = users_quantity // group_size
    remaining_users = users_quantity % group_size

    # Initialize possible groups as empty lists
    groups = [{} for _ in range(n_groups)]

    sorted_users = sorted(mapping.items(), key=lambda x: x[1])

    for idx in cycle([0, -1]):
        if len(sorted_users) < n_groups:
            break

        for i in range(n_groups):
            name, grade = sorted_users.pop(idx)
            groups[i][name] = grade

    j = 0
    for i, user in enumerate(sorted_users):
        name = user[0]
        grade = user[1]
        if j == n_groups:
            j = 0
        groups[j][name] = grade
        j += 1
    return groups


def create_unique_phrases(n):
    phrases = {random_sparta_phrase() for _ in range(n)}
    while len(phrases) < n:
        phrases.add(random_sparta_phrase())
    return list(phrases)


def create_initial_groups(activity):
    """
    Create the initial groups for an Sparta Activity.
    """
    user_grades = activity.user_grades.all()
    mapping = {user_id: grade for user_id, grade in user_grades.values_list('user', 'grade')}
    groups = organize_groups(mapping, activity.groups_size)

    # Inserting all sparta groups in bulk
    phrases = create_unique_phrases(len(groups))
    group_objects = [SpartaGroup(activity=activity, name=phrase) for phrase in phrases]
    SpartaGroup.objects.bulk_create(group_objects)
    group_objects = SpartaGroup.objects.filter(activity=activity)

    # Inserting group members in bulk
    members = []
    for mapping, group in zip(groups, group_objects):
        for user_id, user_grade in mapping.items():
            if user_grade >= activity.grade_threshold:
                role = SpartaMembership.ROLE_TUTOR
            else:
                role = SpartaMembership.ROLE_LEARNER
            membership = SpartaMembership(user_id=user_id, group=group, role=role)
            members.append(membership)

    SpartaMembership.objects.bulk_create(members)
