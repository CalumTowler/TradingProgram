# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:53:55 2019
@author: Calum
"""
from Stock import Stock

StockTickers = ['SPX','DJI']#,'MSFT','AAPL','GOOGL']#, 'A', 'AA', 'AABA', 'AAC']#, 'AAL', 'AAMC', 'AAME', 'AAN', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AAT', 'AAU', 'AAWW', 'AAXN', 'AB', 'ABB', 'ABBV', 'ABC', 'ABCB', 'ABDC', 'ABEO', 'ABEV', 'ABG', 'ABIL', 'ABIO', 'ABM', 'ABUS', 'AC', 'ACA', 'ACAD', 'ACAMU', 'ACB', 'ACBI', 'ACC', 'ACCO', 'ACER', 'ACET', 'ACGL', 'ACGLO', 'ACGLP', 'ACH', 'ACHC', 'ACHN', 'ACHV', 'ACIA', 'ACIU', 'ACIW', 'ACLS', 'ACM', 'ACMR', 'ACN', 'ACNB', 'ACOR', 'ACP', 'ACRE', 'ACRS', 'ACRX', 'ACST', 'ACTG', 'ACU', 'ACV', 'ACY', 'ADAP', 'ADBE', 'ADC', 'ADES', 'ADI', 'ADIL', 'ADM', 'ADMA', 'ADMP', 'ADMS', 'ADNT', 'ADOM', 'ADP', 'ADRO', 'ADS', 'ADSK', 'ADSW', 'ADT', 'ADTN', 'ADUS', 'ADVM', 'ADX', 'ADXS', 'AE', 'AEB', 'AED', 'AEE', 'AEF', 'AEG', 'AEGN', 'AEHR', 'AEIS', 'AEL', 'AEM', 'AEMD', 'AEO', 'AEP', 'AER', 'AERI', 'AES', 'AETI', 'AEY', 'AEYE', 'AEZS', 'AFB', 'AFC', 'AFG', 'AFGB', 'AFGE', 'AFGH', 'AFH', 'AFHBL', 'AFI', 'AFIN', 'AFINP', 'AFL', 'AFMD', 'AFT', 'AG', 'AGCO', 'AGD', 'AGE', 'AGEN', 'AGFS', 'AGI', 'AGIO', 'AGLE', 'AGM', 'AGMH', 'AGN', 'AGNC', 'AGNCB', 'AGNCM', 'AGNCN', 'AGO', 'AGR', 'AGRO', 'AGRX', 'AGS', 'AGTC', 'AGX', 'AGYS', 'AHC', 'AIMT', 'AIN', 'AINC', 'AINV', 'AIPT', 'AIR', 'AIRG', 'AIRI', 'AIRT', 'AIT', 'AIV', 'AIW', 'AIY', 'AIZ', 'AIZP', 'AJG', 'AJRD', 'AJX', 'AJXA', 'AKAM', 'AKAO', 'AKBA', 'AKCA', 'AKER', 'AKG', 'AKP', 'AKR', 'AKRX', 'AKS', 'AKTS', 'AKTX', 'AL', 'ALAC', 'ALACU', 'ALB', 'ALBO', 'ALCO', 'ALDR', 'ALDX', 'ALE', 'ALEC', 'ALEX', 'ALG', 'ALGN', 'ALGR', 'ALGRU', 'ALGT', 'ALIM', 'ALJJ', 'ALK', 'ALKS', 'ALL', 'ALLE', 'ALLK', 'ALLO', 'ALLT', 'ALLY', 'ALNA', 'ALNY', 'ALO', 'ALOT', 'ALPN', 'ALQA', 'ALRM', 'ALRN', 'ALSK', 'ALSN', 'ALT', 'ALTM', 'ALTR', 'ALV', 'ALX', 'ALXN', 'ALYA', 'AM', 'AMAG', 'AMAL', 'AMAT', 'AMBA', 'AMBC', 'AMBO', 'AMBR', 'AMC', 'AMCI', 'AMCIU', 'AMCN', 'AMCX', 'AMD', 'AME', 'AMED', 'AMEH', 'AMG', 'AMGN', 'AMH', 'AMID', 'AMJ', 'AMJL', 'AMKR', 'AMN', 'AMNB', 'AMOT', 'AMOV', 'AMP', 'AMPE', 'AMPH', 'AMR', 'AMRB', 'AMRC', 'AMRH', 'AMRK', 'AMRN', 'AMRS', 'AMRX', 'AMS', 'AMSC', 'AMSF', 'AMSWA', 'AMT', 'AMTD', 'AMTX', 'AMU', 'AMUB', 'AMWD', 'AMX', 'AMZN', 'AN', 'ANAB', 'ANAT', 'ANCN', 'ANDA', 'ANDAU', 'ANDE', 'ANDX', 'ANET', 'ANF', 'ANFI', 'ANGI', 'ANGO', 'ANH', 'ANIK', 'ANIP', 'ANIX', 'ANSS', 'ANTM', 'ANY', 'AOBC', 'AOD', 'AON', 'AOS', 'AOSL', 'AP', 'APA', 'APAM', 'APC', 'APD', 'APDN', 'APEI', 'APEN', 'APF', 'APH', 'APHA', 'APHB', 'APLE', 'APLS', 'APM', 'APO', 'APOG', 'APOP', 'APPF', 'APPN', 'APPS', 'APRN', 'APT', 'APTO', 'APTS', 'APTV', 'APTX', 'APU', 'APVO', 'APWC', 'APY', 'APYX', 'AQ', 'AQB', 'AQMS', 'AQN', 'AQST', 'AQUA', 'AQXP', 'AR', 'ARA', 'ARAV', 'ARAY', 'ARC', 'ARCB', 'ARCC', 'ARCE', 'ARCH', 'ARCI', 'ARCO', 'ARCT', 'ARCW', 'ARD', 'ARDC', 'ARDS', 'ARDX', 'ARE', 'AREC', 'ARES', 'AREX', 'ARGD', 'ARGO', 'ARGX', 'ARI', 'ARKR', 'ARL', 'ARLO', 'ARLP', 'ARMK', 'ARNA', 'ARNC', 'AROC', 'AROW', 'ARPO', 'ARQL', 'ARR', 'ARRS', 'ARRY', 'ARTNA', 'ARTW', 'ARTX', 'ARVN', 'ARW', 'ARWR', 'ARYA', 'ARYAU', 'ASA', 'ASB', 'ASC', 'ASCMA', 'ASFI', 'ASG', 'ASGN', 'ASH', 'ASIX', 'ASLN', 'ASM', 'ASMB', 'ASML', 'ASNA', 'ASND', 'ASPN', 'ASPS', 'ASR', 'ASRT', 'ASRV', 'ASRVP', 'ASTC', 'ASTE', 'ASUR', 'ASV', 'ASX', 'ASYS', 'AT', 'ATAI', 'ATAX', 'ATEC', 'ATEN', 'ATGE', 'ATH', 'ATHM', 'ATHX', 'ATI', 'ATIS', 'ATKR', 'ATLC', 'ATLO', 'ATMP', 'ATNI', 'ATNM', 'ATNX', 'ATO', 'ATOM', 'ATOS', 'ATR', 'ATRA', 'ATRC', 'ATRI', 'ATRO', 'ATRS', 'ATSG', 'ATTO', 'ATTU', 'ATU', 'ATUS', 'ATV', 'ATVI', 'ATXI', 'AU', 'AUBN', 'AUDC', 'AUG', 'AUMN', 'AUO', 'AUPH', 'AUTL', 'AUTO', 'AUY', 'AVA', 'AVAL', 'AVAV', 'AVB', 'AVCO', 'AVD', 'AVDL', 'AVDR', 'AVEO', 'AVGO', 'AVGR', 'AVH', 'AVID', 'AVK', 'AVLR', 'AVNS', 'AVNW', 'AVP', 'AVRO', 'AVT', 'AVX', 'AVXL', 'AVY', 'AVYA', 'AWF', 'AWI', 'AWK', 'AWP', 'AWR', 'AWRE', 'AWSM', 'AWX', 'AX', 'AXAS', 'AXDX', 'AXE', 'AXGN', 'AXGT', 'AXL', 'AXNX', 'AXO', 'AXP', 'AXR', 'AXS', 'AXSM', 'AXTA', 'AXTI', 'AXU', 'AY', 'AYI', 'AYR', 'AYTU', 'AYX', 'AZN', 'AZO', 'AZPN', 'AZRE', 'AZRX', 'AZUL', 'AZZ']


#for i in StockTickers:   
#    Stocks = Stock(i)
#    Stocks.collect_intraday_data()
#    Stocks.collect_daily_data()
#    time.sleep(10)
#    print("Done with "+str(i))

Ticker = Stock('SPX')
Path = 'WebExtract/StockData/'+Ticker.ticker+'/*.csv'
List = glob.glob(Path)
for i in List:
    Data = pd.read_csv(i)

