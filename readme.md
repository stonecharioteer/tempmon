# tempmon

This is a project consisting that uses Raspberry Pis and NodeMCUs.

I'm making it to showcase how IoT could be used around a normal office. Due to time constraints, the first version is simple enough.

## APIs
Each of the components of this project has separate APIs, depending on how they can be coded.

### NodeMCU API

* /whoami - GET
    This is a request that returns a simple JSON:

    ```
    {
        "id": ID, # an integer.
        "type": "nodemcu"
    }
    ```
* /temperature - GET

* /humidity - GET

### enviropi

* /whoami - GET

    ```
    {
        'id': ID, # an integer
        'type': "enviropi"
    }
    ```

* /temperature - GET
* /pressure - GET
* /light - GET
* /light - POST 

### sensehat

* /whoami - GET

    ```
    {
        "id": ID, # an integer
        "type": "sensehat"
    }
    ```

* /temperature
* /humidity
* /pressure
* /show_message - POST


### tempmonpi

* /whoami
* /tempmon
* /sensehatpi
* /enviropi
* /admin



