    # def refresh_images(self):
    #     """Refresh image list from directories and update the database."""
    #     real_path = Path("images/real")
    #     genai_path = Path("images/genai")

    #     cursor = self.conn.cursor()

    #     for img_path in real_path.glob("*"):
    #         creator_name = img_path.stem.split("_")[0]
    #         cursor.execute(
    #             "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)",
    #             (creator_name,),
    #         )
    #         cursor.execute(
    #             "SELECT creator_id FROM creators WHERE creator_name = ?",
    #             (creator_name,),
    #         )
    #         creator_id = cursor.fetchone()[0]
    #         cursor.execute(
    #             "INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) VALUES (?, 1, 1, ?)",
    #             (creator_id, str(img_path).replace("\\", "/")),
    #         )

    #     for img_path in genai_path.glob("*"):
    #         creator_name = img_path.stem.split("_")[0]
    #         cursor.execute(
    #             "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)",
    #             (creator_name,),
    #         )
    #         cursor.execute(
    #             "SELECT creator_id FROM creators WHERE creator_name = ?",
    #             (creator_name,),
    #         )
    #         creator_id = cursor.fetchone()[0]
    #         cursor.execute(
    #             "INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) VALUES (?, 0, 1, ?)",
    #             (creator_id, str(img_path).replace("\\", "/")),
    #         )

    #     self.conn.commit()
#--------------------------
