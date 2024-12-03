import calendar
import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File to store events
EVENTS_FILE = 'events.json'

# Load events from JSON file
def load_events():
    try:
        with open(EVENTS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save events to JSON file
def save_events():
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file)

# In-memory storage for events
events = load_events()


class EventCalendar(calendar.HTMLCalendar):
    def __init__(self, events):
        super().__init__()
        self.events = events

    def formatday(self, day, weekday, year, month):
        if day == 0:
            return '<td></td>'
        date_str = f"{year}-{month:02d}-{day:02d}"
        has_event = any(event['date'] == date_str for event in self.events)

        if has_event:
            return (
                f'<td class="event-day">'
                f'<a href="?year={year}&month={month}&date={date_str}">{day}</a>'
                f'</td>'
            )
        return f'<td>{day}</td>'

    def formatweek(self, theweek, year, month):
        return '<tr>' + ''.join(self.formatday(day, weekday, year, month) for day, weekday in theweek) + '</tr>'

    def formatmonth(self, year, month, withyear=True):
        html = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        html += f'{self.formatmonthname(year, month, withyear=withyear)}\n'
        html += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(year, month):
            html += f'{self.formatweek(week, year, month)}\n'
        html += '</table>'
        return html


# Route: Landing Page
@app.route('/')
def index():
    return render_template('index.html')


# Route: Team Member Page
@app.route('/team')
def team():
    return render_template('team.html')


# Route: Project Charter
@app.route('/project-charter')
def project_charter():
    return render_template('project_charter.html')


# Route: Work Breakdown Structure (WBS)
@app.route('/wbs')
def wbs():
    return render_template('wbs.html')


# Route: Statements of Work (SOW)
@app.route('/sow')
def sow():
    return render_template('sow.html')


# Route: Gantt Chart
@app.route('/gantt-chart')
def gantt_chart():
    return render_template('gantt.html')


# Route: Working Calendar
@app.route('/working-calendar', methods=['GET', 'POST'])
def working_calendar():
    global events

    year = request.args.get('year', default=datetime.today().year, type=int)
    month = request.args.get('month', default=datetime.today().month, type=int)
    selected_date = request.args.get('date', default=None, type=str)

    if request.method == 'POST':
        event_date = request.form.get('event_date')
        event_title = request.form.get('event_title')
        event_description = request.form.get('event_description')

        if event_date and event_title:
            events.append({'date': event_date, 'title': event_title, 'description': event_description})
            save_events()
        return redirect(url_for('working_calendar', year=year, month=month))

    cal = EventCalendar(events).formatmonth(year, month)
    events_for_date = [event for event in events if event['date'] == selected_date] if selected_date else []

    prev_month = (month - 1) or 12
    prev_year = year if month > 1 else year - 1
    next_month = (month % 12) + 1
    next_year = year if month < 12 else year + 1

    return render_template(
        'working_calendar.html',
        calendar=cal,
        events=events,
        selected_date=selected_date,
        events_for_date=events_for_date,
        year=year,
        month=month,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month
    )


# Route: Project Network Diagram
@app.route('/project-network')
def project_network():
    return render_template('project_network.html')


# Route: Critical Path Analysis
@app.route('/critical-path')
def critical_path():
    return render_template('critical_path.html')


# Route: Cost Estimates
@app.route('/cost-estimates')
def cost_estimates():
    return render_template('cost_estimates.html')


# Route: Team Building Exercises
@app.route('/team-building')
def team_building():
    return render_template('team_building.html')


# Route: Risk Management Plans
@app.route('/risk-management')
def risk_management():
    return render_template('risk_management.html')

# Route: Status and Progress Reports
@app.route('/status-reports')
def status_reports():
    return render_template('status_reports.html')



# Route: Delete Event
@app.route('/delete-event/<int:event_index>', methods=['POST'])
def delete_event(event_index):
    global events

    if 0 <= event_index < len(events):
        del events[event_index]
        save_events()

    return redirect(url_for('working_calendar'))


# Route: Edit Event
@app.route('/edit-event/<int:event_index>', methods=['GET', 'POST'])
def edit_event(event_index):
    global events

    if event_index < 0 or event_index >= len(events):
        return redirect(url_for('working_calendar'))

    event_to_edit = events[event_index]

    if request.method == 'POST':
        updated_date = request.form.get('event_date')
        updated_title = request.form.get('event_title')
        updated_description = request.form.get('event_description')

        if updated_date and updated_title:
            events[event_index] = {'date': updated_date, 'title': updated_title, 'description': updated_description}
            save_events()
        return redirect(url_for('working_calendar'))

    return render_template(
        'edit_event.html',
        event=event_to_edit,
        event_index=event_index
    )


if __name__ == '__main__':
    app.run(debug=True)
