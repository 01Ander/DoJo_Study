import random
from datetime import datetime, timedelta

def generate_logs(filename="server_logs.csv", num_lines=2000):
    endpoints = ["/api/v1/users", "/login", "/home", "/api/v1/products", "/checkout", "/cart"]
    statuses = [200, 200, 200, 200, 201, 301, 400, 401, 403, 404, 500, 502, 503]
    
    start_time = datetime(2026, 4, 17, 10, 0, 0)
    
    with open(filename, 'w') as f:
        f.write("timestamp,endpoint,status_code,response_time_ms\n")
        
        for i in range(num_lines):
            # Advance time slightly
            start_time += timedelta(milliseconds=random.randint(10, 5000))
            
            # Determine if this line should be corrupted
            corruption_type = random.choices(
                ["none", "missing_column", "bad_timestamp", "bad_status", "garbage"], 
                weights=[85, 3, 5, 3, 4], 
                k=1
            )[0]
            
            endpoint = random.choice(endpoints)
            status = random.choice(statuses)
            response_time = random.randint(20, 1500)
            
            if corruption_type == "none":
                f.write(f"{start_time.isoformat()},{endpoint},{status},{response_time}\n")
            elif corruption_type == "missing_column":
                f.write(f"{start_time.isoformat()},{endpoint},{status}\n")  # missing response_time
            elif corruption_type == "bad_timestamp":
                # Strange or malformed time format
                bad_time = start_time.strftime("%d-%m-%Y %H:%M:%S")
                f.write(f"{bad_time},{endpoint},{status},{response_time}\n")
            elif corruption_type == "bad_status":
                f.write(f"{start_time.isoformat()},{endpoint},OK,{response_time}\n") # text instead of int
            elif corruption_type == "garbage":
                f.write(f"ERROR: CONNECTION RESET BY PEER at {start_time.isoformat()}\n")

if __name__ == "__main__":
    generate_logs()
    print(f"Generated server_logs.csv successfully!")
