
# OpenAI-Image1 Model Powered Illustration Regeneration

This project leverages OpenAI's **`gpt-image-1`** model to generate and regenerate cartoon illustrations of custom characters with precise artistic guidelines. Users can create new scenes while preserving each character’s unique features, proportions, and color schemes, while allowing expressions and poses to adapt to a specified scenario.  

---

## Features

- Supports multiple cartoon characters (Armie, Bearnice, Bogart, Brick, Plato, Yin, Yang, Oz, Grit, Stax).  
- Maintains character-specific proportions, color palettes, facial expressions, and signature features.  
- Allows generation of scenes with **single or multiple characters**.  
- Uses **OpenAI Image Editing API** (`gpt-image-1`) for high-quality image generation.  
- Customizable scenarios: specify character poses and expressions dynamically.  
- Generates images with a solid-color background for clean, stylized output.  
- Configurable number of images per character and output images.  

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/furqi98/OpenAI-Image1-model-powered-Illustration-regeneration.git
cd OpenAI-Image1-model-powered-Illustration-regeneration
````

2. **Install dependencies:**

```bash
pip install openai python-dotenv
```

3. **Set up OpenAI API key:**

Create a `.env` file in the root directory with your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Usage

1. **Run the script:**

```bash
python charactergen.py
```

2. **Follow the prompts:**

* Select the number of characters (1-4).
* Choose characters from the available list:
  `Armie, Bearnice, Bogart, Brick, Grit, Plato, Stax, Yin, Yang, Oz`.
* Specify the scenario for the selected characters.
* Specify the number of images to generate (default is 5).

3. **View generated images:**

Generated images will be saved in a folder named:

* Single character: `<CharacterName>_generated`
* Multiple characters: `<Character1>_<Character2>_..._generated`

Each image is saved as `scene_<number>.png`.

---

## Character Details

Each character has a **distinctive design** that is preserved during image generation:

* **Armie** – Triangular body, expressive ears, specific color palette.
* **Bearnice** – Cloud-like hair, rainbow overalls, childlike proportions.
* **Bogart** – Worm/caterpillar-like segmented body, expressive eyes and mouth.
* **Brick** – Rectangular head, calm expressions, minimalistic design.
* **Plato** – Platypus-like features, expressive bill, small arms.
* **Yin/Yang** – Tiger or cat-like triangular face, expressive tail, distinct color palette.
* **Oz (Pillow)** – Ghost-duck form, long neck, fashion accessories.
* **Grit** – Triangular/elongated head, tall expressive ears, dynamic body.
* **Stax** – Giraffe-like elongated neck and body, flexible proportions, glasses.

> For full details, see the `charactergen.py` file where each character has its own **specific notes and instructions** to maintain artistic consistency.

---

## Folder Structure

```
.
├── Armie/                # Images for Armie
├── Bearnice/             # Images for Bearnice
├── Bogart_Expressions/   # Images for Bogart
├── Brick/                # Images for Brick
├── Grit/                 # Images for Grit
├── Plato/                # Images for Plato
├── Stax/                 # Images for Stax
├── Yin/                  # Images for Yin
├── Yang/                 # Images for Yang
├── Oz/                   # Images for Oz
├── charactergen.py       # Main script
├── README.md             # Project documentation
└── .env                  # Environment file with OpenAI API key
```

---

## Dependencies

* Python 3.8+
* [openai](https://pypi.org/project/openai/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Contributing

Contributions are welcome! You can add new characters, refine character guidelines, or improve the script’s image generation logic.

---

## License

This project is open source under the MIT License.

---

## Acknowledgments

* OpenAI for the `image-1` model.
* Mrs Wordsmith for illustrations
