import os

file_extensions = {
    '.java' : 'Java',
    '.c' : 'C',
    '.cpp' : 'C++',
    '.js' : 'Javascript',
    '.ejs' : 'EJS'
}

line_counts = {}

def add_to_count(ext, count):
    lang = file_extensions[ext]
    if lang in line_counts.keys():
        line_counts[lang] += count
    else:
        line_counts[lang] = count

def print_clean_output(d):
    total = 0
    for count in line_counts.values():
        total += count
    print("The total no of lines: {}".format(total))
    for lang in d:
        print("{} : {:.2f}%".format(lang, d[lang]/total * 100))


def count_lines(path):
    count = 0;
    contents = os.listdir(path)
    for item in contents:
        item_path = os.path.join(path, item)
        _ , ext = os.path.splitext(item_path)
        if os.path.isfile(item_path) and ext in file_extensions.keys():
            o = open(item_path, 'r')
            add_to_count(ext, len(o.readlines()))
            o.close()
        if os.path.isdir(item_path):
            count_lines(item_path)

count_lines('/home/abialbon/Documents/Projects')
print_clean_output(line_counts)