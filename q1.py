import json

faculty_data = [
    {
        "Faculty ID": "F001",
        "Faculty Name": "Dr. Alice Smith",
        "Department": "Computer Science",
        "Publications": 25,
        "H-index": 12,
        "Project Budget Requested": 120000,
        "Industry Collaboration Score": 85
    },
    {
        "Faculty ID": "F002",
        "Faculty Name": "Dr. Bob Jones",
        "Department": "Electrical Engineering",
        "Publications": 15,
        "H-index": 8,
        "Project Budget Requested": 95000,
        "Industry Collaboration Score": 60
    },
    {
        "Faculty ID": "F003",
        "Faculty Name": "Dr. Carol White",
        "Department": "Computer Science",
        "Publications": 30,
        "H-index": 18,
        "Project Budget Requested": -50000,  # Invalid budget for requirement 10
        "Industry Collaboration Score": 90
    },
    {
        "Faculty ID": "F004",
        "Faculty Name": "Dr. David Brown",
        "Department": "Mechanical Engineering",
        "Publications": 10,
        "H-index": 5,
        "Project Budget Requested": 110000,
        "Industry Collaboration Score": 40
    },
    {
        "Faculty ID": "F005",
        "Faculty Name": "Dr. Eva Green",
        "Department": "Electrical Engineering",
        "Publications": 20,
        "H-index": 10,
        "Project Budget Requested": 150000,
        "Industry Collaboration Score": 75
    }
]

processed_faculty = []

print("=== PROCESSING FACULTY DATA ==-\n")

for faculty in faculty_data:
    # 10. Handle invalid budgets (negative or non-numeric check)
    budget = faculty["Project Budget Requested"]
    try:
        budget = float(budget)
        if budget < 0:
            raise ValueError("Budget cannot be negative.")
    except (ValueError, TypeError):
        print(f"Warning: Invalid budget detected for {faculty['Faculty Name']}. Resetting budget to $0.00.")
        budget = 0.0

    # 1. Calculate research score
    pubs = faculty["Publications"]
    h_index = faculty["H-index"]
    collab = faculty["Industry Collaboration Score"]
    
    research_score = (0.4 * pubs) + (0.3 * h_index) + (0.3 * collab)

    # 2. Allocate grants according to research score (proportional scale capped at requested budget)
    allocation_factor = min(1.0, research_score / 60.0)
    allocated_grant = budget * allocation_factor

    processed_faculty.append({
        "Faculty ID": faculty["Faculty ID"],
        "Faculty Name": faculty["Faculty Name"],
        "Department": faculty["Department"],
        "Research Score": round(research_score, 2),
        "Requested Budget": budget,
        "Allocated Grant": round(allocated_grant, 2)
    })

# 5. Rank faculty members by research score in descending order
ranked_faculty = sorted(processed_faculty, key=lambda x: x["Research Score"], reverse=True)
for rank, f in enumerate(ranked_faculty, start=1):
    f["Rank"] = rank

print("\n--- Faculty Rankings ---")
for f in ranked_faculty:
    print(f"Rank {f['Rank']}: {f['Faculty Name']} ({f['Department']}) | Score: {f['Research Score']} | Grant: ${f['Allocated Grant']:,.2f}")

# 3. Display faculty receiving grants above $100,000
print("\n--- Faculty Receiving Grants Above $100,000 ---")
high_grants = [f for f in ranked_faculty if f["Allocated Grant"] > 100000]
if high_grants:
    for f in high_grants:
        print(f"{f['Faculty Name']} ({f['Department']}): ${f['Allocated Grant']:,.2f}")
else:
    print("No faculty received grants above $100,000.")

# 4. Find the department receiving maximum funding
dept_funding = {}
for f in ranked_faculty:
    dept = f["Department"]
    dept_funding[dept] = dept_funding.get(dept, 0.0) + f["Allocated Grant"]

max_department = max(dept_funding, key=dept_funding.get) if dept_funding else "None"
print(f"\n--- Department with Maximum Funding ---")
print(f"{max_department} with total funding of ${dept_funding[max_department]:,.2f}")

# 6. Calculate average research score
total_score = sum(f["Research Score"] for f in ranked_faculty)
avg_score = total_score / len(ranked_faculty) if ranked_faculty else 0
print(f"\n--- Average Research Score ---")
print(f"Overall Average Research Score: {avg_score:.2f}")

# 7. Identify the top performer
top_performer = ranked_faculty[0] if ranked_faculty else None
print(f"\n--- Top Performer ---")
if top_performer:
    print(f"{top_performer['Faculty Name']} from {top_performer['Department']} (Research Score: {top_performer['Research Score']})")

# 8. Save the rankings to a file
filename = "faculty_rankings.json"
with open(filename, "w") as file:
    json.dump(ranked_faculty, file, indent=4)
print(f"\n--- File Operation ---")
print(f"Rankings successfully saved to '{filename}'.")

# 9. Read the rankings back from the file
print(f"\n--- Reading Rankings Back From File ---")
with open(filename, "r") as file:
    loaded_rankings = json.load(file)
    for f in loaded_rankings:
        print(f"Loaded [Rank {f['Rank']}]: {f['Faculty Name']} | Score: {f['Research Score']} | Grant: ${f['Allocated Grant']:,.2f}")
