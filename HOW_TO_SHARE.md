# How to Share Your Project Locally 🌐

You can allow anyone connected to your **same WiFi/Local Network** to access your dashboard without needing to install anything on their computer.

## Step 1: Run the Project
1.  On your computer (the "Host"), double-click **`run_project.bat`**.
2.  Wait for the dashboard to launch in your browser.
3.  Keep the command prompt (terminal) window **OPEN**. Do not close it.

## Step 2: Find Your Network URL
Look at the text inside the command prompt window. You will see something like this:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.5:8501  <-- SHARE THIS ONE
```

## Step 3: Share with Others
1.  Connect your phone or another laptop to the **SAME WiFi network** as your computer.
2.  Open a browser (Chrome/Safari) on the other device.
3.  Type in the **Network URL** exactly as shown (e.g., `http://192.168.1.5:8501`).
4.  The dashboard will load on their device!

---

## ⚠️ Troubleshooting: "It's Not Connecting!"
If your friends see "This site can't be reached", **Windows Firewall is blocking it.**

### **Solution 1: Fix Windows Firewall (Recommended)**
1.  Press the **Start** button and type: `Allow an app through Windows Firewall`.
2.  Click the result to open settings.
3.  Click the **"Change settings"** button at the top right (Administrator).
4.  Scroll down to find **`python`** or **`python.exe`**.
5.  **Check BOTH boxes** (Private & Public) next to it.
6.  Click **OK**.
7.  **Restart** the dashboard (`run_project.bat`).

### **Solution 2: Use "ngrok" (Easiest for Internet Sharing)**
If the firewall fix doesn't work, or you want to share with someone **outside your WiFi**:

1.  Download **ngrok** from [ngrok.com/download](https://ngrok.com/download) (it's free).
2.  Unzip it.
3.  Open a new terminal window (CMD) in that folder.
4.  Run this command:
    ```cmd
    ngrok http 8501
    ```
5.  It will give you a link like `https://a1b2-c3d4.ngrok-free.app`.
6.  **Send that link to anyone.** They can open it on their phone/laptop anywhere in the world!
