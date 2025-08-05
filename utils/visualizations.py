import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_advanced_radar_chart(player_data, comparison_player=None):
    """Create an advanced radar chart with optional comparison"""
    
    # Define skill categories
    skills = {
        'Pace': 'pace',
        'Shooting': 'shooting', 
        'Passing': 'passing',
        'Dribbling': 'dribbling',
        'Defending': 'defending',
        'Physical': 'physic'
    }
    
    # Extract values
    categories = list(skills.keys())
    values = [player_data[skill] for skill in skills.values()]
    
    fig = go.Figure()
    
    # Add main player
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player_data['long_name'],
        line=dict(color='#1f77b4', width=2),
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    # Add comparison player if provided
    if comparison_player is not None:
        comp_values = [comparison_player[skill] for skill in skills.values()]
        fig.add_trace(go.Scatterpolar(
            r=comp_values,
            theta=categories,
            fill='toself',
            name=comparison_player['long_name'],
            line=dict(color='#ff7f0e', width=2),
            fillcolor='rgba(255, 127, 14, 0.3)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=12)
            )
        ),
        showlegend=True,
        title=dict(
            text="Player Skills Comparison" if comparison_player else f"{player_data['long_name']} - Skills",
            x=0.5,
            font=dict(size=16)
        ),
        height=500
    )
    
    return fig

def create_value_vs_performance_scatter(df, position_filter=None):
    """Create scatter plot of value vs performance metrics"""
    
    # Filter by position if specified
    if position_filter and position_filter != 'All':
        df_filtered = df[df['player_positions'].str.contains(position_filter, na=False)]
    else:
        df_filtered = df
    
    # Sample data for performance
    sample_size = min(1000, len(df_filtered))
    df_sample = df_filtered.sample(sample_size)
    
    fig = px.scatter(
        df_sample,
        x='overall',
        y='value_eur',
        color='age',
        size='potential',
        hover_data=['long_name', 'club_name', 'player_positions'],
        title='Player Value vs Overall Rating',
        labels={
            'overall': 'Overall Rating',
            'value_eur': 'Market Value (€)',
            'age': 'Age',
            'potential': 'Potential'
        },
        color_continuous_scale='viridis'
    )
    
    fig.update_traces(marker=dict(opacity=0.7))
    fig.update_layout(height=500)
    
    return fig

def create_age_distribution_chart(df):
    """Create age distribution with performance overlay"""
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Age Distribution', 'Performance by Age'),
        vertical_spacing=0.1
    )
    
    # Age histogram
    fig.add_trace(
        go.Histogram(x=df['age'], nbinsx=20, name='Age Distribution'),
        row=1, col=1
    )
    
    # Performance by age (box plot)
    fig.add_trace(
        go.Box(x=df['age'], y=df['overall'], name='Overall Rating'),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        title_text="Age Analysis",
        showlegend=False
    )
    
    return fig

def create_position_analysis_chart(df):
    """Create position-based analysis chart"""
    
    # Get top positions by player count
    position_counts = df['player_positions'].value_counts().head(10)
    
    # Calculate average stats for each position
    position_stats = []
    for position in position_counts.index:
        pos_players = df[df['player_positions'] == position]
        stats = {
            'position': position,
            'count': len(pos_players),
            'avg_overall': pos_players['overall'].mean(),
            'avg_value': pos_players['value_eur'].mean(),
            'avg_age': pos_players['age'].mean()
        }
        position_stats.append(stats)
    
    stats_df = pd.DataFrame(position_stats)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Player Count by Position', 'Average Overall Rating', 
                       'Average Market Value', 'Average Age'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Player count
    fig.add_trace(
        go.Bar(x=stats_df['position'], y=stats_df['count'], name='Count'),
        row=1, col=1
    )
    
    # Average overall
    fig.add_trace(
        go.Bar(x=stats_df['position'], y=stats_df['avg_overall'], name='Overall'),
        row=1, col=2
    )
    
    # Average value
    fig.add_trace(
        go.Bar(x=stats_df['position'], y=stats_df['avg_value'], name='Value'),
        row=2, col=1
    )
    
    # Average age
    fig.add_trace(
        go.Bar(x=stats_df['position'], y=stats_df['avg_age'], name='Age'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Position Analysis",
        showlegend=False
    )
    
    # Update x-axis for all subplots
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(tickangle=45, row=i, col=j)
    
    return fig

def create_league_comparison_chart(df, top_n=10):
    """Create league comparison chart"""
    
    # Get top leagues by player count
    league_stats = df.groupby('league_name').agg({
        'player_id': 'count',
        'overall': 'mean',
        'value_eur': 'mean',
        'age': 'mean'
    }).round(2)
    
    league_stats.columns = ['player_count', 'avg_overall', 'avg_value', 'avg_age']
    league_stats = league_stats.sort_values('player_count', ascending=False).head(top_n)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Player Count', 'Average Overall Rating', 
                       'Average Market Value (€)', 'Average Age'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Player count
    fig.add_trace(
        go.Bar(y=league_stats.index, x=league_stats['player_count'], 
               orientation='h', name='Count'),
        row=1, col=1
    )
    
    # Average overall
    fig.add_trace(
        go.Bar(y=league_stats.index, x=league_stats['avg_overall'], 
               orientation='h', name='Overall'),
        row=1, col=2
    )
    
    # Average value
    fig.add_trace(
        go.Bar(y=league_stats.index, x=league_stats['avg_value'], 
               orientation='h', name='Value'),
        row=2, col=1
    )
    
    # Average age
    fig.add_trace(
        go.Bar(y=league_stats.index, x=league_stats['avg_age'], 
               orientation='h', name='Age'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700,
        title_text=f"Top {top_n} Leagues Comparison",
        showlegend=False
    )
    
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap for key attributes"""
    
    # Select numerical columns for correlation
    corr_cols = ['overall', 'potential', 'value_eur', 'age', 'pace', 
                'shooting', 'passing', 'dribbling', 'defending', 'physic']
    
    # Calculate correlation matrix
    corr_matrix = df[corr_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Correlation Matrix - Key Attributes',
        height=500,
        width=500
    )
    
    return fig

def create_performance_evolution_chart(df, player_name):
    """Create performance evolution chart for a player across FIFA versions"""
    
    player_data = df[df['long_name'] == player_name]
    
    if len(player_data) == 0:
        return None
    
    # Sort by FIFA version
    player_data = player_data.sort_values('fifa_version')
    
    fig = go.Figure()
    
    # Overall rating evolution
    fig.add_trace(go.Scatter(
        x=player_data['fifa_version'],
        y=player_data['overall'],
        mode='lines+markers',
        name='Overall Rating',
        line=dict(color='#1f77b4', width=3)
    ))
    
    # Potential evolution
    fig.add_trace(go.Scatter(
        x=player_data['fifa_version'],
        y=player_data['potential'],
        mode='lines+markers',
        name='Potential',
        line=dict(color='#ff7f0e', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=f"{player_name} - Performance Evolution",
        xaxis_title="FIFA Version",
        yaxis_title="Rating",
        height=400,
        hovermode='x unified'
    )
    
    return fig
