import subprocess

# Path to the image you want to display
image_path = "/home/megh/Documents/GitHub/Ollama-Aneki/kitty/saves/default/exp/angry.png"

# Unique ID to refer to the image
image_id = "123"

# Command to display the image with scaling, no newline, and alignment
command = f"kitty icat --image-id {image_id} --align left --scale-up --no-trailing-newline {image_path}"

# Run the command using subprocess to display the image
subprocess.run(command, shell=True)

# Additional code after the image is displayed
print("Image displayed with scaling and no newline, and centered alignment!")
