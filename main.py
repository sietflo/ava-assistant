
import tkinter as tk
from tkinter import ttk
import json
import winsound
from tkinter import filedialog
import subprocess
from OpenAI_settings import char_model
from OpenAI_settings import client
import pyttsx3
import webbrowser
import pyjokes
import os
import random
import speech_recognition as sr
from translate import Translator
import wikipedia
import sys
import datetime
import threading
from PIL import Image, ImageTk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

translator = Translator(to_lang='uk')
interaction = 0
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[4].id)

def loading_page():
    def close_loading():
        root_loading.destroy()
    def update_progress():
        progress_value = 0
        while progress_value <= 99:
            try:
                progress['value'] = progress_value
                progress_value += 3
                root_loading.update_idletasks()
                root_loading.after(50)
            except:
                break
            
    root_loading = tk.Tk()
    root_loading.title("Loading Page")
    screen_width = root_loading.winfo_screenwidth()
    screen_height = root_loading.winfo_screenheight()
    x = (screen_width - 337) // 2
    y = (screen_height - 151) // 2
    root_loading.geometry(f"337x151+{x}+{y}")
    root_loading.resizable(False, False)
    root_loading.overrideredirect(True)
    image = Image.open(resource_path("loading.png"))  
    image = image.resize((337, 151))
    background_image = ImageTk.PhotoImage(image) 
    canvas = tk.Canvas(root_loading, width=337, height=151)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Horizontal.TProgressbar", troughcolor="#D9D9D9", background="#3B8BF2", bordercolor="#3B8BF2")
    progress = ttk.Progressbar(root_loading, orient="horizontal", length=300, mode="determinate", style="Custom.Horizontal.TProgressbar")
    progress.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    
    update_thread = threading.Thread(target=update_progress)
    update_thread.start()
    root_loading.after(2500, close_loading)
    root_loading.mainloop()
    
class VoiceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ava")
        self.master.iconbitmap(resource_path('icona.ico'))
        self.applications = []
        self.api_key = ""
        self.path = ""
        self.create_widgets()
        self.load_applications()
        self.save_applications()
        self.add_api()
        self.current_command = None
        
    def create_widgets(self):
        style = ttk.Style(root)
        style.configure('lefttab.TNotebook', tabposition='wn', tabwidth=120)

        notebook = ttk.Notebook(self.master, style='lefttab.TNotebook')
        notebook.pack(fill="both", expand=True)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)

        notebook.add(tab1, text="           Ava           ")
        notebook.add(tab2, text="Ваші програми")
        notebook.add(tab3, text="Налаштування ")
        # Вкладка "Ava"
        self.black_image = ImageTk.PhotoImage(Image.open(resource_path("black.png")))
        self.blue_image = ImageTk.PhotoImage(Image.open(resource_path("blue.png")))

        self.image_label = tk.Label(tab1, image=self.black_image)
        self.image_label.pack(side="top", pady=0)

        listen_button = tk.Button(tab1, text="Слухати", command=self.start_listening)
        listen_button.pack()

        # Вкладка "Ваші програми"
        command_label = tk.Label(tab2, text="Команда для вашої програми:")
        command_label.grid(row=0, column=0, pady=10)

        self.command_entry = tk.Entry(tab2, width=30)
        self.command_entry.grid(row=0, column=1, padx=20)

        add_button = tk.Button(tab2, text="Додати програму", command=self.add_application)
        add_button.grid(row=0, column=2, padx=10, pady=10)
        
        prog_label = tk.Label(tab2, text="Ваші програми:")
        prog_label.grid(row=1, column=0, pady=10)

        edit_button = tk.Button(tab2, text="Змінити назву", command=self.edit_application)
        edit_button.grid(row=2, column=2, sticky="nsew", padx=10, pady=5)

        delete_button = tk.Button(tab2, text="Видалити програму", command=self.delete_app)
        delete_button.grid(row=3, column=2, sticky="nsew", padx=10, pady=5)

        self.app_listbox = tk.Listbox(tab2, selectmode=tk.SINGLE, height=5, width=30)
        self.app_listbox.grid(row=2, column=0, columnspan=2, rowspan=2, padx=5, pady=5, sticky="nsew")
        # Вкладка "Налаштування"
        api_label = tk.Label(tab3, text="Ваш OpenAI API ключ:")
        api_label.grid(row=0, column=0, pady=10)

        self.api_entry = tk.Entry(tab3, width=30)
        self.api_entry.grid(row=0, column=1, padx=20)

        api_button = tk.Button(tab3, text="Зберегти API", command=self.add_api)
        api_button.grid(row=0, column=2, padx=10, pady=10)
        
        folder_label = tk.Label(tab3, text="""Шлях збереження ваших записів:""")
        folder_label.grid(row=1, column=0, padx=5, pady=5)

        self.folder_entry = tk.Entry(tab3, width=30)
        self.folder_entry.grid(row=1, column=1, padx=5, pady=5)

        browse_button = tk.Button(tab3, text="Обрати папку", command=self.choose_folder)
        browse_button.grid(row=1, column=2, padx=5, pady=5)
        
    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path = folder_path
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)
            self.save_applications()      
    def add_application(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            command = self.command_entry.get()
            if self.check_duplicate_command(command):
                tk.messagebox.showwarning("Помилка", "Така команда вже існує. Будь ласка вкажіть іншу назву!")
            else:
                self.applications.append({"command": command, "path": file_path})
                self.command_entry.delete(0, tk.END)
                self.app_listbox.insert(tk.END, command)
                self.save_applications()
    def check_duplicate_command(self, command):
        for app in self.applications:
            if app["command"] == command.lower():
                return True
        return False        
 
    def launch_application(self):
        if self.current_command:
            for app in self.applications:
                if app["command"] == self.current_command:
                    speak_text("Відкриваю")
                    subprocess.run(app["path"], shell=True)
                    break
    def edit_application(self):
        selected_index = self.app_listbox.curselection()
        if selected_index:
            selected_command = self.app_listbox.get(selected_index)
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Змінити назву команди")
            new_command_entry = tk.Entry(edit_window, width=30)
            new_command_entry.grid(row=0, column=0, padx=10, pady=10)
            new_command_entry.insert(tk.END, selected_command)
            save_button = tk.Button(edit_window, text="Зберегти", command=lambda: self.save_edited_command(edit_window, selected_command, new_command_entry.get()))
            save_button.grid(row=1, column=0, padx=10, pady=5)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            window_width = edit_window.winfo_reqwidth()
            window_height = edit_window.winfo_reqheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
        edit_window.geometry(f"+{x}+{y}")
    
    def save_edited_command(self, edit_window, old_command, new_command):
        for app in self.applications:
            if app["command"] == old_command:
                app["command"] = new_command
                break
        self.save_applications()
        self.refresh_app_listbox()
        edit_window.destroy()

    def refresh_app_listbox(self):
        self.app_listbox.delete(0, tk.END)
        for app in self.applications:
            self.app_listbox.insert(tk.END, app["command"])
        
    def delete_app(self):
        selected_index = self.app_listbox.curselection()
        if selected_index:
            command = self.app_listbox.get(selected_index)
            for app in self.applications:
                if app["command"] == command:
                    self.applications.remove(app)
                    break
            self.save_applications()
            self.app_listbox.delete(0, tk.END)
            for app in self.applications:
                self.app_listbox.insert(tk.END, app["command"])
    def add_api(self):
        new_api_key = self.api_entry.get()
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={new_api_key}\n")
        self.api_key = new_api_key
        self.save_applications()
        
    def save_applications(self):
        data = {"applications": self.applications, "api": self.api_key, "path" : self.path}
        with open('applications.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
            
    def load_applications(self):
        try:
            with open('applications.json', 'r') as json_file:
                data = json.load(json_file)
                self.applications = data.get("applications", [])
                self.api_key = data.get("api", "")
                self.path = data.get("path", "")
                self.api_entry.insert(0, self.api_key)
                self.folder_entry.insert(0, self.path)
                for app in self.applications:
                    self.app_listbox.insert(tk.END, app["command"])
        except FileNotFoundError:
            self.applications = []
            self.api_key = ""
            self.path = ""
    def record_user_input(self, file_path):
        print(f"Recording to file: {file_path}. Speak anything. Say 'stop' to exit.")
        with open(file_path, "w") as file:
            while True:
                command = listen_command()
                if command.lower() == "stop"\
                    or command.lower() == 'стоп':
                    break
                else:
                    file.write(command + "\n")
                    speak_text("Так")
                    
    def toggle_image(self, reset=False):
        if reset:
            self.image_label.configure(image=self.black_image)
            return

        if self.image_label.cget("image") == str(self.black_image):
            self.image_label.configure(image=self.blue_image)
        else:
            self.image_label.configure(image=self.black_image)

    def start_listening(self):
        command = listen_command()
        self.current_command = command
        if "розкажи жарт" in command\
            or 'скажи жарт' in command:
            translator = Translator(to_lang='uk')
            joke = pyjokes.get_joke()
            joke_result = translator.translate(joke)
            speak_text(joke_result)
            print(joke_result)
            return True
        if 'відео' in command:
            speak_text("пошук відео")
            video_name = command.replace('відео', '').strip()
            url = f"https://www.youtube.com/results?search_query={video_name}"
            webbrowser.open(url)
            return True
        if 'пошук' in command:
            speak_text("шукаю")
            search_name = command.replace('пошук', '').strip()
            url = f"https://www.google.com/search?q={search_name}"
            webbrowser.open(url)
            return True
        if 'вікіпедія' in command:
            search_term = command.replace('вікіпедія', '').strip()
            wiki_result = search_wikipedia(search_term)
            speak_text(wiki_result)
            return True
        if 'кинь монетку' in command\
            or 'підкинь монетку' in command\
            or 'монетка' in command:
            winsound.PlaySound("coin.wav", winsound.SND_FILENAME)
            result = random.choice(['орел', 'решка'])
            speak_text(result)
            print(result)
            return True
        if 'запис' in command:
            speak_text("Починаю запис.")
            filename = f"запис_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
            file_path = os.path.join(self.path, filename)
            self.record_user_input(file_path)
            speak_text("Запис завершено.")
            return True
        if 'список команд' in command\
        or 'команди' in command:
            command_list_path = 'commands.txt'
            webbrowser.open(command_list_path)
            return True
        else:
            self.launch_application()
            return True
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
def activate_assistant():
    continued_chat_phrases = ['так', 'слухаю вас', 'слухаю', 'чим можу допомогти?', 'так, бос', 'запитуйте']
    random_chat = ""
    random_chat = random.choice(continued_chat_phrases)
    return random_chat
def trascribe(filename):
    recogniser = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recogniser.record(source)
        print("transcribed")
        try:
            return recogniser.recognize_google(audio, language="uk-UA")
        except:
            print("")
def search_wikipedia(query):
    wikipedia.set_lang('uk')
    page = wikipedia.page(query)
    if page:
        print(page.summary)
        return page.summary
    else:
        return "Вибачте, я не змогла знайти інформацію на цю тему."
def record_prompt():
    filename = 'input.wav'
    try:
        print("recording")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            source.pause_threshold = 0.7
            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, 'wb') as f:
                f.write(audio.get_wav_data())
            text = trascribe(filename)
            print(text)
            return text
    except Exception as e:
        print("Error recording prompt:", e) 
        return None

def listen_command():
    comm = ""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        source.pause_threshold = 0.7
        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
    try:
        print("Recognizing...")
        comm = recognizer.recognize_google(audio, language = "uk-UA").lower()
        print(f"Command: {comm}")

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        print(f"Command: {comm}")
    except sr.RequestError as e:
        print(f"Error: {e}")
    return comm
  
def continuous_listen(app_launcher):
    while True:    
        print("Say 'ava' to start")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                print(transcription)
                if 'ava' in transcription.lower()\
                   or 'eva' in transcription.lower()\
                or 'ейва' in transcription.lower()\
                or 'eve' in transcription.lower()\
                or 'айва' in transcription.lower()\
                or 'ева' in transcription.lower()\
                or 'єва' in transcription.lower()\
                or 'aiwa' in transcription.lower()\
                or 'hey you are' in transcription.lower():
                    readyToWork = activate_assistant()
                    speak_text(readyToWork)
                    app_launcher.toggle_image()
                    print("Trigger phrase 'ava' detected.")
                    continue_listening = app_launcher.start_listening()
                    if not continue_listening:
                        break
                    app_launcher.toggle_image()
                elif 'gpt' in transcription.lower():
                    speak_text("Слухаю ваш запит.")
                    app_launcher.toggle_image()
                    user_prompt = record_prompt()
                    if user_prompt:
                        response = char_model(user_prompt)
                        if response:    
                            speak_text(response)
                            app_launcher.toggle_image()
            except Exception as e:
                continue

if __name__ == "__main__":
    loading_page()
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 700) // 2
    y = (screen_height - 300) // 2
    
    # Set the window position
    root.geometry(f"700x300+{x}+{y}")
    app_launcher = VoiceApp(root)

    listen_thread = threading.Thread(target=continuous_listen, args=(app_launcher,))
    listen_thread.daemon = True
    listen_thread.start()

    root.mainloop()