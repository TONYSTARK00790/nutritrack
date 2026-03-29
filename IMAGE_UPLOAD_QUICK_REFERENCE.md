# 📸 Image Upload Cheatsheet - Quick Reference

## ⚡ TL;DR - 3 Steps to Add 360 Food Images

```bash
# Step 1: Gather 360 images, name them like your foods
my_images/
  ├── Samosa.jpg
  ├── Biryani.jpg
  └── ... (360 files)

# Step 2: Test the upload (DRY RUN - no changes)
python manage.py batch_upload_images ./my_images --dry-run

# Step 3: Actually upload
python manage.py batch_upload_images ./my_images

# Done! Refresh http://localhost:8000/meals/foods/
```

---

## 3 Upload Methods

### 1️⃣ **Admin Panel** (Manual, 1-50 foods)
```
http://localhost:8000/admin/ → Foods → Click food → Upload image → Save
```

### 2️⃣ **Batch Upload** (ALL 360 foods) ⭐
```bash
# See what will upload (safe to test)
python manage.py batch_upload_images /path/to/images --dry-run

# Actually upload all images
python manage.py batch_upload_images /path/to/images
```

### 3️⃣ **List Foods First** (Get correct filenames)
```bash
# See all 360 food names
python manage.py list_foods

# Export to CSV for reference
python manage.py list_foods --export foods.csv

# See which need images (✗)
python manage.py list_foods | grep "✗"
```

---

## 📝 Image Naming Rules

✅ **Good**:
- `Samosa.jpg` - matches "Samosa"
- `butter chicken.png` - matches "Butter Chicken" (case-insensitive)
- `BIRYANI.JPG` - matches "Biryani"

❌ **Bad**:
- `Samosa_1.jpg` - extra characters
- `samosa-crispy.jpg` - doesn't match "Samosa"
- `samosa` - no extension

**Auto Fix**: Run `python manage.py list_foods` to see exact food names!

---

## 🔍 Verify It Worked

```bash
# See how many foods have images now
python manage.py list_foods | grep "✓"

# Check image files stored
ls -la media/food_images/

# See details of specific food
python manage.py list_foods --cuisine indian
```

---

## 🎯 Image Resources

**Free Images** (pick any):
- Unsplash.com - type "samosa", download, rename
- Pexels.com - same process
- Pixabay.com - large food database
- YouTube - screenshot from recipe videos

**AI Generated** (create perfect images):
- DALL-E: "photo of samosa on plate"
- Midjourney: high-quality food images
- Stable Diffusion: open-source alternative

---

## ⚙️ What Gets Installed

| Item | What It Does | File |
|------|-------------|------|
| Image field | Stores image path in database | `models.py` |
| Migration | Updates database schema | `0003_food_image.py` |
| Admin UI | Upload images in admin panel | `admin.py` |
| Template | Shows images on website | `food_database.html` |
| Batch cmd | Upload 360 images at once | `batch_upload_images.py` |
| List cmd | View/export food names | `list_foods.py` |

---

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "NOT FOUND" error | Food doesn't exist. Run `list_foods` to check |
| Can't find command | Make sure in project directory: `cd nutritrack` |
| Image won't show | Filename doesn't match (case matters sort of). Use `list_foods` |
| Dry run failed | Check image format (.jpg, .png, .gif, .webp) |
| Already has image | Use admin panel to replace old image |

---

## 📊 Summary Stats

```
🍽️  Total foods: 360
  ├─ Indian: 251 (69.7%) - samosas, biryanis, street foods, etc.
  ├─ Chinese: 30 (8.3%)
  └─ Continental: 79 (21.9%)

📁 Storage: media/food_images/
```

---

## 🚀 Full Instructions Elsewhere

- **Detailed Guide**: Read [IMAGE_UPLOAD_GUIDE.md](IMAGE_UPLOAD_GUIDE.md)
- **Technical Details**: See [IMAGE_UPLOAD_IMPLEMENTATION.md](IMAGE_UPLOAD_IMPLEMENTATION.md)

---

## Quick Copy-Paste Commands

```bash
# See all foods with image status
python manage.py list_foods

# See which foods NEED images (show ✗)
python manage.py list_foods | findstr "✗"  # Windows
python manage.py list_foods | grep "✗"     # Mac/Linux

# Test upload (always do this first!)
python manage.py batch_upload_images ./my_images --dry-run

# Actually upload
python manage.py batch_upload_images ./my_images

# Export food list for naming reference
python manage.py list_foods --export food_names.csv

# Check what was uploaded
ls -la media/food_images/ | head -20
```

---

**Status**: ✅ Everything ready! Just add images and run the batch upload command.
