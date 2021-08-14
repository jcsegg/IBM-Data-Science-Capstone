# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

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
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', 
                                             options = [
                                                       {'label': 'All Sites', 'value':'ALL_SITES'},
                                                       {'label': 'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                       {'label': 'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                       {'label': 'KSC LC-39A', 'value':'KSC LC-39A'},
                                                       {'label': 'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                       ],
                                             placeholder = 'Select a Launch Site here',
                                             searchable = True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={0: '0',
                                                       2500: '2,500',
                                                       5000: '5,000',
                                                       7500: '7,500',
                                                       10000: '10,000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def plot_the_pie_chart(selected_site):
    if selected_site == 'ALL_SITES':
        temp_df = spacex_df[spacex_df['class']==1]
        temp_df['Counts'] = temp_df.groupby(['Launch Site'])['Booster Version Category'].transform('count')
        #Attribution: https://stackoverflow.com/questions/17709270/create-column-of-value-counts-in-pandas-dataframe
        pie_fig = px.pie(temp_df, values='Counts', names='Launch Site', title='Successful launches per launch site')
    
    else:
        temp_df = spacex_df[spacex_df['Launch Site']==selected_site]
        temp_df['Counts'] = temp_df.groupby(['class'])['Booster Version Category'].transform('count')
        pie_fig = px.pie(temp_df, values='Counts', names='class', title='Launch outcomes for the selected launch site')
    return pie_fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def make_the_scatter_plot(selected_site, payload_slider):
    #Attribution: https://plotly.com/python/line-and-scatter/?utm_medium=Exinfluencer\&utm_source=Exinfluencer\&utm_content=000026UJ\&utm_term=10006555\&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2021-01-01
    low, high = payload_slider
    if selected_site == 'ALL_SITES':
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        temp_df = spacex_df[mask]
        scatter_fig = px.scatter(x=temp_df['Payload Mass (kg)'],
                                 y=temp_df['class'],
                                 color=temp_df['Booster Version Category']
                                 ,hover_data=[temp_df['Payload Mass (kg)']]
                                 )

    else:
        temp_df = spacex_df[spacex_df['Launch Site']==selected_site]
        mask = (temp_df['Payload Mass (kg)'] > low) & (temp_df['Payload Mass (kg)'] < high)
        temp_df = temp_df[mask]
        scatter_fig = px.scatter(x=temp_df['Payload Mass (kg)'],
                                 y=temp_df['class'],
                                 color=temp_df['Booster Version Category'],)
                                 #hover_data =[temp_df['Payload Mass (kg)']])
    return scatter_fig


# Run the app
if __name__ == '__main__':
    app.run_server()
