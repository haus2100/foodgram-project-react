def shopping_cart_text(ingredients):
    shopping_cart = 'Список покупок \n\n'
    for ingredient in ingredients:
        shopping_list += (
            f"{ingredient['ingredient__name']} "
            f"({ingredient['ingredient__measurement_unit']}) - "
            f"{ingredient['amount__sum']}\n"
        )
    return shopping_cart
