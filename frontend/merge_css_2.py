
# Merge new_pages.css to style.css
with open("static/new_pages.css", "r") as f:
    new_css = f.read()

with open("static/style.css", "a") as f:
    f.write("\n" + new_css)
    
import os
os.remove("static/new_pages.css")
print("CSS merged successfully")
