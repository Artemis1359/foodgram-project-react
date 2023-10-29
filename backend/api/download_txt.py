from django.http import HttpResponse


def create_txt(request):
    shopping_list = 'Список покупок: \n'
    shopping_list += '\n'.join([
        f' • {ingredient["ingredient__name"]} '
        f'{ingredient["amount"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in request
    ])
    filename = 'shopping_list.txt'
    response = HttpResponse(
        shopping_list, content_type='text.txt; charset=utf-8'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
