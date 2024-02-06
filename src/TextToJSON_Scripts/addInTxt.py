import os


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    # print(files)
    return files


def add_full_text(folder_path_read, folder_path_write):
    filenames = list_files_in_directory(folder_path_read)
    for filename in filenames:
        with open(folder_path_read + filename, "r") as file:
            lines = file.readlines()
        print(filename)
        cnt = 0
        found = 0
        i = 0
        while not found:
            if "---" in lines[i]:
                cnt += 1
            if cnt == 2:
                for j in range(i, i + 4):
                    if "License-text:" in lines[j]:
                        found = 1
                        break
                if not found:
                    lines[i + 1] = "License-text: \n \n"

            i += 1

        with open(folder_path_write + filename, "w") as file:
            file.writelines(lines)


add_full_text("../licenses/", "../licenses/")
