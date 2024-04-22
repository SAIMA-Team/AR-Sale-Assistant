import speech_recognition as sr
from gtts import gTTS
import os
from pymongo import MongoClient

# Connect to MongoDB
connection_string = "mongodb+srv://ashan:ashan@cluster0.jkjpbuh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client["computer_shop"]
ram_collection = db["ram"]
gpu_collection = db["gpu"]  # Assume you have a collection for GPUs

def insert_ram_data():
    ram_data = [
        {"type": "4gb", "price": 50, "tested_speed": "DDR4-2400MHz", "warranty": "1 year"},
        {"type": "8gb", "price": 80, "tested_speed": "DDR4-3200MHz", "warranty": "2 years"},
        {"type": "16gb", "price": 120, "tested_speed": "DDR4-3600MHz", "warranty": "3 years"},
        {"type": "32gb", "price": 200, "tested_speed": "DDR4-4000MHz", "warranty": "5 years"}
    ]
    ram_collection.insert_many(ram_data)

# Check if RAM data is already inserted, if not, insert it
if ram_collection.count_documents({}) == 0:
    insert_ram_data()

def insert_gpu_data():
    gpu_data = [
        {"model": "GTX 1660", "price": 300, "boost_clock": "1650 MHz", "memory_size": "4gb", "memory_type": "GDDR6", "cuda_cores": 1408},
        {"model": "RTX 2070", "price": 500, "boost_clock": "1800 MHz", "memory_size": "8gb", "memory_type": "GDDR6", "cuda_cores": 2304},
        {"model": "RTX 3080", "price": 900, "boost_clock": "1900 MHz", "memory_size": "12gb", "memory_type": "GDDR6", "cuda_cores": 8704},
        {"model": "RX 580", "price": 200, "boost_clock": "1411 MHz", "memory_size": "8gb", "memory_type": "GDDR5", "cuda_cores": 2304}
    ]
    gpu_collection.insert_many(gpu_data)

if gpu_collection.count_documents({}) == 0:
    insert_gpu_data()


# Function to extract component type from user input
def extract_component_type(input_text):
    ram_keywords = ["ram", "memory", "rams"]
    gpu_keywords = ["gpu", "graphics card", "gpus"]
    for word in input_text.lower().split():
        if word in ram_keywords:
            return "ram"
        elif word in gpu_keywords:
            return "gpu"
    return None

# Function to get price based on user input
def get_price_and_details(input_text, component_type):
    if component_type == "ram":
        ram_type = extract_ram_type(input_text.lower())
        if ram_type:
            ram = ram_collection.find_one({"type": ram_type})
            if ram:
                if "price" in input_text.lower():
                    return f"the {ram_type} ram price is {ram['price']}"
                elif "details" in input_text.lower():
                    return f"the {ram_type} ram has tested speed of {ram['tested_speed']} and it has {ram['warranty']} of warranty period. you can buy this ram for {ram['price']} dollars"
                else:
                    return f"query does not understand"   #No {component_type} found
                
    elif component_type == "gpu":
        gpu_model = extract_gpu_model(input_text.lower())
        if gpu_model:
            gpu = gpu_collection.find_one({"model": gpu_model})
            if gpu:
                if "price" in input_text.lower():
                    return f"the {gpu_model} gpu price is {gpu['price']}"
                elif "details" in input_text.lower():
                    return f"the {gpu_model} gpu has boost clock of {gpu['boost_clock']} and it has {gpu['cuda_cores']} cuda cores. the {gpu_model} gpu has {gpu['memory_type']} {gpu['memory_size']} you can buy this gpu for {gpu['price']} dollars"
                else:
                    return f"query does not understand"
    return f"i did not understand the query"

def get_availability(input_text, component_type):
    if component_type == "ram" and "have" in input_text.lower():
        return "a" 
    elif component_type == "gpu" and "have" in input_text.lower():
        return "b"
    else:
        return get_price_and_details(input_text, component_type)
        

# Function to extract RAM type from user input
def extract_ram_type(input_text):
    ram_types_mapping = {
        "four gb": "4gb",
        "eight gb": "8gb",
        "sixteen gb": "16gb",
        "thirty two gb": "32gb"
    }
    # Check pure English keywords
    for keyword, ram_type in ram_types_mapping.items():
        if keyword in input_text:
            return ram_type
    # Check original types
    for ram_type in ["4gb", "8gb", "16gb", "32gb"]:
        if ram_type in input_text:
            return ram_type
    return None

# Function to extract GPU model from user input
def extract_gpu_model(input_text):
    gpu_models_mapping = {
        "gtx sixteen sixty": "GTX 1660",
        "rtx twenty seventy": "RTX 2070",
        "rtx thirty eighty": "RTX 3080",
        "rx five eighty": "RX 580"
    }
    # Check pure English keywords
    for keyword, gpu_model in gpu_models_mapping.items():
        if keyword in input_text:
            return gpu_model
    # Check original types
    for gpu_model in ["GTX 1660", "RTX 2070", "RTX 3080", "RX 580"]:
        if gpu_model.lower() in input_text:
            return gpu_model
    return None

# Function to handle greetings
def handle_greetings(input_text):
    if "good morning" in input_text.lower():
        return "Good morning! How can I help you?"
    return None

# Function to handle gratitude
def handle_gratitude(input_text):
    if "thank you" in input_text.lower():
        return "Thank you for shopping. Come again!"
    return None

# Function to convert text to speech
def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")  # Save the audio as output.mp3
    os.system("start output.mp3")  # Play the audio using the default audio player

# Main conversation loop
while True:
    recognizer = sr.Recognizer()

    # Listen to user's speech input
    with sr.Microphone() as source:
        print("You: Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        # Convert user's speech to text
        user_input = recognizer.recognize_google(audio_data)
        print("You:", user_input)

        # Handle greetings
        greeting_response = handle_greetings(user_input)
        if greeting_response:
            print("Bot:", greeting_response)
            text_to_speech(greeting_response)
            continue

        # Handle gratitude
        gratitude_response = handle_gratitude(user_input)
        if gratitude_response:
            print("Bot:", gratitude_response)
            text_to_speech(gratitude_response)
            continue

        # If not greetings or gratitude, proceed with component price query
        component_type = extract_component_type(user_input)
        availability_response = get_availability(user_input, component_type)
        if availability_response:
            print("Bot:", availability_response)
            text_to_speech(availability_response)
        else:
            print("Bot:", f"Sorry, I could not understand the question ")
            text_to_speech("Sorry, I could not understand the question ")

    except sr.UnknownValueError:
        print("Bot:", "Sorry, could not understand audio.")
        text_to_speech("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Bot:", f"Error occurred; {str(e)}")
        text_to_speech(f"Error occurred; {str(e)}")

    # Check if the user wants to end the conversation
    if user_input.lower() == "quit":
        print("Bot: Goodbye!")
        text_to_speech("Goodbye!")
        break
