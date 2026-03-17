# Logic Engine CLI
Task management system with SQLite persistence.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python -m src.cli add "Buy milk" -d "Get 2 gallons"
python -m src.cli list
python -m src.cli done 1
python -m src.cli delete 1
```

## Test
```bash
PYTHONPATH=src python3 -m unittest tests.test_task -v
```