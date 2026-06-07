import streamlit as st
import requests
import uuid

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(
        uuid.uuid4()
    )
    
st.set_page_config(
    page_title="Annual Report Intelligence",
    page_icon="📊"
)

st.title("📊 Annual Report Intelligence")
st.caption("Ask questions about company annual reports")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input(
    "Ask a question..."
):

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"query": prompt,
                      "conversation_id":st.session_state.conversation_id
                      }
            )

            answer = response.json()["answer"]

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )