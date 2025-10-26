# Install Dependencies

Install based on your environment based on

[PyG](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)
and
[PyTorch](https://pytorch.org/get-started/locally/)

then use UV to sync other dependencies from `pyproject.toml`

```shell
uv sync --inexact
```

# Usage

> Note: You will have to edit the script to match your file system

Either use `create_indicies.py` on an existing SQLite DB

or run `create_graph.py` a directory of the csv data from EHRShot, then run `create_indicies.py`

Then, you can run `data_query.py` to generate the needed table, then `create_graph_drug_comp.py` if you want the graph described in the paper.
