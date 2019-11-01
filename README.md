This integration does not use your account credentials. To be able to use it, the following paramters need to be extracted from the API calls.
The integration has been tested with 1 home and 1 or 2 zones. It will probably  work with even more zones, but it will require even more values to be collected.

Guide:
1. Configure an SSL-proxy. In this example mitmproxy has been used in a docker container, but other installation may work as well. Mitmproxy listen on port 8080 for traffic and port 8081 for web-gui. https://medium.com/testvagrant/intercept-ios-android-network-calls-using-mitmproxy-4d3c94831f62
2. Configure your phone to use the proxy (covered in the same guide)
3. On your phone, open your Adax wifi app. Make sure you can see traffic in the mitmproxy gui
4. To be able to use the integration, you must extract from the API calls:
- ```account_id```: Passed in the URL in every call, i.e. zone list https://heater.azurewebsites.net/sheater-client-api/rest/zones/list/{account_id} Can also be found in your Adax app, under Account
- ```heat_signature```: Signature passed as parameter with URL: https://heater.azurewebsites.net/sheater-client-api/rest/zones/{zone_id}/heaters/{account_id}
- temperatures (Signature (passed as parameter) for every temperature used between ```MIN_TEMP``` and ```MAX_TEMP``` set in the parameters). To extract, simple set the temperature to the different values in your app. The last URL parameter represents the temperature:
  - ```0```: 302XXXXXXX (found in api-call https://heater.azurewebsites.net/sheater-client-api/rest/zones/{zone_id}/target_temperature/{account_id}/0)
  - ```12```: 302YYYYYY (found in api-call https://heater.azurewebsites.net/sheater-client-api/rest/zones/{zone_id}/target_temperature/{account_id}/1200)
  - ```13```: 302ZZZZZZZ (found in api-call https://heater.azurewebsites.net/sheater-client-api/rest/zones/{zone_id}/target_temperature/{account_id}/1300)
  - ```14```: 302AAAAAAA (found in api-call https://heater.azurewebsites.net/sheater-client-api/rest/zones/{zone_id}/target_temperature/{account_id}/1400)
  - ```15```: ...
You also need to extract the following values, from any call (fixed values in all calls):
- ```appVersion```
- ```device```
- ```os```
- ```timeOffset```
- ```timeZone```
- ```locale``` (not used when parameters are fetched from iOS devices)
5. Update the parameter section in the files 
- parameters.py
	- ```account_id```
	- ```appVersion```
	- ```device```
	- ```os```
	- ```timeOffset```
	- ```timeZone```
	- ```locale``` (not used when parameters are fetched from iOS devices)
	- ```zone_signature``` (signature from zone URL)
	- ```heat_signature``` (signature from heat URL)
	- ```signature``` for every temperature between ```MIN_TEMP``` and ```MAX_TEMP and 0 (0 is used for turning heaters off)
	- Zone ID. Your zone must replace 123456 in function ```get_signature_123456``` (ie ```get_signature_243569```).
	- You also need to update your zone id in the if-clause under function ```set_param()``` (ie ```elif zone == 123456:``` should be  ```elif zone == 243569:```. Also update the function (line below) to match your lookup function (ie ```get_signature_123456```should be ```get_signature_243569```)
- climate.py (optional)
	- DEFAULT_TEMP (temperature to use when turning heaters on)
6. (Optional) To add multiple zones:
	- Copy the entire function ```get_signature_123456```and update with your second zone (ie ```get_signature_884597```)
	- Add you ```signature``` values for the second zone
	- Add a new if-claues under function ```set_param()```` (make sure to add it in the correct section, iOS or other)
	- Update your zone id in the if-clause under function ```set_param()``` (ie ```elif zone == 123456:``` should be  ```elif zone == 884597:```. Also update the function (line below) to match your lookup function (ie ```get_signature_123456```should be ```get_signature_884597```)
7. Put the folder adax_wifi/ in $CONFIG/custom_components/
8. Add parameters in your configuration.yaml
 ```
 sensor:
   - platform: adax_wifi
   ```
```
 climate:
   - platform: adax_wifi
   ```
9. Add debug logging
 ```
 logger:
   logs:
     custom_components.adax_wifi: debug
```
10. Restart Home Assistant
