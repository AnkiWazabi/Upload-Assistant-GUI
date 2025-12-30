import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys

class UploadAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Upload Assistant GUI - v0.1")
        self.root.geometry("1100x950")

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[12, 5])
        style.configure("TLabelframe.Label", font=("Arial", 9))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_ctrl = ttk.Frame(self.notebook)
        self.tab_meta = ttk.Frame(self.notebook)
        self.tab_upload = ttk.Frame(self.notebook)
        self.tab_torrent = ttk.Frame(self.notebook)
        self.tab_img = ttk.Frame(self.notebook)
        self.tab_auto = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_ctrl, text="1. Contrôle & Maintenance")
        self.notebook.add(self.tab_meta, text="2. Métadonnées")
        self.notebook.add(self.tab_upload, text="3. Configuration Upload")
        self.notebook.add(self.tab_torrent, text="4. Torrent")
        self.notebook.add(self.tab_img, text="5. Traitement Image")
        self.notebook.add(self.tab_auto, text="6. Automatisation & File")

        self.setup_tab_controle()
        self.setup_tab_metadonnees()
        self.setup_tab_upload()
        self.setup_tab_torrent()
        self.setup_tab_image()
        self.setup_tab_automation()

        self.setup_footer()

    def setup_tab_controle(self):
        group_path = ttk.LabelFrame(self.tab_ctrl, text=" Cible ", padding=15)
        group_path.pack(fill="x", padx=15, pady=10)
        
        self.path_var = tk.StringVar()
        f = ttk.Frame(group_path); f.pack(fill="x", pady=5)
        ttk.Entry(f, textvariable=self.path_var).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(f, text="Parcourir...", command=self.browse_path).pack(side="right")

        group_opt = ttk.LabelFrame(self.tab_ctrl, text=" Options Système ", padding=15)
        group_opt.pack(fill="x", padx=15, pady=10)

        self.debug_var = tk.BooleanVar()
        ttk.Checkbutton(group_opt, text="Mode Débogage (--debug)", variable=self.debug_var).pack(anchor="w", pady=5)

        self.cleanup_var = tk.BooleanVar()
        ttk.Checkbutton(group_opt, text="Nettoyage (--cleanup)", variable=self.cleanup_var).pack(anchor="w", pady=5)

    def setup_tab_metadonnees(self):
        group_ids = ttk.LabelFrame(self.tab_meta, text=" Métadonnées ", padding=15)
        group_ids.pack(fill="x", padx=15, pady=10)

        self.meta_vars = {}
        fields = [
            ("imdb", "ID IMDb", "tt1234567"),
            ("tmdb", "ID TMDb", "550"),
            ("tvdb", "ID TVDb", "12123"),
            ("mal", "ID MAL", "1535"),
            ("tvmaze_manual", "ID TVMaze", "1")
        ]

        for i, (arg, label, ex) in enumerate(fields):
            ttk.Label(group_ids, text=f"{label} (--{arg}) :").grid(row=i, column=0, sticky="w", pady=5)
            var = tk.StringVar()
            ttk.Entry(group_ids, textvariable=var, width=25).grid(row=i, column=1, padx=10)
            ttk.Label(group_ids, text=f"Ex: {ex}", font=("Arial", 8), foreground="gray").grid(row=i, column=2, sticky="w")
            self.meta_vars[arg] = var

    def setup_tab_upload(self):
        group_tk = ttk.LabelFrame(self.tab_upload, text=" Sélection des Trackers (--trackers) ", padding=5)
        group_tk.pack(fill="x", padx=15, pady=5)

        canvas = tk.Canvas(group_tk, height=180)
        scrollbar = ttk.Scrollbar(group_tk, orient="vertical", command=canvas.yview)
        scroll_tk = ttk.Frame(canvas)
        scroll_tk.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_tk, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y")

        trackers_data = [
            ("Aither", "AITHER"), ("Alpharatio", "AR"), ("AmigosShareClub", "ASC"), ("AnimeLovers", "AL"),
            ("Anthelion", "ANT"), ("AsianCinema", "ACM"), ("AvistaZ", "AZ"), ("Beyond-HD", "BHD"),
            ("BitHDTV", "BHDTV"), ("Blutopia", "BLU"), ("BrasilJapão-Share", "BJS"), ("BrasilTracker", "BT"),
            ("CapybaraBR", "CBR"), ("Cinematik", "TIK"), ("CinemaZ", "CZ"), ("DarkPeers", "DP"),
            ("DigitalCore", "DC"), ("Emuwarez", "EMUW"), ("FearNoPeer", "FNP"), ("FileList", "FL"),
            ("Friki", "FRIKI"), ("FunFile", "FF"), ("GreatPosterWall", "GPW"), ("hawke-uno", "HUNO"),
            ("HDBits", "HDB"), ("HD-Space", "HDS"), ("HD-Torrents", "HDT"), ("HomieHelpDesk", "HHD"),
            ("ImmortalSeed", "IS"), ("InfinityHD", "IHD"), ("ItaTorrents", "ITT"), ("LastDigitalUnderground", "LDU"),
            ("Lat-Team", "LT"), ("Locadora", "LCD"), ("LST", "LST"), ("MoreThanTV", "MTV"),
            ("Nebulance", "NBL"), ("OldToonsWorld", "OTW"), ("OnlyEncodes+", "OE"), ("PassThePopcorn", "PTP"),
            ("PolishTorrent", "PTT"), ("Portugas", "PT"), ("PTerClub", "PTER"), ("PrivateHD", "PHD"),
            ("PTSKIT", "PTS"), ("Racing4Everyone", "R4E"), ("Rastastugan", "RAS"), ("ReelFLiX", "RF"),
            ("RetroFlix", "RTF"), ("Samaritano", "SAM"), ("seedpool", "SP"), ("ShareIsland", "SHRI"),
            ("SkipTheCommercials", "STC"), ("SpeedApp", "SPD"), ("Swarmazon", "SN"), ("TorrentHR", "THR"),
            ("Torrenteros", "TTR"), ("TorrentLeech", "TL"), ("The Leach Zone", "TLZ"), ("ToTheGlory", "TTG"),
            ("TVChaosUK", "TVC"), ("ULCX", "ULCX"), ("UTOPIA", "UTP"), ("YOINKED", "YOINK"), ("YUSCENE", "YUS")
        ]

        self.tracker_vars = {}
        for i, (name, acro) in enumerate(trackers_data):
            var = tk.BooleanVar()
            ttk.Checkbutton(scroll_tk, text=name, variable=var).grid(row=i//6, column=i%6, sticky="w", padx=5, pady=1)
            self.tracker_vars[acro] = var

        group_rel = ttk.LabelFrame(self.tab_upload, text=" Paramètres de la Release ", padding=10)
        group_rel.pack(fill="x", padx=15, pady=10)

        self.upload_vars = {}
        rel_fields = [("category", "Catégorie"), ("type", "Type"), ("screens", "Screens"), ("imghost", "Hébergeur")]
        for i, (arg, label) in enumerate(rel_fields):
            ttk.Label(group_rel, text=f"{label} (--{arg}) :").grid(row=i, column=0, sticky="w", pady=3)
            var = tk.StringVar()
            ttk.Entry(group_rel, textvariable=var, width=25).grid(row=i, column=1, padx=10)
            self.upload_vars[arg] = var

        group_modes = ttk.LabelFrame(self.tab_upload, text=" Modes Spéciaux ", padding=10)
        group_modes.pack(fill="x", padx=15, pady=5)
        self.anon_var = tk.BooleanVar()
        ttk.Checkbutton(group_modes, text="Anonyme (--anon)", variable=self.anon_var).pack(side="left", padx=20)
        self.unattended_var = tk.BooleanVar()
        ttk.Checkbutton(group_modes, text="Auto (--unattended)", variable=self.unattended_var).pack(side="left", padx=20)

    def setup_tab_torrent(self):
        group_tor = ttk.LabelFrame(self.tab_torrent, text=" Configuration du Torrent ", padding=15)
        group_tor.pack(fill="x", padx=15, pady=10)
        
        self.nohash_var = tk.BooleanVar()
        ttk.Checkbutton(group_tor, text="Désactiver le Hash (--nohash)", variable=self.nohash_var).pack(anchor="w")
        self.rehash_var = tk.BooleanVar()
        ttk.Checkbutton(group_tor, text="Forcer le Rehash (--rehash)", variable=self.rehash_var).pack(anchor="w")
        self.force_recheck_var = tk.BooleanVar()
        ttk.Checkbutton(group_tor, text="Forcer Recheck Client (--force_recheck)", variable=self.force_recheck_var).pack(anchor="w")

        self.client_var = tk.StringVar()
        ttk.Label(group_tor, text="Client (--client) :").pack(anchor="w", pady=(10,0))
        ttk.Entry(group_tor, textvariable=self.client_var, width=25).pack(anchor="w")

        self.tag_var = tk.StringVar()
        ttk.Label(group_tor, text="Tag (--tag) :").pack(anchor="w", pady=(10,0))
        ttk.Entry(group_tor, textvariable=self.tag_var, width=25).pack(anchor="w")

        self.rand_var = tk.StringVar(value="0")
        ttk.Label(group_tor, text="Aléatoire (--randomized) :").pack(anchor="w", pady=(10,0))
        ttk.Entry(group_tor, textvariable=self.rand_var, width=10).pack(anchor="w")

    def setup_tab_image(self):
        group_img = ttk.LabelFrame(self.tab_img, text=" Captures d'écran ", padding=15)
        group_img.pack(fill="x", padx=15, pady=10)
        
        self.frames_var = tk.StringVar()
        ttk.Label(group_img, text="Timestamps manuels (--manual_frames) :").pack(anchor="w")
        ttk.Entry(group_img, textvariable=self.frames_var, width=60).pack(anchor="w", pady=5)

        self.cutoff_var = tk.StringVar(value="3")
        ttk.Label(group_img, text="Seuil (--cutoff) :").pack(anchor="w")
        ttk.Entry(group_img, textvariable=self.cutoff_var, width=10).pack(anchor="w", pady=5)

        self.skipimg_var = tk.BooleanVar()
        ttk.Checkbutton(group_img, text="Sauter l'upload images (--skip_imghost_upload)", variable=self.skipimg_var).pack(anchor="w", pady=5)

    def setup_tab_automation(self):
        group_queue = ttk.LabelFrame(self.tab_auto, text=" Gestion File & Emby ", padding=15)
        group_queue.pack(fill="x", padx=15, pady=10)

        self.limit_queue_var = tk.StringVar(value="0")
        ttk.Label(group_queue, text="Limite file (--limit_queue) :").grid(row=0, column=0, sticky="w")
        ttk.Entry(group_queue, textvariable=self.limit_queue_var, width=10).grid(row=0, column=1, padx=10)

        self.site_check_var = tk.BooleanVar()
        ttk.Checkbutton(group_queue, text="Vérifier existence uniquement (--site_check)", variable=self.site_check_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        
        self.search_req_var = tk.BooleanVar()
        ttk.Checkbutton(group_queue, text="Chercher requêtes (--search_requests)", variable=self.search_req_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        self.emby_var = tk.BooleanVar()
        ttk.Checkbutton(group_queue, text="Intégration Emby (--emby)", variable=self.emby_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
        
        self.emby_debug_var = tk.BooleanVar()
        ttk.Checkbutton(group_queue, text="Debug Emby (--emby_debug)", variable=self.emby_debug_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

    def setup_footer(self):
        footer = ttk.Frame(self.root, padding=10)
        footer.pack(side="bottom", fill="x")
        btn_run = ttk.Button(footer, text="🚀 LANCER L'UPLOAD", command=self.executer_commande)
        btn_run.pack(pady=10, ipady=5, ipadx=20)

    def executer_commande(self):
        path = self.path_var.get()
        if not path:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier ou un dossier cible.")
            return

        #upload.py
        cmd = ["python", "upload.py", f'"{path}"']

        if self.debug_var.get(): cmd.append("--debug")
        if self.cleanup_var.get(): cmd.append("--cleanup")
        for arg, var in self.meta_vars.items():
            if var.get().strip(): cmd.extend([f"--{arg}", var.get().strip()])
        selected_trackers = [acro for acro, v in self.tracker_vars.items() if v.get()]
        if selected_trackers: cmd.extend(["--trackers", ",".join(selected_trackers)])
        for arg, var in self.upload_vars.items():
            if var.get().strip(): cmd.extend([f"--{arg}", var.get().strip()])
        if self.anon_var.get(): cmd.append("--anon")
        if self.unattended_var.get(): cmd.append("--unattended")
        if self.nohash_var.get(): cmd.append("--nohash")
        if self.rehash_var.get(): cmd.append("--rehash")
        if self.force_recheck_var.get(): cmd.append("--force_recheck")
        if self.client_var.get().strip(): cmd.extend(["--client", self.client_var.get().strip()])
        if self.tag_var.get().strip(): cmd.extend(["--tag", self.tag_var.get().strip()])
        if self.rand_var.get() != "0": cmd.extend(["--randomized", self.rand_var.get()])
        if self.frames_var.get().strip(): cmd.extend(["--manual_frames", self.frames_var.get().strip()])
        if self.cutoff_var.get() != "3": cmd.extend(["--cutoff", self.cutoff_var.get()])
        if self.skipimg_var.get(): cmd.append("--skip_imghost_upload")
        if self.limit_queue_var.get() != "0": cmd.extend(["--limit_queue", self.limit_queue_var.get()])
        if self.site_check_var.get(): cmd.append("--site_check")
        if self.search_req_var.get(): cmd.append("--search_requests")
        if self.emby_var.get(): cmd.append("--emby")
        if self.emby_debug_var.get(): cmd.append("--emby_debug")

        final_cmd = " ".join(cmd)
        print(f"Lancement de la commande : {final_cmd}")
        
        try:
            subprocess.Popen(final_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror("Erreur d'exécution", f"Impossible de lancer le script : {e}")

    def browse_path(self):
        target = filedialog.askdirectory() or filedialog.askopenfilename()
        if target: self.path_var.set(target)

if __name__ == "__main__":
    root = tk.Tk()
    app = UploadAssistantGUI(root)
    root.mainloop()