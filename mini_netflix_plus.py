import streamlit as st
from operator import itemgetter
from openai import OpenAI

# --- Mock movie dataset ---
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

# --- Helper: Classic search ---
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

# --- Streamlit UI ---
st.set_page_config(page_title='Mini Netflix', layout='wide')
st.title('Mini Netflix 🎬')

# Sidebar filters
min_year, max_year = 1990, 2025
st.sidebar.header('Search & Filters')
query = st.sidebar.text_input('Search title or year', '')
year_filter = st.sidebar.slider('Year range', min_year, max_year, (min_year, max_year))

available_genres = sorted({movie['genre'] for movie in MOVIES})
selected_genres = st.sidebar.multiselect('Genre', available_genres, default=available_genres)
active_genres = selected_genres or available_genres

# Filtered list
filtered = search_movies(query, year_filter, active_genres)
filtered = sorted(filtered, key=itemgetter("year"),reverse=True)



# --- Conversational Movie Assistant ---
st.sidebar.header("🎤 AI Movie Assistant")

# Tone control
tone = st.sidebar.selectbox("Assistant Style", ["Casual 😎", "Serious 🎓", "Emoji-heavy 🤖", "Friendly 🌟"])

user_input = st.sidebar.text_input("Ask me for a recommendation...")

if st.sidebar.button("Ask AI") and user_input:
    # Create OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Build the conversation
    conversation = [{"role": "system", "content": f"You are a helpful movie assistant. Reply in a {tone} style."}]
    
    # Add new user query
    conversation.append({"role": "user", "content": f"{user_input}\nHere is the available movie dataset:\n{MOVIES}"})

    # --- Call OpenAI API (new syntax) ---
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        max_tokens=200,
        temperature=0.7,
    )

    ai_reply = response.choices[0].message.content

    # Display chat
    st.sidebar.markdown(f"**You:** {user_input}")
    st.sidebar.markdown(f"**AI:** {ai_reply}")

    # Try to extract matching titles
    suggestions = [m for m in MOVIES if m["title"].lower() in ai_reply.lower()]
    
    st.session_state.ai_suggestions = suggestions

if "ai_suggestions" not in st.session_state:
    st.session_state["ai_suggestions"] = []
    
# --- Display movies ---
if st.session_state.ai_suggestions:
    st.subheader("✨ Recommended for you")
    movies_to_show = st.session_state.ai_suggestions
else:
    movies_to_show = search_movies(query, year_filter, active_genres)
    movies_to_show = sorted(movies_to_show, key=itemgetter("year"), reverse=True)

st.write(f"Found **{len(movies_to_show)}** movie(s)")
print(movies_to_show)
for movie in movies_to_show:
    st.image(movie["poster"], use_container_width=True)
    st.subheader(f"{movie['title']} ({movie['year']})")
    st.caption(f"{movie['synopsis']} - Genre: {movie['genre']}")
    if st.button(f"Play {movie['title']}", key=movie['title']):
        st.video(movie["url"])