# FIFA Analytics Dashboard - Setup Guide

## Project Structure

```
fifa_dash/
│
├── data/                          # Data directory
│   ├── female_players.csv         
│   ├── male_players.csv          
│   ├── female_teams.csv          
│   ├── male_teams.csv            
│   ├── female_coaches.csv        
│   └── male_coaches.csv          
│
├── utils/                         # Utility modules
│   ├── __init__.py               # Package initializer
│   ├── analytics.py              # Advanced analytics functions
│   └── visualizations.py         # Custom visualization functions
│
├── app.py                        # Main dashboard application
├── advanced_analytics.py         # Advanced analytics dashboard
├── tactical_analysis.py          # Tactical analysis dashboard
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── LICENSE                       # MIT License
└── setup_guide.md               # This setup guide
```

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- Git (for cloning repository)
- Virtual environment (recommended)

### 2. Environment Setup

#### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Data Preparation

Ensure your data directory contains the required CSV files:
- `male_players.csv` - Male player statistics
- `female_players.csv` - Female player statistics

**Required CSV columns:**
- `player_id`: Unique player identifier
- `long_name`: Full player name
- `overall`: Overall rating (0-100)
- `potential`: Potential rating (0-100)
- `value_eur`: Market value in Euros
- `age`: Player age
- `pace`, `shooting`, `passing`, `dribbling`, `defending`, `physic`: Skill ratings
- `club_name`: Current club
- `player_positions`: Playing positions
- `nationality_name`: Player nationality
- `league_name`: Current league

### 4. Running the Application

#### Main Dashboard
```bash
streamlit run app.py
```

#### Advanced Analytics
```bash
streamlit run advanced_analytics.py
```

#### Tactical Analysis
```bash
streamlit run tactical_analysis.py
```

### 5. Application URLs

Once running, access the dashboards at:
- **Main Dashboard**: http://localhost:8501
- **Advanced Analytics**: http://localhost:8502 (if running separately)
- **Tactical Analysis**: http://localhost:8503 (if running separately)

## Features Overview

### Main Dashboard (`app.py`)
- **Overview Tab**: Key statistics and distributions
- **Player Analysis**: Individual player deep dive
- **Comparison**: Side-by-side player comparisons
- **ML Insights**: Machine learning predictions and clustering

### Advanced Analytics (`advanced_analytics.py`)
- **Player Insights**: Comprehensive player reports
- **Market Analysis**: Value trends and undervalued players
- **Performance Prediction**: ML-based value prediction
- **League Comparison**: Cross-league analysis

### Tactical Analysis (`tactical_analysis.py`)
- **Player Clustering**: Behavioral player grouping
- **Formation Analysis**: Best players for formations
- **Team Builder**: Custom team creation and analysis

## Customization Options

### Adding New Visualizations
1. Create new functions in `utils/visualizations.py`
2. Import and use in main application files
3. Follow Plotly/Streamlit conventions

### Extending Analytics
1. Add new analysis functions to `utils/analytics.py`
2. Implement new ML models or statistical methods
3. Update main application to include new features

### Data Sources
- Update data loading functions in each app file
- Ensure new data follows the expected schema
- Add data validation for new columns

## Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

#### Data Loading Errors
- Verify CSV file paths and names
- Check CSV encoding (should be UTF-8)
- Ensure required columns exist

#### Memory Issues
- Reduce data size by filtering
- Use data sampling for large datasets
- Consider using `st.cache_data` for optimization

#### Port Conflicts
```bash
# Run on different ports
streamlit run app.py --server.port 8504
```

### Performance Optimization

#### Data Caching
- Use `@st.cache_data` for expensive operations
- Clear cache when data changes: `st.cache_data.clear()`

#### Large Datasets
- Implement data pagination
- Use lazy loading for visualizations
- Consider data preprocessing

## Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

### Testing
- Test with different data sizes
- Validate filtering functionality
- Check visualization rendering
- Test error handling

### Version Control
- Use meaningful commit messages
- Create feature branches
- Test before merging to main

## Deployment Options

### Local Development
- Use built-in Streamlit server
- Perfect for testing and development

### Cloud Deployment
- **Streamlit Cloud**: Connect GitHub repository
- **Heroku**: Use Procfile and requirements.txt
- **Docker**: Create containerized deployment

### Production Considerations
- Environment variables for configuration
- Error logging and monitoring
- Database integration for large datasets
- User authentication if needed

## Support and Contributing

### Getting Help
- Check existing issues and documentation
- Create detailed issue reports
- Provide sample data and error logs

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request with description

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Guide](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)

---

For more information, see the main [README.md](README.md) file.
