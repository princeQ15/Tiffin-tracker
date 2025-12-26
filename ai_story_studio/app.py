from flask import Flask, render_template, request
import random

app = Flask(__name__)

def generate_story(title, topic, main_character, setting, moral):
    story_templates = [
        f"""# {title}

In the heart of {setting}, where the air was filled with magic, lived a young {main_character}. The story of {main_character} and the {topic} has been passed down through generations, teaching us all about the importance of {moral}.

{main_character} had always been fascinated by {topic}, spending hours exploring every corner of {setting} in search of new discoveries. The people of {setting} often wondered what drove {main_character} to be so curious about {topic}, but they would soon understand.

One day, while wandering through the ancient woods near {setting}, {main_character} stumbled upon something extraordinary - a hidden glade where {topic} grew in abundance. The air shimmered with an otherworldly glow as {main_character} reached out to touch the nearest {topic}.

As days passed, {main_character} learned that the {topic} held a special power - they could show glimpses of the future. But with this power came a great responsibility. The moral of this story is clear: {moral}. {main_character} knew that some things are better left to unfold naturally.

In the end, {main_character} made the difficult decision to let the {topic} be, understanding that the true magic lay not in knowing what's to come, but in experiencing each moment as it happens. And so, {main_character} returned to {setting}, forever changed by the wisdom gained from the magical {topic}.""",

        f"""# {title}

Long ago in the land of {setting}, there was a brave soul named {main_character}. This is the tale of how {main_character} discovered the true meaning of {moral} through the power of {topic}.

Unlike others in {setting}, {main_character} was drawn to the mysteries of {topic}, spending countless hours studying ancient texts and forgotten lore. While most dismissed {topic} as mere legend, {main_character} sensed there was more to the stories.

One fateful evening, as the twin moons rose over {setting}, {main_character} discovered an ancient prophecy about {topic} that would change everything. The prophecy spoke of a great challenge that only someone pure of heart could overcome.

Through trials that tested courage, wisdom, and compassion, {main_character} learned that {moral}. This lesson became the key to unlocking the true power of {topic}, not to control or possess it, but to understand and protect it.

Years later, people would tell stories of how {main_character} saved {setting} by embracing the true meaning of {moral}, proving that even the smallest act of kindness could change the course of history.""",

        f"""# {title}

In the bustling city of {setting}, where the streets hummed with energy and the air smelled of possibility, lived {main_character}. This is a story about {topic}, {main_character}'s greatest adventure, and the timeless lesson of {moral}.

While others chased after gold and glory, {main_character} was captivated by the mysteries of {topic}. Where others saw only ordinary things, {main_character} saw endless possibilities and hidden meanings in the world of {topic}.

One rainy afternoon, while seeking shelter in an old bookstore, {main_character} found a peculiar book about {topic}. The shopkeeper, an elderly woman with knowing eyes, whispered, 'This book chooses its reader as much as the reader chooses it.'

As {main_character} delved deeper into the book's pages, they discovered that {moral}. This revelation transformed how {main_character} saw the world and their place in it.

The story of {main_character}'s journey through the pages of that magical book became legend in {setting}, teaching generations that {moral} isn't just a lesson, but a way of life. And so, the legacy of {main_character} and the power of {topic} lived on, inspiring all who heard the tale."""
    ]
    return random.choice(story_templates)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form.get('title', 'My Amazing Story').strip()
    topic = request.form.get('topic', '').strip()
    main_character = request.form.get('main_character', 'the hero').strip()
    setting = request.form.get('setting', 'a magical land').strip()
    moral = request.form.get('moral', 'with great power comes great responsibility').strip()
    
    if not all([title, topic, main_character, setting, moral]):
        return render_template('index.html', 
                            error="Please fill in all fields",
                            title=title,
                            topic=topic,
                            main_character=main_character,
                            setting=setting,
                            moral=moral)
    
    story_text = generate_story(title, topic, main_character, setting, moral)
    return render_template('story.html', story_text=story_text)

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')