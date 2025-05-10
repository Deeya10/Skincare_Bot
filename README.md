# Skincare-Bot

A skincare assistant bot built with OpenAI's GPT-3.5 that helps users select the right skincare routine and products based on their skin type, concerns, and preferences.
The GPT-3.5 model is an advanced language model by OpenAI that generates human like text based on a given input (or prompt). 

You need to install the following dependencies:

- Streamlit for creating the web interface
- OpenAI Python library for interacting with the OpenAI API

### Setup OpenAI API Key

1. Get your API Key from your OpenAI account (you can find it in the API settings).
2. Create a `.env` file in the root of your project and add your API key: OPENAI_API_KEY=your_openai_api_key_here

 # Main Issues:

The GPT-3.5 model, like most large language models (LLMs), generates non-deterministic responses, meaning that each interaction may lead to different answers, even for the same input. This behavior can sometimes cause the bot to generate inconsistent or incomplete advice.
The chatbot might not always perform a comprehensive search through its knowledge base, leading to less accurate or relevant recommendations.

 ## Future Updates
 
1. **Account Integration**: Users can create accounts to save their profile and track their skincare routines across multiple sessions
2. **Upload Custom Datasets**:The ability to upload custom datasets (e.g., personal skin condition history or product reviews) to enhance the accuracy of recommendations.
3. **Better Handling of Non-Deterministic Responses**: Further prompt engineering and stability improvements to ensure consistent responses.

