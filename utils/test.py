from database import Database

db = Database()
images = db.select_images_real()
print(images)
