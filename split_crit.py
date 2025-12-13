import csv
import re

with open("input.csv", newline="", encoding="utf-8") as infile, \
     open("output.csv", "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=["SiteID", "CriteriaID"])
    writer.writeheader()

    for row in reader:
        site = row["SiteID"].strip()
        criteria = row["CriteriaID"].strip()

        # Find all groups like (i), (ii), (iv), (x)
        matches = re.findall(r"\([^)]+\)", criteria)

        for m in matches:
            writer.writerow({"SiteID": site, "CriteriaID": m})
