import os
import shutil

# Define folder paths
source_folder = r"C:\path\to\source\folder"  # Folder with all delivery notes
destination_folder = r"C:\path\to\destination\folder"  # Folder to copy matched files
dn_list_file = r"C:\path\to\dn_list.txt"  # File containing DN numbers
error_log_file = r"C:\path\to\error_log.txt"  # File to log missing DNs

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Read DN numbers from file
with open(dn_list_file, "r") as file:
    dn_numbers = {line.strip() for line in file}  # Use a set for fast lookups

# Track missing DNs
missing_dns = set(dn_numbers)
copied_files = []

# Iterate through files in source folder
for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)

    # Check if file is a PDF and matches any DN number
    if file_name.endswith(".pdf"):
        dn_number = os.path.splitext(file_name)[0]  # Remove .pdf extension
        if dn_number in dn_numbers:
            shutil.copy(file_path, destination_folder)
            copied_files.append(dn_number)
            missing_dns.discard(dn_number)  # Remove found DN from missing list

# Write missing DNs to error log
if missing_dns:
    with open(error_log_file, "w") as log_file:
        log_file.write("Missing DNs (Not Found in Source Folder):\n")
        for missing_dn in sorted(missing_dns):
            log_file.write(missing_dn + "\n")

# Summary Output
print(f"Task completed. {len(copied_files)} files copied.")
if missing_dns:
    print(f"{len(missing_dns)} missing DNs logged in: {error_log_file}")
else:
    print("All DN files were found and copied.")