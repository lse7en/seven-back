from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
import random

adjectives = [
    "Shadow", "Mystic", "Cyber", "Silent", "Neon", "Crimson", "Lunar", "Ghost",
    "Electric", "Ancient", "Hidden", "Sapphire", "Golden", "Iron", "Quantum", "Echo",
    "Storm", "Wild", "Blazing", "Frozen", "Thunder", "Silver", "Dark", "Solar", "Glowing"
]

nouns = [
    "Hunter", "Ninja", "Wizard", "Knight", "Rider", "Blade", "Ghost", "Phoenix",
    "Dragon", "Tiger", "Wolf", "Falcon", "Shadow", "Eagle", "Sage", "Dancer",
    "Samurai", "Guardian", "Voyager", "Seeker", "Wanderer", "Sorcerer", "Rogue"
]

special_chars = ['_', '.', '-', '']

def stylize_text(text):
    leet_mapping = {
        'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['5', '$'],
        't': ['7'], 'l': ['1', '|'], 'g': ['9'], 'b': ['8'], 'z': ['2']
    }
    new_text = ''
    for c in text:
        if c.lower() in leet_mapping:
            c = random.choice(leet_mapping[c.lower()])
        new_text += c

    new_text = ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in new_text)
    
    if random.choice([True, False]):
        pos = random.randint(1, len(new_text) - 2)
        new_text = new_text[:pos] + random.choice(['_', '.', '-']) + new_text[pos:]
    
    return new_text

async def create_bots(session: AsyncSession):
    bots = []
    existing_usernames = set()
    for _ in range(50):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        special_char = random.choice(special_chars)
        number = random.choice(['', str(random.randint(1, 99))])
        
        username_base = f"{adjective}{special_char}{noun}{number}".lower()
        username = stylize_text(username_base)
        
        while username in existing_usernames:
            number = str(random.randint(1, 99))
            username_base = f"{adjective}{special_char}{noun}{number}".lower()
            username = stylize_text(username_base)
        existing_usernames.add(username)
        
        first_name = adjective
        last_name = noun
        
        bot = User(
            id= -i,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_bot=True,
            points=100000000,
        )
        bots.append(bot)
        session.add(bot)
    await session.commit()
