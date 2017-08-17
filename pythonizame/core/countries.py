from django_countries import countries

COUNTRIES_LIST = ()
COUNTRIES_JSON_LIST = []

for code, name in list(countries):
    COUNTRIES_LIST += (code, name),


for code, name in list(countries):
    COUNTRIES_JSON_LIST.append({'code': code, 'name': name})
