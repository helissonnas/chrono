import csv

def export_to_csv(data, filename):
    # Open the CSV file in write mode
    with open(filename + ".csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'time'])
        writer.writeheader()
        
        # Write each dictionary in the time_list as a separate row in the CSV file
        for item in data:
            writer.writerow(item)
    
    print(f"Data has been exported to {filename}.csv")
