import base64
from openai import OpenAI
import os
import random

# Define character-specific details
armie_specific_notes = """ """
# - Ears are highly expressive and should change position based on emotions:
#  * The ears must maintain their correct proportions relative to the body - they should be approximately the same height as the character's body when fully extended upward. The ears should be slender and elongated, about 2-3 times longer than they are wide, with a gentle taper toward the tips. When the ears bend, they should bend at roughly the midpoint, creating a natural curve rather than a sharp angle.
#  * Ears are always behind the main shapes, never in front (except when ears are down)
#  * Ears are bent for relaxed/neutral poses and straightened upwards for excited emotions

# - The character shape is triangular with exact color scheme:
#  * Face: pink (#ddadc8)
#  * Eyes: teal (#7fc9cc) with black glasses (#000000)
#  * Eye lids: darker teal (#528a8c) when shown
#  * Skin: purple-gray (#6f687e)
#  * Shirt: teal (#6ba3a5)
#  * Cardigan: navy (#233953)
#  * Tongue: coral (#f16973)

# - Body must preserve exact proportions:
#  * Triangle-shaped body with straight bottom line (never volumetric)
#  * Body drawn as one uninterrupted line, sometimes broken in profile
#  * Pupils always below center of eyes
#  * When closed, eyes look like a "U" shape
#  * Front tooth separate from other teeth
#  * Arms must pivot with some sleeve visible on both sides
#  * Feet have 3 short pointy toes with no curves in the heel
#  * Tail starts small and grows bigger, always behind main body

# - The nose should be preserved exactly


bogart_specific_notes = """
- The character should NEVER have arms or limbs of any kind
- Body must maintain its segmented worm/caterpillar form with defined rings/segments
- Eyes are highly expressive and essential to character's emotion:
  * Bright red eyes (#dc1515) with upper and lower lids a shade darker than body
  * When happy/excited: Eyes wide open, may have slight upper curve
  * When angry: Eyes may have green/olive upper portion with narrowed appearance
  * When suspicious: Eyes may appear half-lidded or asymmetrical
  * When surprised: Eyes perfectly round and wide
  * When closed: A "U" shape drawn inside in eyelid color (not red)

- Mouth is extremely elastic and should dramatically express emotions:
  * When happy: Wide smile showing teeth (upper teeth only or full mouth)
  * When laughing: Large open mouth with visible tongue
  * When surprised: Perfect "O" shape
  * When shouting: Exaggerated open mouth
  * When worried/sad: Downturned, often asymmetrical
  
- Teeth are a critical feature and change with expressions:
  * When smiling: Shows a row of large, rectangular white teeth
  * When menacing/angry: Can show sharp-looking teeth
  * When laughing: Full display of upper and sometimes lower teeth
  * Teeth should always be white with clear definition between each tooth
  * Sometimes shows a single front tooth when smirking
  
- The character's eyebrows (black curved shapes above eyes) are critical for expressions:
  * Angled downward when angry
  * Raised high when surprised
  * Asymmetrical when confused or suspicious
  
- The character's body posture/curve should reflect emotion:
  * When excited: May be curved like an "S" shape
  * When sad: May droop downward
  * When surprised: May stand more vertically straight
  * The body can be squashed and stretched a lot, keeping overall volume
  * When fully stretched, body and tail are one thing
  * Bogart can use its tail as a limb and grab things with it
  
- Color scheme must remain consistent: 
  * Skin: cream/beige (#dfd9c1)
  * Eyes: red (#dc1515)
  * Eyelids: olive green (#a2a678)
  * Tongue: pink (#ed6c80)
  * Teeth: white (#ffffff)
  * All with black outlines
"""

bearnice_specific_notes = """
- The character's distinctive gray cloud-like hair must be preserved exactly:
  * Two poofy cloud-shaped gray sections on each side of the head (#9d8d89)
  * Small pink bunny-like ears visible between the hair puffs
  * The hair should always have the distinctive curly lines/swirls
  * The hair puffs can be drawn in front or behind the head shape

- Face characteristics must remain consistent:
  * Pink rounded face (#f7b6a7) with rosy cheeks (small red dots)
  * Eyes are small ovals in the top half of face with three lashes
  * The character has prominent front teeth (usually two) that must be visible
  * Mouth is highly expressive and can range from small smile to wide open
  * The nose is shaped like a heart with a line connecting to the mouth
  * 3 freckles same color as lower lip

- Body features to preserve:
  * Pink rounded body shape 
  * Always wearing rainbow striped overalls with yellow buttons
  * Small gray hands/feet with limited digits
  * The rainbow colors must appear in the correct order (red, orange, yellow, green, blue, purple)
  * The small pentagon-shaped pocket on the overalls
  * Wears rainbow socks and yellow "converse" sneakers
  * Head is as big as body+legs combined
  
- Expressions should be shown through:
  * Eye shape and size (wide when surprised, half-lidded when smug/tired)
  * Eyebrows (even though they may not always be visible)
  * Mouth position and shape
  * Tongue may be visible when the character is being silly/playful
  * Displaying objects the character is holding
  
- The character should always maintain its childlike, cute proportions
- The colors should remain consistent according to the color palette:
  * Teeth/Eyes white (#ffffff)
  * Face/Inner Ears pink (#f7b6a7)
  * Rainbow top in correct spectrum (#c31918, #8080bc, #80c0e1, #88c58c, #f9ee78, #f9b774)
  * Skin gray (#9d8d89)
  * Dungarees pink (#ec98c1)
  * Buttons yellow (#e0b51f)
  * Eye lids purple (#bc8fa4)
  * Lips/Cheeks pink (#e6376e)
  * Tongue pink (#ea6c82)
"""

brick_specific_notes = """
- The character has a distinctive rectangular brick-like head shape that must be preserved exactly:
  * Brown/tan colored head (#ba8f73) with thick black outline
  * Small pink bunny-like ears (#f39b92) on top of the head
  * The head maintains its angular, brick-like geometry
  * Head is a little less voluminous than the tummy
  
- Face characteristics that must remain consistent and recognizable:
  * Eyes should be simple black dots/ovals - never complex or detailed
  * The eyes maintain a consistent sleepy/calm look even when expressing emotions
  * Small black nose (just a simple dot or short line)
  * The mouth should be a simple black line or basic shape - never showing detailed teeth or overly dramatic expressions
  * The face should maintain Brick's characteristic calm, simple demeanor even in different emotions
  * Expressions should be subtle and understated, not exaggerated
  * Front tooth is disjointed from other teeth
  * To direct Brick's gaze, a small line is drawn turning the dot into a "comma"
  
- Body features to preserve:
  * White or light-colored shirt/top (#ffffff)
  * Blue/navy pants or shorts (#324a61)
  * Simple stick-like arms and legs with basic hands (sometimes just ovals)
  * Black shoes or simple foot shapes (#131313)
  * The body should maintain its basic geometric, blocky proportions
  * When Brick bends backward, a fat roll appears behind his neck
  * One decisive line separates the t-shirt from shorts
  * Legs are half-covered by shorts
  * 4 fingers, or 3 when thumb is hidden
  
- Expression guidelines - CRITICAL for character consistency:
  * Eyes should remain simple ovals/dots and keep Brick's naturally calm look
  * Even when happy, sad, or surprised, maintain the understated, simple facial style
  * Mouth expressions should be minimal - simple curves, lines, or small open shapes
  * Avoid overly cartoonish or dramatic facial expressions
  * The character should look recognizably like the same personality in all images
  * Keep the minimalist, geometric art style consistent
  
- Color scheme must remain consistent:
  * Brown/tan head (#ba8f73), pink ears (#f39b92), white shirt (#ffffff), blue pants/shorts (#324a61)
  * Eye lids darker brown (#785b47) when shown
  * Tongue pink (#e85660)
  * Black outlines and simple black features (eyes, nose, mouth)
  * The character should maintain its blocky, geometric aesthetic with clean lines
"""

plato_specific_notes = """
- The character is a platypus-like creature with a distinctive bill that must be preserved exactly:
  * Green duck-like bill (#6ba3a5 or similar) that's highly expressive and central to character identity
  * Two small oval nostrils on the bill
  * Bill should maintain its shape but can be extremely elastic for expressions
  * Bill changes shape dramatically with emotions (wide open when excited, curved down when sad)

- Face and head characteristics must remain consistent:
  * Brown/tan rounded head (#ba8f73) with red baseball cap (#c31918) worn backward with small button on top
  * Yellow oval eyes (#f9ee78) that can change shape with expressions
  * When angry, eyes narrow and eyebrows appear
  * When sad, eyes droop or appear half-lidded
  * The head maintains its round shape with the bill as the focal point

- Body features to preserve:
  * Teal/turquoise shirt (#6ba3a5) with collar and buttons
  * Brown furry body with the same color as head
  * Simple stick-like arms with small hands (3-4 fingers)
  * Distinctive furry tail with black spikes/hairs
  * Small bird-like feet with three toes
  * Body proportions should be maintained - small body with large head and bill

- Expression guidelines:
  * Teeth are visible when smiling wide or laughing (rectangular yellow teeth)
  * Pink tongue (#f16973) visible during excited expressions
  * When happy/excited: Wide open bill, arms outstretched, energetic posture
  * When angry: Furrowed brows, clenched teeth, tense posture
  * When sad/worried: Drooping bill, slumped posture
  * Bill can sometimes hang open when confused or surprised

- Color scheme must remain consistent:
  * Head/Body: Brown/tan (#ba8f73)
  * Bill: Green (#6ba3a5)
  * Eyes: Yellow (#f9ee78)
  * Cap: Red (#c31918)
  * Shirt: Teal/turquoise (#6ba3a5)
  * Tongue: Pink (#f16973)
  * Teeth: Yellow (#f9ee78)
"""

yin_specific_notes = """
- The character is a tiger-like creature with a triangular face that must be preserved exactly:
  * Bright orange face and body (#ff7d1e or similar) with black tiger-like stripes
  * CRITICAL: The character's snout/muzzle area should be preserved exactly as a unified white region that contains both the nose and mouth
  * Large, pointed black ears with white inner portions
  * Orange tuft/hair on top of the head with a light green band/collar
  * Distinctive white oval eyes with black pupils and feminine eyelashes
  * Small pink nose and expressive mouth that changes with emotions
  * Small white teeth that are visible in various expressions

- Face and head characteristics must remain consistent:
  * Triangular head shape with pointed chin
  * Eyes are oval/almond-shaped and positioned in the upper half of the face
  * Eyes change shape with expressions but maintain their distinctive look
  * Eyelashes should always be present to maintain feminine appearance
  * Eyebrows (when shown) appear as darker orange lines above eyes

- Body features to preserve:
  * Slender orange body with black tiger stripes
  * Small orange hands/paws with three fingers
  * White front/chest area
  * Light green diaper/shorts with blue safety pin
  * Striped tail that curves expressively based on emotions
  * Small orange feet with three toes

- Expression guidelines:
  * When happy: Wide smile, eyes may be closed or open
  * When excited: Arms raised, wide mouth, energetic posture
  * When surprised: Wide eyes, open mouth, raised eyebrows
  * When sad/worried: Downturned mouth, half-lidded eyes, slumped posture
  * When angry: Narrowed eyes, tight mouth or visible teeth
  * Tail position changes with emotions - curled when happy, straight when alert

- Color scheme must remain consistent:
  * Main Body/Face: Bright orange (#ff7d1e)
  * Stripes: Black (#000000)
  * Eyes: White with black pupils
  * Ear interiors: White
  * Nose: Pink (#ff9eb3)
  * Diaper/Shorts: Light green (#c6e6a9)
  * Safety pin: Blue (#7fc9cc)
  * Mouth interior: Black with pink tongue
  * Teeth: White
"""

yang_specific_notes = """
- The character is a cat-like creature with a triangular face that must be preserved exactly:
  * Bright orange face and body (#ff7d1e or similar) with black tiger-like stripes
  * CRITICAL: The character has a distinctive WHITE MUZZLE/SNOUT AREA that forms a unified white region containing both the nose and mouth - this is the most defining facial feature
  * The white muzzle contrasts sharply with the orange face and has a clean black outline
  * Large, pointed black ears with white inner portions
  * Orange tuft/hair on top of the head with a light purple/lavender band/collar
  * White oval eyes with black pupils and feminine eyelashes
  * Small pink triangular nose (#ff9eb3) centered on the white muzzle
  * Small white teeth that are visible in various expressions

- Face and head characteristics must remain consistent:
  * Triangular head shape with pointed chin
  * The white muzzle/snout area must maintain its shape and contrast with the orange face
  * Eyes are oval/almond-shaped and positioned in the upper half of the face
  * Eyes change shape with expressions but maintain their distinctive look
  * Eyelashes should always be present to maintain feminine appearance
  * Eyebrows (when shown) appear as darker orange lines above eyes

- Body features to preserve:
  * Slender orange body with black tiger stripes
  * Small orange hands/paws with three fingers
  * White front/chest area that connects with the facial white muzzle
  * Light purple/lavender diaper/shorts with blue safety pin
  * Striped tail that curves expressively based on emotions
  * Small orange feet with three toes

- Expression guidelines:
  * When happy: Wide smile, eyes may be closed or open
  * When excited: Arms raised, wide mouth, energetic posture
  * When surprised: Wide eyes, round "O" shaped mouth
  * When sad/worried: Downturned mouth, half-lidded eyes, slumped posture
  * When angry: Narrowed eyes, tight mouth or visible teeth
  * Tail position changes with emotions - curled when happy, straight when alert

- Color scheme must remain consistent:
  * Main Body/Face: Bright orange (#ff7d1e)
  * Stripes: Black (#000000)
  * Eyes: White with black pupils
  * Ear interiors: White
  * Muzzle/Snout: White (#ffffff)
  * Nose: Pink (#ff9eb3)
  * Diaper/Shorts: Light purple/lavender (#e8c6e0)
  * Safety pin: Blue (#7fc9cc)
  * Mouth interior: Black with pink tongue
  * Teeth: White
  * Hair band: Light purple/lavender (#e8c6e0)
"""

pillow_specific_notes = """
- The character has a distinctive ghost-duck form that must be preserved exactly:
  * Pure white body (#ffffff) with a teardrop/ghost-like shape
  * Bright red bow (#c83231) on top of head that is quite voluminous 
  * The bow can have 3-4 distinct sections and is critical to character identity
  * The bow's position changes with emotions - drooping when sad, upright when excited
  * Distinctive wispy "feathers"/curls on sides of head that must always be drawn
  * These curls can express emotion and are considered her own feathers

- Face characteristics must remain consistent:
  * Yellow oval eyes (#f7e928) with three distinctive eyelashes that move from top to outer sides
  * Purple/gray eyelids (#968aa1) when shown
  * Beak is very flexible with a top ridge that can sometimes be omitted
  * Pink lips/beak (#f29394) that changes dramatically with emotions
  * When smiling: Shows pale yellow rectangular teeth (#f6f09e)
  * Eyes and beak are generally separated but can overlap for stronger expressions
  * Eyebrows (when shown) can cross out of her head, sometimes with an extra fold on her skin

- Body features to preserve:
  * Long neck with head making up a large portion of body
  * Small black dress (#232323) with gray cuffs (#6e6968) and two buttons
  * White hands with exactly 4 fingers
  * Pink/coral legs (#f29493) that must always come out from bottom of dress
  * Legs bend in smooth curves
  * "Kitten heel" shoes with 2 toes and distinctive heel shape
  * Black shoes (#000100)

- Expression guidelines:
  * When happy: Curved eyes, wide smile
  * When excited: Upright bow, arms outstretched
  * When angry: Can be shown with head on fire and intense expression
  * When sad: Drooping bow, half-lidded eyes, downturned mouth
  * When surprised: Wide eyes, O-shaped beak
  * Tongue (#d43d58) visible during certain expressions
  
- The character is a fashionista but is most often seen in her signature black dress
- The character maintains a ghostly, floating quality in movement
- Her proportions must be preserved: long neck, long limbs, big feet, with head making up about half of her body
- The curls/feathers must always be drawn regardless of outfit or pose
"""

# Add the new character - Grit
grit_specific_notes = """
- The character has a distinctive triangular/elongated head that must be preserved exactly:
  * Gray skin color (#757576) with a triangular/drop-shaped body
  * Large, pointed tall ears that are highly expressive and change position based on emotions
  * Ears bend, flap, fold and help convey Grit's mood
  * Small black round nose and three whisker-dots on one side only
  * Pink oval eyes (#f6b7b9) with black pupils
  * Eyebrows are thicker than most other characters (second only to Bogart's)
  * Eyes are very close to each other, usually touching in the middle
  * Long head with eyes sitting in the bottom half, while brows move freely in upper half

- Face and expression characteristics must remain consistent:
  * The muzzle's bottom is made of 3 curves with a line dividing the snout
  * Teeth can be round (open mouth) or square (one or two rows)
  * When happy, a cheek is often drawn to enhance satisfied mood
  * When mouth is exaggerated, the neck falls lower
  * Multiple mouth styles: smooth lip, visible lip, various teeth configurations
  
- Body features to preserve:
  * The body is about half the length of the head
  * Body is shaped like a drop and more pronounced towards the tail end
  * Red t-shirt (#b53239) with sleeves
  * Blue shorts (#2759a1)
  * Simple gray hands/feet
  * White shoes/teeth (#ffffff)
  * Small body with large head
  * Body can be drawn bigger to strengthen a pose or allow better action

- Critical design elements:
  * "Quiff" that protrudes decisively continuing the line of the top of his head
  * "Sideburn" made of 3 curves that help visualize emotions
  * Pink tongue (#ed6f74) when visible
  * Body proportions maintain distinctive silhouette with tall ears
  * Gray eyelids (#444444) when shown
"""

# Add Stax character
stax_specific_notes = """
- The character is a giraffe-like creature with a distinctive elongated neck and body that must be preserved exactly:
  * Yellow skin/body (#e6bf0c) with brown spots (#6b3d28)
  * The character has two yellow oval-shaped ossicones (antenna-like structures) on top of the head
  * Brown hair (#6b3d28) in an "inverted bowl shape" with approximately 17 tufts
  * Hair can change and move around but maintains its distinctive tufted appearance
  * Green rectangular glasses (#aecb44) with curved corners that frame the eyes

- Face characteristics must remain consistent:
  * The snout can change shape and size with different expressions
  * Small oval nostrils on the snout
  * Eyes are small yellow ovals (#e7e344) that can touch when the space inside the lenses is too small
  * Eyes can have various expressions but maintain their simple style
  * Eyebrows can move freely in/out of glasses or stay between
  * Mouth is highly expressive and can take many forms
  * White rectangular teeth (#ffffff) when smiling
  * Pink tongue (#e96b82) visible during certain expressions

- Body features to preserve:
  * The neck is extremely flexible and can elongate, shrink, thicken and take many shapes
  * Head, neck, and body each take approximately 1/3 of Stax's height, plus ossicones on top
  * Body has a triangular/elongated shape with the distinctive yellow and brown spot pattern
  * Wears a green hoodie (#1fa538) with front pocket
  * Blue shorts (#184c98)
  * White shoes/teeth (#ffffff)
  * The tail ends in 3 tufts
  * The foot has 2 toes
  * The ankle enters the shoe graphically, with no real entry point

- Expression guidelines:
  * The character's highly flexible neck and body allow for a wide range of expressions
  * When happy: Wide smile showing rectangular teeth, slightly curved eyes
  * When excited: Stretched neck, raised arms, energetic posture
  * When sad/worried: Drooping neck, slumped posture
  * When surprised: Elongated neck, wide eyes
  * The ossicones can be animated to help convey emotions

- Color scheme must remain consistent:
  * Body/Skin: Yellow (#e6bf0c)
  * Hair/Spots: Brown (#6b3d28)
  * Hoodie: Green (#1fa538)
  * Shorts: Blue (#184c98)
  * Shoes/Teeth: White (#ffffff)
  * Eye Lids: Yellow-green (#aeaa15)
  * Glasses: Lime green (#aecb44)
  * Eyes: Yellow (#e7e344)
  * Tongue: Pink (#e96b82)
"""

# Function to get character details
def get_character_details(character_choice):
    if character_choice == "armie":
        folder_path = "Armie"
        character_specific_note = armie_specific_notes
        add_to_section = "ONLY change"
    elif character_choice == "bogart":
        folder_path = "Bogart_Expressions"
        character_specific_note = bogart_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "brick":
        folder_path = "Brick"
        character_specific_note = brick_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "plato":
        folder_path = "plato"
        character_specific_note = plato_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "yin":
        folder_path = "yin"
        character_specific_note = yin_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "yang":
        folder_path = "yang"
        character_specific_note = yang_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "oz":
        folder_path = "Oz"
        character_specific_note = pillow_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "grit":  # Added Grit character
        folder_path = "Grit"
        character_specific_note = grit_specific_notes
        add_to_section = "IMPORTANT"
    elif character_choice == "stax":  # Added Stax character
        folder_path = "Stax"
        character_specific_note = stax_specific_notes
        add_to_section = "IMPORTANT"
    else:  # Default to Bearnice or handle any other input
        folder_path = "Bearnice"
        character_specific_note = bearnice_specific_notes
        add_to_section = "IMPORTANT"
        
    return folder_path, character_specific_note, add_to_section

# Function to get images from a folder
def get_images_from_folder(folder_path, max_images=None):
    images = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".png"):
                images.append(os.path.join(root, file))
    
    # If max_images is specified, limit the number of images
    if max_images and len(images) > max_images:
        images = random.sample(images, max_images)
    
    # Open the image files
    return [open(img_path, "rb") for img_path in images]

# Ask how many characters to use
num_characters = input("How many characters do you want to use? (1-4): ").strip()

# Validate input
try:
    num_characters = int(num_characters)
    if num_characters < 1 or num_characters > 4:
        print("Invalid number. Using 1 character.")
        num_characters = 1
except ValueError:
    print("Invalid input. Using 1 character.")
    num_characters = 1

# Initialize variables
selected_characters = []
character_details = []
images = []
character_specific_note = ""
add_to_section = "IMPORTANT"

if num_characters > 1:
    # Let the user choose multiple characters
    print("Available characters: Armie, Bearnice, Bogart, Brick, Grit, Plato, Stax, Yin, Yang, Oz")
    
    for i in range(num_characters):
        char = input(f"Choose character {i+1}: ").strip().lower()
        selected_characters.append(char)
        folder_path, char_note, add_section = get_character_details(char)
        character_details.append((char, folder_path, char_note, add_section))
    
    # Ask how many images to use from each character after selecting all characters
    images_per_character = 3  # Reduced default since we may have more characters
    try:
        images_per_input = input(f"How many images to use from each character? (default: {images_per_character}): ")
        if images_per_input.strip():
            images_per_character = int(images_per_input)
    except ValueError:
        print(f"Invalid input. Using default value of {images_per_character}.")
    
    # Get images from all character folders
    all_images = []
    for char, folder_path, _, _ in character_details:
        char_images = get_images_from_folder(folder_path, max_images=images_per_character)
        all_images.extend(char_images)
    
    images = all_images
    
    # Combine all character notes
    combined_notes = ""
    for i, (char, _, char_note, _) in enumerate(character_details, 1):
        combined_notes += f"""
Character {i} ({char.capitalize()}) notes:
{char_note}
"""
    
    # We'll add the combined notes to the IMPORTANT section
    character_specific_note = combined_notes
    add_to_section = "IMPORTANT"
    
    # Create a combined output folder name
    folder_path = "_".join(selected_characters) + "_combined"
else:
    # Single character flow (original behavior)
    character_choice = input("Choose a character (Armie, Bearnice, Bogart, Brick, Grit, Plato, Oz, Stax, Yin, or Yang): ").strip().lower()
    selected_characters = [character_choice]  # Make it a list for consistency
    folder_path, character_specific_note, add_to_section = get_character_details(character_choice)
    
    # Get all images for the selected character
    images = get_images_from_folder(folder_path)

# Use environment variables for API key if available, otherwise use the provided key
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    # If environment variable not found, use the hardcoded key
    openai_api_key = ''

client = OpenAI(api_key=openai_api_key)

# Prompt the user for the scenario
if num_characters > 1:
    user_scenario = input(f"Please enter the scenario for the {num_characters} characters: ")
else:
    user_scenario = input("Please enter the scenario for the character: ")

# Create the base prompt
if num_characters > 1:
    if len(selected_characters) > 1:
        character_list = ", ".join([char.capitalize() for char in selected_characters[:-1]]) + f", and {selected_characters[-1].capitalize()}"
    else:
        character_list = selected_characters[0].capitalize()
    
    base_prompt = f"""
You are a professional artist. Create a new scene with these cartoon characters: {character_list}.
IMPORTANT: Preserve ALL of these aspects of each character exactly:
- Body shape and proportions unique to each character
- Each character's distinctive outline
- Facial structure and features specific to each character
- Color palette with exact hex codes for each character
- Style of expression unique to each character
- Style and texture for each character
ONLY change:
- Each character's expression according to the scenario
- Each character's pose according to the scenario
- The background should be a SOLID COLOR (such as light blue, pink, yellow, teal, or other simple flat color)
Make sure each character is instantly recognizable as the same character from the input images.
Ensure all characters maintain their distinct identities and styles. They should interact naturally while each preserving their unique appearance and expression style.
Scenario:
{user_scenario}
"""
else:
    base_prompt = f"""
You are a professional artist. Create a new scene with this cartoon character.
IMPORTANT: Preserve ALL of these aspects of the character exactly:
- Body shape and proportions
- Character's distinctive outline
- Facial structure and features
- Color palette with exact hex codes
- Style of expression unique to this character
- Style and texture
ONLY change:
- The character's expression according to the scenario
- The character's pose according to the scenario
- The background should be a SOLID COLOR (such as light blue, pink, yellow, teal, or other simple flat color)
Make sure the character is instantly recognizable as the same character from the input image.
Scenario:
{user_scenario}
"""

# Add the character-specific note to the appropriate section
if character_specific_note and add_to_section == "IMPORTANT":
    # Add to IMPORTANT section
    base_prompt = base_prompt.replace("Style and texture", f"Style and texture\n{character_specific_note}")
elif character_specific_note and add_to_section == "ONLY change":
    # Add to ONLY change section
    if num_characters > 1:
        base_prompt = base_prompt.replace("- Each character's pose according to the scenario", 
                                         f"- Each character's pose according to the scenario\n{character_specific_note}")
    else:
        base_prompt = base_prompt.replace("- The character's pose according to the scenario", 
                                         f"- The character's pose according to the scenario\n{character_specific_note}")

# Format the prompt
prompt = base_prompt

# Number of images to generate
num_images = 5
try:
    num_images_input = input(f"How many images to generate? (default: {num_images}): ")
    if num_images_input.strip():
        num_images = int(num_images_input)
except ValueError:
    print(f"Invalid input. Using default value of {num_images}.")

# Create output folder
if num_characters > 1:
    output_folder = "_".join(selected_characters) + "_generated"
else:
    output_folder = f"{folder_path}_generated"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i in range(num_images):
    print(f"Generating image {i+1}...")
    result = client.images.edit(
        model="gpt-image-1",
        image=images,
        prompt=prompt,
        size="1024x1024",
        quality="high"
    )
    print(f"Image {i+1} generated successfully!")
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    
    # Save the image to a file
    with open(f"{output_folder}/scene_{i+1}.png", "wb") as f:
        f.write(image_bytes)
    print(f"Saved to {output_folder}/scene_{i+1}.png")

# Close all open file handles
for img in images:
    if not img.closed:
        img.close()

print("\nImage generation completed!")