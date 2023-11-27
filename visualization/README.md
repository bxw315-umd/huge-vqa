flask --app visualization/app.py run --debug

or

(for powershell)
$env:FLASK_APP=".\visualization\app"
$env:FLASK_ENV="development"
python -m flask run