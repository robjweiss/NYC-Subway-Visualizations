api_ids = {}
api_ids[1] = ["1", "2", "3", "4", "5", "6"]
api_ids[26] = ["A", "C", "E", "H", "S"]
api_ids[16] = ["N", "Q", "R", "W"]
api_ids[21] = ["B", "D", "F", "M"]
api_ids[2] = ["L"]
api_ids[11] = ["SIR"]
api_ids[31] = ["G"]
api_ids[36] = ["J", "Z"]
api_ids[51] = ["7"]

def find_id(route):
	for k,v in api_ids.items():
		if route in v:
			return k
	return -1