-- switch.lua
print('Setting up WIFI...')
station_config = {}
station_config.ssid = "xiaoou"
station_config.pwd = "123456789"
wifi.setmode(wifi.STATION)
wifi.sta.config(station_config)
wifi.sta.connect()

tcpS = net.createServer(net.TCP, 10)
gpio.mode(1, gpio.OUTPUT)


function switch(command)
    if command == "on" then
        gpio.write(1, gpio.LOW)
        return "on"
    else
        gpio.write(1, gpio.HIGH)
        return "off"
    end
end

function sayHelloToManager(json)
    srv = net.createConnection(net.TCP, 0)
    srv:connect(22223, "192.168.12.1")
    srv:send(json)
    srv:on("receive", function(sck, c) 
        print(c) 
        recvJson = sjson.decode(c)
        if recvJson.cmd_ans == true and recvJson.log_ans == true and recvJson.equip == 'switch002' then
            return true
        else 
            sayHelloToManager(json)
        end
    end)
end

function buildJSON(ip)
    msgtable = {}
    msgtable.ip = ip
    msgtable.cmd = ""
    msgtable.log = "up"
    msgtable.repo = "xjhuang"
    msgtable.equip = "switch003"
    msgtable.imname = "hfv/switch:v2.0"
    
    ok, json = pcall(sjson.encode, msgtable)
    if ok then
        print(json)
        return json
    else
        print("failed to encode!")
    end
end

tmr.alarm(1, 1000, tmr.ALARM_AUTO, function()
    if wifi.sta.getip() == nil then
        print('Waiting for IP ...')
    else
        print('IP is ' .. wifi.sta.getip())
        json = buildJSON(wifi.sta.getip())
        sayHelloToManager(json)
        tmr.stop(1)
    end
end)

if tcpS then
    tcpS:listen(8085, function(conn)
        conn:on("receive", function(c, data)
            print(data)
            c:send(switch(data))
        end)
        conn:on("disconnection", function(c, d) print("disconnect") end)
    end)
end
