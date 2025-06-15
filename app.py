import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from random import randint
from PIL import Image

#настройки странички
st.set_page_config(page_title = "Анализ продаж видеоигр", layout = "wide", page_icon = "👾")

#css оформление
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poiret+One&display=swap" rel="stylesheet">

    <style>
        .stApp{
            background: linear-gradient(135deg, #2A9D8F, #203a43, #9D69A3) !important; 
            color: white !important;
            font-family: 'Poiret One', serif !important;
            margin: 0 !important; 
            padding: 0 !important;
        }
        /*звёздочки*/
         .stars {
            position: fixed;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            background: black;
            z-index: -1;
        }

        .star-field {
            position: absolute;
            width: 100%;
            height: 100%;
            animation: moveStars 10s linear infinite;
            background: radial-gradient(white 1px, transparent 1px);
            background-size: 400px 400px;
        }

        @keyframes moveStars {
            from { transform: translateY(0); }
            to { transform: translateY(-400px); }
        }

        h1, h2, h3 {
            font-family: 'Poiret One', sans-serif !important;
            color: #0fffc7 !important;
            text-align: center !important;
        }

        .stTextInput input, .stSelectbox select, .stMultiSelect select {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
            border: 1px solid #0fffc7 !important;
            border-radius: 20px !important;
            padding: 10px !important;
        }

        .stButton button {
            background-color: #0fffc7 !important;
            color: #0e1117 !important;
            border-radius: 10px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(16, 255, 199, 0.3) !important;
        }
        /*картинка, её контейнер*/
        div[data-testid="stImageContainer"]{
            allign-items: center
            box-shadow: 0 4px 8px rgba(16, 255, 199, 0.3) !important;
        }

        header[data-testid="stHeader"]{
            background: linear-gradient(135deg,  #1F1F23, #066459, #1F1F23) !important;
            border-bottom: 2px solid #203A43 !important;
            box-shadow: 0 4px 8px rgba(32, 58, 67, 0.3) !important;
        }

        div[data-testid="stPlotlyChart"]{
            border: 2px solid #ffffff !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 8px rgba(16, 255, 199, 0.3) !important;
        }
        div[data-testid="stFullScreenFrame"]{
            border: 2px solid #ffffff !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 8px rgba(16, 255, 199, 0.3) !important;
        }
        img{
            border-radius: 15px !important;
        }
        div[class="st-an st-aq st-ao st-ap st-b1 st-b2 st-af st-ak st-b3 st-b4 st-b5 st-b6 st-b7 st-b8 st-b9 st-ba st-bb st-bc st-bd st-be st-bf st-bg st-bh st-bi st-bj st-bk st-bl st-bm"]{
            color: #19d0a5;
        }
    </style>
""", unsafe_allow_html=True)



#картинка наверху
st.markdown('<h1 style="text-align:center;">Дашборд по видеоиграм</h1>', unsafe_allow_html=True)
st.markdown('<div class="centered">', unsafe_allow_html=True)
st.image("assets/header.jpg", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

#продажи по платформам
df = pd.read_csv("data/sales_by_platform.csv")

figure = px.bar(df, x = "Platform", y = "Global_Sales", color = "Global_Sales", 
                color_continuous_scale = "agsunset",
                height = 700, width = 1400,
                labels = {"Platform":"Платформа", "Global_Sales":"Продажи"})

#поворот по оси х
figure.update_layout(xaxis_tickangle = 45, plot_bgcolor='rgba(255,255,255,0.1)',
    paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
#увеличение ширины столбцов
figure.update_traces(width = 0.5)


st.subheader("Продажи по платформам")
st.plotly_chart(figure, use_container_width = True)

#Топ 10 издателей
df_publishers = pd.read_csv("data/top_10_publishers.csv")

colors = ["#52BBB7", "#8FDEB4", "#EF798A",  "#F16764", "#CA4862", "#7b4b94", "#7D82B8", "#B7E3CC", "#C4FFB2", "#D6F7A3"]
figure_publishers = px.pie(df_publishers, names = "Publisher", values = "Global_Sales",
                           labels={"Global_Sales": "Продажи (млн)", "Publisher": "Издатель"}, 
                           color_discrete_sequence = colors)
figure_publishers.update_layout(height = 600, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20))

st.subheader("Топ 10 издателей")
st.plotly_chart(figure_publishers, use_container_width=True)

#Лучшие игры по десятилетиям
df_selling_games = pd.read_csv("data/top_selling_games.csv")

#создание колонки с десятилетием
df_selling_games["Decade"] = (df_selling_games["Year"]//10).astype(int) * 10

#фильтр по десятилетиям
st.subheader("Самые продаваемые игры в каждом году")
decades = df_selling_games["Decade"].unique()
select_decade = st.select_slider("Десятилетия", decades)

decade = df_selling_games[df_selling_games["Decade"] == select_decade]
figure_decades = px.bar(decade, x = "Year", y = "Global_Sales", text = "Name",
                         labels = {"Global_Sales" : "Продажи (млн)", "Year" : "Год", "Name" : "Название"},
                         title = f"Продажи игр с {select_decade} - {select_decade+9}",
                         color = "Global_Sales", color_continuous_scale = "agsunset", animation_frame = "Decade")
figure_decades.update_layout(height = 800, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(figure_decades, use_container_width = True)

#две колонки с двумя графиками
col1, col2 = st.columns(2)

with col1:
    #лучшие продаваемые игры по регионам
    st.subheader("Топ продаваемых 10 игр по регионам")
    df_regions = pd.read_csv("data/top_games_by_region.csv", keep_default_na = False) #чтобы NA (North America) не читался как NaN
    df_regions = df_regions.replace({"NA":"North America", "JP" : "Japan", "EU" : "Europe"})
    regions = df_regions["Region"].unique()

    select_regions = st.selectbox("Регион:", regions)

    #фильтрация по выбранному региону
    regions_filter = df_regions[df_regions["Region"] == select_regions]

    #фильтрация по продажам (первые 10)
    regions_filter = regions_filter.sort_values(by = 'Sales', ascending  = False).head(10).reset_index(drop = True)

    custom_color_scale = ["#592E83", "#82FF9E", "#A9FBC3", "#B594B6", "#D991BA"]
    regions_figure = px.bar(regions_filter, x = "Name", y = "Sales", color = "Sales", color_continuous_scale = custom_color_scale,
        labels = {"Name" : "Название", "Sales" : "Продажи (млн)"})
    regions_figure.update_layout(plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20))

    st.plotly_chart(regions_figure, use_container_width=True)

with col2:
    #Топ 10 игр по жанрам
    df_genres = pd.read_csv('data/top_10_games_in_genre.csv')

    genres = df_genres["Genre"].unique()

    st.subheader("Топ 10 игр по жанрам")
    select_genre = st.selectbox("Жанр:", genres)

    #фильтрация
    filter_df = df_genres[df_genres['Genre'] == select_genre]

    genre_figure = px.bar(filter_df, x = "Name", y = "Global_Sales",
                    color = "Global_Sales", color_continuous_scale="bupu",
                    labels={"Name": "Название", "Global_Sales":"Продажи (млн)"})
    genre_figure.update_layout(height = 700, plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(genre_figure, use_container_width=True)

#heatmap по жанрам
st.subheader("Популярность жанров по годам")

#загрузка таблицы
df_genres = pd.read_csv("data/genre_year_pivot.csv", index_col = 0)

#получение списка жанров для фильтрации
genres_for_heatmap = df_genres.index.tolist()
genre_selection_for_heatmap = st.multiselect("Жанры:", options = genres_for_heatmap, default = genres_for_heatmap)

#фильтрация по выбранным жанрам
filtered_data = df_genres.loc[genre_selection_for_heatmap]

#тепловая карта через go.heatmap
figure_genres = go.Figure(data = go.Heatmap(z = filtered_data.values,
    x = filtered_data.columns.tolist(),  #годы
    y = filtered_data.index.tolist(),    #жанры
    colorscale ='Viridis',
    text = filtered_data.values,
    texttemplate = "%{text:.2f}",
    textfont = {"size": 8},
    hoverongaps = False
))

#обновление макета графика
figure_genres.update_layout(xaxis_title = "Год", yaxis_title = "Жанр",
    yaxis = dict(tickmode = 'linear'), height = 800, width = 1800,
    font = dict(family = "Arial", size = 12),
    title_x = 0.5, title = "Тепловая карта жанров",
    plot_bgcolor='rgba(255,255,255,0.1)', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(figure_genres, use_container_width = True)