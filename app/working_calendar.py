from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory storage for events
events = []

@app.route('/working-calendar', methods=['GET', 'POST'])
def working_calendar():
    if request.method == 'POST':
        return "POST request received!"
    return "GET request received!"


    # Generate calendar for the current month
    today = datetime.today()
    year, month = today.year, today.month
    cal = calendar.HTMLCalendar().formatmonth(year, month)

    # Highlight days with events
    for event in events:
        event_date = datetime.strptime(event['date'], "%Y-%m-%d")
        if event_date.year == year and event_date.month == month:
            event_day = event_date.day
            cal = cal.replace(f'>{event_day}<', f' class="event-day">{event_day}<')

    # Sort events by date
    sorted_events = sorted(events, key=lambda x: x['date'])

    return render_template('working_calendar.html', calendar=cal, events=sorted_events)

if __name__ == '__main__':
    app.run(debug=True)

