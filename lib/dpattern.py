from gapbide import Gapbide
class DP(object):
	def __init__(self, min_sup):
		self.min_sup = min_sup

	def compose(self, dp, p):
		for k,v in p.iteritems():
			try:
				dp[k] += v
			except:
				dp[k] = v
		return dp

	def d_patterns(self, doc):
			if len(doc) > 1:
				min_sup = 2 if self.min_sup*len(doc) < 1 else self.min_sup*len(doc)
				sp = Gapbide(doc, min_sup, 0, 0).run()
			else:
				sp = doc
			print len(sp)
			dp = {}
			for pat in sp:
				p = {}
				for t in pat:
					p[t] = 1
				dp = self.compose(dp, p)
			return dp
