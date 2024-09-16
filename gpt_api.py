# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

search_query = [
    {
        "text": "A chic interior and medley of innovative cocktails guaranteed at Artesian. Named after the original, 360-feet deep well under the hotel, the award-winning bar is perfect for celebrations, after-work tipples or an indulgent nightcap.\n\nExciting food menu and a cocktail pairing experience which has been inspired by traditional Japanese dishes and meticulously researched ingredients that show remarkable sustainability and versatility."
    },
    {
        "text": "We decided to stop by for a drink on our way to dinner. And they certainly did not disappoint. The cocktails were just made to perfection. Looks amazing and taste great! And with the great service as expected from a 5 star hotel. Off course, expect the price tag to go with it 😁"
    },
    {
        "text": "I love the vibe of Artesian, the decor looks great especially the bar area.\n\nAnd the cocktails were amazing. I’ve tried the old fashioned from signature menu, it was nice and funny. My friend kept saying it looked like Chinese soup with soils LOL. And then I’ve ordered penicillin which is my favourite. It’s another good one in London. It’s smoky, fresh and gingery. It definitely surprised me.\n\nOther than that, the service was great! The waiters are very thoughtful and caring. And they served us the birthday drinks as well. I will definitely go back for the service and cocktails."
    },
    {
        "text": "Opened in 1865 as Europe’s first ‘Grand Hotel’, The Langham, London is situated in the Marylebone district on Langham Place. Within The Langham is Artesian Bar, which was named the best bar in the world for 4 years in a row starting in 2012. Known for its lavish interior and eye-catching purple leather chairs, Artesian is currently led by the charismatic Giulia Cuccurullo. Her team’s current menu Ingredients of the Future, was a finalist for the 2023 Los Siete Misterios Best Cocktail Menu Award by the World’s 50 Best Bars. Each cocktail on the menu highlights a single and sometimes unusual ingredient. For example, Insects is a smoky whiskey sour featuring Michter’s bourbon, Campari, Nixta Corn Liqueur, chicatanas, coffee, lime and crickets. Other than world class drinks and hospitality, Artesian has some of the best bar food in London thanks to a collaboration with Angelo Sato of Humble Chicken in Soho. A must are the buttermilk chicken karaage with spicy miso mayo."
    },
    {
        "text": "Cosy place, great service and the cocktails are all amazing. No doubt I will come back again next time I am in london."
    }
]


response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": f"I am going to pass a JSON object with some reviews of a place from Google Places. Generate a single summary made from the following reviews: {search_query}"},
    ],
    temperature=0,
)

prompt_response = response.choices[0].message.content


if __name__ == '__main__':
    print(prompt_response)
