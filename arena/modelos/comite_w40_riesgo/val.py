import sys; sys.path.insert(0,'/home/user/New1')
from herramientas.parametros import parametros_efectivos
from herramientas.riesgo import validar_orden, tamano_por_stop, tamano_vol_objetivo, kelly_fraccional
p=parametros_efectivos('arena_agresivo'); fx=18.145
print('riesgo', p['riesgo_por_operacion'], 'kelly',p['kelly'],'bruto',p['apalancamiento'])
print(tamano_por_stop(20441.67,150.88,134.40,tipo_cambio=fx,parametros=p))
print(tamano_por_stop(10000,150.88,134.40,tipo_cambio=fx,parametros=p))
# vol: UPRO ~3*16%=48%; vol objetivo de la manga 3x tal que DD 4m 2sigma = 12% de la cuenta → sigma4m 6% → anual 10.5%
print(tamano_vol_objetivo(20441.67,0.105,0.48,peso_max=0.5))
pf={'capital':20441.67,'fase':1,'posiciones':{'SPYM':{'valor_mxn':5*90.6*fx,'clase':'etf','subclase':'indice'},'QQQM':{'valor_mxn':5601.18,'clase':'etf','subclase':'indice'}}}
print(validar_orden(pf,{'ticker':'UPRO','lado':'compra','cantidad':2,'precio':150.88,'tipo_cambio':fx,'clase':'etf','subclase':'apalancado','tactica':True,'stop':134.40},p))
pr={'capital':10000,'fase':1,'posiciones':{'SPYM':{'valor_mxn':3*90.6*fx,'clase':'etf','subclase':'indice'}}}
print(validar_orden({'capital':10000,'fase':1,'posiciones':{}},{'ticker':'SPYM','lado':'compra','cantidad':3,'precio':90.6,'tipo_cambio':fx,'clase':'etf','subclase':'indice'},p))
print(validar_orden(pr,{'ticker':'UPRO','lado':'compra','cantidad':1,'precio':150.88,'tipo_cambio':fx,'clase':'etf','subclase':'apalancado','tactica':True,'stop':134.40},p))
