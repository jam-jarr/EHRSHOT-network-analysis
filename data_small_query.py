import sqlite3

conn = sqlite3.connect(
    "../EHR2000.db"
)  # Connect (and create if it doesn't exist) database
curr = conn.cursor()  # Object to run queries

# create sampled person table
curr.execute("""
	CREATE TABLE small_person AS
	SELECT * FROM sampled_person
    ORDER BY RANDOM()
	LIMIT 200
""")

# create sampled_data table
curr.execute("""
    CREATE TABLE project_small_sampled_data AS 
    SELECT p.*, d.*, dc.concept_name as drug_name FROM small_person as p
    JOIN sampled_drug_exposure as d ON p.person_id=d.person_id
    LEFT JOIN concept as dc ON d.drug_concept_id=dc.concept_id
    ORDER BY p.person_id
""")

curr.execute("""
    CREATE INDEX idx_small_person_id
    ON small_person (person_id)
""")

conn.commit()

conn.close()
