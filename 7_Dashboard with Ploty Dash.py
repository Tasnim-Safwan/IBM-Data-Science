# Import Required Packages
import pandas as pd
import plotly.express as px
from dash import dcc, Dash, html, Input, Output

# Create a dash application
app= Dash(__name__)

# Data preparation 
df= pd.read_csv('spacex_launch_geo.csv')

min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()
df['Booster Version Category'] = df['Booster Version'].str.split(' ').str[1]




app.layout= html.Div([
    html.H1("Spacex Launch Records Dash board",
            style={'textAlign': 'center', 
                   'color': '#503D36',
                    'font-size': 40}),
    
    html.Div([
          dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
                ),
          
          html.Br(),
          
          html.Div(
                dcc.Graph(id='success-pie-chart', figure={})
                ),
          
          html.Br(),
          
          html.Div([
              html.H3("Payload Mass (kg) Range:"),
              dcc.RangeSlider(id='payload-slider', 
                min=0, max=10000, step=1000,
                marks={i: str(i) for i in range(0, 10001, 1000)},
                
                value=[min_payload, max_payload]),
          
              
          ]),
          
          html.Br(),
          
          html.Div(
              dcc.Graph(id='success-payload-scatter-chart', figure={})
          )
          
    ]),

        
])

#---------------------------------------------------------------------------------------
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = df[df['class']==1]
        fig = px.pie(filtered_df, 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df= df[df['Launch Site']== entered_site] 
        fig= px.pie(filtered_df, names= 'class',
        title=f'Total Success Launches for site {entered_site}')

        return fig
#-----------------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_payload_df = df[(df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_payload_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category', 
                         title=f'Payload vs. Mission Outcome for All Sites (Payload: {low}-{high} kg)')
        fig.update_layout(
            yaxis_range=[-0.5, 1.5], 
            xaxis_title='Payload Mass (kg)', 
            yaxis_title='Mission Outcome' 
            )        
        
        return fig
    else:
        filtered_site_payload_df = filtered_payload_df[filtered_payload_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_site_payload_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category', 
                         title=f'Payload vs. Mission Outcome for {entered_site} (Payload: {low}-{high} kg)')
        return fig


if __name__ == '__main__':
    app.run()
    
    
    


