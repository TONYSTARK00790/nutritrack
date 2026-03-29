# 📚 Batch Upload Examples & Use Cases

## Example 1: Upload All 360 Foods (Complete Scenario)

### Setup
```bash
# Create image folder
mkdir food_images
cd food_images

# Download all 360 images from your source
# (Unsplash, YouTube screenshots, AI generation, etc.)
# Name them exactly like the foods:
#   samosa.jpg
#   biryani.jpg
#   butter chicken.png
#   ... (360 files)

# Verify you have 360 files
ls -la | wc -l    # Should show 362-365 (360 + . + ..)
```

### Test Upload (Recommended!)
```bash
cd ..  # Go back to project root
python manage.py batch_upload_images ./food_images --dry-run
```

**Output Example:**
```
Found 360 image files
  ✓ WOULD UPLOAD: Samosa (Samosa.jpg)
  ✓ WOULD UPLOAD: Biryani (Biryani.jpg)
  ✓ WOULD UPLOAD: Butter Chicken (Butter Chicken.jpg)
  ✓ WOULD UPLOAD: Paneer Tikka (Paneer Tikka.jpg)
  ✓ WOULD UPLOAD: Gol Gappa (Gol Gappa.jpg)
  ✓ WOULD UPLOAD: Dal Makhani (Dal Makhani.jpg)
  ...
  ⚠ NOT FOUND: RandomImageNameThatDoesntMatch.jpg

Summary:
  📁 Total image files: 361
  ✓ Matched foods: 360
  [DRY RUN] Would upload: 360
  ⚠ Skipped (already have image): 0

⚠️  DRY RUN MODE - No changes made. Run without --dry-run to upload.
```

### Actually Upload
```bash
python manage.py batch_upload_images ./food_images

# This takes 30-60 seconds depending on image sizes
```

**Output Example:**
```
Found 360 image files
  ✓ UPLOADED: Samosa (Samosa.jpg)
  ✓ UPLOADED: Biryani (Biryani.jpg)
  ✓ UPLOADED: Butter Chicken (Butter Chicken.jpg)
  ... (357 more uploads) ...
  ✓ UPLOADED: Chai (Chai.png)

Summary:
  📁 Total image files: 360
  ✓ Matched foods: 360
  ✓ Successfully uploaded: 360
  ⚠ Skipped (already have image): 0

✅ Upload complete!
```

### Verify
```bash
# Check uploaded files
ls -la media/food_images/
# Should show 360 image files like:
#   Samosa_1704234521.jpg
#   Biryani_1704234522.jpg
#   ... etc

# Verify via command
python manage.py list_foods | grep "✓" | wc -l
# Should show: 360

# Or check in admin
http://localhost:8000/admin/foods/
# You'll see checkmarks next to foods with images
```

---

## Example 2: Partial Upload (Gradual Approach)

### Scenario: Start with Indian foods only

```bash
# Create folders by cuisine
mkdir food_images_indian
mkdir food_images_chinese
mkdir food_images_continental

# Download just Indian images first (251 foods)
# cp samosa_image.jpg food_images_indian/Samosa.jpg
# cp biryani_image.jpg food_images_indian/Biryani.jpg
# ... (up to 251)
```

### Upload Indian Foods
```bash
python manage.py batch_upload_images ./food_images_indian --dry-run
# Check: should show 251 matched foods

python manage.py batch_upload_images ./food_images_indian
# ✅ 251 Indian foods now have images!
```

### Later: Add Chinese Foods
```bash
python manage.py batch_upload_images ./food_images_chinese --dry-run
python manage.py batch_upload_images ./food_images_chinese
# ✅ 30 Chinese foods added!
```

### Finally: Add Continental Foods
```bash
python manage.py batch_upload_images ./food_images_continental --dry-run
python manage.py batch_upload_images ./food_images_continental
# ✅ 79 Continental foods added!
# Total: 360 foods!
```

### Check Progress
```bash
python manage.py list_foods | grep "✓" | wc -l
# After step 1: 251
# After step 2: 281 (251 + 30)
# After step 3: 360 (251 + 30 + 79) ✅
```

---

## Example 3: Update Existing Images

### Scenario: Want to replace some low-quality images

```bash
# Create folder with better versions
mkdir better_images
cp nice_samosa.jpg better_images/Samosa.jpg
cp nice_biryani.jpg better_images/Biryani.jpg
# ... (just the ones you want to replace)
```

### Current Issue: Command skips if image exists
```bash
python manage.py batch_upload_images ./better_images --dry-run

# Output:
# ✓ WOULD UPLOAD: Samosa (nice_samosa.jpg)
# ⚠ SKIP: Biryani - already has image
```

### Solution: Replace via Admin Panel
```
1. Go to http://localhost:8000/admin/foods/
2. Find "Biryani"
3. Scroll to Image field
4. Click "Clear"
5. Click "Choose File" 
6. Upload the better_images/Biryani.jpg
7. Save
```

Then batch upload will pick it up next time!

---

## Example 4: Getting Food Names for Image Naming

### View All Foods
```bash
python manage.py list_foods

# Output:
# 📋 360 Food(s) Found:
# ────────────────────────────────────────────
#   1. [✗] Samosa                    | Snack     | Indian
#   2. [✗] Biryani                   | Grain     | Indian
#   3. [✗] Butter Chicken            | Non-Veg   | Indian
#   ... (357 more) ...
# 360. [✗] Panipuri                  | Snack     | Indian
#
# Summary:
#   Total: 360
#   ✓ With images: 0
#   ✗ Without images: 360
```

### Export to CSV for Reference
```bash
python manage.py list_foods --export food_names.csv

# Creates file: food_names.csv with:
# Food Name,Category,Cuisine,Calories,Protein,Carbs,Fat
# Samosa,Snack,Indian,250,5.2,45.2,8
# Biryani,Grain,Indian,280,8.1,52.3,6
# ... (358 more rows)
```

### Use CSV to Name Images
1. Open food_names.csv in Excel/Sheets
2. Download images for each food
3. Name file exactly like "Food Name" column:
   - Samosa.jpg
   - Biryani.jpg
   - Butter Chicken.jpg
   - etc.

---

## Example 5: Filter by Category

### Upload Only Vegetarian Foods
```bash
python manage.py list_foods --category veg

# Shows only vegetarian foods:
# Samosa, Paneer Tikka, Aloo Gobi, etc.

# Then when uploading, can upload just veg folder
python manage.py batch_upload_images ./veg_images --dry-run
```

### Upload by Cuisine
```bash
python manage.py list_foods --cuisine indian

# Shows only 251 Indian foods
python manage.py list_foods --cuisine chinese

# Shows only 30 Chinese foods
python manage.py list_foods --cuisine continental

# Shows only 79 Continental foods
```

---

## Example 6: Troubleshooting - Finding Mismatches

### Problem: Some images not uploading

```bash
# First, list ALL foods
python manage.py list_foods > all_foods.txt

# Then check what's in your image folder
ls food_images/ > image_list.txt

# Compare the two files
# Any food name in all_foods.txt but NOT in image_list.txt = missing image

# Example mismatch:
# Database has: "Samosa Pack"
# Your file is: "Samosa.jpg"  ❌ Won't match!
# Should be: "Samosa Pack.jpg"  ✅
```

### Run dry-run to identify issues
```bash
python manage.py batch_upload_images ./food_images --dry-run | grep "NOT FOUND"

# Shows exactly which foods didn't match:
# ✗ NOT FOUND: wrong_name.jpg
# ✗ NOT FOUND: misspelled.jpg
```

### Fix and retry
```bash
# Rename the problematic files
mv food_images/wrong_name.jpg food_images/"Correct Food Name".jpg

# Try again
python manage.py batch_upload_images ./food_images --dry-run

# Should now show:
# ✓ WOULD UPLOAD: Correct Food Name
```

---

## Example 7: Different Image Types

### Mix of formats
```bash
food_images/
├── Samosa.jpg           ✓ JPG format
├── Biryani.png          ✓ PNG format (transparent OK)
├── Paneer Tikka.gif     ✓ GIF format (works but larger)
├── Butter Chicken.webp  ✓ WebP format (modern, small)
└── Some Image.bmp       ❌ BMP not supported - skip
```

### Upload behavior
```bash
python manage.py batch_upload_images ./food_images --dry-run

# Result:
# ✓ WOULD UPLOAD: Samosa (Samosa.jpg)
# ✓ WOULD UPLOAD: Biryani (Biryani.png)
# ✓ WOULD UPLOAD: Paneer Tikka (Paneer Tikka.gif)
# ✓ WOULD UPLOAD: Butter Chicken (Butter Chicken.webp)
# [Some Image.bmp ignored - unsupported format]

# Command supports: JPG, JPEG, PNG, GIF, WEBP
# Command ignores: BMP, TIFF, SVG, etc.
```

---

## Example 8: Large Image Optimization

### Problem: 360 images = lots of storage

### Solution: Optimize before upload
```bash
# Using ImageMagick (install if needed)
for img in food_images/*; do
  # Resize to 800x800 max, compress quality to 85%
  convert "$img" -resize 800x800\> -quality 85 "$img"
done

# Reduces size by 50-70% while keeping quality!
```

### Or use online tool
```
Go to: tinypng.com
Upload: food_images/ folder
Download: Compressed versions
Rename files to match foods again
```

### Result
```
Before optimization: 1.2 GB (360 images)
After optimization: 300-400 MB
Upload speed: 2-3x faster!
Website load: Faster image display!
```

---

## Quick Reference Commands

```bash
# See all foods
python manage.py list_foods

# See foods that need images (✗)
python manage.py list_foods | grep "✗"

# Export food names
python manage.py list_foods --export foods.csv

# Filter by cuisine
python manage.py list_foods --cuisine indian
python manage.py list_foods --cuisine chinese
python manage.py list_foods --cuisine continental

# Filter by category  
python manage.py list_foods --category veg
python manage.py list_foods --category non_veg

# TEST upload (always first!)
python manage.py batch_upload_images ./images --dry-run

# Actually upload
python manage.py batch_upload_images ./images

# Check how many have images now
python manage.py list_foods | grep "✓" | wc -l
```

---

**Tip**: Always run `--dry-run` first to catch naming mismatches before uploading!
