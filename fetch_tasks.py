
import requests
import csv
import sys

API_URL = "https://jsonplaceholder.typicode.com/todos"


def fetch_tasks():
    """Fetch tasks from a third-party REST API."""
    try:
        # Step 1: Send HTTP GET request
        response = requests.get(API_URL, timeout=10)

        # Step 2: Check HTTP status
        response.raise_for_status()

        # Step 3: Parse JSON response
        tasks = response.json()

        # Step 4: Validate response format
        if not isinstance(tasks, list):
            raise ValueError("Expected a list of tasks")

        return tasks

    except requests.exceptions.Timeout:
        print("Error: API request timed out.", file=sys.stderr)

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}", file=sys.stderr)

    except ValueError as error:
        print(f"Invalid API response: {error}", file=sys.stderr)

    return None


def save_to_csv(tasks, filename="tasks.csv"):
    """Save task data to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write CSV header
        writer.writerow(["userId", "id", "title", "completed"])

        # Write task records
        for task in tasks:
            writer.writerow([
                task["userId"],
                task["id"],
                task["title"],
                task["completed"]
            ])


def main():
    # Fetch data from API
    tasks = fetch_tasks()

    if tasks is None:
        return 1

    try:
        # Print summary
        print(f"Successfully fetched {len(tasks)} tasks.")

        completed = sum(
            1 for task in tasks if task["completed"] is True
        )

        pending = len(tasks) - completed

        print(f"Completed tasks: {completed}")
        print(f"Pending tasks: {pending}")

        # Save to CSV
        save_to_csv(tasks)

        print("Data saved to tasks.csv")

    except (KeyError, TypeError, ValueError) as error:
        print(f"Invalid task data: {error}", file=sys.stderr)
        return 1

    except OSError as error:
        print(f"File error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
