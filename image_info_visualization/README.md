flask --app image_info_visualization/app.py run --debug

or

(for powershell)
$env:FLASK_APP=".\image_info_visualization\app"
$env:FLASK_ENV="development"
python -m flask run