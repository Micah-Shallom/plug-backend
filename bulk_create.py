import json, requests

def read_json(file_path):
    """
    Function to read JSON data from a file.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - data (list): A list containing JSON objects read from the file.
    """

    print(file_path)

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    except Exception as e:
        # Handle exceptions if needed
        print(f"Error occurred while reading JSON file: {str(e)}")
        return []
    

def bulk_post_data():
    data_list = read_json("./category.json")
    url = "http://localhost:5000/project"

    response_list = []
    for data in data_list:
        try:
            response = requests.post(url,  data)
            response_list.append(response)

        except Exception as e:
            print(f"Error occured while making POST request: {str(e)}")

    return response_list

responses = bulk_post_data()
for response in responses:
    print(response.status_code, response.text)