import os
import streamlit as st
import litellm
import time
import asyncio
from pprint import pprint

litellm.set_verbose = True

st.set_page_config(page_title="🌿 EcoQuest 🌿")

with st.sidebar:
    st.title("🌿 EcoQuest 🌿")
    st.subheader('A Solarpunk Future!')
    st.write('An interactive, text-based game designed to inspire and educate players about environmental sustainability and the solarpunk movement.')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('OpenAI key already provided!', icon='✅')
        openai_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_key = st.text_input('Enter OpenAI API token:', type='password')
        
        if not (openai_key and len(openai_key) > 0):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Now go play the game!!', icon='👉')
    os.environ['OPENAI_API_KEY'] = openai_key

    st.markdown('📖 Access our [Github Repository](https://github.com/oicaroabreu/llm-eco-quest/)!')



async def get_assistant_response(placeholder):

    response = await litellm.acompletion(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        max_tokens=400,
        stream=True
    )
    full_response = ""
    async for chunk in response:
        pprint(chunk)
        full_response += str(chunk['choices'][0]['delta']['content'])
        time.sleep(0.05)
        placeholder.markdown(full_response)

    return full_response


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """Welcome to EcoQuest, a game of environmental problem-solving as a Solarpunk Master. Each level, Local, Regional, and Global, presents unique challenges that require thoughtful and creative solutions.
                Game Logic:
                - Introduce a series of environmental challenges at different scales.
                - Limit to three challenges per level(Local, Regional, and Global) to maintain focus and engagement.
                - Ensure challenges are unique and randomized for diverse experiences.
                - Encourage creative and sustainable problem-solving from the player.
                - Use markdown for engaging content presentation.
                - Integrate educational content for real-world relevance and learning.

                First Challenge:
                - Present a unique local level eco challenge focused on a specific environmental issue.
                - Address a local level critical issue with important details to guide resolution.
                - Encourage initial problem-solving ideas from the player.
                - Promptly reward effective solutions with a '🌿CONGRATULATIONS🌿' message to reinforce positive learning and progression and ask if the player wants a new local challenge or move up to regional.
                
                 Second Challenge:
                - Present a unique regional level eco challenge focused on a specific environmental issue.
                - Address a regional level critical issue with important details to guide resolution.
                - Encourage initial problem-solving ideas from the player.
                - Promptly reward effective solutions with a '🌿CONGRATULATIONS🌿' message to reinforce positive learning and progression and ask if the player wants a new regional challenge or move up to regional.

                Third Challenge:
                - Present a unique local level eco challenge focused on a specific environmental issue.
                - Address a global level critical issue with important details to guide resolution.
                - Encourage initial problem-solving ideas from the player.
                - Promptly reward effective solutions with a '🌿CONGRATULATIONS🌿' message to reinforce positive learning and progression and give the player the title of SolarPunk Master.

                Player Interaction:
                - Encourage players to propose initial solutions and expand upon them.
                - Quickly acknowledge effective ideas with positive reinforcement.

                Dificulty:
                - Easy, for children

                Goal:
                - Educate and engage players in sustainable thinking and action.

                Responses:
                - Short responses, to deepen the knoledge, recommend research points after the `🌿CONGRATULATIONS🌿` message.
                
                SUPER IMPORTANT:
                - Stimulate player interaction by encouraging questions and exploration.
                - Provide constructive feedback on solutions, guiding players without being overly directive.
                - Balance the difficulty based on player interaction and responses.
                - Do not overexplain the mechanics of the game
                """
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            placeholder = st.empty()
            assistant_response = asyncio.run(get_assistant_response(placeholder))
            placeholder.markdown(assistant_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )


user_input = st.chat_input(">")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    time.sleep(0.1)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()
