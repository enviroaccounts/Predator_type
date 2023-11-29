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
    # Calculate percentages and create custom text labels
    total = sum(values)
    percents = [(v / total * 100) for v in values]
    custom_text = [f"<1%" if 0 < p < 1 else f"{p:.0f}%" for p in percents]

    pie_chart = go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        hoverinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{percent:.0%}<br>Total: %{value}<extra></extra>',
        texttemplate=custom_text  # Use custom text labels
    )

    fig = go.Figure(data=[pie_chart])
    fig.update_layout(
        title={
            'text': "Types of pests being caught in traps across the catchment.",
            'y': 0.08,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'bottom'
        }
    )

    return fig

def setup_predator_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app for predator visualization."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='predator-pie-chart', figure=fig_pie_chart)
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
