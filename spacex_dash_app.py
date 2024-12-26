# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min = 0, max = 10000, step = 1000,
                                    marks = {0: '0', 5000: '5000', 10000: '10000'},
                                    value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output("success-pie-chart","figure"),
    Input("site-dropdown", "value"))

def get_pie_chart(input_site):
    if input_site == "ALL":
        df = spacex_df[spacex_df["class"] == 1]
        df = df["Launch Site"].value_counts().reset_index()
        fig = px.pie(df, values="count",
            names="Launch Site",
            title="Total Success Launches by site")
    else:
        df = spacex_df[spacex_df["Launch Site"] == input_site]
        df = df["class"].value_counts().reset_index()
        fig = px.pie(df, values="count",
            names="class",
            title=f"Total Success Launches for site {input_site}")
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")])

def get_scatter_chart(input_site, input_payload):
    df = spacex_df[spacex_df["Payload Mass (kg)"] >= input_payload[0]]
    df = df[df["Payload Mass (kg)"] <= input_payload[1]]

    if input_site != "ALL":
        df = df[spacex_df["Launch Site"] == input_site]

    fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()