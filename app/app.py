from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory storage for calendar events
events = []

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Team Page
@app.route('/team')
def team():
    return render_template('team.html')

# Project Charter
@app.route('/project-charter')
def project_charter():
    return render_template('project_charter.html')

# Work Breakdown Structure (WBS)
@app.route('/wbs')
def wbs():
    return render_template('wbs.html')

# Statements of Work (SOW)
@app.route('/sow')
def sow():
    return render_template('sow.html')

# Gantt Chart
@app.route('/gantt-chart')
def gantt_chart():
    return render_template('gantt.html')

# Working Calendar
import calendar
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory storage for events
events = []

class EventCalendar(calendar.HTMLCalendar):
    def __init__(self, events):
        super().__init__()
        self.events = events

    def formatday(self, day, weekday, year, month):
        """Format a single day in the calendar."""
        if day == 0:  # Empty cells in the calendar
            return '<td></td>'
        
        # Check if the day has events
        date_str = f"{year}-{month:02d}-{day:02d}"
        has_event = any(event['date'] == date_str for event in self.events)

        if has_event:
            return (
                f'<td class="event-day">'
                f'<a href="?year={year}&month={month}&date={date_str}">{day}</a>'
                f'</td>'
            )
        else:
            return f'<td>{day}</td>'

    def formatweek(self, theweek, year, month):
        """Format a week in the calendar."""
        return '<tr>' + ''.join(self.formatday(day, weekday, year, month) for day, weekday in theweek) + '</tr>'

    def formatmonth(self, year, month, withyear=True):
        """Format a month as a table."""
        html = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        html += f'{self.formatmonthname(year, month, withyear=withyear)}\n'
        html += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(year, month):
            html += f'{self.formatweek(week, year, month)}\n'
        html += '</table>'
        return html

@app.route('/working-calendar', methods=['GET', 'POST'])
def working_calendar():
    global events

    # Get the year and month from query parameters
    year = request.args.get('year', default=datetime.today().year, type=int)
    month = request.args.get('month', default=datetime.today().month, type=int)
    selected_date = request.args.get('date', default=None, type=str)

    # Handle form submission to add a new event
    if request.method == 'POST':
        event_date = request.form.get('event_date')
        event_title = request.form.get('event_title')
        if event_date and event_title:
            events.append({'date': event_date, 'title': event_title})
        return redirect(url_for('working_calendar', year=year, month=month))  # Preserve navigation

    # Generate the calendar
    cal = EventCalendar(events).formatmonth(year, month)

    # Filter events for the selected date
    events_for_date = [event for event in events if event['date'] == selected_date] if selected_date else []

    # Calculate previous and next month
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



@app.route('/delete-event/<int:event_index>', methods=['POST'])
def delete_event(event_index):
    global events
    if 0 <= event_index < len(events):  # Ensure the index is valid
        del events[event_index]  # Remove the event from the list
    return redirect(url_for('working_calendar'))


# Project Network Diagram
@app.route('/project-network')
def project_network():
    return render_template('project_network.html')

# Critical Path Analysis
@app.route('/critical-path')
def critical_path():
    return render_template('critical_path.html')

# Cost Estimates
@app.route('/cost-estimates')
def cost_estimates():
    return render_template('cost_estimates.html')

# Team Building Exercises
@app.route('/team-building')
def team_building():
    return render_template('team_building.html')

# Status and Progress Report Templates
@app.route('/status-reports')
def status_reports():
    return render_template('status_reports.html')

# Risk Management Plans
@app.route('/risk-management')
def risk_management():
    return render_template('risk_management.html')

if __name__ == '__main__':
    app.run(debug=True)
