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
min_value = spacex_df["Payload Mass (kg)"].min()
max_value = spacex_df["Payload Mass (kg)"].max()
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                        options=[
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'All Sites', 'value': 'ALL'},
                                        ],
                                        value='ALL',
                                        placeholder="Select Launch Site",
                                        searchable=True
                                        ),
                                       
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        100: '100'},
                                    value=[min_value, max_value]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success rate by Launch Site')
        return fig
    elif entered_site == 'KSC LC-39A':
        filtered_df11 = spacex_df[spacex_df["Launch Site"]=="KSC LC-39A"]
        labels = filtered_df11['class'].value_counts().index
        values = filtered_df11['class'].value_counts().values
        print(filtered_df11)
        fig = px.pie( values=values, names=labels, 
        title='Success rate by Launch Site')
        return fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df22 = spacex_df[spacex_df["Launch Site"]=="CCAFS LC-40"]
        print(filtered_df22)
        labels = filtered_df22['class'].value_counts().index
        values = filtered_df22['class'].value_counts().values

        fig = px.pie( values=values, names=labels, 
        title='Success rate by Launch Site')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        filtered_df33 = spacex_df[spacex_df["Launch Site"]=="VAFB SLC-4E"]
        print(filtered_df33)
        labels = filtered_df33['class'].value_counts().index
        values = filtered_df33['class'].value_counts().values
        fig = px.pie( values=values, names=labels, 
        title='Success rate by Launch Site')
        return fig
       
# TASK 4:


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_mass):
    print(payload_mass)
    spacex_df2 = spacex_df[(spacex_df["Payload Mass (kg)"]>=payload_mass[0]) & (spacex_df["Payload Mass (kg)"]<=payload_mass[1])]
    if entered_site == 'ALL':
        filtered_df = spacex_df2
        fig = px.scatter(x = filtered_df["Payload Mass (kg)"], y=filtered_df["class"])
        fig.update_layout(title='Payload Mass (kg) vs Class', xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        return fig
    elif entered_site == 'KSC LC-39A':
        filtered_df = spacex_df2[spacex_df2["Launch Site"]=="KSC LC-39A"]
        fig = px.scatter(x = filtered_df["Payload Mass (kg)"], y='class')
        fig.update_layout(title='Payload Mass (kg) vs Class', xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        return fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df = spacex_df2[spacex_df2["Launch Site"]=="CCAFS LC-40"]
        fig = px.scatter(x = filtered_df["Payload Mass (kg)"], y=filtered_df["class"])
        fig.update_layout(title='Payload Mass (kg) vs Class', xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        filtered_df = spacex_df2[spacex_df2["Launch Site"]=="VAFB SLC-4E"]
        fig = px.scatter(x = filtered_df["Payload Mass (kg)"], y=filtered_df["class"])
        fig.update_layout(title='Payload Mass (kg) vs Class', xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        return fig
    

# Run the app
if __name__ == '__main__':
    app.run_server()
