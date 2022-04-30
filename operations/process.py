from cgitb import html
import markdown
import codecs
import shutil
import os

MDS_PATH = "../mds/"
OUT_PATH = "../pages/"

EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
    'markdown.extensions.tables',
    'fenced_code',
]

INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>##TITLE##</title>
    <style>
        html {
            user-select: none;
        }
        b {
            position: absolute;
        }
        h1 {
            color: #000000;
            position: absolute;
            left: 5%;
            top: 0%;
        }
        .dir {
            color: blue;
        }
        .dir:hover {
            color: cornflowerblue;
            text-decoration: none;
        }
        .file {
            color: black;
        }
        .file:hover {
            color: cornflowerblue;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <h1>##TITLE##</h1>
    <hr noshade="noshade" size="3" color="#7F7F7F" style="width:100%;position:fixed;top:8%" />
    ##HERFS##
</body>
</html>
'''

ARTICLE_TEMPLATE = '''
<html lang="zh-cn">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>##TITLE##</title>
        <link href="##ROOT_PATH##/css/default.css" rel="stylesheet">
    </head>
    <body>
        ##BODY##
    </body>
</html>
'''

def process_current_path(current_path = "./", root_path = "..", depth = "|-"):
    print(f"{depth}进入文件夹 - {current_path}")
    fileList  = os.listdir(MDS_PATH + current_path)
    dir_list  = []
    file_list = []
    for file in fileList:
        temp = current_path + file
        if os.path.isdir(MDS_PATH + temp):
            dir_list.append([temp, file])
        else:
            file_list.append([temp, file[:file.find('.')]])
    title = current_path
    index_file  = open(OUT_PATH + current_path + "index.html", "w+", encoding="utf-8")
    # TODO title can't include "##HERFS##"
    index_text  = INDEX_TEMPLATE.replace("##TITLE##", title)
    herfs_text  = ""
    # process dir list first
    current_top = 128
    top_adder   = 32
    next_depth  = "| " + depth
    for dir in dir_list:
        href_path    = dir[1] + "/index.html"
        herfs_text  += f"<a href=\"{href_path}\"><b class=\"dir\" style=\"top:{current_top}px;left:8%;\">{dir[1]}</b></a>\n"
        current_top += top_adder
        os.mkdir(OUT_PATH + current_path + dir[1])
        process_current_path(dir[0] + "/", root_path + "/..", next_depth)
    for file in file_list:
        print(f"{next_depth}处理文件 - {file[0]}")

        input_file  = open(MDS_PATH + file[0], mode="r", encoding="utf-8")
        text        = input_file.read()
        body_text   = markdown.markdown(text, extensions=EXTENSIONS)
        html_name   = file[1] + ".html"
        html_text   = ARTICLE_TEMPLATE.replace("##TITLE##", file[1])
        html_text   = html_text.replace("##BODY##", body_text)
        html_text   = html_text.replace("##ROOT_PATH##", root_path)
        output_file = open(OUT_PATH + current_path + html_name, "w+", encoding="utf-8")
        output_file.write(html_text)
        output_file.close()

        herfs_text  += f"<a href=\"{html_name}\"><b class=\"file\" style=\"top:{current_top}px;left:8%;\">{file[1]}</b></a>\n"
        current_top += top_adder
    index_text = index_text.replace("##HERFS##", herfs_text)
    index_file.write(index_text)
    index_file.close()
    print(f"{depth}退出文件夹 - {current_path}")

if os.path.exists("./process.py"):
    shutil.rmtree(OUT_PATH)
    os.mkdir(OUT_PATH)
    process_current_path()