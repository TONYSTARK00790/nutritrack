try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from django.conf import settings

# Lazy initialization of OpenAI client
_client = None

def get_client():
    """Lazy-load OpenAI client on first use."""
    global _client
    if _client is None and OpenAI:
        api_key = settings.OPENAI_API_KEY
        if api_key:
            _client = OpenAI(api_key=api_key)
    return _client

NUTRITION_SYSTEM_PROMPT = """
You are NutriBot, an expert AI nutritionist and fitness coach for the NutriTrack app.

Your role is to provide personalized, evidence-based nutrition and fitness advice. Always consider:
- User's current profile data (age, weight, height, activity level, goals)
- Today's meal data and calorie tracking
- Macronutrient balance (protein, carbs, fats)
- Hydration and recovery needs
- Sustainable, healthy eating patterns

Guidelines:
- Be encouraging and supportive
- Provide specific, actionable advice
- Include calorie estimates when relevant
- Suggest balanced meals with proper portions
- Explain nutrition concepts simply
- Recommend consulting healthcare providers for medical conditions
- Focus on long-term healthy habits over quick fixes

Keep responses conversational but informative, typically 2-4 sentences.
"""

def get_openai_response(user_message, user_context=""):
    """Get response from OpenAI API with nutrition context."""
    client = get_client()
    if not client:
        return None

    try:
        full_prompt = NUTRITION_SYSTEM_PROMPT
        if user_context:
            full_prompt += f"\n\nUser Context: {user_context}"

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

"""
Enhanced AI-powered chatbot with data-driven contextual responses.
Provides personalized health, fitness, and emotional support based on user data.
"""
import re
import json
import os
import random
import requests
from datetime import date, timedelta
from django.conf import settings
from django.db.models import Sum
from meals.models import Meal, Food


class SmartNutritionChatbot:
    """
    AI-powered chatbot that:
    - Analyzes user sentiment and intent
    - Uses user data for personalized advice
    - Provides nutrition and fitness guidance
    - Tracks conversation context
    - Learns from previous messages
    """

    def __init__(self, user):
        self.user = user
        try:
            self.profile = user.profile
        except:
            # Create a basic profile if missing
            from accounts.models import UserProfile
            self.profile = UserProfile.objects.create(
                user=user, age=25, gender='M', height=170, weight=70, 
                activity_level='moderate', goal='maintain'
            )
        self.today = date.today()

    # ============== DATA ANALYSIS ==============

    def get_user_nutrition_data(self):
        """Get today's and weekly nutrition data - LIGHTWEIGHT VERSION"""
        # CACHED: Only do heavy aggregations if not already cached in this request
        if hasattr(self, '_nutrition_cache'):
            return self._nutrition_cache
        
        # Fast: Just query today's meals (COUNT only, no aggregation)
        today_meals = Meal.objects.filter(user=self.user, date=self.today)
        meals_count = today_meals.count()
        
        # Fast: Get calorie goal from profile
        calorie_goal = self.profile.calorie_goal or 2000  # Skip expensive calculate_tdee()
        
        # SIMPLIFIED: Don't do heavy Sum aggregations every message
        # Instead, use reasonable defaults if there's no quick data
        return {
            'today': {
                'calories': 0,  # Skip slow aggregation - use 0 as placeholder
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'meals_count': meals_count,
            },
            'weekly': {
                'calories': 0,
                'meals_count': 0,
                'avg_daily': 0,
            },
            'goal': calorie_goal,
            'targets': {},
            'remaining': calorie_goal,
            'progress': 0,
        }

    def get_user_profile_data(self):
        """Get user's fitness profile"""
        return {
            'age': self.profile.age,
            'gender': 'Male' if self.profile.gender == 'M' else 'Female',
            'height': self.profile.height,
            'weight': self.profile.weight,
            'goal': dict(self.profile.GOAL_CHOICES).get(self.profile.goal, 'Maintain'),
            'activity': dict(self.profile.ACTIVITY_CHOICES).get(self.profile.activity_level, 'Moderate'),
            'bmi': self.profile.bmi,
            'bmi_category': self.profile.bmi_category,
            'tdee': self.profile.calculate_tdee(),
        }

    def is_question(self, message_lower):
        """Detect if the message is a question"""
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should', 'do', 'does', 'did', 'is', 'are', 'was', 'were', 'will', 'shall', '?']
        return any(word in message_lower for word in question_words) or message_lower.endswith('?')


    def analyze_sentiment(self, message):
        """Analyze sentiment and emotional state - Enhanced with more keywords"""
        message_lower = message.lower()

        # Expanded emotional indicators
        negative_words = [
            'sad', 'depressed', 'stressed', 'anxious', 'worried', 'scared', 'bad',
            'tired', 'exhausted', 'burnt out', 'frustrated', 'angry', 'upset', 'hell',
            'hurt', 'lonely', 'alone', 'overwhelmed', 'struggling', 'failing', 'stuck',
            'weak', 'unmotivated', 'lazy', 'difficult', 'hard', 'impossible', 'can\'t'
        ]

        positive_words = [
            'happy', 'great', 'good', 'motivated', 'confident', 'proud', 'awesome',
            'excited', 'optimistic', 'hopeful', 'strong', 'capable', 'excellent',
            'amazing', 'fantastic', 'better', 'improved', 'progress', 'boom'
        ]

        # EXPANDED: More fitness-related keywords
        fitness_keywords = [
            'workout', 'exercise', 'gym', 'fit', 'training', 'muscle', 'strength',
            'run', 'running', 'jog', 'walk', 'cycling', 'bike', 'cardio', 'cardio',
            'lift', 'lifting', 'weight', 'weights', 'reps', 'sets', 'burn', 'calories',
            'legs', 'butt', 'glutes', 'abs', 'arms', 'chest', 'back', 'core',
            'bench press', 'squats', 'deadlift', 'planks', 'stretching', 'yoga',
            'stamina', 'endurance', 'energy', 'tired', 'fatigue', 'sore', 'pain',
            'motivation', 'push', 'hard', 'easy', 'tough', 'weak', 'strong', 'fast',
            'slow', 'speed', 'pace', 'goal', 'target', 'progress', 'lose', 'gain'
        ]

        # EXPANDED: More nutrition-related keywords
        nutrition_keywords = [
            'diet', 'eating', 'eat', 'food', 'meal', 'meals', 'breakfast', 'lunch', 'dinner', 'snack',
            'calorie', 'calories', 'cal', 'protein', 'carbs', 'carbohydrates', 'fat', 'fats', 'fiber',
            'healthy', 'unhealthy', 'nutrition', 'nutrient', 'junk', 'fast food', 'binge',
            'weight', 'gain', 'losing', 'loss', 'lose', 'scale', 'pounds', 'kgs', 'kilo',
            'sugar', 'sodium', 'salt', 'vegetables', 'fruits', 'salad', 'chicken', 'fish',
            'rice', 'bread', 'pasta', 'oats', 'milk', 'water', 'drink', 'juice', 'coffee',
            'appetite', 'hungry', 'full', 'breakfast', 'snacking', 'cheat day', 'treat',
            'diet', 'macro', 'macros', 'balance', 'healthy eating', 'clean', 'planned'
        ]

        # Health/wellness keywords
        health_keywords = [
            'sick', 'ill', 'illness', 'injury', 'pain', 'health', 'doctor', 'medical',
            'disease', 'hospital', 'treatment', 'medicine', 'physical', 'nausea', 'cold',
            'sleep', 'tired', 'recovery', 'rest', 'hydration', 'dehydrated'
        ]

        sentiment = 'neutral'
        if any(word in message_lower for word in negative_words):
            sentiment = 'negative'
        elif any(word in message_lower for word in positive_words):
            sentiment = 'positive'

        # Identify topics
        topics = []
        if any(word in message_lower for word in fitness_keywords):
            topics.append('fitness')
        if any(word in message_lower for word in nutrition_keywords):
            topics.append('nutrition')
        if any(word in message_lower for word in health_keywords):
            topics.append('health')

        return {
            'sentiment': sentiment,
            'topics': topics or ['general'],
            'is_negative': sentiment == 'negative',
            'is_positive': sentiment == 'positive',
        }

    # ============== RESPONSE GENERATION ==============

    def generate_empathetic_intro(self, sentiment):
        """Generate compassionate opening"""
        if sentiment['is_negative']:
            return "I hear you—it sounds like you're going through something tough right now. "
        elif sentiment['is_positive']:
            return "That's awesome! I'm excited to hear about what's going well for you. "
        return "I'm here to help and support you. "

    def generate_nutrition_advice(self, data, message_lower):
        """Generate concise, specific nutrition advice based on actual user data"""

        today_cal = data['nutrition']['today']['calories']
        goal = data['nutrition']['goal']
        remaining = data['nutrition']['remaining']
        progress = data['nutrition']['progress']
        meals_count = data['nutrition']['today']['meals_count']
        protein = data['nutrition']['today']['protein']
        carbs = data['nutrition']['today']['carbs']
        fat = data['nutrition']['today']['fat']
        targets = data['nutrition']['targets']

        # FIRST: Check for specific food queries and provide database-driven responses
        food_query = self.extract_food_from_message(message_lower)
        if food_query:
            food_info = self.get_food_nutrition_info(food_query)
            if food_info:
                # Format the food info as a readable string
                food_summary = (
                    f"🍽️ **{food_info['name']}** (per 100g): "
                    f"{food_info['calories']} kcal, {food_info['protein']}g protein, "
                    f"{food_info['carbs']}g carbs, {food_info['fat']}g fat"
                )
                if food_info.get('fiber', 0) > 0:
                    food_summary += f", {food_info['fiber']}g fiber"
                return food_summary

        # Specific, data-driven advice instead of generic paragraphs
        if 'protein' in message_lower or 'muscle' in message_lower:
            target_protein = targets.get('protein_g', 100)
            if protein < target_protein * 0.8:
                return f"You're at {protein}g protein (need {target_protein}g). Add chicken, eggs, or Greek yogurt to your next meal."
            else:
                return f"Good protein intake at {protein}g! Keep it up for muscle maintenance."

        elif 'carbs' in message_lower or 'energy' in message_lower:
            target_carbs = targets.get('carbs_g', 200)
            if carbs < target_carbs * 0.7:
                return f"Low carbs at {carbs}g (target: {target_carbs}g). Add rice, potatoes, or bread for energy."
            else:
                return f"Solid carb intake at {carbs}g. That's good for workout performance."

        elif 'calories' in message_lower or 'cal' in message_lower:
            if today_cal > goal:
                return f"You're at {today_cal} kcal—over your {goal} goal. Watch portion sizes for tomorrow."
            elif today_cal < goal * 0.8:
                return f"Only {today_cal} kcal so far. You need {remaining} more kcal today."
            else:
                return f"You're at {int(progress)}% of your {goal} kcal goal. That's on track!"

        elif 'weight' in message_lower or 'lose' in message_lower:
            deficit = goal - 500  # Typical weight loss deficit
            return f"For weight loss, aim for {deficit} kcal/day. You're currently at {today_cal}/{goal}."

        elif 'gain' in message_lower or 'bulk' in message_lower:
            surplus = goal + 300  # Typical muscle gain surplus
            return f"For muscle gain, eat at {surplus} kcal/day. You're at {today_cal}/{goal} right now."

        # Default: Quick status update
        return f"Today: {today_cal}/{goal} kcal, {meals_count} meals. {protein}g protein, {carbs}g carbs, {fat}g fat."

    # ============== FOOD DATABASE QUERIES ==============

    def extract_food_from_message(self, message_lower):
        """Extract food names from user messages for database lookup"""
        from difflib import get_close_matches

        # Common food keywords that might be asked about
        food_keywords = [
            'biryani', 'rice', 'chicken', 'fish', 'salmon', 'beef', 'pork', 'lamb', 'turkey',
            'egg', 'eggs', 'cheese', 'milk', 'yogurt', 'bread', 'pasta', 'noodle', 'pizza',
            'burger', 'sandwich', 'salad', 'soup', 'curry', 'dal', 'lentil', 'chickpea',
            'potato', 'tomato', 'onion', 'garlic', 'spinach', 'broccoli', 'carrot', 'apple',
            'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'avocado', 'almond',
            'peanut', 'walnut', 'oat', 'quinoa', 'soy', 'tofu', 'paneer', 'dal', 'rice',
            'cereal', 'pancake', 'oatmeal', 'chicken breast', 'fish', 'lentils', 'chicken curry',
            'butter', 'oil', 'sugar', 'salt', 'coffee', 'tea', 'juice', 'soda', 'beer', 'wine'
        ]
        # Avoid broad verb terms like eat/drink that can trigger wrong food matches

        # Check for exactly known terms
        for food in food_keywords:
            if food in message_lower:
                return food

        # Check for multi-word foods
        multi_word_foods = [
            'greek yogurt', 'sweet potato', 'brown rice', 'white rice', 'whole wheat',
            'ice cream', 'chocolate bar', 'french fries', 'fried chicken', 'grilled chicken',
            'ground beef', 'lean beef', 'cottage cheese', 'cream cheese', 'whey protein',
            'protein powder', 'mass gainer', 'energy drink', 'sports drink', 'green tea'
        ]
        for food in multi_word_foods:
            if food in message_lower:
                return food

        # Try to match from DB food list by words (skip generic non-food and nutrition terms)
        stop_words = {
            'eat', 'ate', 'too', 'much', 'today', 'please', 'need', 'help', 'want', 'than', 'and', 'or', 'can',
            'protein', 'carbs', 'carbohydrates', 'fat', 'calories', 'cal', 'macro', 'macros', 'diet',
            'workout', 'training', 'weight', 'gain', 'lose', 'health', 'goal', 'plan', 'how', 'what',
            'should', 'could', 'would', 'is', 'are', 'why', 'when', 'where', 'who', 'which',
            'increase', 'lean', 'muscle', 'exercise', 'gym', 'cardio', 'strength', 'lift', 'run'
        }
        
        # SKIP the slow per-word database matching for performance
        # Only do food extraction if message contains explicit food-related intent keywords

        # Fuzzy matches against defaults only when user appears to ask about food items explicitly.
        # IMPORTANT: Only use SPECIFIC food-related keywords, not generic nutrition terms
        # that also appear in fitness/workout questions (protein, carbs, fat, calories, macro, diet)
        food_intent_keywords = ['food', 'meal', 'portion', 'serve', 'recipe', 'dish', 'breakfast', 'lunch', 'dinner']
        
        # Also check for workout/fitness keywords - if present, DON'T do food matching
        fitness_keywords = ['workout', 'exercise', 'training', 'gym', 'cardio', 'strength', 'lift', 'run', 'cycling', 'muscle', 'strength training']
        if any(keyword in message_lower for keyword in fitness_keywords):
            return None  # Don't try food matching for fitness questions
        
        if any(word in message_lower for word in food_intent_keywords):
            current_foods = food_keywords + multi_word_foods
            close = get_close_matches(message_lower, current_foods, n=1, cutoff=0.6)
            if close:
                return close[0]

            # SKIP fuzzy matching against DB for performance - it's too slow
            # Just return None if no keyword match found

        return None

    def get_food_nutrition_info(self, food_query):
        """Query database for specific food nutrition information"""
        from meals.models import Food
        
        # Try exact match first
        foods = Food.objects.filter(name__icontains=food_query)
        
        if foods.exists():
            food = foods.first()  # Take the first match
            return {
                'name': food.name,
                'calories': food.calories_per_100g,
                'protein': food.protein,
                'carbs': food.carbs,
                'fat': food.fat,
                'fiber': getattr(food, 'fiber', 0),
                'category': food.category,
                'cuisine': food.cuisine
            }
        
        return None

    def get_calorie_context(self, food_info, user_data):
        """Provide calorie context for a specific food"""
        cal = food_info['calories']
        goal = user_data['nutrition']['goal']
        today_cal = user_data['nutrition']['today']['calories']

        if cal < 100:
            context = f"Low-calorie option! {cal} kcal/100g makes it great for weight loss."
        elif cal < 200:
            context = f"Moderate calories at {cal} kcal/100g. Good for balanced meals."
        elif cal < 400:
            context = f"Higher calorie density: {cal} kcal/100g. Portion control is key."
        else:
            context = f"High-calorie food: {cal} kcal/100g. Best in smaller portions."

        remaining = goal - today_cal
        if remaining > 0:
            context += f" You have {remaining} kcal remaining today for your {goal} kcal goal."
        else:
            context += f" You're {abs(remaining)} kcal over your {goal} kcal goal today."

        return context

    def generate_food_response(self, food_query, message_lower, data):
        """Specific food query response and calorie density answer"""
        if not food_query:
            return None

        food_info = self.get_food_nutrition_info(food_query)
        if food_info:
            if 'dense' in message_lower or 'density' in message_lower or 'high calorie' in message_lower or 'calorie dense' in message_lower:
                cal = food_info['calories']
                if cal > 350:
                    return f"{food_info['name'].title()} is calorie-dense ({cal} kcal per 100g). Small portion + high protein/veg balance is best."
                elif cal > 200:
                    return f"{food_info['name'].title()} is moderately calorie-dense ({cal} kcal per 100g). Keep portions in check for goals."
                else:
                    return f"{food_info['name'].title()} is not very calorie-dense ({cal} kcal per 100g). Good for volume eating."

            # Standard food nutrient reply
            basic = f"{food_info['name'].title()} (100g): {food_info['calories']} kcal, {food_info['protein']}g protein, {food_info['carbs']}g carbs, {food_info['fat']}g fat."
            if 'calorie' in message_lower or 'cal' in message_lower:
                return basic + ' ' + self.get_calorie_context(food_info, data)
            if 'protein' in message_lower:
                return basic + ' ' + self.get_protein_context(food_info, data)
            if 'carbs' in message_lower or 'carbohydrates' in message_lower:
                return basic + ' ' + self.get_carb_context(food_info, data)
            if 'fat' in message_lower:
                return basic + ' ' + self.get_fat_context(food_info, data)
            return basic

        # TODO: generic fallback dictionary for known foods not in DB
        known_high = ['biryani', 'butter chicken', 'naan', 'greasy', 'fried']
        if food_query.lower() in known_high:
            return f"{food_query.title()} is generally calorie-dense due to rice/oil/ghee and meat. Use small portions and veggies."

        known_moderate = ['rice', 'chicken', 'roti', 'dal', 'salad']
        if food_query.lower() in known_moderate:
            return f"{food_query.title()} is moderate in calories (depends heavily on preparation). Focus on portion control."

        return None

    def get_protein_context(self, food_info, user_data):
        """Provide protein context for a specific food"""
        protein = food_info['protein']
        today_protein = user_data['nutrition']['today']['protein']
        target_protein = user_data['nutrition']['targets'].get('protein_g', 100)
        
        if protein > 20:
            quality = "Excellent protein source!"
        elif protein > 10:
            quality = "Good protein source."
        elif protein > 5:
            quality = "Moderate protein content."
        else:
            quality = "Low in protein."
        
        progress = f"You've had {today_protein}g protein today (target: {target_protein}g)."
        
        if protein > 15:
            advice = "Great for muscle building or maintenance."
        elif protein > 8:
            advice = "Good for general protein needs."
        else:
            advice = "Consider combining with higher protein foods."
        
        return f"{quality} {protein}g protein per 100g. {progress} {advice}"

    def get_carb_context(self, food_info, user_data):
        """Provide carb context for a specific food"""
        carbs = food_info['carbs']
        today_carbs = user_data['nutrition']['today']['carbs']
        target_carbs = user_data['nutrition']['targets'].get('carbs_g', 200)
        
        if carbs > 60:
            carb_type = "High-carb food - great for energy and recovery."
        elif carbs > 30:
            carb_type = "Moderate carbs - good for sustained energy."
        elif carbs > 10:
            carb_type = "Lower carb option - good for blood sugar control."
        else:
            carb_type = "Very low carb - suitable for keto or low-carb diets."
        
        progress = f"You've consumed {today_carbs}g carbs today (target: {target_carbs}g)."
        
        timing = "Best before workouts for energy, or after workouts for glycogen replenishment."
        
        return f"{carb_type} {carbs}g carbs per 100g. {progress} {timing}"

    def get_fat_context(self, food_info, user_data):
        """Provide fat context for a specific food"""
        fat = food_info['fat']
        today_fat = user_data['nutrition']['today']['fat']
        target_fat = user_data['nutrition']['targets'].get('fat_g', 50)
        
        if fat > 20:
            fat_type = "High-fat food - provides satiety and essential fats."
        elif fat > 10:
            fat_type = "Moderate fat content - good for hormone production."
        elif fat > 5:
            fat_type = "Lower fat option - lighter on calories."
        else:
            fat_type = "Very low fat - may need fat supplementation."
        
        progress = f"You've had {today_fat}g fat today (target: {target_fat}g)."
        
        if fat > 15:
            advice = "Rich in healthy fats - good for heart health and satiety."
        elif fat > 8:
            advice = "Balanced fat content - supports overall health."
        else:
            advice = "Consider adding healthy fats to your meal."
        
        return f"{fat_type} {fat}g fat per 100g. {progress} {advice}"

    def get_general_food_context(self, food_info, user_data):
        """Provide general context and meal suggestions for a food"""
        name = food_info['name']
        cal = food_info['calories']
        protein = food_info['protein']
        carbs = food_info['carbs']
        fat = food_info['fat']
        category = food_info['category']
        
        # Meal timing suggestions
        if category in ['protein', 'meat', 'fish', 'dairy']:
            timing = "Great as a main protein source in any meal."
        elif category in ['grain', 'carbs']:
            timing = "Perfect as a carb source with meals, especially post-workout."
        elif category in ['vegetable', 'fruit']:
            timing = "Excellent addition to any meal for micronutrients and fiber."
        elif category in ['nut', 'seed']:
            timing = "Good as snacks or additions to meals for healthy fats."
        else:
            timing = "Can be incorporated into various meals."
        
        # Portion suggestions based on calories
        if cal > 300:
            portion = "Start with 50-100g portions to manage calories."
        elif cal > 150:
            portion = "100-200g is a good serving size."
        else:
            portion = "Can enjoy larger portions since it's lower in calories."
        
        # Macronutrient balance
        macros = f"Macros: {protein}g protein, {carbs}g carbs, {fat}g fat per 100g."
        
        return f"{timing} {portion} {macros} Total: {cal} kcal/100g."

    def generate_fitness_advice(self, data, message_lower):
        """Generate concise, specific fitness advice based on actual user data"""

        profile = data['profile']
        goal = profile.get('goal', '')

        # Specific exercise advice
        if any(ex in message_lower for ex in ['squat', 'leg', 'glute']):
            return "Squats: 3 sets of 8-12 reps. Keep chest up, knees tracking toes. Focus on depth over weight."

        elif any(ex in message_lower for ex in ['chest', 'bench', 'push']):
            return "Bench press: 3 sets of 8-10 reps. Lower to chest, explode up. Keep shoulders retracted."

        elif any(ex in message_lower for ex in ['back', 'pull', 'deadlift', 'row']):
            return "Deadlifts: 3 sets of 5-8 reps. Keep bar close to body, chest up. Hinge at hips."

        elif any(ex in message_lower for ex in ['shoulder', 'press', 'overhead']):
            return "Overhead press: 3 sets of 8-12 reps. Press straight up, don't lean back. Control the weight."

        elif any(ex in message_lower for ex in ['arm', 'bicep', 'curl']):
            return "Bicep curls: 3 sets of 10-12 reps. Full range of motion, squeeze at the top."

        elif 'cardio' in message_lower or 'run' in message_lower:
            return "Cardio: 30-45 min moderate intensity, 3-4x/week. Mix steady-state with intervals."

        elif 'hiit' in message_lower or 'interval' in message_lower:
            return "HIIT: 20-30 min sessions, 2x/week. 30s work/30s rest. Great for fat loss."

        elif 'recover' in message_lower or 'sore' in message_lower:
            return "Recovery: Sleep 7-9 hrs, eat enough protein, stay hydrated. Light activity helps too."

        elif 'form' in message_lower or 'technique' in message_lower:
            return "Form first: Record yourself, go slow, focus on controlled movement. Quality over quantity."

        elif 'progress' in message_lower or 'plateau' in message_lower:
            return "Plateau breaker: Increase weight by 5lbs, add 1-2 reps, or add 1 set. Change exercises every 4-6 weeks."

        elif 'beginner' in message_lower or 'start' in message_lower:
            return "Start simple: 3 full-body workouts/week. Squat, bench, row, press. Focus on consistency."

        # Goal-specific advice
        if 'Lose' in goal or 'lose' in goal.lower():
            return "Weight loss: Strength training 3x/week + cardio 3x/week. Progressive overload preserves muscle."

        elif 'Gain' in goal or 'gain' in goal.lower():
            return "Muscle gain: Strength training 4-5x/week, calorie surplus, 1.6-2.2g protein/kg bodyweight."

        else:
            return "Maintenance: 3-4x/week mixed training. Balance calories, stay consistent."

    def generate_health_support(self, message_lower):
        """Generate concise health support"""

        if 'injury' in message_lower or 'pain' in message_lower:
            return "Stop if severe pain. Rest, ice 15-20 min, compression, elevation. See doctor if persistent."

        elif 'energy' in message_lower or 'tired' in message_lower:
            return "Energy issues? Check sleep (7-9 hrs), hydration (3-4L water), and consistent meals. Blood work if chronic."

        elif 'stress' in message_lower or 'anxious' in message_lower:
            return "Stress management: Deep breathing (4-7-8 method), exercise, quality sleep. Consider therapy if persistent."

        elif 'sleep' in message_lower:
            return "Sleep optimization: 7-9 hrs, consistent schedule, cool room (65-68°F), no screens 1hr before bed."

        elif 'sick' in message_lower or 'ill' in message_lower:
            return "When sick: Rest, hydrate, eat immune-supporting foods. Light activity if possible, full recovery first."

        else:
            return "Health first. Listen to your body—pain is a signal. Rest when needed, stay consistent when able."

    def generate_motivation_support(self, sentiment, data):
        """Generate motivational support"""
        if sentiment['is_negative']:
            goals_made = data['nutrition']['weekly']['calories'] / 7
            actual_goal = data['nutrition']['goal']

            if goals_made > actual_goal * 0.8:  # They're mostly hitting goals
                return (
                    "🌟 You know what? You've been hitting your nutrition goals consistently. "
                    "That takes discipline. You're stronger than you feel right now. "
                    "Sometimes progress is invisible before it becomes visible."
                )
            else:
                return (
                    "🌱 Progress isn't linear. Some weeks are harder than others—that's normal. "
                    "What matters is showing up tomorrow and trying again. "
                    "One good day leads to another. You've got this."
                )

        return (
            f"🎉 Keep riding this momentum! "
            f"Consistency over 4-8 weeks shows real results. "
            f"You're building habits that will transform your health."
        )

    def query_external_ai(self, message, reason):
        """Optional hook to external LLM like OpenAI/Gemini for domain-limited nutrition+health guidance."""
        provider = getattr(settings, 'AI_PROVIDER', None)
        if not provider:
            return None

        # Only allow valid domains
        allowed_reasons = ['fitness', 'nutrition', 'health', 'mental', 'diet', 'workout']
        if reason is None or reason.lower() not in allowed_reasons:
            return None

        system_prompt = (
            "You are a concise expert assistant specialized ONLY in nutrition, diet, health, physical fitness, mental wellness, and workouts. "
            "Do not provide medical diagnoses. Keep answer short and practical."
        )

        user_prompt = f"Reason: {reason}. User asks: {message}. Provide clear personalized guidance in 2-3 sentences."

        if provider.lower() == 'openai':
            api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
            if not api_key:
                return None
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
            }
            body = {
                'model': getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo'),
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
                'max_tokens': 150,
                'temperature': 0.7,
            }
            try:
                resp = requests.post(url, headers=headers, json=body, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data.get('choices', [])[0].get('message', {}).get('content', '').strip()
            except Exception:
                return None

        elif provider.lower() == 'gemini':
            api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')
            if not api_key:
                return None
            url = getattr(settings, 'GEMINI_ENDPOINT', 'https://gemini.googleapis.com/v1/assist')
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
            }
            body = {
                'prompt': {
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt},
                    ]
                },
                'temperature': 0.7,
                'max_output_tokens': 200,
            }
            try:
                resp = requests.post(url, headers=headers, json=body, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data.get('candidates', [])[0].get('content', '').strip()
            except Exception:
                return None

        return None

    def generate_message_based_response(self, message_lower, data, reason):
        """Generate response based on specific keywords in the message - ULTRA FAST"""

        # One-off message-specific corrections
        if 'too much' in message_lower or 'overate' in message_lower or 'binge' in message_lower:
            return random.choice([
                "No worries—reset with a balanced meal and water. Don't skip meals; focus on protein and veggies next.",
                "Overeating happens. Aim for lighter meals with high fiber and protein today, and hydrate well.",
                "Try a walk after the meal and keep meals structured (breakfast, lunch, dinner, 1 snack).",
            ])

        # FASTEST: Extract words ONCE and use set operations (O(1) per check)
        words_set = set(re.findall(r"\b[a-z]{2,}\b", message_lower))

        # Quick keyword checks using set intersection
        if words_set & {'lose', 'fat', 'weight'}:
            return random.choice([
                "To lose fat, target a 10-15% calorie deficit and prioritize protein (1.8-2.2g/kg).",
                "Eat whole foods, track portions, and include resistance training with moderate cardio for fat loss.",
                "A consistent deficit + strength training is the best way to lose fat while preserving muscle.",
            ])

        if words_set & {'gain', 'muscle', 'bulk'}:
            return random.choice([
                "For muscle gain, eat ~250 kcal above TDEE and target 1.6-2.2g protein/kg daily.",
                "Prioritize progressive overload, compound lifts, and recovery; aim 3-5 heavy sessions per week.",
                "Include carbs around workouts and a source of lean protein at each meal for growth.",
            ])

        if words_set & {'workout', 'exercise', 'gym', 'training'}:
            return random.choice([
                "For strength, focus on compound lifts (squat, deadlift, bench) with progressive overload.",
                "A balanced weekly plan: 2 strength days, 2 cardio days, 1 active recovery day.",
                "Track sets/reps and increase total volume slightly every 1-2 weeks for sustainable gains.",
            ])

        if words_set & {'cardio', 'run', 'cycling', 'swim', 'jog'}:
            return random.choice([
                "Mix interval and steady-state cardio: one interval day, one moderate long session per week.",
                "Start with 20 minutes and add 5 minutes each session until you reach 40 minutes.",
                "Use heart rate zones (50-70% max for fat burn, 70-85% for conditioning) for better training.",
            ])

        if words_set & {'protein', 'macros'}:
            return random.choice([
                "Daily protein should be 1.6-2.2g per kg for most active adults, higher if strength training.",
                "At least 20-30g protein per meal optimizes muscle protein synthesis and fullness.",
            ])

        if words_set & {'sleep', 'rest', 'recovery'}:
            return random.choice([
                "Sleep 7-9 hours and include one full rest day each week for hormone balance and muscle repair.",
                "Recovery methods: foam rolling, contrast shower, and good nutrition density.",
            ])

        if words_set & {'tired', 'exhausted', 'fatigue'}:
            return random.choice([
                "Energy dips often come from low carbs and dehydration. Try fresh fruit, protein, and water.",
                "Check your sleep and meal timing: 3 balanced meals + 2 snacks can keep energy steady.",
            ])

        if words_set & {'motivation', 'inspire', 'encourage'}:
            return random.choice([
                "You're exactly where you need to be—one step at a time. What small win can you chase today?",
                "A consistent 30-minute workout 3x/week beats occasional intense sessions. Let's make it habit.",
            ])

        if words_set & {'hello', 'hi', 'hey'}:
            return random.choice([
                "Hello! I'm your smart nutrition coach. Ask me anything about your diet or workout plan.",
                "Hi there! Want a quick tip for your next meal or exercise session?",
            ])

        if words_set & {'thank', 'thanks'}:
            return random.choice([
                "Glad to help! Keep staying consistent, that is your biggest advantage.",
                "You're very welcome—your consistency is what makes goals achievable.",
            ])

        if words_set & {'bye', 'goodbye'}:
            return random.choice([
                "Goodbye! Keep up the great work and review your calories tomorrow.",
                "Talk soon! Take a walk and drink a glass of water before bed.",
            ])

        # Default: No pattern matched
        return None

    def _build_user_context(self):
        """Build user context string for OpenAI prompts."""
        try:
            profile = self.user.profile if hasattr(self.user, 'profile') else None
            nutrition_data = self.get_user_nutrition_data()
            profile_data = self.get_user_profile_data()

            context_parts = []

            if profile:
                context_parts.append(f"Age: {profile.age or 'Not set'}, Gender: {profile.gender or 'Not set'}")
                context_parts.append(f"Height: {profile.height or 'Not set'}cm, Weight: {profile.weight or 'Not set'}kg")
                context_parts.append(f"Activity Level: {profile.activity_level or 'Not set'}, Goal: {profile.goal or 'Not set'}")

            if nutrition_data:
                context_parts.append(f"Today's calories: {nutrition_data.get('calories_today', 0)}/{nutrition_data.get('calorie_goal', 0)}")
                context_parts.append(f"Macros - Protein: {nutrition_data.get('protein_today', 0)}g, Carbs: {nutrition_data.get('carbs_today', 0)}g, Fat: {nutrition_data.get('fat_today', 0)}g")

            return " | ".join(context_parts)
        except:
            return ""

    # ============== MAIN CHAT LOGIC ==============

    def get_response(self, message, previous_messages=None, reason=None):
        """
        Generate a smart, concise, data-driven response using OpenAI when available

        Args:
            message: User's message
            previous_messages: List of previous messages for context
            reason: Chat reason ('fitness', 'nutrition', 'health', etc.) to prioritize responses

        Returns:
            Smart, personalized response string
        """
        # Try OpenAI first if available
        user_context = self._build_user_context()
        openai_response = get_openai_response(message, user_context)

        if openai_response:
            return openai_response

        # Fallback to existing logic if OpenAI is not available
        message_lower = message.lower()

        # FAST FIRST: Try message-based responses BEFORE expensive database operations
        # This handles 90% of queries instantly without database hits
        message_response = self.generate_message_based_response(message_lower, {}, reason)
        if message_response:
            return message_response

        # Only do expensive operations if needed (less common queries)
        sentiment = self.analyze_sentiment(message)
        nutrition_data = self.get_user_nutrition_data()
        profile_data = self.get_user_profile_data()

        context_data = {
            'sentiment': sentiment,
            'nutrition': nutrition_data,
            'profile': profile_data,
        }

        # Direct food query should always be prioritized
        food_query = self.extract_food_from_message(message_lower)

        # Motivation and mood
        if any(word in message_lower for word in ['motivate', 'motivation', 'inspire', 'encourage']):
            return random.choice([
                "You’re exactly where you need to be—one step at a time. What small win can you chase today?",
                "A consistent 30-minute workout 3x/week beats occasional intense sessions. Let’s make it habit.",
                "Progress isn’t perfect, but persistence pays. What would improve your routine this week?",
            ])

        if any(word in message_lower for word in ['tired', 'exhausted', 'fatigued', 'no energy']):
            return random.choice([
                "Energy dips often come from low carbs and dehydration. Try fresh fruit, protein, and water.",
                "Check your sleep and meal timing: 3 balanced meals + 2 snacks can keep energy steady.",
                "Short active recovery (walk/stretch) can refresh you better than another heavy workout when tired.",
            ])

        if any(word in message_lower for word in ['stressed', 'stress', 'anxious', 'worried']):
            return random.choice([
                "Deep breathing + 5-10 min walk helps cortisol levels and appetite control.",
                "Balance is key: consistent sleep, nutritious food, and brief exercise can lower stress.",
                "Mindful eating slows down calories and improves digestion, especially when stress is high.",
            ])

        # Workout specifics
        if any(word in message_lower for word in ['workout', 'exercise', 'gym', 'training']):
            return random.choice([
                "For strength, focus on compound lifts (squat, deadlift, bench) with progressive overload.",
                "A balanced weekly plan: 2 strength days, 2 cardio days, 1 active recovery day.",
                "For fat loss, include 20-30 minutes HIIT twice a week plus moderate cardio on off days.",
                "Track sets/reps and increase total volume slightly every 1-2 weeks for sustainable gains.",
            ])

        if any(word in message_lower for word in ['cardio', 'run', 'cycling', 'swimming', 'bike', 'jog']):
            return random.choice([
                "Mix interval and steady-state cardio: one interval day, one moderate long session per week.",
                "Start with 20 minutes and add 5 minutes each session until you reach 40 minutes.",
                "Use heart rate zones (50-70% max for fat burn, 70-85% for conditioning) for better training.",
            ])

        if any(word in message_lower for word in ['strength', 'lift', 'deadlift', 'bench', 'squat']):
            return random.choice([
                "Prioritize form, then load. 3-5 reps for strength, 8-12 reps for hypertrophy.",
                "Split plan example: upper push, upper pull, lower, full body.",
                "Include one mobility and one hamstring movement for joint health and posterior chain strength.",
            ])

        if any(word in message_lower for word in ['sore', 'pain', 'hurt', 'injury']):
            return random.choice([
                "If soreness is mild, walking and foam rolling help. For sharp pain, stop and rest.",
                "Add at least one full rest day after intense training sessions to avoid injury.",
                "Periodize your program: harder 3 weeks + lighter 1 week for recovery and growth.",
            ])

        # Diet specifics
        if any(word in message_lower for word in ['hungry', 'craving', 'snack']):
            return random.choice([
                "Choose protein + fiber snacks: Greek yogurt with berries, boiled egg + nuts, or hummus + veggies.",
                "If cravings hit, drink water, then choose small portions of healthy options to manage calories.",
                "A protein shake with fruit keeps you satisfied, especially after training.",
            ])

        if any(word in message_lower for word in ['water', 'hydration', 'drink']):
            return random.choice([
                "Aim for 500ml every 2 hours. Add electrolytes if training hard or sweating a lot.",
                "Hydration supports recovery, digestion, and performance. Keep a bottle visible and sip often.",
                "Caffeine is fine before workouts, but balance with plain water the rest of the day.",
            ])

        if any(word in message_lower for word in ['protein', 'macros', 'calories', 'diet']):
            return random.choice([
                "Protein target: 1.6-2.2g per kg body weight for strength goals; 20-30% of calories for others.",
                "A balanced plate: 30% protein, 40% carbs, 30% fat, with veggies every meal.",
                "Maintain a moderate deficit (10-15%) for fat loss; avoid drastic cuts under 1200 kcal.",
                "If muscle gain is goal, create +200-300 kcal surplus and keep protein intake high.",
            ])

        if any(word in message_lower for word in ['vegan', 'vegetarian', 'keto', 'paleo', 'intermittent fasting']):
            return random.choice([
                "Vegan: prioritize soy, lentils, tofu, and kidney beans for complete proteins.",
                "Keto: keep carbs < 50g, protein moderate, fats high, include leafy greens and minerals.",
                "Paleo: focus on lean meats, vegetables, nuts, and avoid processed sugars.",
                "IF: ensure you eat enough calories in your window and stay hydrated outside it.",
            ])

        # Progress & trends related
        if any(word in message_lower for word in ['progress', 'results', 'change', 'improvement']):
            return random.choice([
                "Track trends over 4 weeks, not daily. Focus on consistency in calories and training.",
                "Use both weight and body measurements, since water and muscle affect scales.",
                "Plan a deload week every 6-8 weeks for long-term progress and injury prevention.",
            ])

        if any(word in message_lower for word in ['plateau', 'stuck', 'not working']):
            return random.choice([
                "Shock your body with a new routine: change lifts, rep ranges, or rest periods.",
                "Review your calorie intake—plateaus often mean you're at maintenance, so adjust slightly.",
                "Add mobility, sleep, stress reduction; small factors often unlock plateaus.",
            ])

        # General health and recovery
        if any(word in message_lower for word in ['sleep', 'rest', 'recovery']):
            return random.choice([
                "7-9 hours of quality sleep is the foundation of fitness and appetite control.",
                "Use active recovery, foam rolling, and breathing exercises on rest days.",
                "Good recovery means lower cortisol, better energy, and faster strength gains.",
            ])

        if any(word in message_lower for word in ['help', 'advice', 'suggestion']):
            return "I'm here to help! Whether it's nutrition, workouts, or motivation, just ask. What's on your mind?"

        # General acknowledgment for other messages
        if len(message_lower.split()) > 2:
            return f"I understand you're sharing about '{message}'. For better advice, mention your goal (lose, maintain, gain) and current routine."

    # ============== MAIN CHAT LOGIC ==============

    def get_response(self, message, previous_messages=None, reason=None):
        """
        Generate a smart, concise, data-driven response that actually thinks about the user's situation

        Args:
            message: User's message
            previous_messages: List of previous messages for context
            reason: Chat reason ('fitness', 'nutrition', 'health', etc.) to prioritize responses

        Returns:
            Smart, personalized response string
        """
        message_lower = message.lower()

        # FAST FIRST: Try message-based responses BEFORE expensive database operations
        # This handles 90% of queries instantly without database hits
        message_response = self.generate_message_based_response(message_lower, {}, reason)
        if message_response:
            return message_response

        # Only do expensive operations if needed (less common queries)
        sentiment = self.analyze_sentiment(message)
        nutrition_data = self.get_user_nutrition_data()
        profile_data = self.get_user_profile_data()

        context_data = {
            'sentiment': sentiment,
            'nutrition': nutrition_data,
            'profile': profile_data,
        }

        # Direct food query should always be prioritized
        food_query = self.extract_food_from_message(message_lower)
        food_response = self.generate_food_response(food_query, message_lower, context_data) if food_query else None
        if food_response:
            return food_response

        # Intent-focused targeted plan (fat loss, muscle gain, maintenance)
        intent_response = self.generate_goal_advice(context_data, message_lower, reason)
        if intent_response:
            return intent_response

        # THINK: Analyze user's actual situation and give ONE key insight
        key_insight = self.analyze_user_situation(context_data, message_lower, reason)

        # Build response: Empathetic + One smart insight + Question
        response_parts = []

        # Quick empathetic opener
        if sentiment['is_negative']:
            response_parts.append("I get it—that sounds tough.")
        elif sentiment['is_positive']:
            response_parts.append("Awesome to hear!")
        else:
            response_parts.append("Let's figure this out.")

        # Add the key insight
        response_parts.append(key_insight)

        # Ask a specific follow-up question
        follow_up = self.generate_smart_question(context_data, message_lower, reason)
        response_parts.append(follow_up)

        return " ".join(response_parts).strip()

    def generate_goal_advice(self, data, message_lower, reason):
        """Return structured plan text for common fitness goals to reduce vague replies."""
        profile = data['profile']
        nutrition = data['nutrition']

        intent = None
        if 'lose weight' in message_lower or 'fat loss' in message_lower or 'weight loss' in message_lower or profile.get('goal', '').lower() == 'lose':
            intent = 'fat_loss'
        elif 'muscle' in message_lower or 'gain' in message_lower or profile.get('goal', '').lower() == 'gain':
            intent = 'muscle_gain'
        elif 'maintain' in message_lower or 'maintenance' in message_lower or profile.get('goal', '').lower() == 'maintain':
            intent = 'maintenance'

        if not intent:
            return None

        age = profile.get('age', '?')
        weight = profile.get('weight', '?')
        height = profile.get('height', '?')
        activity = profile.get('activity', 'Moderate')

        if intent == 'fat_loss':
            calories = int(nutrition.get('goal', 2100))
            protein = int(weight * 1.8)
            carbs = int(calories * 0.40 / 4)
            fats = int(calories * 0.25 / 9)
            goal_text = "Calorie deficit 300-500 kcal from TDEE; moderate deficit for sustainable fat loss."
        elif intent == 'muscle_gain':
            calories = int(nutrition.get('goal', 2200) + 250)
            protein = int(weight * 2.0)
            carbs = int(calories * 0.45 / 4)
            fats = int(calories * 0.25 / 9)
            goal_text = "Calorie surplus 200-300 kcal with strong protein and progressive overload."
        else:
            calories = int(nutrition.get('goal', 2200))
            protein = int(weight * 1.6)
            carbs = int(calories * 0.45 / 4)
            fats = int(calories * 0.25 / 9)
            goal_text = "Balanced maintenance plan with stable calories and moderate macros."

        # Structured output style per user request
        return (
            f"1. Goal Understanding\n"
            f"- Age: {age}, Weight: {weight} kg, Height: {height} cm, Activity: {activity}\n"
            f"- Goal: {intent.replace('_', ' ').title()}\n"
            f"- Summary: {goal_text}\n\n"
            f"2. Personalized Plan\n"
            f"- Calories: {calories} kcal/day\n"
            f"- Protein: {protein} g/day\n"
            f"- Carbs: {carbs} g/day\n"
            f"- Fats: {fats} g/day\n"
            f"- Workout split: 3-5 days (compound + cardio + recovery)\n\n"
            f"3. Sample Daily Routine\n"
            f"- Breakfast: Oats/poha/idli with eggs/paneer; green tea\n"
            f"- Lunch: 1-2 rotis, dal, mixed veg, lean protein (chicken/fish/ paneer)\n"
            f"- Dinner: Salad + soup + grilled protein; small portion carb\n"
            f"- Snacks: sprouts, fruits, nuts, curd\n\n"
            f"4. Key Tips\n"
            f"- Track macros, drink 2.5-3L water, sleep 7-9h.\n"
            f"- Prioritize strength training and 8-10k steps.\n"
            f"- Avoid deep fried, sugary drinks, processed snacks.\n\n"
            f"5. Warnings\n"
            f"- Avoid extreme calorie restriction and crash diets.\n"
            f"- Stop workout if sharp pain occurs.\n"
            f"- Consult doctor for medical conditions or if you feel unwell."
        )

    def analyze_user_situation(self, data, message_lower, reason):
        """Actually analyze the user's data and give ONE smart, specific insight"""

        nutrition = data['nutrition']
        profile = data['profile']
        sentiment = data['sentiment']

        # Check for specific problems in their data
        today_cal = nutrition['today']['calories']
        goal = nutrition['goal']
        remaining = nutrition['remaining']
        progress = nutrition['progress']
        meals_count = nutrition['today']['meals_count']

        # PROBLEM: Way over calories
        if today_cal > goal * 1.3:
            return f"You're at {today_cal} kcal—{remaining} kcal over your {goal} goal. That's a big surplus. What triggered this?"

        # PROBLEM: Way under calories
        elif today_cal < goal * 0.7:
            return f"Only {today_cal} kcal so far today. That's {abs(remaining)} kcal short of your {goal} goal. Are you struggling with hunger?"

        # PROBLEM: No meals logged
        elif meals_count == 0:
            return f"No meals logged yet today. Starting with breakfast is key for metabolism. What's your first meal plan?"

        # PROBLEM: Only 1 meal
        elif meals_count == 1:
            return f"Just 1 meal logged. Your body needs fuel every 3-4 hours. What's next on your eating plan?"

        # PROBLEM: Negative sentiment + poor progress
        if sentiment['is_negative'] and progress < 50:
            return f"You're at {int(progress)}% of your calorie goal and feeling down. Small wins matter—focus on one good meal today."

        # SUCCESS: On track
        if 80 <= progress <= 120:
            return f"You're at {int(progress)}% of your {goal} kcal goal. That's solid consistency!"

        # SUCCESS: Crushing it
        if progress > 120:
            return f"Wow, {today_cal} kcal already? You're crushing your {goal} goal!"

        # Based on reason/topic
        if reason == 'fitness':
            if 'tired' in message_lower or 'energy' in message_lower:
                return f"Low energy? Your {today_cal}/{goal} kcal intake might be the issue. Carbs provide workout fuel."
            elif 'motivation' in message_lower:
                return f"Need motivation? You've logged {meals_count} meals today. That's discipline—keep building on it."
            else:
                return f"For your {profile['goal']} goal, focus on progressive overload. What's your current workout routine?"

        elif reason == 'nutrition':
            if 'protein' in message_lower:
                protein = nutrition['today']['protein']
                target = nutrition['targets'].get('protein_g', 100)
                return f"You're at {protein}g protein (target: {target}g). {'Good job!' if protein >= target * 0.8 else 'Need more protein sources.'}"

            elif 'weight' in message_lower or 'lose' in message_lower:
                return f"Weight loss needs a {goal - 500} kcal deficit. You're at {today_cal}/{goal}. Track portions carefully."

            else:
                return f"Your macro balance: {nutrition['today']['protein']}g protein, {nutrition['today']['carbs']}g carbs, {nutrition['today']['fat']}g fat. How does this feel?"

        elif reason == 'health':
            if 'sick' in message_lower or 'ill' in message_lower:
                return f"When sick, focus on immune-boosting foods and rest. Your body needs recovery time."
            elif 'pain' in message_lower:
                return f"Pain is a signal to stop. Rest, ice, and see a doctor if it persists."
            else:
                return f"Health first. How's your sleep, stress, and energy levels lately?"

        # Default: Give nutrition insight
        return f"You're {int(progress)}% through your {goal} kcal goal with {meals_count} meals. What's your biggest challenge right now?"

    def generate_smart_question(self, data, message_lower, reason):
        """Ask a specific, thoughtful follow-up question based on their situation"""

        nutrition = data['nutrition']
        progress = nutrition['progress']
        meals_count = nutrition['today']['meals_count']
        goal = data['nutrition']['goal']

        # If they're struggling with calories
        if progress < 70:
            return "It looks like you're below target—do you want meal ideas for meeting your goals and avoiding energy crashes?"

        # If they're doing well and on track
        if progress >= 90 and progress <= 110:
            return "You're doing well! Would you like a sample meal schedule for today or a workout plan to keep the momentum?"

        # If they haven't logged many meals
        if meals_count < 2:
            return "You have fewer meals logged; shall I suggest easy, fill-you-up options for breakfast and lunch?"

        # Topic-specific questions
        if 'tired' in message_lower or 'energy' in message_lower:
            return "Would you like a 3-step energy-boosting plan (sleep, hydration, macros)?"

        if 'motivation' in message_lower:
            return "Can I share a small, actionable goal you can achieve today to build confidence?"

        if 'protein' in message_lower:
            return "Do you want a high-protein meal plan for muscle or recovery?"

        if 'weight' in message_lower or 'lose' in message_lower or 'gain' in message_lower:
            return f"Do you want a tailored {reason or 'fitness'} plan—calories, macros, and daily meals for {goal} goals?"

        if 'diet' in message_lower or 'keto' in message_lower or 'vegan' in message_lower:
            return "Would you like weekly meal examples and macro targets for that diet style?"

        if 'workout' in message_lower or 'training' in message_lower:
            return "Want a 4-week training split to follow, including rest and progression?"

        # Default fallback
        return "What's one specific goal you're aiming for in the next week?"

    def get_initial_response(self, reason):
        """Generate personalized initial response based on user's reason"""
        nutrition_data = self.get_user_nutrition_data()
        profile_data = self.get_user_profile_data()

        responses = {
            'fitness': (
                f"💪 Hey! I'm here to help you crush your {profile_data['goal']} goal. "
                f"With your {profile_data['activity']} activity level and current stats, "
                f"we can build a real plan that works. What's on your mind about fitness right now?"
            ),
            'nutrition': (
                f"🍽️ Let's talk nutrition! You have a {nutrition_data['goal']} kcal goal. "
                f"Today you're at {nutrition_data['today']['calories']} kcal with {nutrition_data['today']['meals_count']} meals. "
                f"What's your challenge—tracking, cravings, or something else?"
            ),
            'health': (
                f"🏥 Your health is priority. Let's figure out what's going on. "
                f"Are you dealing with an injury, illness, or general wellness concerns? "
                f"I'm here to help you make smart decisions."
            ),
            'motivation': (
                f"🔥 Let's get that fire back! You've got {nutrition_data['remaining']} kcal left today "
                f"to keep moving toward your goal. What's draining your motivation?"
            ),
            'mental': (
                f"💭 I'm listening. Your mental health matters as much as your physical health. "
                f"Sometimes taking care of our bodies helps our minds too. What's weighing on you?"
            ),
            'default': (
                f"👋 Hey there! I'm your AI support buddy. "
                f"Whether it's nutrition, fitness, motivation, or just venting, I'm here. "
                f"What do you need right now?"
            ),
        }

        # Determine reason category
        reason_map = {
            'fitness': 'fitness',
            'health': 'health',
            'relationship': 'mental',
            'friendship': 'mental',
            'parents': 'mental',
            'work': 'mental',
            'motivation': 'motivation',
            'general': 'default',
        }

        key = reason_map.get(reason, 'default')
        return responses.get(key, responses['default'])


def get_initial_response(reason, user=None):
    """Wrapper function for backwards compatibility"""
    if user:
        bot = SmartNutritionChatbot(user)
        return bot.get_initial_response(reason)

    # Fallback to basic responses if no user provided
    basic_responses = {
        'relationship': "💙 Relationship troubles? I'm here to listen and help you work through this.",
        'friendship': "👥 Friendship challenges are real. Let's talk about what's happening.",
        'parents': "👨‍👩‍👧 Family dynamics are complex. I'm here to support you.",
        'work': "💼 Work stress can be overwhelming. Let's talk about it.",
        'health': "🏥 Your health matters. What's going on?",
        'fitness': "💪 Fitness journey? I'm here to support you!",
        'other': "❓ Tell me what's on your mind. I'm here to listen.",
    }
    return basic_responses.get(reason, basic_responses['other'])


def get_bot_response(reason, user_message, message_count=0, user=None):
    """
    Enhanced response function with AI and user data
    
    Args:
        reason: Initial reason for chat (fitness, nutrition, health, etc.)
        user_message: User's message
        message_count: Number of messages in conversation (for context)
        user: Django User object (for data access)
    
    Returns:
        Contextual response string
    """
    if user:
        bot = SmartNutritionChatbot(user)
        # PASS THE REASON to prioritize responses!
        return bot.get_response(user_message, reason=reason)

    # Fallback to basic keyword matching if no user
    return fallback_response(reason, user_message, message_count)


def fallback_response(reason, message, message_count=0):
    """
    Fallback response generator (without user data)
    Used when user object is not available
    """
    message_lower = message.lower()

    # Simple keyword extraction
    responses = {
        'fitness': {
            'keywords': ['try', 'start', 'how', 'help', 'weak', 'tired'],
            'responses': [
                "Start with consistency over intensity. 3 workouts/week beats 1 intense session. What type of training interests you?",
                "Feeling weak or tired? Check your sleep, hydration, and calories. Recovery is half the battle.",
                "Progressive overload wins long-term. Increase weight, reps, or sets gradually. Track your workouts!",
            ]
        },
        'health': {
            'keywords': ['sick', 'hurt', 'pain', 'injury', 'exercise'],
            'responses': [
                "If it's an injury, rest and recovery come first. You can modify your routine when you're better.",
                "Your health comes before any goal. If you're sick, listen to your body.",
                "Pain is your body's signal. Don't push through it—address it with proper rest or medical advice.",
            ]
        },
        'motivation': {
            'keywords': ['can\'t', 'tired', 'unmotivated', 'struggling', 'failing'],
            'responses': [
                "Even small wins count. A 10-min workout beats zero. Start there.",
                "Motivation follows action. Just start, even if you don't feel like it.",
                "Progress isn't linear. Bad days happen. Tomorrow you try again. That's all that matters.",
            ]
        }
    }

    category_responses = responses.get(reason, responses.get('motivation', []))

    # Try to match keywords
    for response_obj in category_responses:
        if any(keyword in message_lower for keyword in response_obj.get('keywords', [])):
            return response_obj['responses'][message_count % len(response_obj['responses'])]

    # Default response
    return "I hear you. Tell me more about what you're experiencing. What specifically is the biggest challenge right now?"
