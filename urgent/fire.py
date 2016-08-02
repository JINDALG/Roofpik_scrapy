from firebase import firebase
import traceback
from pprint import pprint
from api import entry_data

def display(data):
	minn = 10e16
	maxx = 0
	count,avg = 0,0
	for web in data:
		for bhk in data[web]:
			minn = min(minn,data[web][bhk]['min'])
			maxx = max(minn,data[web][bhk]['max'])
			avg += data[web][bhk]['avg']*data[web][bhk]['count']
			count += data[web][bhk]['count']
	avg /= count

	return {
		'min':minn,
		'max' : maxx,
		'avg' : avg
	}

try :
	base = firebase.FirebaseApplication("https://roofpik-26701.firebaseio.com/", None)
	protected_version_editable = base.get('/protectedResidentialVersions/-KN7HFa3un2SPyrUKosy/projects',None)
	for project_id in protected_version_editable:
		ver = protected_version_editable[project_id]['editable']['version']
		protected_residentials = base.get('/protectedResidential/-KN7HFa3un2SPyrUKosy/projects/'+project_id+'/'+ver,None)
		try :
			urls = protected_residentials['aggregator']['url']
			for url in urls:
				if "buy" in url:
					data = entry_data(urls[url])
					i = 0
					while i < 3 and not isinstance(data,dict):
						data = entry_data(urls[url])
						i+=1
					if isinstance(data,dict):
						if 'acres' in url:
							url = '99'+urls
						response = base.put('/protectedResidential/-KN7HFa3un2SPyrUKosy/projects/'+project_id+'/'+ver,'/aggregator/buy/'+url.replace('buy',''),data)
				if "rent" in url:
					data = entry_data(urls[url])
					i = 0
					while i < 3 and not isinstance(data,dict):
						data = entry_data(urls[url])
						i+=1
					if isinstance(data,dict):
						if 'acres' in url:
							url = '99'+urls
						response = base.put('/protectedResidential/-KN7HFa3un2SPyrUKosy/projects/'+project_id+'/'+ver,'/aggregator/rent/'+url.replace('rent',''),data)
				pprint(response)
				pprint(project_id)
			try :
				pricing = base.get('/protectedResidential/-KN7HFa3un2SPyrUKosy/projects/'+project_id+'/'+ver+'/aggregator',None)
				if 'buy' in pricing:
					buy_data = display(pricing['buy'])
					buy_data = response = base.put('/protectedResidential/-KN7HFa3un2SPyrUKosy/projects/'+project_id+'/'+ver,'/displayCost/buy',buy_data)
				if 'rent' in pricing:
					rent_data = display(pricing['rent'])
					rent_data = response = base.put('/protectedResidential/-KN7HFa3un2SPyrUKosy/projects/'+project_id+'/'+ver,'/displayCost/rent',rent_data)
			except :
				print traceback.print_exc();
		except :
			print traceback.print_exc();
except :
	print traceback.print_exc();