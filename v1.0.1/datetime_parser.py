import datetime
timestamp = "1628235491618"
print(datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime("%Y-%m-%d %H:%M:%S"))