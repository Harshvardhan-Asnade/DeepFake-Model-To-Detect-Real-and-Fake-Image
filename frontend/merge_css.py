
# Append results.css to style.css
with open("static/results.css", "r") as f:
    new_css = f.read()

with open("static/style.css", "a") as f:
    f.write("\n" + new_css)
    
import os
os.remove("static/results.css")
print("CSS updated")
