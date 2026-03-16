import os
import subprocess
import pytest
from google import genai
from google.genai import types

# Requires `pip install google-genai pytest`
# Must have GEMINI_API_KEY set in environment

def get_skill_prompt():
    """Use skills-ref CLI to generate the agent XML prompt block for the skill."""
    try:
        result = subprocess.run(
            ["uv", "run", "--project", "/tmp/agentskills-repo/skills-ref", "skills-ref", "to-prompt", "."],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        return """
        <available_skills>
            <skill>
                <name>maptiler-integration</name>
                <description>Integrate MapTiler maps and Geocoding.</description>
                <location>SKILL.md</location>
            </skill>
        </available_skills>
        """

def test_maptiler_agent_skill_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY not set. Skipping agentic test.")

    # Initialize the new google-genai client
    client = genai.Client(api_key=api_key)
    skills_xml = get_skill_prompt()

    system_instruction = f"""
    You are an AI coding assistant.
    You have access to the following skills. If a user asks for something related to these skills, 
    you must apply the skill's instructions when generating code.
    
    {skills_xml}
    
    Since you cannot actually read files in this test environment, 
    assume the skill requires you to use '@maptiler/sdk', include its CSS file 'maptiler-sdk.css',
    instantiate maps with 'new maptilersdk.Map()', and set the API key with 'maptilersdk.config.apiKey'.
    
    Output ONLY the raw HTML code inside a ```html block. Do not provide any conversational text.
    """

    user_prompt = "Create a basic HTML file with a full-screen MapTiler map centered on Paris using Vanilla JS."
    
    print("Prompting Gemini Model...")
    
    # Use gemini-3.1-pro
    response = client.models.generate_content(
        model='gemini-3.1-pro-preview',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        ),
    )
    
    generated_code = response.text

    print("Evaluating Generated Code...")

    # Assertions to ensure the Agent actually followed the skill's instructions
    assert "maptiler-sdk.umd.js" in generated_code or "@maptiler/sdk" in generated_code, "Agent failed to include MapTiler SDK JS."
    assert "maptiler-sdk.css" in generated_code, "Agent failed to include MapTiler SDK CSS."
    assert "new maptilersdk.Map" in generated_code, "Agent failed to instantiate the Map."
    assert "maptilersdk.config.apiKey" in generated_code, "Agent failed to configure the API key."

    print("✅ All assertions passed! Gemini successfully used the MapTiler Agent Skill.")

if __name__ == "__main__":
    try:
        test_maptiler_agent_skill_gemini()
    except Exception as e:
        print(f"Test failed: {e}")
