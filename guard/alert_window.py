"""Beacon Guard -- Persistent Alert Window.

Creates an always-on-top, unmissable alert window that stays visible
until the user explicitly clicks Dismiss. Uses tkinter (built into Python,
no extra dependencies).
"""

import threading
import tkinter as tk
from pathlib import Path


def show_alert(title: str, message: str, severity: str = "high"):
    """Show a persistent, always-on-top alert window.

    This window:
    - Stays on screen until dismissed
    - Is always on top of other windows
    - Has a colored border based on severity
    - Shows the Beacon branding
    - Can't be accidentally closed (no X button, must click Dismiss)
    """
    def _create_window():
        root = tk.Tk()
        root.title("Beacon Guard Alert")
        root.attributes("-topmost", True)
        root.overrideredirect(True)  # Remove title bar

        # Colors based on severity
        colors = {
            "critical": {"bg": "#1a0505", "border": "#ef4444", "accent": "#ef4444", "text": "#fecaca"},
            "high": {"bg": "#1a0505", "border": "#ef4444", "accent": "#ef4444", "text": "#fecaca"},
            "medium": {"bg": "#1a1000", "border": "#f59e0b", "accent": "#f59e0b", "text": "#fed7aa"},
            "low": {"bg": "#0a1628", "border": "#3b82f6", "accent": "#3b82f6", "text": "#bfdbfe"},
        }
        c = colors.get(severity.lower(), colors["high"])

        # Window size and position (top-right corner)
        w, h = 420, 220
        screen_w = root.winfo_screenwidth()
        x = screen_w - w - 20
        y = 20
        root.geometry(f"{w}x{h}+{x}+{y}")

        # Main frame with colored border
        outer = tk.Frame(root, bg=c["border"], padx=3, pady=3)
        outer.pack(fill="both", expand=True)

        inner = tk.Frame(outer, bg=c["bg"])
        inner.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(inner, bg=c["border"], height=36)
        header.pack(fill="x")
        header.pack_propagate(False)

        icon_label = tk.Label(
            header, text="  BEACON GUARD", font=("Segoe UI", 10, "bold"),
            bg=c["border"], fg="white", anchor="w"
        )
        icon_label.pack(side="left", padx=8)

        severity_label = tk.Label(
            header, text=f"  {severity.upper()}  ", font=("Segoe UI", 8, "bold"),
            bg="white", fg=c["border"]
        )
        severity_label.pack(side="right", padx=8, pady=6)

        # Body
        body = tk.Frame(inner, bg=c["bg"], padx=16, pady=12)
        body.pack(fill="both", expand=True)

        title_label = tk.Label(
            body, text=title, font=("Segoe UI", 11, "bold"),
            bg=c["bg"], fg="white", anchor="w", wraplength=380, justify="left"
        )
        title_label.pack(anchor="w")

        msg_label = tk.Label(
            body, text=message, font=("Segoe UI", 9),
            bg=c["bg"], fg=c["text"], anchor="w", wraplength=380, justify="left"
        )
        msg_label.pack(anchor="w", pady=(6, 0))

        # Footer with Dismiss button
        footer = tk.Frame(inner, bg=c["bg"], padx=16, pady=8)
        footer.pack(fill="x")

        dismiss_btn = tk.Button(
            footer, text="Dismiss", font=("Segoe UI", 9, "bold"),
            bg=c["accent"], fg="white", activebackground="#ffffff",
            activeforeground=c["accent"], relief="flat", padx=20, pady=4,
            cursor="hand2", command=root.destroy
        )
        dismiss_btn.pack(side="right")

        safe_label = tk.Label(
            footer, text="Do not interact with the suspicious content.",
            font=("Segoe UI", 8), bg=c["bg"], fg="#666666"
        )
        safe_label.pack(side="left")

        # Play alert sound
        try:
            import winsound
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception:
            pass

        root.mainloop()

    # Run in a separate thread so it doesn't block the guard loop
    t = threading.Thread(target=_create_window, daemon=True)
    t.start()


# Test
if __name__ == "__main__":
    show_alert(
        title="Phishing Attempt Detected",
        message="A fake payment update page was detected on your screen. The email claims your 'Cloud subscription' payment has expired and asks you to click 'Update Payment Details'. This is a common phishing tactic. Do not click any links.",
        severity="critical"
    )
    import time
    time.sleep(60)
