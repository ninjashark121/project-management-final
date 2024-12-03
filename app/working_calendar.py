from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for form handling

# In-memory storage for events
events = []

@app.route('/working-calendar', methods=['GET', 'POST'])
def working_calendar():
    global events

    # Handle form submission to add a new event
    if request.method == 'POST':
        event_date = request.form.get('event_date')
        event_title = request.form.get('event_title')
        if event_date and event_title:
            events.append({'date': event_date, 'title': event_title})
        return redirect(url_for('working_calendar'))  # Redirect to avoid resubmission issues

    # Generate the calendar for the current month
    today = datetime.today()
    cal = calendar.HTMLCalendar().formatmonth(today.year, today.month)

    # Highlight days with events
    for event in events:
        event_day = int(event['date'].split('-')[2])
        cal = cal.replace(f'>{event_day}<', f' class="event-day">{event_day}<')

    return render_template('working_calendar.html', calendar=cal, events=events)



if __name__ == '__main__':
    app.run(debug=True)
