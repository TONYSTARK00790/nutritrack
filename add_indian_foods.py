import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

from meals.models import Food

# Comprehensive list of 250+ Indian foods with nutritional data
INDIAN_FOODS = [
    # Breads & Grains
    ('Roti', 'grain', 265, 8.5, 50, 3.5, 2),
    ('Naan', 'grain', 310, 9, 53, 6.5, 1.5),
    ('Paratha', 'grain', 350, 9, 45, 15, 2),
    ('Dosa', 'grain', 180, 5, 32, 3, 2),
    ('Idli', 'grain', 95, 2, 20, 1, 0.5),
    ('Uttapam', 'grain', 200, 6, 38, 2, 1),
    ('Poori', 'grain', 320, 7, 35, 12, 1.5),
    ('Bhakri', 'grain', 280, 7, 55, 2, 4),
    ('Khichdi', 'grain', 120, 4, 24, 1, 0.5),
    ('Puttu', 'grain', 140, 4, 28, 1, 2),
    ('Appam', 'grain', 160, 3, 32, 2, 0.5),
    ('Puri', 'grain', 305, 6, 32, 14, 1),
    
    # Rice Dishes
    ('Biryani', 'non_veg', 180, 8, 28, 4, 1.5),
    ('Fried Rice', 'non_veg', 130, 4, 18, 4, 1),
    ('Tahdig (rice)', 'grain', 180, 3, 40, 1, 0.5),
    ('Pilaf', 'grain', 145, 3, 30, 2, 0.5),
    ('Pulao', 'grain', 155, 3, 32, 3, 1),
    ('Chakli Rice', 'grain', 130, 2, 28, 1, 0.5),
    
    # Curries - Vegetarian
    ('Aloo Gobi', 'veg', 95, 3, 18, 1.5, 3),
    ('Baingan Bharta', 'veg', 80, 2.5, 12, 3, 2.5),
    ('Chana Masala', 'veg', 140, 9, 20, 2, 5),
    ('Chole Bhature', 'veg', 280, 9, 40, 7, 6),
    ('Dal Makhani', 'veg', 165, 9, 15, 8, 4),
    ('Rajma Curry', 'veg', 120, 8, 18, 2, 5),
    ('Sambar', 'veg', 90, 5, 15, 2, 5),
    ('Rasam', 'veg', 35, 1.5, 6, 0.5, 1),
    ('Methi Aloo', 'veg', 110, 3, 16, 4, 2),
    ('Aloo Mutter', 'veg', 95, 4, 16, 2, 2),
    ('Bindi Fry', 'veg', 65, 2, 10, 2, 2),
    ('Paneer Butter Masala', 'veg', 210, 14, 8, 15, 1),
    ('Shahi Paneer', 'veg', 220, 15, 8, 16, 1),
    ('Paneer Tikka Masala', 'veg', 195, 13, 8, 13, 1),
    ('Methi Paneer', 'veg', 180, 12, 6, 13, 1.5),
    ('Palak Paneer', 'veg', 165, 11, 7, 11, 1),
    ('Malai Kofta', 'veg', 240, 8, 20, 14, 2),
    ('Vegetable Korma', 'veg', 155, 4, 14, 9, 2),
    ('Navratan Korma', 'veg', 185, 6, 16, 11, 2),
    ('Matar Mushroom', 'veg', 120, 6, 14, 5, 2),
    ('Bhindi Masala', 'veg', 85, 2.5, 12, 3, 2.5),
    ('Gajar Mutter', 'veg', 80, 3, 14, 2, 2),
    ('Lauki Khichdi', 'veg', 95, 2.5, 20, 0.5, 1),
    ('Mooli Paratha', 'grain', 280, 7, 42, 8, 2),
    ('Aloo Paratha', 'grain', 300, 8, 44, 10, 2),
    ('Paneer Paratha', 'grain', 320, 11, 42, 12, 1.5),
    ('Methi Paratha', 'grain', 290, 8, 42, 9, 2.5),
    
    # Curries - Non-Vegetarian
    ('Butter Chicken', 'non_veg', 160, 16, 4, 9, 0),
    ('Tikka Masala', 'non_veg', 145, 15, 5, 7, 0.5),
    ('Rogan Josh', 'non_veg', 155, 18, 2, 8, 1),
    ('Keema', 'non_veg', 185, 24, 3, 9, 2),
    ('Nihari', 'non_veg', 175, 22, 5, 8, 1),
    ('Haleem', 'non_veg', 200, 18, 18, 7, 4),
    ('Fish Curry', 'non_veg', 130, 20, 2, 5, 1),
    ('Prawn Curry', 'non_veg', 110, 18, 2, 4, 0.5),
    ('Crab Curry', 'non_veg', 125, 19, 3, 4, 1),
    ('Chicken Curry', 'non_veg', 140, 18, 3, 7, 0.5),
    ('Mutton Curry', 'non_veg', 170, 22, 2, 9, 1),
    ('Egg Curry', 'non_veg', 165, 14, 3, 12, 1),
    ('Tandoori Chicken', 'non_veg', 165, 29, 2, 4, 0),
    ('Chicken Tandoori', 'non_veg', 165, 29, 2, 4, 0),
    ('Seekh Kebab', 'non_veg', 210, 25, 2, 12, 1),
    ('Reshmi Kebab', 'non_veg', 195, 22, 3, 11, 0.5),
    ('Fish Fry', 'non_veg', 165, 24, 2, 8, 1.5),
    ('Chicken 65', 'non_veg', 240, 20, 8, 15, 1),
    ('Chicken Lollipop', 'non_veg', 260, 22, 5, 18, 1),
    ('Amritsari Kulcha', 'non_veg', 250, 9, 38, 6, 1),
    
    # Snacks & Street Food
    ('Samosa', 'snack', 260, 6, 27, 14, 2),
    ('Golgappa/Pani Puri', 'snack', 80, 2, 15, 1, 1),
    ('Chaat', 'snack', 150, 3, 22, 6, 2),
    ('Aloo Tikki', 'snack', 180, 3, 22, 8, 2),
    ('Dahi Bhalle', 'snack', 120, 5, 12, 6, 0.5),
    ('Pakora', 'snack', 240, 5, 18, 15, 1.5),
    ('Bhajiya', 'snack', 200, 4, 16, 12, 1),
    ('Momo', 'snack', 130, 5, 20, 3, 1),
    ('Momos Veg', 'snack', 120, 4, 22, 2, 1),
    ('Spring Roll', 'snack', 210, 5, 24, 10, 1.5),
    ('Cutlet', 'snack', 200, 6, 18, 11, 1.5),
    ('Kachori', 'snack', 280, 7, 32, 14, 2),
    ('Jalebi', 'snack', 290, 1, 73, 0.5, 0),
    ('Gulab Jamun', 'snack', 310, 3, 45, 13, 0),
    ('Laddu', 'snack', 350, 6, 45, 17, 2),
    ('Barfi', 'snack', 320, 8, 42, 14, 1),
    ('Kheer', 'snack', 180, 4, 24, 8, 0.5),
    ('Halwa', 'snack', 340, 4, 52, 12, 2),
    ('Laddoo', 'snack', 360, 7, 44, 18, 2),
    ('Chakli', 'snack', 380, 6, 48, 18, 1.5),
    
    # Dals & Legumes
    ('Moong Dal', 'veg', 100, 9, 16, 0.5, 6),
    ('Masoor Dal', 'veg', 115, 9, 20, 0.5, 7),
    ('Chana Dal', 'veg', 120, 8, 22, 1, 5),
    ('Urad Dal', 'veg', 105, 9, 18, 0.5, 6),
    ('Arhar Dal', 'veg', 118, 8.5, 21, 0.5, 6),
    ('Dal Tadka', 'veg', 130, 8.5, 18, 3, 5),
    ('Dal Bhat', 'veg', 140, 9, 24, 1, 5),
    ('Chickpeas', 'veg', 145, 10, 22, 2.5, 6),
    ('Kidney Beans', 'veg', 127, 8.5, 22, 0.5, 6),
    ('Black Beans', 'veg', 132, 9, 24, 0.5, 6),
    
    # Vegetables
    ('Spinach', 'veg', 23, 2.9, 3.6, 0.4, 2.2),
    ('Tomato', 'veg', 18, 0.9, 3.9, 0.2, 1.2),
    ('Onion', 'veg', 40, 1.1, 9, 0.1, 1.7),
    ('Potato', 'veg', 77, 2, 17, 0.1, 2.1),
    ('Carrot', 'veg', 41, 0.9, 10, 0.2, 2.8),
    ('Cucumber', 'veg', 16, 0.7, 3.6, 0.1, 0.5),
    ('Cabbage', 'veg', 25, 1.3, 5.8, 0.1, 2.4),
    ('Cauliflower', 'veg', 25, 1.9, 5, 0.4, 2.4),
    ('Broccoli', 'veg', 34, 2.8, 7, 0.4, 2.4),
    ('Pepper', 'veg', 31, 1, 7.3, 0.3, 1.6),
    ('Peas', 'veg', 81, 5.4, 14.5, 0.4, 5.7),
    ('Beans', 'veg', 31, 1.8, 7, 0.2, 2.7),
    ('Eggplant', 'veg', 25, 0.98, 5.9, 0.2, 3),
    ('Zucchini', 'veg', 17, 1.6, 3.5, 0.4, 1),
    ('Radish', 'veg', 16, 0.7, 3.4, 0.1, 1.6),
    ('Beetroot', 'veg', 43, 1.6, 10, 0.2, 2.8),
    ('Lauki/Bottle Gourd', 'veg', 12, 0.6, 2.5, 0.1, 0.6),
    ('Ridge Gourd', 'veg', 20, 0.8, 4.5, 0.2, 1.2),
    ('Okra/Bhindi', 'veg', 33, 1.9, 7.5, 0.2, 3.7),
    
    # Fruits
    ('Mango', 'fruit', 60, 0.8, 15, 0.3, 1.6),
    ('Banana', 'fruit', 89, 1.1, 23, 0.3, 2.6),
    ('Apple', 'fruit', 52, 0.3, 14, 0.2, 2.4),
    ('Orange', 'fruit', 47, 0.7, 12, 0.3, 2.4),
    ('Guava', 'fruit', 68, 2.6, 14, 0.9, 5.4),
    ('Papaya', 'fruit', 43, 0.6, 11, 0.3, 1.7),
    ('Watermelon', 'fruit', 30, 0.6, 7.6, 0.2, 0.4),
    ('Grapes', 'fruit', 67, 0.6, 17, 0.2, 0.9),
    ('Pineapple', 'fruit', 50, 0.5, 13, 0.1, 1.4),
    ('Strawberry', 'fruit', 32, 0.7, 7.7, 0.3, 2),
    ('Kiwi', 'fruit', 61, 1.1, 15, 0.5, 3),
    ('Pomegranate', 'fruit', 83, 1.7, 19, 1.2, 4),
    ('Coconut', 'fruit', 354, 3.3, 15, 33, 9),
    ('Litchi', 'fruit', 66, 0.8, 17, 0.4, 1.3),
    ('Jackfruit', 'fruit', 94, 1.5, 23, 0.3, 1.5),
    
    # Dairy & Milk Products
    ('Milk', 'dairy', 61, 3.2, 4.8, 3.3, 0),
    ('Yogurt', 'dairy', 59, 3.5, 3.3, 0.4, 0),
    ('Cheese', 'dairy', 402, 25, 1.3, 33, 0),
    ('Ghee', 'dairy', 884, 0, 0, 99, 0),
    ('Butter', 'dairy', 717, 0.9, 0.1, 81, 0),
    ('Paneer', 'dairy', 265, 25, 2, 17, 0),
    ('Curd', 'dairy', 61, 3.5, 3.1, 3.4, 0),
    ('Milk Cream', 'dairy', 337, 2.2, 2.4, 35, 0),
    ('Khoa', 'dairy', 420, 20, 12, 32, 0),
    ('Mozzarella', 'dairy', 280, 28, 3.2, 17, 0),
    
    # Beverages
    ('Tea', 'beverage', 1, 0.3, 0, 0, 0),
    ('Coffee', 'beverage', 2, 0.1, 0, 0, 0),
    ('Lassi', 'beverage', 60, 3, 4, 2.5, 0),
    ('Masala Chai', 'beverage', 25, 0.5, 4, 0.8, 0),
    ('Buttermilk', 'beverage', 40, 3.3, 3, 1, 0),
    ('Coconut Water', 'beverage', 19, 0.7, 3.7, 0.2, 1.2),
    ('Fresh Juice', 'beverage', 45, 0.5, 11, 0.1, 0.5),
    ('Sugarcane Juice', 'beverage', 42, 0.2, 10, 0, 0),
    ('Badam Milk', 'beverage', 100, 3, 6, 7, 0),
    ('Thandai', 'beverage', 95, 3, 8, 6, 1),
    
    # Condiments & Spices
    ('Ghee', 'dairy', 884, 0, 0, 99, 0),
    ('Oil', 'snack', 884, 0, 0, 100, 0),
    ('Mustard Oil', 'snack', 884, 0, 0, 100, 0),
    ('Coconut Oil', 'snack', 892, 0, 0, 99, 0),
    ('Pickle', 'snack', 135, 1.5, 8, 10, 1),
    ('Chutney', 'snack', 160, 2, 10, 12, 1.5),
    ('Sauce', 'snack', 120, 1, 10, 8, 0.5),
    
    # Sweets & Desserts
    ('Rasgulla', 'snack', 230, 5, 42, 3, 0.5),
    ('Sandesh', 'snack', 280, 8, 42, 8, 0),
    ('Kalakand', 'snack', 310, 9, 48, 8, 0),
    ('Peda', 'snack', 340, 6, 52, 12, 0),
    ('Ksar', 'snack', 350, 8, 48, 15, 0.5),
    ('Mysore Pak', 'snack', 350, 8, 45, 16, 1),
    ('Sohan Papdi', 'snack', 360, 6, 50, 15, 2),
    ('Gajak', 'snack', 380, 8, 48, 18, 2),
    ('Burfi', 'snack', 330, 8, 42, 15, 1),
    ('Kheer', 'snack', 180, 4, 24, 8, 0),
    ('Payasam', 'snack', 220, 3, 38, 7, 1),
    ('Phirni', 'snack', 150, 3, 20, 6, 0),
    ('Ras Malai', 'snack', 280, 6, 42, 10, 0),
    ('Rabri', 'snack', 200, 5, 22, 10, 0),
    
    # Regional Specialties
    ('Sambar Rice', 'grain', 145, 3, 32, 1.5, 2),
    ('Curd Rice', 'grain', 140, 3.5, 25, 2, 1),
    ('Lemon Rice', 'grain', 150, 2.5, 32, 2, 1),
    ('Tamarind Rice', 'grain', 155, 2, 34, 2.5, 1),
    ('Coconut Rice', 'grain', 165, 2.5, 32, 4, 1),
    ('Vegetable Rice', 'grain', 130, 2, 28, 1.5, 1.5),
    ('Pongal', 'grain', 160, 4, 28, 4, 1),
    ('Uthappam', 'grain', 200, 6, 38, 2, 1),
    ('Upma', 'grain', 165, 4, 28, 5, 1.5),
    ('Poha', 'grain', 140, 2, 30, 1, 1),
    ('Sabudana Khichdi', 'grain', 220, 2, 50, 2, 1),
    ('Batata Vada', 'snack', 250, 4, 28, 14, 2),
    ('Misal Pav', 'snack', 220, 8, 32, 6, 4),
    ('Pav Bhaji', 'snack', 240, 6, 36, 8, 2),
    ('Vada Pav', 'snack', 280, 7, 38, 12, 2),
    
    # Additional Proteins
    ('Chicken Breast', 'non_veg', 165, 31, 0, 3.6, 0),
    ('Mutton', 'non_veg', 235, 25, 0, 14, 0),
    ('Fish', 'non_veg', 120, 20, 0, 5, 0),
    ('Shrimp', 'non_veg', 99, 24, 0, 0.3, 0),
    ('Egg', 'non_veg', 155, 13, 1.1, 11, 0),
    ('Tofu', 'veg', 76, 8, 1.9, 4.8, 0.3),
    ('Lentil', 'veg', 116, 9, 20, 0.4, 11),
    
    # Additional Common Foods
    ('Noodles', 'grain', 380, 13, 69, 1, 2),
    ('Pasta', 'grain', 371, 13, 75, 1.1, 3),
    ('Bread', 'grain', 265, 9, 49, 3.3, 2.7),
    ('White Rice', 'grain', 206, 2.7, 45, 0.3, 0.4),
    ('Brown Rice', 'grain', 215, 2.6, 45, 1, 3.5),
    ('Oats', 'grain', 389, 17, 66, 7, 10.6),
    ('Wheat', 'grain', 340, 13, 70, 2, 10),
    ('Cornflakes', 'grain', 417, 8, 84, 1.3, 4),
    ('Sugar', 'snack', 387, 0, 100, 0, 0),
    ('Salt', 'snack', 0, 0, 0, 0, 0),
    ('Honey', 'snack', 304, 0.3, 82, 0, 0.2),
    ('Jaggery', 'snack', 383, 0.1, 98, 0, 0),
]

# Check existing foods
existing_count = Food.objects.count()
print(f"Existing foods: {existing_count}")

# Add foods that don't already exist
added_count = 0
similar_foods = []

for name, category, cal, protein, carbs, fat, fiber in INDIAN_FOODS:
    # Check if food already exists (case-insensitive)
    if not Food.objects.filter(name__iexact=name).exists():
        try:
            Food.objects.create(
                name=name,
                category=category,
                calories_per_100g=cal,
                protein=protein,
                carbs=carbs,
                fat=fat,
                fiber=fiber,
                cuisine='indian'
            )
            added_count += 1
        except Exception as e:
            print(f"Error adding {name}: {e}")
    else:
        similar_foods.append(name)

print(f"\nSuccessfully added: {added_count} new foods")
print(f"Total foods in database: {Food.objects.count()}")
print(f"Skipped (already exist): {len(similar_foods)}")

# Show some of the newly added foods
print("\nSample of added foods:")
for food in Food.objects.filter(cuisine='indian').order_by('-created_at')[:10]:
    print(f"  - {food.name}: {food.calories_per_100g} kcal, Protein: {food.protein}g, Carbs: {food.carbs}g, Fat: {food.fat}g")
