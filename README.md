Note that in the excel sheet, only the headers should have borders. Other rows cannot have, otherwise, an error may appear

entry point
run_project.py: extract listings based on keyword
extract_jd.py: extract job description based on link extract in run_project.py

Bugs
Excel
Occassionally, a header is not formatted correctly in excel, although it looks find when you open the excel sheet
Simply copy the cell that is formatted correctly and paste it back to the affected cell, remembering to change the text to the original header name
You can also move the selecter in excel away from the affected header, that might work sometimes
However, the best way is always to copy the entre