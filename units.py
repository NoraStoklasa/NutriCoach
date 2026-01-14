UNIT_WEIGHTS = {
    "Hard Boiled Egg": 50,
}


UNIT_WEIGHTS = {
    # Eggs
    "Hard Boiled Egg": 50,  # 1 medium egg (without shell)
    # Fruit
    "Apple": 150,  # medium apple
    "Banana": 120,  # medium banana (peeled)
    "Orange": 130,  # medium orange
    # Bread & bakery
    "Toast": 35,  # 1 slice of toast
    "Slice of bread": 35,
    "Bread white": 35,
    "Bread wholemeal": 35,
    # Vegetables (common unit-style ones)
    "Tomato": 100,  # medium tomato
    "Carrot": 60,  # medium carrot
    # Dairy / spreads (optional – only if you want)
    "Cheese slice": 20,  # 1 slice
}


def format_portion(name, grams):
    unit_weight = UNIT_WEIGHTS.get(name)

    # No unit → grams only
    if not unit_weight:
        return f"{grams} g"

    units = grams / unit_weight

    if units < 1.25:
        unit_text = "1 egg"
    elif units < 1.75:
        unit_text = "1.5 eggs"
    else:
        unit_text = f"{round(units)} eggs"

    return f"{unit_text} ({grams} g)"
