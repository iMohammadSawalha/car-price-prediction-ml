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


`brand(الشركة المصنعة)`: `@String`, Cars Brand

`model(موديل السيارة)`: `@String`, Cars Model

`year(سنة الانتاج)`: `@Number`, Cars Release Year

`fuel_type(نوع الوقود)`: `@String`, Cars Fuel Type .e.g: بنزين, ديزل

`vehicle_history(أصل السيارة)`: `@String`, Cars History .e.g: خصوصي, عمومي

`licence(رخصة السيارة)`: `@String`, Cars Licence .e.g: فلسطينية , نمرة صفراء

`transmission_type(نوع الجير)`: `@String`, Cars Transmission .e.g: عادي, اوتوماتيك

`windows_type(الشباك)`: `@String`, Cars Winodws .e.g: الكتروني, يدوي

`engine_capacity(سعة المحرك)`: `@Number`, Cars Engine Capacity (cc)

`kilometers_driven(عداد السيارة)`: `@Number`, Cars Driven Kilometers (km)

`seats(عدد كراسي السيارة)`: `@Number/String`, Cars Number of Seats .e.g: 4 + 1, 5 ...

`payment_method(طريقة الدفع)`: `@String`, Payment Method .e.g:  نقدا فقط, إمكانية التقسيط

`previous_owners(اصحاب سابقون)`: `@Number/String`, Number of Previous Owners

`radio(يوجد راديو)`: `@Number`, If car has Radio give value (1) if not give (0)

`air_conditioner(يوجد مكيف)`: `@Number`, If car has Air Conditioner give value (1) if not give (0)

`central_lock(يوجد اغلاق مركزي)`: `@Number`, If car has Central Lock give value (1) if not give (0)

`airbag(يوجد وسادة هوائية)`: `@Number`, If car has Airbag give value (1) if not give (0)

`alert_system(يوجد جهاز انذار)`: `@Number`, If car has Alert System give value (1) if not give (0)

`leather_seats(يوجد مقاعد جلد)`: `@Number`, If car has Leather Seats give value (1) if not give (0)

`sunroof(فتحة سقف)`: `@Number`, If car has Sunroof give value (1) if not give (0)

`panoramic sunroof(سقف بانوراما)`:  `@Number`, If car has Panoramic Sunroof give value (1) if not give (0)
