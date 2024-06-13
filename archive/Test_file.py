from utils.Database_file import Database

db = Database()
images_real = db.select_images_real()
images_ai = db.select_images_ai()
print(images_ai)
