
import csv
import json

#read csv file
def read_csv_file(file_path: str):
    try:
        print(f"Reading CSV file from path: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames 
            rows = [row for row in reader]
        
        if rows:
            questions_only = []
            for row in rows:
                questions_only.append(row['email'])

        return {
            "rows": questions_only,
        }

    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except PermissionError:
        return {"error": f"Permission denied: {file_path}"}
    except Exception as e:
        return {"error": str(e)}
    


def write_csv_file(file_path: str, rows: list[dict[str, str]]):

    print(f"Writing CSV file to path: {file_path}")
    print(f"Rows to write: {rows}")

    try:
        if not rows:
            return {"error": "No rows provided to write to CSV"}

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                writer.writerow([
                    row.get("enquiry", ""),
                    row.get("response", ""),
                ])

        return {"status": "success", "file_path": file_path}

    except Exception as e:
        return {"error": f"Unable to write CSV: {e}"}
    
def write_text_to_csv(file_path: str, content: str):

    print(f"Writing text file to path: {file_path}")
    print(f"Content to write: {content}")

    try:
        with open(file_path, "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([content])

        return {"status": "success", "file_path": file_path}

    except Exception as e:
        return {"error": f"Unable to write text file: {e}"}
