import pandas as pd
import streamlit

import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# Define the expected columns for the worship song database
EXPECTED_COLUMNS = [
    'Id', 'Title', 'CCLI', 'Themes', 'Notes', 'Last Scheduled Data', 'Song Tag 1',
    'Arrangement 1 Name', 'Arrangement 1 BPM', 'Arrangement 1 Length', 'Arrangement 1 Notes',
    'Arrangement 1 Keys', 'Arrangement 1 Chord Chart', 'Arrangement 1 Chord Chart Key',
    'Arrangement 1 Tag 1', 'Arrangement 1 Tag 2', 'Arrangement 2 Name', 'Arrangement 2 BPM',
    'Arrangement 2 Length.', 'Arrangement 2 Notes', 'Arrangement 2 Keys', 'Arrangement 2 Chord Chart',
    'Arrangement 2 Chord Chart Key'
]


def load_songs_database(file_path):
    """Load songs from CSV file"""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"CSV file '{file_path}' not found. Please make sure the file exists.")
        return None
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return None


def validate_columns(df):
    """Check if the dataframe has the expected columns"""
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in EXPECTED_COLUMNS]

    if missing_columns:
        st.warning(f"Missing expected columns: {', '.join(missing_columns)}")
    if extra_columns:
        st.info(f"Extra columns found: {', '.join(extra_columns)}")

    return len(missing_columns) == 0


def select_random_songs(df, num_songs):
    """Randomly select specified number of songs from dataframe"""
    if len(df) < num_songs:
        st.warning(f"Only {len(df)} songs available in database. Showing all songs.")
        return df

    return df.sample(n=num_songs, random_state=random.randint(1, 10000))


def display_song_card(song, index):
    """Display a single song in a card format"""
    with st.container():
        st.markdown(f"### 🎵 Song {index}")

        # Main song information
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**Title:** {song.get('Title', 'N/A')}")
            st.markdown(f"**CCLI:** {song.get('CCLI', 'N/A')}")
        with col2:
            st.markdown(f"**ID:** {song.get('Id', 'N/A')}")
            st.markdown(f"**Song Tag:** {song.get('Song Tag 1', 'N/A')}")
        with col3:
            last_scheduled = song.get('Last Scheduled Data', 'N/A')
            st.markdown(f"**Last Scheduled:** {last_scheduled}")

        # Themes and Notes
        if pd.notna(song.get('Themes')):
            st.markdown(f"**Themes:** {song['Themes']}")
        if pd.notna(song.get('Notes')):
            st.markdown(f"**Notes:** {song['Notes']}")

        # Arrangements
        arr1_col, arr2_col = st.columns(2)

        with arr1_col:
            if pd.notna(song.get('Arrangement 1 Name')):
                st.markdown("**🎼 Arrangement 1**")
                st.markdown(f"• **Name:** {song.get('Arrangement 1 Name', 'N/A')}")
                st.markdown(f"• **BPM:** {song.get('Arrangement 1 BPM', 'N/A')}")
                st.markdown(f"• **Length:** {song.get('Arrangement 1 Length', 'N/A')}")
                st.markdown(f"• **Keys:** {song.get('Arrangement 1 Keys', 'N/A')}")
                st.markdown(f"• **Chord Chart Key:** {song.get('Arrangement 1 Chord Chart Key', 'N/A')}")

                # Display chord chart content
                if pd.notna(song.get('Arrangement 1 Chord Chart')):
                    chord_chart = song.get('Arrangement 1 Chord Chart', '')
                    if chord_chart and str(chord_chart).strip().lower() not in ['', 'yes', 'no', 'true', 'false']:
                        st.markdown("• **Chord Chart:**")
                        st.code(chord_chart, language=None)
                    else:
                        st.markdown(f"• **Has Chord Chart:** {chord_chart}")

                tags = []
                if pd.notna(song.get('Arrangement 1 Tag 1')):
                    tags.append(song['Arrangement 1 Tag 1'])
                if pd.notna(song.get('Arrangement 1 Tag 2')):
                    tags.append(song['Arrangement 1 Tag 2'])
                if tags:
                    st.markdown(f"• **Tags:** {', '.join(tags)}")

                if pd.notna(song.get('Arrangement 1 Notes')):
                    st.markdown(f"• **Notes:** {song['Arrangement 1 Notes']}")

        with arr2_col:
            if pd.notna(song.get('Arrangement 2 Name')):
                st.markdown("**🎼 Arrangement 2**")
                st.markdown(f"• **Name:** {song.get('Arrangement 2 Name', 'N/A')}")
                st.markdown(f"• **BPM:** {song.get('Arrangement 2 BPM', 'N/A')}")
                st.markdown(f"• **Length:** {song.get('Arrangement 2 Length.', 'N/A')}")
                st.markdown(f"• **Keys:** {song.get('Arrangement 2 Keys', 'N/A')}")
                st.markdown(f"• **Chord Chart Key:** {song.get('Arrangement 2 Chord Chart Key', 'N/A')}")

                # Display chord chart content for Arrangement 2
                if pd.notna(song.get('Arrangement 2 Chord Chart')):
                    chord_chart = song.get('Arrangement 2 Chord Chart', '')
                    if chord_chart and str(chord_chart).strip().lower() not in ['', 'yes', 'no', 'true', 'false']:
                        st.markdown("• **Chord Chart:**")
                        st.code(chord_chart, language=None)
                    else:
                        st.markdown(f"• **Has Chord Chart:** {chord_chart}")

                if pd.notna(song.get('Arrangement 2 Notes')):
                    st.markdown(f"• **Notes:** {song['Arrangement 2 Notes']}")

        st.divider()


def filter_songs_by_theme(df, selected_themes):
    """Filter songs by themes"""
    if not selected_themes or 'All' in selected_themes:
        return df

    filtered_df = df[df['Themes'].str.contains('|'.join(selected_themes), case=False, na=False)]
    return filtered_df


def main():
    st.set_page_config(page_title="Worship Song Selector", page_icon="🎵", layout="wide")

    st.title("🎵 Worship Song Selector")
    st.write("Randomly select songs from your worship song database for service planning!")

    # Sidebar for file input and filters
    with st.sidebar:
        st.header("📁 Database Input")

        # File upload option
        uploaded_file = st.file_uploader("Upload your songs CSV file", type=['csv'])

        # Alternative: use a default file path
        csv_file_path = st.text_input("Or enter CSV file path:", value="worship_songs.csv")

    # Load the database
    df = None
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} songs from uploaded file!")
        validate_columns(df)
    elif csv_file_path and os.path.exists(csv_file_path):
        df = load_songs_database(csv_file_path)
        if df is not None:
            st.success(f"✅ Loaded {len(df)} songs from {csv_file_path}!")
            validate_columns(df)
    elif csv_file_path:
        st.info("📄 CSV file not found. Please upload a file or check the file path.")

    if df is not None:
        # Sidebar filters
        with st.sidebar:
            st.header("🔍 Filters")

            # Theme filter
            all_themes = []
            for themes in df['Themes'].dropna():
                if isinstance(themes, str):
                    all_themes.extend([theme.strip() for theme in themes.split(',')])
            unique_themes = ['All'] + sorted(list(set(all_themes)))

            selected_themes = st.multiselect(
                "Filter by Themes:",
                options=unique_themes,
                default=['All']
            )

            # Apply theme filter
            filtered_df = filter_songs_by_theme(df, selected_themes)

            if len(filtered_df) != len(df):
                st.info(f"Filtered to {len(filtered_df)} songs")

        # Main content area
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric("Total Songs", len(df))
        with col2:
            st.metric("Filtered Songs", len(filtered_df))
        with col3:
            songs_with_arr2 = len(filtered_df[filtered_df['Arrangement 2 Name'].notna()])
            st.metric("Songs with 2 Arrangements", songs_with_arr2)

        # Preview database
        with st.expander("📊 Preview Database"):
            st.dataframe(filtered_df.head(10))

        # Song selection
        st.header("🎲 Random Song Selection")

        col1, col2 = st.columns([2, 1])
        with col1:
            max_songs = len(filtered_df)
            num_songs = st.number_input(
                "How many songs would you like to select?",
                min_value=1,
                max_value=max_songs,
                value=min(3, max_songs),
                step=1
            )

        with col2:
            st.write("")  # spacing
            st.write("")  # spacing
            generate_button = st.button("🎲 Generate Song List", type="primary", use_container_width=True)

        # Generate random selection
        if generate_button and len(filtered_df) > 0:
            selected_songs = select_random_songs(filtered_df, num_songs)

            st.header(
                f"🎵 Your Random Song Selection ({len(selected_songs)} song{'s' if len(selected_songs) != 1 else ''})")

            # Display selected songs
            for idx, (_, song) in enumerate(selected_songs.iterrows(), 1):
                display_song_card(song, idx)

            # Download options
            st.header("📥 Export Options")
            col1, col2 = st.columns(2)

            with col1:
                # Full details CSV
                csv_data = selected_songs.to_csv(index=False)
                st.download_button(
                    label="📄 Download Full Details (CSV)",
                    data=csv_data,
                    file_name=f"selected_songs_full_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )

            with col2:
                # Summary CSV (key info only)
                summary_cols = ['Title', 'CCLI', 'Themes', 'Arrangement 1 Name', 'Arrangement 1 BPM',
                                'Arrangement 1 Keys', 'Arrangement 2 Name', 'Arrangement 2 BPM', 'Arrangement 2 Keys']
                summary_df = selected_songs[summary_cols]
                summary_csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📋 Download Summary (CSV)",
                    data=summary_csv,
                    file_name=f"selected_songs_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )

    # Instructions sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.write("""
        **How to use:**
        1. Upload your worship songs CSV file
        2. Use filters to narrow down song selection
        3. Choose number of songs to select
        4. Click "Generate Song List"
        5. Download the results for service planning

        **CSV Format:**
        Your CSV should have these columns:
        - Id, Title, CCLI, Themes, Notes
        - Last Scheduled Data, Song Tag 1
        - Arrangement 1 & 2 details (Name, BPM, Length, Keys, etc.)
        """)

        # Sample data generator
        if st.button("📝 Generate Sample CSV"):
            sample_data = {
                'Id': [1, 2, 3],
                'Title': ['Amazing Grace', 'How Great Thou Art', 'Blessed Be Your Name'],
                'CCLI': ['22025', '14181', '3798438'],
                'Themes': ['Grace, Redemption', 'Praise, Worship', 'Worship, Trust'],
                'Notes': ['Classic hymn', 'Traditional favorite', 'Contemporary worship'],
                'Last Scheduled Data': ['2024-01-15', '2024-02-03', '2024-01-28'],
                'Song Tag 1': ['Hymn', 'Hymn', 'Contemporary'],
                'Arrangement 1 Name': ['Traditional', 'Classic', 'Full Band'],
                'Arrangement 1 BPM': [80, 85, 78],
                'Arrangement 1 Length': ['4:30', '5:15', '4:45'],
                'Arrangement 1 Notes': ['Piano only', 'Organ preferred', 'Electric guitar lead'],
                'Arrangement 1 Keys': ['G', 'C', 'D'],
                'Arrangement 1 Chord Chart': ['Yes', 'Yes', 'Yes'],
                'Arrangement 1 Chord Chart Key': ['G', 'C', 'D'],
                'Arrangement 1 Tag 1': ['Slow', 'Medium', 'Medium'],
                'Arrangement 1 Tag 2': ['Reflective', 'Majestic', 'Uplifting'],
                'Arrangement 2 Name': ['', 'Modern', 'Acoustic'],
                'Arrangement 2 BPM': ['', 95, 72],
                'Arrangement 2 Length.': ['', '4:45', '5:00'],
                'Arrangement 2 Notes': ['', 'Contemporary style', 'Acoustic guitar focus'],
                'Arrangement 2 Keys': ['', 'D', 'C'],
                'Arrangement 2 Chord Chart': ['', 'Yes', 'Yes'],
                'Arrangement 2 Chord Chart Key': ['', 'D', 'C']
            }
            sample_df = pd.DataFrame(sample_data)
            csv_sample = sample_df.to_csv(index=False)

            st.download_button(
                label="📥 Download Sample CSV",
                data=csv_sample,
                file_name="sample_worship_songs.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()

