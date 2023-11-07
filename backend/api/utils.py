def create_txt(request):
    shopping_list = 'Список покупок: \n'
    shopping_list += '\n'.join([
        f' • {ingredient["ingredient__name"]} '
        f'{ingredient["amount"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in request
    ])
    return shopping_list
