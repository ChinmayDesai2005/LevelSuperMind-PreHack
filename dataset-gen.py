import pandas as pd
import random

post_types = ['Text', 'Image', 'Video', 'Link', 'Poll', 'Short Video']
engagement_ranges = {
    'Text': (50, 500),
    'Image': (100, 2000),
    'Video': (200, 5000),
    'Link': (20, 300),
    'Poll': (10, 1000),
    'Short Video': (300, 10000)
}

data = []
for _ in range(100):
    post_type = random.choice(post_types)
    likes = random.randint(*engagement_ranges[post_type])
    shares = random.randint(0, int(likes * 0.5))
    comments = random.randint(0, int(likes * 0.3))
    engagement_time = random.uniform(1, 15)
    sentiment = random.choice(['Positive', 'Neutral', 'Negative'])
    reach = random.randint(500, 10000)
    impressions = random.randint(1000, 15000)
    hashtags = random.sample(['#fun', '#news', '#viral', '#love', '#tech', '#sports', '#health'], k=random.randint(1, 4))
    platform = random.choice(['Facebook', 'Twitter', 'Instagram', 'LinkedIn'])
    day_of_week = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    post_time = random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])

    data.append({
        'post_id': f"POST_{random.randint(1000, 9999)}",
        'post_type': post_type,
        'likes': likes,
        'shares': shares,
        'comments': comments,
        'engmnt_time': round(engagement_time, 2),
        'sentiment': sentiment,
        'react': reach,
        'impressions': impressions,
        'hashtags': hashtags,
        'platform': platform,
        'day_of_week': day_of_week,
        'post_time': post_time,
        'content': ''
    })

df = pd.DataFrame(data)

print(df.head())

df.to_json('datasets/social_media_engagement01.json', orient='records')
