#check if virtual environment is already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment"
    source backend/.venv/bin/activate
    uwsgi --manage-script-name --http-socket :5000 -R --ini uwsgi.ini
else
    uwsgi --manage-script-name --http-socket :5000 -R --ini uwsgi.ini
fi
