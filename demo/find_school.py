
import ct_schools.schools as schools
import json
# print schools.school_by_name("Shepau Valley", closest=True)

# print schools.schooldf().head(1)

# print schools.school_by_name("Shepaug")

print json.dumps(
    json.loads(
        schools.school_by_name("Shepau Valley", closest=True).to_json(orient="records")
        ), indent=2
    )


