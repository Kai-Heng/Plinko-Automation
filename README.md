# Plinko-Automation

### **📌 Plinko Automation Bot**
#### **Automated Plinko Betting Bot for Stake.us**
This project automates betting on the Plinko game on Stake.us using **Selenium** with **Undetected ChromeDriver**, allowing for automated gameplay, dynamic bet adjustments, and session management via cookies.

---

## **🚀 Features**
✅ **Automated Betting** – Places bets based on dynamic calculations.  
✅ **Target Balance Control** – Set a stop condition to halt automation when a balance is reached.  
✅ **Hotkey Support** – Press `p` to pause/resume betting dynamically.  
✅ **Cookie Management** – Saves and loads login cookies to avoid repeated logins.  
✅ **Bet Logging** – Saves betting history in a CSV file for later analysis.  
✅ **Audio Muting** – Disables site audio for silent execution.  

---

## **🛠️ Setup Instructions**
### **1️⃣ Install Dependencies**
Ensure you have **Python 3.8+** installed, then install the required packages:
```bash
pip install -r requirements.txt
```
---
### **2️⃣ Run the Script**
Run the automation script with:
```bash
python main.py
```
> **Note:** If you are on **macOS**, run it with `sudo` to enable keyboard hotkeys:
```bash
sudo python main.py
```

---

### **3️⃣ How to Use**
1️⃣ **Login to Stake.us** [First-Time] (Manually).  
2️⃣ **Press "Enter"** when logged in and on the Plinko page.  
3️⃣ **Set a target balance** (Automation stops once reached).  
4️⃣ **Use `p`** to **pause/resume** automation dynamically.  

---
## **🔑 Hotkeys**
| Key  | Action |
|------|--------|
| `p` | Pause/Resume betting automation |

---
## **📂 Log File (Bet Tracking)**
All bets are saved in a CSV file:  
📁 **`plinko_log.csv`**
```
Bet Number, Bet Amount, Wallet Balance
1, 4.78, 4786.33
2, 4.77, 4781.54
...
```

---
## **🔧 Configuration Options**
You can modify the script to:
- **Change betting strategy** (Modify the percentage calculation in the `stake_plinko_automation()` function).
- **Enable/Disable headless mode** (Uncomment `options.add_argument("--headless")` in `main.py`).
- **Adjust betting frequency** (`time.sleep(0.005)` can be changed for faster/slower execution).

---
## **📌 Dependencies**
- **Python 3.8+**
- `selenium`
- `undetected_chromedriver`
- `pickle` (For saving/loading cookies)
- `csv` (For logging bets)

---
## **💡 Future Improvements**
✅ Implement **profit/loss tracking**  
✅ Add **multi-threaded logging** for real-time bet visualization  
✅ Introduce **betting multipliers** based on past win/loss trends  

---
## **⚠️ Disclaimer**
⚠ **Use this bot responsibly.** Gambling comes with risks. This project is intended for educational purposes only. **The developer is not responsible for any financial losses.**  

---
## **📜 License**
This project is licensed under the **MIT License**. Feel free to modify and distribute it.

---
## **🤝 Contributing**
1. Fork the repo.  
2. Create a new branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Added feature"`).  
4. Push to your branch (`git push origin feature-name`).  
5. Open a **Pull Request**.  
