import vitparser

sigs = vitparser.VitalParser(1700)
presigs = sigs.preprocessing()
sigs.display_parameters((2000,3000))
print(presigs)
