# habitats
Monitoring temperature and humidity in my apartment.

## Installation

Create and activate a local Conda environment with Python 3.9:

```bash
conda create -n habitats python=3.9
conda activate habitats
```

Then, from the repository root, install the package in editable mode:

```bash
pip install -e .
```

This makes the `habitats` package importable and installs the CLI entry points:

```bash
habitats-sync-sensors
habitats-collect-readings
```
