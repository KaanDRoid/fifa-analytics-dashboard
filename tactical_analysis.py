import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

class PlayerClusterAnalyzer:
    """
    Advanced player clustering and tactical analysis
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = None
        self.pca = None
        self.cluster_features = [
            'pace', 'shooting', 'passing', 'dribbling', 
            'defending', 'physic', 'overall'
        ]
    
    def perform_clustering(self, df, n_clusters=6):
        """Perform K-means clustering on player data"""
        
        # Prepare data
        cluster_data = df[self.cluster_features].dropna()
        
        # Scale features
        scaled_data = self.scaler.fit_transform(cluster_data)
        
        # Perform clustering
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.kmeans.fit_predict(scaled_data)
        
        # Add cluster labels
        result_df = df.loc[cluster_data.index].copy()
        result_df['cluster'] = clusters
        
        return result_df
    
    def get_cluster_characteristics(self, clustered_df):
        """Get characteristics of each cluster"""
        
        cluster_stats = []
        
        for cluster_id in sorted(clustered_df['cluster'].unique()):
            cluster_players = clustered_df[clustered_df['cluster'] == cluster_id]
            
            # Calculate average stats
            avg_stats = cluster_players[self.cluster_features].mean()
            
            # Determine playing style based on highest attributes
            sorted_attributes = avg_stats.sort_values(ascending=False)
            
            # Determine cluster name based on dominant attributes
            if avg_stats['defending'] > 70 and avg_stats['pace'] < 60:
                cluster_name = "Defensive Anchors"
            elif avg_stats['pace'] > 80 and avg_stats['shooting'] > 70:
                cluster_name = "Pace & Power"
            elif avg_stats['passing'] > 80 and avg_stats['dribbling'] > 75:
                cluster_name = "Playmakers"
            elif avg_stats['shooting'] > 80:
                cluster_name = "Clinical Finishers"
            elif avg_stats['defending'] > 60 and avg_stats['passing'] > 70:
                cluster_name = "Box-to-Box"
            else:
                cluster_name = f"Balanced Players"
            
            cluster_info = {
                'cluster_id': cluster_id,
                'cluster_name': cluster_name,
                'player_count': len(cluster_players),
                'avg_overall': avg_stats['overall'],
                'avg_pace': avg_stats['pace'],
                'avg_shooting': avg_stats['shooting'],
                'avg_passing': avg_stats['passing'],
                'avg_dribbling': avg_stats['dribbling'],
                'avg_defending': avg_stats['defending'],
                'avg_physic': avg_stats['physic'],
                'top_players': cluster_players.nlargest(3, 'overall')['long_name'].tolist()
            }
            
            cluster_stats.append(cluster_info)
        
        return pd.DataFrame(cluster_stats)
    
    def create_cluster_visualization(self, clustered_df):
        """Create PCA visualization of clusters"""
        
        # Prepare data for PCA
        feature_data = clustered_df[self.cluster_features]
        scaled_data = self.scaler.transform(feature_data)
        
        # Perform PCA
        self.pca = PCA(n_components=2)
        pca_data = self.pca.fit_transform(scaled_data)
        
        # Create visualization dataframe
        viz_df = pd.DataFrame({
            'PC1': pca_data[:, 0],
            'PC2': pca_data[:, 1],
            'cluster': clustered_df['cluster'],
            'player_name': clustered_df['long_name'],
            'overall': clustered_df['overall'],
            'position': clustered_df['player_positions']
        })
        
        # Create scatter plot
        fig = px.scatter(
            viz_df,
            x='PC1',
            y='PC2',
            color='cluster',
            size='overall',
            hover_data=['player_name', 'position', 'overall'],
            title='Player Clusters (PCA Visualization)',
            labels={
                'PC1': f'PC1 ({self.pca.explained_variance_ratio_[0]:.1%} variance)',
                'PC2': f'PC2 ({self.pca.explained_variance_ratio_[1]:.1%} variance)'
            }
        )
        
        fig.update_traces(marker=dict(opacity=0.7))
        fig.update_layout(height=600)
        
        return fig

def tactical_formation_analyzer(df, formation="4-3-3"):
    """Analyze best players for a specific formation"""
    
    formation_positions = {
        "4-3-3": {
            "GK": 1,
            "CB": 2, 
            "LB": 1,
            "RB": 1,
            "CM": 2,
            "CAM": 1,
            "LW": 1,
            "RW": 1,
            "ST": 1
        },
        "4-4-2": {
            "GK": 1,
            "CB": 2,
            "LB": 1, 
            "RB": 1,
            "CM": 2,
            "LM": 1,
            "RM": 1,
            "ST": 2
        }
    }
    
    if formation not in formation_positions:
        return None
    
    best_team = {}
    
    for position, count in formation_positions[formation].items():
        # Filter players by position
        position_players = df[df['player_positions'].str.contains(position, na=False)]
        
        # Get best players for this position
        best_players = position_players.nlargest(count * 3, 'overall')
        best_team[position] = best_players[['long_name', 'club_name', 'overall', 'value_eur']]
    
    return best_team

def create_team_chemistry_analysis(df, selected_players):
    """Analyze team chemistry based on selected players"""
    
    if len(selected_players) < 11:
        return None
    
    team_df = df[df['long_name'].isin(selected_players)]
    
    # Calculate team stats
    team_stats = {
        'avg_overall': team_df['overall'].mean(),
        'avg_age': team_df['age'].mean(),
        'total_value': team_df['value_eur'].sum(),
        'nationality_diversity': team_df['nationality_name'].nunique(),
        'league_diversity': team_df['league_name'].nunique(),
        'avg_pace': team_df['pace'].mean(),
        'avg_shooting': team_df['shooting'].mean(),
        'avg_passing': team_df['passing'].mean(),
        'avg_defending': team_df['defending'].mean()
    }
    
    return team_stats

def main():
    st.set_page_config(page_title="Tactical Analysis", page_icon="⚽", layout="wide")
    
    st.title("⚽ FIFA Tactical Analysis Dashboard")
    
    # Load data
    @st.cache_data
    def load_data():
        try:
            male_players = pd.read_csv('data/male_players.csv')
            female_players = pd.read_csv('data/female_players.csv')
            
            male_players['gender'] = 'Male'
            female_players['gender'] = 'Female'
            
            all_players = pd.concat([male_players, female_players], ignore_index=True)
            return all_players.dropna(subset=['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic'])
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.header("⚙️ Analysis Options")
    analysis_mode = st.sidebar.selectbox(
        "Select Analysis Mode",
        ["Player Clustering", "Formation Analysis", "Team Builder"]
    )
    
    if analysis_mode == "Player Clustering":
        st.header("🎯 Player Clustering Analysis")
        
        # Clustering parameters
        col1, col2 = st.columns(2)
        
        with col1:
            n_clusters = st.slider("Number of Clusters", 3, 10, 6)
        
        with col2:
            min_overall = st.slider("Minimum Overall Rating", 60, 90, 70)
        
        # Filter data
        filtered_df = df[df['overall'] >= min_overall]
        
        # Perform clustering
        analyzer = PlayerClusterAnalyzer()
        
        with st.spinner("Performing cluster analysis..."):
            clustered_df = analyzer.perform_clustering(filtered_df, n_clusters)
            cluster_chars = analyzer.get_cluster_characteristics(clustered_df)
        
        # Display cluster visualization
        st.subheader("📊 Cluster Visualization")
        cluster_viz = analyzer.create_cluster_visualization(clustered_df)
        st.plotly_chart(cluster_viz, use_container_width=True)
        
        # Display cluster characteristics
        st.subheader("📋 Cluster Characteristics")
        st.dataframe(cluster_chars)
        
        # Detailed cluster analysis
        st.subheader("🔍 Detailed Cluster Analysis")
        selected_cluster = st.selectbox("Select Cluster for Details", cluster_chars['cluster_id'].tolist())
        
        cluster_players = clustered_df[clustered_df['cluster'] == selected_cluster]
        cluster_info = cluster_chars[cluster_chars['cluster_id'] == selected_cluster].iloc[0]
        
        st.write(f"**Cluster Name:** {cluster_info['cluster_name']}")
        st.write(f"**Player Count:** {cluster_info['player_count']}")
        st.write(f"**Average Overall:** {cluster_info['avg_overall']:.1f}")
        
        # Top players in cluster
        st.write("**Top Players:**")
        top_cluster_players = cluster_players.nlargest(10, 'overall')[
            ['long_name', 'club_name', 'player_positions', 'overall', 'value_eur']
        ]
        st.dataframe(top_cluster_players)
    
    elif analysis_mode == "Formation Analysis":
        st.header("📐 Formation Analysis")
        
        # Formation selection
        formation = st.selectbox("Select Formation", ["4-3-3", "4-4-2"])
        
        # Analyze formation
        with st.spinner("Analyzing best players for formation..."):
            best_team = tactical_formation_analyzer(df, formation)
        
        if best_team:
            st.subheader(f"Best Players for {formation} Formation")
            
            for position, players in best_team.items():
                st.write(f"**{position}:**")
                st.dataframe(players.head(5))
                st.write("---")
    
    elif analysis_mode == "Team Builder":
        st.header("🏗️ Team Builder")
        
        # Player selection for team building
        st.subheader("Select Your Team (11 Players)")
        
        available_players = df['long_name'].dropna().tolist()
        selected_players = st.multiselect(
            "Choose Players",
            available_players,
            max_selections=11
        )
        
        if len(selected_players) == 11:
            # Analyze team chemistry
            team_stats = create_team_chemistry_analysis(df, selected_players)
            
            if team_stats:
                st.subheader("📊 Team Analysis")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Average Overall", f"{team_stats['avg_overall']:.1f}")
                    st.metric("Average Age", f"{team_stats['avg_age']:.1f}")
                
                with col2:
                    st.metric("Total Value", f"€{team_stats['total_value']/1000000:.0f}M")
                    st.metric("Nationality Diversity", team_stats['nationality_diversity'])
                
                with col3:
                    st.metric("Average Pace", f"{team_stats['avg_pace']:.1f}")
                    st.metric("Average Shooting", f"{team_stats['avg_shooting']:.1f}")
                
                with col4:
                    st.metric("Average Passing", f"{team_stats['avg_passing']:.1f}")
                    st.metric("Average Defending", f"{team_stats['avg_defending']:.1f}")
                
                # Team roster
                st.subheader("👥 Team Roster")
                team_df = df[df['long_name'].isin(selected_players)][
                    ['long_name', 'club_name', 'player_positions', 'age', 'overall', 'value_eur']
                ]
                st.dataframe(team_df)
        else:
            st.info(f"Please select {11 - len(selected_players)} more players to complete your team.")

if __name__ == "__main__":
    main()
