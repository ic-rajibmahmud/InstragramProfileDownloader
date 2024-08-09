import customtkinter as ctk
import instaloader
import os
from tkinter import messagebox

# Set appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class InstagramDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Instagram Downloader")
        self.geometry("600x600")

        self.loader = instaloader.Instaloader(
            download_comments=True,  # Download comments
            save_metadata=True,  # Save metadata
            post_metadata_txt_pattern='{caption}',  # Save captions
            compress_json=False  # Save JSON metadata without compression
        )
        self.logged_in = False

        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, height=50)
        self.header_frame.pack(fill="x")
        ctk.CTkLabel(self.header_frame, text="Instagram Downloader", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Username and Password
        self.username_label = ctk.CTkLabel(self, text="Instagram Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="Password (Optional):")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        # Profile to download
        self.profile_label = ctk.CTkLabel(self, text="Profile to Download:")
        self.profile_label.pack(pady=5)
        self.profile_entry = ctk.CTkEntry(self)
        self.profile_entry.pack(pady=5)

        # Download Options
        self.download_dp_var = ctk.BooleanVar()
        self.download_dp_check = ctk.CTkCheckBox(self, text="Display Picture", variable=self.download_dp_var)
        self.download_dp_check.pack(pady=5)

        self.download_albums_var = ctk.BooleanVar()
        self.download_albums_check = ctk.CTkCheckBox(self, text="Albums", variable=self.download_albums_var)
        self.download_albums_check.pack(pady=5)

        self.download_stories_var = ctk.BooleanVar()
        self.download_stories_check = ctk.CTkCheckBox(self, text="Stories", variable=self.download_stories_var)
        self.download_stories_check.pack(pady=5)

        self.download_button = ctk.CTkButton(self, text="Download", command=self.download_profile)
        self.download_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.loader.login(username, password)
            self.logged_in = True
            messagebox.showinfo("Login Success", "Logged in successfully!")
        except Exception as e:
            messagebox.showerror("Login Error", f"Failed to log in: {e}")

    def download_profile(self):
        profile_name = self.profile_entry.get()
        try:
            profile = instaloader.Profile.from_username(self.loader.context, profile_name)
            base_dir = os.path.join(os.getcwd(), profile_name)
            os.makedirs(base_dir, exist_ok=True)

            if self.download_dp_var.get():
                dp_dir = os.path.join(base_dir, "Profile_Picture")
                os.makedirs(dp_dir, exist_ok=True)
                self.loader.dirname_pattern = os.path.join(dp_dir, '{profile}')
                self.loader.download_profilepic(profile)

            if self.download_albums_var.get():
                albums_dir = os.path.join(base_dir, "Albums")
                os.makedirs(albums_dir, exist_ok=True)
                self.loader.dirname_pattern = os.path.join(albums_dir, '{profile}')
                self.loader.download_profile(profile, profile_pic=False, fast_update=True, download_videos=True)

            if self.download_stories_var.get():
                stories_dir = os.path.join(base_dir, "Stories")
                os.makedirs(stories_dir, exist_ok=True)
                self.loader.dirname_pattern = os.path.join(stories_dir, '{profile}')
                self.loader.download_stories(userids=[profile.userid])

            messagebox.showinfo("Download Success", "Profile downloaded successfully!")
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            messagebox.showerror("Download Error", "Profile is private and you are not following it.")
        except instaloader.exceptions.LoginRequiredException:
            messagebox.showerror("Download Error", "Login required to download this profile.")
        except instaloader.exceptions.ConnectionException as e:
            messagebox.showerror("Download Error", f"Connection error: {e}")
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to download profile: {e}")

if __name__ == "__main__":
    app = InstagramDownloaderApp()
    app.mainloop()
