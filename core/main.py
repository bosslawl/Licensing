from assets.modules import *

database = "assets/database/main.sqlite"
app = FastAPI()

@app.get("/")
async def root(request: Request, license = None):
    
    connection = request.headers.get('CF-Connecting-IP')
    database = sqlite3.connect(database)
    cursor = database.cursor()
    
    if license is None:
        print(f'{connection} connected to the API without passing a license key.')
        return {"Status": "Failed", "Reason": "No License Provided"}
    
    current = datetime.utcnow()
    cursor.execute(f'SELECT License FROM Licenses WHERE License = "{license}" AND Expiry > "{current}"')
    result = cursor.fetchone()
    
    if result is None:
        print(f'{connection} connected to the API with an invalid license key.')
        return {"Status": "Failed", "Reason": "Invalid License Provided"}
    
    cursor.execute(f'SELECT Expiry FROM Licenses WHERE License = "{license}" AND expiry > "{current}"')
    expiry = cursor.fetchone()
    cursor.execute(f'SELECT IPv4 FROM Licenses WHERE License = "{license}" AND expiry > "{current}"')
    result = cursor.fetchone()
    
    

@app.get('/')
async def checklic(request: Request, license = None):
	forwarded = request.headers.get("CF-Connecting-IP")
	db = sqlite3.connect('license.sqlite')
	cursor = db.cursor()
	if license is None:
		print(f"No License Passed:\nOrigin: {forwarded}")
		return {"Status": "Failed", "Reason": "No License Provided"}
	rn = datetime.utcnow()
	cursor.execute(f'SELECT License FROM Licenses WHERE License = "{license}" AND Expiry > "{rn}"')
	result = cursor.fetchone()
	if result is None:
		print(f"Invalid License Passed:\nOrigin: {forwarded}")
		return {"Status": "Failed", "Reason": "Invalid License Provided"}
	cursor.execute(f'SELECT Expiry FROM Licenses WHERE License = "{license}" AND expiry > "{rn}"')
	urmom = cursor.fetchone()
	cursor.execute(f'SELECT IPv4 FROM Licenses WHERE License = "{license}" AND expiry > "{rn}"')
	result = cursor.fetchone()
	if result == (None,):
		cursor.execute(f'UPDATE Licenses SET IPv4 = "{forwarded}" WHERE License = "{license}"')
		db.commit()
		return {"Status": "Success", "Reason": urmom[0]}
	elif result[0] != forwarded:
		print(f"IP Lock Fail:\nOrigin: {forwarded}\nLicense: {license}")
		return {"Status": "Failed", "Reason": "IP Lock"}
	else:
		return {"Status": "Success", "Reason": urmom[0]}

@app.get('/cnc')
async def checkcnc(request: Request, license = None):
	forwarded = request.headers.get("CF-Connecting-IP")
	db = sqlite3.connect('licensecnc.sqlite')
	cursor = db.cursor()
	if license is None:
		print(f"No License Passed:\nOrigin: {forwarded}")
		return {"Status": "Failed", "Reason": "No License Provided"}
	rn = datetime.utcnow()
	cursor.execute(f'SELECT License FROM Licenses WHERE License = "{license}" AND Expiry > "{rn}"')
	result = cursor.fetchone()
	if result is None:
		print(f"Invalid License Passed:\nOrigin: {forwarded}")
		return {"Status": "Failed", "Reason": "Invalid License Provided"}
	cursor.execute(f'SELECT Expiry FROM Licenses WHERE License = "{license}" AND expiry > "{rn}"')
	urmom = cursor.fetchone()
	cursor.execute(f'SELECT IPv4 FROM Licenses WHERE License = "{license}" AND expiry > "{rn}"')
	result = cursor.fetchone()
	if result == (None,):
		cursor.execute(f'UPDATE Licenses SET IPv4 = "{forwarded}" WHERE License = "{license}"')
		db.commit()
		return {"Status": "Success", "Reason": urmom[0]}
	elif result[0] != forwarded:
		print(f"IP Lock Fail:\nOrigin: {forwarded}\nLicense: {license}")
		return {"Status": "Failed", "Reason": "IP Lock"}
	else:
		return {"Status": "Success", "Reason": urmom[0]}