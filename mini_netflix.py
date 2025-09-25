import streamlit as st

# Mock movie dataset
MOVIES = [
    {
        'title': 'The Demon Hunter',
        'year': 2025,
        'genre': 'Horror',
        'poster': 'https://www.republicrecords.com/cdn/shop/files/REPU-00092_KPOP_DemonHunters_CollectionPage-Banner-02Desktop.png?v=1751556729&width=2000',
        'synopsis': 'A grieving detective uncovers secrets in a small town.',
        'url': 'https://youtu.be/3JTVQTk36R8?si=tLugG5Ib-SRZaixD',
    },
    {
        'title': 'Smurf',
        'year': 2025,
        'genre': 'Animation',
        'poster': 'https://i.ebayimg.com/images/g/oBIAAOSwDxJoJWG6/s-l1600.webp',
        'synopsis': 'In a neon-lit future, a courier becomes an unlikely hero.',
        'url': 'https://www.youtube.com/watch?v=EqPtz5qN7HM',
    },
    {
        'title': 'Toy Story',
        'year': 1995,
        'genre': 'Animation',
        'poster': 'https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg',
        'synopsis': 'Woody and Buzz must work together after getting separated from their kid.',
        'url': 'https://www.youtube.com/watch?v=KYz2wyBy3kc',
    },
    {
        'title': 'Frozen',
        'year': 2013,
        'genre': 'Animation',
        'poster': 'https://image.tmdb.org/t/p/w500/kgwjIb2JDHRhNk13lmSxiClFjVk.jpg',
        'synopsis': 'Anna and her friends search for Elsa to end a kingdom-wide winter.',
        'url': 'https://www.youtube.com/watch?v=TbQm5doF_Uc',
    },
    {
        'title': 'Moana',
        'year': 2016,
        'genre': 'Adventure',
        'poster': 'https://image.tmdb.org/t/p/w500/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg',
        'synopsis': 'Moana sets sail with demigod Maui to save her island.',
        'url': 'https://www.youtube.com/watch?v=LKFuXETZUsI',
    },
    {
        'title': 'Finding Nemo',
        'year': 2003,
        'genre': 'Adventure',
        'poster': 'https://image.tmdb.org/t/p/w500/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg',
        'synopsis': 'Marlin searches the ocean with Dory to rescue his son Nemo.',
        'url': 'https://www.youtube.com/watch?v=wZdpNglLbt8',
    },
]


def search_movies(query, year_range, genres):
    query_lower = query.lower()
    start_year, end_year = year_range
    return [
        movie
        for movie in MOVIES
        if (query_lower in movie['title'].lower() or query in str(movie['year']))
        and start_year <= movie['year'] <= end_year
        and (not genres or movie['genre'] in genres)
    ]


def year_bounds():
    years = [movie['year'] for movie in MOVIES]
    return min(years), max(years)


# --- App UI ---
min_year, max_year = year_bounds()
st.set_page_config(page_title='Mini Netflix', layout='wide')
st.title('Mini Netflix')

# Sidebar filters
st.sidebar.header('Search & Filters')
query = st.sidebar.text_input('Search title or year', '')
year_filter = st.sidebar.slider('Year range', min_year, max_year, (min_year, max_year))

available_genres = sorted({movie['genre'] for movie in MOVIES})
selected_genres = st.sidebar.multiselect('Genre', available_genres, default=available_genres)
active_genres = selected_genres or available_genres

# Filter movies
filtered = search_movies(query, year_filter, active_genres)

st.write(f'Found **{len(filtered)}** movie(s)')

# Display movies in a grid
for idx, movie in enumerate(filtered):
    title = movie['title']
    year = movie['year']
    synopsis = movie['synopsis']
    genre = movie['genre']
    st.image(movie['poster'], use_container_width=True)
    st.subheader(f'{title} ({year})')
    st.caption(f'{synopsis} - Genre: {genre}')
    if st.button(f'Play {title}', key=title):
        st.video(movie['url'])
