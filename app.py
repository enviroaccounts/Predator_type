from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go

def load_predator_data():
    """Loads data about predator types."""
    data = pd.read_csv("static/data/Predator_type.csv")
    return data

def prepare_predator_chart_data(data_df):
    """Prepares data for the predator pie chart."""
    labels = data_df.iloc[:, 0].tolist()
    values = [float(str(value).strip()) for value in data_df.iloc[:, 1].tolist()]
    return labels, values



def create_predator_pie_chart(labels, values):
    """Creates a pie chart for predator data."""
    return go.Figure(data=[go.Pie(labels=labels, values=values)])

def setup_predator_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app for predator visualization."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='predator-pie-chart', figure=fig_pie_chart)
        ]),
        html.Div([  
            html.H3(id='predator-pie-chart-description', children='Types of pests being caught in traps across the catchment.')
        ])
    ], id='predator-pie-chart-layout')

def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load and prepare data
    data_df = load_predator_data()
    labels, values = prepare_predator_chart_data(data_df)

    # Create pie chart
    fig_pie_chart = create_predator_pie_chart(labels, values)

    # Setup layout
    setup_predator_layout(app, fig_pie_chart)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
