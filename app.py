
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies


# premier data set
df_ratp =pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
df_ratp_classe_par_Trafic1 = df_ratp.sort_values(by=['Trafic'], ascending=False).head(10)
df_ratp_classe_par_Trafic2 = df_ratp.sort_values(by=['Trafic'], ascending=False)

df_ratp_ville_trafic_eleve1 = df_ratp.groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).head(5).reset_index()
df_ratp_ville_trafic_eleve2 = df_ratp.groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).reset_index()



# deuxième data set
df_idf_mobilite = pd.read_csv('emplacement-des-gares-idf.csv', sep=";")
df_idf_mobilite_classe_par_nom = df_idf_mobilite.sort_values(by=['nom'], ascending=False)
df_idf_mobilite_classe_par_exploitant_en_fonction_des_station = df_idf_mobilite_classe_par_nom.groupby('exploitant', as_index= False)['nom_iv'].count()
df_idf_mobilite_classe_par_exploitant_en_fonction_des_station = df_idf_mobilite_classe_par_exploitant_en_fonction_des_station.sort_values('nom_iv', ascending=False)
nbr_station_par_ligne = df_idf_mobilite.groupby('ligne',as_index=False)['nom_iv'].count().sort_values('nom_iv', ascending=False)


#Pour la question 4 (Carte)
# sélectionner les lignes où la colonne 'metro' est différente de 0

df_idf_mobilite_metro = df_idf_mobilite[df_idf_mobilite['metro'] != 0]

df_idf_mobilite[['lat', 'lng']] = df_idf_mobilite_metro['Geo Point'].str.split(',', expand=True)

df_idf_mobilite['lat'] = df_idf_mobilite['lat'].str.strip().astype(float)
df_idf_mobilite['lng'] = df_idf_mobilite['lng'].str.strip().astype(float)


app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H2('Question 3'),
        dcc.Dropdown(
            id='reseau-filter-RATP',
            options=[{'label': Réseau, 'value': Réseau} for Réseau in df_ratp_classe_par_Trafic1 ['Réseau'].unique()],
            value=None,
            placeholder='Selectionner un réseau de la RATP'
        ),

        html.H2('Question 1'),
        html.Div(style={'display': 'flex'},
                 children=[
                     dcc.Graph(
                         id='Trafic annuel des entrants par stations',
                         figure=px.bar(df_ratp_classe_par_Trafic1 , x='Station', y='Trafic', title="Trafic annuel des entrants par stations")),

                     dcc.Graph(
                     id='trafic par ville',
                     figure=px.pie(df_ratp_ville_trafic_eleve1, names='Ville', values='Trafic', title='Trafic par Ville')),
             ]),

        html.H2('Question 3'),
            dcc.Dropdown(
                id='reseau-filter-IDF',
                options=[{'label': exploitant, 'value': exploitant } for exploitant in df_idf_mobilite_classe_par_exploitant_en_fonction_des_station ["exploitant"].unique()],
                value=None,
                placeholder="Selectionner un exploitant d'IDF"
            ),


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
                                       labels={'x': 'Ligne de metro ', 'y': 'nombres de stations'})),
                 ]),

        html.H2('Question 4'),

        html.Div(
                 children=[
                     dcc.Graph(id="map-graph", figure=px.scatter_mapbox(df_idf_mobilite, lat='lat', lon='lng',hover_name='nom_iv',zoom=1).update_layout(mapbox_style='open-street-map')
                     )]),

                 ])






@app.callback(
    [dependencies.Output('Trafic annuel des entrants par stations', 'figure'),
    dependencies.Output('trafic par ville', 'figure')],
    [dependencies.Input('reseau-filter-RATP', 'value'),
    dependencies.Input('reseau-filter-IDF', 'value')])

def update_graphs(selected_reseau_ratp, selected_reseau_idf):

    if selected_reseau_ratp is None:
        df_ratp_filtered = df_ratp
    else:
        df_ratp_filtered = df_ratp[df_ratp['Réseau'] == selected_reseau_ratp]


    # Mise à jour des graphiques avec les données filtrées
    fig1 = px.bar(df_ratp_filtered.sort_values(by=['Trafic'], ascending=False).head(10), x='Station', y='Trafic')
    fig2 = px.pie(df_ratp_filtered.groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).head(5).reset_index(),
                  names='Ville', values='Trafic')

    return fig1, fig2



@app.callback(
    [dependencies.Output('Nombre de station par exploitant', 'figure'),
     dependencies.Output('Nombre de station par ligne', 'figure')],
    [dependencies.Input('reseau-filter-IDF', 'value')])


def update_graphs2(selected_exploitant):
    if selected_exploitant is None:
        filtered_df = nbr_station_par_ligne
    else:
        filtered_df = df_idf_mobilite_classe_par_exploitant_en_fonction_des_station[
            df_idf_mobilite_classe_par_exploitant_en_fonction_des_station['exploitant'] == selected_exploitant]

    fig1 = px.bar(filtered_df, x='exploitant', y='nom_iv', title="Nombre de station par exploitant",
                  labels={'x': 'Exploitant', 'y': 'Nombre de station'})

    nbr_station_par_ligne_filtre = df_idf_mobilite[df_idf_mobilite['exploitant'] == selected_exploitant].groupby('ligne', as_index=False)['nom_iv'].count().sort_values('nom_iv', ascending=False)
    fig2 = px.bar(nbr_station_par_ligne_filtre, x='ligne', y='nom_iv', title='Nombre de station par ligne',
                  labels={'x': 'Ligne', 'y': 'Nombre de stations'})

    return fig1, fig2



if __name__ == '__main__':
    app.run_server( port=8050, debug=True)

