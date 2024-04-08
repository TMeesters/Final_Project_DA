import re
from utils import extract_text_from_image, parse_nutrition_facts, display_nutrition_info


def calculate_points_for_fat(fat_amount):
    if fat_amount <= 3:
        return 0
    elif 3 < fat_amount <= 17.5:
        return 1
    else:
        return 2

def calculate_points_for_sugar(sugar_amount):
    if sugar_amount <= 4:
        return 0
    elif 4 < sugar_amount <= 9:
        return 1
    else:
        return 2
    
def calculate_points_for_protein(protein_amount):
    if protein_amount >= 8:
        return 0
    elif 6 <= protein_amount < 8:
        return 1
    else:
        return 2

def calculate_points_for_energy(energy_amount):
    if energy_amount <= 80:
        return 0
    elif 80 < energy_amount <= 160:
        return 1
    elif 160 < energy_amount <= 280:
        return 2
    elif 280 < energy_amount <= 400:
        return 3
    elif 400 < energy_amount <= 520:
        return 4
    else:
        return 5

def calculate_points_for_saturated_fat(saturated_fat_amount):
    if saturated_fat_amount <= 1:
        return 0
    elif 1 < saturated_fat_amount <= 4:
        return 1
    elif 4 < saturated_fat_amount <= 8:
        return 2
    elif 8 < saturated_fat_amount <= 12:
        return 3
    elif 12 < saturated_fat_amount <= 16:
        return 4
    else:
        return 5

def calculate_points_for_fruit_vegetables_pulses(fvp_amount):
    if fvp_amount >= 80:
        return 0
    elif 40 <= fvp_amount < 80:
        return 1
    else:
        return 2

def calculate_points_dynamically(nutrition_facts):
    point_calculations = {
        'Total Fat': calculate_points_for_fat,
        'Total Sugars': calculate_points_for_sugar,
        'Protein': calculate_points_for_protein,
        'Energy': calculate_points_for_energy,
        'Saturated Fat': calculate_points_for_saturated_fat,
        'Fruit, Vegetables, Pulses': calculate_points_for_fruit_vegetables_pulses,
    }

    for component, calculation_function in point_calculations.items():
        if component in nutrition_facts and isinstance(nutrition_facts[component], dict) and 'value' in nutrition_facts[component]:
            value = nutrition_facts[component]['value']
            if value != "less than 1":
                points = calculation_function(float(value))
            else:
                points = 0
            nutrition_facts[f'{component} Points'] = points

    return nutrition_facts


extracted_text = """Nutrition Facts 30 Servings per container Serving size Amount per serving Calories 1 tbsp (14g) 35 I can't believe it's not Butter! % Daily Value Total Fat 4g Saturated Fat 1g 5% 5% Polyunsaturated Fat 2g Monounsaturated Fat 1g Sodium 85mg 4% A GOOD SOURCE OF OMEGA 3-ALA* Og TRANS FAT PER SERVING AND NO PARTIALLY HYDROGENATED OILS 60% FEWER CALORIES THAN BUTTER 80% LESS SATURATED Total Carbohydrate Og 0% FAT THAN BUTTER* Protein Og *CONTAINS 190mg OF OMEGA-3 ALA PER SERVING (11% OF THE 1.6g DAILY VALUE) *TOTAL FAT IS 4g PER SERVING. Vitamin A 15% Not a significant source of trans fat, cholesterol, dietary fiber, total sugars, added sugars, vitamin D, calcium, iron and potassium. INGREDIENTS: PURIFIED WATER, SOYBEAN OIL, PALM KERNEL AND PALM OIL, SALT, LECITHIN (SOY), MONO AND DIGLYCERIDES, VINGEGAR NATURAL FLAVORS, VITAMIN A PALMITATE, BETA CAROTENE (COLOR)."""
parsed_nutrition_facts = parse_nutrition_facts(extracted_text)
print("Extracted Text:")
print(extracted_text)
display_nutrition_info(parsed_nutrition_facts)


def calculate_nutrient_points(nutrition_facts):
    point_calculations = {
        'Total Fat': calculate_points_for_fat,
        'Total Sugars': calculate_points_for_sugar,
        'Protein': calculate_points_for_protein,
        'Energy': calculate_points_for_energy,
        'Saturated Fat': calculate_points_for_saturated_fat,
        'Dietary Fibre': calculate_points_for_dietary_fiber,
        'Fruit, Vegetables, Pulses': calculate_points_for_fruit_vegetables_pulses,
    }

    for component, calculation_function in point_calculations.items():
        if component in nutrition_facts and isinstance(nutrition_facts[component], dict) and 'value' in nutrition_facts[component]:
            value = nutrition_facts[component]['value']
            if value != "less than 1":
                points = calculation_function(float(value))
            else:
                points = "less than one"
            nutrition_facts[f'{component} Points'] = points

    return nutrition_facts

def calculate_nutri_score(nutrition_facts):
    negative_thresholds = {
        'Energy': [335, 670, 1005, 1340, 1675],
        'Total Sugars': [4.5, 9, 13.5, 18, 22.5],
        'Saturated Fat': [1, 2, 3, 4, 5],
        'Sodium': [90, 180, 270, 360, 450]
    }
    negative_multiplier = [1, 1, 1, 1, 1] 

    positive_thresholds = {
        'Fruit, Vegetables, Pulses': [40, 80, 120, 160, 200],
        'Dietary Fibre': [0.9, 1.9, 2.8, 3.7, 4.7],
        'Protein': [1.6, 3.2, 4.8, 6.4, 8]
    }
    positive_multiplier = [-1, -1, -1, -1, -1] 
    
    total_points = 0

    for nutrient, value in nutrition_facts.items():
        if nutrient in negative_thresholds and isinstance(value, dict) and 'value' in value:  
            for i, threshold in enumerate(negative_thresholds[nutrient]):
                if float(value['value']) > threshold:  # Convert value to float
                    total_points += negative_multiplier[i]
                    break

        elif nutrient in positive_thresholds and isinstance(value, dict) and 'value' in value:
            for i, threshold in enumerate(positive_thresholds[nutrient]):
                if float(value['value']) >= threshold:
                    total_points += positive_multiplier[i]
                    break

    if total_points <= -1:
        nutri_score = 'A'
    elif -1 < total_points <= 2:
        nutri_score = 'B'
    elif 2 < total_points <= 10:
        nutri_score = 'C'
    elif 10 < total_points <= 18:
        nutri_score = 'D'
    else:
        nutri_score = 'E'

    return total_points, nutri_score

# Calculate points dynamically
nutrition_facts_with_points = calculate_points_dynamically(parsed_nutrition_facts)

# Calculate Nutri-score
total_points, nutri_score = calculate_nutri_score(nutrition_facts_with_points)

print("Total Points:", total_points)
print("Nutri-Score:", nutri_score)