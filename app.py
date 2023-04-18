"""from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()

"""

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

# premier data set
df_ratp =pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
df_ratp_classe_par_Trafic = df_ratp.sort_values(by=['Trafic'], ascending=False).head(10)
df_ratp_ville_trafic_eleve = df_ratp.groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).head(5).reset_index()



# deuxième data set
df_idf_mobilite = pd.read_csv('emplacement-des-gares-idf.csv', sep=";")
df_idf_mobilite_classe_par_nom = df_idf_mobilite.sort_values(by=['nom'], ascending=False)
df_idf_mobilite_classe_par_exploitant_en_fonction_des_station = df_idf_mobilite_classe_par_nom.groupby('exploitant', as_index= False)['nom_iv'].count()
df_idf_mobilite_classe_par_exploitant_en_fonction_des_station = df_idf_mobilite_classe_par_exploitant_en_fonction_des_station.sort_values('nom_iv', ascending=False)
nbr_station_par_ligne = df_idf_mobilite.groupby('ligne',as_index=False)['nom_iv'].count().sort_values('nom_iv', ascending=False)






app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1('Filtre pour le réseau', style={'color': '#ADD8E6'}),
        dcc.Dropdown(
            id='reseau-filter',
            options=[{'label': station, 'value': station} for station in df_ratp_classe_par_Trafic ['Station']],
            value=None,
            placeholder='Select a category'
        ),

        html.H2('Question 1'),
        html.Div(style={'display': 'flex'},
                 children=[
                     dcc.Graph(
                         id='Trafic annuel des entrants par stations',
                         figure=px.bar(df_ratp_classe_par_Trafic , x='Station', y='Trafic', title="Trafic annuel des entrants par stations")),

                     dcc.Graph(
                         id='trafic par ville',
                         figure=px.pie(df_ratp_ville_trafic_eleve, names='Ville', values='Trafic', title='Trafic par Ville')),
                 ]),
        html.H2('Question 2'),

        html.Div(style={'display': 'flex'},
                 children=[
                     dcc.Graph(
                         id='Nombre de station par exploitant',
                         figure=px.bar(df_idf_mobilite_classe_par_exploitant_en_fonction_des_station, x='exploitant', y='nom_iv',
                                       title="Nombre de station par exploitant",
                                       labels={'x': 'Exploitant', 'y': 'Nombre de station'})),

                     dcc.Graph(
                         id='Nombre de station par ligne',
                         figure=px.bar(nbr_station_par_ligne, x='ligne', y='nom_iv',
                                       title='Nombre de station par ligne',
                                       labels={'x': 'Ligne', 'y': 'nombres de stations'})),
                 ]),
                 ])




# Define callback for updating the bar chart based on the category filter
@app.callback(
    dependencies.Output('bar-chart', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = df_ratp
    else:
        # Filter the df based on selection
        filtered_df = df_ratp[df_ratp['Rang'] == category]

    return px.bar(filtered_df, x='Rang', y='Traffic')


if __name__ == '__main__':
    app.run_server(debug=False)