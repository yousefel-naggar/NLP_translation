from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import customtkinter as ctk
from tkinter import messagebox


def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    print(f"Model and tokenizer loaded from: {model_path}")
    return tokenizer, model

def translate_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    outputs = model.generate(**inputs, max_length=128)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


tokenizer, model = load_model("models")


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("🌍 Arabic to English Translator")
app.geometry("600x500")
app.resizable(False, False)


title = ctk.CTkLabel(app, text="🌍 Arabic to English Translator", font=("Arial", 24, "bold"))
title.pack(pady=(20, 10))


input_label = ctk.CTkLabel(app, text="Arabic Text", font=("Arial", 16))
input_label.pack(anchor="w", padx=40, pady=(10, 5))

input_box = ctk.CTkTextbox(app, height=100, width=500, corner_radius=10, font=("Arial", 14))
input_box.pack(pady=5)


def on_translate():
    arabic_text = input_box.get("0.0", "end").strip()
    if not arabic_text:
        messagebox.showwarning("Input Error", "Please enter Arabic text.")
        return
    try:
        translation = translate_text(arabic_text, tokenizer, model)
        output_box.configure(state="normal")
        output_box.delete("0.0", "end")
        output_box.insert("end", translation)
        output_box.configure(state="disabled")
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))


translate_button = ctk.CTkButton(app, text="Translate", command=on_translate, font=("Arial", 14))
translate_button.pack(pady=15)


output_label = ctk.CTkLabel(app, text="English Translation", font=("Arial", 16))
output_label.pack(anchor="w", padx=40, pady=(10, 5))

output_box = ctk.CTkTextbox(app, height=100, width=500, corner_radius=10, font=("Arial", 14))
output_box.configure(state="disabled")
output_box.pack(pady=5)

app.mainloop()
