import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib
import warnings
warnings.filterwarnings('ignore')

class PlayerValuePredictor:
    """
    Advanced player value prediction using ensemble methods
    """
    
    def __init__(self):
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_cols = [
            'overall', 'potential', 'age', 'pace', 'shooting', 
            'passing', 'dribbling', 'defending', 'physic',
            'height_cm', 'weight_kg', 'weak_foot', 'skill_moves'
        ]
        self.is_trained = False
    
    def prepare_data(self, df):
        """Prepare data for training"""
        # Select features and target
        X = df[self.feature_cols].copy()
        y = df['value_eur'].copy()
        
        # Remove outliers (values > 200M or < 0)
        mask = (y > 0) & (y < 200000000) & X.notna().all(axis=1)
        X = X[mask]
        y = y[mask]
        
        return X, y
    
    def train(self, df):
        """Train the ensemble model"""
        X, y = self.prepare_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        self.rf_model.fit(X_train_scaled, y_train)
        self.gb_model.fit(X_train_scaled, y_train)
        
        # Make predictions
        rf_pred = self.rf_model.predict(X_test_scaled)
        gb_pred = self.gb_model.predict(X_test_scaled)
        
        # Ensemble prediction (weighted average)
        ensemble_pred = 0.6 * rf_pred + 0.4 * gb_pred
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, ensemble_pred)
        r2 = r2_score(y_test, ensemble_pred)
        rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))
        
        self.is_trained = True
        
        return {
            'mae': mae,
            'r2': r2,
            'rmse': rmse,
            'test_size': len(y_test)
        }
    
    def predict(self, player_features):
        """Predict player value"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        # Scale features
        features_scaled = self.scaler.transform([player_features])
        
        # Make predictions
        rf_pred = self.rf_model.predict(features_scaled)[0]
        gb_pred = self.gb_model.predict(features_scaled)[0]
        
        # Ensemble prediction
        ensemble_pred = 0.6 * rf_pred + 0.4 * gb_pred
        
        return ensemble_pred
    
    def get_feature_importance(self):
        """Get feature importance from Random Forest"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        importance = self.rf_model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'feature': self.feature_cols,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance_df

class PlayerAnalyzer:
    """
    Advanced player analysis and comparison tools
    """
    
    @staticmethod
    def calculate_performance_index(player_data):
        """Calculate a comprehensive performance index"""
        # Weight different attributes based on position
        position = player_data.get('player_positions', '')
        
        if 'GK' in position:
            # Goalkeeper weights
            weights = {
                'goalkeeping_diving': 0.2,
                'goalkeeping_handling': 0.2,
                'goalkeeping_kicking': 0.15,
                'goalkeeping_positioning': 0.2,
                'goalkeeping_reflexes': 0.25
            }
        elif any(pos in position for pos in ['CB', 'LB', 'RB', 'LWB', 'RWB']):
            # Defender weights
            weights = {
                'defending': 0.3,
                'physic': 0.2,
                'pace': 0.2,
                'passing': 0.2,
                'dribbling': 0.1
            }
        elif any(pos in position for pos in ['CM', 'CDM', 'CAM']):
            # Midfielder weights
            weights = {
                'passing': 0.3,
                'dribbling': 0.25,
                'defending': 0.15,
                'physic': 0.15,
                'shooting': 0.15
            }
        else:
            # Forward/Winger weights
            weights = {
                'shooting': 0.3,
                'pace': 0.25,
                'dribbling': 0.25,
                'passing': 0.1,
                'physic': 0.1
            }
        
        # Calculate weighted score
        performance_index = 0
        total_weight = 0
        
        for attribute, weight in weights.items():
            if attribute in player_data and pd.notna(player_data[attribute]):
                performance_index += player_data[attribute] * weight
                total_weight += weight
        
        if total_weight > 0:
            performance_index /= total_weight
        
        return performance_index
    
    @staticmethod
    def find_similar_players(df, target_player_id, n_similar=5):
        """Find similar players using cosine similarity"""
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Select numerical features for similarity
        feature_cols = [
            'overall', 'pace', 'shooting', 'passing', 
            'dribbling', 'defending', 'physic', 'age'
        ]
        
        # Get target player data
        target_player = df[df['player_id'] == target_player_id]
        if target_player.empty:
            return pd.DataFrame()
        
        target_features = target_player[feature_cols].values
        
        # Get all players' features
        all_features = df[feature_cols].dropna()
        similarities = cosine_similarity(target_features, all_features)[0]
        
        # Get most similar players (excluding the target player)
        similar_indices = similarities.argsort()[-n_similar-1:-1][::-1]
        similar_players = df.loc[all_features.index[similar_indices]]
        
        # Add similarity scores
        similar_players = similar_players.copy()
        similar_players['similarity_score'] = similarities[similar_indices]
        
        return similar_players[['long_name', 'club_name', 'overall', 'value_eur', 'similarity_score']]
    
    @staticmethod
    def analyze_market_trends(df):
        """Analyze market value trends by various factors"""
        trends = {}
        
        # Age trend
        age_trend = df.groupby('age')['value_eur'].mean()
        trends['age'] = age_trend
        
        # Overall rating trend
        overall_trend = df.groupby('overall')['value_eur'].mean()
        trends['overall'] = overall_trend
        
        # Position trend
        position_trend = df.groupby('player_positions')['value_eur'].mean().sort_values(ascending=False)
        trends['position'] = position_trend.head(10)
        
        # League trend
        league_trend = df.groupby('league_name')['value_eur'].mean().sort_values(ascending=False)
        trends['league'] = league_trend.head(10)
        
        return trends
    
    @staticmethod
    def identify_undervalued_players(df, threshold=0.8):
        """Identify potentially undervalued players based on performance vs value"""
        # Calculate value per overall point
        df_copy = df.copy()
        df_copy['value_per_overall'] = df_copy['value_eur'] / df_copy['overall']
        
        # Find players with low value relative to their overall rating
        median_value_per_overall = df_copy['value_per_overall'].median()
        undervalued = df_copy[
            df_copy['value_per_overall'] < median_value_per_overall * threshold
        ]
        
        # Sort by overall rating (descending) and value (ascending)
        undervalued = undervalued.sort_values(['overall', 'value_eur'], ascending=[False, True])
        
        return undervalued[['long_name', 'club_name', 'overall', 'value_eur', 'value_per_overall']].head(20)

def generate_player_report(df, player_id):
    """Generate a comprehensive player report"""
    player_data = df[df['player_id'] == player_id].iloc[0]
    analyzer = PlayerAnalyzer()
    
    report = {
        'basic_info': {
            'name': player_data['long_name'],
            'club': player_data['club_name'],
            'position': player_data['player_positions'],
            'age': player_data['age'],
            'nationality': player_data['nationality_name']
        },
        'ratings': {
            'overall': player_data['overall'],
            'potential': player_data['potential'],
            'performance_index': analyzer.calculate_performance_index(player_data)
        },
        'market_info': {
            'value': player_data['value_eur'],
            'wage': player_data['wage_eur']
        },
        'similar_players': analyzer.find_similar_players(df, player_id),
        'strengths_weaknesses': {
            'pace': player_data['pace'],
            'shooting': player_data['shooting'],
            'passing': player_data['passing'],
            'dribbling': player_data['dribbling'],
            'defending': player_data['defending'],
            'physic': player_data['physic']
        }
    }
    
    return report
