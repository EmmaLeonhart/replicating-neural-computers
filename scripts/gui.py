"""Windowed launcher for the one runnable demo in "Neural Computers".

A Tkinter front-end over scripts/run.py — the Wan2.1 VAE terminal-reconstruction
test (Experiment 1, Table tab:cli-vae-recon). This is the ONLY part of the paper
that runs on public artifacts: the authors never released the trained CLIGen /
GUIWorld (NCCLIGen / NCGUIWorld) checkpoints. See FINDINGS.md.

On first run, the public Wan2.1 VAE (~hundreds of MB) is downloaded from
HuggingFace automatically by diffusers, then cached. Nothing else to fetch.

Launch it with the repo-root `Run Neural Computers Demo.bat`, or:
    python scripts/gui.py
"""
from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_PY = os.path.join(ROOT, "scripts", "run.py")
RESULTS_DIR = os.path.join(ROOT, "results")

CAVEAT = (
    "Runnable demo: the off-the-shelf Wan2.1 VAE reconstructing terminal frames "
    "(paper Experiment 1). The paper's trained Neural Computers (CLIGen / "
    "GUIWorld) were never released, so they cannot be run — this is the one "
    "result built only from public weights. First run downloads the VAE from "
    "HuggingFace (~hundreds of MB), then caches it."
)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.proc: subprocess.Popen | None = None
        self.q: queue.Queue[str] = queue.Queue()

        root.title("Neural Computers — Wan2.1 VAE Terminal Reconstruction (Exp. 1)")
        root.geometry("860x640")
        root.minsize(720, 520)

        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Neural Computers (arXiv:2604.06425) — Experiment 1 demo",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        ttk.Label(main, text=CAVEAT, wraplength=820, foreground="#555").pack(
            anchor="w", pady=(2, 10)
        )

        # --- Controls ---------------------------------------------------
        ctl = ttk.LabelFrame(main, text="Settings", padding=8)
        ctl.pack(fill="x")

        self.device = tk.StringVar(value="auto")
        self.num_samples = tk.IntVar(value=8)
        self.frames = tk.IntVar(value=5)
        self.font_sizes = tk.StringVar(value="13,6")
        self.densities = tk.StringVar(value="1.0,0.5,0.25")

        row = ttk.Frame(ctl)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text="Device:").pack(side="left")
        ttk.Combobox(
            row, textvariable=self.device, values=["auto", "cuda", "cpu"],
            width=7, state="readonly",
        ).pack(side="left", padx=(4, 16))
        ttk.Label(row, text="Clips / setting:").pack(side="left")
        ttk.Spinbox(row, from_=1, to=64, textvariable=self.num_samples, width=5).pack(
            side="left", padx=(4, 16)
        )
        ttk.Label(row, text="Frames / clip:").pack(side="left")
        ttk.Spinbox(row, from_=1, to=16, textvariable=self.frames, width=5).pack(
            side="left", padx=(4, 16)
        )

        row2 = ttk.Frame(ctl)
        row2.pack(fill="x", pady=2)
        ttk.Label(row2, text="Font sizes (px):").pack(side="left")
        ttk.Entry(row2, textvariable=self.font_sizes, width=12).pack(
            side="left", padx=(4, 16)
        )
        ttk.Label(row2, text="Densities:").pack(side="left")
        ttk.Entry(row2, textvariable=self.densities, width=18).pack(
            side="left", padx=(4, 16)
        )

        hint = ttk.Frame(ctl)
        hint.pack(fill="x", pady=(4, 0))
        ttk.Label(
            hint,
            text="Tip: no GPU? Set Device=cpu, Clips=2, Frames=1, Densities=0.25 "
                 "for a quick smoke test.",
            foreground="#777", font=("Segoe UI", 8),
        ).pack(anchor="w")

        # --- Action buttons --------------------------------------------
        btns = ttk.Frame(main)
        btns.pack(fill="x", pady=8)
        self.run_btn = ttk.Button(btns, text="▶  Run demo", command=self.start)
        self.run_btn.pack(side="left")
        self.stop_btn = ttk.Button(
            btns, text="■  Stop", command=self.stop, state="disabled"
        )
        self.stop_btn.pack(side="left", padx=6)
        ttk.Button(btns, text="Open results folder", command=self.open_results).pack(
            side="left", padx=6
        )
        ttk.Button(
            btns, text="View 13px compare", command=lambda: self.open_img(13)
        ).pack(side="left", padx=6)
        ttk.Button(
            btns, text="View 6px compare", command=lambda: self.open_img(6)
        ).pack(side="left", padx=6)

        # --- Log --------------------------------------------------------
        self.log = ScrolledText(
            main, height=18, wrap="word", font=("Consolas", 9),
            background="#101216", foreground="#d6d6d6",
        )
        self.log.pack(fill="both", expand=True, pady=(4, 0))
        self.log.configure(state="disabled")

        self.status = tk.StringVar(value="Idle.")
        ttk.Label(main, textvariable=self.status, relief="sunken", anchor="w").pack(
            fill="x", pady=(6, 0)
        )

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(100, self.drain_queue)

    # -- subprocess plumbing --------------------------------------------
    def start(self):
        if self.proc is not None:
            return
        cmd = [
            sys.executable, "-u", RUN_PY,
            "--device", self.device.get(),
            "--num-samples", str(self.num_samples.get()),
            "--frames", str(self.frames.get()),
            "--font-sizes", self.font_sizes.get().strip(),
            "--densities", self.densities.get().strip(),
        ]
        self._append(f"$ {' '.join(cmd)}\n\n")
        self.status.set("Running… (first run downloads the VAE from HuggingFace)")
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        try:
            self.proc = subprocess.Popen(
                cmd, cwd=ROOT, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception as exc:  # interpreter/path problems surface here
            self._append(f"[gui] failed to launch: {exc}\n")
            self._reset_buttons()
            self.status.set("Launch failed.")
            return
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        assert self.proc and self.proc.stdout
        for line in self.proc.stdout:
            self.q.put(line)
        code = self.proc.wait()
        self.q.put(f"\n[gui] process exited with code {code}\n")
        self.q.put(f"__DONE__{code}")

    def drain_queue(self):
        try:
            while True:
                item = self.q.get_nowait()
                if item.startswith("__DONE__"):
                    code = item.replace("__DONE__", "")
                    self.proc = None
                    self._reset_buttons()
                    self.status.set(
                        f"Done (exit {code}). Results in results/vae_recon.json."
                        if code == "0" else f"Stopped/failed (exit {code})."
                    )
                else:
                    self._append(item)
        except queue.Empty:
            pass
        self.root.after(100, self.drain_queue)

    def stop(self):
        if self.proc is not None:
            self._append("\n[gui] stopping…\n")
            self.proc.terminate()

    # -- helpers ---------------------------------------------------------
    def _append(self, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _reset_buttons(self):
        self.run_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def open_results(self):
        os.makedirs(RESULTS_DIR, exist_ok=True)
        self._open_path(RESULTS_DIR)

    def open_img(self, font_px: int):
        path = os.path.join(RESULTS_DIR, f"compare_{font_px}px.png")
        if not os.path.exists(path):
            messagebox.showinfo(
                "Not found yet",
                f"compare_{font_px}px.png hasn't been generated.\n"
                "Run the demo first (it's written when {font_px}px is in Font "
                "sizes).".replace("{font_px}", str(font_px)),
            )
            return
        self._open_path(path)

    def _open_path(self, path: str):
        try:
            os.startfile(path)  # Windows
        except AttributeError:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.Popen([opener, path])

    def on_close(self):
        if self.proc is not None:
            if not messagebox.askokcancel("Quit", "A run is in progress. Stop it and quit?"):
                return
            self.proc.terminate()
        self.root.destroy()


def main():
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")  # nicer on Windows; harmless if absent
    except tk.TclError:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
