import streamlit as st
import requests
import json
import traceback

# Page config
st.set_page_config(page_title="What's In A Name", page_icon="🎭", layout="wide")

st.title("🎭 What's In A Name?")
st.write("Enter a name and discover interesting facts about it!")

# Input field
name = st.text_input("Enter a name:", placeholder="e.g., Shakespeare, Einstein, etc.")

if name:
    st.write("---")
    
    # Show loading spinner
    with st.spinner("Generating fun facts..."):
        try:
            # Debug: Show what we're working with
            with st.expander("Debug Info (click to expand)", expanded=False):
                try:
                    api_key = st.secrets["GROQ_API_KEY"]
                    st.write(f"✅ API Key loaded: {api_key[:10]}...")
                except KeyError:
                    st.error("❌ GROQ_API_KEY not found in secrets!")
                    st.stop()
                except Exception as e:
                    st.error(f"❌ Error accessing secrets: {e}")
                    st.stop()
            
            # Prepare the API request
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-oss-20b",  # Using the model from your working curl
                "messages": [
                    {
                        "role": "user",
                        "content": f"Tell me 3 interesting and fun facts about the name '{name}'. Include historical significance, famous people with this name, or cultural meanings. Keep it engaging and informative."
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            # Debug: Show request details
            with st.expander("Request Details", expanded=False):
                st.json({
                    "url": url,
                    "model": payload["model"],
                    "prompt_preview": payload["messages"][0]["content"][:100] + "..."
                })
            
            # Make the API request
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # Debug: Show response status
            st.write(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Debug: Show raw response
                with st.expander("Raw API Response", expanded=False):
                    st.json(result)
                
                # Extract and display the content
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    
                    st.subheader(f"Fun Facts about '{name}':")
                    st.write(content)
                    
                    # Show token usage if available
                    if "usage" in result:
                        with st.expander("Usage Info", expanded=False):
                            st.json(result["usage"])
                else:
                    st.error("❌ No content found in API response")
                    st.json(result)
                    
            elif response.status_code == 401:
                st.error("❌ Authentication failed! Please check your API key.")
                st.write(f"API Key being used: {st.secrets['GROQ_API_KEY'][:10]}...")
                
            elif response.status_code == 429:
                st.error("❌ Rate limit exceeded. Please wait and try again.")
                
            elif response.status_code == 400:
                st.error("❌ Bad request. Check the model name or request format.")
                try:
                    error_detail = response.json()
                    st.json(error_detail)
                except:
                    st.text(response.text)
                    
            else:
                st.error(f"❌ API request failed with status code: {response.status_code}")
                try:
                    error_detail = response.json()
                    st.json(error_detail)
                except:
                    st.text(response.text)
                    
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection error. Please check your internet connection.")
            
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON decode error: {e}")
            st.text(f"Raw response: {response.text if 'response' in locals() else 'No response'}")
            
        except KeyError as e:
            st.error(f"❌ Missing key in secrets: {e}")
            st.write("Make sure you have GROQ_API_KEY in your .streamlit/secrets.toml file")
            
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            st.text("Full error traceback:")
            st.text(traceback.format_exc())

# Instructions
st.write("---")
st.write("### Setup Instructions:")
st.write("1. Create a `.streamlit/secrets.toml` file in your project")
st.write("2. Add your Groq API key:")
st.code('GROQ_API_KEY = "your_groq_api_key_here"')
st.write("3. Make sure the key starts with 'gsk_'")

# Test section
st.write("---")
st.write("### Quick Test:")
if st.button("Test API Connection"):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        if api_key.startswith("gsk_"):
            st.success("✅ API key format looks correct!")
        else:
            st.warning("⚠️ API key doesn't start with 'gsk_' - this might be incorrect")
    except KeyError:
        st.error("❌ GROQ_API_KEY not found in secrets!")
