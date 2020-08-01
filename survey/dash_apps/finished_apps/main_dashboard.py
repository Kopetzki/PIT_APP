import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from django.db.models import Count
from survey.models import Observation, Observation_Individual, Survey, Survey_Individual, Survey_IndividualExtra
from django.contrib.auth.models import User
import plotly.graph_objs as go
from itertools import chain
import dash_table
import pandas as pd
import dash

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('main_dash', external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

#colors in order Teal, Lavendar, Chartreuse, Cyan, Light Blue, Purple, Meadow Green, Amber
colors = ["#6CD6C3", "#DDCAF5", "#D0E46B", "#6ED2E6", "#6BB4D5", "#6B7FD5", "#6BD58D", "#D5C26B"]

config = {'displayModeBar': False}


#defines the column data properties
def column_properties(data):
    columns = []
    if data == 1:
        columns = [
            {'name': 'ID', 'id': 'id', 'type': 'numeric'},
            {'name': 'Reason', 'id': 'obs_reason', 'type': 'numeric'},
            {'name': 'Adults', 'id': 'obs_adults', 'type': 'numeric'},
            {'name': 'Children', 'id': 'obs_children', 'type': 'numeric'},
            {'name': 'Unsure', 'id': 'obs_unsure', 'type': 'numeric'},
            {'name': 'Household Total', 'id': 'obs_householdnum', 'type': 'numeric'},
            {'name': 'Time Observed', 'id': 'obs_time', 'type': 'datetime'},
            {'name': 'User ID', 'id': 'obs_user_id', 'type': 'numeric'},
        ]
    if data == 2:
        columns = [
            {'name': 'ID', 'id': 'id', 'type': 'numeric'},
            {'name': 'Location', 'id': 'client_location', 'type': 'text'},
            {'name': 'Homeless', 'id': 'client_homeless_id', 'type': 'numeric'},
            {'name': 'Age', 'id': 'client_age_id', 'type': 'numeric'},
            {'name': 'Gender', 'id': 'client_gender_id', 'type': 'numeric'},
            {'name': 'Ethnicity', 'id': 'client_ethnicity_id', 'type': 'numeric'},
            {'name': 'Extra Information', 'id': 'client_information', 'type': 'text'},
            {'name': 'User ID', 'id': 'c_obs_user_id', 'type': 'numeric'},
        ]
    if data == 3:
        columns = [
            {'name': 'ID', 'id': 'id', 'type': 'numeric'},
            {'name': 'Last Night', 'id': 'survey_lastnight_id', 'type': 'numeric'},
            {'name': 'Repeat Survey', 'id': 'survey_repeat', 'type': 'numeric'},
            {'name': 'Adults', 'id': 'survey_adults', 'type': 'numeric'},
            {'name': 'Children', 'id': 'survey_children', 'type': 'numeric'},
            {'name': 'Household Total', 'id': 'survey_householdnum', 'type': 'numeric'},
            {'name': 'User ID', 'id': 'survey_user_id', 'type': 'numeric'},
        ]
    if data == 4:
        columns = [
            {'name': 'ID', 'id': 'id', 'type': 'numeric'},
            {'name': 'Initials', 'id': 'client_survey_initials', 'type': 'text'},
            {'name': 'HoH Relationship', 'id': 'client_survey_relationship_id', 'type': 'numeric'},
            {'name': 'HoH Confirm', 'id': 'client_survey_hhconfirm', 'type': 'numeric'},
            {'name': 'Last Night Stay', 'id': 'client_survey_nonhhlastnight', 'type': 'text'},
            {'name': 'Exact Age', 'id': 'client_survey_age_exact', 'type': 'numeric'},
            {'name': 'Age Group', 'id': 'client_survey_age_grouped_id', 'type': 'numeric'},
            {'name': 'Ethnicity', 'id': 'client_survey_ethnicity', 'type': 'numeric'},
            {'name': 'Race Other', 'id': 'client_survey_race_other', 'type': 'text'},
            {'name': 'Gender', 'id': 'client_survey_gender_id', 'type': 'numeric'},
            {'name': 'Veteran', 'id': 'client_survey_served', 'type': 'numeric'},
            {'name': 'Guard/Reserve', 'id': 'client_survey_served_guard_res', 'type': 'numeric'},
            {'name': 'VHA Benefits', 'id': 'client_survey_served_VHA', 'type': 'numeric'},
            {'name': 'SSI/SSDI', 'id': 'client_survey_benefits', 'type': 'numeric'},
            {'name': 'First Time', 'id': 'client_surey_firsttime', 'type': 'numeric'},
            {'name': 'Homeless Length', 'id': 'client_survey_homelesslength_id', 'type': 'numeric'},
            {'name': 'Homeless Length Number', 'id': 'client_survey_homelesslength_number', 'type': 'numeric'},
            {'name': 'Times Homeless', 'id': 'client_survey_timeshomeless_id', 'type': 'numeric'},
            {'name': 'Times Homeless Type', 'id': 'client_survey_timeshomeless_length_id', 'type': 'numeric'},
            {'name': 'Times Homeless Num', 'id': 'client_survey_timeshomeless_number', 'type': 'numeric'},
            {'name': 'ExtraID', 'id': 'client_survey_over18_id', 'type': 'numeric'},
            {'name': 'User ID', 'id': 's_obs_user_id', 'type': 'numeric'},
        ]
    return columns


def pop_count_graph(obs_inds , inds, sur_inds_sur, inds_sur):
    #graph that counts households + individuals
    xaxis = ['Groups', 'Individuals']

    trace1 = go.Bar(
        x = xaxis,
        y = [obs_inds.count(), inds.count()],
        name = 'Observed',
        marker = dict(
            color = ["#6CD6C3", "#6CD6C3"]
        )
    )
    trace2 = go.Bar(
        x=xaxis,
        y=[sur_inds_sur.count(), inds_sur.count()],
        name = 'Surveyed',
        marker=dict(
            color=["#DDCAF5", "#DDCAF5"]
        )
    )

    data = [trace1, trace2]

    layout = go.Layout(
        title = 'Observed Households and Individuals',
        title_x = 0.5,
        font = dict(
                size = 12,
                family = 'sans-serif'
                ),
        barmode = 'stack',
        xaxis = dict(tickvals=['Groups', 'Individuals']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis = go.YAxis(
            showticklabels=False
        )
    )

    figure = go.Figure(data=data, layout=layout)

    return figure

def age_graph(inds, inds_sur):
    #simple pie chart for age groups
    age_lookup = {
      1: "Under 18",
      2: "18 - 24",
      3: "25+",
      4: "Not Sure"
    }

    data_group = inds.values('client_age').annotate(dcount=Count('client_age'))
    data_group_sur = inds_sur.values('client_survey_age_grouped').annotate(dcount=Count('client_survey_age_grouped'))
    #uses itertools function to combine the two query sets
    combined_data = chain(data_group, data_group_sur)
    data_values = []
    data_annotations = []
    #goes through query sets and matches it with the proper annotation for graph display
    for x in combined_data:
      data_values.append(list(x.values())[1])
      y = list(x.values())[0]
      data_annotations.append(age_lookup[y])
    figure = {
      "data": [
        {
          "values": data_values,
          "labels": data_annotations,
          "textposition":"inside",
          "name": 'Age',
          "hoverinfo":"label+value",
          "hole": .5,
          "type": "pie",
          "marker": {"colors": colors},
        }],
        "layout": {
          "title":"Age Groups",
          "font" : dict(
            size = 12,
            family = 'sans-serif'
          ),
        }
      }
    return figure

def gender_graph(inds, inds_sur):
    #simple gender breakdown
    gender_lookup = {
      1: "Male",
      2: "Female",
      3: "Not Sure",
    }

    gender_detailed_lookup = {
        1:"Male",
        2: "Female",
        3: "Transgender",
        4: "Gender Non-Conforming(i.e., not exclusively male or female)",
        5: "Not Sure"
    }

    data_group = inds.values('client_gender').annotate(dcount=Count('client_gender'))
    data_group_sur = inds_sur.values('client_survey_gender').annotate(dcount=Count('client_survey_gender'))
    data_values = []
    data_annotations = []
    # goes through query sets and matches it with the proper annotation for graph display
    # can't combine with itertools since they have different values, have to be looked up separately
    for x in data_group:
      data_values.append(list(x.values())[1])
      y = list(x.values())[0]
      data_annotations.append(gender_lookup[y])
    for x in data_group_sur:
      data_values.append(list(x.values())[1])
      y = list(x.values())[0]
      data_annotations.append(gender_detailed_lookup[y])
    figure = {
      "data": [
        {
          "values": data_values,
          "labels": data_annotations,
          "textposition":"inside",
          "name": 'Gender',
          "hoverinfo":"label+value",
          "hole": .5,
          "type": "pie",
          "marker": {"colors": colors}
        }],
      "layout": {
        "title":"Gender Groups",
        "font" : dict(
          size = 12,
          family = 'sans-serif'
        ),
      }
    }
    return figure

def race_graph(inds, inds_sur):
    #pie chart for race
    race_lookup = {
        1: "American Indian or Alaska Native",
        2: "Asian",
        3: "Black or African American",
        4: "Native Hawaiian or Other Pacific Islander",
        5: "White",
        6: "Other",
        7: "Not Sure"
         }

    data_group = inds.values('client_race').annotate(dcount=Count('client_race'))
    data_group_sur = inds_sur.values('client_survey_race').annotate(dcount=Count('client_survey_race'))
    #uses itertools function to combine the two query sets
    combined_data = chain(data_group, data_group_sur)
    data_values = []
    data_annotations = []
    for x in combined_data:
        data_values.append(list(x.values())[1])
        y = list(x.values())[0]
        data_annotations.append(race_lookup[y])
    figure = {
      "data": [
        {
          "values": data_values,
          "labels": data_annotations,
          "textposition":"inside",
          "name": 'Race',
          "hoverinfo":"label+value",
          "hole": .5,
          "type": "pie",
          "marker": {"colors": colors}
        }],
      "layout": {
            "title":"Race",
            "font" : dict(
                        size = 12,
                        family = 'sans-serif'
                    ),
        }
    }
    return figure

def sub_populations(inds, inds_sur, inds_sur_ex):
    try:
        vets = inds_sur.filter(client_survey_served=1).values('client_survey_served').annotate(dcount=Count('client_survey_served'))[0]['dcount']
    except IndexError:
        vets = 0
    try:
        ethnicity = inds_sur.filter(client_survey_ethnicity=1).values(
                'client_survey_ethnicity').annotate(dcount=Count(
                'client_survey_ethnicity'))[0]['dcount'] +inds.filter(
                 client_ethnicity=1).values('client_ethnicity').annotate(
                dcount=Count('client_ethnicity'))[0]['dcount']
    except IndexError:
        ethnicity = 0
    try:
        first_time = inds_sur.filter(client_surey_firsttime=1).values('client_surey_firsttime').annotate(dcount=Count('client_surey_firsttime'))[0]['dcount']
    except IndexError:
        first_time = 0
    try:
        dv_victim = inds_sur_ex.filter(client_survey_DV=1).values('client_survey_DV').annotate(dcount=Count('client_survey_DV'))[0]['dcount']
    except IndexError:
        dv_victim = 0
    try:
        hiv = inds_sur_ex.filter(client_survey_HIVAIDS=1).values('client_survey_HIVAIDS').annotate(dcount=Count('client_survey_HIVAIDS'))[0]['dcount']
    except IndexError:
        hiv = 0

    values = [vets, ethnicity, first_time, dv_victim, hiv]
    annotations = ["Veterans", "Hispanic", "First Time Homeless", "Homeless due to Domestic Violence", "HIV/AIDS"]

    trace1 = go.Bar(
        x = annotations,
        y = values,
        name = 'Sub-Population',
        marker = dict(
            color = colors
        )
    )
    layout = go.Layout(
                font = dict(
                        size = 12,
                        family = 'sans-serif'
                    ),
                title='Sub-Population Categories',
                title_x=0.5,
                yaxis = dict(
                showticklabels=False
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

    data = [trace1]
    figure = go.Figure(data=data, layout=layout)
    return figure

def barriers(inds_sur_ex):
    barriers_lookup = {
        0:  "Alcohol use/Illegal drug use",
        1 : "Psychiatric/emotional condition",
        2 : "Physical disability",
        3 : "Don't Know/Refused'"
    }
    data_values = []
    data_annotations = []
    data_group = inds_sur_ex.values('client_survey_barriers').annotate(dcount=Count('client_survey_barriers'))
    for x in data_group:
      data_values.append(list(x.values())[1])
      y = list(x.values())[0]
      data_annotations.append(barriers_lookup[y])

    figure = {
      "data": [
        {
          "values": data_values,
          "labels": data_annotations,
          "textposition":"inside",
          "name": 'Barriers',
          "hoverinfo":"label+value",
          "hole": .5,
          "type": "pie",
          "marker": {"colors": colors}
        }],
      "layout": {
            "title":"Barriers to Housing",
            "font" : dict(
                        size = 12,
                        family = 'sans-serif'
                    ),
        }
    }
    return figure

def last_night(sur_inds_sur):
    last_night_lookup= {
        1: "Street or sidewalk",
        2: "Vehicle (car, van, RV, truck)",
        3: "Park",
        4: "Abandoned building",
        5: "Bus, train station, airport",
        6: "Under bridge/overpass",
        7: "Woods or outdoor encampment",
        8: "Other location",
        9: "Emergency Shelter",
        10: "Transitional Housing",
        11: "Motel/Hotel",
        12: "House or apartment",
        13: "Jail, hospital, treatment program"
    }

    data_values = []
    data_annotations = []
    data_group = sur_inds_sur.values('survey_lastnight').annotate(dcount=Count('survey_lastnight'))
    for x in data_group:
      data_values.append(list(x.values())[1])
      y = list(x.values())[0]
      data_annotations.append(last_night_lookup[y])

    figure = {
      "data": [
        {
          "values": data_values,
          "labels": data_annotations,
          "textposition":"inside",
          "name": 'Last Night Stay',
          "hoverinfo":"label+value",
          "hole": .5,
          "type": "pie",
          "marker": {"colors": colors}
        }],
      "layout": {
            "title":"Where did People Sleep Last Night?",
            "font" : dict(
                        size = 12,
                        family = 'sans-serif'
                    ),
        }
    }
    return figure

def main_dashboard(obs_inds , inds, sur_inds_sur, inds_sur, inds_sur_ex):
    return html.Div(children=[
        #### first row of graphs
        html.Div(children=[
            html.Div([dcc.Graph(
                id='groups-individuals',
                figure=pop_count_graph(obs_inds, inds,sur_inds_sur, inds_sur),
                config=config
            )],
                style={'display': 'inline-block', 'width': '49%'}),

            html.Div([dcc.Graph(
                id='age-groups',
                figure=age_graph(inds, inds_sur),
                config=config)
            ], style={'display': 'inline-block', 'width': '49%'})
        ], className='row'),
        #### second row of graphs
        html.Div(children=[
            html.Div([dcc.Graph(
                id='gender-groups',
                figure=gender_graph(inds, inds_sur),
                config=config
            )],
                style={'display': 'inline-block', 'width': '49%'}),

            html.Div([dcc.Graph(
                id='race-groups',
                figure=race_graph(inds, inds_sur),
                config=config)
            ], style={'display': 'inline-block', 'width': '49%'})
        ], className='row'),
        ###### third row
        html.Div(children=[
            html.Div([dcc.Graph(
                id='sub-pop',
                figure=sub_populations(inds, inds_sur, inds_sur_ex),
                config=config)
            ], style={'display': 'inline-block', 'width': '80%', 'padding-left' : '10%', 'padding-right' : '10%'})
        ], className='row'),
    ####### row 4
        html.Div(children=[
            html.Div([dcc.Graph(
                id='barriers',
                figure=barriers(inds_sur_ex),
                config=config
            )],
                style={'display': 'inline-block', 'width': '49%'}),

            html.Div([dcc.Graph(
                id='race-groups',
                figure=last_night(sur_inds_sur),
                config=config)
            ], style={'display': 'inline-block', 'width': '49%'})
        ], className='row'),
    ])

def admin_table(users):
    df = pd.DataFrame(users.values())
    df = df.drop('password', 1)
    table = dash_table.DataTable(
        id='user_table',
        filter_action='native',
        sort_action="native",
        columns = [{"name": i, "id":i} for i in df.columns],
        data=df.to_dict('records'),
        export_format='csv',
        page_action='none',
        style_table={
            'overflowX': 'auto',
            'height': '300px',
            'overflowY': 'auto'
        }
    )
    return table

def data_table(data, columns):
    df = pd.DataFrame(data.values())
    table = dash_table.DataTable(
        id='data_table',
        #columns=[{"name": i, "id": i} for i in df.columns],
        columns = columns,
        data=df.to_dict('records'),
        export_format='csv',
        sort_action="native",
        filter_action='native',
        page_action='none',
        style_table={
            'overflowX': 'auto',
            'height': '300px',
            'overflowY': 'auto'
        }
    )
    return table

def admin_dashboard(users):
    return html.Div(children=[
        html.Div([
            html.H2("Active Users: {}".format(users.count()))
            ],className='row', style={'display': 'inline-block', 'width': '49%'}),
        html.Div([
            admin_table(users)
        ],className='row', style={'padding-bottom' : '10%'}),
    html.Div([
        dcc.Tabs(id='tabs_2', value='tab-1', children=[
            dcc.Tab(label='Observations', value='tab-1'),
            dcc.Tab(label='Observation Data', value='tab-2'),
            dcc.Tab(label='Surveys', value='tab-3'),
            dcc.Tab(label='Survey Data', value='tab-4'),
        ],className='row'),
        html.Div(id='data-dashboard')
    ])
    ])


def layout():
    survey_exists = Observation_Individual.objects.exists()
    if survey_exists:
      return html.Div([
        html.Div(id='none', children=[], style={'display': 'none'}),
        dcc.Tabs(id='tabs', value='tab-1'),
        html.Div(id='main-dashboard')
        ])
    else:
      return html.Div(
        html.H2('You must have at least one individual created to see charts.'),
        style={'text-align': 'center'})



@app.expanded_callback(
    dash.dependencies.Output('tabs','children'),
    [dash.dependencies.Input('none', 'children')]
    )
def render_hidded_tab(*args, **kwargs):
    user_is_admin = not kwargs['user'].is_staff
    return [
        dcc.Tab(label='Survey Data', value='tab-1'),
        dcc.Tab(label='Admin', value='tab-2', disabled = user_is_admin),
        ]

#tabs for main dashboard/admin dashboard
@app.expanded_callback(dash.dependencies.Output('main-dashboard', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def render_content(tab, *args, **kwargs):
    user_is_admin = kwargs['user'].is_staff
    obs_inds = Observation.objects.all()
    inds = Observation_Individual.objects.all()
    sur_inds_sur = Survey.objects.all()
    inds_sur = Survey_Individual.objects.all()
    inds_sur_ex = Survey_IndividualExtra.objects.all()
    if tab == 'tab-1':
        return main_dashboard(obs_inds , inds, sur_inds_sur, inds_sur, inds_sur_ex)
    elif tab == 'tab-2':
        if user_is_admin:
            users = User.objects.all()
            return admin_dashboard(users)
        else:
            return html.H2("You must be an Administrator to view this page")

@app.expanded_callback(dash.dependencies.Output('data-dashboard', 'children'),
              [dash.dependencies.Input('tabs_2', 'value')])
def render_data_dashboard(tab, *args, **kwargs):
    if tab == 'tab-1':
        data = Observation.objects.all()
        return data_table(data, column_properties(1))
    elif tab == 'tab-2':
        data = Observation_Individual.objects.all()
        return data_table(data, column_properties(2))
    elif tab == 'tab-3':
        data = Survey.objects.all()
        return data_table(data, column_properties(3))
    elif tab == 'tab-4':
        data = Survey_Individual.objects.all()
        return data_table(data, column_properties(4))



app.layout = layout