"""
FIFA Dashboard Demo Script
Test the basic functionality and data loading
"""

import pandas as pd
import numpy as np
import sys
import os

def test_data_loading():
    """Test if data can be loaded successfully"""
    print("🔍 Testing data loading...")
    
    try:
        # Load male players data
        male_players = pd.read_csv('data/male_players.csv')
        print(f"✅ Male players loaded: {len(male_players):,} records")
        
        # Load female players data  
        female_players = pd.read_csv('data/female_players.csv')
        print(f"✅ Female players loaded: {len(female_players):,} records")
        
        # Combine datasets
        all_players = pd.concat([male_players, female_players], ignore_index=True)
        print(f"✅ Combined dataset: {len(all_players):,} total players")
        
        return all_players
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def test_data_quality(df):
    """Test data quality and show basic statistics"""
    print("\n📊 Data Quality Check...")
    
    # Basic info
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    
    # Key columns check
    key_columns = ['player_id', 'long_name', 'overall', 'potential', 'value_eur']
    missing_cols = [col for col in key_columns if col not in df.columns]
    
    if missing_cols:
        print(f"❌ Missing key columns: {missing_cols}")
    else:
        print("✅ All key columns present")
    
    # Data completeness
    print("\n📈 Data Completeness:")
    for col in key_columns:
        if col in df.columns:
            completeness = (1 - df[col].isna().sum() / len(df)) * 100
            print(f"  {col}: {completeness:.1f}% complete")
    
    # Sample statistics
    if 'overall' in df.columns:
        print(f"\n⚽ Player Statistics:")
        print(f"  Average Overall: {df['overall'].mean():.1f}")
        print(f"  Best Player: {df.loc[df['overall'].idxmax(), 'long_name']} ({df['overall'].max()})")
        print(f"  Age range: {df['age'].min()}-{df['age'].max()}")

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 
        'sklearn', 'seaborn', 'matplotlib'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")

def create_sample_visualization():
    """Create a sample visualization to test plotting"""
    print("\n📊 Testing visualization capabilities...")
    
    try:
        import matplotlib.pyplot as plt
        
        # Simple test plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        plt.figure(figsize=(8, 4))
        plt.plot(x, y)
        plt.title('Sample Plot - Libraries Working')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.grid(True)
        plt.savefig('test_plot.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        print("✅ Matplotlib visualization test passed")
        
        # Test Plotly
        import plotly.graph_objects as go
        
        fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[1, 3, 2]))
        fig.update_layout(title='Sample Plotly Chart')
        fig.write_html('test_plotly.html')
        
        print("✅ Plotly visualization test passed")
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")

def main():
    """Main demo function"""
    print("🚀 FIFA Dashboard Demo")
    print("=" * 50)
    
    # Test dependencies
    test_dependencies()
    
    # Test data loading
    df = test_data_loading()
    
    if df is not None:
        # Test data quality
        test_data_quality(df)
        
        # Test visualizations
        create_sample_visualization()
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"📁 Ready to run: streamlit run app.py")
        print(f"🌐 Dashboard will be available at: http://localhost:8501")
        
    else:
        print("\n❌ Demo failed - please check data files")

if __name__ == "__main__":
    main()
