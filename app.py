import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FIFA Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess FIFA player data"""
    try:
        # Load both male and female player data
        male_players = pd.read_csv('data/male_players.csv')
        female_players = pd.read_csv('data/female_players.csv')
        
        # Add gender column
        male_players['gender'] = 'Male'
        female_players['gender'] = 'Female'
        
        # Combine datasets
        all_players = pd.concat([male_players, female_players], ignore_index=True)
        
        # Clean data
        all_players = all_players.dropna(subset=['overall', 'potential', 'value_eur'])
        all_players['value_eur'] = all_players['value_eur'].fillna(0)
        all_players['wage_eur'] = all_players['wage_eur'].fillna(0)
        
        # Create age groups
        all_players['age_group'] = pd.cut(all_players['age'], 
                                        bins=[0, 20, 25, 30, 35, 50], 
                                        labels=['U20', '20-25', '25-30', '30-35', '35+'])
        
        return all_players
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_player_skills(df, player_id):
    """Extract skill attributes for radar chart"""
    skill_cols = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    player = df[df['player_id'] == player_id].iloc[0]
    return {col: player[col] for col in skill_cols if col in df.columns}

def create_radar_chart(player_skills, player_name):
    """Create radar chart for player skills"""
    categories = list(player_skills.keys())
    values = list(player_skills.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player_name,
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"{player_name} - Skill Radar"
    )
    
    return fig

def predict_player_value(df, player_features):
    """Predict player market value using Random Forest"""
    # Select features for prediction
    feature_cols = ['overall', 'potential', 'age', 'pace', 'shooting', 
                   'passing', 'dribbling', 'defending', 'physic']
    
    # Prepare data
    X = df[feature_cols].dropna()
    y = df.loc[X.index, 'value_eur']
    
    # Remove outliers (values > 200M)
    mask = y < 200000000
    X, y = X[mask], y[mask]
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make prediction
    prediction = model.predict([player_features])[0]
    
    # Calculate model performance
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return prediction, mae, r2

def main():
    # Header
    st.markdown('<div class="main-header">⚽ FIFA Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Gender filter
    gender_options = ['All'] + list(df['gender'].unique())
    selected_gender = st.sidebar.selectbox("Gender", gender_options)
    
    # Position filter
    position_options = ['All'] + sorted(df['player_positions'].dropna().unique())
    selected_position = st.sidebar.selectbox("Position", position_options)
    
    # League filter
    league_options = ['All'] + sorted(df['league_name'].dropna().unique())
    selected_league = st.sidebar.selectbox("League", league_options)
    
    # Age range
    age_range = st.sidebar.slider("Age Range", 
                                 int(df['age'].min()), 
                                 int(df['age'].max()), 
                                 (18, 35))
    
    # Overall rating range
    overall_range = st.sidebar.slider("Overall Rating", 
                                    int(df['overall'].min()), 
                                    int(df['overall'].max()), 
                                    (60, 95))
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
    
    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['player_positions'].str.contains(selected_position, na=False)]
    
    if selected_league != 'All':
        filtered_df = filtered_df[filtered_df['league_name'] == selected_league]
    
    filtered_df = filtered_df[
        (filtered_df['age'] >= age_range[0]) & 
        (filtered_df['age'] <= age_range[1]) &
        (filtered_df['overall'] >= overall_range[0]) & 
        (filtered_df['overall'] <= overall_range[1])
    ]
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👤 Player Analysis", "🔍 Comparison", "🤖 ML Insights"])
    
    with tab1:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Players", len(filtered_df))
        with col2:
            st.metric("Average Overall", f"{filtered_df['overall'].mean():.1f}")
        with col3:
            st.metric("Average Age", f"{filtered_df['age'].mean():.1f}")
        with col4:
            st.metric("Average Value", f"€{filtered_df['value_eur'].mean()/1000000:.1f}M")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Overall distribution
            fig = px.histogram(filtered_df, x='overall', nbins=20, 
                             title="Overall Rating Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top leagues by player count
            if not filtered_df.empty:
                league_counts = filtered_df['league_name'].value_counts().head(10)
                fig = px.bar(x=league_counts.values, y=league_counts.index, 
                           orientation='h', title="Top Leagues by Player Count")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age vs Overall scatter
            fig = px.scatter(filtered_df.sample(min(1000, len(filtered_df))), 
                           x='age', y='overall', color='gender',
                           title="Age vs Overall Rating")
            st.plotly_chart(fig, use_container_width=True)
            
            # Value distribution by position
            if selected_position == 'All' and len(filtered_df) > 0:
                position_value = filtered_df.groupby('player_positions')['value_eur'].mean().head(10)
                fig = px.bar(x=position_value.index, y=position_value.values,
                           title="Average Value by Position")
                fig.update_xaxis(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Player Analysis")
        
        # Player selection
        player_options = filtered_df['long_name'].dropna().tolist()
        if player_options:
            selected_player = st.selectbox("Select a Player", player_options)
            
            if selected_player:
                player_data = filtered_df[filtered_df['long_name'] == selected_player].iloc[0]
                
                # Player info
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.image(player_data['player_face_url'], width=150)
                
                with col2:
                    st.subheader(player_data['long_name'])
                    st.write(f"**Club:** {player_data['club_name']}")
                    st.write(f"**Position:** {player_data['player_positions']}")
                    st.write(f"**Age:** {player_data['age']}")
                    st.write(f"**Overall:** {player_data['overall']}")
                    st.write(f"**Potential:** {player_data['potential']}")
                    st.write(f"**Value:** €{player_data['value_eur']/1000000:.1f}M")
                
                with col3:
                    st.write(f"**Nationality:** {player_data['nationality_name']}")
                    st.write(f"**Height:** {player_data['height_cm']} cm")
                    st.write(f"**Weight:** {player_data['weight_kg']} kg")
                    st.write(f"**Preferred Foot:** {player_data['preferred_foot']}")
                    st.write(f"**Weak Foot:** {player_data['weak_foot']} ⭐")
                    st.write(f"**Skill Moves:** {player_data['skill_moves']} ⭐")
                
                # Radar chart
                player_skills = get_player_skills(filtered_df, player_data['player_id'])
                if player_skills:
                    fig = create_radar_chart(player_skills, selected_player)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No players found with the current filters.")
    
    with tab3:
        st.header("Player Comparison")
        
        if len(player_options) >= 2:
            col1, col2 = st.columns(2)
            
            with col1:
                player1 = st.selectbox("Select First Player", player_options, key="player1")
            
            with col2:
                player2 = st.selectbox("Select Second Player", 
                                     [p for p in player_options if p != player1], key="player2")
            
            if player1 and player2:
                p1_data = filtered_df[filtered_df['long_name'] == player1].iloc[0]
                p2_data = filtered_df[filtered_df['long_name'] == player2].iloc[0]
                
                # Comparison table
                comparison_data = {
                    'Attribute': ['Overall', 'Potential', 'Age', 'Value (€M)', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical'],
                    player1: [p1_data['overall'], p1_data['potential'], p1_data['age'], 
                             p1_data['value_eur']/1000000, p1_data['pace'], p1_data['shooting'], 
                             p1_data['passing'], p1_data['dribbling'], p1_data['defending'], p1_data['physic']],
                    player2: [p2_data['overall'], p2_data['potential'], p2_data['age'], 
                             p2_data['value_eur']/1000000, p2_data['pace'], p2_data['shooting'], 
                             p2_data['passing'], p2_data['dribbling'], p2_data['defending'], p2_data['physic']]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True)
                
                # Side-by-side radar charts
                col1, col2 = st.columns(2)
                
                with col1:
                    skills1 = get_player_skills(filtered_df, p1_data['player_id'])
                    if skills1:
                        fig1 = create_radar_chart(skills1, player1)
                        st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    skills2 = get_player_skills(filtered_df, p2_data['player_id'])
                    if skills2:
                        fig2 = create_radar_chart(skills2, player2)
                        st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Need at least 2 players for comparison.")
    
    with tab4:
        st.header("Machine Learning Insights")
        
        # Player clustering
        st.subheader("Player Clustering Analysis")
        
        if len(filtered_df) > 10:
            # Prepare data for clustering
            cluster_features = ['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
            cluster_data = filtered_df[cluster_features].dropna()
            
            if len(cluster_data) > 5:
                # Standardize features
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(cluster_data)
                
                # Perform clustering
                n_clusters = st.slider("Number of Clusters", 2, 8, 4)
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(scaled_data)
                
                # Add cluster labels to dataframe
                cluster_df = filtered_df.loc[cluster_data.index].copy()
                cluster_df['cluster'] = clusters
                
                # Visualize clusters
                fig = px.scatter(cluster_df, x='overall', y='value_eur', 
                               color='cluster', title="Player Clusters",
                               hover_data=['long_name', 'club_name'])
                st.plotly_chart(fig, use_container_width=True)
                
                # Cluster characteristics
                st.subheader("Cluster Characteristics")
                cluster_summary = cluster_df.groupby('cluster')[cluster_features].mean()
                st.dataframe(cluster_summary)
        
        # Value prediction
        st.subheader("Player Value Prediction")
        
        # Select a player for prediction
        if player_options:
            prediction_player = st.selectbox("Select Player for Value Prediction", player_options, key="prediction")
            
            if prediction_player:
                player_data = filtered_df[filtered_df['long_name'] == prediction_player].iloc[0]
                
                # Extract features
                feature_values = [
                    player_data['overall'], player_data['potential'], player_data['age'],
                    player_data['pace'], player_data['shooting'], player_data['passing'],
                    player_data['dribbling'], player_data['defending'], player_data['physic']
                ]
                
                # Make prediction
                try:
                    predicted_value, mae, r2 = predict_player_value(df, feature_values)
                    actual_value = player_data['value_eur']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Actual Value", f"€{actual_value/1000000:.1f}M")
                    with col2:
                        st.metric("Predicted Value", f"€{predicted_value/1000000:.1f}M")
                    with col3:
                        difference = abs(predicted_value - actual_value) / actual_value * 100
                        st.metric("Difference", f"{difference:.1f}%")
                    
                    st.info(f"Model Performance: MAE = €{mae/1000000:.1f}M, R² = {r2:.3f}")
                    
                except Exception as e:
                    st.error(f"Prediction error: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Inspired by [FifaDash](https://github.com/EkremBayar/FifaDash)")

if __name__ == "__main__":
    main()
