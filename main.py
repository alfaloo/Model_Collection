import pymysql
my_db = pymysql.connect(
    host='localhost',
    database='iex',
    user='root',
    password='',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = my_db.cursor()
create_user_table = """
CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(32) NOT NULL,
  `password` VARCHAR(256) NOT NULL,
  `is_admin` TINYINT NULL,
  PRIMARY KEY (`id`)
);"""
create_patient_table = """
CREATE TABLE `patient` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NOT NULL,
  `sex` VARCHAR(16) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `phone` VARCHAR(32) NOT NULL,
  `address` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`)
);"""
create_diagnosis_table = """
CREATE TABLE `diagnosis` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `author_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `category` VARCHAR(32) NOT NULL,
  `description` TEXT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `author_id_foreign_key`
    FOREIGN KEY (`author_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `patient_id_foreign_key`
    FOREIGN KEY (`patient_id`)
    REFERENCES `patient` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);
"""


# cursor.execute(create_user_table)
# cursor.execute(create_patient_table)
cursor.execute(create_diagnosis_table)
my_db.close()
