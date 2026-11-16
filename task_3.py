import sys
from pathlib import Path

LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")

def parse_log_line(line: str) -> dict:
    """Parse "date time LEVEL message" into a dict

    Returns an empty dict if the line is invalid or the level is unknown
    """
    data = line.split()
    if len(data) > 3:
        date, time, level, *message = data
        if level in LEVELS:
            return {"date": date,
                      "time": time,
                      "level": level,
                      "message": " ".join(message)}
        
    return {}

def load_logs(file_path: str) -> list:
    """Read the file and return a list of parsed log entries"""
    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                # in case of an empty line
                if not line:
                    continue
                data = parse_log_line(line)
                if data:
                    logs.append(data)
                else:
                    print(f"Skipping invalid line: {line}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except (OSError, UnicodeDecodeError) as error:
        print(f"Cannot read {file_path}: {error}")
        return []
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    """Return only the entries with the given level"""
    return list(filter(lambda x: x["level"] == level, logs))

def count_logs_by_level(logs: list) -> dict:
    """Return {level: number of entries} for every known level"""
    return {level: len(filter_logs_by_level(logs, level)) for level in LEVELS}
    
def display_log_counts(counts: dict):
    """Print the counts as a table"""
    headers = ["Рівень логування", "Кількість"]
    columns_widths = [max([len(headers[0])] + [len(level) for level in counts.keys()]),
                      max([len(headers[1])] + [len(str(count)) for count in counts.values()])]
    
    print(f"{headers[0]:<{columns_widths[0]}} | {headers[1]:<{columns_widths[1]}}")
    print(f"{'-' * (columns_widths[0] + 1)}|{'-' * (columns_widths[1] + 1)}")
    for level, count in counts.items():
        print(f"{level:<{columns_widths[0]}} | {count:<{columns_widths[1]}}")


        


def main():
    if len(sys.argv) < 2:
        print("Please provide a file path!")
        return
    
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Path does not exist: {path}")
        return
    
    logs = load_logs(path)
    if not logs:
            print("No valid information in the file")
            return
    
    display_log_counts(count_logs_by_level(logs))
    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        if level not in LEVELS:
            print("Log level is unknown!")
            return
        
        logs_for_level = filter_logs_by_level(logs,level) 
        if not logs_for_level:
            print("No logs for the level available")
            return
        print(f"\nДеталі логів для рівня {level}:")
        for log in logs_for_level:
            print(f"{log['date']} {log['time']} - {log['message']}")
        

                

if __name__ == "__main__":
    main()