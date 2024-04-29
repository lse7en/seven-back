dictionary = {
    "en": {
        "start_message": """Hello! Wellcome to WYD. I'm a bot that can help you find activities to do in your area. 
You can start by sending me a location now.""",
        "help_message": """Welcome to WYD Bot! 🎉 Your go-to Telegram buddy for finding and joining exciting activities shared by others. 
Whether you're into sports, books, games, or looking for something new, WYD Bot connects you with a vibrant community eager to share and explore together. 
Discover activities around you, join in with a tap, or create your own and invite friends. Dive into a world of shared experiences and make every day memorable. Let's get started!""",
        "user_location_set_message": "Your location has been set successfully. you can now start by pressing the Application button below.",
        "activity_location_set_message": "The location of the activity with the name ({}) has been set successfully.",
        "user_location_request_message": "Please send me a location to find activities around you.",
        "activity_location_request_message": "Please send me a location for the activity with the name ({}).",
    }
}


def get_text(language_code: str, key: str) -> str:
    return dictionary.get(language_code, dictionary['en'])[key]
