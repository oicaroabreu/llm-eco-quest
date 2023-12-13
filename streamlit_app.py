import os
import streamlit as st
import litellm
import time

litellm.set_verbose = True

st.set_page_config(page_title="🌿 EcoQuest 🌿")

st.title("A Solarpunk Future!")


def get_assistant_response():

    response = litellm.completion(
        model="ollama/llama2:13b",
        messages=st.session_state.messages,
        api_base="http://localhost:11434",
        max_tokens=400,
    )
    print(response)
    return response.choices[0].message.content


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
                - Award points and quick recognition for successful solutions with a '🌿CONGRATULATIONS🌿' message after the player's first somewhat satisfying proposal.
                - Integrate educational content for real-world relevance and learning.

                SUPER IMPORTANT:
                - Stimulate player interaction by encouraging questions and exploration.
                - Provide constructive feedback on solutions, guiding players without being overly directive.
                - Balance the difficulty based on player interaction and responses.

                Player Interaction:
                - Encourage players to propose initial solutions and expand upon them.
                - Quickly acknowledge effective ideas with positive reinforcement.

                Dificulty:
                - Easy, for children

                Goal:
                - Educate and engage players in sustainable thinking and action.

                Responses:
                - Short responses, to deepen the knoledge, recommend research points after the `🌿CONGRATULATIONS🌿` message.
                
                First Challenge:
                - Present a unique local level eco challenge focused on a specific environmental issue.
                - Address a critical issue like water pollution in a river.
                - Encourage initial problem-solving ideas from the player.
                - Promptly reward effective solutions with a '🌿CONGRATULATIONS🌿' message to reinforce positive learning and progression."""
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
            assistant_response = get_assistant_response()
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
