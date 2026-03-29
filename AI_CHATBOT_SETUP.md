# AI Chatbot Integration Setup

## Overview
NutriTrack now includes AI-powered chatbot functionality using OpenAI's GPT models for personalized nutrition and fitness advice.

## Features Added
- **Dashboard-integrated AI Chatbot**: Direct chatbot in the main dashboard area
- **Quick action buttons**: Pre-filled questions for common queries
- **Context-aware responses**: Considers your profile and nutrition data
- **Fallback system**: Works with or without OpenAI API key

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key (Optional but Recommended)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (keep it secure!)

### 3. Configure Environment
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### 4. Choose AI Model (Optional)
You can specify which GPT model to use in `.env`:
```
OPENAI_MODEL=gpt-3.5-turbo  # Faster, cheaper
# or
OPENAI_MODEL=gpt-4          # More accurate, expensive
```

### 5. Test the Integration
1. Start the Django server:
   ```bash
   python manage.py runserver
   ```

2. Visit the dashboard and use the AI chatbot section
3. Try the quick action buttons or type your own questions
4. If OpenAI is configured, responses will be powered by GPT
5. If not configured, it falls back to the basic chatbot

## Dashboard Chatbot Features

### Quick Action Buttons
- **Lunch ideas**: "What should I eat for lunch?"
- **Protein needs**: "How much protein do I need?"
- **Workout plan**: "Suggest a workout plan"

### AI-Powered Responses
- Personalized nutrition advice based on your profile
- Calorie and macro recommendations
- Meal planning suggestions
- Fitness and workout guidance
- Health and wellness tips

### Context-Aware
The AI considers:
- Your age, gender, height, weight
- Activity level and fitness goals
- Today's calorie intake and macros
- Meal history and preferences

### Fallback System
If OpenAI API is not available, the chatbot gracefully falls back to the existing rule-based responses.

### AI-Powered Responses
- Personalized nutrition advice based on your profile
- Calorie and macro recommendations
- Meal planning suggestions
- Fitness and workout guidance
- Health and wellness tips

### Context-Aware
The AI considers:
- Your age, gender, height, weight
- Activity level and fitness goals
- Today's calorie intake and macros
- Meal history and preferences

### Fallback System
If OpenAI API is not available, the chatbot gracefully falls back to the existing rule-based responses.

## API Usage & Costs

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens (very cost-effective)
- **GPT-4**: ~$0.03 per 1K tokens (higher quality but more expensive)
- Typical chat response: 100-200 tokens
- Monitor usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)

## Security Notes

- API keys are stored locally in `.env` file
- Never commit `.env` file to version control
- Add `.env` to your `.gitignore` file
- The app only sends user messages and basic profile data to OpenAI

## Troubleshooting

### "OpenAI API error" in console
- Check your API key is correct in `.env`
- Verify your OpenAI account has credits
- Check internet connection

### Still using basic chatbot
- Ensure `.env` file exists and is properly formatted
- Restart Django server after adding API key
- Check console for any import errors

## Testing the Dashboard Chatbot

1. Visit `http://127.0.0.1:8000/dashboard/`
2. Look for the "🤖 AI Nutrition Assistant" section in the main content area
3. Try clicking the quick action buttons:
   - "Lunch ideas"
   - "Protein needs" 
   - "Workout plan"
4. Or type your own nutrition questions in the input field
5. The chatbot should respond with personalized advice based on your profile data

## Welcome Message
The dashboard chatbot greets users with: **"May I help you with your nutrition goals?"** and provides quick action buttons for common queries.