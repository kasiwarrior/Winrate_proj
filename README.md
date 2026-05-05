# Winrate_proj

A Python data science project for collecting, preprocessing, validating, and visualizing win rate data from game match and player datasets.

## Project Structure

- `Datacollection.ipynb` - Notebook for gathering and saving raw match and player data.
- `DataPreprocessor.ipynb` - Notebook for cleaning and transforming the collected data.
- `DataProcessor.ipynb` - Notebook for feature engineering and preparing data for analysis.
- `DataValidator.ipynb` - Notebook for validating dataset quality and consistency.
- `Visualizations.ipynb` - Notebook for exploring win rate trends and visual patterns.
- `Data/` - Data directory containing raw and processed CSV files.
  - `player_master_list.csv` - Master list of player metadata.
  - `Downloaded/` - Downloaded dataset files, including `match_ids.csv`, `matchData.csv`, and player-specific CSV exports.
  - `match/` - Individual player match data CSV files.

## Requirements

- Python 3.x
- Jupyter Notebook or JupyterLab
- Common data science libraries like `pandas`, `numpy`, and `matplotlib` / `seaborn`

## Notes

- The project relies on CSV files stored under `Data/`.
- If the raw files are not present, regenerate them using the data collection notebook.

## License


