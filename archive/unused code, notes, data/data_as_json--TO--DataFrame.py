#data derping with data cocktail object retruned from line 330#
#>	elif glass in ['json','JSON','Json','first_mixed_and_Pouredson','javascript']:
#			save_dir=raw_input('Great! paste in the full path where you would like your file. For now, it will be a csv.')
#			save_dir=str(save_dir)
#			os.chdir(save_dir)
#			with open('data_cocktail.json', 'w') as fp:
#				json.dump(Mixed_and_Poured, fp)
##############
#daft=open("C:\USERS\VINCE\DESKTOP\DATA_COCKTAIL1.json",'r')
#dat=daft.read()
#first_mixed_and_Poured=json.loads(dat)


##merge on country and year first, scanning to compare eache item with eeach item

d=0
nxt_i=d+1
while d <= len(first_mixed_and_Poured):
	if nxt_i < len(first_mixed_and_Poured):
		if first_mixed_and_Poured[d]['Country'] + first_mixed_and_Poured[d]['Year'] == first_mixed_and_Poured[nxt_i]['Country'] + first_mixed_and_Poured[nxt_i]['Year']:
			first_mixed_and_Poured[d].update(first_mixed_and_Poured[nxt_i])
			first_mixed_and_Poured.pop(nxt_i)
		else:
			nxt_i+=1
	else:
		print 'moving to next ob at nxt ob at'
		print nxt_i
		d+=1
		nxt_i=d+1

#bind to DF and index by country and year
duff=pd.DataFrame()

for s in range(len(first_mixed_and_Poured)):
		duff=duff.append(first_mixed_and_Poured[s], ignore_index=True)

duff.set_index(['Country', 'Year'], drop=True, append=False, inplace=True, verify_integrity=False)