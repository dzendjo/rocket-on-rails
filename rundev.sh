export $(grep -v '^#' ../app.env) &&
python engine.py
