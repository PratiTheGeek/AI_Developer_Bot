import streamlit as st
import requests
st.set_page_config(page_title="Developer Documentation Bot")
st.title("Developer Documentation Bot :robot_face:")
user_question=st.text_input("Ask a question from the provided document:")
if st.button("Ask the Bot") and user_question.strip():
    n8n_webhook_url = "https://madhuriiiii.app.n8n.cloud/webhook-test/chatbot"

    try:
        with st.spinner("Getting response from the bot..."):
            response=requests.get(n8n_webhook_url, params={"question": user_question})
            if response.status_code==200:
                data=response.json()
                st.markdown(f"**Answer:** {data['response']}")
                
            else:
                st.error("Error in getting response from the bot. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
