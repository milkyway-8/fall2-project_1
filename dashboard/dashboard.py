import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from stop_words import get_stop_words
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.sidebar.header("Навигация")

@st.cache_data
def load_italian_restaurants():
    df_ital = pd.read_excel('/Users/damiraalimallaeva/PycharmProjects/PythonProject/italian_final.xlsx')
    return df_ital

def load_georgian_restaurants():
    df_georg = pd.read_excel('/Users/damiraalimallaeva/PycharmProjects/PythonProject/georgian_final.xlsx')
    return df_georg

def load_all_restaurants():
    df_all= pd.read_excel('/Users/damiraalimallaeva/PycharmProjects/PythonProject/restaurants_final.xlsx')
    return df_all


if st.sidebar.button("Главная"):
    st.session_state.page = "Главная"
if st.sidebar.button("Данные"):
    st.session_state.page = "Данные"

if st.sidebar.button("EDA"):
    st.session_state.page = "EDA"
if st.sidebar.button("Тренды & закономерности"):
    st.session_state.page = "Тренды & закономерности"
if st.sidebar.button("Выводы & рекомендации"):
    st.session_state.page = "Выводы & рекомендации"

if "page" not in st.session_state:
    st.session_state.page = "Главная"


if st.session_state.page == "Главная":
    st.markdown(
        '<h1 style="color: #FF6347;">Сравнение грузинских и итальянских ресторанов в Санкт-Петербурге</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h2 style="color: #FFFFFF;">ФИО автора: Алималлаева Дамира Фагилевна(464978)</h2>',
        unsafe_allow_html=True
    )
    st.write('')
    st.write("Сравниваю рестораны по СПб с сайта Irecommend с фильтрами 'грузинская кухня' и 'итальянская кухня'")
if st.session_state.page == "Данные":
    col1, col2 = st.columns(2)
    with col1:
        df_ital = load_italian_restaurants()
        st.markdown(
            '<h3 style="color: #FF6347;">Итальянские рестораны</h3>',
            unsafe_allow_html=True
        )
        n_rows_italy = st.slider("Сколько строк показать?", min_value=5, max_value=len(df_ital), key="ital_slider")
        median_rating_ital = df_ital.head(n_rows_italy)['rating'].median()
        total_likes_italy = df_ital.head(n_rows_italy)['likes'].sum()
        total_dislikes_italy = df_ital.head(n_rows_italy)['dislikes'].sum()
        st.metric('Средний рейтинг(медиана)', round(median_rating_ital, 2), delta=None, delta_color="normal", help=None,
                  label_visibility="visible", border=False)
        st.metric('Количество лайков', total_likes_italy, delta=None, delta_color="normal", help=None,
                  label_visibility="visible", border=False)
        st.metric('Количество дизлайков', total_dislikes_italy, delta=None, delta_color="normal", help=None,
                  label_visibility="visible", border=False)
        st.dataframe(df_ital.head(n_rows_italy))
    with col2:
        df_georg = load_georgian_restaurants()
        st.markdown(
            '<h3 style="color: #FF6347;">Грузинские рестораны</h3>',
            unsafe_allow_html=True
        )
        n_rows_georg = st.slider("Сколько строк показать?", min_value=5, max_value=len(df_georg), key="georg_slider")
        median_rating_georg = df_georg.head(n_rows_georg)['rating'].median()
        total_likes_georg = df_georg.head(n_rows_georg)['likes'].sum()
        total_dislikes_georg = df_georg.head(n_rows_georg)['dislikes'].sum()
        st.metric('Средний рейтинг(медиана)', round(median_rating_georg, 2), delta=None, delta_color="normal", help=None, label_visibility="visible",
                  border=False)
        st.metric('Количество лайков', total_likes_georg, delta=None, delta_color="normal", help=None,
                  label_visibility="visible", border=False)
        st.metric('Количество дизлайков', total_dislikes_georg, delta=None, delta_color="normal", help=None,
                  label_visibility="visible", border=False)
        st.dataframe(df_georg.head(n_rows_georg))
    st.markdown(
        '<h3 style="color: #FF6347;">Итальянские и грузинские рестораны</h3>',
        unsafe_allow_html=True
    )
    df_all = load_all_restaurants()
    n_rows_all = st.slider("Сколько строк показать?", min_value=5, max_value=len(df_all), key="all_slider")
    median_rating = df_all.head(n_rows_all)['rating'].median()
    total_likes_all = df_all.head(n_rows_all)['likes'].sum()
    total_dislikes_all = df_all.head(n_rows_all)['dislikes'].sum()
    st.metric('Средний рейтинг(медиана)', round(median_rating, 2), delta=None, delta_color="normal", help=None,
              label_visibility="visible", border=False)
    st.metric('Количество лайков', total_likes_all, delta=None, delta_color="normal", help=None,
              label_visibility="visible", border=False)
    st.metric('Количество дизлайков', total_dislikes_all, delta=None, delta_color="normal", help=None,
              label_visibility="visible", border=False)
    st.dataframe(df_all.head(n_rows_all))
    st.divider()
elif st.session_state.page == "EDA":
    st.markdown(
        '<h3 style="color: #FF6347;">Общая информация о всех данных</h3>',
        unsafe_allow_html=True
    )
    st.write(f"Всего записей: {len(load_all_restaurants())}")
    st.write(f"Колонки: {', '.join(load_all_restaurants().columns)}")
    st.write(f"Количество пропусков: 0")
    st.dataframe(load_all_restaurants().head(5))

    fig = px.histogram(
        load_georgian_restaurants(),
        x='rating',
        nbins=100,
        title='Распределение оценок грузинских ресторанов',
        labels={'rating': 'Оценка', 'count': 'Частота'},
        color_discrete_sequence=['blue'],
        opacity=0.8
    )
    fig.update_layout(
        bargap=0.1,
        xaxis_title='Оценка',
        yaxis_title='Частота'
    )
    st.plotly_chart(fig, use_container_width=True)
    fig = px.histogram(
        load_italian_restaurants(),
        x='rating',
        nbins=100,
        title='Распределение оценок итальянских ресторанов',
        labels={'rating': 'Оценка', 'count': 'Частота'},
        color_discrete_sequence=['blue'],
        opacity=0.8
    )
    fig.update_layout(
        bargap=0.1,
        xaxis_title='Оценка',
        yaxis_title='Частота'
    )
    st.plotly_chart(fig, use_container_width=True)
    @st.cache_data
    def generate_wordcloud_georgian(text_georgian, max_words=200, colormap='viridis'):
        STOPWORDS_RU = get_stop_words('russian')
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=STOPWORDS_RU,
            max_words=max_words,
            colormap=colormap,
            collocations=False,
            font_path='/System/Library/Fonts/Supplemental/Arial.ttf' # Здесь следует поменять под собственную ОС
        ).generate(text_georgian)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        return fig

    @st.cache_data
    def generate_wordcloud_italian(text_italian, max_words=200, colormap='viridis'):
        STOPWORDS_RU = get_stop_words('russian')
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=STOPWORDS_RU,
            max_words=max_words,
            colormap=colormap,
            collocations=False,
            font_path='/System/Library/Fonts/Supplemental/Arial.ttf' # Здесь следует поменять под собственную ОС
        ).generate(text_italian)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        return fig
    st.markdown(
        '<h3 style="color: #FF6347;">Облако слов из отзывов на грузинские рестораны:</h3>',
        unsafe_allow_html=True
    )
    st.write("")
    text_georgian = ''
    text_georgian = ' '.join(load_georgian_restaurants()['reviews'].astype(str))
    fig_georg = generate_wordcloud_georgian(text_georgian)
    st.pyplot(fig_georg)

    st.markdown(
        '<h3 style="color: #FF6347;">Облако слов из отзывов на итальянские рестораны:</h3>',
        unsafe_allow_html=True
    )
    st.write("")
    text_italian = ''
    text_italian = ' '.join(load_italian_restaurants()['reviews'].astype(str))
    fig_italian = generate_wordcloud_georgian(text_italian)
    st.pyplot(fig_italian)
elif st.session_state.page == "Тренды & закономерности":
    st.markdown(
        '<h2 style="color: #FF6347;">Сравнение кухонь</h2>',
        unsafe_allow_html=True
    )
    cuisines = st.multiselect(
        "Кухня",
        options=load_all_restaurants()["cuisine"].unique(),
        default=load_all_restaurants()["cuisine"].unique()
    )
    metric = st.selectbox("Метрика для сравнения", ["rating", "likes", "dislikes"])
    rating_range = st.slider(
        "Диапазон рейтинга",
        min_value=0.0,
        max_value=5.0,
        value=(3.0, 5.0)
    )
    filtered_df = load_all_restaurants()[
        (load_all_restaurants()["cuisine"].isin(cuisines)) &
        (load_all_restaurants()["rating"] >= rating_range[0]) &
        (load_all_restaurants()["rating"] <= rating_range[1])
        ]
    if metric == "rating":
        fig = px.bar(
            filtered_df.groupby("cuisine")[metric].mean().reset_index(),
            x="cuisine",
            y=metric,
            title=f"Средний рейтинг по кухням"
        )
    elif metric == "likes":
        fig = px.bar(
            filtered_df.groupby("cuisine")[metric].sum().reset_index(),
            x="cuisine",
            y=metric,
            title=f"Количество лайков по кухням"
        )
    elif metric == "dislikes":
        fig = px.bar(
            filtered_df.groupby("cuisine")[metric].sum().reset_index(),
            x="cuisine",
            y=metric,
            title=f"Количество дизлайков по кухням"
        )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<h2 style="color: #FF6347;">Корреляции</h2>',
        unsafe_allow_html=True
    )
    x_axis = st.selectbox("Ось X", load_all_restaurants().select_dtypes(include="number").columns)
    y_axis = st.selectbox("Ось Y", load_all_restaurants().select_dtypes(include="number").columns)

    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        title=f"Зависимость {x_axis} от {y_axis}"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '<h2 style="color: #FF6347;">Топ - 10 ресторанов по разным критериям</h2>',
        unsafe_allow_html=True
    )
    top_by = st.selectbox(
        "Критерий:",
        ["rating", "likes", "dislikes"]
    )
    n_top = 10
    top_df = filtered_df.nlargest(n_top, top_by)
    st.dataframe(
        top_df[["name", "cuisine", top_by]],
        hide_index=True
    )
elif st.session_state.page == "Выводы & рекомендации":
    st.markdown(
        '<h2 style="color: #FF6347;">Выводы:</h2>',
        unsafe_allow_html=True
    )
    st.write('1) Рестораны с высоким рейтингом максиум имеют около 5 - 10 лайков')
    st.write('2) Анализ подтверждает мысль, что качество не равно популярность. '
             'Рестораны с высоким рейтингом могут иметь малое количество лайков')
    st.write('3) Если у ресторанов лайков много, но сами они занимают в рейтинге не высокое место, '
             'то,скорее всего, маркетинг у таких заведений на высоком уровне. Быть может, они даже дают какие-то плюшки за оставленный отзыв. '
             'Замечание: в нашем случае кол-во лайков+ кол-во дизлайков = кол-во отзывов')
    st.write('4) Есть связь между количеством дизлайков и рейтингом ресторанов обеих кухонь. Может быть, негативные отзывы вызывают больше реакции')
    st.write('5) Вероятность того, что выбранное заведение грузинской кухни понравится больше,чем выбранное заведение итальянской кухни')
    st.write('6) В своем проекте я представила топ-10 ресторанов по разным критериям(рейтинг, кол-во лайков/дизлайков), '
             'поэтому в следующий раз я пойду в ресторан из предложенного мною списка')
    st.write('7) Говоря об анализе слов, я поняла, что акцент в отзывах на грузинские рестораны делается на '
             'обстановку и атмосферу, а в отзывах на итальяскую кухню на еду и эмоции')

    st.markdown(
        '<h2 style="color: #FF6347;">Обсуждение:</h2>',
        unsafe_allow_html=True
    )
    st.write('В рамках моего исследования я хотела сравнить грузинские и итальянские рестораны, найти какие-то закономерности, '
             'а также выявить топ-10 ресторанов по различным критериям. Это удалось сделать.')
    st.write("Изначально я планировала брать данные с сайта Tripadvisor, однако меня он постоянно блокировал, а API у него платный. В Tripadvisor, конечно, больше информации о ресторанах, например, о ценовом сегменте. Еще там намного больше представлено отзывов. "
             "В будущем хотелось бы собрать больше информации о ресторанах с сайтов, которые предоставляют такую информацию. (Irecommend в этом плане немного скудный). Также можно в будущем анализировать отзывы не только которые отображаются на главной странице, но и те, которые видны при переходе на вкладку 'Читать все отзывы'.")

    st.write('Мое исследование может быть полезно маркетологам ресторанов для разработки стратегии продвижения по привлечению новых клиентов, они могут увидеть рейтинг своего ресторана относительно других. Быть может, шеф-повара, благодаря облаку слов, смогут проанализировать часто встречащиеся блюда и сформировать меню в соответствии с результатами. Логику моего исследования можно повторить с любыми ресторанами сайта, других сайтов с ресторанами. Поменяв названия колонок, адаптиров их под новую тему, можно анализировать развлечения, отели и так далее.')
