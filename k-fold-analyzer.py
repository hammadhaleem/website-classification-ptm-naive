import json

RESULT_DIR = "result"
MODEL_DIR = "model"
TYPES = ["words", "dp"]
BASE_URL = "http://pmsipilot.github.io"

categories = [u'entertain',u'politics',u'econonics',u'sports',u'education',u'religion',u'health']
counts = json.load(open('%s/data.json'%MODEL_DIR, 'r'))
tsum = sum([c for c in counts.values()])*1.0
stats = {}

for t in TYPES:
	for t1 in TYPES:
		f1 = open('%s/%s-%s.html'%(RESULT_DIR, t, t1), 'w')
		f1.write('''<!DOCTYPE html>
					<html>
					<head>
					<link rel="stylesheet" href="http://pmsipilot.github.io/jquery-highchartTable-plugin/css/bootstrap.min.css">
					<link rel="stylesheet" href="http://pmsipilot.github.io/jquery-highchartTable-plugin/css/main.css">
					<link rel="stylesheet" href="http://pmsipilot.github.io/jquery-highchartTable-plugin/css/prettify.css">
					</head>
					<body>
					<div class="span-one-third">
					<table class="highchart" data-graph-container=".. .. .highchart-container" data-graph-type="line">
              		<caption>%s %s</caption>
              		<thead>
					<tr>
					<th>k</th>
				'''%(t, t1))
		for cat in categories:
			f1.write('\n<th>%s</th>'%cat.title())
		f1.write('\n<th>Total</th>\n</tr>\n</thead>\n<tbody>')
		for i in range(2, 11):
			f = open('%s/%s-%s-%d'%(RESULT_DIR, t, t1, i))
			for cat in categories:
				stats[cat] = 0
			while True:
				temp = f.readline().split()
				if len(temp)== 0:
					break
				if temp[0] == temp[1]:
					stats[temp[0]] += 1
			f1.write('\n<tr>\n<td>%d</td>'%i)
			for cat in categories:
				f1.write('\n<td>%f</td>'%(stats[cat]*100.0/counts[cat]))
				# print i, stats[cat]*1.0/counts[cat]
			acc_sum = sum([c for c in stats.values()])
			f1.write('\n<td>%f</td>\n</tr>'%(acc_sum*100.0/tsum))
		f1.write('''</tbody>
			</table>
			</div>
			<div class="span-two-third">
	            <div class="highchart-container">
	            </div>
          </div>
		</body>''')
		f1.write('''
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/jquery.min.js"></script> 
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/prettify.js"></script>
		    <script>$(function () { prettyPrint() })</script>
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/bootstrap-scrollspy.js"></script>
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/bootstrap-modal.js"></script>
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/highcharts.js"></script> 
		    <script src="https://rawgithub.com/pmsipilot/jquery-highchartTable-plugin/master/jquery.highchartTable.js"></script>
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/jquery.tablesorter.min.js"></script>
		    <script src="http://pmsipilot.github.io/jquery-highchartTable-plugin/js/main.js"></script>
		    ''')
		f1.write('\n</html>')
