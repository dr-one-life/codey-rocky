import codey, event, time
import urequests
import ujson

# Settings
wifi_name = 'yournet'
wifi_password = 'yourpwd'
request_url = 'http://api.openweathermap.org/data/2.5/onecall?lat=50.05&lon=7.07&exclude=hourly&units=metric&appid=your_api_key'

# Initialize variables
# - Weather JSON
weather = ''
# - Selected day
day = 0
# - Weather image / temperature switch
w_mode = 1
# - Max days
max_days = 7

# On Codey start
@event.start
def on_start():
    global wifi_name, wifi_password
    codey.led.show(255, 0, 0)
    # Connect to WiFi network
    codey.wifi.start(wifi_name, wifi_password, codey.wifi.STA)
    while not codey.wifi.is_connected():
        pass
    codey.display.show_image("00003c7e7e3c000000003c7e7e3c0000")
    codey.led.show(0, 255, 21)
    # Update weather information
    update_weather()
    # Show current weather
    show_day()

# On A button pressed - go to previous day
@event.button_a_pressed
def on_button_a_pressed():
    global day, w_mode, max_days
    if day <= 0:
        day = max_days
        w_mode *= -1
    else:
        day -= 1
    show_day()

# On B button pressed - go to next day
@event.button_b_pressed
def on_button_b_pressed():
    global day, w_mode, max_days
    if day >= max_days:
        day = 0
        w_mode *= -1
    else:
        day += 1
    show_day()

# On C button pressed - update weather information
@event.button_c_pressed
def on_button_c_pressed():
    global day, w_mode
    update_weather()
    day = 0
    w_mode = 1
    show_day()

# Show weather for selected day
def show_day():
    global weather, day, w_mode
    codey.led.off()
    src = ''
    if weather != '':
        # Today
        if day == 0:
            src = weather['current']
            temp_val = src['temp']
        # Forecast
        else:
            src = weather['daily'][day-1]
            temp_val = src['temp']['day']
        # Show weather picture
        if w_mode == 1:
            bild = src['weather'][0]['icon'][:2]
            if bild == '01':
                # Sunny
                codey.display.show_image("00000000003844828282443800000000")
            elif bild == '02' or bild == '03':
                # Few clouds
                codey.display.show_image("00182424448484844424241408000000")
            elif bild == '04':
                # Clouds
                codey.display.show_image("00183c3c7cfcfcfc7c3c3c1c08000000")
            elif bild == '10':
                # Rain
                codey.display.show_image("00182526448586844526241408000000")
            elif bild == '09':
                # Shower rain
                codey.display.show_image("00183d3e7cfdfefc7d3e3c1c08000000")
            elif bild == '11':
                # Thunderstorm
                codey.display.show_image("00000000071335589007133558900000")
            elif bild == '13':
                # Snow
                codey.display.show_image("0000000082ab44ba28ba44ab82000000")
            elif bild == '50':
                # Mist
                codey.display.show_image("00444454555515959191929292100000")
        # Show temperature
        else:
            if temp_val >= 0:
                codey.display.show("+" + str(int(temp_val)))
            else:
                codey.display.show(str(int(temp_val)))
    # No weather information available
    else:
        codey.display.show('***')
    # Show day indicator
    codey.display.set_pixel(15, day, True)

# Update weather information
def update_weather():
    global weather, max_days
    weather = get_weather_info()
    # Set max days value
    if weather != '':
        max_days = len(weather['daily'])
    if max_days > 7:
        max_days = 7

# Get weather information (REST API call)
def get_weather_info():
    global request_url
    result = ''
    if not codey.wifi.is_connected():
        return result
    codey.led.show(255, 255, 21)
    resp = urequests.get(request_url)
    if resp.status_code < 299:
        result = resp.json()
        resp.close()
        codey.led.show(0, 255, 21)
        return result
    else:
        resp.close()
        codey.led.show(0, 255, 21)
        return ''
