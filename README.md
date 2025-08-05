# FIFA Analytics Dashboard

A modern, interactive FIFA player analytics dashboard built with Python, inspired by [FifaDash](https://github.com/EkremBayar/FifaDash). This project demonstrates how to create advanced football analytics using Python's powerful data science ecosystem with enhanced features and machine learning capabilities.

## Features

### Core Analytics
- **Interactive Player Statistics**: Comprehensive player performance metrics
- **Advanced Visualizations**: Radar charts, heatmaps, and dynamic plots
- **Multi-dimensional Filtering**: Filter by position, league, age, nationality, and more
- **Comparative Analysis**: Side-by-side player comparisons

### Enhanced Features
- **Machine Learning Predictions**: Player value estimation and potential growth forecasting
- **Clustering Analysis**: Player similarity analysis using K-means clustering
- **Performance Insights**: Advanced metrics and performance indicators
- **Real-time Data Processing**: Efficient data handling for large datasets

### Modern UI/UX
- **Responsive Design**: Clean, modern interface built with Streamlit
- **Interactive Elements**: Dynamic charts with Plotly
- **User-friendly Navigation**: Intuitive dashboard layout
- **Mobile-responsive**: Works seamlessly across devices

## Technology Stack

- **Data Processing**: `pandas`, `numpy`
- **Visualization**: `plotly`, `matplotlib`, `seaborn`
- **Web Framework**: `streamlit`
- **Machine Learning**: `scikit-learn`
- **Statistical Analysis**: `scipy`, `statsmodels`

## Data Structure

The dashboard supports both male and female player data with comprehensive attributes based on the [FIFA 23 Complete Player Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset):
- Player demographics and physical attributes
- Technical skills (pace, shooting, passing, dribbling, defending, physic)
- Detailed skill breakdowns (70+ attributes)
- Club and national team information
- Market values and contract details

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/KaanDRoid/fifa-analytics-dashboard.git
   cd fifa-analytics-dashboard
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## Usage

### Dashboard Navigation
1. **Home**: Overview and key statistics
2. **Player Explorer**: Detailed player analysis and comparison
3. **Team Analytics**: Club and national team insights
4. **Market Analysis**: Transfer values and market trends
5. **ML Predictions**: Machine learning-powered insights

### Key Features
- **Search Players**: Find players by name, position, or club
- **Filter & Compare**: Advanced filtering options and side-by-side comparisons
- **Interactive Charts**: Click and explore data dynamically
- **Export Data**: Download filtered data and visualizations

## Machine Learning Features

### Player Value Prediction
- Predicts market value based on player attributes
- Uses ensemble methods for improved accuracy
- Provides confidence intervals for predictions

### Player Clustering
- Groups similar players using K-means clustering
- Identifies playing styles and tactical roles
- Suggests transfer targets and alternatives

### Performance Analysis
- Calculates advanced performance metrics
- Identifies over/underperforming players
- Provides development recommendations

## Sample Visualizations

The dashboard includes various chart types:
- **Radar Charts**: Player skill comparison
- **Scatter Plots**: Attribute relationships
- **Heatmaps**: League and position analysis
- **Time Series**: Career progression tracking
- **Geographic Maps**: Player distribution by country

## Project Inspiration

This project was inspired by the excellent work on [FifaDash](https://github.com/EkremBayar/FifaDash) by EkremBayar. While the original was built with R Shiny, this Python implementation adds:

- Enhanced machine learning capabilities
- Modern web interface with Streamlit
- Advanced statistical analysis
- Improved performance and scalability
- Additional visualization types

## Future Enhancements

- [ ] Real-time data integration via APIs
- [ ] Advanced ML models (neural networks, XGBoost)
- [ ] Player career trajectory prediction
- [ ] Team formation optimization
- [ ] Social sentiment analysis integration
- [ ] Mobile app development

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [EkremBayar](https://github.com/EkremBayar) for the original FifaDash inspiration
- EA Sports for FIFA data
- Streamlit community for excellent documentation
- Python data science community

## Contact

For questions or suggestions, feel free to reach out or open an issue.

---

**If you find this project helpful, please consider giving it a star!**
