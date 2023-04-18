import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

df = pd.DataFrame({'Category': ['A', 'B', 'C', 'D'],
                   'Value': [10, 20, 15, 5]})

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1('My First Dash App'),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': category, 'value': category} for category in df['Category']],
            value=None,
            placeholder='Select a category'
        ),
        dcc.Graph(
            id='bar-chart',
            figure=px.bar(df, x='Category', y='Value')
        )
    ]
)


# Define callback for updating the bar chart based on the category filter
@app.callback(
    dependencies.Output('bar-chart', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = df
    else:
        # Filter the df based on selection
        filtered_df = df[df['Category'] == category]

    return px.bar(filtered_df, x='Category', y='Value')


if __name__ == '__main__':
    app.run_server(debug=True)


"""

import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc

app = Dash(__name__)

df = pd.DataFrame({'City': ['Paris', 'New York', 'Los Angeles', 'Tokyo'],
                   'Lat': [48.8566, 40.7128, 34.0522, 35.6895],
                   'Lon': [2.3522, -74.0060, -118.2437, 139.6917],
                   'Value': [10, 20, 15, 5]})

app.layout = html.Div(children=[
    html.H1("My first map", style={'color': '#ADD8E6'}),
    dcc.Graph(id="map-graph", figure=px.scatter_mapbox(
        df,
        lat='Lat',
        lon='Lon',
        hover_name='City',
        zoom=1
    ).update_layout(mapbox_style='open-street-map'))
])

if __name__ == '__main__':
    app.run_server(debug=True)
"""