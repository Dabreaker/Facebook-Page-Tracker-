<div align="center">

# 🛠️ DEEP-MINER v2.1
### **The Professional Data Mining Engine for Termux**

[![Author: Dabreakr](https://img.shields.io/badge/Author-Dabreakr-magenta?style=for-the-badge&logo=github)](https://github.com/Dabreakr)
[![Platform: Termux](https://img.shields.io/badge/Platform-Termux-orange?style=for-the-badge&logo=linux)](https://termux.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

<p align="left">
  Engineered for precision data extraction in <b>headless chromium environments</b>. 
  Deep-Miner automates the tracking of social feeds, media preservation, and session-based content scraping with military-grade efficiency.
</p>

</div>

---

## 🛡️ CREDITS & OWNERSHIP
> [!IMPORTANT]  
> **Core Engine Architect:** **Dabreakr** > This software is the intellectual property of **Dabreakr**. If you use this code or its logic, proper attribution to Dabreakr is strictly required.

---

## ⚠️ OPERATIONAL DOMAIN RESTRICTION
<div align="center">

| Requirement | Specification |
| :--- | :--- |
| **Execution Path** | `/data/data/com.termux/files/home/` |
| **Storage Type** | Internal Termux storage ONLY |
| **Forbidden Path** | `/sdcard` or Shared Storage |

</div>

> [!CAUTION]  
> **BINARY CONSTRAINTS:** This tool relies on the Termux-specific `chromium-browser` and `chromedriver` binaries. These drivers **cannot execute** from external storage due to Android's `noexec` mount flags. You **MUST** clone and run this project from your Termux home directory (`~`).

---

## 🚀 DEPLOYMENT PROTOCOL

### 1. Environment Initialization
```bash
# Return to the safe-zone (Home Directory)
cd ~

# Clone the repository
git clone [https://github.com/Dabreakr/deep-miner.git](https://github.com/Dabreakr/deep-miner.git)
cd deep-miner

# Grant execution permissions to setup script
chmod +x setup.sh

# Initialize system dependencies and drivers
./setup.sh
---



2. Mining Execution
python miner.py --url "[https://target-page.com](https://target-page.com)" --cookies "path/to/cookies.txt"

🏗️ SYSTEM ARCHITECTURE
<details>
<summary><b>View Internal Data Pipeline</b></summary>
 * Session Infiltration: Custom Netscape cookie injector for persistent auth.
 * Precision Clicker: OpenCV-backed coordinate mapping for UI interaction.
 * Data Vaulting:
   * [ID].png: Full-state visual capture.
   * [ID].txt: DOM body text extraction (1000ch).
   * [ID].mp4: Video stream recovery via yt-dlp integration.
 * Visual Debugging: Generates last_click_debug.png marking exactly where the automated click occurred with a 20px red dot.
</details>
📂 REPOSITORY STRUCTURE
 * miner.py: The core execution engine.
 * setup.sh: Automated dependency resolver (pkg & pip).
 * requirements.txt: Python module manifest.
 * .gitignore: Pre-configured to prevent your mined data and cookies from being leaked to public repositories.
📊 MINING WORKFLOW
graph TD
    A[Target URL Input] --> B{Cookie Injection}
    B --> C[Feed Scanner]
    C --> D[Queue New Post IDs]
    D --> E[Deep Mining Cycle]
    E --> F[Capture PNG / TXT]
    E --> G[Extract MP4 via yt-dlp]
    G --> H[Storage Vault]
    F --> H

<div align="center">


<b>Developed by Dabreakr</b>

<sub>"Mining data from the complex, one packet at a time."</sub>
</div>


