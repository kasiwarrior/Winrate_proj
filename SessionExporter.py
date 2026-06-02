import os
import glob
import pandas as pd

# ==========================================
# SETTINGS
# ==========================================
FOLDER_PATH = "Data/match/"                     # The folder where your scraped player files are
OUTPUT_DIR = "Data/Sessions/SessionGames"       # The folder where the new files will go
SESSION_THRESHOLD_MS = 2 * 60 * 60 * 1000       # 2 hours in milliseconds

print(f"Scanning folder: {FOLDER_PATH} for CSV files...")

# Find all CSV files in the folder
file_pattern = os.path.join(FOLDER_PATH, "*.csv")
match_files = glob.glob(file_pattern)

print(f"Found {len(match_files)} player files. Processing...")

# Create the output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

session_count = 0
processed_count = 0

for file in match_files:
    try:
        # Load the player's match data
        df = pd.read_csv(file)
        
        # Validate that the file isn't empty and has the columns we need
        if df.empty or 'game_start_timestamp' not in df.columns or 'win' not in df.columns or 'puuid' not in df.columns:
            continue
            
        # 1. Sort chronologically (oldest game first)
        df = df.sort_values(by='game_start_timestamp').reset_index(drop=True)
        
        # 2. Extract player ID
        player_id = df['puuid'].iloc[0]
        
        # 3. Calculate time differences between games
        df['time_diff'] = df['game_start_timestamp'].diff()
        
        # 4. Mark new sessions (True if gap > 2 hours OR if it's the very first game)
        df['is_new_session'] = (df['time_diff'] > SESSION_THRESHOLD_MS) | df['time_diff'].isna()
        
        # 5. Create a session ID (1, 2, 3...)
        df['session_id'] = df['is_new_session'].cumsum()
        
        # 6. Group by session and save each session to its own file
        grouped_sessions = df.groupby('session_id')
        
        for session_id, session_df in grouped_sessions:
            # Remove the temporary columns we added
            session_df = session_df.drop(columns=['time_diff', 'is_new_session', 'session_id'])
            
            # Create a filename with player ID and session number
            filename = f"player_{player_id}_session_{session_id:03d}.csv"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Save the full session data to CSV
            session_df.to_csv(filepath, index=False)
            session_count += 1
        
        processed_count += 1
        print(f"Processed: {player_id} ({len(grouped_sessions)} sessions)")
        
    except Exception as e:
        print(f"Error processing {file}: {e}")

print(f"\nSUCCESS! Processed {processed_count} players.")
print(f"Saved {session_count} total sessions to: {OUTPUT_DIR}")
