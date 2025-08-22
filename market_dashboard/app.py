"""Flask application serving the market dashboard."""

from __future__ import annotations

from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from .data_fetcher import fetch_market_data

app = Flask(__name__)
market_data = []


def update_data() -> None:
    """Refresh the global market data."""
    global market_data
    market_data = fetch_market_data()


scheduler = BackgroundScheduler(timezone=pytz.timezone("US/Eastern"))
scheduler.add_job(update_data, CronTrigger(hour=18, minute=0))
scheduler.start()

# Initial population
update_data()


@app.route("/")
def dashboard():
    """Render the dashboard table."""
    return render_template("dashboard.html", data=market_data)


if __name__ == "__main__":
    app.run(debug=True)
