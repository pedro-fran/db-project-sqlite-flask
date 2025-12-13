import csv

# Open input file and create output file
with open("input.csv", newline="", encoding="utf-8") as infile, \
     open("output.csv", "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=["SiteID", "CountryID"])
    writer.writeheader()

    for row in reader:
        site = row["SiteID"].strip()
        countries = row["CountryID"].split(",")
        for c in countries:
            writer.writerow({"SiteID": site, "CountryID": c.strip()})
