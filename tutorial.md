# Set up tutorial for Elastic Search

## 1. build enbvironment
```
docker compose up -d
```
Then, you can access to http://localhost:5601/ 
When you access it, you can wathc the interface below.
![img](tutorial/token_screen.png)


## 2. get token code
```
docker exec demo-elasticsearch bin/elasticsearch-create-enrollment-token --scope kibana
```
Then, you can get the token code.
When you paste it to the interface, the screen will change like below.

![img](tutorial/verification_code.png)

## 3. get verification code
```
docker exec demo-kibana bin/kibana-verification-code
```
Then, you can get the verification code.
When you fill it to the screen, you will see the login screen like below.

![img](tutorial/login.png)

## 4. reset password
```
docker exec -it demo-elasticsearch bin/elasticsearch-reset-password -u elastic
```
Then, you can get new password and now you can login.
Username: elastic
Password: the result by the command above.
