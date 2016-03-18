## SKO Demo
The SKO Demo will allow you to select a specific client to monitor, then notify you via twitter when that client connects or disconnects from the network. Additionally, it can be configured to work with IFTTT to control lighting, fans, connected coffee makers, set the thermostat on a Nest device, or open & close a connected garage door.

This application is provided "As-is" by Aerohive free of charge. It is intended to demonstrate a capability using the APIs on the Aerohive Cloud Services platform. It is not intended for mission critical applications, and Aerohive does not provide support for this product. You are free to modify, the source code as you see fit, but appliccation usability and security are your responsibility. 

**Security Notice:** For demonstration purposes, the code may use short-cuts that are not acceptable for production-quality code. Things such as storing credentials in the script, passing or storing passwords, access tokens, client secrets, or usernames unincrypted is generally frowned upon. We aren't worried about the security of the demo data, but it would be wise to be security consious when adapting the concepts and ideas from this demo into your own environment or production application.

#### Running the Application:
##### Prerequisites:
The binary package includes all 3rd party libraries necessary to run in any environment. If you choose to make edits to the script and run the .py file, you may need to install the following Python packages:
* requests: http://docs.python-requests.org/en/master/
* twitter: https://github.com/bear/python-twitter/

##### Execution:
In the Binaries folder, execute SKO-Demo. You will be prompted for some information:
```sh
We need your VHM ID and access token to fetch data from your Hive Manager instance.
For information on how to get yours, look here: https://developer.aerohive.com/docs/authentication



VHM information can be obtained from NGs About section.
Please enter your VHM: 
```

Navigate to HiveManager NG and click on 'About'. Here you will see your VHM ID. Type that number into the console, and write it down somewhere you will remember.
![about](https://raw.githubusercontent.com/aerohive/Geofencing/master/ScreenShots/About.tiff)

If you don't already have an access token for the demo apps, now is a good time to set that up. Go to the settings page of Hive Manger, select API Token Management, and click the '+' icon.
![TokenManagement](https://raw.githubusercontent.com/aerohive/Geofencing/master/ScreenShots/GenerateToken.tiff)

After generating an access token (or if you have one already), enter it into the console.
You will then be asked how long you want the demo to run, and how frequently the application should request location data from Aerohive Cloud Services. If you will run the demo for a long period of time, increase the wait period between refreshes to reduce the total number of requests.

The application will now ask you for your twitter handle so that we can mention you.
Note that this application has the keys to the account "@whats_up_home" embedded in it. You can configure the script to use your own twitter account instead by getting keys from http://developer.twitter.com. **Note:** Unless you will be retaining strict control over the application, it is not advisable to store the keys in the application itself. You should encrpyt them and retreive them from secure media when needed.

```sh
I want to be able to send you a message on Twitter when something happens.
What is your Twitter handle? danielororke
Please make sure the device to track is connected to your network.
Press Enter when ready:
```

After pressing enter, the application will query the monitoring APIs for connected clients and present a list. Select the client you want to keep track of:
```sh
OK, great! Checking for clients that are connected...
Requesting: https://cloud-va.aerohive.com/xapi/v1/monitor/clients/?ownerId=1265
Monitoring API response code: 200
1.	DanielsiPhone5S
2.	Daniels-MacBook-Pro
3.	Employee T440
4.	Employee iPhone
```

When you select a client, the application will begin polling for the device's network state. When the person carrying the device walks out of range of the network, you will be notifed via twitter. If you have enabled IFTTT integration by using the Make API, you can set up other API driven actions based on these events such as:
* add a record to a Google sheet
* Turn on or off a light or Fan with WeMo
* Open or close a garage door
* Start a pot of coffee brewing

Many more options are available through the [IFTTT service].

When the device is no longer present, you will see:
```sh
Checking for DanielsiPhone5S. The Time is: 2016-03-17 17:16:03.702792
State Changed. DanielsiPhone5S: Was True. Now False.
```
At this time, a twitter message will be created:
```
"@"+userTwitterName+", "+hostToTrack+" has left the building! #LightsOff 
```
When a user comes back, you will see a similar message on the screen that the connected state is now True, and a twitter message will be posted that the user has entered the building.

Note that #LightsOn and #LightsOff can be used as flags to take action on by any script reading the Twitter feed of @Whats_up_home, or a user you set the script to communicate *from*.

[IFTTT service]: http://iftt.com