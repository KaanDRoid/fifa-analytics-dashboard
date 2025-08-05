# FIFA Analytics Dashboard Sample Data

This folder contains FIFA player data. Actual data files are not included in GitHub due to size constraints.

## Required Data Files

The following CSV files are needed for the project to function:

- `male_players.csv` - Male player statistics
- `female_players.csv` - Female player statistics
- `male_teams.csv` - Male team information (optional)
- `female_teams.csv` - Female team information (optional)
- `male_coaches.csv` - Male coach information (optional)
- `female_coaches.csv` - Female coach information (optional)

## Data Format

CSV files should contain the following columns:

### Required Columns
- `player_id`: Unique player identifier
- `long_name`: Player name
- `overall`: Overall rating (0-100)
- `potential`: Potential rating (0-100)
- `value_eur`: Market value (Euro)
- `age`: Age
- `pace`, `shooting`, `passing`, `dribbling`, `defending`, `physic`: Skill ratings
- `club_name`: Current club
- `player_positions`: Playing positions
- `nationality_name`: Nationality
- `league_name`: Current league

### Optional Columns
- `wage_eur`: Wage
- `height_cm`: Height
- `weight_kg`: Weight
- `preferred_foot`: Preferred foot
- `weak_foot`: Weak foot rating
- `skill_moves`: Skill moves rating

## Data Sources

You can obtain data files from the following sources:
- [FIFA 23 Complete Player Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset) - Kaggle (Primary source used)
- EA Sports FIFA databases
- Other Kaggle FIFA datasets

