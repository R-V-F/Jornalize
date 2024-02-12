from datetime import datetime

# Get the current timestamp
current_timestamp = datetime.now()

# Print the timestamp in a custom format
formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
print("Executando scriptX:", formatted_timestamp)