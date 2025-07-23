import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pymongo import MongoClient
from datetime import datetime


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["github_tracker"]
collection = db["repo_data"]

# Get unique usernames
all_data = list(collection.find({}))
usernames = sorted(list(set([repo["username"] for repo in all_data])))

# Init Dash app
app = dash.Dash(__name__)
app.title = "GitHub Repo Tracker"

app.layout = html.Div([
    html.H1("GitHub Repository Tracker Dashboard", style={"textAlign": "center"}),
    html.Div([
        html.Label("Select GitHub Username:"),
        dcc.Dropdown(
            id='username-dropdown',
            options=[{"label": user, "value": user} for user in usernames],
            value=usernames[0]
        )
    ], style={"width": "50%", "margin": "auto"}),

    dcc.Graph(id='repo-bar-chart'),
    dcc.Graph(id='stars-vs-forks-pie'),
    html.Div(id='last-updated', style={"textAlign": "center", "marginTop": 20})
])

@app.callback(
    [Output('repo-bar-chart', 'figure'),
     Output('stars-vs-forks-pie', 'figure'),
     Output('last-updated', 'children')],
    [Input('username-dropdown', 'value')]
)
def update_dashboard(selected_user):
    data = list(collection.find({"username": selected_user}))
    repo_names = [d["repo_name"] for d in data]
    stars = [d["stars"] for d in data]
    forks = [d["forks"] for d in data]

    last_updated = data[0]["last_updated"] if data else "N/A"
    formatted_time = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")

    bar_chart = {
        'data': [
            go.Bar(name='Stars', x=repo_names, y=stars, marker_color='gold'),
            go.Bar(name='Forks', x=repo_names, y=forks, marker_color='lightblue')
        ],
        'layout': go.Layout(title=f"Repo Activity for {selected_user}", barmode='group')
    }

    pie_chart = {
        'data': [go.Pie(
            labels=['Stars', 'Forks'],
            values=[sum(stars), sum(forks)],
            marker=dict(colors=['gold', 'lightblue'])
        )],
        'layout': go.Layout(title='Total Stars vs Forks')
    }

    return bar_chart, pie_chart, f"🕒 Last Updated: {formatted_time}"

if __name__ == '__main__':
    app.run(debug=True)
