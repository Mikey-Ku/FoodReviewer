# pylint: skip-file
import requests
from TikTokApi import TikTokApi
import pandas as pd
import os


class BostonFoodReviewScraper:
    def __init__(self, output_dir="tiktok_food_reviews"):
        """
        Initialize the scraper with output directory and TikTok API

        Args:
            output_dir (str): Directory to save downloaded videos
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Initialize TikTok API
        # Note: You may need to handle verification challenges
        self.api = TikTokApi()

    def search_food_reviews(self, location="Boston", max_videos=50):
        """
        Search for food review videos in Boston

        Args:
            location (str): Location to search for reviews
            max_videos (int): Maximum number of videos to retrieve

        Returns:
            pandas.DataFrame: Dataframe with video metadata
        """
        # Construct search queries
        search_terms = [
            f"food review {location}",
            f"restaurant review {location}",
            f"{location} food tiktok",
            f"{location} restaurant tour",
        ]

        all_videos = []

        for term in search_terms:
            try:
                # Search videos
                videos = self.api.search(term, count=max_videos)

                for video in videos:
                    video_info = {
                        "id": video.id,
                        "description": video.description,
                        "create_time": video.create_time,
                        "likes": video.stats.digg_count,
                        "comments": video.stats.comment_count,
                        "author": video.author.username,
                        "video_url": video.url,
                    }

                    all_videos.append(video_info)

            except Exception as e:
                print(f"Error searching for term '{term}': {e}")

        # Convert to DataFrame
        df = pd.DataFrame(all_videos)
        return df

    def download_videos(self, videos_df):
        """
        Download videos from the dataframe

        Args:
            videos_df (pandas.DataFrame): Dataframe with video metadata
        """
        for index, row in videos_df.iterrows():
            try:
                video = self.api.video(url=row["video_url"])
                filename = os.path.join(
                    self.output_dir, f"{row['id']}_{row['author']}_review.mp4"
                )

                video.download(filename)
                print(f"Downloaded: {filename}")

            except Exception as e:
                print(f"Could not download video {row['id']}: {e}")

    def run(self):
        """
        Run the entire scraping process
        """
        print("Searching for Boston food review videos...")
        videos_df = self.search_food_reviews()

        print(f"Found {len(videos_df)} videos")

        if not videos_df.empty:
            self.download_videos(videos_df)

            # Save metadata
            videos_df.to_csv(
                os.path.join(self.output_dir, "video_metadata.csv"), index=False
            )


def main():
    scraper = BostonFoodReviewScraper()
    scraper.run()


if __name__ == "__main__":
    main()
