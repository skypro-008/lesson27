from django.http import JsonResponse

from vacancies.models import Vacancy


def index(request):
    if request.method == "GET":
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


def get(request, vacancy_id):
    if request.method == "GET":
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
        })
