# 🖼️ Food Image Upload Guide - NutriTrack

Your image upload infrastructure is now fully set up! Here are the **3 ways** to add images for your 360 foods:

---

## **Option 1: Django Admin Panel** (Best for 1-50 foods)

### Quick Steps:
1. **Start server**: `python manage.py runserver`
2. **Go to**: http://localhost:8000/admin/
3. **Login** with your admin credentials
4. **Click "Foods"** → Select any food → Scroll to **Image** field
5. **Click "Choose File"** → Upload JPG/PNG (300x300px or larger recommended)
6. **Click "Save"** → Image stored in `media/food_images/`

✅ **Pros**: Visual, immediate feedback, no command line needed  
❌ **Cons**: Manual for 360 foods (tedious)

---

## **Option 2: Batch Upload Script** (Best for bulk uploads)

### Perfect for uploading all 360 foods at once!

### Step 1: Prepare Your Images
Create a folder with images named exactly like food names (case-insensitive):

```
my_food_images/
  ├── Samosa.jpg
  ├── Biryani.jpg
  ├── Butter Chicken.jpg
  ├── Paneer Tikka.png
  ├── KFC Fried Chicken.jpg
  └── ... (360 images total)
```

**💡 Filename Rules:**
- Must match food name exactly (case-insensitive)
- Extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Examples: `samosa.jpg`, `BIRYANI.PNG`, `KFC fried chicken.jpg`

### Step 2: Test with Dry Run (RECOMMENDED)
See what will be uploaded without making changes:

```bash
python manage.py batch_upload_images /path/to/my_food_images --dry-run
```

**Example output:**
```
Found 360 image files
  ✓ WOULD UPLOAD: Samosa (Samosa.jpg)
  ✓ WOULD UPLOAD: Biryani (Biryani.jpg)
  ⚠ NOT FOUND: SomeUnknownFood - no matching food in database
  
Summary:
  📁 Total image files: 360
  ✓ Matched foods: 358
  [DRY RUN] Would upload: 358
```

### Step 3: Upload for Real
Once you're happy with the dry run:

```bash
python manage.py batch_upload_images /path/to/my_food_images
```

**Console output:**
```
✓ UPLOADED: Samosa (Samosa.jpg)
✓ UPLOADED: Biryani (Biryani.jpg)
✓ UPLOADED: Butter Chicken (Butter Chicken.jpg)

Summary:
  📁 Total image files: 360
  ✓ Matched foods: 358
  ✓ Successfully uploaded: 358
  ⚠ Skipped (already have image): 2

✅ Upload complete!
```

### Step 4: Verify on Website
- Refresh food database page: http://localhost:8000/meals/foods/
- Food cards now show uploaded images at the top
- Hover over images for zoom effect
- Category icons show as fallback if no image

---

## **Option 3: Individual Admin Upload** (Best for replacing specific images)

To update a single food's image:

1. **Admin panel**: http://localhost:8000/admin/foods/
2. **Search** for the food
3. **Click to edit**
4. **Find Image field** → Click "Clear" to remove old, then "Choose File"
5. **Upload new image**
6. **Save**

---

## **Getting Food Images** (If you don't have them)

### Option A: Free Image Resources
- **Unsplash**: https://unsplash.com (free high-quality images)
  - Search: "samosa", "biryani", "chicken tikka", etc.
  - Download → Rename to match food names
  
- **Pexels**: https://www.pexels.com
  - Same process as Unsplash
  
- **Pixabay**: https://pixabay.com
  - Large food image database

### Option B: AI Image Generation
- **DALL-E**: Generate food images (requires account)
- **Stable Diffusion**: Open-source image generation
- **Midjourney**: High-quality AI food images

### Option C: YouTube Screenshots
1. Search YouTube for "Indian food names"
2. Take clean screenshots (high contrast)
3. Save as JPG with food name

### Option D: Restaurant Photos
- Most chain restaurants have online menus with food photos
- Can download or screenshot and rename

---

## **Image Recommendations**

### Size Guidelines:
- **Minimum**: 200x200 pixels
- **Recommended**: 400x400 to 800x800 pixels (larger = better quality)
- **Format**: JPG (smaller file size) or PNG (supports transparency)

### Best Practices:
- ✅ Clear, well-lit food photos
- ✅ White or neutral background
- ✅ Food fills 60-80% of image
- ✅ High contrast (readable at small sizes)
- ✅ Consistent style across images
- ❌ Avoid: Blurry, dark, cluttered, or rotated images
- ❌ Avoid: Text overlays or watermarks

---

## **Troubleshooting**

### Image not showing?
1. Check filename matches food name exactly (case-insensitive)
2. Verify file format is `.jpg`, `.png`, `.gif`, or `.webp`
3. Run dry-run again: `python manage.py batch_upload_images [folder] --dry-run`

### Batch upload says "NOT FOUND"?
- That food doesn't exist in database
- Check spelling in database vs filename
- May need to add food first via Food Add page or admin

### Already has image warning?
- Food already has an image uploaded
- To replace: Use admin panel → click "Clear" → upload new image
- Or delete current image and re-run batch script

### Command not found error?
- Ensure you're in project directory: `cd /path/to/nutritrack`
- Run: `python manage.py batch_upload_images --help`

---

## **Current System Status** ✅

✅ **Image field added** to Food model  
✅ **Database migration applied** (0003_food_image)  
✅ **Admin interface configured** for image uploads  
✅ **Food database template updated** to display images  
✅ **Media serving configured** (static file handling)  
✅ **Batch upload script created** (batch_upload_images.py)  
✅ **Image storage ready** (media/food_images/ directory)  

---

## **What Happens When You Upload Images?**

### Backend (Django handles automatically):
1. File uploaded → saved to `media/food_images/food_name_timestamp.jpg`
2. File path stored in Food model's `image` field
3. Accessible via `{{ food.image.url }}` in templates

### Frontend (visible to users):
- Food cards show image in header
- Hover over image → zoom animation
- Falls back to category icon if no image
- Responsive design (mobile/tablet/desktop)

---

## **Quick Commands Reference**

```bash
# Test upload (no changes made)
python manage.py batch_upload_images ./my_images --dry-run

# Actually upload images
python manage.py batch_upload_images ./my_images

# View admin panel
http://localhost:8000/admin/

# View food database
http://localhost:8000/meals/foods/

# Check media folder
ls -la media/food_images/
```

---

## **Next Steps**

1. **Gather 360 food images** (~2-4 hours depending on source)
2. **Organize in folder** following naming convention
3. **Run dry-run** to verify matches
4. **Execute batch upload** when ready
5. **Refresh website** and enjoy visual food database!

**Total time to implement**: 10-15 minutes for the script + 2-4 hours to gather images = **Ready in ~4 hours!**

---

**Questions?** Check the batch upload help:
```bash
python manage.py batch_upload_images --help
```
