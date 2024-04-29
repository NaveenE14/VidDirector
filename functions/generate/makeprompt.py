
def generate_prompts(text):
    image_prompts = []
    narrator_prompts = []
    paragraphs = text.split('\n')

    current_prompt_type = None
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph.startswith("Image:"):
            current_prompt_type = "Image Prompts"
            paragraph = paragraph[len("Image: "):]
            image_prompts.append(paragraph)
        elif paragraph.startswith("Narrator:"):
            current_prompt_type = "Narrator Prompts"
            paragraph = paragraph[len("Narrator: "):]
            narrator_prompts.append(paragraph)

    image_prompts = [prompt for prompt in image_prompts if prompt.strip()]
    narrator_prompts = [prompt for prompt in narrator_prompts if prompt.strip()]

    return image_prompts, narrator_prompts
