from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# Function to fetch data from the PostgreSQL database
def get_ads_from_database():
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {os.getenv('POSTGRES_TABLE')};")
    ads = cursor.fetchall()
    conn.close()
    return ads

@app.route("/")
def index():
    # Fetch data from the database
    ads = get_ads_from_database()
    app.logger.error(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa{ads[-2:]}')
    return render_template("index.html", ads=ads)

if __name__ == "__main__":
    app.logger.info("run() called")
    app.run()