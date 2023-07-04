# fundCheck

```python
import requests
import json

# data
# name
# jzrq
# dwjz
# gsz
# zszzl
# gztime

#        code      ownVal  ownAmount  fakeName
myFunds = [
        ['013195', 0.6790, 8836.34,   "car 1    "],
        ['014605', 0.9338, 1285.07,   "light    "]
    ]

toUpdate = []

def getFundData(fundCode) -> dict:
    responser = requests.get(f"http://fundgz.1234567.com.cn/js/{fundCode}.js")
    jsonStr = responser.text
    jsonStr = jsonStr[8:]
    jsonStr = jsonStr[:-2]
    data = json.loads(jsonStr)
    return data

def deltaFloat(aimFloat, roundCount, limit = 0):
    res = f"{round(aimFloat, roundCount)}"
    if aimFloat >= 0:
        if res[0] != '-':
            res  = '+' + res
    while len(res) < limit:
        res += ' '
    return res

def debugData():
    for fund in myFunds:
        fakeName        = fund[3]
        data            = getFundData(fund[0])
        fundName        = data["name"]
        lastRealValDate = data["jzrq"]
        lastRealVal     = data["dwjz"]
        estVal          = data["gsz"]
        estValDelta     = data["gszzl"]
        estValTime      = data["gztime"]
        print(f"{fakeName}, {lastRealVal}, {lastRealValDate}, {estVal}, {estValDelta}. {estValTime}")

def fixLengthStr(originalStr, length):
    res = originalStr
    if len(res) > length:
        return res[:length]
    while len(res) < length:
        res += ' '
    return res

#{fixLengthStr("TIME", 9)}

def formalPrint():
    print(f"{fixLengthStr('NAME', 9)}  |  {fixLengthStr(' VDA(%)', 9)}  {fixLengthStr(' VDT(%)', 9)}  |  {fixLengthStr(' MDA(Y)', 9)}  {fixLengthStr(' MDT(Y)', 9)}  |  {fixLengthStr('TIME', 9)}")
    moneyDeltaAllCount   = 0.0
    moneyDeltaTodayCount = 0.0
    fundCostALL          = 0.0
    lastFundValALL       = 0.0
    for fund in myFunds:
        data            = getFundData(fund[0])
        fundName        = data["name"]
        fakeName        = fund[3]
        lastRealVal     = float(data["dwjz"])
        valDeltaAll     = (float(data["gsz"]) - fund[1]) * 100 / fund[1]
        valDeltaToday   = float(data["gszzl"])
        moneyDeltaAll   = (float(data["gsz"]) - fund[1]) * fund[2]
        moneyDeltaToday = (float(data["gsz"]) - lastRealVal) * fund[2]
        updateTime      = data["gztime"]
        print(f"{fixLengthStr(fakeName, 9)}  |  {deltaFloat(valDeltaAll, 4, 9)}  {deltaFloat(valDeltaToday, 4, 9)}  |  {deltaFloat(moneyDeltaAll, 2, 9)}  {deltaFloat(moneyDeltaToday, 2, 9)}  |  {fixLengthStr(updateTime, 16)}")
        moneyDeltaAllCount   += moneyDeltaAll
        moneyDeltaTodayCount += moneyDeltaToday
        fundCostALL          += fund[1] * fund[2]
        lastFundValALL       += lastRealVal * fund[2]
    moneyDeltaALLRatio   = (moneyDeltaAllCount / fundCostALL) * 100
    moneyDeltaTodayRatio = (moneyDeltaTodayCount / lastFundValALL) * 100
    print(f"{fixLengthStr('ALL', 9)}  |  {deltaFloat(moneyDeltaALLRatio, 2, 9)}  {deltaFloat(moneyDeltaTodayRatio, 2, 9)}  |  {deltaFloat(moneyDeltaAllCount, 2, 9)}  {deltaFloat(moneyDeltaTodayCount, 2, 9)}  |  {fixLengthStr('---', 16)}")
    if len(toUpdate) > 0:
        updateStr = "\nTO UPDATE :"
        for updateFundName in toUpdate:
            updateStr += f" {updateFundName}"
        print(updateStr)

formalPrint()
# debugData()
```

如有侵权请联系treat@qq.com