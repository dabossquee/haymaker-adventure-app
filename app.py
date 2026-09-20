import sys
import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load the secret variables from the hidden .env file
load_dotenv()

# Grab the key securely from your Mac's background environment
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("\n[System Error] Could not find your 'OPENAI_API_KEY' inside the hidden .env file.")
    sys.exit()

# Initialize the OpenAI Connection cleanly
try:
    client = OpenAI(api_key=API_KEY)
except Exception as e:
    print(f"[System Error] Failed to initialize AI client: {e}")
    sys.exit()

SAVE_FILE = "world_save.json"

# 2. INITIALIZE ENGINE STATE FRAMEWORK
world_engine = {
    "world_name": "",
    "world_genre": "",
    "player_character": {
        "name": "",
        "backstory": "",
        "health": 100,
        "inventory": ["survival gear"]
    },
    "story_log": []
}

def save_game():
    """Converts the active world state into a JSON file on your hard drive."""
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(world_engine, f, indent=4)
        print("\n💾 [System] Universe configuration and story timeline auto-saved successfully.")
    except Exception as e:
        print(f"\n[System Error] Failed to auto-save file: {e}")

def load_game():
    """Reads the JSON file from your disk and overwrites the active engine variables."""
    global world_engine
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                world_engine = json.load(f)
            print(f"\n📂 [System] State loaded successfully! Welcome back to '{world_engine['world_name']}'.")
            return True
        except Exception as e:
            print(f"\n[System Error] Failed to read save file: {e}")
            return False
    else:
        print("\n❌ [System Error] No existing save file found. Start a new game first!")
        return False

def display_status_bar():
    """Prints a clean game dashboard bar with updated stats."""
    char = world_engine["player_character"]
    print("\n" + "="*50)
    print(f" 🪐 WORLD: {world_engine['world_name'].upper()}")
    print(f" 🎭 CHARACTER: {char['name']} | ❤️ HEALTH: {char['health']}/100")
    print(f" 🎒 INVENTORY: {', '.join(char['inventory'])}")
    print("="*50)

# 3. INTERACTIVE WORLD SETUP MENU
print("=== HAYMAKER INDUSTRY WORLD-ENGINE VER. 1.2 ===")
print("1. [New Game] Create a fresh universe architecture")
print("2. [Load Game] Initialize existing saved world parameters")
print("3. [Exit Engine] Close application terminal")

menu_choice = input("\nSelect an operational profile (1-3): ").strip()

if menu_choice == "3":
    print("Shutting down engine core.")
    sys.exit()
elif menu_choice == "2":
    # Attempt to load, if it fails or file doesn't exist, exit gracefully
    if not load_game():
        sys.exit()
else:
    # Option 1 or anything else defaults to creating a fresh configuration
    print("\nLet's configure your custom universe architecture...\n")
    world_engine["world_name"] = input("Name your world/universe: ").strip()
    world_engine["world_genre"] = input("What is the genre? (e.g., Cyberpunk, Dark Fantasy, Sci-Fi): ").strip()
    world_engine["player_character"]["name"] = input("\nWhat is your character's name? ").strip()
    world_engine["player_character"]["backstory"] = input("Give your character a quick backstory/role: ").strip()
    print("\n[System] New universe initialized.")

print("\n[System] Entering your story loop now.\n")

# 4. THE INFINITE RUNTIME LOOP
while True:
    char_data = world_engine["player_character"]
    
    if char_data["health"] <= 0:
        print("\n💀 GAME OVER. Your character has perished in the wilderness.")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE) # Clear out save file on absolute death
        sys.exit()

    display_status_bar()
    
    master_prompt = (
        f"You are the master engine for an advanced worldbuilding and text-game called Haymaker.\n"
        f"The user's world: '{world_engine['world_name']}' (Genre: '{world_engine['world_genre']}').\n"
        f"Character: '{char_data['name']}' (Backstory: '{char_data['backstory']}').\n"
        f"Current Inventory: {', '.join(char_data['inventory'])}.\n"
        f"Current Health: {char_data['health']}/100.\n\n"
        f"CRITICAL STATE ENGINE RULES:\n"
        f"1. Never break character or mention you are an AI language model.\n"
        f"2. Immersively narrate the outcome of the user's action matching the genre's atmosphere.\n"
        f"3. Always end your response by prompting them on what to do next.\n"
        f"4. DATA COMMAND TRIGGERS: If the character finds an item, gets hurt, heals, or loses an item based on your narration, you MUST append hidden data tags at the absolute bottom of your response using these exact structures:\n"
        f"   - To award an item: [LOOT: item_name]\n"
        f"   - To remove an item: [REMOVE: item_name]\n"
        f"   - To change health (damage or healing): [HEALTH: +20] or [HEALTH: -15]\n"
    )
    
    messages = [{"role": "system", "content": master_prompt}]
    
    for past_turn in world_engine["story_log"]:
        messages.append({"role": past_turn["role"], "content": past_turn["content"]})
        
    if not world_engine["story_log"]:
        user_input = "Wake up and look around."
    else:
        user_input = input("\nWhat do you want to do next? ").strip()
        
    if user_input.lower() == "quit":
        print("\nShutting down World Engine. Progress safely saved.")
        sys.exit()

    if world_engine["story_log"]:
        world_engine["story_log"].append({"role": "user", "content": user_input})
        print("\n⏳ Simulating action...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=450,
            temperature=0.7
        )
        
        raw_ai_narrative = response.choices[0].message.content
        
        # 5. THE DELIMITER PARSER ENGINE
        cleaned_narrative = raw_ai_narrative
        
        # Parse LOOT tags
        loot_matches = re.findall(r'\[LOOT:\s*(.*?)\]', raw_ai_narrative, re.IGNORECASE)
        for item in loot_matches:
            item_clean = item.strip()
            if item_clean not in char_data["inventory"]:
                char_data["inventory"].append(item_clean)
            cleaned_narrative = re.sub(rf'\[LOOT:\s*{re.escape(item)}\]', '', cleaned_narrative, flags=re.IGNORECASE)
            
        # Parse REMOVE tags
        remove_matches = re.findall(r'\[REMOVE:\s*(.*?)\]', raw_ai_narrative, re.IGNORECASE)
        for item in remove_matches:
            item_clean = item.strip()
            if item_clean in char_data["inventory"]:
                char_data["inventory"].remove(item_clean)
            cleaned_narrative = re.sub(rf'\[REMOVE:\s*{re.escape(item)}\]', '', cleaned_narrative, flags=re.IGNORECASE)
            
        # Parse HEALTH tags
        health_matches = re.findall(r'\[HEALTH:\s*([+-]\d+)\]', raw_ai_narrative)
        for modifier in health_matches:
            char_data["health"] += int(modifier)
            char_data["health"] = max(0, min(100, char_data["health"]))
            cleaned_narrative = re.sub(rf'\[HEALTH:\s*{re.escape(modifier)}\]', '', cleaned_narrative)

        # Print out the clean, immersive narrative text
        print("\n" + "="*50)
        print(cleaned_narrative.strip())
        print("="*50)
        
        # Save raw turn data to application memory logs
        world_engine["story_log"].append({"role": "assistant", "content": raw_ai_narrative})
        
        # Automatically save everything to your hard drive file at the end of every successful turn
        save_game()
            
    except Exception as e:
        print(f"\n[Engine Error] Failed to connect to AI server: {e}")
        sys.exit()

