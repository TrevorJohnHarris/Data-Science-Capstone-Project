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
                                dcc.Dropdown(id='site-dropdown',options=[{'label':'CCAFS LC-40','value':'CCAFS LC-40'},{'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},{'label':'KSC LC-39A','value':'KSC LC-39A'},{'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},{'label':'ALL','value':'ALL'}],value='ALL',placeholder='Select a Launch Site here',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def update_figure1(selected_site):
    if selected_site == 'ALL':
            success = spacex_df.groupby('Launch Site')['class'].apply(lambda x: x[x == 1].count())
            failed = spacex_df.groupby('Launch Site')['class'].apply(lambda x: x[x == 0].count())
            successrate = round(success/(success + failed)*100,2)
            successrate = pd.DataFrame(successrate)
            launchsites = spacex_df['Launch Site'].unique()
            figure = px.pie(successrate,names=launchsites,values='class',title='Total Success Launches by site')
    else:
        success = spacex_df[spacex_df['Launch Site']==selected_site]['class'].sum()
        total = spacex_df[spacex_df['Launch Site']==selected_site]['class'].count()
        x1 = round(success/(total)*100,2)
        x2 = round((total-success)/(total)*100,2)
        successrate = pd.DataFrame([x2,x1],columns=[selected_site])
        figure = px.pie(successrate, values = selected_site,names=[0,1],title='Total Success Launches for '+selected_site)
        
    return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),Input('payload-slider', 'value'))
def update_figure2(selected_site,selected_payload):
    if selected_site == 'ALL':
        # making a bool series
        bool_series = spacex_df['Payload Mass (kg)'].between(selected_payload[0], selected_payload[1], inclusive = True)
        figure = px.scatter(spacex_df[bool_series], x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        newspacex_df=spacex_df[spacex_df['Launch Site']==selected_site]
        bool_series = newspacex_df['Payload Mass (kg)'].between(selected_payload[0], selected_payload[1], inclusive = True)
        figure = px.scatter(newspacex_df[bool_series], x='Payload Mass (kg)', y='class', color='Booster Version Category')

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server()
