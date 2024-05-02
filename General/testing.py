import numpy as np
import math
class Trader:
  def BSM(self,timestamp):
        T=(int((timestamp))/(100*10000))
        d1=np.log(9989/10000)+(((0.16)**2)/2)*T
        self.d1=abs(float(d1)/(0.16)*float(np.sqrt(T)))
        self.d2=abs(float(self.d1)-(float(0.16)*float(np.sqrt(T))))
        print(f"d1:{self.d1}")
        print(f"d2:{self.d2}")
  def C(self):
        self.coupon_fair=((9989*(0.5 * (1 + math.erf(self.d1 / math.sqrt(2)))))-(10000*(0.5 * (1 + math.erf(self.d1 / math.sqrt(2))))))
        print(f"coupon_fair:{self.coupon_fair}")
trader = Trader()
print(trader.BSM(500))   
print(trader.C() )    
