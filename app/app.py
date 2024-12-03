from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/project-charter')
def project_charter():
    return render_template('project_charter.html')

@app.route('/wbs')
def wbs():
    return render_template('wbs.html')

@app.route('/sow')
def sow():
    return render_template('sow.html')

@app.route('/gantt-chart')
def gantt_chart():
    return render_template('gantt.html')

@app.route('/working-calendar')
def working_calendar():
    return render_template('working_calendar.html')

@app.route('/project-network')
def project_network():
    return render_template('project_network.html')

@app.route('/critical-path')
def critical_path():
    return render_template('critical_path.html')

@app.route('/cost-estimates')
def cost_estimates():
    return render_template('cost_estimates.html')

@app.route('/team-building')
def team_building():
    return render_template('team_building.html')

@app.route('/status-reports')
def status_reports():
    return render_template('status_reports.html')

@app.route('/risk-management')
def risk_management():
    return render_template('risk_management.html')

if __name__ == '__main__':
    app.run(debug=True)
