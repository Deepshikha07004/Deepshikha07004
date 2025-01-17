import os
import requests

# Constants
GITHUB_USERNAME = "Deepshikha07004"
README_FILE = "README.md"
DEVICON_URL = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons"

# Social links
SOCIAL_LINKS = {
    "LinkedIn": "https://www.linkedin.com/in/deepshikha-dutta-98540b272/",
    "Twitter": "https://x.com/08_dutta39113",
    "GeeksforGeeks": "https://www.geeksforgeeks.org/user/deepshikhax5i5/",
    "LeetCode": "https://leetcode.com/u/user0449fy/"
}

# Function to fetch languages from GitHub repositories
def fetch_languages_and_tools(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repositories: {response.status_code}, {response.text}")
    
    languages = set()
    repos = response.json()
    
    for repo in repos:
        if repo.get("language"):
            languages.add(repo["language"])
    
    return languages

# Generate markdown for tools using Devicon
def generate_tools_section(languages):
    tools_md = ""
    
    # Language name to Devicon mapping (for inconsistencies)
    devicon_mapping = {
        "C++": "cplusplus",
        "C#": "csharp",
        "HTML": "html5",
        "CSS": "css3",
        "Jupyter Notebook": "jupyter",
        "Shell": "bash",
        # Add other custom mappings here if needed
    }
    
    for language in sorted(languages):
        # Normalize language names for Devicon
        devicon_name = devicon_mapping.get(language, language.lower().replace(" ", ""))
        icon_url = f"{DEVICON_URL}/{devicon_name}/{devicon_name}-original.svg"
        
        # Check if the icon exists in Devicon
        response = requests.get(icon_url)
        if response.status_code == 200:
            tools_md += (
                f'<img align="left" alt="{language}" width="30px" style="padding-right:10px;" '
                f'src="{icon_url}" />\n'
            )
        else:
            print(f"Icon not found for {language} ({devicon_name}), skipping.")
    
    return tools_md

# Generate markdown for social media links
def generate_social_section(social_links):
    social_md = "<div>\n"
    for platform, url in social_links.items():
        social_md += (
            f'  <a href="{url}" target="_blank">'
            f'    <img src="https://img.shields.io/badge/{platform}-{url.split("/")[-1]}?style=for-the-badge&logo={platform.lower()}&logoColor=white" alt="{platform}" />\n'
            f'  </a>\n'
        )
    social_md += "</div>\n"
    return social_md

# Generate markdown for GitHub Stats
def generate_github_stats(username):
    stats_md = f'''
    ![GitHub Stars](https://img.shields.io/github/stars/{username}?style=for-the-badge&color=FFD700)  
    ![GitHub Followers](https://img.shields.io/github/followers/{username}?style=for-the-badge&color=0E76A8)  
    ![GitHub Forks](https://github-readme-streak-stats.herokuapp.com?user={username}&theme=vue&hide_border=true)  

    ![{username}'s GitHub Stats](https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme=vue&bg_color=0066FF&title_color=FFFFFF&text_color=FFFFFF&icon_color=FFD700)  
    ![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme=vue&bg_color=0066FF&title_color=FFFFFF&text_color=FFFFFF&langs_count=100)
    '''
    return stats_md

# Update README.md with the generated sections
def update_readme(tools_section, social_section, stats_section):
    with open(README_FILE, "r") as file:
        content = file.read()

    # Replace the relevant sections in README
    tools_marker = "### 🔧 Tools"
    tools_start = content.find(tools_marker)
    if tools_start == -1:
        raise Exception(f"'{tools_marker}' section not found in README.md")
    
    tools_end = content.find("---", tools_start)
    if tools_end == -1:
        raise Exception("End of tools section not found in README.md")

    social_marker = "## 🌐 Connect with Me"
    social_start = content.find(social_marker)
    if social_start == -1:
        raise Exception(f"'{social_marker}' section not found in README.md")

    social_end = content.find("---", social_start)
    if social_end == -1:
        raise Exception("End of social section not found in README.md")

    stats_marker = "## 📊 GitHub Stats"
    stats_start = content.find(stats_marker)
    if stats_start == -1:
        raise Exception(f"'{stats_marker}' section not found in README.md")
    
    stats_end = content.find("---", stats_start)
    if stats_end == -1:
        raise Exception("End of stats section not found in README.md")

    # Insert the updated sections
    updated_content = (
        content[:tools_start]
        + f"{tools_marker}\n{tools_section}\n<br />\n\n"
        + content[tools_end: social_start]
        + f"{social_marker}\n{social_section}\n\n"
        + content[social_end: stats_start]
        + f"{stats_marker}\n{stats_section}\n"
        + content[stats_end:]
    )

    with open(README_FILE, "w") as file:
        file.write(updated_content)

if __name__ == "__main__":
    try:
        # Fetch languages and tools
        print("Fetching languages from GitHub repositories...")
        languages = fetch_languages_and_tools(GITHUB_USERNAME)

        # Generate tools section
        print("Generating tools section...")
        tools_section = generate_tools_section(languages)

        # Generate social section
        print("Generating social section...")
        social_section = generate_social_section(SOCIAL_LINKS)

        # Generate GitHub stats section
        print("Generating GitHub stats section...")
        stats_section = generate_github_stats(GITHUB_USERNAME)

        # Update README.md
        print("Updating README.md...")
        update_readme(tools_section, social_section, stats_section)

        print("README.md updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
