import streamlit as st
import pandas as pd
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.analytics import PlayerValuePredictor, PlayerAnalyzer, generate_player_report
from utils.visualizations import (
    create_advanced_radar_chart, 
    create_value_vs_performance_scatter,
    create_position_analysis_chart,
    create_league_comparison_chart,
    create_correlation_heatmap
)

st.set_page_config(
    page_title="Advanced FIFA Analytics",
    page_icon="🏆",
    layout="wide"
)

def main():
    st.title("🏆 Advanced FIFA Analytics Dashboard")
    
    # Load data
    @st.cache_data
    def load_data():
        try:
            male_players = pd.read_csv('data/male_players.csv')
            female_players = pd.read_csv('data/female_players.csv')
            
            male_players['gender'] = 'Male'
            female_players['gender'] = 'Female'
            
            all_players = pd.concat([male_players, female_players], ignore_index=True)
            return all_players.dropna(subset=['overall', 'potential'])
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.header("🔧 Advanced Filters")
    
    # Analysis type
    analysis_type = st.sidebar.selectbox(
        "Analysis Type",
        ["Player Insights", "Market Analysis", "Performance Prediction", "League Comparison"]
    )
    
    if analysis_type == "Player Insights":
        st.header("🎯 Player Deep Dive Analysis")
        
        # Player selection
        player_name = st.selectbox("Select Player", df['long_name'].dropna().unique())
        
        if player_name:
            player_data = df[df['long_name'] == player_name].iloc[0]
            
            # Generate comprehensive report
            with st.spinner("Generating player report..."):
                report = generate_player_report(df, player_data['player_id'])
            
            # Display basic info
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if 'player_face_url' in player_data and pd.notna(player_data['player_face_url']):
                    st.image(player_data['player_face_url'], width=150)
            
            with col2:
                st.subheader(report['basic_info']['name'])
                st.write(f"**Club:** {report['basic_info']['club']}")
                st.write(f"**Position:** {report['basic_info']['position']}")
                st.write(f"**Age:** {report['basic_info']['age']}")
                st.write(f"**Nationality:** {report['basic_info']['nationality']}")
            
            with col3:
                st.metric("Overall", report['ratings']['overall'])
                st.metric("Potential", report['ratings']['potential'])
                st.metric("Performance Index", f"{report['ratings']['performance_index']:.1f}")
            
            # Advanced radar chart
            st.subheader("📊 Skills Analysis")
            radar_fig = create_advanced_radar_chart(player_data)
            st.plotly_chart(radar_fig, use_container_width=True)
            
            # Similar players
            if not report['similar_players'].empty:
                st.subheader("👥 Similar Players")
                st.dataframe(report['similar_players'])
    
    elif analysis_type == "Market Analysis":
        st.header("💰 Market Analysis")
        
        # Market trends
        analyzer = PlayerAnalyzer()
        trends = analyzer.analyze_market_trends(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Value vs Performance")
            scatter_fig = create_value_vs_performance_scatter(df)
            st.plotly_chart(scatter_fig, use_container_width=True)
        
        with col2:
            st.subheader("Correlation Analysis")
            corr_fig = create_correlation_heatmap(df)
            st.plotly_chart(corr_fig, use_container_width=True)
        
        # Undervalued players
        st.subheader("💎 Potentially Undervalued Players")
        undervalued = analyzer.identify_undervalued_players(df)
        st.dataframe(undervalued)
    
    elif analysis_type == "Performance Prediction":
        st.header("🔮 Performance Prediction")
        
        # Train predictor
        predictor = PlayerValuePredictor()
        
        with st.spinner("Training machine learning model..."):
            metrics = predictor.train(df)
        
        # Display model performance
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model R²", f"{metrics['r2']:.3f}")
        with col2:
            st.metric("MAE (€M)", f"{metrics['mae']/1000000:.1f}")
        with col3:
            st.metric("Test Samples", metrics['test_size'])
        
        # Feature importance
        st.subheader("📈 Feature Importance")
        importance_df = predictor.get_feature_importance()
        st.bar_chart(importance_df.set_index('feature')['importance'])
        
        # Make prediction for selected player
        st.subheader("🎯 Player Value Prediction")
        selected_player = st.selectbox("Select Player for Prediction", df['long_name'].dropna().unique())
        
        if selected_player:
            player_data = df[df['long_name'] == selected_player].iloc[0]
            
            # Extract features
            features = [
                player_data['overall'], player_data['potential'], player_data['age'],
                player_data['pace'], player_data['shooting'], player_data['passing'],
                player_data['dribbling'], player_data['defending'], player_data['physic'],
                player_data['height_cm'], player_data['weight_kg'],
                player_data['weak_foot'], player_data['skill_moves']
            ]
            
            predicted_value = predictor.predict(features)
            actual_value = player_data['value_eur']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Actual Value", f"€{actual_value/1000000:.1f}M")
            with col2:
                st.metric("Predicted Value", f"€{predicted_value/1000000:.1f}M")
            with col3:
                difference = abs(predicted_value - actual_value) / max(actual_value, 1) * 100
                st.metric("Prediction Error", f"{difference:.1f}%")
    
    elif analysis_type == "League Comparison":
        st.header("🏟️ League Analysis")
        
        # League comparison charts
        league_fig = create_league_comparison_chart(df)
        st.plotly_chart(league_fig, use_container_width=True)
        
        # Position analysis
        st.subheader("📍 Position Analysis")
        position_fig = create_position_analysis_chart(df)
        st.plotly_chart(position_fig, use_container_width=True)

if __name__ == "__main__":
    main()
