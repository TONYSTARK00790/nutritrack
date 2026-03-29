# Chatbox Troubleshooting Guide

## What Should Happen When You Open the Dashboard

1. **👁️ Chatbox Visibility**
   - On **desktop (lg screens)**: Chatbox appears on the RIGHT side of the dashboard
   - On **mobile/tablet**: Chatbox might appear at the bottom or need scrolling
   - The chatbox shows a robot emoji (🤖) with "AI-Powered Support Ready" text
   - Below that are 4 quick mood buttons: 😴 Tired, 💪 Motivated, ❓ Confused, 😓 Struggling
   - At the bottom is a "Start Chat 💬" button

2. **🔵 Using the Chatbox**
   - **Option 1**: Click the "Not Feeling Well 💬" button in the top right
     - A modal appears asking "What's Bothering You?"
     - Choose from 7 reasons (fitness, nutrition, health, etc.)
     - Chat opens with personalized greeting
   
   - **Option 2**: Click "Start Chat 💬" button inside the chatbox
     - Same reason selection modal appears
     - Chat opens

   - **Option 3**: Use Quick Mood buttons (😴 Tired, 💪 Motivated, etc.)
     - Immediately sends a pre-filled message related to that mood
     - Chat activates instantly

## If Chatbox is NOT Working

### Step 1: Verify Visibility
```
□ Can you see the "Your AI Support" header on the right side?
□ Can you see the robot emoji (🤖) below it?
□ Can you see the 4 mood buttons?
□ Can you see the "Start Chat 💬" button?
```

If **NO** to any:
- **On mobile**: Try landscape orientation or larger screen
- **On desktop**: Check if sidebar is covering it - scroll right
- Check browser zoom level (Ctrl + 0 to reset)

### Step 2:Test Button Click
```
□ Can you click the "Not Feeling Well 💬" button in the top navigation?
□ Does a modal appear with "What's Bothering You?" title?
□ Can you see 7 buttons with emojis in the modal?
```

If **NO**:
- Open Browser Console (F12 → Console tab)
- Look for red ERROR messages
- Try refreshing the page (Ctrl + F5)
- Clear browser cache

### Step 3: Test Modal Interaction
```
□ Click "💪 Fitness Motivation" in the modal
□ Do you see a chat message appear?
□ Does the modal close?
```

If **NO**:
- Check Browser Console for errors
- Check if JavaScript is enabled in your browser
- Try a different browser

### Step 4: Test Chat Message
```
□ Type a message in the input field
□ Click "Send" button
□ Do you see your message appear in blue?
□ Does a bot response appear in below?
```

If **NO**:
- Check Network tab (F12 → Network)
- Send a message and look for failed requests
- Check if /accounts/api/chat/send/ is responding with 200 status

## Browser Console Debugging (F12 → Console)

Try these commands:

```javascript
// Check if elements exist
document.getElementById('notWellBtn')  // Should show: <button id="notWellBtn">...</button>
document.getElementById('reasonModal')  // Should show: <div id="reasonModal">...</div>
document.getElementById('chatboxPanel')  // Should show: <div id="chatboxPanel">...</div>

// Check if functions exist
typeof startChat  // Should show: "function"
typeof sendMessage  // Should show: "function"
typeof getCsrfToken  // Should show: "function"

// Test chat creation manually
fetch('/accounts/api/chat/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken()
  },
  body: JSON.stringify({ reason: 'fitness' })
}).then(r => r.json()).then(d => console.log(d))

// Should show: {status: 'ok', session_id: XX, initial_message: '...'}
```

## Server Status Check

Run this command to verify the API is working:

```bash
python manage.py shell
>>> from accounts.models import UserProfile, ChatSession, ChatMessage
>>> ChatSession.objects.all().count()  # Should show count > 0
```

## If You Get a 500 Error

Check Django logs:
1. Look at the terminal where Django server is running
2. You should see error messages
3. Share those errors for debugging

## Quick Fix Checklist

- [ ] Server is running (`python manage.py runserver`)
- [ ] You're logged in (not on login page)
- [ ] Browser console shows no red errors
- [ ] You can access http://localhost:8000/dashboard/
- [ ] Page content loads (meals, nutrition data visible)
- [ ] Try browser refresh (Ctrl + F5)
- [ ] Try different browser (Chrome, Firefox, Edge)
- [ ] Clear browser cache and cookies

---

**If still not working**: Share:
1. Browser Console errors (F12 → Console tab, take screenshot)
2. Network tab failures (F12 → Network tab, try clicking button)
3. Terminal/server logs where Django is running
4. Exact steps you took before getting stuck
