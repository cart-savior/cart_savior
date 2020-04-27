def get_dpr1(item, start_date):
# 	df = None
# 	while (1):
# 		obj = extract_from_url(start_date, item)
# 		try:
# 			df = pd.DataFrame(obj['data']['item'])
# 			df = df[df.item_name == item['item_name']]
# 		except TypeError:
# 			start_date = start_date - timedelta(days=1)
# 			continue
# 		# rank가 일치하는 행 뽑아내기
# 		import pdb; pdb.set_trace()
# 		row = df[df['rank']==item['rank']].iloc[0]
# 		if ("-" in row.dpr1):
# 			start_date = start_date - timedelta(days=1)
# 			continue
# 		else:
# 			break