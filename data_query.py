import sqlite3

conn = sqlite3.connect(
    "../EHR2000.db"
)  # Connect (and create if it doesn't exist) database
curr = conn.cursor()  # Object to run queries


curr.execute("""
    CREATE TABLE project_full_sampled_data_drug_comp AS
    SELECT p.*, d.*, c.concept_name as drug_name, ca.ancestor_concept_id as drug_component_id FROM sampled_person as p
    JOIN sampled_drug_exposure as d ON p.person_id=d.person_id
    LEFT JOIN concept_ancestor as ca ON d.drug_concept_id = ca.descendant_concept_id
    LEFT JOIN concept as c ON ca.ancestor_concept_id = c.concept_id
    WHERE 
        d.drug_concept_id != 0
    AND
        c.concept_class_id = 'Clinical Drug Comp'
    ORDER BY p.person_id
""")


conn.commit()

conn.close()
