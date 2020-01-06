import quandl

quandl.ApiConfig.api_key = 'dK3_BFEhqi_zGsM1n1hW'
data = quandl.get("EIA/PET_RWTC_D", returns="numpy")
print(data)
print(len(data))