-- waterSensor.lua
print('Setting up WIFI...')
station_config = {}
station_config.ssid = "xiaoou"
station_config.pwd = "123456789"
wifi.setmode(wifi.STATION)
wifi.sta.config(station_config)
wifi.sta.connect()

tcpS = net.createServer(net.TCP, 1)
gpio.mode(1, gpio.OUTPUT)


function water_depth()
    return adc.read(0)
end

function sayHelloToManager(json)
    srv = net.createConnection(net.TCP, 0)
    srv:connect(22223, "192.168.12.1")
    srv:send(json)
    srv:on("receive", function(sck, c) 
        print(c) 
        recvJson = sjson.decode(c)
        if recvJson.cmd_ans == true and recvJson.log_ans == true and recvJson.equip == 'waterSensorv2.0' then
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
    msgtable.equip = "waterSensorv2.0"
    msgtable.imname = "hfv/depth:v2.0"
    
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
            c:send(water_depth())
        end)
        conn:on("disconnection", function(c, d) print("disconnect") end)
    end)
end
