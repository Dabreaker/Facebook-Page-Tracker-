import os
import time
import random
import argparse
import re
import cv2
import subprocess
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from rich.console import Console

console = Console()

# Environment Constants
CHROME_BIN = "/data/data/com.termux/files/usr/bin/chromium-browser"
DRIVER_BIN = "/data/data/com.termux/files/usr/bin/chromedriver"

class DeepMiner:
    def __init__(self, target_url, cookie_path):
        self.target_url = target_url
        self.cookie_path = os.path.expanduser(cookie_path)
        self.target_id = self._get_target_id(target_url)
        self.page_dir = os.path.join(os.getcwd(), re.sub(r'[^a-zA-Z0-9]', '_', self.target_id))
        self.processed = set()
        
        if not os.path.exists(self.page_dir):
            os.makedirs(self.page_dir)

    def _get_target_id(self, url):
        if 'id=' in url: return url.split('id=')[-1].split('&')[0]
        return url.rstrip('/').split('/')[-1]

    def _init_driver(self):
        options = Options()
        options.binary_location = CHROME_BIN
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1080,1920")
        return webdriver.Chrome(service=Service(executable_path=DRIVER_BIN), options=options)

    def inject_cookies(self, driver):
        try:
            with open(self.cookie_path, 'r') as f:
                for line in f:
                    if not line.strip() or line.startswith('#'): continue
                    p = line.split('\t')
                    if len(p) < 7: continue
                    driver.add_cookie({
                        'name': p[5], 
                        'value': p[6].strip(), 
                        'domain': p[0], 
                        'path': p[2], 
                        'secure': p[3] == 'TRUE'
                    })
            console.print("[green]✓ Cookies Injected.[/green]")
        except Exception as e:
            console.print(f"[red]✗ Cookie Injection Failed: {e}[/red]")

    def precision_click_debug(self, driver, target_text):
        try:
            element = driver.find_element(By.XPATH, f"//*[contains(text(), '{target_text}')]")
            if element.is_displayed():
                loc, size = element.location, element.size
                jx, jy = random.uniform(-5, 5), random.uniform(-5, 5)
                
                scr = driver.get_screenshot_as_png()
                img = cv2.imdecode(np.frombuffer(scr, np.uint8), cv2.IMREAD_COLOR)
                abs_x = int(loc['x'] + (size['width']/2) + jx)
                abs_y = int(loc['y'] + (size['height']/2) + jy)
                cv2.circle(img, (abs_x, abs_y), 20, (0, 0, 255), -1)
                cv2.imwrite(os.path.join(self.page_dir, "last_click_debug.png"), img)
                
                ActionChains(driver).move_to_element_with_offset(element, jx, jy).click().perform()
                console.print(f"[bold yellow]🎯 Action Performed: {target_text}[/bold yellow]")
                return True
        except: return False

    def execute(self):
        driver = self._init_driver()
        try:
            driver.get("https://web.facebook.com")
            self.inject_cookies(driver)
            
            while True:
                console.print(f"\n[bold magenta]Scanning Target: {self.target_id}[/bold magenta]")
                driver.get(self.target_url)
                time.sleep(6)
                self.precision_click_debug(driver, "Continue as")
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)

                elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'fbid=') or contains(@href, '/reels/') or contains(@href, '/photos/')]")
                
                queue = []
                for e in elements:
                    href = e.get_attribute("href")
                    if href and self.target_id in href:
                        clean = href.split('&__tn__')[0].split('?')[0] if 'fbid' not in href else href.split('&__tn__')[0]
                        if clean not in self.processed:
                            self.processed.add(clean)
                            queue.append(clean)

                for link in queue:
                    self._process_item(driver, link)

                console.print(f"[dim]Cycle Complete. Total items: {len(self.processed)}. Sleeping 30s...[/dim]")
                time.sleep(30)
        finally:
            driver.quit()

    def _process_item(self, driver, link):
        pid = link.split('fbid=')[-1].split('&')[0] if 'fbid=' in link else link.rstrip('/').split('/')[-1]
        console.print(f"[cyan]Mining Content: {pid}[/cyan]")

        driver.execute_script(f"window.open('{link}');")
        driver.switch_to.window(driver.window_handles[1])
        self.inject_cookies(driver)
        time.sleep(10)
        
        self.precision_click_debug(driver, "Continue as")
        driver.save_screenshot(os.path.join(self.page_dir, f"{pid}.png"))
        
        try:
            text = driver.find_element(By.TAG_NAME, "body").text[:1000]
        except: text = "N/A"
        
        with open(os.path.join(self.page_dir, f"{pid}.txt"), "w") as f:
            f.write(f"ID: {pid}\nURL: {link}\n\n{text}")

        if any(x in link for x in ['reels', 'videos', 'watch']):
            out = os.path.join(self.page_dir, f"{pid}.%(ext)s")
            subprocess.run(["yt-dlp", "--cookies", self.cookie_path, "-o", out, link], capture_output=True)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep Miner - High Precision Page Tracker")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-c", "--cookies", required=True, help="Path to Netscape cookies.txt")
    args = parser.parse_args()
    
    miner = DeepMiner(args.url, args.cookies)
    miner.execute()
