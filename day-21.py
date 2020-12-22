class Food:

    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens

    def __len__(self):
        return len(self.allergens)

    def remove_allergen(self, allergen):
        self.allergens.remove(allergen)

    def remove_ingredient(self, ingredient):
        self.ingredients = list(filter(lambda x: x != ingredient, self.ingredients))

    def contains_ingredient(self, ingredient):
        return ingredient in self.ingredients


def create_foods():
    food_list = []
    with open('inputs/foods.txt', 'r') as file:
        for line in file:
            ingredients, allergens = line.strip().split(' (')
            ingredients = ingredients.split()
            allergens = allergens[9:-1].split(', ')
            food_list.append(Food(ingredients, allergens))
    return food_list


def determine_unsafe_foods():
    foods = create_foods()
    unsafe_foods = {}
    safe_foods = []
    while len(foods) > 0:
        # --- Move food with only one allergen to top of list ---
        for food in foods:
            if len(food) == 1:
                foods.insert(0, foods.pop(foods.index(food)))
                break

        # --- Find all other foods containing the allergen ---
        current = foods[0]
        allergen = current.allergens[0]
        contains_allergen = [food for food in foods[1:] if allergen in food.allergens]

        # --- Check whether an ingredient can be found in all foods with the allergen
        potential_matches = []
        if len(current) == 1 and len(current.ingredients) == 1:
            potential_matches.append(current.ingredients[0])
        for ingredient in current.ingredients:
            if len(potential_matches) > 1:
                break
            if all(map(lambda x: ingredient in x.ingredients, contains_allergen)):
                potential_matches.append(ingredient)

        # --- If a single match found remove the matching ingredient and matching allergen from all foods ---
        if len(potential_matches) == 1:
            unsafe_foods.update({allergen: potential_matches[0]})
            for food in foods[:]:
                if allergen in food.allergens:
                    food.remove_allergen(allergen)
                food.remove_ingredient(potential_matches[0])
                # --- Remove foods without any allergens and check that the unsafe food isn't in the safe food list ---
                if len(food) == 0:
                    safe_foods += food.ingredients
                    foods.remove(food)
            safe_foods = list(filter(lambda x: x != potential_matches[0], safe_foods))
        else:
            foods.append(foods.pop(0))
    return unsafe_foods, safe_foods


translation = determine_unsafe_foods()

# --- Solution 1 ---

print(len(translation[1]))

# --- Solution 2 ---

print([value for _, value in sorted(translation[0].items())])

