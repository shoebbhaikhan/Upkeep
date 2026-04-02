# Upkeep: The Lightweight WinGet Update Manager

**Upkeep** is an open-source, minimalist system tray application designed to bridge the gap between the power of the Windows Package Manager (**WinGet**) and the convenience of a graphical user interface. It monitors your installed software in the background and provides a "one-click" solution to keep your environment secure and up to date.

---

## What Upkeep Does
At its core, **Upkeep** acts as an automated "butler" for your Windows applications. 

* **Silent Monitoring:** It periodically runs a background check against the WinGet repository to identify which of your installed programs have newer versions available.
* **Visual Status:** The system tray icon changes dynamically—turning from grayscale to color—to signal when updates are pending, allowing you to stay informed without intrusive pop-up windows.
* **Granular Control:** It parses complex command-line data into a simple, readable list, allowing you to see exactly which versions are currently installed and what the new versions are.

---

## How to Use the Tray Menu
Once launched, **Upkeep** lives in your Windows Taskbar tray (near the clock). Right-clicking the icon reveals a professional, tiered menu:

* **Outdated Package Count:** The top of the menu shows a real-time count of how many apps need updates and the exact timestamp of the last check.
* **Install Updates (X)...**: A primary action button that launches a visible terminal window to update **all** pending software simultaneously.
* **Outdated Packages Sub-menu:** Hovering here reveals a list of specific apps (e.g., *Notion*, *VS Code*, *Zoom*). Clicking an individual app will trigger an update for **only** that selection.
* **Check Frequency:** Allows you to customize how often the app scans for updates (ranging from every 30 minutes to once a day).
* **Start with Windows:** A simple toggle to ensure **Upkeep** protects your system from the moment you boot up.
* **Check Now:** Forces an immediate manual scan of your software library.

---

## Why I Built Upkeep
As an industrial designer and educator, I value tools that are functional, unobtrusive, and efficient. While **WinGet** is an incredibly powerful tool for developers, it lacks a native, lightweight "notification" system for everyday users who don't want to live in the command prompt. 

I built **Upkeep** to provide:
1.  **Focus:** To remove the "annoyance" of multiple independent software updaters popping up throughout the day.
2.  **Transparency:** By using a visible terminal window during updates, users can see the actual progress bars and verify the integrity of the installation.
3.  **Efficiency:** To automate the maintenance of a professional workstation with zero overhead.

---

## Disclaimer & Attribution
This project, from the initial logic architecture to the final Python implementation and documentation, was developed in collaboration with **Google Gemini**. It serves as a testament to how AI-assisted development can empower individuals to build high-quality, functional, and open-source utility software tailored to specific professional needs.
