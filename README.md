# Sock-shop_load

Commands
```
.\venv\Scripts\activate
```
```
locust -f locust_slave.py --host http://10.161.2.161:30001 --user 20 --spawn-rate 1 --headless
```
or
```
python -m locust -f locust_slave.py --host http://10.161.2.161:30001 --user 20 --spawn-rate 1 --headless
```
Only user rate of 1 is allowed to prevent multiple users sharing the same account
