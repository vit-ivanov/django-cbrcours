=====
CBR course (cbr.ru)
=====

Quick start
-----------
1. Install `pip install -e git://github.com/myarik/django-cbrcours.git#egg=cbrcours`

2. Add "myblog" to INSTALLED_APPS:
 ```
  INSTALLED_APPS = {
    ...
    'cbrcours'
  }
 ```
  
3. Run `python manage.py syncdb` to create cbrcour's models or `python manage.py migrate`.

4. Get cours:
    ```
    from cbrcurrencies import get_course
    get_course('USD')
    ```

5.  Convert price:
    ```
    from cbrcurrencies import conver_price
    conver_price(526, 'EUR')
    ``` 
