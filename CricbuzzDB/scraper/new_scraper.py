import os
import time
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION: 10 MATCHES ---
MATCH_LIST = [
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/121406/ind-vs-nz-3rd-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/live-cricket-scores/121406/ind-vs-nz-3rd-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/cricket-match-squads/121406/ind-vs-nz-3rd-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/cricket-match-facts/121406/ind-vs-nz-3rd-t20i-new-zealand-tour-of-india-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/121389/ind-vs-nz-1st-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/live-cricket-scores/121389/ind-vs-nz-1st-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/cricket-match-squads/121389/ind-vs-nz-1st-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/cricket-match-facts/121389/ind-vs-nz-1st-t20i-new-zealand-tour-of-india-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/121400/ind-vs-nz-2nd-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/live-cricket-scores/121400/ind-vs-nz-2nd-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/cricket-match-squads/121400/ind-vs-nz-2nd-t20i-new-zealand-tour-of-india-2026",
        "https://www.cricbuzz.com/cricket-match-facts/121400/ind-vs-nz-2nd-t20i-new-zealand-tour-of-india-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/133011/sl-vs-eng-2nd-odi-england-tour-of-sri-lanka-2026",
        "https://www.cricbuzz.com/live-cricket-scores/133011/sl-vs-eng-2nd-odi-england-tour-of-sri-lanka-2026",
        "https://www.cricbuzz.com/cricket-match-squads/133011/sl-vs-eng-2nd-odi-england-tour-of-sri-lanka-2026",
        "https://www.cricbuzz.com/cricket-match-facts/133011/sl-vs-eng-2nd-odi-england-tour-of-sri-lanka-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/133000/sl-vs-eng-1st-odi-england-tour-of-sri-lanka-2026",
        "https://www.cricbuzz.com/live-cricket-scores/133000/sl-vs-eng-1st-odi-england-tour-of-sri-lanka-2026",
        "https://www.cricbuzz.com/cricket-match-squads/133000/sl-vs-eng-1st-odi-england-tour-of-sri-lanka-2026",
        "https://www.cricbuzz.com/cricket-match-facts/133000/sl-vs-eng-1st-odi-england-tour-of-sri-lanka-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/140559/ire-vs-ita-3rd-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/live-cricket-scores/140559/ire-vs-ita-3rd-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-squads/140559/ire-vs-ita-3rd-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-facts/140559/ire-vs-ita-3rd-t20i-ireland-vs-italy-in-uae-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/140548/ire-vs-ita-2nd-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/live-cricket-scores/140548/ire-vs-ita-2nd-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-squads/140548/ire-vs-ita-2nd-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-facts/140548/ire-vs-ita-2nd-t20i-ireland-vs-italy-in-uae-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/140537/ire-vs-ita-1st-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/live-cricket-scores/140537/ire-vs-ita-1st-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-squads/140537/ire-vs-ita-1st-t20i-ireland-vs-italy-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-facts/140537/ire-vs-ita-1st-t20i-ireland-vs-italy-in-uae-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/137831/afg-vs-wi-3rd-t20i-afghanistan-v-west-indies-in-uae-2026",
        "https://www.cricbuzz.com/live-cricket-scores/137831/afg-vs-wi-3rd-t20i-afghanistan-v-west-indies-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-squads/137831/afg-vs-wi-3rd-t20i-afghanistan-v-west-indies-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-facts/137831/afg-vs-wi-3rd-t20i-afghanistan-v-west-indies-in-uae-2026"
    ],
    [
        "https://www.cricbuzz.com/live-cricket-scorecard/137826/afg-vs-wi-2nd-t20i-afghanistan-v-west-indies-in-uae-2026",
        "https://www.cricbuzz.com/live-cricket-scores/137826/afg-vs-wi-2nd-t20i-afghanistan-v-west-indies-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-squads/137826/afg-vs-wi-2nd-t20i-afghanistan-v-west-indies-in-uae-2026",
        "https://www.cricbuzz.com/cricket-match-facts/137826/afg-vs-wi-2nd-t20i-afghanistan-v-west-indies-in-uae-2026"
    ]
    # Add more match sets here
]

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def init_driver():
    print("Initializing Chrome Driver...")
    return webdriver.Chrome(options=options)

def get_folder_name(scorecard_url):
    match_id = re.search(r'/(\d+)/', scorecard_url).group(1)
    slug = scorecard_url.split(match_id + "/")[1]
    slug = slug.replace("-", "")
    return f"{match_id}_{slug}"

def get_text_by_label(soup, label_text):
    label = soup.find(string=lambda x: x and label_text in x)
    if label:
        parent = label.find_parent('div')
        if parent:
            val = parent.find_next_sibling('div')
            if val: return val.text.strip()
    return "N/A"

def scrape_result(driver, url, output_dir):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    status = soup.find('div', class_='text-cbTextLink')
    res_text = status.text.strip() if status else "N/A"
    
    # Capture Score Details via XPath
    def get_xpath_text(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return "N/A"

    t1_code = get_xpath_text("/html/body/div/main/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]")
    t2_code = get_xpath_text("/html/body/div/main/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]")
    t1_score = get_xpath_text("/html/body/div/main/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[2]")
    t2_score = get_xpath_text("/html/body/div/main/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[2]")

    pom_text = "N/A"
    pom_label = soup.find(string=re.compile("PLAYER OF THE MATCH", re.IGNORECASE))
    if pom_label:
        try:
            pom_span = pom_label.find_parent('div').find_next('span')
            if pom_span: pom_text = pom_span.text.strip()
        except: pass

    data = [{
        "Result": res_text, 
        "Player of Match": pom_text,
        "Team 1 name code": t1_code,
        "Team 2 name code": t2_code,
        "Team 1 Score": t1_score,
        "Team 2 Score": t2_score
    }]
    pd.DataFrame(data).to_csv(f'{output_dir}/match_result.csv', index=False)

def scrape_scorecard(driver, url, output_dir):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    batting, bowling = [], []
    
    grids = soup.find_all('div', class_=lambda c: c and ('scorecard-bat-grid' in c or 'cb-scrd-itms' in c))
    for row in grids:
        link = row.find('a', href=lambda x: x and '/profiles/' in x)
        if link:
            cols = [c.text.strip() for c in row.find_all('div') if c.text.strip()]
            nums = [c for c in cols if c.replace('.','',1).isdigit()]
            if len(nums) >= 4:
                batting.append({"Player": link.text.strip(), "Runs": nums[0], "Balls": nums[1], "4s": nums[2], "6s": nums[3]})
    
    bowl_grids = soup.find_all('div', class_=lambda c: c and ('scorecard-bowl-grid' in c or 'cb-scrd-itms' in c))
    for row in bowl_grids:
        link = row.find('a', href=lambda x: x and '/profiles/' in x)
        if link:
            cols = [c.text.strip() for c in row.find_all('div') if c.text.strip()]
            nums = [c for c in cols if c.replace('.','',1).isdigit()]
            if len(nums) >= 4:
                bowling.append({"Bowler": link.text.strip(), "Overs": nums[0], "Runs": nums[2], "Wickets": nums[3]})
    
    pd.DataFrame(batting).to_csv(f'{output_dir}/batting_scorecard.csv', index=False)
    pd.DataFrame(bowling).to_csv(f'{output_dir}/bowling_scorecard.csv', index=False)

def scrape_info(driver, url, output_dir):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    info_data = []
    labels = ["Match", "Date", "Toss", "Time", "Venue", "Umpires", "3rd Umpire", "Referee", "City", "Capacity"]
    for lbl in labels:
        tag = soup.find('div', string=re.compile(f"^{lbl}", re.IGNORECASE))
        if tag:
            val = tag.find_next_sibling('div')
            if val: info_data.append({"Info": lbl, "Value": val.text.strip()})
    pd.DataFrame(info_data).to_csv(f'{output_dir}/info_segment.csv', index=False)

def scrape_playing_xi_profiles(driver, url, output_dir):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    xi_map = {}
    
    links = soup.find_all('a', href=re.compile(r'/profiles/\d+/'))
    for link in links:
        name = re.sub(r"\(.*?\)|,", "", link.text).strip()
        p_url = "https://www.cricbuzz.com" + link['href']
        if name and name not in xi_map and len(xi_map) < 22:
            xi_map[name] = p_url

    profiles = []
    for name, p_url in xi_map.items():
        driver.get(p_url)
        time.sleep(1)
        p_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Capture Team Name via XPath
        team_name = "N/A"
        try:
            team_element = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/span")
            team_name = team_element.text.strip()
        except: pass

        profiles.append({
            "Name": name,
            "Team": team_name,
            "Born": get_text_by_label(p_soup, "Born"),
            "Role": get_text_by_label(p_soup, "Role"),
            "Batting Style": get_text_by_label(p_soup, "Batting Style"),
            "Bowling Style": get_text_by_label(p_soup, "Bowling Style")
        })
    pd.DataFrame(profiles).to_csv(f'{output_dir}/playing_11_profiles_detailed.csv', index=False)

def main():
    driver = init_driver()
    try:
        for idx, match_set in enumerate(MATCH_LIST):
            if not match_set: continue
            score_url, result_url, squad_url, facts_url = match_set
            base_dir = "matches"
            os.makedirs(base_dir, exist_ok=True)

            folder_name = os.path.join(base_dir, get_folder_name(score_url))
            os.makedirs(folder_name, exist_ok=True)

            
            print(f"\nðŸ   Processing Match {idx+1}: {folder_name}")
            scrape_result(driver, result_url, folder_name)
            scrape_scorecard(driver, score_url, folder_name)
            scrape_info(driver, facts_url, folder_name)
            scrape_playing_xi_profiles(driver, squad_url, folder_name)
            print(f"âœ… Match {idx+1} Complete.")
    finally:
        driver.quit()
        print("\nAll tasks finished.")

if __name__ == "__main__":
    main()