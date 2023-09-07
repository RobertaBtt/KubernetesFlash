from project import create_app, create_table_csv


# Calls the application factory function to construct a Flask application
app = create_app()
create_table_csv()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

