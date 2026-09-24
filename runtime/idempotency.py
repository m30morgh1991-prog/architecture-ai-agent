class IdempotencyGuard:
 def __init__(self): self._completed={}
 def check(self,key): return self._completed.get(key)
 def store(self,key,result):
  if key in self._completed: return self._completed[key]
  self._completed[key]=result; return result
