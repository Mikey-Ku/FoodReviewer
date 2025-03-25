# pylint: skip-file
import asyncio
from TikTokApi import TikTokApi

# Initialize TikTokApi with custom verifyFp (if needed)
api = TikTokApi()

# Define the hashtag to search for
hashtag = "bostonrestaurants"


async def fetch_videos():
    try:
        # Load posts under the hashtag
        posts = api.hashtag(name=hashtag).videos(count=100)

        # Iterate over posts and print video URLs
        async for post in posts:
            video = await post
            print(video["video"]["playAddr"])
    except Exception as e:
        print(f"An unexpected error occurred while fetching posts: {e}")


# Run the asynchronous function
asyncio.run(fetch_videos())
