-- init.lua
print('Setting up WIFI...')
wifi.setmode(wifi.STATION)
wifi.sta.config('what_the_hell', 'daiguaCancan')
wifi.sta.connect()

tcpS = net.createServer(net.TCP, 10)

gpio.mode(1, gpio.OUTPUT)

function switch(command)
    if command == "HIGH" then
        gpio.write(1, gpio.HIGH)
    else 
        gpio.write(1, gpio.LOW)
    end
end

tmr.alarm(1, 1000, tmr.ALARM_AUTO, function()
    if wifi.sta.getip() == nil then
        print('Waiting for IP ...')
    else
        print('IP is ' .. wifi.sta.getip())
        tmr.stop(1)
    end
end)

if tcpS then
    tcpS:listen(8085, function(conn)
        conn:on("receive", function(c, data)
            print(data)
            c:send("ok")
            switch(data)
        end)
        conn:on("disconnection", function(c, d) print("disconnect") end)
    end)
end
