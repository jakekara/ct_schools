
import ct_schools.schools as schools

print "-" * 20
print "FIND THE CLOSEST MATCH"
print schools.closest("Shepau Vall")

print "-" * 20
print "FIND THE CLOSEST 3 MATCHES"
print schools.closest("Shepaug Valley School",lim=3)

print "-" * 20
print "FIND AN EXACT (CASE-INSENSITIVE) MATCH"
print schools.exact("Shepaug Valley School")

print "-" * 20
print "FIND ALL MATCHES WITH A FUZZ RATIO ABOVE 80"
print schools.fuzzy("Shepaug Valley School", ratio=80)



