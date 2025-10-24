import sqlite3

conn = sqlite3.connect(
    "EHR2000.db"
)  # Connect (and create if it doesn't exist) database
curr = conn.cursor()  # Object to run queries

curr.execute(
    """
    CREATE INDEX "idx_concept_ancestor_id" ON "concept_ancestor" (
        "ancestor_concept_id"
    );
    """
)

curr.execute(
    """
    CREATE INDEX "idx_concept_descendant_id" ON "concept_ancestor" (
        "descendant_concept_id"
    );
    """
)

curr.execute(
    """
    CREATE INDEX "idx_drug_concept_id" ON "sampled_drug_exposure" (
        "drug_concept_id"
    );
    """
)

curr.execute(
    """
    CREATE INDEX "idx_drug_exposure_person_id" ON "sampled_drug_exposure" 
    (
        "person_id"
    );
    """
)

curr.execute(
    """
    CREATE INDEX "idx_drug_type_concept_id" ON "sampled_drug_exposure" (
        "drug_type_concept_id"
    );
    """
)

curr.execute(
    """
    CREATE UNIQUE INDEX "idx_person_id" ON "sampled_person" (
        "person_id"
    );
    """
)

curr.execute(
    """
    CREATE INDEX "idx_concept_relationship_concept_id" ON "concept_relationship" (
        "concept_id_1",
        "concept_id_2"
    )   
    """
)

curr.execute(
    """
    CREATE INDEX "idx_concept_relationship_relationship_id" ON "concept_relationship" (
        "relationship_id"
    )
    """
)

conn.close()
