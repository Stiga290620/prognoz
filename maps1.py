import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server=app.server

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("dead-infected-12.csv")

#df = df.groupby(['Country'])[['Data']].mean()
#df.reset_index(inplace=True)
#print(df[:10])

#d1 = dict.fromkeys(['label', 'value'],df[1])

# data = open('dead-infected-11.csv').readline().strip().split(',')[1:]
# options1=[]
# for i in data:
#     options1.append({'"label"':'"'+i+'"','"value"':i})

# data = open('dead-infected-1.csv').readline().strip().split(',')[1:]
# options1=[]
# for i in data:
#     options1.append({"label":i,"value":i})
#
# ss = str(options1)[1:-1]
# print(ss)

#available_indicators = open('dead-infected-12.csv').readline().strip().split(',')[2:]
#d1 = [{'label': i, 'value': i} for i in available_indicators]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("ОТНОШЕНИЕ смертельных случаев COVID-19 к выявленным, %", style={'text-align': 'center'}),

    # dcc.Dropdown(id="slct_year",
    #              options=[
    #                  {"label": "01.08.20", "value": 010820},
    #                  {"label": "02.08.20", "value": 020820},
    #                  {"label": "03.08.20", "value": 030820},
    #                  {"label": "04.08.20", "value": 040820}],
    #              multi=False,
    #              value=2015,
    #              style={'width': "40%"}
    #              ),
    dcc.Dropdown(id="slct_year",
    #             options=[{'label': i, 'value': i} for i in available_indicators],
                 options=[{'label': i, 'value': i} for i in  df.columns[2:]],
                 multi=False,
                 value='18.03.20',
                 style={'width': "40%"}
                 ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The data chosen by user was: {}".format(option_slctd)

    # dff = df.copy()
    if (option_slctd!=None):
        dff = df[option_slctd]
        ss=option_slctd
    else:
        dff = df['18.03.20']
        ss='18.03.20'

    print(option_slctd)
    # dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    # fig = px.choropleth(
    #     df.columns[2:],
    #     data_frame=df.columns[2:],
    # #    locationmode='USA-states',
    #     locations=df['Code'],
    # #    scope="usa",
    # #    color='Pct of Colonies Impacted',
    # #    hover_data=df,
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
    #     animation_frame=df.columns[2:], #Data for animation, time-series data
    #     template='plotly_dark'
    # )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=df['Country'],
    #         z=df[c].astype(float),
    #         colorscale='Reds',
    #     )]
    # )

    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    fig = go.Figure(data=go.Choropleth(
        locations = df['Code'],
        z = dff,
        text = df['Country'],
        colorscale = 'Reds',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '%',

#        colorbar_title = 'GDP<br>Billions US$',
    ))

    fig.update_layout(
        title_text=ss,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='',
            #text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            #   CIA World Factbook</a>',
            showarrow = False
        )]
    )


    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

