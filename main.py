from requests import *
from datetime import datetime
from smtplib import *

MY_LAT = 22.804565
MY_LONG = 86.202873
MY_EMAIL = "kg180205@gmail.com"
MY_PASSWORD = "Todoroki123#"


def is_overhead():
    response = get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()
    iss_longitude = (data["iss_position"]["longitude"])
    iss_latitude = (data["iss_position"]["latitude"])

    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        return True


def n_o_d():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    time_now = datetime.now()
    response = get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = ((data["results"]["sunrise"]).split("T"))[1].split(":")[0]
    sunset = ((data["results"]["sunset"]).split("T"))[1].split(":")[0]

    if sunset <= time_now <= sunrise:
        return True


if is_overhead() and n_o_d():
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:Happy Birthday!\n\n The International Space Station is right above you. Go "
                                f"out"
                                f"and see you might be able to see it.")
