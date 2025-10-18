# Install Dependencies

Either install based on your environment based on

[PyG](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)
and
[PyTorch](https://pytorch.org/get-started/locally/)

then use UV to sync other dependencies from `pyproject.toml`

```shell
uv sync --inexact
```

You can also simply use pip for a cpu & linux installation (compatible with WSL)
```shell
pip install -r requirements.txt
```
