
import ct_schools.schools as schools

print schools.schooldf().head(1)

print schools.school_by_name("Shepaug")

print schools.school_by_name("Shepau Valley", closest=True)


