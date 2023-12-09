## Car Price Prediction ML Assignment

To run this app you would need to install the following using `pip install`:

```
scikit-learn
scipy
numpy
pandas
flask
```

Then you can explore the notebooks and test each block by your self

If you want to test the API, you can run the `server.py`  and go to the endpoint `/predict `and send the data as JSON format using `POST` method

Here are the params that you can send in the POST body:


`brand`: `@String`, Cars Brand

`model`: `@String`, Cars Model

`year`: `@Number`, Cars Release Year

`fuel_type`: `@String`, Cars Fuel Type .e.g: بنزين, ديزل

`vehicle_history`: `@String`, Cars History .e.g: خصوصي, عمومي

`licence`: `@String`, Cars Licence .e.g: فلسطينية , نمرة صفراء

`transmission_type`: `@String`, Cars Transmission .e.g: عادي, اوتوماتيك

`windows_type`: `@String`, Cars Winodws .e.g: الكتروني, يدوي

`engine_capacity`: `@Number`, Cars Engine Capacity (cc)

`kilometers_driven`: `@Number`, Cars Driven Kilometers (km)

`seats`: `@Number/String`, Cars Number of Seats .e.g: 4 + 1, 5 ...

`payment_method`: `@String`, Payment Method .e.g:  نقدا فقط, إمكانية التقسيط

`previous_owners`: `@Number/String`, Number of Previous Owners

`radio`: `@Number`, If car has Radio give value (1) if not give (0)

`air_conditioner`: `@Number`, If car has Air Conditioner give value (1) if not give (0)

`central_lock`: `@Number`, If car has Central Lock give value (1) if not give (0)

`airbag`: `@Number`, If car has Airbag give value (1) if not give (0)

`alert_system`: `@Number`, If car has Alert System give value (1) if not give (0)

`leather_seats`: `@Number`, If car has Leather Seats give value (1) if not give (0)

`sunroof`: `@Number`, If car has Sunroof give value (1) if not give (0)

`panoramic sunroof`:  `@Number`, If car has Panoramic Sunroof give value (1) if not give (0)
