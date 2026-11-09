# Data

Put the FIFA player CSVs in this folder. They are not tracked in git because of their size.

## Required Data Files

The apps read these files:

- `male_players.csv` - Male player statistics
- `female_players.csv` - Female player statistics

## Data Format

The code uses the following columns:

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

### Also used when present
- `wage_eur`: Wage
- `height_cm`: Height
- `weight_kg`: Weight
- `preferred_foot`: Preferred foot
- `weak_foot`: Weak foot rating
- `skill_moves`: Skill moves rating

## Source

[FIFA 23 Complete Player Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset) on Kaggle. The dataset also ships team and coach files, which the apps do not use.
