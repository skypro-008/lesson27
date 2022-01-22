import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


@method_decorator(csrf_exempt, name='dispatch')
class VacancyView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()

        search_text = request.GET.get("text", None)
        if search_text:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy()
        vacancy.slug = vacancy_data["slug"]
        vacancy.text = vacancy_data["text"]
        vacancy.status = vacancy_data["status"]
        vacancy.created = vacancy_data["created"]
        try:
            vacancy.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        vacancy.save()
        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
        })


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        try:
            vacancy = self.get_object()
        except Vacancy.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
        })
