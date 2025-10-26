import sqlite3

import pandas as pd

import torch
from torch_geometric.data import Data

conn = sqlite3.connect(
    "../EHR2000.db"
)  # Connect (and create if it doesn't exist) database
curr = conn.cursor()  # Object to run queries

full_clean = "project_full_sampled_data_clean"
full_drug_comp = "project_full_sampled_data_drug_comp"

table = full_drug_comp

medicationdf = pd.read_sql_query(
    f"""
    SELECT DISTINCT drug_ingredient_concept_id, drug_name FROM {table}
    ORDER BY drug_ingredient_concept_id
    """,
    conn,
)

df = pd.read_sql_query(
    f"""
    SELECT person_id, drug_ingredient_concept_id, drug_name, COUNT(drug_ingredient_concept_id) FROM {table}
    WHERE drug_ingredient_concept_id != 0
    GROUP BY drug_ingredient_concept_id, person_id
    ORDER BY person_id
    """,
    conn,
)


conn.close()

# Notes:
# Goal:
#   create a graph with
#   nodes: medications
#   edges: co-occur together in a patient (weighted)

# process:
#   --Generate nodes--
#   query for a unique list of medications
#   for each medication:
#     create a node

#   --Generate edges--
#   scan list of patients, ordered by patient id and grouped by drug_ingredient_concept_id
#   any medication that occurs together in a single patient is connected


# Generate adjacency_list (edges)

a = 0
b = 1

adjacency_list = dict()

while b < len(df):
    rowA, rowB = df.iloc[a], df.iloc[b]
    medicationA, medicationB = (
        rowA["drug_ingredient_concept_id"],
        rowB["drug_ingredient_concept_id"],
    )
    idA, idB = rowA["person_id"], rowB["person_id"]
    if medicationA != medicationB and idA == idB:
        if medicationA not in adjacency_list:
            adjacency_list[medicationA] = dict()
        AtoB = adjacency_list[medicationA].get(medicationB)
        AtoB = AtoB if AtoB is not None else 0
        adjacency_list[medicationA][medicationB] = AtoB + 1

        if medicationB not in adjacency_list:
            adjacency_list[medicationB] = dict()
        BtoA = adjacency_list[medicationB].get(medicationA)
        BtoA = BtoA if BtoA is not None else 0
        adjacency_list[medicationB][medicationA] = BtoA + 1

    a += 1
    b += 1

# adjacency_list = {
#   medication1 : {medication4: 1, medication2: 5, medication3: 2}
# }

# Create edge tensors for PyG

edge_list = [[], []]
edge_weights = []

for edge, connections in adjacency_list.items():
    for connection, weight in connections.items():
        edge_list[0].append(edge)
        edge_list[1].append(connection)
        edge_weights.append([weight])


edge_index = torch.tensor(edge_list, dtype=torch.long)
edge_attr = torch.tensor(edge_weights, dtype=torch.int64)


def pyg_data_to_edges_csv(data, filename="edges.csv"):
    if data.edge_index is None or data.edge_index.numel() == 0:
        print("No edges to export")
        return

    src, dst = data.edge_index
    src = src.cpu().numpy()
    dst = dst.cpu().numpy()

    edge_data = {"source": src, "target": dst}

    # Add edge attributes (e.g., weights) if present
    if hasattr(data, "edge_attr") and data.edge_attr is not None:
        edge_attr = data.edge_attr.cpu().numpy()
        for i in range(edge_attr.shape[1]):
            edge_data["weight"] = edge_attr[:, i]

    df = pd.DataFrame(edge_data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(src)} edges to {filename}")


nodes = []
node_drug_name = []

for i in range(0, len(medicationdf)):
    med = medicationdf.iloc[i]
    drug_id = med["drug_ingredient_concept_id"]
    nodes.append(drug_id)
    drug_name = med["drug_name"]
    node_drug_name.append(drug_name)

node_data = {"id": nodes, "Label": node_drug_name}

df = pd.DataFrame(node_data)

df.to_csv("nodes.csv", index=False)

data = Data(edge_index=edge_index, edge_attr=edge_attr)

pyg_data_to_edges_csv(data)
