import streamlit as st
import pandas as pd

# Load the model/stats
agg_stats = pd.read_pickle("agg_stats.pkl")

def recommend_batting_order(team_players, opposition, venue):
    scores = []
    for player in team_players:
        player_data = agg_stats[
            (agg_stats['batsman'] == player) &
            (agg_stats['bowling_team'] == opposition) &
            (agg_stats['venue'] == venue)
        ]
        if player_data.empty:
            scores.append((player, 0))
        else:
            best_row = player_data.sort_values('runs', ascending=False).iloc[0]
            scores.append((player, best_row['runs']))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return [player for player, _ in scores]

st.title("🏏 Optimal Batting Order Recommender (IPL)")

team_input = st.text_area("Enter playing XI (comma-separated)", "Virat Kohli, Faf du Plessis, Glenn Maxwell, Dinesh Karthik, Shahbaz Ahmed, ...")
opposition = st.selectbox("Select Opposition Team", agg_stats['bowling_team'].unique())
venue = st.selectbox("Select Venue", agg_stats['venue'].unique())

if st.button("Recommend Order"):
    players = [p.strip() for p in team_input.split(",")]
    order = recommend_batting_order(players, opposition, venue)
    st.subheader("🔢 Recommended Order")
    for i, player in enumerate(order, 1):
        st.markdown(f"**{i}. {player}**")
