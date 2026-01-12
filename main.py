from ingredients import search_ingredient, extract_nutrients, extract_portion

result = search_ingredient("banana raw")
dict_nutrient = extract_nutrients(result)
portion = extract_portion(result)
print(dict_nutrient)
print(portion)
