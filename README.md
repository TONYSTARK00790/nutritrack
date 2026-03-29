# 🥗 NutriTrack — Smart Calories Calculator & Meal Tracker

A modern, full-stack Django web application for tracking calories, planning meals, and monitoring your nutrition goals. Built with a stunning green-themed UI, dark mode, animated charts, and a pre-loaded Indian food database.

---

## ✨ Features

### 🔐 User Authentication
- Register / Login / Logout
- Secure password hashing (Django built-in)
- User-specific data isolation
- Profile with fitness stats

### 🧮 BMR & Calorie Calculator
- **Mifflin-St Jeor Formula** for accuracy
- Calculates BMR + TDEE based on activity level
- Shows targets for: Fat Loss, Maintenance, Muscle Gain
- Macro split: 30% Protein / 40% Carbs / 30% Fat
- BMI calculation with category
- Save results directly to your profile

### 🗃️ Food Database (35+ Pre-loaded Foods)
**Indian Staples:** Idli, Dosa, Chapati, Dal, Sambar, Poha, Upma, Aloo Paratha  
**Proteins:** Paneer, Chicken Breast, Boiled Egg, Fish, Egg White, Whey Protein  
**Fruits:** Banana, Apple, Mango, Orange  
**Dairy:** Milk, Curd, Greek Yogurt, Butter  
**Beverages:** Tea, Coffee, Coconut Water  
**Snacks:** Peanuts, Almonds, Biscuits  
**Grains:** Rice, Brown Rice, Oats, Quinoa

Features:
- Live search with instant filtering
- Filter by category (Veg, Non-Veg, Beverage, etc.)
- Click any food for detailed nutrition modal
- Add custom foods
- Admin panel management

### 🍽️ Meal Tracking
- Log meals by type: Breakfast, Lunch, Dinner, Snack
- **Auto-calculates** calories + macros from quantity (grams)
- Live calorie preview as you type
- Quick quantity shortcuts (50g, 100g, 150g, etc.)
- Edit and delete meals
- Date-based navigation (view any past day)

### 📊 Dashboard & Analytics
- Animated calorie ring (SVG progress circle)
- Daily progress bar toward goal
- Macro breakdown cards (Protein, Carbs, Fat)
- Doughnut chart for macro distribution
- **Weekly bar chart** with calorie goal line
- Meals grouped by type
- Profile completion prompts

### 🎨 UI/UX
- **Green primary theme** (`#22c55e`)
- **Dark / Light mode toggle** (persisted per user)
- Glassmorphism effects on notifications
- Smooth animations (fade-up, progress bars)
- Fully **responsive** — works on mobile
- **Sticky FAB button** (Add Meal) on mobile
- Bottom navigation bar on mobile

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip

### 2. Clone & Setup
```bash
git clone <your-repo-url>
cd nutritrack

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Load food database (35+ foods)
python manage.py loaddata meals/fixtures/foods.json

# Create superuser (for admin panel)
python manage.py createsuperuser

# OR use the all-in-one setup command:
python manage.py setup_nutritrack --demo
```

### 3. Run
```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

---

## 📁 Project Structure

```
nutritrack/
│
├── nutritrack/              # Django project config
│   ├── settings.py          # Settings (SQLite dev, PostgreSQL prod)
│   ├── urls.py              # Root URL routing
│   └── wsgi.py
│
├── accounts/                # User auth + profiles
│   ├── models.py            # UserProfile (BMR, goals, dark mode)
│   ├── views.py             # Login, Register, Profile, Dashboard
│   ├── forms.py             # Auth + Profile forms
│   └── urls.py
│
├── meals/                   # Core tracking app
│   ├── models.py            # Food & Meal models
│   ├── views.py             # CRUD + food search API
│   ├── forms.py             # Meal & Food forms
│   ├── admin.py             # Admin registration
│   ├── fixtures/
│   │   └── foods.json       # 35+ pre-loaded foods
│   └── management/
│       └── commands/
│           └── setup_nutritrack.py
│
├── calculator/              # BMR Calculator
│   ├── views.py             # Mifflin-St Jeor calculation
│   └── urls.py
│
├── templates/               # All HTML templates
│   ├── base.html            # Base layout (sidebar, mobile nav)
│   ├── dashboard.html       # Main dashboard with charts
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── meals/
│   │   ├── meal_list.html   # Date-based meal log
│   │   ├── add_meal.html    # Log meal with live preview
│   │   ├── food_database.html
│   │   └── add_food.html
│   └── calculator/
│       └── calculator.html  # BMR calculator with results
│
├── static/                  # Static files (CSS, JS)
├── requirements.txt
├── setup.sh                 # Bash setup script
└── manage.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | Django ORM |
| Frontend | HTML5, Tailwind CSS (CDN) |
| Charts | Chart.js 4.4 |
| Fonts | Syne (display) + DM Sans (body) |
| Auth | Django built-in auth |
| Icons | SVG (inline) |

---

## 🔧 Configuration

### Switch to PostgreSQL (Production)
In `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nutritrack_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables (Production)
```bash
export SECRET_KEY='your-long-random-secret-key'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
```

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `/` | Redirects to Dashboard |
| `/dashboard/` | Main dashboard |
| `/accounts/login/` | Login |
| `/accounts/register/` | Register |
| `/accounts/profile/` | User profile & goals |
| `/meals/` | Meal log (today) |
| `/meals/add/` | Log a new meal |
| `/meals/foods/` | Food database |
| `/meals/foods/add/` | Add custom food |
| `/calculator/` | BMR / Calorie calculator |
| `/admin/` | Django admin panel |

---

## 🔮 Future Enhancements

- [ ] Weight progress tracker with graph
- [ ] Water intake tracker
- [ ] Export daily report as PDF
- [ ] REST API (DRF) for mobile app
- [ ] Barcode scanner integration
- [ ] AI-powered meal suggestions
- [ ] Recipe builder with total macros
- [ ] Meal plan templates

---

## 👨‍💻 Demo Account
After running `python manage.py setup_nutritrack --demo`:
- **Username:** `demo`
- **Password:** `demo1234`

---

## 📄 License
MIT License — free to use and modify.
