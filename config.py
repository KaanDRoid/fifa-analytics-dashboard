# FIFA Analytics Dashboard Configuration

# Data Settings
DATA_PATH = "data/"
MALE_PLAYERS_FILE = "male_players.csv"
FEMALE_PLAYERS_FILE = "female_players.csv"
SAMPLE_SIZE = 1000  # For large datasets, sample for performance

# Dashboard Settings
DEFAULT_PORT = 8501
ADVANCED_PORT = 8502
TACTICAL_PORT = 8503

# Performance Settings
CACHE_TTL = 3600  # Cache time-to-live in seconds
MAX_ROWS_DISPLAY = 100  # Maximum rows to display in tables
CHART_HEIGHT = 500  # Default chart height
CHART_WIDTH = 700   # Default chart width

# ML Model Settings
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_CLUSTERS_DEFAULT = 6
MIN_OVERALL_RATING = 60

# UI Settings
SIDEBAR_WIDTH = 300
MAIN_TITLE = "⚽ FIFA Analytics Dashboard"
THEME_COLOR = "#1f77b4"

# Feature Flags
ENABLE_ML_PREDICTIONS = True
ENABLE_CLUSTERING = True
ENABLE_ADVANCED_VISUALIZATIONS = True
ENABLE_EXPORT_FEATURES = True
