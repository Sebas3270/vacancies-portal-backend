from rest_framework import serializers
from .models import Vacancy, CandidatesApplied

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class CandidatesAppliedSerializer(serializers.ModelSerializer):

    vacancy = VacancySerializer()

    class Meta:
        model = CandidatesApplied
        fields = ('user','resume','appliedAt', 'vacancy')