import requests
import pandas as pd
import time


def fetch_anime_info(name, work_type):     
    # GraphQL query
    query = '''
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            title {
                romaji
                english
            }
            format
            episodes
            duration
            source
            season
            seasonYear
            genres
            tags {
                name
            }
            startDate {
                year
                month
                day
            }
            countryOfOrigin
            averageScore
            nextAiringEpisode {
                episode
            }
        }
    }
    '''
    
    variables = {'search': name}
    url = 'https://graphql.anilist.co'
    
    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        response.raise_for_status()
        data = response.json()
        
        if 'errors' in data or 'data' not in data or data['data']['Media'] is None:
            print(f"Error: No match found for '{name}'")
            time.sleep(1)
            return "" 
        
        media = data['data']['Media']
        
        # Check if format matches the type
        media_format = media.get('format', '').lower()
        if media_format != work_type:
            print(f"Error: No match found for '{name}' with type '{work_type}'")
            time.sleep(1)
            return ""
        
        # Format start_date
        start_date = None
        if media.get('startDate'):
            sd = media['startDate']
            if sd.get('year') and sd.get('month') and sd.get('day'):
                start_date = f"{sd['year']}-{sd['month']}-{sd['day']}"
        
        # Extract and format genres
        genres = ';'.join(media.get('genres', [])) if media.get('genres') else None
        
        # Extract and format tags
        tags = ';'.join([tag['name'] for tag in media.get('tags', [])]) if media.get('tags') else None
        
        # Extract next episode number
        next_episode = None
        if media.get('nextAiringEpisode'):
            next_episode = media['nextAiringEpisode'].get('episode')
        
        # Create dataframe
        df = pd.DataFrame([{
            'title': media.get('title', {}).get('romaji'),
            'english_title': media.get('title', {}).get('english'),
            'type': media.get('format'),
            'episodes': media.get('episodes'),
            'duration': media.get('duration'),
            'source': media.get('source'),
            'season': media.get('season'), 
            'genres': genres,
            'tags': tags,
            'score': media.get('averageScore'),
            'start_date': start_date,
            'country_of_origin': media.get('countryOfOrigin'),
            'next_episode_number': next_episode
        }])
        
        time.sleep(2)
        return df
        
    except Exception as e:
        print(f"Error: {str(e)}")
        time.sleep(1)
        return ""

