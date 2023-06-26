
import os


# Function to convert
def str_to_dict(str_content):
    dic_content = eval(str_content)
    if not isinstance(dic_content, dict):
        raise ValueError("The input string does not represent a valid dictionary.")
    return dic_content

def dict_to_obj(json_data):
    if type(json_data) == dict:  # If it's a dictionary
        converted_data = {}
        for key, value in json_data.items():
            converted_data[key] = dict_to_obj(value)  # Recursively convert the values
        return converted_data
    elif type(json_data) == list:  # If it's a list
        converted_data = []
        for item in json_data:
            converted_data.append(dict_to_obj(item))  # Recursively convert the items
        return converted_data
    else:  # Otherwise, it's a primitive value
        return json_data

def obj_to_dict(obj):
    if isinstance(obj, dict):  # If it's a dictionary
        converted_data = {}
        for key, value in obj.items():
            converted_data[key] = obj_to_dict(value)  # Recursively convert the values
        return converted_data
    elif isinstance(obj, list):  # If it's a list
        converted_data = []
        for item in obj:
            converted_data.append(obj_to_dict(item))  # Recursively convert the items
        return converted_data
    else:  # Otherwise, it's a primitive value
        return obj

def dict_to_str(dictionary, indent_level=0):
    indent = '\t' * indent_level
    dict_str = "{\n"
    for key, value in dictionary.items():
        dict_str += f"{indent}\t{repr(key)}: "
        if isinstance(value, dict):
            dict_str += dict_to_str(value, indent_level + 1)
        else:
            dict_str += repr(value)
        dict_str += ",\n"
    dict_str += f"{indent}}}"

    dict_str = dict_str.replace("'",'"')
    
    for i in range(len(dict_str)):
        if dict_str[i] == ',':
            j = i
            while j < len(dict_str):
                if dict_str[j] == '}':
                    dict_str = dict_str[:i] + ' ' + dict_str[i + 1:]
                    break
                elif dict_str[j] == '"':
                    break
                j += 1
           
    return dict_str

def str_to_arr(str_in):
    # Remove extra spaces between elements and split the string
    arr = str_in.replace(" ", "").split(",")

    # Remove empty elements (if any)
    arr = [element.strip() for element in arr if element.strip()]

    return arr

# User Functions 
def print_data(file):
    print("\n--Show mode--")
    file.flush()
    file.seek(0)
    data = file.read()
    
    if len(data) == 0:
        print("JSON file is empty:")
        return
    print(data)
    print("-Done-")

def edit_data(file, path):
    print("\n--Edit mode--")
    file.flush()
    file.seek(0)
    data_in = file.read()
    if len(data_in) == 0:
        print("JSON file is empty:")
        return

    # convert data to object
    dict_in = str_to_dict(data_in)
    obj = dict_to_obj(dict_in)

    key = input("Enter the key to edit(use ':' for deep level): ").replace(" ", "")
    key = key.split(":") # key is array of key strings

    key_levels = [obj]  # List to store the levels of nested dictionaries

    # Traverse through the levels of keys
    for k in key[:-1]:
        if key_levels[-1].get(k) == None:
            print(f"Key '{k}' wasn't found")
            return
        key_levels.append(key_levels[-1][k])

    # Check if the last key exists in the last level
    if key[-1] not in key_levels[-1]:
        print(f"Key '{key[-1]}' wasn't found")
        return

    print(f"Key was found in {len(key_levels)} level(s)")
    value = input("Enter the value to edit (use ',' to separate values): ").replace(" ", "")
    value = value.split(",")  # value is an array of value strings

    # Assign the value to the last key in the last level
    if len(value) > 1:
        key_levels[-1][key[-1]] = value
    else:
        key_levels[-1][key[-1]] = value[0]

    #reconvert object to string
    dict_out = obj_to_dict(obj)
    str_out = dict_to_str(dict_out)
    
    # open temp write sream
    file_tmp = open(path, "w")  
    file_tmp.truncate() 
    file_tmp.write(str_out)
    file_tmp.close()

    print("-Done-")
def add_data(file, path):
    print("\n--Add mode--")
    file.flush()
    file.seek(0)
    data_in = file.read()
    if len(data_in) == 0:
        print("JSON file is empty:")
        return

    # convert data to object
    dict_in = str_to_dict(data_in)
    obj = dict_to_obj(dict_in)

    key = input("Enter the key to add(use ':' for deep level): ").replace(" ", "")
    key = key.split(":") # key is array of key strings
    
    def check_input(prompt):
        ans = input(prompt)
        while ans not in ['y', 'n', 'N', 'Y']:
            ans = input("Incorrect command, enter 'y' or 'n': ")
        return ans in ['y', 'Y']

    if len(key) == 1:
        if obj.get(key[0]) != None:
            print("Key already exists")
            print(key[0] + ' : ', end="")
            print(obj[key[0]])
            
            if check_input("Change mode to edit? (enter 'y' to confirm or 'n' to cancel): "):
                edit_data(file, path)
            else:
                print("- Canceled -")
                return
        else:
            value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
            obj[key[0]] += value[0] if len(value) == 1 else value

    elif len(key) == 2:
        if obj.get(key[0]) is not None:
            if obj[key[0]].get(key[1]) is not None:
                print("Key already exists")
                print(key[0] + ' : ' + key[1] + ' : ', end='')
                print(obj[key[0]][key[1]])

                if check_input("Change mode to edit? (enter 'y' to confirm or 'n' to cancel): "):
                    edit_data(file, path)
                else:
                    print("- Canceled -")
                    return
            else:
                value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
                if len(value) == 1:
                    obj[key[0]][key[1]] = value[0]
                else:
                    obj[key[0]][key[1]] = value
        else:
            value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
            if len(value) == 1:
                obj[key[0]] = {key[1]: value[0]}
            else:
                obj[key[0]] = {key[1]: value}
    elif len(key) == 3:
        if obj.get(key[0]) != None:
            if obj.get(key[0]).get(key[1]) != None:
                if obj.get(key[0]).get(key[1]).get(key[2]) != None:
                    print("Key already exists")
                    print(key[0] + ' : ' + key[1] + ' : ' + key[2] + ' : ', end="")
                    print(obj[key[0]][key[1]][key[2]])

                    if check_input("Change mode to edit? (enter 'y' to confirm or 'n' to cancel): "):
                        edit_data(file, path)
                    else:
                        print("- Canceled -")
                        return
                else:
                    value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
                    if len(value) == 1:
                        obj[key[0]][key[1]][key[2]] = value[0]
                    else:
                        obj[key[0]][key[1]][key[2]] = value
            else:
                value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
                if len(value) == 1:
                    obj[key[0]][key[1]][key[2]] = value[0]
                else:
                    obj[key[0]][key[1]][key[2]] = value
        else:
            value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
            if len(value) == 1:
                obj[key[0]][key[1]][key[2]] = value[0]
            else:
                obj[key[0]][key[1]][key[2]] = value
    else:
        print("Incorrect Key!")
        return
  

    #reconvert object to string
    dict_out = obj_to_dict(obj)
    str_out = dict_to_str(dict_out)
    
    # open temp write sream
    file_tmp = open(path, "w")  
    file_tmp.truncate() 
    file_tmp.write(str_out)
    file_tmp.close()

    print("-Done-")

    # convert data to object
    dict_in = str_to_dict(data_in)
    obj = dict_to_obj(dict_in)

    key = input("Enter the key to add(use ':' for deep level): ").replace(" ", "")
    key = key.split(":") # key is array of key strings
    
    def check_input(prompt):
        ans = input(prompt)
        while ans not in ['y', 'n', 'N', 'Y']:
            ans = input("Incorrect command, enter 'y' or 'n': ")
        return ans == 'y' or ans == 'Y'

    if len(key) == 1:
        if obj.get(key[0]) != None:
            print("Key already exists")
            print(key[0] + ' : ', end="")
            print(obj[key[0]])
            
            if check_input("Change mode to edit? (enter 'y' to confirm or 'n' to cancel): "):
                edit_data(file, path)
            else:
                print("- Canceled -")
                return
        else:
            value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
            obj[key[0]] = value[0] if len(value) == 1 else value

    elif len(key) == 2:
        if obj.get(key[0]) != None:
            if obj.get(key[0]).get(key[1]) != None:
                print("Key already exists")
                print(key[0] + ' : ' + key[1] + ' : ', end='')
                print(obj[key[0]][key[1]])

                if check_input("Change mode to edit? (enter 'y' to confirm or 'n' to cancel): "):
                    edit_data(file, path)
                else:
                    print("- Canceled -")
                    return
            else:
                value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
                obj[key[0]][key[1]] = value[0] if len(value) == 1 else value
        else:
            value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
            obj[key[0]][key[1]] = value[0] if len(value) == 1 else value

    elif len(key) == 3:
        if obj.get(key[0]) != None:
            if obj.get(key[0]).get(key[1]) != None:
                if obj.get(key[0]).get(key[1]).get(key[2]) != None:
                    print("Key already exists")
                    print(key[0] + ' : ' + key[1] + ' : ' + key[2] + ' : ', end="")
                    print(obj[key[0]][key[1]][key[2]])

                    if check_input("Change mode to edit? (enter 'y' to confirm or 'n' to cancel): "):
                        edit_data(file, path)
                    else:
                        print("- Canceled -")
                        return
                else:
                    value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
                    obj[key[0]][key[1]][key[2]] = value[0] if len(value) == 1 else value
            else:
                value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
                obj[key[0]][key[1]][key[2]] = value[0] if len(value) == 1 else value
        else:
            value = input("Enter the value (use ',' to separate values): ").replace(" ", "").split(",")
            obj[key[0]][key[1]][key[2]] = value[0] if len(value) == 1 else value

  

    #reconvert object to string
    dict_out = obj_to_dict(obj)
    str_out = dict_to_str(dict_out)
    
    # open temp write sream
    file_tmp = open(path, "w")  
    file_tmp.truncate() 
    file_tmp.write(str_out)
    file_tmp.close()

    print("-Done-")

def delete_data(file, path):
    print("\n--Delete mode--")
    file.flush()
    file.seek(0)
    data_in = file.read()
    if len(data_in) == 0:
        print("JSON file is empty:")
        return
    
    # convert data to object
    dict_in = str_to_dict(data_in)
    obj = dict_to_obj(dict_in)
    
    key = input("Enter the key to delete (use ':' for deep level): ").replace(" ", "")
    key = key.split(":") # key is array of key strings

    def confirm_delete(key):
        ans = input("Delete? (enter 'y' to confirm or 'n' to cancel): ").replace(" ", "")
        while ans.lower() not in ['y', 'n']:
            ans = input("Incorrect command. Enter 'y' for yes or 'n' for no: ")
        return ans.lower() == 'y'


    if len(key) == 1 and key[0] in obj:
        print("Key was found at level 1")
        print(key[0] + " : ", end="")
        print(obj[key[0]])

        if confirm_delete(key):
            del obj[key[0]]
        else:
            print("-Canceled-")
            return

    elif len(key) == 2 and key[0] in obj and key[1] in obj[key[0]]:
        print("Key was found at level 2")
        print(key[0] + " : " + key[1] + " : ", end="")
        print(obj[key[0]][key[1]])

        if confirm_delete(key):
            del obj[key[0]][key[1]]
        else:
            print("-Canceled-")
            return

    elif len(key) == 3 and key[0] in obj and key[1] in obj[key[0]] and key[2] in obj[key[0]][key[1]]:
        print("Key was found at level 3")
        print(key[0] + " : " + key[1] + " : " + key[2] + " : ", end="")
        print(obj[key[0]][key[1]][key[2]])

        if confirm_delete(key):
            del obj[key[0]][key[1]][key[2]]
        else:
            print("-Canceled-")
            return

    else:
        print("Key wasn't found!")
        return

    #reconvert object to string
    dict_out = obj_to_dict(obj)
    str_out = dict_to_str(dict_out)
    
     # open temp write sream
    file_tmp = open(path, "w")  
    file_tmp.truncate() 
    file_tmp.write(str_out)
    file_tmp.close()

    print("-Done-")



#int main(){

# path = "data.json"
# file = open(path, "r")

# while True:
#     print("\n----PYTHON JSON PARSER----")
#     print("1. Show data.")
#     print("2. Edit data.")
#     print("3. Add data.")
#     print("4. Delete data.")
#     print("5. Exit.")

#     com_id = input("Enter the command ID: ")
#     while com_id != '1' and com_id != '2' and com_id != '3' and com_id != '4' and com_id != '5':
#         com_id = input("Incorrect command ID, enter '1' '2' '3' '4' or '5': ")

#     com_id = int(com_id)

# # main commands
#     if com_id == 5:
#         file.close()
#         quit()

#     if com_id == 1:
#         print_data(file)
    
#     elif com_id == 2:
#         edit_data(file, path)
    
#     elif com_id == 3:
#         add_data(file, path)
    
#     elif com_id == 4:
#         delete_data(file, path)
        
        
def main():
    path = 'data.json'
    
    if not os.path.exists(path):
        with open(path, mode='w') as file:
            file.write('{\n\n}')
        
    file = open(path, mode='r+')
    
    while True:
        print("\n----PYTHON JSON PARSER----")
        print("1. Show data.")
        print("2. Edit data.")
        print("3. Add data.")
        print("4. Delete data.")
        print("5. Exit.")
    
        com_id = int(input('Enter the command ID: '))
        while com_id not in range(1, 6):
            com_id = int(input("Incorrect command ID, enter '1' '2' '3' '4' or '5': "))
            
        if com_id == 5:
            file.close()
            break

        if com_id == 1:
            print_data(file)
        
        elif com_id == 2:
            edit_data(file, path)
        
        elif com_id == 3:
            add_data(file, path)
        
        elif com_id == 4:
            delete_data(file, path)
    
    
    file.close()
    

if __name__ == '__main__':
    main()
