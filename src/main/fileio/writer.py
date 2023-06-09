import csv


def write_billing_results(output_file, users):
    try:
        with open(output_file, 'w') as file:
            writer = csv.writer(file)
            for user in sorted(users.values(), key=lambda x: x.user_id):
                writer.writerow([user.user_id, user.charge])
    except PermissionError:
        print(f"Error: You do not have permission to write to {output_file}.")
    except IOError as e:
        print(f"An IO error occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
