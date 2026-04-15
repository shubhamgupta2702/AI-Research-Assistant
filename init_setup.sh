
echo "$(date): START"

echo "$(date): Creating virtual environment"
python -m venv .venv

echo "$(date): Activating virtual environment"
source .venv/Scripts/activate

echo "$(date): Upgrading pip"
pip install --upgrade pip

echo "$(date): Installing requirements"
pip install -r requirements.txt

# Optional: dev requirements
if [ -f requirements_dev.txt ]; then
  echo "$(date): Installing dev requirements"
  pip install -r requirements_dev.txt
fi

echo "$(date): DONE"