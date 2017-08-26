-- init.lua
print('Setting up WIFI...')
wifi.setmode(wifi.STATION)
wifi.sta.config('what_the_hell', 'daiguaCancan')
wifi.sta.connect()

function sayHello()
    srv = net.createConnection(net.TCP, 0)
    srv:connect(8085, "192.168.1.242")
    srv:on("receive", function(sck, c) print(c) end)
    srv:send("Hi, this is NodeMCU")
    end
    

function reportTempAndHumi()
    pin = 1
    local status, temp, humi , temp_dec, humi_dec = dht.read11(pin)
    srv = net.createConnection(net.TCP, 0)
    srv:connect(8085, "192.168.1.242")
    data = ""
    data = "Temperature: " .. temp .. "." .. temp_dec .. "*C\n"
    data = data .. "Humidity: " .. humi .. "." .. humi_dec .. "%"
    srv:send(data)
    end

tmr.alarm(1, 1000, tmr.ALARM_AUTO, function()
    if wifi.sta.getip() == nil then
        print('Waiting for IP ...')
    else
        print('IP is ' .. wifi.sta.getip())
        sayHello()
        tmr.stop(1)
    end
end)


tmr.alarm(2, 20 * 1000, tmr.ALARM_AUTO, function()
    reportTempAndHumi()
    --tmr.stop(2)
end)
