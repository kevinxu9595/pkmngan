import os
import json
import requests
import re

target_folder = input()
print(f"Downloading images and putting them in {target_folder}...")

# Make sure the target folder exists
os.makedirs(target_folder, exist_ok=True)

# Start on page 1
next_page_number = 1

# Fetch pages until we tell it to break
while True:
    # Make a URL to download data
    next_page_url = f"https://api.pokemontcg.io/v1/cards?page={next_page_number}"
    print(f"Loading {next_page_url}")

    try:
        # Download the blob of JSON
        response = requests.get(next_page_url)
        response.raise_for_status()
        next_page_data = response.text

        # Parse it into a Python dictionary
        next_page_hash = json.loads(next_page_data)

        # Get the cards from the dictionary
        cards = next_page_hash.get("cards", [])

        if not cards:
            # There weren't any cards on this page, so terminate the script
            print("No more cards, terminating")
            break

        # For each card, download the image and write it to a file
        for card in cards:
            # Create a target filepath based on the card ID & name
            raw_filepath = f"{target_folder}/{card['id']}-{card['name']}.png"

            # Filter out problem characters from the filename, only allow:
            # - lowercase & uppercase letters
            # - numbers
            # - special characters: \/-_.
            # Replace any other characters with `-`
            filepath = re.sub(r"[^a-zA-Z0-9\-_\/.]", "-", raw_filepath)

            if os.path.exists(filepath):
                print(f" -> skip {filepath}")
                continue

            print(f" -> {filepath}")

            try:
                # Get the URL from this card's JSON
                # If you want the low-res URL,
                # remove "imageUrlHiRes" only on the line below and put "imageUrl" instead.
                image_url = card.get("imageUrlHiRes")
                if not image_url:
                    print(f" -> No image URL for card {card['id']}, skipping...")
                    continue

                # Read the file from the URL
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                # Write the image data to a local file
                with open(filepath, "wb") as image_file:
                    image_file.write(image_response.content)

            except Exception as err:
                print(f"Encountered an error: {err}, continuing...")
                print(f"Image URL: {image_url}")
                print(f"Card data: {card}")

    except Exception as e:
        print(f"Failed to load page {next_page_number}: {e}")
        break

    # Increment the page number so that we get the next page
    next_page_number += 1