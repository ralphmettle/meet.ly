from app import create_app
from waitress import serve

run_app = create_app()

if __name__ == '__main__':
    # serve(run_app, host='0.0.0.0', port=8080)
    run_app.run(debug=True)