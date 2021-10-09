import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from maps02 import m as fig001
from maps02 import txtx

app = dash.Dash(__name__)
server=app.server

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df0 = pd.read_csv("2-1.csv")



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Отношение смертельных случаев COVID-19 к выявленным, %", style={'text-align': 'center'}),
    html.Div(
        html.P(['(Динамика летальности во время пандемии COVID-19 за период c '
                + df0.Date[0]+' по '+df0.Date[len(df0.Date)-1]+')']),
        style={'text-align': 'center'},
    ),

    html.Iframe(
        '787832873783278',
        # src = 'https://cdny.de/p/x/c/f0f/7188223.jpg',
        # src = 'map0001.htm',
        srcDoc = txtx,
        width="1300", height="260",
    ),
    # html.P(['Разработал:', html.A('Юрий', href='#map0001.html')]),

    html.Div(id='input_container', children=[]),
#    html.Div(id='output_container', children=[]),
#    html.Br(),

    dcc.Graph(id='my_bee_map', figure={}),

    html.Footer([
        html.P(['Разработал:', html.A('Юрий', href='https://twitter.com/t_Yriy_w')]),
        # html.A('Юрий', href='https://twitter.com/t_Yriy_w'),
        html.P('2021 год'),
    ],
        style={'text-align': 'center'},
    ),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
     #Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure'),
    [Input(component_id='input_container', component_property='children')]
)
#
def update_graph(option_slctd):
#    container = [] #"The data chosen by user was: {}".format(option_slctd)

    # Plotly Express


    fig = px.choropleth(
       #df0[:200],
       data_frame=df0.Data,
        #   locationmode='USA-states',
       locations=df0.Code,
        #    scope="usa",
       color=df0.Data,
        #    hover_data=df,
       color_continuous_scale=px.colors.sequential.YlOrRd,
       labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
       animation_frame=df0.Date, #Data for animation, time-series data
       template='plotly_dark'
    )

    sss='Анимация для периода с '+ df0.Date[0]+' по '+df0.Date[len(df0.Date)-1]
    fig.update_layout(
        geo=dict(
        showframe=False,
        showcoastlines= False,
        projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.55,
            xref='paper',
            yref='paper',
            text='0009099ej98uhn38ou',
            showarrow = True
        )]
        )


    return  fig   #container,


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
