import streamlit as st
import pandas as pd
import altair as alt
from sklearn.linear_model import LinearRegression
import numpy as np
import geopandas as gpd
import json

st.set_page_config(page_title="Einlfuss der Tonart",
                   page_icon="📈", layout='wide')

csv_file_path = 'spotify_angereichert_cleaned.csv'


df = pd.read_csv(csv_file_path)

df.drop(['Unnamed: 0'], axis=1, inplace=True)


# Streams nach Tonart
mode_streams = df.groupby('mode')['streams'].mean()

mode_song_count = df.groupby('mode').size().reset_index(name='song_count')


mode_streams_df = mode_streams.reset_index()

max_streams = mode_song_count['song_count'].max()

highlighted_line = alt.Chart(pd.DataFrame({'max_streams': [max_streams]})).mark_rule(color='red', strokeWidth=2).encode(
    y='max_streams:Q'
)


chart_mode_bar = alt.Chart(mode_song_count).mark_bar(clip=True, size=80).encode(
    x=alt.X('mode', axis=alt.Axis(title='Tonart')),
    y=alt.Y('song_count', scale=alt.Scale(domain=[250, 450]), axis=alt.Axis(
        title='Anzahl der Songs', tickCount=5, tickMinStep=50)),
    color=alt.Color('mode', legend=None, scale=alt.Scale(
        range=['#4ee2e6', '#a5ff9e'])),

    tooltip=[
        alt.Tooltip('mode', title='Tonart'),
        alt.Tooltip('song_count', title='Ø Streams')
    ]
)


final_chart = alt.layer(chart_mode_bar,  highlighted_line).properties(
    title={'text': 'Anzahl der Top-Songs nach Tonart ', 'dy': -0},
    width=550,
    height=400
).configure_title(
    fontSize=25,
    anchor='start',
    color='gray'
).configure_axis(
    labelFontSize=14,
    titleFontSize=20,
    titleColor='gray',
    labelColor='gray',
    titlePadding=12,
    grid=False
).configure_legend(
    titleFontSize=16,
    labelFontSize=14
).configure_view(
    strokeWidth=0,
).configure_axisX(
    labelAngle=0,
    titleAnchor='start'
).configure_axisY(
    grid=False,
    titleAnchor='end',
    titleFontSize=20
)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("Report ***Spotify Trend Analyse***")

st.markdown("""
Grundlegend gibt es zwei Tonarten, <span style="color: #4ee2e6;">Major(Dur)</span> und <span style="color: #a5ff9e;">Minor(Moll)</span>. Diese Tonarten haben Einfluss auf die Stimmung des Songs. Songs mit der 
            Tonart <span style="color: #4ee2e6;">Major</span> haben eine eher fröhliche und lebendige Stimmung. Songs mit der Tonart <span style="color: #a5ff9e;">Minor</span> sind dabei eher melancholisch und haben
            eine traurige Stimmung. In dem untenstehenden Chart wird die Anzahl der Top-Songs der jeweiligen Tonart gegenübergestellt. 
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    final_chart

with col2:
    st.markdown("""
                <br/>
                <br/>
    <div style="text-align: center">👍</div>
    <div>
        Wie in dem Diagramm zu sehen ist, haben die meisten Top-Songs die Tonart <span style="color: #4ee2e6;">Major</span>: <span style="color: red;">445 Songs</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('----')
    st.markdown("""
    <div style="text-align: center">👎</div>
    <div>
        Deutlich weniger Top-Songs haben die Tonart <span style="color: #4ee2e6;">Minor</span>: 351 Songs
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
:point_right: Um einen Hit zu landen, sollten sie daher die Tonart <span style="color: #4ee2e6;"> <u>Major</u></span> verwenden
""", unsafe_allow_html=True)

st.markdown("""-----""")

# Keys


key_streams = df.groupby('key')['streams'].mean()


key_streams_df = key_streams.reset_index()

max_streams_key = key_streams_df['streams'].max()

min_streams_key = key_streams_df['streams'].min()


# Erstelle das Balkendiagramm
chart_mode_bar = alt.Chart(key_streams_df).mark_bar(clip=True, size=40, opacity=0.5).encode(
    x=alt.X('key', axis=alt.Axis(title='Tonart')),
    y=alt.Y('streams', scale=alt.Scale(domain=[400000000, 650000000]), axis=alt.Axis(title='Ø Streams (Millionen)',
                                                                                     format='.0s', tickCount=5, tickMinStep=1e9, labelExpr='datum.value / 1e6')),
    color=alt.Color('key', legend=None),

    tooltip=[
        alt.Tooltip('key', title='Tonart'),
        alt.Tooltip('streams', title='Ø Streams')
    ]
)

# Erstelle eine Linie über dem größten Balken
highlighted_line_max = alt.Chart(pd.DataFrame({'max_streams': [max_streams_key]})).mark_rule(color='red', strokeWidth=2).encode(
    y='max_streams:Q'
)

highlighted_line_min = alt.Chart(pd.DataFrame({'min_streams': [min_streams_key]})).mark_rule(color='white', strokeDash=[12, 11], strokeWidth=2, opacity=0.5).encode(
    y='min_streams:Q'
)


final_chart = alt.layer(
    chart_mode_bar,  highlighted_line_max, highlighted_line_min).properties(
    title={'text': 'Ø Streams nach Key ', 'dy': -0},
    width=550,
    height=400
).configure_title(
    fontSize=25,
    anchor='start',
    color='gray'
).configure_axis(
    labelFontSize=14,
    titleFontSize=20,
    titleColor='gray',
    labelColor='gray',
    titlePadding=12,
    grid=False
).configure_legend(
    titleFontSize=16,
    labelFontSize=14
).configure_view(
    strokeWidth=0,
).configure_axisX(
    labelAngle=0,
    titleAnchor='start'
).configure_axisY(
    grid=False,
    titleAnchor='end',
    titleFontSize=20
)


st.markdown("""
Aber auch der Key eines Songs hat einen Einfluss auf die Popularität. Keys
             sind die musikalischen Bausteine, die bestimmen, wie die Musik klingt und sich anhört.
            In dem untenstehenden Diagramm ist die durchschnittliche Anzahl der Spotify-Streams nach dem Key des Songs zu sehen.
 """)

col1, col2 = st.columns([3, 2])

with col1:
    final_chart

with col2:
    st.markdown("""
                <br/>
                <br/>
    <div style="text-align: center">👍</div>
    <div>
        Wie in dem Barplot zu sehen ist, haben Songs mit dem Key <span style="color: red;">C#</span> die meisten Streams: ca. <span style="color: red;">610</span>
                Millionen Streams
    </div>
    """, unsafe_allow_html=True)
    st.markdown('----')
    st.markdown("""
    <div style="text-align: center">👎</div>
    <div>
        Deutlich weniger Streams haben Songs mit dem Key <span style="color: #4ee2e6;">A</span>: ca. 415 Millionen Streams
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
:point_right: Für einen Kassenschlager sollte ihr Song den Key :red[C#] haben

""")

st.markdown("----")


# Release Month

monthly_releases = df.groupby(
    'released_month').size().reset_index(name='count')

month_labels = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

monthly_releases['released_month'] = monthly_releases['released_month'].map(
    month_labels)


def base_chart(df):
    chart = alt.Chart(df).mark_line(strokeWidth=3).encode(
        x=alt.X('released_month', axis=alt.Axis(title='Monat',
                                                labelFontSize=14), sort=list(month_labels.values())),
        y=alt.Y('count', scale=alt.Scale(domain=(30, 120)), axis=alt.Axis(
                title='Veröffentlichungen', titleFontSize=20, labelFontSize=14,)),
        tooltip=['released_month', 'count']
    )
    return chart


data_januar = pd.DataFrame({'count': [112], 'released_month': ['Jan']})
data_may = pd.DataFrame({'count': [112], 'released_month': ['May']})
data_Aug = pd.DataFrame({'count': [39], 'released_month': ['Aug']})

max_points = monthly_releases[monthly_releases['count']
                              == monthly_releases['count'].max()]
min_points = monthly_releases[monthly_releases['count']
                              == monthly_releases['count'].min()]

min_points_chart = base_chart(min_points).mark_point(
    size=100, color='white', opacity=0.8,  filled=True)
max_points_chart = base_chart(max_points).mark_point(
    size=100, color='red', opacity=0.8, filled=True)
min_points_chart_line = alt.Chart(data_Aug).mark_rule(strokeDash=[12, 6], size=1, color='white', fontSize=12, opacity=1).encode(
    y='count',
    x=alt.X('released_month', sort=list(month_labels.values())),
)
max_points_chart_line_jan = alt.Chart(data_januar).mark_rule(strokeDash=[12, 6], size=1, color='red', fontSize=12, opacity=0.8).encode(
    y='count',
    x=alt.X('released_month', sort=list(month_labels.values())),
)
max_points_chart_line_may = alt.Chart(data_may).mark_rule(strokeDash=[12, 6], size=1, color='red', fontSize=12, opacity=0.8).encode(
    y='count',
    x=alt.X('released_month', sort=list(month_labels.values())),
)


final_chart = alt.layer(
    max_points_chart_line_jan,
    base_chart(monthly_releases),  # Basisliniendiagramm
    max_points_chart_line_may,     # Gestrichelte Linien und Punkte für Mai-Maximum
    min_points_chart,              # Minimumpunkte
    max_points_chart,              # Maximumpunkte
    min_points_chart_line          # Gestrichelte Linien für Minimumpunkte
).properties(
    title={'text': 'Anzahl der Songveröffentlichungen pro Monat', 'dy': -0},
    width=550,
    height=400
).configure_title(
    fontSize=25,
    anchor='start',
    color="gray"
).configure_axis(
    labelFontSize=14,
    titleFontSize=20,
    titleColor='gray',
    labelColor='gray',
    titlePadding=12
).configure_legend(
    titleFontSize=16,
    labelFontSize=14
).configure_view(
    strokeWidth=0,
).configure_axisX(
    labelAngle=0,
    titleAnchor='start'
).configure_axisY(
    grid=False,
    titleAnchor='end',
    titleFontSize=20
)


st.markdown("""
Wann sollten sie ihren Song releasen? Der Releasezeitpunkt hat einen großen Einfluss auf die Popularität eines Songs.
Im untenstehenden Diagramm sind die Anzahl der releasten Top-Songs pro Monat dargestellt. 
            Über das Jahr 2023 hinweg waren deutliche Schwankungen zu sehen.
""")

col1, col2 = st.columns([3, 2])

with col1:
    final_chart

with col2:
    st.markdown("""
                <br/>
                <br/>
    <div style="text-align: center">👍</div>
    <div>
        Wie in dem Line-Chart zu sehen ist, wurden die meisten Top-Songs in den Monaten <span style="color: red;">Janaur </span> und  <span style="color: red;">Mai </span> released
    </div>
    """, unsafe_allow_html=True)
    st.markdown('----')
    st.markdown("""
    <div style="text-align: center">👎</div>
    <div>
        Die wenigsten Top-Songs wurden im August released    </div>
    """, unsafe_allow_html=True)


st.markdown("""
:point_right: Releasen sie ihren Song im :red[Januar] oder im :red[Mai]!

""")

st.markdown("----")

# Speechiness


song_count_df = df.groupby(
    'speechiness_%').size().reset_index(name='song_count')
# Filtern des DataFrames auf speechiness-Werte von 40 oder weniger
filtered_song_count_df = song_count_df[song_count_df['speechiness_%'] <= 40]

# Verwenden des gefilterten DataFrames für die Regression
X_filtered = filtered_song_count_df['speechiness_%'].values.reshape(-1, 1)
y_filtered = filtered_song_count_df['song_count'].values
reg_filtered = LinearRegression().fit(X_filtered, y_filtered)

# Erstellen einer DataFrame für die Regressionslinie mit dem gefilterten Bereich
regression_df_filtered = pd.DataFrame({'speechiness_%': np.linspace(
    filtered_song_count_df['speechiness_%'].min(), filtered_song_count_df['speechiness_%'].max(), 100)})
regression_df_filtered['song_count_predicted'] = np.clip(
    reg_filtered.predict(regression_df_filtered[['speechiness_%']]), 0, None)

# Erstellen der Regressionslinie mit dem gefilterten DataFrame
regression_line_filtered = alt.Chart(regression_df_filtered).mark_line(color='red', size=1).encode(
    x=alt.X('speechiness_%'),
    y=alt.Y('song_count_predicted')
)


scatter_plot_filtered_with_reg_line = alt.Chart(filtered_song_count_df).mark_circle(opacity=0.5).encode(
    x=alt.X('speechiness_%', axis=alt.Axis(
        title='Speechiness %', tickCount=10, tickMinStep=5)),
    y=alt.Y('song_count', axis=alt.Axis(
        title='Anzahl der Songs', tickCount=10, tickMinStep=20)),
    size=alt.Size('song_count', scale=alt.Scale(
        range=[10, 1000]), legend=None),
    color=alt.Color('song_count', scale=alt.Scale(
        scheme='viridis')),
    tooltip=['speechiness_%', 'song_count']
)

# Kombinieren der Scatterplot- und Regressionslinie mit dem gefilterten DataFrame
combined_chart_filtered = alt.layer(scatter_plot_filtered_with_reg_line + regression_line_filtered).properties(
    title={'text': 'Beziehung zwischen Speechiness und Streams', 'dy': -0},

    width=550,
    height=400
).configure_title(
    fontSize=25,
    anchor='start',
    color="gray"
).configure_axis(
    labelFontSize=14,
    titleFontSize=20,
    titleColor="gray",
    labelColor="gray",
    titlePadding=12,
    grid=False
).configure_view(
    strokeWidth=0,
).configure_axisX(
    labelAngle=0,
    titleAnchor='start'
).configure_axisY(
    grid=False,
    titleAnchor='end'
)


st.markdown("""

Um wieder zurück zu den musikalischen Merkmalen mit Einfluss auf die Popularität eines Songs zu kommen, schauen wir uns
die Speechiness der Top-Songs im Jahr 2023 an. Die Speechiness, auf deutsch Sprechanteil, ist der Anteil der gesprochenen Worte
            in einem Song. Rap hat zum Beispiel, in den meisten Fällen einen sehr hohen Sprechanteil. In folgendem Scatter-Plot ist
            die Anzahl der Top-Songs im Jahre 2023 mit dem jeweiligen Sprechanteil dargestellt.
                   
            """)


col1, col2 = st.columns([3, 2])

with col1:
    combined_chart_filtered
with col2:
    st.markdown("""
                <br/>
                <br/>
    <div style="text-align: center">👍</div>
    <div>
        Wie in dem Scatter-Plot zu sehen, haben die meisten Top-Songs einen sehr geringen Sprechanteil, im Bereich von ca. <span style="color: red;">3-8 %</span>.
                 Die Anzahl der Songs nimmt mit zunehmendem Sprechanteil ab.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('----')
    st.markdown("""
    <div style="text-align: center">👎</div>
    <div>
        Die wenigsten Top-Songs haben einen Sprechanteil von über 10%   </div>
    """, unsafe_allow_html=True)


st.markdown("""
:point_right: Ihr Song sollte einen :red[geringen] Sprechanteil aufweisen! Achten sie auf Gesang und Melodie. 

""")


st.markdown("---")
# Energy


energy_grouped = df.groupby(pd.cut(df['energy_%'], range(
    0, 101, 10))).size().reset_index(name='average_song_count')

# Umbenennung der Spalte für die Energiebereiche
energy_grouped.columns = ['energy_range', 'average_song_count']

energy_grouped['energy_range'] = energy_grouped['energy_range'].apply(
    lambda x: f"{x.left}-{x.right}")


energy_grouped_line_chart = alt.Chart(energy_grouped).mark_line(interpolate='monotone', size=2).encode(
    x=alt.X('energy_range', axis=alt.Axis(
        title='Energy (%)')),
    y=alt.Y('average_song_count', axis=alt.Axis(
        title='Anzahl der Songs')),
    color=alt.value('red'),
    tooltip=['energy_range', 'average_song_count']
)

energy_grouped_chart = alt.Chart(energy_grouped).mark_bar(opacity=0.6).encode(
    x=alt.X('energy_range', axis=alt.Axis(
        title='Energy (%)')),
    y=alt.Y('average_song_count', axis=alt.Axis(tickCount=10, tickMinStep=20,
                                                title='Anzahl der Songs')),
    color=alt.Color('energy_range',  scale=alt.Scale(
        scheme='viridis'), legend=alt.Legend(title="Energy (%)")),
    tooltip=['energy_range', 'average_song_count']
)

with_line = alt.layer(energy_grouped_chart, energy_grouped_line_chart).properties(
    title={'text': 'Durchschnittliche Anzahl der Songs nach Energy', 'dy': -0},

    width=550,
    height=400
).configure_title(
    fontSize=25,
    anchor='start',
    color="gray"
).configure_axis(
    labelFontSize=14,
    titleFontSize=20,
    titleColor="gray",
    labelColor="gray",
    titlePadding=12,
    grid=False
).configure_view(
    strokeWidth=0,
).configure_axisX(
    labelAngle=0,
    titleAnchor='start'
).configure_axisY(
    grid=False,
    titleAnchor='end'
)

st.markdown("""

Ein weiteres musikalisches Merkmal mit Einfluss auf die Popularität eines Songs ist die Energy. Die Energy eines Songs ist ein Maß für seine Intensität und Dynamik,
             basierend auf Faktoren wie Tempo, Lautstärke und Rhythmus. Dazu schauen wir uns die Energy-Werte der Top-Songs im Jahr 2023 an. In diesem Verteilungsdiagramm können sie die Anzahl der 
            Songs pro Energykategorie sehen. Dabei wird deutlich, dass die Verteilung einer Normalverteilung mit einer leichten Linksschiefe gleicht.

""")

col1, col2 = st.columns([3, 2])

with col1:
    with_line
with col2:
    st.markdown("""
                <br/>
                <br/>
    <div style="text-align: center">👍</div>
    <div>
        Wie in dem Verteilungsdiagramm zu sehen ist, sind die meisten Songs in dem Energybereich <span style="color: red;"> 60-70 %</span> einzuordnen.
                
    </div>
    """, unsafe_allow_html=True)
    st.markdown('----')
    st.markdown("""
    <div style="text-align: center">👎</div>
    <div>
        Ein sehr hoher oder geringer Energy-Wert sollte vermieden werden  </div>
    """, unsafe_allow_html=True)


st.markdown("""
:point_right: Sie sollten darauf achten, dass ihr Song einen :red[hohen] Energy-Wert hat, jedoch sollten sie Extreme vermeiden. 

""")


st.markdown("---")

# Map

country_mapping = {
    'England': 'United Kingdom',
    'Scotland': 'United Kingdom',
    'Buenos Aires': 'Argentina',
    'Guadalajara': 'Mexico',
    'Nashville': 'United States of America',
    'Downingtown': 'United States of America',
    'McAllen': 'United States of America',
    'Cabreúva': 'Brazil',
    'Monroe': 'United States of America',
    'Torrance': 'United States of America',
    'Los Angeles': 'United States of America',
    'Helsinki': 'Finland',
    'Manchester': 'United Kingdom',
    'Berlin': 'Germany',
    'Ipswich': 'United Kingdom',
    'Goiás': 'Brazil',
    'Mato Grosso do Sul': 'Brazil',
    'Las Palmas de Gran Canaria': 'Spain',
    'Providence': 'United States of America',
    'Orlando': 'United States of America',
    'New York': 'United States of America',
    'Austin': 'United States of America',
    'Türkiye': 'Turkey',
    'Punjab': 'India',
    'Boston': 'United States of America',
    'Amazonas': 'Brazil',
    'Rio de Janeiro': 'Brazil',
    'Sundsvall': 'Sweden',
    'Gujarat': 'India',
    'Philadelphia': 'United States of America',
    'United States': 'United States of America',
    'Oshawa': 'Canada'
}


df['artist_country'] = df['artist_country'].replace(country_mapping)

# Erstellen des DataFrames 'artist_count_by_country'
artist_count_by_country = df['artist_country'].value_counts().reset_index()
artist_count_by_country.columns = ['name', 'artist_count']


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Zusammenführen der Daten
world = world.merge(artist_count_by_country, on='name', how='left')
world['artist_count'].fillna(0, inplace=True)

json_data = json.loads(world.to_json())

# Basis-Karte mit angepassten Eigenschaften
base = alt.Chart(alt.Data(values=json_data['features'])).mark_geoshape(
    stroke='black'
).encode(
    color=alt.condition(
        'datum.properties.artist_count > 0',  # Bedingung
        alt.Color('properties.artist_count:Q', scale=alt.Scale(type="log", domain=[
            1, 368], scheme='blues',), legend=None),
        # Alternative Farbe, wenn Bedingung nicht erfüllt ist
        alt.value('lightgray')
    ),
    tooltip=[
        alt.Tooltip('properties.name:N', title='Land'),
        alt.Tooltip('properties.artist_count:Q',
                    title='Anzahl der Künstler')
    ]
).project('equirectangular').properties(
    width=1000,
    height=500
)

# Konvertieren der Geometrie in Längen- und Breitengrade
world['longitude'] = world.centroid.x
world['latitude'] = world.centroid.y

# Erstellen eines normalen Pandas DataFrame
world_df = pd.DataFrame({
    'name': world['name'],
    'artist_count': world['artist_count'],
    'longitude': world['longitude'],
    'latitude': world['latitude']
})

# Altair-Diagramm erstellen
points = alt.Chart(world_df).mark_circle(opacity=0).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    size=alt.Size('artist_count:Q', title='Anzahl der Künstler',
                  legend=None),  # Legende für die Größe entfernen
    color=alt.Color('artist_count:Q', scale=alt.Scale(scheme='blues')),
    tooltip=[alt.Tooltip('name:N', title='Land'), alt.Tooltip(
        'artist_count:Q', title='Anzahl der Künstler')]
).properties(
    title='Weltkarte der Anzahl der Künstler nach Ländern',
    width=1000,
    height=500
)

final_chart = alt.layer(base, points).configure_title(
    fontSize=25,
    anchor='start'
)


st.markdown("""
Auch die geografische Herkunft eines Künstlers spielt eine Rolle im Bezug auf den Erfolg eines Songs. In der untenstehenden 
            Map ist die Anzahl der Künstler aus dem jeweiligen Land zu sehen. Je stärker das Land eingefärbt ist,
             desto mehr Top-Künstler hat dieses Land hervorgebracht. 
""")

final_chart

st.markdown("""
:point_right: Wie in diesem Diagramm veranschaulicht, kommen die meisten Top-Künstler aus englisch- oder spanischsprachigen
            Ländern. Produzieren sie einen :red[englischen] oder :red[spanischen] Song!
""")

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.subheader("Geheimformel zum Erfolg")

st.markdown("""
$$
{Erfolg} = {Tonart(Major)} + {Key(C\#)} + {ReleaseMonat(Jan|Feb)} + {Speechiness(3\%)} + {Energy(65\%)} + {Language(Englisch|Spanisch)}
$$
""", unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("© 2023 Laurenz Brahner - Alle Rechte vorbehalten.")
