from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from matplotlib import pyplot as plt

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# DynamoDB resource determination. Change region name based on which region the table is on
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

# The name of the table, change based on table
table = dynamodb.Table('sensor_receiver_test')
# the sensor number, change based on sensor data desired. with the quotes it is a string, but other tables use a number
# simply remove the quotes for a number
sensor = '2'
sensordata = 'Temp'  # the name of the data to be projected
primaryKey = 'Row'  # The primary key of the table, the name of the first column
secondaryKey = 'PositionInRow'  # the secondary key of the table, the name of the 2nd column
# Amazon database service calls these the Sort key and partition key respectively
print(sensordata + " Sensor Data")

response = table.query(
    KeyConditionExpression=Key(primaryKey).eq(sensor)
)

xaxis = []
yaxis = []
# 'payload' is the name of the 3rd column in the table that was used for testing.
# other tables, such as humidity are simply called humidity with the data inside
# in such cases, payload can just be deleted along with its brackets
for i in response['Items']:
    print(i[primaryKey], ":", i[secondaryKey], ":", i['payload'][sensordata])
    xaxis.append(float(i[secondaryKey]))
    yaxis.append(float(i['payload'][sensordata]))

# ensures the numbers are in order and matched to their respective values in order
z = [yaxis for _,yaxis in sorted(zip(xaxis,yaxis))]
xaxis.sort()

plt.plot(xaxis, z, 'ro')  # plots the data, 'ro' means read dots to plot, can be changed as desired
plt.ylabel(sensordata)
plt.xlabel('Reading')
plt.title('Sensor' + sensor)
plt.xticks(range(0, int(xaxis[-1]) + 1))  # makes sure each tick mark is shown.
plt.show()  # shows the plot

