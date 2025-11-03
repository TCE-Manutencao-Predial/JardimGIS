# jardimgis.py - Sistema JardimGIS

from app import create_app
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

if __name__ == '__main__':
    serve(app, listen='127.0.0.1:4242')
    # app.run(debug=True)
