import pyperclip
import customtkinter
import tkinter as tk
import main
import utilities
import time
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")
root.iconbitmap("./Images/Safe Journey Badge Big.ico")

def check_state(origin,
                destination):  # vaildates origin and destination addresses are in Colorado start program or trigger alert
    origin_state = utilities.get_state_from_address(origin)
    destination_state = utilities.get_state_from_address(destination)
    if (origin_state == "CO" or origin_state == "Colorado") and (
            destination_state == "CO" or destination_state == "Colorado"):
        return True
    if origin_state == "CO" or origin_state == "Colorado":
        return "destination"
    else:
        return "origin"


def execute_calculation():  # starts calculation if entries are valid
    origin = input_origin_var.get()
    destination = input_destination_var.get()
    valid_input = check_state(origin, destination)  # checks if entries are valid - in Colorado
    if valid_input == True:
        label_calculating.configure(text="Calculating...", text_color="green")
        label_calculating.grid(row=7, column=0, pady=12, padx=10, columnspan=2)
        label_calculating.update()
        center_lat = 39.75930514626203  # Center map: Denver CO
        center_lon = -104.98707405613654  # Center map: Denver CO
        num_points = 300  # number of route points
        num_accidents = 10000  # total number of accidents in Colorado
        # num_accidents = 90885  # total number of accidents in Colorado
        state = "CO"  # state of calculation

        score, link, route_number = main.draw_map(center_lat, center_lon, origin, destination, num_points,
                                                  num_accidents, state)
        label_score.configure(text=f"Total score is {score}", text_color="White")
        label_score.grid(row=5, column=0, pady=12, padx=10, columnspan=2)
        label_score.update()
        button_copy_clipboard.configure(text=f"Copy Safest Journey Directions Link \n Take Route # {route_number + 1}",
                                        text_color="black",
                                        command=lambda: copy_clip(link))

        button_copy_clipboard.grid(row=7, column=0, pady=12, padx=10, columnspan=2)
        button_copy_clipboard.update()

    else:
        label_calculating.configure(text=f"Invalid {valid_input} address, limited to Colorado only", text_color="red")
        label_calculating.grid(row=7, column=0, pady=12, padx=10, columnspan=2)


def exit_click():  # exit button
    label_calculating.configure(text="Safe Journey !", text_color="green")
    label_calculating.grid(row=7, column=0, pady=12, padx=10, columnspan=2)
    time.sleep(2)
    root.destroy()


def copy_clip(link):  # copies google maps link to clipboard
    pyperclip.copy(link)
    button_copy_clipboard.configure(text="Copied")
    time.sleep(2)
    reset_copy_button()


def reset_copy_button():  # reset text of copy to clipboard button
    button_copy_clipboard.configure(text="Copy Safest Route Directions Link")
    button_copy_clipboard.update()


frame = customtkinter.CTkFrame(master=root)
frame.grid(pady=20, padx=60, sticky="nsew")
frame.grid_rowconfigure(1, minsize=40)

# Input variables
input_origin_var = tk.StringVar()
input_destination_var = tk.StringVar()

label_font = ("Helvetica", 20)
label_safety_score = customtkinter.CTkLabel(master=frame, text="Safe Journey:", text_color="White", font=label_font)
label_safety_score.grid(row=0, column=0, pady=12, padx=10, columnspan=2)

image_path = "./Images/Safe Journey Badge Small.jpg"
image = Image.open(image_path)
image = ImageTk.PhotoImage(image)

# Create a Label to display the image
image_label = tk.Label(frame, image=image)
image_label.image = image  # To prevent image from being garbage collected
image_label.grid(row=1, column=0, pady=12, padx=10, columnspan=2)




# Define entry variables within the function scope
origin_name = customtkinter.CTkEntry(master=frame, placeholder_text="Origin Place", textvariable=input_origin_var,
                                     text_color="white")
destination_name = customtkinter.CTkEntry(master=frame, placeholder_text="Destination Place",
                                          textvariable=input_destination_var, text_color="white")

# placements of entries
origin_name.grid(row=2, column=0, padx=5, pady=10)
destination_name.grid(row=2, column=1, padx=5, pady=10)

label_calculating = customtkinter.CTkLabel(master=frame)
label_score = customtkinter.CTkLabel(master=frame)
label_link = customtkinter.CTkLabel(master=frame)

button_execute = customtkinter.CTkButton(master=frame, text="Calculate", text_color="black",
                                         command=execute_calculation)
button_execute.grid(row=6, column=0, columnspan=2, pady=12, padx=10)

button_copy_clipboard = customtkinter.CTkButton(master=frame)

button_exit = customtkinter.CTkButton(master=frame, text="Exit", text_color="black", command=exit_click)
button_exit.grid(row=8, column=0, columnspan=2, pady=12, padx=10)

root.mainloop()
