from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Vacancy, CandidatesApplied
from .serializers import VacancySerializer, CandidatesAppliedSerializer

from .filters import VacancyFilter

from django.utils import timezone

# Create your views here.
@api_view(['GET'])
def get_all_vacancies(request):
    vacancies = Vacancy.objects.all().order_by('id')
    vacancies_fs = VacancyFilter(request.GET, queryset=vacancies)
    count = vacancies_fs.qs.count()

    resPerPage = 4
    paginator = PageNumberPagination()
    paginator.page_size= resPerPage
    vacancies_qs = paginator.paginate_queryset(vacancies_fs.qs, request)

    vacancies_serialized = VacancySerializer(vacancies_qs, many=True)
    return Response({"resPerPage": resPerPage, "count": count, "vacancies":vacancies_serialized.data})

@api_view(['GET'])
def get_one_vacancy(request, id):
    vacancy = get_object_or_404(Vacancy, id=id)
    candidates_amount = vacancy.candidatesapplied_set.all().count()
    vacancy_serialized = VacancySerializer(vacancy, many=False)
    return Response({
        'vacancy':vacancy_serialized.data,
        'candidates':candidates_amount
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vacancy(request):
    request.data['user'] = request.user.id
    data = request.data
    vacancy_serialized = VacancySerializer(data=data, many=False)
    vacancy_serialized.is_valid(raise_exception=True)
    vacancy_serialized.save()
    return Response(vacancy_serialized.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_vacancy(request, id):
    vacancy = get_object_or_404(Vacancy, id=id)
    data = request.data

    if vacancy.user != request.user: 
        return Response({'detail': "You can not manipulate this resource since you're not the creator"}, status=status.HTTP_401_UNAUTHORIZED)

    vacancy_serialized = VacancySerializer(vacancy,data=data, many=False)
    vacancy_serialized.is_valid(raise_exception=True)
    vacancy_serialized.save()

    return Response(vacancy_serialized.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vacancy(request, id):
    vacancy = get_object_or_404(Vacancy, id=id)

    if vacancy.user != request.user: 
        return Response({'detail': "You can not manipulate this resource since you're not the creator"}, status=status.HTTP_401_UNAUTHORIZED)

    vacancy.delete()
    return Response({'msg': f'vacancy with id {id} deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_vacancy(request, id):
    user = request.user
    vacancy = get_object_or_404(Vacancy, id=id)

    if user.userprofile.resume == '':
        return Response({'detail': "You have not uploaded your resume, you cannot apply"}, status=status.HTTP_400_BAD_REQUEST)
    
    if vacancy.last_date < timezone.now():
        return Response({'detail': "You can not apply to this vacancy, the deathline is over"}, status=status.HTTP_400_BAD_REQUEST)
    
    already_applied = vacancy.candidatesapplied_set.filter(user=user).exists()

    if already_applied:
        return Response({'detail': "You have already applied to this vacancy"}, status=status.HTTP_400_BAD_REQUEST)
    
    vacancyApplied = CandidatesApplied.objects.create(
        vacancy = vacancy,
        user = user,
        resume = user.userprofile.resume
    )

    return Response({
        'applied': True,
        'vacancy_id': vacancy.id,
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_applied_vacancies(request):
    args = {'user_id': request.user.id}
    vacancies = CandidatesApplied.objects.filter(**args)
    serializer = CandidatesAppliedSerializer(vacancies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_applied(request, id):
    user = request.user
    vacancy = get_object_or_404(Vacancy, id=id)
    applied = vacancy.candidatesapplied_set.filter(user=user).exists()
    return Response(applied)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_published_vacancies(request):
    args = {'user_id': request.user.id}
    vacancies = Vacancy.objects.filter(**args)
    serializer = VacancySerializer(vacancies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_candidates_applied(request, id):
    user = request.user
    vacancy = get_object_or_404(Vacancy, id=id)

    if vacancy.user != user:
        return Response({'detail': "You have not access to this vacancy"}, status=status.HTTP_401_UNAUTHORIZED)
    
    candidates = vacancy.candidatesapplied_set.all()
    serializer = CandidatesAppliedSerializer(candidates, many=True)
    return Response(serializer.data)
